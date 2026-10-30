"""Measure compilation-only Regular curve approximation after joint cu2qu."""
from pathlib import Path
import json,numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.basePen import BasePen
C=Path(__file__).resolve().parent
class Sample(BasePen):
 def __init__(self,g):super().__init__(g);self.points=[]
 def _moveTo(self,p):self.p=np.array(p);self.start=self.p;self.points.append(p)
 def _lineTo(self,p):
  p=np.array(p);a=self.p;self.points.extend(tuple((1-t)*a+t*p) for t in np.linspace(0,1,max(2,int(np.linalg.norm(p-a)*4))));self.p=p
 def _qCurveToOne(self,c,p):
  a=self.p;c=np.array(c);p=np.array(p);self.points.extend(tuple((1-t)**2*a+2*(1-t)*t*c+t*t*p) for t in np.linspace(0,1,max(2,int((np.linalg.norm(c-a)+np.linalg.norm(p-c))*4))));self.p=p
 def _closePath(self):self._lineTo(self.start)
fonts=[instantiateVariableFont(TTFont(C/f'assets/{n}.ttf'),{'wght':400}).getGlyphSet() for n in ['before','after']]
r=json.loads((C/'verification.json').read_text());out={}
for name in r['compiled_changes']['400']['outlines_or_widths']:
 ps=[]
 for f in fonts:
  p=Sample(f);f[name].draw(p);ps.append(np.array(p.points))
 def dist(a,b):
  return max(float(np.sqrt(((a[i:i+64,None,:]-b[None,:,:])**2).sum(axis=2)).min(axis=1).max()) for i in range(0,len(a),64))
 d=max(dist(*ps),dist(*ps[::-1]));out[name]=d;assert d<1.5,(name,d)
(C/'regular-approximation.json').write_text(json.dumps({'method':'Bidirectional densely sampled outline distance, source units; sampling <=0.25 unit control-polygon spacing. Regular GLIF bytes and advances unchanged; joint cu2qu changes quadratic subdivision/rounding.','maximum_distance':max(out.values()),'glyphs':out},indent=2)+'\n')
print(max(out.values()))
