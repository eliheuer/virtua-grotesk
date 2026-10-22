from pathlib import Path
import sys,json,copy,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'))
from curve_profile import profile,read_contours,all_segments,bez
S=Path(json.loads((C/'baseline.json').read_text())['scratch'])
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def intersects(a,b,c,d):return cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0
D=C/'intermediate';D.mkdir(exist_ok=True);reports=[]
for glyph in ['sevensuperior']:
 roots=[E.parse(C/f'candidate-sources/sources/VirtuaGrotesk-{m}.ufo/glyphs/{glyph}.glif').getroot() for m in ['Regular','Bold']]
 for w in [400,475,550,625,700]:
  t=(w-400)/300;r=copy.deepcopy(roots[0]);ps=r.findall('outline/contour/point');a=roots[0].findall('outline/contour/point');b=roots[1].findall('outline/contour/point')
  for p,x,y in zip(ps,a,b):
   for k in ['x','y']:p.set(k,str(float(x.get(k))*(1-t)+float(y.get(k))*t))
  p=D/f'{glyph}-{w}.glif';E.ElementTree(r).write(p);report=profile(p);crossings=[]
  for ci,c in enumerate(read_contours(p)):
   points=[]
   for seg in all_segments(c):
    points.extend([seg[0]] if seg[4] else [bez(*seg[:4],i/128) for i in range(128)])
   ss=list(zip(points,points[1:]+points[:1]))
   crossings += [(ci,i,j) for i,(a,b) in enumerate(ss) for j,(c,d) in enumerate(ss) if j>i+1 and not(i==0 and j==len(ss)-1) and intersects(a,b,c,d)]
  assert not crossings
  reports.append({'glyph':glyph,'weight':w,'sampled_proper_crossings':crossings,'curves':report['curves'],'warnings':report['warnings'],'joins':report['joins'],'note':'Standalone scaled figure skeletons with explicit terminal corrections; proper crossings checked within each contour.'})
(C/'five-weight-curves.json').write_text(json.dumps(reports,indent=2)+'\n');print([(r['weight'],r['warnings']) for r in reports])