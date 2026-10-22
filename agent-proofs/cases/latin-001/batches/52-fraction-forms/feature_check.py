from pathlib import Path
import json,uharfbuzz as hb
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;S=Path(json.loads((C/'baseline.json').read_text())['scratch'])
features=[{}, {'frac':1},{'numr':1},{'dnom':1},{'tnum':1,'frac':1},{'sups':1},{'frac':0,'numr':0,'dnom':0}]
def shape(p,t,w,opts):
 f=hb.Font(hb.Face(p.read_bytes()));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(t);b.guess_segment_properties();hb.shape(f,b,opts);names=TTFont(p).getGlyphOrder();return [(names[i.codepoint],j.x_advance,j.x_offset,j.y_offset) for i,j in zip(b.glyph_infos,b.glyph_positions)]
rows=[]
for p in (S/'fonts').rglob('*.ttf'):
 f=TTFont(p);before=C/'baseline-fonts'/p.relative_to(S/'fonts')
 for w in ([400,475,550,625,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
  for t in ['¼½¾','¼́ ½̧ ¾̈']:
   expected=shape(p,t,w,{})
   assert all(g[0]!='.notdef' for g in expected)
   for opts in features:assert shape(p,t,w,opts)==expected;rows.append({'font':p.name,'weight':w,'text':t,'features':opts,'encoded_idempotent':True})
  for t in ['1/4 1/2 3/4','1234567890','1⁄4 1⁄2 3⁄4','ببب שָׁלוֹם µm fi fl']:
   for opts in features:assert shape(p,t,w,opts)==shape(before,t,w,opts);rows.append({'font':p.name,'weight':w,'text':t,'features':opts,'baseline_equal':True})
(C/'feature-checks.json').write_text(json.dumps({'cases':len(rows),'note':'Unsupported U2044 contexts remain baseline-equivalent, not covered. Optional features were not added.','rows':rows},ensure_ascii=False,indent=2)+'\n');print(len(rows),'feature-mode cases')
