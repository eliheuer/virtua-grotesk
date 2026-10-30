"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-breve-'));(S/'sources').mkdir()
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
 shutil.copy2('/tmp/latin-breve-closure.json',C/'dependencies.json')
b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items())
closure=json.loads((C/'dependencies.json').read_text());assert all(not v['green'] and not v['arabic_intersection'] for v in closure.values())
def bowl(bold):
 # Symmetric open bowl, two outer and two inner cubics, 16-unit cap cuts.
 x0,x1,x2,x3,top,bot,inside,ko,ki=(16,112,240,336,800,640,736,88,32) if bold else (32,96,256,320,784,640,704,80,48)
 pts=[(x0,top,'curve'),(x0+16,top+16,'line'),(x1-16,top+16,'line'),(x1,top,'line'),
      (x1,top-ki,None),(176-ki,inside,None),(176,inside,'curve'),
      (176+ki,inside,None),(x2,top-ki,None),(x2,top,'curve'),
      (x2+16,top+16,'line'),(x3-16,top+16,'line'),(x3,top,'line'),
      (x3,top-ko,None),(176+ko,bot,None),(176,bot,'curve'),
      (176-ko,bot,None),(x0,top-ko,None)]
 return '\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"'+(' smooth="yes"' if i in [6,15] else '') if t else '')+'/>\n' for i,(x,y,t) in enumerate(pts))+'\t\t</contour>'
changes=[]
for master,names in [('Regular',['breve','brevecomb']),('Bold',['breve','brevecomb'])]:
 d=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs');idx=plistlib.loads((R/d/'contents.plist').read_bytes())
 for name in names:
  p=d/idx[name];old=(R/p).read_text();r=E.fromstring(old)
  new=old
  if name=='breve':
   outline='\t<outline>\n'+bowl(master=='Bold')+'\n\t</outline>'
   new=re.sub(r'\t<outline>.*?</outline>',outline,new,flags=re.S)
   new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
   new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  new=new.replace('name="top" x="180" y="792"',f'name="top" x="180" y="{848 if master=="Bold" else 832}"')
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   target=C/folder/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
