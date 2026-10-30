from pathlib import Path
import sys,copy,json,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'))
from curve_profile import profile,read_contours,all_segments,bez
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def intersects(a,b,c,d):return cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0
roots=[E.parse(C/f'candidate-sources/sources/VirtuaGrotesk-{m}.ufo/glyphs/longs.glif').getroot() for m in ['Regular','Bold']]
D=C/'intermediate';D.mkdir(exist_ok=True);reports=[]
for w in [400,475,550,625,700]:
 t=(w-400)/300;r=copy.deepcopy(roots[0]);ps=r.findall('outline/contour/point');a=roots[0].findall('outline/contour/point');b=roots[1].findall('outline/contour/point')
 for p,x,y in zip(ps,a,b):
  for k in ['x','y']:p.set(k,str(float(x.get(k))*(1-t)+float(y.get(k))*t))
 p=D/f'longs-{w}.glif';E.ElementTree(r).write(p)
 report=profile(p);assert not report['warnings']
 points=[]
 for seg in all_segments(read_contours(p)[0]):
  if seg[4]:points.append(seg[0])
  else:points.extend(bez(*seg[:4],i/128) for i in range(128))
 segments=list(zip(points,points[1:]+points[:1]));crossings=[(i,j) for i,(a,b) in enumerate(segments) for j,(c,d) in enumerate(segments) if j>i+1 and not(i==0 and j==len(segments)-1) and intersects(a,b,c,d)];assert not crossings
 reports.append({'weight':w,'sampled_proper_crossings':crossings,'curves':len(report['curves']),'warnings':report['warnings'],'joins':report['joins']})
(C/'five-weight-curves.json').write_text(json.dumps(reports,indent=2)+'\n');print('Five weights: no sampled reversals/intersections; inherited tangent G1 line joins retained')
