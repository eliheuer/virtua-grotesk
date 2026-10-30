"""Compare precomposed-plus-mark contexts with canonically decomposed text."""
from pathlib import Path
import json,unicodedata
import pathops,uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
C=Path(__file__).resolve().parent;R=C.parents[2];p=R/'fonts/variable/VirtuaGrotesk[wght].ttf';f=TTFont(p);h=hb.Font(hb.Face(p.read_bytes()));rows=json.loads((C/'rebuild.json').read_text())['forms'][:29]
issues=[];count=0
for w in [400,550,700]:
 gs=f.getGlyphSet(location={'wght':w});h.set_variations({'wght':w})
 for row in rows:
  cp=chr(int(row['codepoint'][2:],16))
  for mark in '\u05b0\u05b7\u05bd\u0591\u0592':
   if mark in row['decomposition'] or (mark in '\u05b0\u05b7' and any(c in '\u05b7\u05b8' for c in row['decomposition'])):continue
   outlines=[];advs=[]
   for txt in [cp+mark,unicodedata.normalize('NFD',cp+mark)]:
    b=hb.Buffer();b.add_str(txt);b.guess_segment_properties();hb.shape(h,b);cursor=0;shape=pathops.Path()
    for info,pos in zip(b.glyph_infos,b.glyph_positions):
     gs[f.getGlyphName(info.codepoint)].draw(TransformPen(shape.getPen(),(1,0,0,1,cursor+pos.x_offset,pos.y_offset)));cursor+=pos.x_advance
    outlines.append(pathops.simplify(shape));advs.append(cursor)
   delta=abs(pathops.op(*outlines,pathops.PathOp.XOR).area);count+=1
   if delta>.1 or advs[0]!=advs[1]:issues.append(dict(weight=w,glyph=row['glyph'],mark=f'U+{ord(mark):04X}',difference_area=delta,advances=advs))
out=dict(comparisons=count,issues=issues);(C/'contexts.json').write_text(json.dumps(out,indent=2)+'\n');print(count,'contexts;',len(issues),'differences');print(issues[:8])
