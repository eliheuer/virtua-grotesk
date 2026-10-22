from pathlib import Path
import json,hashlib,re,plistlib
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'candidate.json').read_text());S=Path(m['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changed={g['path'] for g in m['glyphs']}
for p,h in m['source_hashes'].items():
 assert sha(R/p)==h,p
 if p not in changed:assert sha(S/p)==h,p
for g in m['glyphs']:
 a=(C/'before-sources'/g['path']).read_text();b=(C/'candidate-sources'/g['path']).read_text();assert re.sub(r'<advance[^>]+>','',a)==re.sub(r'<advance[^>]+>','',b)
 assert sha(S/g['path'])==g['candidate_sha256']
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];order=TTFont(paths[0]).getGlyphOrder();assert order==TTFont(paths[1]).getGlyphOrder();lib=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes());ps=lambda n:lib.get('public.postscriptNames',{}).get(n,n.replace('-',''));allowed={ps(g['name']) for g in m['glyphs']};fs=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
checks=[];diffs={}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [(order[i.codepoint],i.cluster,p.x_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,550,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[]
 for n in sets[0]:
  pens=[]
  for gs in sets:
   pen=DecomposingRecordingPen(gs);gs[n].draw(pen);pens.append(pen.value)
  assert pens[0]==pens[1],('outline change',w,n)
  if sets[0][n].width!=sets[1][n].width:diff.append(n)
 assert set(diff)<=allowed;diffs[w]=diff
 for f in fs:f.set_variations({'wght':w})
 for t in ['ڢڢڢ ڢ', 'ڥڥڥ ڥ', 'ڧڧڧ ڧ', 'ڨڨڨ ڨ', 'ٻٻٻ ٻ', 'ٽٽٽ ٽ', 'ٹٹٹ ٹ', 'ٺٺٺ ٺ', 'ټټټ ټ', 'ڤڤڤ ڤ', 'يآ يإ يٱ', 'ببب ب', 'ههه ه', 'ھھھ ھ', 'العربية جميلة']:
  a,b=[shape(f,t) for f in fs];assert len(a)==len(b)
  for x,y in zip(a,b):
   assert x[:2]==y[:2] and x[3:]==y[3:] and y[0]!='.notdef',(t,x,y)
   assert abs(y[2]-x[2]-(sets[1][y[0]].width-sets[0][x[0]].width))<=1,(t,x,y)
  checks.append({'weight':w,'text':t,'glyphs':b})
(C/'verification.json').write_text(json.dumps({'all_outlines_unchanged':True,'all_source_changes_advance_only':True,'reserved':len(m['reserved']),'compiled_width_changes':diffs,'shaping':checks},ensure_ascii=False,indent=2)+'\n')
print('All compiled outlines unchanged at400/550/700; only named advances change; all34 reserved sources intact.')
