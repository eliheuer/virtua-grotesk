"""Detached mark construction trial. Does not write active UFO sources."""
from pathlib import Path
import hashlib,json,re,shutil,math,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[2];S=R/'out/hebrew-010-chamfer-v3';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'chamfer-v3.json').exists(),'Preserve trial evidence'
names=[g['glyph'] for g in json.loads((C/'bold-candidate-v2.json').read_text())['glyphs']]
(S/'sources').mkdir(parents=True,exist_ok=True)
for p in (R/'sources').iterdir():
 if p.name in ['VirtuaGrotesk.designspace','config.yaml'] or (p.is_dir() and p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']):
  if p.is_dir():shutil.copytree(p,S/'sources'/p.name)
  else:shutil.copy2(p,S/'sources'/p.name)
manifest={'state':'detached proposal, not installed','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
snap=lambda x:round(x/8)*8
sign=lambda x:(x>0)-(x<0)
def beveled(poly):
 out=[]
 for i,(x,y) in enumerate(poly):
  a=poly[i-1];b=poly[(i+1)%len(poly)];cross=(x-a[0])*(b[1]-y)-(y-a[1])*(b[0]-x)
  d=16 if cross>0 else 8
  # Axis-parallel landings at splayed qamats-qatan corners retain diagonal stem.
  def step(q):
   dx,dy=q[0]-x,q[1]-y
   return (x+sign(dx)*d,y) if abs(dx)>abs(dy) else (x,y+sign(dy)*d)
  out.extend([step(a),step(b)])
 assert len(set(out))==len(out),out
 return out
for master in ['Regular','Bold']:
 for name in names:
  rel=f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif';old=(R/rel).read_text();root=E.fromstring(old);polys=[]
  for c in root.findall('outline/contour'):
   pts=[(float(p.get('x')),float(p.get('y'))) for p in c]
   if any(p.get('type')=='curve' for p in c):
    x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
    size=64 if master=='Regular' else int(min(x1-x0,y1-y0))
    cx=snap((x0+x1)/2);cy=snap((y0+y1)/2);r=size//2
    poly=[(cx+r,cy-r),(cx+r,cy+r),(cx-r,cy+r),(cx-r,cy-r)]
   else:poly=[(snap(x),snap(y)) for x,y in pts]
   polys.append(beveled(poly))
  outline='\t<outline>\n'+''.join('\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}" type="line"/>\n' for x,y in poly)+'\t\t</contour>\n' for poly in polys)+'\t</outline>'
  new=re.sub(r'\t<outline>.*?</outline>',outline,old,flags=re.S)
  for folder,text in [('before-chamfer-v3',old),('candidate-chamfer-v3',new)]:
   p=C/folder/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
  (S/rel).write_text(new)
  manifest['glyphs'].append({'glyph':name,'master':master,'path':rel,'before_sha256':sha(R/rel),'candidate_sha256':sha(S/rel),'contour_points':[len(p) for p in polys]})
for name in names:
 a=E.parse(S/f'sources/VirtuaGrotesk-Regular.ufo/glyphs/{name}.glif');b=E.parse(S/f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{name}.glif')
 assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')]
for rel,h in manifest['source_hashes'].items():assert sha(R/rel)==h
(C/'chamfer-v3.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(S)
