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
rr=roots['Bold'];cc=contents['Bold'];drawings={'hehGoal-ar'};names=drawings|{'hehGoalHamzaabove-ar','tehMarbutaGoal-ar'};closure=set(drawings)
while True:
 add={n for n,t in trees['Bold'].items() if any(co.get('base') in closure for co in t.findall('outline/component'))}-closure
 if not add:break
 closure|=add
assert closure==names
for n in closure:
 s=(rr/cc[n]).read_text();assert '<string>red</string>' in s;assert '0,1,0,1' not in s and '0.09,0.72,0.44,1' not in s;assert str((rr/cc[n]).relative_to(R)) not in reserved
counter=[(384,240),(384,192),(344,160),(288,160),(232,160),(192,192),(192,240),(192,288),(232,320),(288,320),(344,320),(384,288)]
iso=[(32,240),(32,104),(144,0),(288,0),(432,0),(544,104),(544,240),(544,496),(528,512),(400,512),(384,496),(384,456),(376,456),(360,472),(328,480),(288,480),(144,480),(32,376)]+counter
final=counter+[(32,240),(32,104),(144,0),(288,0),(344,0),(424,24),(464,80),(472,80),(504,16),(592,0),(672,0),(672,176),(600,176),(544,208),(544,272),(544,496),(528,512),(400,512),(384,496),(384,456),(376,456),(360,472),(328,480),(288,480),(144,480),(32,376)]
coords={'hehGoal-ar':iso,'hehGoal-ar.fina':final};widths={n:672 if n.endswith('.fina') else 576 for n in names}
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(closure),'placements':{}}
for n in sorted(names):
 p=rr/cc[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 if n in drawings:
  it=iter(coords[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
  new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 if n=='hehGoalHamzaabove-ar':
  new=new.replace('xOffset="112" yOffset="-336"','xOffset="176" yOffset="-224"');m['placements'][n]={'base':'hamzaabove-ar','xOffset':'176','yOffset':'-224'}
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[n]}"/>',new)
 a=E.fromstring(new);b=trees['Regular'][n];assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n]
  for stage in ['before','candidate']:
   dst=C/(stage+'-sources')/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,metrics_only=n not in drawings and n!='hehGoalHamzaabove-ar',local_placement_only=n=='hehGoalHamzaabove-ar',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'25-heh-joining/assets/after.ttf',C/'assets/before.ttf')
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared 3 Bold files; full Goal closure checked; Beh18 reserved.')
