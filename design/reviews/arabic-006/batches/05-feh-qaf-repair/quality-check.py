"""Case-specific rejection regression, not a universal font-quality score.

Catches the failed batch's unfair smooth joins, stretched initial return, and
sampled crossing contours. Does not replace looking at actual font rasters.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'scripts'))
from curve_profile import read_contours,all_segments,sample
m=json.loads((C/'applied.json').read_text());out={'limits':'20% curvature jump at smooth cubic/cubic joins in these revised heads; return aspect <=2; sampled proper segment crossings. Not release or human approval.','glyphs':[]}
def crossings(path):
 lines=[]
 for contour in read_contours(path):
  for seg in all_segments(contour):
   points=[tuple(seg[0]),tuple(seg[3])] if seg[4] else [sample(seg,i/128)['point'] for i in range(129)]
   lines.extend((a,b) for a,b in zip(points,points[1:]) if a!=b)
 z=np.asarray(lines);a=z[:,0];b=z[:,1];count=0
 def cross(u,v):return u[...,0]*v[...,1]-u[...,1]*v[...,0]
 for start in range(0,len(z),128):
  aa=a[start:start+128,None,:];bb=b[start:start+128,None,:];cc=a[None,:,:];dd=b[None,:,:]
  q1=cross(bb-aa,cc-aa);q2=cross(bb-aa,dd-aa);q3=cross(dd-cc,aa-cc);q4=cross(dd-cc,bb-cc)
  hit=(q1*q2 < -1e-10)&(q3*q4 < -1e-10)
  # Strict proper intersections only; adjoining endpoints do not count.
  for i in range(hit.shape[0]):hit[i,:start+i+1]=False
  count+=int(hit.sum())
 return count
for g in m['glyphs']:
 if not g['drawing']:continue
 name=g['name'];reports=json.loads((C/(name+'-curves.json')).read_text())['reports'];row={'name':name}
 for label,report in zip(['before','after'],reports):
  path=C/'before-sources'/g['path'] if label=='before' else R/g['path']
  assert hashlib.sha256(path.read_bytes()).hexdigest()==report['sha256']
  faults=list(report['warnings'])
  for j in report['joins']:
   if j['classification'] in ['kink','undefined'] or (j['classification']=='G1' and j['relative_jump']>.2):faults.append({'join':j['point'],'class':j['classification'],'relative_jump':j['relative_jump']})
  n=crossings(path)
  if n:faults.append({'sampled_proper_crossings':n})
  if name=='fehDotless-ar.init':
   curves=report['curves'];seg=curves[-1]['controls'];dx=abs(seg[3][0]-seg[0][0]);dy=abs(seg[3][1]-seg[0][1]);aspect=dx/dy if dy else 1e9
   row[label+'_return']={'extent':[dx,dy],'aspect':aspect}
   if aspect>2:faults.append({'stretched_return':aspect})
  row[label]={'faults':faults,'sampled_crossings':n}
 out['glyphs'].append(row)
out['new_faults']=sum(len(g['after']['faults']) for g in out['glyphs']);out['previous_faults']=sum(len(g['before']['faults']) for g in out['glyphs'])
(C/'quality-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('Prior faults:',out['previous_faults'],'revised faults:',out['new_faults'])
assert out['previous_faults']>0,'Regression must expose the rejected drawings'
assert out['new_faults']==0,out
