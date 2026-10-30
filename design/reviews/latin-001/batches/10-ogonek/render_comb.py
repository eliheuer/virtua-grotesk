"""Rasterize this diagnostic's simple SVG using sampled vector paths."""
from pathlib import Path
import re,xml.etree.ElementTree as E
from PIL import Image,ImageDraw,ImageFont
from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import parse_path
C=Path(__file__).resolve().parent;root=E.parse(C/'curve-comb.svg').getroot();im=Image.new('RGB',(int(root.get('width')),int(root.get('height'))),'#eeeeee');d=ImageDraw.Draw(im)
class Pen(BasePen):
 def __init__(self):super().__init__(None);self.pts=[]
 def _moveTo(self,p):self.pts.append(p)
 def _lineTo(self,p):self.pts.append(p)
 def _curveToOne(self,a,b,c):
  p=self._getCurrentPoint()
  for i in range(1,49):
   t=i/48;u=1-t;self.pts.append(tuple(u**3*p[k]+3*u*u*t*a[k]+3*u*t*t*b[k]+t**3*c[k] for k in [0,1]))
 def _closePath(self):self.pts.append(self.pts[0])
for e in root:
 tag=e.tag.split('}')[-1]
 if tag=='text':d.text((float(e.get('x')),float(e.get('y'))-16),e.text,font=ImageFont.load_default(size=16),fill='#222222')
 if tag!='g':continue
 tx,ty,sx,sy=map(float,re.findall(r'-?\d+(?:\.\d+)?',e.get('transform')))
 def xy(x,y):return tx+float(x)*sx,ty+float(y)*sy
 for v in e:
  tag=v.tag.split('}')[-1]
  if tag=='path':
   p=Pen();parse_path(v.get('d'),p);pts=[xy(*x) for x in p.pts]
   fill=v.get('fill','none')
   if fill!='none':d.polygon(pts,fill=fill)
   d.line(pts,fill=v.get('stroke','#222222'),width=2)
  elif tag=='line':d.line([xy(v.get('x1'),v.get('y1')),xy(v.get('x2'),v.get('y2'))],fill=v.get('stroke','#555555'),width=1)
  elif tag=='circle':
   x,y=xy(v.get('cx'),v.get('cy'));r=abs(float(v.get('r'))*sx);d.ellipse((x-r,y-r,x+r,y+r),fill=v.get('fill','#222222'))
im.save(C/'curve-comb.png')
