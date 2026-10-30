from pathlib import Path
import json,pathops,uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
C=Path(__file__).resolve().parent;data=(C/'assets/after.ttf').read_bytes();f=TTFont(C/'assets/after.ttf');rows=[]
for w in [400,475,550,625,700]:
 gs=f.getGlyphSet(location={'wght':w});hf=hb.Font(hb.Face(data));hf.set_variations({'wght':w})
 for text in ['1⁄4','1⁄2','3⁄4','H⁄H']:
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(hf,b);x=0;paths=[];names=[]
  for info,p in zip(b.glyph_infos,b.glyph_positions):
   name=f.getGlyphName(info.codepoint);a=pathops.Path();gs[name].draw(TransformPen(a.getPen(),(1,0,0,1,x+p.x_offset,p.y_offset)));a.simplify();paths.append(a);names.append(name);x+=p.x_advance
  overlaps=[abs(pathops.op(paths[i],paths[i+1],pathops.PathOp.INTERSECTION).area) for i in range(len(paths)-1)];rows.append({'weight':w,'text':text,'glyphs':names,'adjacent_intersection_areas':overlaps})
assert any(any(a>0 for a in r['adjacent_intersection_areas']) for r in rows)
(C/'default-collisions.json').write_text(json.dumps({'application':'REJECTED as standalone encoded slash','reason':'Narrow negative bearings require coherent fraction-layout behavior. Numeric preservation passes do not override visible default collisions.','rows':rows},ensure_ascii=False,indent=2)+'\n');print(rows[0],rows[-4])
