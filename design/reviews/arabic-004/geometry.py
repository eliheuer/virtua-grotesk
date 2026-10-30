"""Read-only source interpolation/clearance check of the three component pieces."""
from pathlib import Path
import sys,json,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'scripts'));import curve_lint as lint
m=json.loads((C/'candidate.json').read_text())
donors={master:{name:lint.parse((C/'donors'/master/f'{name}.glif').read_text())[0] for name in ['hamzaabove-ar','fatha-ar']} for master in ['Regular','Bold']}
for name in donors['Regular']:
 a,b=[donors[master][name] for master in ['Regular','Bold']]
 assert len(a)==len(b) and [(p['on'],p['smooth']) for p in a]==[(p['on'],p['smooth']) for p in b]
def poly(name,t,dy=0):
 points=[dict(a,x=a['x']*(1-t)+b['x']*t,y=a['y']*(1-t)+b['y']*t+dy) for a,b in zip(donors['Regular'][name],donors['Bold'][name])]
 out=[]
 for s in lint.all_segments(points):
  n=1 if s[4] else 96
  out.extend(lint.bez(*s[:4],i/n) for i in range(n))
 return out
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def point_segment(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy
 t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
 return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def inside(p,poly):
 result=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:result=not result
 return result
def clearance(a,b):
 assert not inside(a[0],b) and not inside(b[0],a),'Containment'
 result=float('inf')
 for x,y in zip(a,a[1:]+a[:1]):
  for u,v in zip(b,b[1:]+b[:1]):
   assert not (cross(x,y,u)*cross(x,y,v)<0 and cross(u,v,x)*cross(u,v,y)<0),'Intersection'
   result=min(result,point_segment(x,u,v),point_segment(y,u,v),point_segment(u,x,y),point_segment(v,x,y))
 return result
checks=[]
for weight in range(400,701,25):
 t=(weight-400)/300;upper=464*(1-t)+608*t;lower=352*(1-t)+432*t
 polygons=[poly('hamzaabove-ar',t),poly('fatha-ar',t,lower),poly('fatha-ar',t,upper)]
 gaps=[clearance(polygons[0],polygons[1]),clearance(polygons[1],polygons[2]),clearance(polygons[0],polygons[2])]
 assert min(gaps)>0
 checks.append(dict(weight=weight,offsets=[upper,lower],sampled_min_gaps=gaps,hamza_to_lower_bbox_gap=min(p[1] for p in polygons[1])-max(p[1] for p in polygons[0])))
(C/'geometry.json').write_text(json.dumps({'samples_per_curve':96,'checks':checks},indent=2)+'\n')
print('Three separate pieces at 13 weights; min sampled clearance:',min(min(x['sampled_min_gaps']) for x in checks))
