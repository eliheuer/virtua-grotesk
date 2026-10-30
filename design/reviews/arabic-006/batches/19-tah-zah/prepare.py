"""Bounded Bold Tah/Zah family; preserve Regular geometry and Beh."""
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
rr=roots['Bold'];cc=contents['Bold'];drawings={'tah-ar'+s for s in ['', '.init','.medi','.fina']};deps=set(drawings)
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={n+s for n in ['tah-ar','zah-ar'] for s in ['', '.init','.medi','.fina']},deps
iso=[(80,0),(984,0),(1000,16),(1000,224),(1000,368),(920,448),(776,448),(512,448),(368,448),(360,456),(360,752),(344,768),(216,768),(200,752),(200,168),(192,160),(80,160),(64,144),(64,16),(368,160),(360,168),(360,280),(368,288),(776,288),(816,288),(840,264),(840,224),(840,168),(832,160)]
# Preserve Regular's extra shoulder segments as collinear runs at Bold's crown.
neck=[(448,448),(416,448),(384,448),(352,448),(336,448),(328,448),(320,448),(312,448),(304,448),(296,448),(296,448),(288,456),(288,752),(272,768),(144,768),(128,752),(128,240),(128,200),(80,176),(0,176),(-16,160),(-16,16)]
# Avoid duplicate endpoint/handle: the final cubic remains a straight horizontal run.
neck[8:11]=[(304,448),(304,448),(296,448)]
init=[(0,0),(704,0),(848,0),(928,80),(928,224),(928,368),(848,448),(704,448)]+neck
medi=[(0,0),(1024,0),(1024,176),(944,176),(928,192),(928,200),(928,208),(928,224),(928,368),(848,448),(704,448)]+neck
final=list(medi);final[0]=(80,0);final[-4:]=[(104,176),(80,176),(64,160),(64,16)]
counter=[(288,200),(288,248),(288,272),(304,288),(328,288),(728,288),(752,288),(768,272),(768,248),(768,200),(768,176),(752,160),(728,160),(328,160),(304,160),(288,176)]
coords={'tah-ar':iso,'tah-ar.init':init+counter,'tah-ar.medi':medi+counter,'tah-ar.fina':final+counter}
placements={n:{'base':'dotabove-ar','xOffset':str(448 if n=='zah-ar' else 376),'yOffset':'-128'} for n in deps-drawings}
widths={'.init':992,'.medi':1024,'.fina':1024,'':1064}
def insert_regular(text):
 return text.replace('<point x="192" y="184" type="curve" smooth="yes"/>','<point x="192" y="184" type="curve" smooth="yes"/>\n\t\t\t<point x="192" y="192" type="line"/>')
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(deps-drawings),'placements':placements}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n in drawings and n!='tah-ar':
  new=new.replace('<point x="228" y="184" type="curve" smooth="yes"/>','<point x="228" y="184" type="curve"/>\n\t\t\t<point x="228" y="192" type="line"/>')
 if n in drawings:
  it=iter(coords[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:
  co=placements[n];new=re.sub(r'<component base="'+co['base']+r'"[^>]*/>',f'<component base="{co["base"]}" xOffset="{co["xOffset"]}" yOffset="{co["yOffset"]}"/>',new)
 width=widths[next((x for x in ['.init','.medi','.fina'] if n.endswith(x)), '')]
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);reg=(roots['Regular']/contents['Regular'][n]).read_text()
 if n in drawings and n!='tah-ar':reg=insert_regular(reg)
 b=E.ElementTree(E.fromstring(reg));assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,before_sha256=sha(p),candidate_sha256=sha(dst)))
# Exact geometry-neutral Regular additions and isolated wrapper metric repair.
for n in ['tah-ar.init','tah-ar.medi','tah-ar.fina','zah-ar']:
 p=roots['Regular']/contents['Regular'][n];rel=str(p.relative_to(R));old=p.read_text();new=old
 assert '<string>orange</string>' in old and rel not in reserved
 if n.startswith('tah-ar'):new=insert_regular(new)
 else:
  base=E.fromstring(old).find('outline/component').get('base')
  width=E.parse(roots['Regular']/contents['Regular'][base]).find('advance').get('width')
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Regular',drawing=False,metrics_only=n=='zah-ar',collinear_only=n!='zah-ar',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'18-sad-dad/assets/after.ttf',C/'assets/before.ttf')
# Recheck entire source baseline, including inherited green and manual sources.
for p,h in m['source_hashes'].items():assert sha(R/p)==h
# Application follows candidate geometry checks.
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
