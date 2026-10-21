"""Bounded Meem diagnostics; intentional overlaps and S returns need visual review."""
from pathlib import Path
import json,sys,hashlib
import numpy as np
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'scripts'))
from curve_profile import read_contours,all_segments,sample
m=json.loads((C/'applied.json').read_text())
def crossings(contours):
 lines=[]
 for contour in contours:
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

out={'limits':'Sampled within-contour crossings only. Medial positive contours intentionally overlap; final compiled union and counters require raster inspection. Curvature transitions are reported, not hidden.', 'glyphs':[]}
for g in m['glyphs']:
 p=R/g['path'];r=json.loads((C/(g['name']+'-curves.json')).read_text())['reports'][1]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 row={'name':g['name'],'within_contour_crossings':[crossings([c]) for c in read_contours(p)],'warnings':r['warnings'],'non_G2_curve_joins':[j for j in r['joins'] if j['classification'] in ['G1','kink','undefined']]}
 assert not any(row['within_contour_crossings']),row
 assert not any(j['classification'] in ['kink','undefined'] for j in row['non_G2_curve_joins']),row
 out['glyphs'].append(row)
(C/'quality-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('No sampled within-contour crossings or tangent kinks; intentional S transitions retained in report.')
