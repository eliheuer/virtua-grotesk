"""Prepare scoped Bold Noon trial; --apply checks all source hashes first."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,sys
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shapes={
'noonghunna-ar':(752,[(32,144),(32,-72),(144,-192),(344,-192),(544,-192),(656,-72),(656,144),(656,304),(640,320),(504,320),(488,304),(488,144),(488,24),(432,-32),(344,-32),(256,-32),(200,24),(200,144),(200,304),(184,320),(48,320),(32,304)]),
'noonghunna-ar.fina':(784,[(32,32),(32,-128),(144,-256),(344,-256),(544,-256),(656,-128),(656,-8),(664,0),(784,0),(784,176),(664,176),(656,184),(656,304),(640,320),(504,320),(488,304),(488,32),(488,-56),(432,-96),(344,-96),(256,-96),(200,-56),(200,32),(200,160),(184,176),(48,176),(32,160)])}
widths={'noon-ar':752,'noon-ar.fina':784}
manifest=C/'candidate.json'
if not manifest.exists():
 m={'baseline_commit':'da883a7c','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
 root=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes())
 deps=set(shapes)
 while True:
  added={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
  if not added:break
  deps|=added
 for n in deps:assert '<string>green</string>' not in (root/cs[n]).read_text(),n
 for n in shapes.keys()|widths.keys():
  p=root/cs[n];rel=p.relative_to(R);old=p.read_text();new=old
  for master in ['Regular','Bold']:
   src=R/str(rel).replace('-Bold','-'+master);dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
  assert '<string>green</string>' not in old
  if n in shapes:
   width,pts=shapes[n];assert '<string>red</string>' in old
   it=iter(pts)
   def point(mat):
    x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
   new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
   new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
  else:width=widths[n]
  if n=='noon-ar.fina':
   new=new.replace('<component base="dotabove-ar" xOffset="248" yOffset="-456"/>','<component base="dotabove-ar" xOffset="192" yOffset="-288"/>')
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  reg=E.parse(R/str(rel).replace('-Bold','-Regular'));draft=E.fromstring(new)
  assert [[x.get('type') for x in c] for c in reg.findall('outline/contour')]==[[x.get('type') for x in c] for c in draft.findall('outline/contour')]
  dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
  m['glyphs'].append(dict(name=n,path=str(rel),drawing=n in shapes,before_sha256=sha(p),candidate_sha256=sha(dst)))
 m['inherited_bold_glyphs']=sorted(deps-set(shapes));manifest.write_text(json.dumps(m,indent=2)+'\n')
 (C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf')
 print('Prepared',len(shapes),'outlines and',len(widths),'wrapper widths; all Regular preserved.')
if '--apply' in sys.argv:
 m=json.loads(manifest.read_text());assert not (C/'applied.json').exists()
 for p,h in m['source_hashes'].items():assert sha(R/p)==h,('external source edit',p)
 for g in m['glyphs']:assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
 for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
 (C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied exact hash-checked candidate.')
