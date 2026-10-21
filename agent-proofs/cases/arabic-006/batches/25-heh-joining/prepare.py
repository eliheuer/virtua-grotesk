"""Repair Bold Heh bowls; reserve Beh closure, all green consumers and Regular bytes."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'applied.json').exists()
roots={};contents={};reserved={};trees={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc;trees[master]={n:E.parse(rr/f) for n,f in cc.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in dep for co in trees[master][n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
rr=roots['Bold'];cc=contents['Bold'];drawings={'heh-ar.init','heh-ar.medi'};names=drawings;closure=set(drawings)
while True:
 add={n for n,t in trees['Bold'].items() if any(co.get('base') in closure for co in t.findall('outline/component'))}-closure
 if not add:break
 closure|=add
assert closure==drawings
for n in closure:
 s=(rr/cc[n]).read_text();assert '<string>red</string>' in s;assert str((rr/cc[n]).relative_to(R)) not in reserved
initial=[(608,0),(832,0),(960,104),(960,256),(960,368),(896,456),(832,496),(448,736),(424,736),(336,576),(336,552),(672,384),(736,352),(800,312),(800,256),(800,192),(704,176),(608,176),(528,176),(528,184),(552,184),(576,208),(576,256),(576,400),(464,496),(320,496),(176,496),(64,400),(64,256),(64,208),(88,184),(112,184),(112,176),(0,176),(-16,160),(-16,16),(0,0), (320,176),(264,176),(224,208),(224,256),(224,304),(264,336),(320,336),(376,336),(416,304),(416,256),(416,208),(376,176)]
medial=[(368,-192),(288,-192),(224,-120),(224,-40),(224,-8),(232,0),(368,0),(424,0),(464,-40),(464,-96),(464,-152),(424,-192), (256,176),(232,176),(224,184),(224,256),(224,304),(280,336),(336,336),(392,336),(432,304),(432,256),(432,192),(336,176), (368,-352),(512,-352),(624,-248),(624,-112),(624,-64),(608,-32),(584,-8),(584,0),(704,0),(704,176),(512,176),(512,184),(552,184),(592,192),(592,256),(592,400),(480,496),(336,496),(192,496),(64,400),(64,256),(64,184),(56,176),(0,176),(-16,160),(-16,16),(0,0),(56,0),(64,-8),(64,-40),(64,-216),(208,-352)]
coords={'heh-ar.init':initial,'heh-ar.medi':medial};widths={'heh-ar.init':992,'heh-ar.medi':704}
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(closure),'placements':{}}
for n in sorted(names):
 p=rr/cc[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 if n in drawings:
  it=iter(coords[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
  new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[n]}"/>',new)
 a=E.fromstring(new);b=trees['Regular'][n];assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n]
  for stage in ['before','candidate']:
   dst=C/(stage+'-sources')/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,metrics_only=n not in drawings,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'24-heh-bowls/assets/after.ttf',C/'assets/before.ttf')
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared 2 Bold files; no inherited consumers; Beh18 reserved.')
