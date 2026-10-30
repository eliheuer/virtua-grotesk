from pathlib import Path
import sys,json,copy,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'))
from curve_profile import profile,svg,read_contours
from curve_lint import all_segments,bez
p=C/'profiles';p.mkdir(exist_ok=True)
a=E.parse(C/'candidate-sources/sources/VirtuaGrotesk-Regular.ufo/glyphs/ogonek.glif').getroot();b=E.parse(C/'candidate-sources/sources/VirtuaGrotesk-Bold.ufo/glyphs/ogonek.glif').getroot()
reports=[];summary=[]
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
for w in [400,475,550,625,700]:
 t=(w-400)/300;r=copy.deepcopy(a)
 for q,x,y in zip(r.findall('.//point'),a.findall('.//point'),b.findall('.//point')):
  for k in ['x','y']:q.set(k,str(float(x.get(k))*(1-t)+float(y.get(k))*t))
 f=p/f'ogonek-{w}.glif';f.write_bytes(E.tostring(r));report=profile(f);assert not report['warnings'],report['warnings'];reports.append(report)
 assert all(j['classification'] in ['G0','G2','G1','G1line'] for j in report['joins'])
 curves=all_segments(read_contours(f)[0]);poly=[]
 for seg in curves:poly.extend(bez(*seg[:4],i/32) for i in range(32))
 edges=list(zip(poly,poly[1:]+poly[:1]));intersections=[]
 for i,(x,y) in enumerate(edges):
  for j in range(i+2,len(edges)):
   if i==0 and j==len(edges)-1:continue
   u,v=edges[j]
   if cross(x,y,u)*cross(x,y,v)<0 and cross(u,v,x)*cross(u,v,y)<0:intersections.append([i,j])
 assert not intersections
 area=sum(x[0]*y[1]-x[1]*y[0] for x,y in edges)/2
 assert area>0
 summary.append({'weight':w,'sampled_intersections':intersections,'signed_area':area,'curve_warnings':report['warnings'],'joins':[j['classification'] for j in report['joins']]})
# Compact per-curve sample diagnostics are retained in profiles; full JSON compresses samples.
(C/'geometry.json').write_text(json.dumps(summary,indent=2)+'\n')
(C/'curve-profile.json').write_text(json.dumps(reports,separators=(',',':'))+'\n')
(C/'curve-comb.svg').write_text(svg([reports[0],reports[-1]],12000))
print('Five-weight curve profiles and sampled outline intersections checked')
