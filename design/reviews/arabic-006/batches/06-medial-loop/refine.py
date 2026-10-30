from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil
R=Path.cwd();C=R/'agent-proofs/cases/arabic-006/batches/06-medial-loop';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((C/'applied.json').read_text());t=C/'trial-01';t.mkdir(exist_ok=True)
for p in [C/'feh-700.png',C/'feh-700.json',C/'assets/after.ttf',R/'sources/VirtuaGrotesk-Bold.ufo/glyphs/fehD_otless-ar.medi.glif']:shutil.copy2(p,t/p.name)
root=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes())
medi=E.parse(root/cs['fehDotless-ar.medi']);points=medi.findall('outline/contour')[1].findall('point')
for i in [0,1,11]:points[i].set('y','248')
mp=[(int(p.get('x')),int(p.get('y'))) for p in medi.findall('outline/contour/point')]
outer=mp[:21];counter=mp[21:]
fp=[(272,0),(552,0),(600,0),(640,0),(680,0),(688,0),(736,0),(800,0),(848,0),(1056,0),(1056,176)]+[(x+448,y) for x,y in outer[2:17]]+[(272,176),(224,176),(192,208),(192,256),(192,304),(176,320),(48,320),(32,304),(32,256),(32,112),(112,0)]+[(x+448,y) for x,y in counter]
shapes={'fehDotless-ar.medi':mp,'fehDotless-ar.fina':fp}
deps=set(shapes)
while True:
 add={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
m['inherited_bold_glyphs']=sorted(deps-set(shapes))
for n in sorted(deps):
 p=root/cs[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 assert rel not in m['reserved_beh_hashes']
 assert '<string>green</string>' not in old,n
 if n in shapes:
  it=iter(shapes[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 elif n.endswith('.fina'):
  co=E.fromstring(old).findall('outline/component')
  if len(co)>1 and co[1].get('base') in ['dotabove-ar','twodotshorizontalabove-ar','threedotsupabove-ar']:
   attrs=dict(co[1].attrib);attrs['yOffset']=str(int(attrs.get('yOffset','0'))+88)
   new=re.sub('<component base="'+attrs['base']+'"[^>]*/>',lambda _: '<component '+' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>',new);m['placements'][n]=attrs
 if new==old:continue
 prev=next((g for g in m['glyphs'] if g['name']==n),None)
 if prev:assert sha(p)==prev['candidate_sha256']
 else:
  assert sha(p)==m['source_hashes'][rel]
  for master in ['Regular','Bold']:
   src=R/rel.replace('-Bold','-'+master);dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
  prev=dict(name=n,path=rel,drawing=n in shapes,before_sha256=sha(p));m['glyphs'].append(prev)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new);prev['candidate_sha256']=sha(dst)
 p.write_text(new)
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for f in ['applied.json','candidate.json']:(C/f).write_text(json.dumps(m,indent=2)+'\n')
(C/'refinement.json').write_text(json.dumps({'reason':'Shorten over-tapered counter; extend the same correction to the final Feh head','shapes':shapes},indent=2)+'\n')
print(len(m['glyphs']),'source files;',len(deps),'affected glyphs; Beh components preserved.')
