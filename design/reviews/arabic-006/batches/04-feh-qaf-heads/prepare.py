"""Prepare scoped Bold initial/medial Feh-Qaf trial; --apply checks all source hashes first."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,sys
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shapes={'fehDotless-ar.init': (544, [(232, 384), (192, 400), (192, 448), (192, 488), (216, 512), (256, 512), (312, 512), (352, 464), (352, 408), (352, 392), (344, 384), (304, 384), (0, 176), (-16, 160), (-16, 16), (0, 0), (216, 0), (408, 0), (512, 80), (512, 248), (512, 352), (512, 552), (408, 672), (256, 672), (120, 672), (32, 600), (32, 448), (32, 312), (144, 224), (304, 224), (344, 224), (352, 216), (352, 208), (352, 192), (312, 176), (216, 176)]), 'fehDotless-ar.medi': (560, [(560, 0), (560, 176), (344, 176), (344, 184), (432, 200), (496, 264), (496, 328), (496, 456), (400, 568), (272, 568), (144, 568), (48, 456), (48, 328), (48, 264), (112, 200), (200, 184), (200, 176), (0, 176), (-16, 160), (-16, 16), (0, 0), (272, 216), (232, 216), (200, 264), (200, 328), (200, 376), (232, 408), (272, 408), (312, 408), (344, 376), (344, 328), (344, 264), (312, 216)])}
widths={'feh-ar.init': 544, 'feh-ar.medi': 560, 'fehDotmovedbelow-ar.init': 544, 'fehDotmovedbelow-ar.medi': 560, 'fehThreedotsbelow-ar.init': 544, 'fehThreedotsbelow-ar.medi': 560, 'qaf-ar.init': 544, 'qaf-ar.medi': 560, 'qafDotabove-ar.init': 544, 'qafDotabove-ar.medi': 560, 'qafThreedotsabove-ar.init': 544, 'qafThreedotsabove-ar.medi': 560, 'veh-ar.init': 544, 'veh-ar.medi': 560}
manifest=C/'candidate.json'
if not manifest.exists():
 m={'baseline_commit':'1f7dc7f6','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
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
  if n in widths and 'below' not in n:
   # Above-dot roots are preserved; only wrapper placement changes.
   def component(mat):
    elem=E.fromstring(mat[0]);dx,dy=(32,64) if n.endswith('.init') else (-32,104)
    elem.set('xOffset',str(int(elem.get('xOffset','0'))+dx))
    elem.set('yOffset',str(int(elem.get('yOffset','0'))+dy))
    return E.tostring(elem,encoding='unicode').replace(' />','/>')
   new=re.sub(r'<component base="(?:dotabove-ar|twodotshorizontalabove-ar|threedotsupabove-ar)"[^>]*/>',component,new)
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
