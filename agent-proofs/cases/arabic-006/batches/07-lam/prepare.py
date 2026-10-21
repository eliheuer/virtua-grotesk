"""Bounded Bold Lam trial; preserve Regular, final Lam and Beh dependency closure."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent
assert not (C/'candidate.json').exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
roots={};contents={};reserved={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in names for co in E.parse(rr/cc[n]).findall('outline/component')}-names
  if not add:break
  names|=add
 for n in names:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
root=roots['Bold'];cs=contents['Bold']
points={
 'lam-ar':[(32,0),(32,-176),(144,-272),(352,-272),(560,-272),(672,-176),(672,0),(672,752),(656,768),(528,768),(512,752),(512,0),(512,-64),(448,-96),(352,-96),(256,-96),(192,-64),(192,0),(192,64),(176,80),(48,80),(32,64)],
 'lam-ar.init':[(0,0),(144,0),(256,112),(256,272),(256,752),(240,768),(112,768),(96,752),(96,272),(96,216),(56,176),(0,176),(-16,160),(-16,16)],
 'lam-ar.medi':[(0,0),(64,0),(128,0),(184,0),(216,32),(232,32),(264,0),(320,0),(384,0),(448,0),(464,16),(464,160),(448,176),(384,176),(336,176),(304,208),(304,256),(304,752),(288,768),(160,768),(144,752),(144,256),(144,208),(112,176),(64,176),(0,176),(-16,160),(-16,16)]}
widths={'lam-ar':704,'lam-ar.init':320,'lam-ar.medi':448}
deps=set(points)
while True:
 add={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
for n in deps:
 t=(root/cs[n]).read_text()
 assert '<string>green</string>' not in t and '<string>0.09,0.72,0.44,1</string>' not in t,n
 assert str((root/cs[n]).relative_to(R)) not in reserved,n
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'placements':{},'inherited_bold_glyphs':sorted(deps-set(points))}
for n in sorted(deps):
 p=root/cs[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 if n in points:
  it=iter(points[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[n]}"/>',new)
 elif n.startswith('lam_alef'):
  # These final wrappers append the medial Lam at x=256; retain overlap beyond advance.
  new=new.replace('<advance width="672"/>','<advance width="704"/>')
 if new==old:continue
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 # Topology must match the protected master without altering it.
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n])
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')],n
 for master in ['Regular','Bold']:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,drawing=n in points,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'06-medial-loop/assets/after.ttf',C/'assets/before.ttf')
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied',len(m['glyphs']),'files; affected',sorted(deps),'reserved',len(reserved),'Beh/component files.')
