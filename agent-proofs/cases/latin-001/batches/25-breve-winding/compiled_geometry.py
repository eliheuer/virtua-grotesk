from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.varLib.instancer import instantiateVariableFont
import json
C=Path(__file__).resolve().parent
class Segments(BasePen):
 def __init__(self,gs):super().__init__(gs);self.segments=[]
 def _moveTo(self,p):self.first=p;self.current=p
 def add(self,points):
  seq=tuple(points);self.segments.append(min(seq,seq[::-1]));self.current=seq[-1]
 def _lineTo(self,p):self.add([self.current,p])
 def _qCurveToOne(self,c,p):self.add([self.current,c,p])
 def _curveToOne(self,a,b,p):self.add([self.current,a,b,p])
 def _closePath(self):
  if self.current!=self.first:self._lineTo(self.first)
 def _endPath(self):pass
before=TTFont(C/'assets/before.ttf');after=TTFont(C/'assets/after.ttf');checks=0
for w in [400,475,550,625,700]:
 a=instantiateVariableFont(before,{'wght':w},inplace=False).getGlyphSet();b=instantiateVariableFont(after,{'wght':w},inplace=False).getGlyphSet()
 for n in before.getGlyphOrder():
  ap=Segments(a);bp=Segments(b);a[n].draw(ap);b[n].draw(bp)
  assert sorted(ap.segments)==sorted(bp.segments),(w,n)
  checks+=1
(C/'compiled-geometry.json').write_text(json.dumps({'comparisons':checks,'weights':[400,475,550,625,700],'method':'Exact undirected line/quadratic/cubic segment multisets with recursively decomposed components, instantiated compiled VF. Only traversal differs.','all_glyph_geometry_equal':True},indent=2)+'\n');print(checks,'compiled glyph geometry comparisons pass')
