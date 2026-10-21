"""Reconcile Tcheh forms and its exclusive dot group; hash-guarded source edits."""
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
ns=['tcheh-ar','tcheh-ar.init','tcheh-ar.medi','tcheh-ar.fina','threedotsdowncenter-ar']
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[]}
for master in roots:
 rr=roots[master];cc=contents[master];deps=set(ns)
 while True:
  add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
  if not add:break
  deps|=add
 assert deps==set(ns),deps
 for n in ns:
  p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
  assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
  if n=='threedotsdowncenter-ar':
   # Compact, symmetric circles retain the three-contour donor structure.
   radius,handle,centers=(40,24,[(176,384),(288,384),(232,288)]) if master=='Regular' else (56,32,[(160,384),(304,384),(232,264)])
   pts=[]
   for x,y in centers:pts += [(x,y+radius),(x-handle,y+radius),(x-radius,y+handle),(x-radius,y),(x-radius,y-handle),(x-handle,y-radius),(x,y-radius),(x+handle,y-radius),(x+radius,y-handle),(x+radius,y),(x+radius,y+handle),(x+handle,y+radius)]
   it=iter(pts)
   def point(mat):
    x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
   new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,old)
  else:
   suffix=n[len('tcheh-ar'):];base='hah-ar'+suffix
   offsets=({'':(200,-344),'.fina':(144,-344),'.init':(96,-504),'.medi':(96,-504)} if master=='Regular' else {'':(248,-328),'.fina':(192,-328),'.init':(104,-520),'.medi':(104,-520)})
   x,y=offsets[suffix];outline=f'<outline>\n\t\t<component base="{base}"/>\n\t\t<component base="threedotsdowncenter-ar" xOffset="{x}" yOffset="{y}"/>\n\t</outline>'
   new=re.sub(r'<outline>.*?</outline>',outline,old,flags=re.S)
   width=E.parse(rr/cc[base]).find('advance').get('width');new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  new=re.sub(r'(<key>com.runebender.markLabel</key>\s*)<string>[^<]*</string>',r'\1<string>purple</string>',new)
  new=re.sub(r'(<key>public.markColor</key>\s*)<string>[^<]*</string>',r'\1<string>0.54,0.44,0.88,1</string>',new)
  for label,data in [('before-sources',old),('candidate-sources',new)]:
   dst=C/label/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(data)
  m['glyphs'].append(dict(name=n,master=master,path=rel,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
for n in ns:
 a,b=[E.parse(C/'candidate-sources'/ (roots[k]/contents[k][n]).relative_to(R)) for k in ['Regular','Bold']]
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 assert [x.get('base') for x in a.findall('.//component')]==[x.get('base') for x in b.findall('.//component')]
(C/'assets').mkdir();shutil.copy2(C.parent/'10-hah-family/assets/after.ttf',C/'assets/before.ttf')
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
