"""Render raw stored glyphs from compiled fonts, without Unicode normalization."""
from pathlib import Path
import json,cairo
from fontTools.ttLib import TTFont
from fontTools.pens.cairoPen import CairoPen
C=Path(__file__).resolve().parent;R=C.parents[2]
rows=json.loads((C/'rebuild.json').read_text())['forms'][:29]
paths=[C/'before-fonts/VirtuaGrotesk[wght].ttf',R/'fonts/variable/VirtuaGrotesk[wght].ttf']
fonts=[TTFont(p) for p in paths]
for weight in [400,550,700]:
 surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,1600,1880);ctx=cairo.Context(surface);ctx.set_source_rgb(.094,.094,.094);ctx.paint();ctx.set_source_rgb(.87,.87,.87)
 ctx.select_font_face('Helvetica');ctx.set_font_size(24);ctx.move_to(24,34);ctx.show_text(f'HEB-009  /  {weight}  /  Stored glyphs: Before left, Working right')
 gs=[f.getGlyphSet(location={'wght':weight}) for f in fonts]
 for i,row in enumerate(rows):
  x=24+(i%5)*316;y=65+(i//5)*300;cp=int(row['codepoint'][2:],16)
  ctx.set_font_size(17);ctx.move_to(x,y+18);ctx.show_text(row['glyph'].replace('-hb',''))
  ctx.move_to(x,y+42);ctx.show_text(row['codepoint'])
  for k,f in enumerate(fonts):
   ctx.save();ctx.translate(x+12+k*145,y+235);ctx.scale(.17,-.17);gs[k][f.getBestCmap()[cp]].draw(CairoPen(gs[k],ctx));ctx.fill();ctx.restore()
 surface.write_to_png(str(C/f'stored-forms-{weight}.png'))
print('Rendered all 29 forms at 400 / 550 / 700')
