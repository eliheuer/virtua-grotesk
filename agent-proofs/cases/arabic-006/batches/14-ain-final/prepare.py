"""Bounded Bold final Ain/Ghain repair; preserve Regular and Beh closure."""
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
rr=roots['Bold'];cc=contents['Bold'];deps={'ain-ar.fina'}
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={'ain-ar.fina','ghain-ar.fina'},deps
pts=[(344, 0), (424, 0), (472, 0), (520, 0), (552, 0), (568, 0), (600, 0), (648, 0), (696, 0), (912, 0), (912, 176), (752, 176), (744, 184), (744, 192), (816, 288), (840, 320), (848, 352), (848, 384), (848, 464), (760, 512), (656, 512), (464, 512), (360, 512), (272, 464), (272, 384), (272, 352), (280, 320), (304, 288), (376, 192), (376, 184), (368, 176), (344, 176), (168, 176), (64, 48), (64, -128), (64, -320), (232, -432), (464, -432), (704, -432), (720, -416), (720, -288), (704, -272), (464, -272), (304, -272), (224, -224), (224, -128), (224, -48), (264, 0), (568, 192), (552, 192), (488, 288), (472, 312), (464, 328), (464, 336), (464, 344), (480, 352), (496, 352), (624, 352), (640, 352), (656, 344), (656, 336), (656, 328), (648, 312), (632, 288)]
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':['ghain-ar.fina'],'placements':{'ghain-ar.fina':{'base':'dotabove-ar','xOffset':'408','yOffset':'-64'}}}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n=='ain-ar.fina':
  it=iter(pts)
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:new=re.sub(r'<component base="dotabove-ar"[^>]*/>', '<component base="dotabove-ar" xOffset="408" yOffset="-64"/>',new)
 new=re.sub(r'<advance width="[^"]+"/>','<advance width="912"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n=='ain-ar.fina',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir();shutil.copy2(C.parent/'13-ain-medial/assets/after.ttf',C/'assets/before.ttf')
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
