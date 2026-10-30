"""Bounded Bold isolated Ain/Ghain repair; preserve Regular and Beh closure."""
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
rr=roots['Bold'];cc=contents['Bold'];deps={'ain-ar'}
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={'ain-ar','ghain-ar'},deps
pts=[(216, -240), (416, -240), (704, -240), (720, -224), (720, -96), (704, -80), (416, -80), (296, -80), (224, -48), (224, 0), (224, 56), (296, 96), (416, 96), (624, 96), (640, 112), (640, 240), (624, 256), (448, 256), (384, 256), (352, 312), (352, 384), (352, 424), (384, 448), (416, 448), (448, 448), (480, 424), (480, 384), (496, 368), (624, 368), (640, 384), (640, 512), (544, 608), (416, 608), (288, 608), (192, 512), (192, 384), (192, 336), (208, 304), (240, 272), (240, 256), (224, 256), (144, 256), (64, 144), (64, 0), (64, -160)]
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':['ghain-ar'],'placements':{'ghain-ar':{'base':'dotabove-ar','xOffset':'264','yOffset':'32'}}}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n=='ain-ar':
  it=iter(pts)
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:new=re.sub(r'<component base="dotabove-ar"[^>]*/>', '<component base="dotabove-ar" xOffset="264" yOffset="32"/>',new)
 new=re.sub(r'<advance width="[^"]+"/>','<advance width="784"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n=='ain-ar',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir();shutil.copy2(C.parent/'14-ain-final/assets/after.ttf',C/'assets/before.ttf')
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
