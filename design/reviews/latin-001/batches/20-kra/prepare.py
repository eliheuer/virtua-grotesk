"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-kra-'));(S/'sources').mkdir()
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
 consumers={'k'}
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
 assert 'k' in grades and 'kgreenlandic' not in idx
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_k_consumers':sorted(consumers),'green_hashes':grades,'targets':['kgreenlandic'],'existing_target_consumers':[]}
 old=(d/idx['k']).read_text();snap=C/'donor-sources'/str((d/idx['k']).relative_to(R));snap.parent.mkdir(parents=True,exist_ok=True);snap.write_text(old)
 points=rr['k'].findall('outline/contour/point');assert len(points)==23
 import copy
 pp=[copy.deepcopy(p) for p in points]
 # New draft only: preserve branch topology, choose upper8-grid neighbors for
 # donor optical x values; shorten the four stem-cap points192 to x-height.
 for i,p in enumerate(pp):
  x=int(p.get('x'));p.set('x',str((x+7)//8*8))
  if i>=19:p.set('y',str(int(p.get('y'))-192))
 def point(p):return '\t\t\t<point '+ ' '.join(f'{k}="{p.get(k)}"' for k in ['x','y','type','smooth'] if p.get(k) is not None)+'/>'
 text=old.replace('name="k"','name="kgreenlandic"').replace('hex="006B"','hex="0138"')
 text=re.sub(r'\t\t<contour>.*?</contour>','\t\t<contour>\n'+'\n'.join(point(p) for p in pp)+'\n\t\t</contour>',text,flags=re.S)
 width=664 if master=='Bold' else 600
 text=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',text)
 text=text.replace('y="768"/>','y="576"/>')
 text=re.sub(r'\t<lib>.*?</lib>','''\t<lib>
\t\t<dict>
\t\t\t<key>com.runebender.markLabel</key>
\t\t\t<string>purple</string>
\t\t\t<key>public.markColor</key>
\t\t\t<string>0.54,0.44,0.88,1</string>
\t\t</dict>
\t</lib>''',text,flags=re.S)
 stage(str((d/'kgreenlandic.glif').relative_to(R)),text)
 p=d/'contents.plist';stage(str(p.relative_to(R)),p.read_text().replace('</dict>','\t<key>kgreenlandic</key>\n\t<string>kgreenlandic.glif</string>\n</dict>'))
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+'\n\t\t<string>kgreenlandic</string>'+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>\n\t\t<key>kgreenlandic</key>\n\t\t<string>base</string>');stage(str(p.relative_to(R)),text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
