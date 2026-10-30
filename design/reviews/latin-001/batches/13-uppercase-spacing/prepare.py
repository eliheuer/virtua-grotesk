"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-uppercase-spacing-'));(S/'sources').mkdir()
 for p in (R/'sources').iterdir():
  if p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']:shutil.copytree(p,S/'sources'/p.name)
  elif p.is_file():shutil.copy2(p,S/'sources'/p.name)
 for n in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/n,S/n)
 shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv')
 (C/'assets').mkdir(exist_ok=True)
 for n,src in [('before',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parents[1]/'assets/rubik.ttf')]:shutil.copy2(src,C/'assets'/f'{n}.ttf')
 shutil.copytree(R/'fonts',C/'baseline-fonts')
 sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
 (C/'baseline.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'scratch':str(S),'sources':sources},indent=2)+'\n')

b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items())
closure=json.loads((C/'dependencies.json').read_text());assert all(not v['green'] and not v['arabic_intersection'] for v in closure.values())
changes=[]
for master,v in closure.items():
 for name,t in v['targets'].items():
  p=Path(t['path']);old=(R/p).read_text();width=int(t['after_width'])
  new=re.sub(r'<advance width="[^\"]+"/>',f'<advance width="{width}"/>',old)
  assert new!=old
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   dest=C/folder/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p),'before_width':t['before_width'],'after_width':width,'kind':'advance-only match to unchanged base; human grade preserved'})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
