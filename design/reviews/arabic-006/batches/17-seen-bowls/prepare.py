"""Bounded Bold Seen bowls and four inherited wrappers; preserve Regular and Beh."""
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
rr=roots['Bold'];cc=contents['Bold'];drawings={'seen-ar','seen-ar.fina'};deps=set(drawings)
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={n+s for n in ['seen-ar','sheen-ar','seenSixdots-ar'] for s in ['','.fina']},deps
coords={
'seen-ar':[(800,-152),(800,-8),(808,0),(824,0),(840,0),(864,0),(896,0),(944,0),(976,0),(992,0),(1024,0),(1088,0),(1152,0),(1296,0),(1376,80),(1376,224),(1376,368),(1360,384),(1232,384),(1216,368),(1216,224),(1216,184),(1192,160),(1152,160),(1112,160),(1088,184),(1088,224),(1088,368),(1072,384),(944,384),(928,368),(928,224),(928,184),(904,160),(864,160),(824,160),(800,184),(800,224),(800,368),(784,384),(656,384),(640,368),(640,48),(640,-48),(552,-96),(416,-96),(288,-96),(224,-48),(224,32),(224,160),(208,176),(80,176),(64,160),(64,32),(64,-144),(176,-256),(416,-256),(656,-256)],
'seen-ar.fina':[(64,16),(64,-160),(176,-256),(320,-256),(480,-256),(672,-256),(800,-192),(800,-16),(800,-8),(808,0),(824,0),(840,0),(864,0),(896,0),(944,0),(976,0),(992,0),(1024,0),(1088,0),(1152,0),(1184,0),(1232,0),(1264,0),(1280,0),(1328,0),(1400,0),(1472,0),(1472,176),(1408,176),(1376,200),(1376,240),(1376,368),(1360,384),(1232,384),(1216,368),(1216,224),(1216,184),(1192,160),(1152,160),(1112,160),(1088,184),(1088,224),(1088,368),(1072,384),(944,384),(928,368),(928,224),(928,184),(904,160),(864,160),(824,160),(800,184),(800,224),(800,368),(784,384),(656,384),(640,368),(640,48),(640,-48),(592,-96),(480,-96),(352,-96),(272,-96),(224,-64),(224,32),(224,160),(208,176),(80,176),(64,160),(64,48)]}
placements={n:{'base':'threedotsupabove-ar' if n.startswith('sheen') else 'threedotsdownabove-ar','xOffset':'776','yOffset':'-160'} for n in deps-drawings}
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
  co=placements[n];new=re.sub(r'<component base="'+co['base']+r'"[^>]*/>',f'<component base="{co["base"]}" xOffset="776" yOffset="-160"/>',new)
 width=1472 if n.endswith('.fina') else 1440
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir();shutil.copy2(C.parent/'16-seen-teeth/assets/after.ttf',C/'assets/before.ttf')
# Recheck entire source baseline, including inherited green and manual sources.
for p,h in m['source_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
