"""Prepare round Bold Arabic single dots, preserving all placement and Regular."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,math
R=Path(__file__).resolve().parents[4];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'candidate.json').exists()
m={'baseline_commit':'211c3b8d','baseline_note':'ARB-005 base trial already applied; accepted as an improvement, dots corrected next.','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
for master in ['Regular','Bold']:
 p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';contents=plistlib.loads((p/'contents.plist').read_bytes())
 for n in ['dotbelow-ar','dotabove-ar']:
  path=p/contents[n];rel=path.relative_to(R);old=path.read_text()
  q=C/'before-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(path.read_bytes())
  if master=='Regular':continue
  assert '<string>red</string>' in old
  cx,cy=(120,-192) if n=='dotbelow-ar' else (152,768)
  r,h=112,64
  points=[(cx,cy-r),(cx+h,cy-r),(cx+r,cy-h),(cx+r,cy),(cx+r,cy+h),(cx+h,cy+r),(cx,cy+r),(cx-h,cy+r),(cx-r,cy+h),(cx-r,cy),(cx-r,cy-h),(cx-h,cy-r)]
  if n=='dotbelow-ar':points=points[-1:]+points[:-1]
  it=iter(points)
  def pt(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',pt,old)
  assert next(it,None) is None
  new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
  q=C/'candidate-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(new)
  m['glyphs'].append(dict(name=n,path=str(rel),before_sha256=sha(path),candidate_sha256=sha(q),center=[cx,cy],radius=r,handle=h))
p=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';contents=plistlib.loads((p/'contents.plist').read_bytes());deps={g['name'] for g in m['glyphs']}
while True:
 new={n for n,f in contents.items() if any(x.get('base') in deps for x in E.parse(p/f).findall('.//component'))}-deps
 if not new:break
 deps|=new
for n in deps:assert '<string>green</string>' not in (p/contents[n]).read_text(),n
m['dependency_closure']=sorted(deps)
(C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf');shutil.copy2(R/'OFL.txt',C/'assets/Virtua-OFL.txt')
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
for p,h in m['source_hashes'].items():assert sha(R/p)==h,p
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied two Bold single-dot donors;',len(deps),'glyphs in dependency closure; Regular preserved.')
