"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-latvian-'));(S/'sources').mkdir()
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
 shutil.copy2('/tmp/latin-latvian-closure.json',C/'dependencies.json')
b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items())
closure=json.loads((C/'dependencies.json').read_text());assert all(not v['green'] and not v['arabic_intersection'] for v in closure.values())
names=['Gcommaaccent','gcommaaccent','Kcommaaccent','kcommaaccent','Lcommaaccent','lcommaaccent','Ncommaaccent','ncommaaccent','Rcedilla','rcedilla']
changes=[]
for master in ['Regular','Bold']:
 d=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs');idx=plistlib.loads((R/d/'contents.plist').read_bytes())
 for name in names:
  p=d/idx[name];old=(R/p).read_text();r=E.fromstring(old);mark=r.find("outline/component[@base='cedilla']");assert mark is not None
  if name=='gcommaaccent':
   offset=448 if master=='Regular' else 488
   new=old
   new=re.sub(r'<component base="cedilla"[^>]+/>',f'<component base="commaaccent" xScale="-1" yScale="-1" xOffset="{offset}" yOffset="576"/>',new)
   ax=312 if master=='Regular' else 352;bottom=-216 if master=='Regular' else -240
   new=new.replace('\t</outline>','\t</outline>\n'+f'\t<anchor name="top" x="{ax}" y="800"/>\n\t<anchor name="bottom" x="{ax}" y="{bottom}"/>')
  else:
   offset=8*round((int(mark.get('xOffset','0'))-6)/8)
   new=re.sub(r'<component base="cedilla"[^>]+/>',f'<component base="commaaccent" xOffset="{offset}"/>',old)
  # A changed composite construction is an AI draft; frozen base/donor grades remain untouched.
  if 'com.runebender.markLabel' in new:new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
  else:new=new.replace('\t\t<dict>','\t\t<dict>\n\t\t\t<key>com.runebender.markLabel</key>\n\t\t\t<string>purple</string>')
  new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   target=C/folder/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p)})
# Canonical decomposition must retain the language-specific mark construction
# when a serving subset omits the precomposed cmap entries.
for master in ['Regular','Bold']:
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/features.fea');old=(R/p).read_text()
 rules='\n'.join('\t\tsub '+base+' cedillacomb by '+name+';' for base,name in zip('GgKkLlNnRr',names))
 new=old.replace('\t} ccmp_latin_extended;',rules+'\n\t} ccmp_latin_extended;')
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  target=C/folder/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'master':master,'before':sha(R/p),'after':sha(S/p)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
