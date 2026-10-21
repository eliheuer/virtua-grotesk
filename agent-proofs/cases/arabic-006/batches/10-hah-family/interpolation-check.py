"""Sample source interpolation crossings separately from raster review."""
from pathlib import Path
import runpy,json
C=Path(__file__).resolve().parent;R=C.parents[4];h=runpy.run_path(str(C/'quality-check.py'));m=json.loads((C/'applied.json').read_text());rows=[]
for g in m['glyphs']:
 if not g['drawing']:continue
 b=h['read_contours'](R/g['path']);a=h['read_contours'](R/g['path'].replace('-Bold','-Regular'))
 for t in [0,.25,.5,.75,1]:
  cc=[[dict(p,x=p['x']*(1-t)+q['x']*t,y=p['y']*(1-t)+q['y']*t) for p,q in zip(c,d)] for c,d in zip(a,b)]
  crosses=h['crossings'](cc);assert crosses==0,(g['name'],t,crosses);rows.append(dict(glyph=g['name'],weight=400+300*t,crossings=crosses))
(C/'interpolation-check.json').write_text(json.dumps(rows,indent=2)+'\n')
