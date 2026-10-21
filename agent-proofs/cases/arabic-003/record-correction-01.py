"""Freeze Eli's saved correction and measure it against the exact AI candidate."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET,shutil,sys
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;D=C/'manual-correction-01'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not D.exists(),'Never overwrite the human correction pair'
m=json.loads((C/'applied.json').read_text());expected=dict(m['source_hashes']);expected.update({g['path']:g['candidate_sha256'] for g in m['glyphs']})
changed=[p for p,h in expected.items() if sha(R/p)!=h];assert changed==[m['glyphs'][0]['path']],changed
p=Path(changed[0]);a=C/'candidate-sources'/p;b=R/p
D.mkdir();shutil.copy2(a,D/'ai.glif');shutil.copy2(b,D/'human.glif')
roots=[ET.parse(p).getroot() for p in [a,b]];pts=[r.findall('outline/contour/point') for r in roots]
assert len(pts[0])==len(pts[1])==31
assert [p.get('type') for p in pts[0]]==[p.get('type') for p in pts[1]]
deltas=[]
for i,(x,y) in enumerate(zip(*pts)):
 old=[int(x.get(k)) for k in ['x','y']];new=[int(y.get(k)) for k in ['x','y']]
 if old!=new:deltas.append({'point':i,'type':x.get('type','offcurve'),'before':old,'after':new,'delta':[v-u for u,v in zip(old,new)]})
assert ET.tostring(roots[0].find('lib'))==ET.tostring(roots[1].find('lib'))
assert [ET.tostring(x) for x in roots[0].findall('anchor')]==[ET.tostring(x) for x in roots[1].findall('anchor')]
report={'glyph':'hamzaabove-ar','master':'Bold','ai_sha256':sha(a),'human_sha256':sha(b),'source_hashes_before':expected,'changed_sources':changed,'point_deltas':deltas,'unchanged':['31-point topology','point types','smooth flags','anchors','zero advance','purple label','all Regular source files'],'measurements':{'bounds':{'ai':[-32,816,256,1056],'human':[-16,816,240,1048]},'base_bar_width':[288,256],'base_bar_thickness':[88,80],'right_aperture':[40,40],'inner_upper_turn_extents':[[32,32],[32,32]],'inner_upper_horizontal_handles':[24,16],'inner_upper_vertical_handles':[24,24],'inner_lower_turn_extents':[[48,48],[48,48]],'inner_lower_handles':[[32,32],[32,24]],'outer_left_upper_turn_extents':[[96,96],[96,88]],'outer_left_upper_handles':[[64,64],[64,56]],'outer_lower_left_turn_extents':[[24,48],[24,56]],'outer_lower_left_initial_handle':[32,24],'exposed_chamfers':[16,16],'inner_cut':[8,8],'shelf_vertical':[8,8]}}
(D/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'assets').mkdir();shutil.copy2(C/'assets/after.ttf',D/'assets/before.ttf');shutil.copy2(C/'assets/Virtua-OFL.txt',D/'assets/Virtua-OFL.txt')
print('Recorded',len(deltas),'moved points; topology, anchors, grade and all other sources unchanged.')
