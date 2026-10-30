"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-filig-'));(S/'sources').mkdir()
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
 consumers={'f','i','l'}
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
 assert 'f' in grades and 'i' in grades and not {'fi','fl'} & set(idx)
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_donor_consumers':sorted(consumers),'green_hashes':grades,'targets':['fi','fl'],'existing_target_consumers':[]}
 for donor in ['f','i','l']:
  snap=C/'donor-sources'/str((d/idx[donor]).relative_to(R));snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes((d/idx[donor]).read_bytes())
 import copy
 for name,cp in [('fi','FB01'),('fl','FB02')]:
  f=copy.deepcopy(rr['f'].find('outline/contour'));pp=f.findall('point')
  # Extend both crossbar edges into the second stem by32 units. Compiler unions.
  shift=(320 if name=='fi' else 352) if master=='Bold' else 288
  for j in [6,9]:pp[j].set('x',str(shift+88))
  for j in [7,8]:pp[j].set('x',str(shift+104))
  if name=='fi':
   end=584 if master=='Bold' else 456
   for j in [16,19]:pp[j].set('x',str(end-16))
   for j in [17,18]:pp[j].set('x',str(end))
   second=copy.deepcopy(rr['i'].findall('outline/contour')[1]);width=656 if master=='Bold' else 528
  else:
   second=copy.deepcopy(rr['l'].find('outline/contour'));width=672 if master=='Bold' else 560
  for p in second:p.set('x',str(int(p.get('x'))+shift))
  def contour(c):return '\t\t<contour>\n'+'\n'.join('\t\t\t<point '+' '.join(f'{k}="{p.get(k)}"' for k in ['x','y','type','smooth'] if p.get(k) is not None)+'/>' for p in c)+'\n\t\t</contour>'
  x1=216 if master=='Bold' else 184
  x2=(488 if master=='Bold' else 408) if name=='fi' else (536 if master=='Bold' else 448)
  text=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
\t<unicode hex="{cp}"/>
\t<advance width="{width}"/>
\t<outline>
{contour(f)}
{contour(second)}
\t</outline>
\t<anchor name="top_1" x="{x1}" y="768"/>
\t<anchor name="top_2" x="{x2}" y="768"/>
\t<anchor name="bottom_1" x="{x1}" y="0"/>
\t<anchor name="bottom_2" x="{x2}" y="0"/>
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
  stage(str((d/f'{name}.glif').relative_to(R)),text)
 p=d/'contents.plist';stage(str(p.relative_to(R)),p.read_text().replace('</dict>','\t<key>fi</key>\n\t<string>fi.glif</string>\n\t<key>fl</key>\n\t<string>fl.glif</string>\n</dict>'))
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+'\n\t\t<string>fi</string>\n\t\t<string>fl</string>'+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>\n\t\t<key>fi</key>\n\t\t<string>ligature</string>\n\t\t<key>fl</key>\n\t\t<string>ligature</string>');stage(str(p.relative_to(R)),text)
 p=root/'features.fea';text=p.read_text();assert 'feature liga' not in text
 text+='\n# Latin standard ligatures; intervening marks prevent replacement.\nfeature liga {\n\tlookup LATIN_F_LIGATURES {\n\t\tlookupflag 0;\n\t\tsub f i by fi;\n\t\tsub f l by fl;\n\t} LATIN_F_LIGATURES;\n\tscript DFLT;\n\tlanguage dflt;\n\tlookup LATIN_F_LIGATURES;\n\tscript latn;\n\tlanguage dflt;\n\tlookup LATIN_F_LIGATURES;\n} liga;\n'
 stage(str(p.relative_to(R)),text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
