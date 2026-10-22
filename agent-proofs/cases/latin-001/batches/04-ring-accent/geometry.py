from pathlib import Path
import json,math,sys,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'))
from curve_profile import profile,svg
from curve_lint import all_segments,bez
rpath=C/'candidate-sources/sources/VirtuaGrotesk-Regular.ufo/glyphs/ring.glif';bpath=C/'candidate-sources/sources/VirtuaGrotesk-Bold.ufo/glyphs/ring.glif';rp=E.parse(rpath).findall('.//point');bp=E.parse(bpath).findall('.//point');reports=[];summary=[]
(C/'profiles').mkdir(exist_ok=True)
for w in [400,475,550,625,700]:
 t=(w-400)/300;root=E.parse(rpath).getroot()
 for p,a,b in zip(root.findall('.//point'),rp,bp):
  for axis in ['x','y']:p.set(axis,str(float(a.get(axis))*(1-t)+float(b.get(axis))*t))
 p=C/'profiles'/f'ring-{w}.glif';E.ElementTree(root).write(p,encoding='UTF-8',xml_declaration=True);report=profile(p);assert not report['warnings'],report['warnings'];assert all(j['classification']=='G2' for j in report['joins']);reports.append(report)
 cy=728+8*t;radii=[]
 for ci,c in enumerate(report['contours']):
  points=[bez(*seg[:4],i/128) for seg in all_segments(c) for i in range(129)]
  rad=[math.hypot(x-152,y-cy) for x,y in points];radii.append((min(rad),max(rad)))
  vals=[s['curvature'] for curve in report['curves'] if curve['contour']==ci for s in curve['samples']]
  assert all(v is not None and (v>0 if ci==0 else v<0) for v in vals)
 assert radii[0][0]>radii[1][1]
 summary.append({'weight':w,'radial_bounds_outer_inner':radii,'minimum_radial_separation_bound':radii[0][0]-radii[1][1],'curvature_warnings':report['warnings'],'joins':[j['classification'] for j in report['joins']]})
(C/'geometry.json').write_text(json.dumps(summary,indent=2)+'\n');(C/'curve-profile.json').write_text(json.dumps({'reports':reports},indent=2)+'\n');(C/'curve-comb.svg').write_text(svg([reports[0],reports[-1]])+'\n');print('Five-weight signed curvature and nested radial bounds passed')
