"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-superior-zero-'));(S/'sources').mkdir()
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
changes=[];dependencies={}
def stage(rel,text):
 p=R/rel;before=sha(p) if p.exists() else None
 if before:
  assert before==b['sources'][rel]
  q=C/'before-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
 q=C/'candidate-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text);(S/rel).write_text(text)
 changes.append({'path':rel,'before':before,'after':sha(q)})
for master in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{master}.ufo';d=root/'glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{x.get('base') for x in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 donors={'zero','four','five','six','seven','eight','nine'};consumers=set(donors)
 while True:
  new=consumers|{n for n,v in deps.items() if v&consumers}
  if new==consumers:break
  consumers=new
 grades={}
 for n,r in rr.items():
  lib=r.find('lib/dict')
  if lib is None:continue
  g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>');rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):grades[n]=sha(d/idx[n])
 names=['zerosuperior'];assert not set(names)&set(idx)
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_reference_consumers':sorted(consumers),'green_hashes':grades,'targets':names,'existing_target_consumers':[]}
 for donor in donors:
  snap=C/'donor-sources'/str((d/idx[donor]).relative_to(R));snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes((d/idx[donor]).read_bytes())
 # New oval follows the protected zero skeleton; source bytes remain unchanged.
 for name,cp in [('zerosuperior','2070')]:
  bold=master=='Bold';advance=416 if bold else 368
  outer=([(144,376),(208,376),(272,376),(376,416),(376,576),(376,736),(272,776),(208,776),(144,776),(40,736),(40,576),(40,416)] if bold else [(120,376),(184,376),(248,376),(328,432),(328,576),(328,720),(248,776),(184,776),(120,776),(40,720),(40,576),(40,432)])
  inner=([(248,456),(208,456),(168,456),(128,496),(128,576),(128,656),(168,696),(208,696),(248,696),(288,656),(288,576),(288,496)] if bold else [(240,424),(184,424),(128,424),(96,480),(96,576),(96,672),(128,728),(184,728),(240,728),(272,672),(272,576),(272,480)])
  outline=''.join('\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(' type="curve" smooth="yes"' if i in [1,4,7,10] else '')+'/>\n' for i,(x,y) in enumerate(contour))+'\t\t</contour>\n' for contour in [outer,inner])
  text=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
\t<unicode hex="{cp}"/>
\t<advance width="{advance}"/>
\t<outline>
{outline}\t</outline>
\t<lib>
\t\t<dict>
\t\t\t<key>com.runebender.markLabel</key>
\t\t\t<string>purple</string>
\t\t\t<key>public.markColor</key>
\t\t\t<string>0.54,0.44,0.88,1</string>
\t\t</dict>
\t</lib>
</glyph>
'''
  stage(str((d/(name+'.glif')).relative_to(R)),text)
 p=d/'contents.plist';text=p.read_text().replace('</dict>',''.join('\t<key>'+n+'</key>\n\t<string>'+n+'.glif</string>\n' for n in names)+'</dict>');stage(str(p.relative_to(R)),text)
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+''.join('\n\t\t<string>'+n+'</string>' for n in names)+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>'+''.join('\n\t\t<key>'+n+'</key>\n\t\t<string>base</string>' for n in names));stage(str(p.relative_to(R)),text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
