"""Preserve and prepare a compatible, bounded Bold hamza-above repair."""
from pathlib import Path
import hashlib,json,re,shutil,xml.etree.ElementTree as ET,plistlib
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'candidate.json').exists(), 'Do not overwrite retained evidence'
prev=R/'agent-proofs/cases/arabic-002';m=json.loads((prev/'applied.json').read_text())
expected=dict(m['source_hashes']);expected.update({g['path']:g['candidate_sha256'] for g in m['glyphs']})
assert all(sha(R/p)==h for p,h in expected.items()), 'Sources changed; inspect first'
font=R/'fonts/variable/VirtuaGrotesk[wght].ttf';assert sha(font)==sha(prev/'assets/after.ttf')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(font,C/'assets/before.ttf');shutil.copy2(prev/'assets/Virtua-OFL.txt',C/'assets/Virtua-OFL.txt')
rel=Path('sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif');p=R/rel;before=p.read_text();assert '<string>red</string>' in before
# Same 31-point contour and segment types as Regular. Square bounded turns,
# a flat base bar, fixed-size terminal chamfers and an open right aperture.
xy=[(-16,816),(240,816),(256,832),(256,888),(240,904),(136,904),
 (104,904),(88,920),(88,952),(88,976),(96,984),(120,984),
 (144,984),(152,976),(152,952),(160,944),(192,944),(208,960),
 (208,1024),(176,1056),(112,1056),(48,1056),(16,1024),(16,960),
 (16,928),(24,928),(40,912),(40,904),(-16,904),(-32,888),(-32,832)]
pts=list(ET.fromstring(before).findall('outline/contour/point'));assert len(pts)==len(xy)
index=iter(xy)
def point(m):
 x,y=next(index);return re.sub(r'x="[^"]+" y="[^"]+"',f'x="{x}" y="{y}"',m.group())
after=re.sub(r'<point [^>]+/>',point,before)
for name,y in [('bottom',816),('bottomDots',816),('topDots',1056),('top',1104)]:
 after=re.sub(rf'(<anchor name="{name}" x="112" y=")[^"]+("/>)',rf'\g<1>{y}\2',after)
after=after.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
regular=R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif'
a=ET.fromstring(after);b=ET.parse(regular).getroot();assert [p.get('type') for p in a.findall('outline/contour/point')]==[p.get('type') for p in b.findall('outline/contour/point')]
for state,s in [('before-sources',before),('candidate-sources',after)]:
 q=C/state/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s)
q=C/'before-sources'/regular.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(regular,q)
folder=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';contents=plistlib.loads((folder/'contents.plist').read_bytes());roots={n:ET.parse(folder/f).getroot() for n,f in contents.items()};affected={'hamzaabove-ar'}
while True:
 more={n for n,r in roots.items() if any(x.get('base') in affected for x in r.findall('outline/component'))}
 if more<=affected:break
 affected|=more
for n in affected:
 assert '0.09,0.72,0.44,1' not in ET.tostring(roots[n],encoding='unicode'),f'Protected dependency {n}'
manifest={'baseline_case':'arabic-002','source_hashes':expected,'glyphs':[{'name':'hamzaabove-ar','path':str(rel),'before_sha256':sha(p),'candidate_sha256':sha(C/'candidate-sources'/rel)}],'dependent_source_glyphs':sorted(affected),'regular_sha256':sha(regular),'construction':{'bounds':[-32,816,256,1056],'base_bar':88,'outer_upper_turn':[96,96,64,64],'inner_upper_turn':[32,32,24,24],'inner_lower_turn':[48,48,32,32],'aperture_min_vertical':40,'terminal_chamfer':16,'inner_cut':8}}
(C/'candidate.json').write_text(json.dumps(manifest,indent=2)+'\n')
scratch=R/'out/qa/arabic-003/sources';scratch.mkdir(parents=True,exist_ok=True)
for master in ['Regular','Bold']:
 shutil.copytree(R/f'sources/VirtuaGrotesk-{master}.ufo',scratch/f'VirtuaGrotesk-{master}.ufo',dirs_exist_ok=True)
shutil.copy2(C/'candidate-sources'/rel,scratch/'VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif')
print('Prepared one Bold draft; active sources unchanged; dependencies:',len(affected))
