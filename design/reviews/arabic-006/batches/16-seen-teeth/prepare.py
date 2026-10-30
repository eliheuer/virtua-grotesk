"""Bounded Bold Seen teeth and four inherited wrappers; preserve Regular and Beh."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'applied.json').exists()
roots={};contents={};reserved={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in names for co in E.parse(rr/cc[n]).findall('outline/component')}-names
  if not add:break
  names|=add
 for n in names:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
rr=roots['Bold'];cc=contents['Bold'];drawings={'seen-ar.init','seen-ar.medi'};deps=set(drawings)
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={n+s for n in ['seen-ar','sheen-ar','seenSixdots-ar'] for s in ['.init','.medi']},deps
coords={
'seen-ar.init':[(0,0),(48,0),(104,0),(136,0),(144,0),(160,0),(192,0),(256,0),(320,0),(384,0),(416,0),(448,0),(464,0),(496,0),(552,0),(608,0),(752,0),(832,80),(832,224),(832,368),(816,384),(688,384),(672,368),(672,224),(672,184),(648,160),(608,160),(568,160),(544,184),(544,224),(544,368),(528,384),(400,384),(384,368),(384,224),(384,184),(360,160),(320,160),(280,160),(256,184),(256,224),(256,368),(240,384),(112,384),(96,368),(96,240),(96,200),(56,176),(0,176),(-16,160),(-16,16)],
'seen-ar.medi':[(160,0),(208,0),(272,0),(320,0),(368,0),(400,0),(432,0),(448,0),(480,0),(528,0),(560,0),(576,0),(592,0),(608,0),(640,0),(688,0),(720,0),(736,0),(784,0),(856,0),(928,0),(928,176),(864,176),(832,200),(832,240),(832,368),(816,384),(688,384),(672,368),(672,224),(672,184),(648,160),(608,160),(568,160),(544,184),(544,224),(544,368),(528,384),(400,384),(384,368),(384,224),(384,184),(360,160),(320,160),(280,160),(256,184),(256,224),(256,368),(240,384),(112,384),(96,368),(96,240),(96,200),(56,176),(0,176),(-16,160),(-16,16),(0,0),(48,0),(96,0),(128,0),(144,0)]}
placements={n:{'base':'threedotsupabove-ar' if n.startswith('sheen') else 'threedotsdownabove-ar','xOffset':'232','yOffset':'-160'} for n in deps-drawings}
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(deps-drawings),'placements':placements}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n in drawings:
  it=iter(coords[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:
  co=placements[n];new=re.sub(r'<component base="'+co['base']+r'"[^>]*/>',f'<component base="{co["base"]}" xOffset="232" yOffset="-160"/>',new)
 width=896 if n.endswith('.init') else 928
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir();shutil.copy2(C.parent/'15-ain-isolated/assets/after.ttf',C/'assets/before.ttf')
# Recheck entire source baseline, including inherited green and manual sources.
for p,h in m['source_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
