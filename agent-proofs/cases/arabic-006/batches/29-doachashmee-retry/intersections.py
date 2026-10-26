from pathlib import Path
import ast,json,sys
C=Path(__file__).resolve().parent;R=C.parents[4];sys.path.insert(0,str(R/'scripts'))
from curve_profile import read_contours,all_segments,sample
import numpy as np
old=ast.parse((C.parent/'27-doachashmee/quality-check.py').read_text());f=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name=='crossings');exec(compile(ast.Module(body=[f],type_ignores=[]),'crossings','exec'))
m=json.loads((C/'candidate.json').read_text());rows=[]
for n in sorted(set(g['name'] for g in m['glyphs'])):
 a,b=[read_contours(C/'candidate-sources'/next(g['path'] for g in m['glyphs'] if g['name']==n and g['master']==master)) for master in ['Regular','Bold']]
 for t in [0,.25,.5,.75,1]:
  cc=[[dict(p,x=p['x']*(1-t)+q['x']*t,y=p['y']*(1-t)+q['y']*t) for p,q in zip(c,d)] for c,d in zip(a,b)]
  count=crossings(cc);assert count==0,(n,t,count);rows.append({'glyph':n,'weight':400+300*t,'sampled_crossings':count})
(C/'intersections.json').write_text(json.dumps(rows,indent=2)+'\n');print('No sampled contour intersections at five weights.')
