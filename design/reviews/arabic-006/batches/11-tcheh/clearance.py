"""Sample all dot boundaries against base ink at endpoints and midpoint."""
from pathlib import Path
import json,sys,plistlib,xml.etree.ElementTree as E
from defcon import Font,Glyph
from fontTools.pens.pointInsidePen import PointInsidePen
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'));from curve_profile import all_segments,sample
fs=[Font(str(R/f'sources/VirtuaGrotesk-{m}.ufo')) for m in ['Regular','Bold']]
def interp(name,t):
 g=Glyph();p=g.getPointPen();cs=[]
 for a,b in zip(fs[0][name],fs[1][name]):
  p.beginPath();points=[]
  for x,y in zip(a,b):
   pos=(x.x*(1-t)+y.x*t,x.y*(1-t)+y.y*t);p.addPoint(pos,segmentType=x.segmentType,smooth=x.smooth);points.append(dict(x=pos[0],y=pos[1],on=x.segmentType is not None,type=x.segmentType,smooth=x.smooth))
  p.endPath();cs.append(points)
 return g,cs
out=[]
for w in [400,475,550,625,700]:
 t=(w-400)/300;_,dots=interp('threedotsdowncenter-ar',t)
 for suffix in ['', '.init','.medi','.fina']:
  name='tcheh-ar'+suffix;a,b=[f[name].components[1].transformation[-2:] for f in fs];dx,dy=[x*(1-t)+y*t for x,y in zip(a,b)];base,_=interp('hah-ar'+suffix,t);inside=[]
  for ci,c in enumerate(dots):
   for seg in all_segments(c):
    for i in range(65):
     p=sample(seg,i/64)['point'];pen=PointInsidePen(None,(p[0]+dx,p[1]+dy));base.draw(pen)
     if pen.getResult():inside.append([ci,p[0]+dx,p[1]+dy])
  out.append(dict(weight=w,glyph=name,inside=inside));assert not inside,(w,name,inside[:3])
(C/'dot-clearance.json').write_text(json.dumps(out,indent=2)+'\n');print('Dot boundary clear of base ink in 20 interpolated forms.')
