"""Prepare scoped Bold Waw trial; --apply checks all source hashes first."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,sys
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
counter=[(376,160),(352,176),(352,208),(352,248),(376,272),(416,272),(456,272),(480,248),(480,208),(480,168),(472,160),(416,160)]
outer=[(256,-96),(192,-80),(192,-32),(192,-16),(176,0),(48,0),(32,-16),(32,-48),(32,-176),(144,-256),(336,-256),(528,-256),(640,-160),(640,0),(640,128),(640,320),(544,432),(416,432),(288,432),(192,352),(192,224),(192,96),(288,0),(416,0),(472,0),(480,-8),(480,-24),(480,-64),(432,-96),(336,-96)]
# Final retains the 32-unit offset between Regular's isolated and final heads.
final=[(x+32,y) for x,y in outer]
final[13]=(672,-8)
final[14:15]=[(680,0),(800,0),(800,176),(680,176),(672,184)]
shapes={'waw-ar':(704,counter+outer),'waw-ar.fina':(800,[(x+32,y) for x,y in counter]+final)}
widths={'wawHamzaabove-ar':704,'wawHamzaabove-ar.fina':800}
manifest=C/'candidate.json'
if not manifest.exists():
 m={'baseline_commit':'b3cdbae3','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
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
   if n=='waw-ar.fina':
    new=new.replace('<point x="672" y="-8" type="curve" smooth="yes"/>','<point x="672" y="-8" type="curve"/>').replace('<point x="672" y="184" type="line" smooth="yes"/>','<point x="672" y="184" type="line"/>')
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
