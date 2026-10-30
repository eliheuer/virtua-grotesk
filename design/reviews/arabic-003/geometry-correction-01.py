"""Source contour crossing and tangent checks for this compatible mark pair."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'scripts'));import curve_lint as lint
reg=lint.parse((R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif').read_text())[0]
bold=lint.parse((C/'manual-correction-01/human.glif').read_text())[0]
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def check(cont):
 segs=lint.all_segments(cont);poly=[]
 for s in segs:
  for i in range(16 if not s[4] else 1):poly.append(lint.bez(*s[:4],i/(16 if not s[4] else 1)))
 n=len(poly);collisions=[]
 for i in range(n):
  a,b=poly[i],poly[(i+1)%n]
  for j in range(i+2,n):
   if i==0 and j==n-1:continue
   c,d=poly[j],poly[(j+1)%n]
   if cross(a,b,c)*cross(a,b,d)<-1e-6 and cross(c,d,a)*cross(c,d,b)<-1e-6:collisions.append([i,j])
 return collisions
checks=[]
for weight in range(400,701,25):
 t=(weight-400)/300;cont=[dict(a,x=a['x']*(1-t)+b['x']*t,y=a['y']*(1-t)+b['y']*t) for a,b in zip(reg,bold)]
 crossings=check(cont);assert not crossings,(weight,crossings)
 checks.append({'weight':weight,'sampled_crossings':crossings})
audit=lint.join_audit([bold]);assert not [a for a in audit if a['smooth'] and a['classification']=='kink']
(C/'manual-correction-01/geometry.json').write_text(json.dumps({'interpolation_checks':checks,'bold_join_audit':audit,'bold_curve_lint':lint.lint_glyph(C/'manual-correction-01/human.glif','hamzaabove-ar')},indent=2)+'\n')
print('13 interpolation samples without crossings; no marked-smooth tangent kinks.')
