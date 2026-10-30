"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-comma-'));(S/'sources').mkdir()
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
for master in ['Regular','Bold']:
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/commaaccent.glif');old=(R/p).read_text()
 pts=[(112,-200),(144,-200),(160,-184),(192,-56),(176,-40),(144,-40),(128,-56),(96,-184)] if master=='Regular' else [(96,-200),(160,-200),(176,-184),(208,-56),(192,-40),(128,-40),(112,-56),(80,-184)]
 outline='\t<outline>\n\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}" type="line"/>\n' for x,y in pts)+'\t\t</contour>\n\t</outline>'
 new=re.sub(r'\t<outline>.*?</outline>',outline,old,flags=re.S)
 new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
 new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'glyph':'commaaccent','master':master,'before':sha(R/p),'after':sha(S/p)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
