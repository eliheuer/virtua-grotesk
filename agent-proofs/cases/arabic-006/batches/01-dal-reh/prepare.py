"""Prepare scoped Bold Dal/Reh trial; --apply checks all source hashes first."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,sys
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shapes={
'dal-ar':(616,[(360,0),(488,0),(552,64),(552,200),(552,416),(536,432),(400,432),(384,416),(384,216),(384,192),(368,176),(344,176),(272,176),(248,176),(232,192),(232,216),(232,288),(216,304),(80,304),(64,288),(64,200),(64,64),(128,0),(256,0)]),
'dal-ar.fina':(528,[(240,-16),(296,-16),(352,16),(384,64),(392,64),(408,24),(448,0),(488,0),(528,0),(528,176),(512,176),(488,176),(472,200),(472,240),(472,368),(368,448),(256,448),(208,448),(192,432),(192,304),(208,288),(240,288),(280,288),(312,264),(312,224),(312,184),(288,152),(248,152),(224,152),(200,168),(200,200),(200,224),(184,240),(48,240),(32,224),(32,200),(32,72),(128,-16)]),
'reh-ar':(672,[(536,0),(536,416),(520,432),(384,432),(368,416),(368,32),(368,-56),(328,-96),(232,-96),(48,-96),(32,-112),(32,-240),(48,-256),(248,-256),(448,-256),(536,-168)]),
'reh-ar.fina':(640,[(640,0),(640,176),(552,176),(536,192),(536,320),(520,336),(384,336),(368,320),(368,32),(368,-56),(328,-96),(232,-96),(48,-96),(32,-112),(32,-240),(48,-256),(248,-256),(448,-256),(536,-144),(536,-16),(536,-8),(544,0)])}
# Match the inherited advance to its base; old wrapper advances clipped or
# extended joining origins. Anchors/offsets and donor drawings stay unchanged.
widths={'thal-ar':616,'jeh-ar':672,'rreh-ar':672,'zain-ar':672,'zain-ar.fina':640}
manifest=C/'candidate.json'
if not manifest.exists():
 m={'baseline_commit':'05b8d2e1','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
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
