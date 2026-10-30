"""Bounded Bold Meem repair; preserve green Regular and Beh dependency closure."""
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
# Shared 480-unit head, 160-unit side and 144/176 crown/base.
head=[(496,336),(544,336),(576,304),(576,256),(576,208),(544,176),(496,176),(424,176),(416,184),(416,256),(416,304),(448,336)]
iso=[(32,-240),(48,-256),(176,-256),(192,-240),(192,-64),(192,-24),(216,0),(256,0),(496,0),(640,0),(736,96),(736,240),(736,384),(640,480),(496,480),(352,480),(256,384),(256,240),(256,184),(248,176),(240,176),(112,176),(32,96),(32,-64)]+head
init=[(-16,16),(0,0),(264,0),(408,0),(504,96),(504,240),(504,384),(408,480),(264,480),(120,480),(24,384),(24,240),(24,184),(16,176),(0,176),(-16,160)]+[(x-232,y) for x,y in head]
fina=iso[:9]+[(584,0),(640,24),(688,72),(696,72),(728,24),(784,0),(848,0),(880,0),(880,176),(832,176),(744,176),(736,200),(736,240)]+iso[12:24]+head
# Raised medial head with S shoulders entering the bar horizontally. Existing separate
# bar contours intentionally overlap the head; compile and inspect their union.
medi=[(448, 0), (624, 176), (592, 176), (512, 176), (544, 480), (304, 480), (64, 480), (96, 176), (16, 176), (-16, 176), (160, 0), (304, 0), (256, 176), (224, 208), (224, 256), (224, 304), (256, 336), (304, 336), (352, 336), (384, 304), (384, 256), (384, 208), (352, 176), (304, 176), (304, 0), (608, 0), (608, 176), (304, 176), (-16, 160), (-16, 16), (0, 0), (304, 0), (304, 176), (0, 176)]
points={'meem-ar':iso,'meem-ar.init':init,'meem-ar.medi':medi,'meem-ar.fina':fina}
widths={'meem-ar':800,'meem-ar.init':568,'meem-ar.medi':608,'meem-ar.fina':880}

deps=set(points)
while True:
 add={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
for n in deps:
 t=(root/cs[n]).read_text()
 assert '<string>green</string>' not in t and '<string>0.09,0.72,0.44,1</string>' not in t and '<string>0,1,0,1</string>' not in t,n
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
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'08-lam-final/assets/after.ttf',C/'assets/before.ttf')
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied',len(m['glyphs']),'files; affected',sorted(deps),'reserved',len(reserved),'Beh/component files.')
