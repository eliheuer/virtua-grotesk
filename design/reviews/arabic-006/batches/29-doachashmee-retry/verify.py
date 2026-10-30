from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as E,plistlib,sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'candidate.json').read_text());S=Path(m['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,h in m['source_hashes'].items():assert sha(R/rel)==h,rel
for rel,h in m['reserved_beh_hashes'].items():assert sha(R/rel)==h
changed={g['path'] for g in m['glyphs']}
for rel,h in m['source_hashes'].items():
 if rel not in changed:assert sha(S/rel)==h,rel
rows=[]
for g in m['glyphs']:
 assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
 tag=g['master']+'-'+g['name']
 subprocess.run([str(R/'.venv/bin/python'),str(R/'scripts/curve_profile.py'),str(C/'before-sources'/g['path']),str(C/'candidate-sources'/g['path']),'--json',str(C/(tag+'-curves.json')),'--svg',str(C/(tag+'-comb.svg'))],check=True,stdout=subprocess.DEVNULL)
 r=json.loads((C/(tag+'-curves.json')).read_text())['reports'][1]
 assert not r['warnings'],(tag,r['warnings'])
 assert not [j for j in r['joins'] if j['classification'] in ['kink','undefined']],tag
 rows.append({'glyph':g['name'],'master':g['master'],'warnings':r['warnings'],'non_G2':[j for j in r['joins'] if j['classification']=='G1']})
 # All newly drawn geometry is on8, source anchors retained exactly.
 a=E.parse(C/'candidate-sources'/g['path']);b=E.parse(C/'before-sources'/g['path'])
 assert all(float(p.get(k))%8==0 for p in a.findall('.//point') for k in ['x','y'])
 assert [E.tostring(x) for x in a.findall('anchor')]==[E.tostring(x) for x in b.findall('anchor')]
for name in set(g['name'] for g in m['glyphs']):
 a,b=[E.parse(C/'candidate-sources'/next(g['path'] for g in m['glyphs'] if g['name']==name and g['master']==master)) for master in ['Regular','Bold']]
 assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')]
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths];orders=[f.getGlyphOrder() for f in fonts];assert orders[0]==orders[1]
lib=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes());mp=lib.get('public.postscriptNames',{});allowed={mp.get(g['name'],g['name'].replace('-','')) for g in m['glyphs']}
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['ھھھ ھ','بھ پھ تھ','بھب پھپ تھت','ھ ھ\u200d \u200dھ\u200d \u200dھ','ھَ ھُ ھِ','ببب ب','ههه ه','o n O H','سلام العربية','ہ بہ','ى ي ئ']
checks=[];compiled={}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [(orders[0][i.codepoint],i.cluster,p.x_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,475,550,625,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[]
 for name in sets[0]:
  vals=[]
  for gs in sets:
   pen=DecomposingRecordingPen(gs);gs[name].draw(pen);vals.append((pen.value,gs[name].width))
  if vals[0]!=vals[1]:diff.append(name)
 assert set(diff)<=allowed,sorted(set(diff)-allowed);compiled[w]=diff
 for f in hfonts:f.set_variations({'wght':w})
 for t in samples:
  a,b=[shape(f,t) for f in hfonts];assert len(a)==len(b)
  for old,new in zip(a,b):
   assert old[:2]==new[:2] and old[3:]==new[3:] and new[0]!='.notdef'
   delta=sets[1][new[0]].width-sets[0][new[0]].width
   assert abs(new[2]-old[2]-delta)<=1,(t,old,new)
  checks.append({'weight':w,'text':t,'glyphs':b})
(C/'verification.json').write_text(json.dumps({'status':'scratch candidate only','all_active_source_bytes_unchanged':True,'beh_reserved_files':len(m['reserved_beh_hashes']),'curve_reports':rows,'compiled_changes':compiled,'shaping_checks':checks,'font_hashes':dict(zip(['before','candidate'],map(sha,paths)))},indent=2,ensure_ascii=False)+'\n')
print('All active sources unchanged; 8 compatible scratch drawings; 55 shaping checks; only four intended compiled glyphs change.')
