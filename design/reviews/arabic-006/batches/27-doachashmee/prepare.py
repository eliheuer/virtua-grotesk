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
rr=roots['Bold'];cc=contents['Bold'];drawings={'hehDoachashmee-ar.medi'};names=drawings;closure=set(drawings)
while True:
 add={n for n,t in trees['Bold'].items() if any(co.get('base') in closure for co in t.findall('outline/component'))}-closure
 if not add:break
 closure|=add
assert closure==drawings
for n in closure:
 s=(rr/cc[n]).read_text();assert '<string>red</string>' in s;assert '0,1,0,1' not in s and '0.09,0.72,0.44,1' not in s;assert str((rr/cc[n]).relative_to(R)) not in reserved
# Reuse the measured 160-unit loop construction from batch25, not a font reference outline.
donor=roots['Bold']/cc['heh-ar.medi'];donor_xml=E.parse(donor)
coords={'hehDoachashmee-ar.medi':[(int(p.get('x')),int(p.get('y'))) for p in donor_xml.findall('.//point')]}
widths={'hehDoachashmee-ar.medi':704}
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
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'26-goal-bowls/assets/after.ttf',C/'assets/before.ttf')
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared 1 Bold file; no inherited consumers; Beh18 reserved.')
