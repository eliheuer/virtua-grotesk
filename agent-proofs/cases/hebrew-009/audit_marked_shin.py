"""Read-only comparison: stored presentation glyph versus shaped current base/marks."""
from pathlib import Path
import json,hashlib,unicodedata,sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;R=C.parents[2];path=R/'fonts/variable/VirtuaGrotesk[wght].ttf'
f=TTFont(path);h=hb.Font(hb.Face(path.read_bytes()));cmap=f.getBestCmap();rows=[]
class Raster(BasePen):
 def __init__(self,gs,d,x,y,s):super().__init__(gs);self.d=d;self.x=x;self.y=y;self.s=s;self.pts=[]
 def _moveTo(self,p):self.pts=[p]
 def _lineTo(self,p):self.pts.append(p)
 def _curveToOne(self,a,b,c):
  p=self._getCurrentPoint()
  for j in range(1,65):
   t=j/64;u=1-t;self.pts.append(tuple(u**3*p[k]+3*u*u*t*a[k]+3*u*t*t*b[k]+t**3*c[k] for k in [0,1]))
 def _closePath(self):self.d.polygon([(self.x+x*self.s,self.y-y*self.s) for x,y in self.pts],fill='#dedede')
im=Image.new('RGB',(1600,900),'#181818');d=ImageDraw.Draw(im);lab=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',23)
for row,w in enumerate([400,700]):
 gs=f.getGlyphSet(location={'wght':w});h.set_variations({'wght':w})
 d.text((20,row*450+12),f'{w}: stored form (left) / current base + marks (right)',font=lab,fill='#dedede')
 for col,cp in enumerate([0xfb2a,0xfb2b,0xfb49,0xfb2c,0xfb2d]):
  x=20+col*316;y=300+row*450;s=.165
  d.text((x,row*450+64),f'U+{cp:04X}',font=lab,fill='#dedede');gs[cmap[cp]].draw(Raster(gs,d,x,y,s))
  text=unicodedata.normalize('NFD',chr(cp));buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(h,buf);cursor=0;placements=[]
  for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
   name=f.getGlyphName(info.codepoint);gs[name].draw(Raster(gs,d,x+155+s*(cursor+pos.x_offset),y-s*pos.y_offset,s));placements.append({'glyph':name,'x':cursor+pos.x_offset,'y':pos.y_offset});cursor+=pos.x_advance
  rows.append({'codepoint':f'U+{cp:04X}','weight':w,'stored':cmap[cp],'decomposed':text,'placements':placements})
im.save(C/'marked-shin-audit.png')
(C/'audit.json').write_text(json.dumps({'font_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':rows,'state':'Read-only evidence, no source edits.'},ensure_ascii=False,indent=2)+'\n')
