"""Bounded Bold medial Ain/Ghain repair; preserve Regular and Beh closure."""
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
rr=roots['Bold'];cc=contents['Bold'];deps={'ain-ar.medi'}
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={'ain-ar.medi','ghain-ar.medi'},deps
pts=[(704,0),(704,176),(544,176),(536,184),(536,192),(608,288),(632,320),(640,352),(640,384),(640,464),(552,512),(448,512),(256,512),(152,512),(64,464),(64,384),(64,352),(72,320),(96,288),(168,192),(168,184),(160,176),(0,176),(-16,160),(-16,16),(0,0),
(360,192),(352,184),(344,192),(272,288),(248,320),(240,328),(240,336),(240,344),(256,352),(272,352),(432,352),(448,352),(464,344),(464,336),(464,328),(456,320),(432,288)]
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':['ghain-ar.medi'],'placements':{'ghain-ar.medi':{'base':'dotabove-ar','xOffset':'200','yOffset':'-64'}}}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n=='ain-ar.medi':
  it=iter(pts)
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:new=new.replace('<component base="dotabove-ar"/>','<component base="dotabove-ar" xOffset="200" yOffset="-64"/>')
 new=re.sub(r'<advance width="[^"]+"/>','<advance width="704"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n=='ain-ar.medi',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir();shutil.copy2(C.parent/'12-ain-initial/assets/after.ttf',C/'assets/before.ttf')
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
