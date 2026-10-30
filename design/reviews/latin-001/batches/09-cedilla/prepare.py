"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-cedilla-'));(S/'sources').mkdir()
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
 # A short diagonal neck leads into concentric right-hand turns. The open
 # left aperture and terminal landings distinguish this from a comma below.
 if master=='Regular':
  pts=[(80,-224,'line'),(144,-224,'line'),(192,-224,None),(224,-192,None),(224,-144,'curve'),(224,-96,None),(192,-64,None),(144,-64,'curve'),(112,-64,'line'),(160,-16,'line'),(160,0,'line'),(112,0,'line'),(64,-48,'line'),(64,-96,'line'),(80,-112,'line'),(144,-112,'line'),(160,-112,None),(176,-128,None),(176,-144,'curve'),(176,-160,None),(160,-176,None),(144,-176,'curve'),(80,-176,'line'),(64,-192,'line'),(64,-208,'line')]
  bottom=-256
 else:
  pts=[(80,-256,'line'),(144,-256,'line'),(200,-256,None),(240,-216,None),(240,-160,'curve'),(240,-104,None),(200,-64,None),(144,-64,'curve'),(112,-64,'line'),(160,-16,'line'),(160,0,'line'),(96,0,'line'),(32,-64,'line'),(32,-112,'line'),(48,-128,'line'),(144,-128,'line'),(160,-128,None),(176,-144,None),(176,-160,'curve'),(176,-176,None),(160,-192,None),(144,-192,'curve'),(80,-192,'line'),(64,-208,'line'),(64,-240,'line')]
  bottom=-288
 for name in ['cedilla','cedillacomb']:
  p=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif');old=(R/p).read_text();new=old
  if name=='cedilla':
   outline='\t<outline>\n\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"' if t else '')+(' smooth="yes"' if i in [1,4,7,15,18,21] else '')+'/>\n' for i,(x,y,t) in enumerate(pts))+'\t\t</contour>\n\t</outline>'
   new=re.sub(r'\t<outline>.*?</outline>',outline,new,flags=re.S)
   new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
   new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  new=new.replace('name="bottom" x="134" y="-200"',f'name="bottom" x="134" y="{bottom}"')
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p)})
# Newly deep repeated below marks require clipping protection, not line spacing.
for master in ['Regular','Bold']:
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/fontinfo.plist');old=(R/p).read_text();new=old.replace('<key>openTypeOS2WinDescent</key>\n\t<integer>512</integer>','<key>openTypeOS2WinDescent</key>\n\t<integer>576</integer>');assert old!=new
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'master':master,'before':sha(R/p),'after':sha(S/p)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
