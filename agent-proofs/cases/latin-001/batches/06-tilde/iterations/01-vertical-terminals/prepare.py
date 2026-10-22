"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-tilde-'));(S/'sources').mkdir()
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
 shutil.copy2('/tmp/latin-tilde-closure.json',C/'dependencies.json')
b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items())
closure=json.loads((C/'dependencies.json').read_text());assert all(not v['green'] and not v['arabic_intersection'] for v in closure.values())
def bowl(bold):
 h=96 if bold else 64
 # Paired waves with horizontal tangents at crest and trough, clipped terminal ends.
 pts=[(80,640,'line'),(104,640,None),(104,704,None),(160,704,'curve'),
 (216,704,None),(264,640,None),(320,640,'curve'),
 (376,640,None),(376,704,None),(400,704,'curve'),
 (416,720,'line'),(416,688+h,'line'),(400,704+h,'line'),
 (376,704+h,None),(376,640+h,None),(320,640+h,'curve'),
 (264,640+h,None),(216,704+h,None),(160,704+h,'curve'),
 (104,704+h,None),(104,640+h,None),(80,640+h,'curve'),
 (64,624+h,'line'),(64,656,'line')]
 return '\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"'+(' smooth="yes"' if i in [3,6,15,18] else '') if t else '')+'/>\n' for i,(x,y,t) in enumerate(pts))+'\t\t</contour>'
changes=[]
for master,names in [('Regular',['tilde','tildecomb']),('Bold',['tilde','tildecomb'])]:
 d=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs');idx=plistlib.loads((R/d/'contents.plist').read_bytes())
 for name in names:
  p=d/idx[name];old=(R/p).read_text();r=E.fromstring(old)
  new=old
  if name=='tilde':
   outline='\t<outline>\n'+bowl(master=='Bold')+'\n\t</outline>'
   new=re.sub(r'\t<outline>.*?</outline>',outline,new,flags=re.S)
   new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
   new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  new=new.replace('name="top" x="240" y="826"',f'name="top" x="240" y="{832 if master=="Bold" else 800}"')
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   target=C/folder/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
