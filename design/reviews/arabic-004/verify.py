"""Bounded source and compiled shaping/contour regression checks."""
from pathlib import Path
import hashlib,json,sys,shutil
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text())
changed=[p for p,h in m['source_hashes'].items() if sha(R/p)!=h]
assert set(changed)=={g['path'] for g in m['glyphs']}
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
for master in ['Regular','Bold']:
 for name in ['hamzaabove-ar','fatha-ar']:
  assert sha(R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif')==sha(C/f'donors/{master}/{name}.glif')
shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/after.ttf')
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths]
orders=[f.getGlyphOrder() for f in fonts];assert orders[0]==orders[1]
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['أً','أً','أً','بأً','ؤً','ؤً','ئً','ئً','بئً','بًٔ','بًٔ','تًٔ','لًٔ','بً','تً','اً','بًا','رَأْس','سُؤَال','بِئْر','أَ','أُ','أٌ','أْ','ء']
report={'source_changes':changed,'font_hashes':dict(zip(['before','working'],map(sha,paths))),'compiled_changes':{},'checks':[]}
def shape(f,text):
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [dict(name=orders[0][i.codepoint],cluster=i.cluster,advance=p.x_advance,offset=[p.x_offset,p.y_offset]) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths]
 diff=[]
 for name in sets[0]:
  values=[]
  for gs in sets:
   pen=DecomposingRecordingPen(gs);gs[name].draw(pen);values.append((pen.value,gs[name].width))
  assert values[0][1]==values[1][1],(w,name,'advance changed')
  if values[0]!=values[1]:diff.append(name)
 assert set(diff)=={'uni064B','uni0654064B'},(w,diff)
 for name,count in [('uni064B',2),('uni0654064B',3)]:
  pen=DecomposingRecordingPen(sets[1]);sets[1][name].draw(pen)
  assert sum(op=='moveTo' for op,args in pen.value)==count,(w,name,'pieces not separate')
 report['compiled_changes'][str(w)]=diff
 for f in hfonts:f.set_variations({'wght':w})
 for text in samples:
  a,b=[shape(f,text) for f in hfonts]
  assert all(x['name']!='.notdef' for x in a+b)
  assert [(x['name'],x['cluster'],x['advance']) for x in a]==[(x['name'],x['cluster'],x['advance']) for x in b],(w,text)
  if '\u064b' not in text:assert a==b,(w,text,'unrelated shaping changed')
  report['checks'].append(dict(weight=w,text=text,before=a,working=b))
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(report['checks']),'shaping comparisons; only Fathatan and Hamza/Fathatan outlines differ; all advances unchanged')
