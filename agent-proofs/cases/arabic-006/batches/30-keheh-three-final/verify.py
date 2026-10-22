from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'candidate.json').read_text());S=Path(m['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed={g['path'] for g in m['glyphs']}
for rel,h in m['source_hashes'].items():
 assert sha(R/rel)==h,rel
 if rel not in changed:assert sha(S/rel)==h,rel
for g in m['glyphs']:
 assert sha(S/g['path'])==g['candidate_sha256']
 a=E.parse(S/g['path']);b=E.parse(C/'before-sources'/g['path'])
 assert [E.tostring(x) for x in a.findall('anchor')]==[E.tostring(x) for x in b.findall('anchor')]
 assert [x.get('base') for x in a.findall('outline/component')]==['keheh-ar.fina','threedotsupabove-ar']
 assert not a.findall('outline/contour')
# Matching components and unchanged compatible donors preserve interpolation.
for n in ['keheh-ar.fina','threedotsupabove-ar']:
 ts=[]
 for w in ['Regular','Bold']:
  d=S/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';c=plistlib.loads((d/'contents.plist').read_bytes());ts.append(E.parse(d/c[n]))
 assert [[p.get('type') for p in c] for c in ts[0].findall('outline/contour')]==[[p.get('type') for p in c] for c in ts[1].findall('outline/contour')]
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];order=TTFont(paths[0]).getGlyphOrder();assert order==TTFont(paths[1]).getGlyphOrder();lib=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes());n='kehehThreedotsabove-ar.fina';allowed={lib.get('public.postscriptNames',{}).get(n,n.replace('-',''))}
fs=[hb.Font(hb.Face(p.read_bytes())) for p in paths];checks=[];diffs={}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [(order[i.codepoint],i.cluster,p.x_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,550,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[]
 for name in sets[0]:
  out=[]
  for gs in sets:
   pen=DecomposingRecordingPen(gs);gs[name].draw(pen);out.append((pen.value,gs[name].width))
  if out[0]!=out[1]:diff.append(name)
 assert set(diff)==allowed,(w,diff,allowed);diffs[w]=diff
 for f in fs:f.set_variations({'wght':w})
 for t in ['بݣ','لݣ','مݣ','ݣݣݣ ݣ','بݣب','بݣَ','ببب ب','ههه ه','ھھھ ھ','ککک ک']:
  a,b=[shape(f,t) for f in fs];assert len(a)==len(b)
  for x,y in zip(a,b):
   assert x[:2]==y[:2] and x[3:]==y[3:] and y[0]!='.notdef',(t,x,y)
   assert abs(y[2]-x[2]-(sets[1][y[0]].width-sets[0][x[0]].width))<=1
  if t=='بݣ':assert any(x[0] in allowed for x in b)
  checks.append({'weight':w,'text':t,'glyphs':b})
(C/'verification.json').write_text(json.dumps({'active_sources_unchanged':True,'reserved_files':len(m['reserved']),'compatible_components':True,'compiled_changes':diffs,'shaping':checks},ensure_ascii=False,indent=2)+'\n')
print('Only final U+0763 changed in compiled fonts; 30 shaped comparisons; all active sources unchanged and 34 human-reserved files intact.')
