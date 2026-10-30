from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from fontTools.ufoLib import UFOReader
C=Path(__file__).resolve().parent;R=C.parents[3]
class Raster(BasePen):
 def __init__(self,gs,d,x,y,s):super().__init__(gs);self.d=d;self.x=x;self.y=y;self.s=s;self.pts=[]
 def _moveTo(self,p):self.pts=[p]
 def _lineTo(self,p):self.pts.append(p)
 def _curveToOne(self,a,b,c):
  p=self._getCurrentPoint()
  for j in range(1,81):
   t=j/80;u=1-t;self.pts.append(tuple(u**3*p[k]+3*u*u*t*a[k]+3*u*t*t*b[k]+t**3*c[k] for k in [0,1]))
 def _closePath(self):self.d.polygon([(self.x+x*self.s,self.y-y*self.s) for x,y in self.pts],fill='#dedede')
font=TTFont(next((C.parent/'working-v5/fonts').glob('rubik*.ttf')))
im=Image.new('RGB',(1800,1200),'#181818');d=ImageDraw.Draw(im);lab=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24)
for row,(master,w) in enumerate([('Regular',400),('Bold',700)]):
 for col,kind in enumerate(['Before','Trial','Rubik']):
  gs=font.getGlyphSet(location={'wght':w}) if kind=='Rubik' else UFOReader(R/('sources' if kind=='Before' else 'out/qa/hebrew-008-v6/sources')/f'VirtuaGrotesk-{master}.ufo').getGlyphSet()
  for ix,name in enumerate(['shin-hb','finaltsadi-hb']):
   x=20+col*600+ix*300;y=440+row*600
   d.text((x,20+row*600),f'{kind} {master} {name}',fill='#dedede',font=lab)
   g=font.getBestCmap()[0x5e9 if ix==0 else 0x5e5] if kind=='Rubik' else name
   gs[g].draw(Raster(gs,d,x,y,.34))
im.save(C/'draft.png')
