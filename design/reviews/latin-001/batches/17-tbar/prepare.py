"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-tbar-'));(S/'sources').mkdir()
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
 consumers={'T','t'}
 while True:
  new=consumers|{n for n,v in deps.items() if v&consumers}
  if new==consumers:break
  consumers=new
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_base_consumers':sorted(consumers),'base_hashes':{n:sha(d/idx[n]) for n in ['T','t']},'targets':['Tbar','tbar'],'existing_target_consumers':[]}
 isbold=master=='Bold'
 # Local bars only. The T/t components and every existing source glyph are frozen.
 specs=[('Tbar','T',0x166,'T_bar.glif',648 if isbold else 680,(112,288,536,416) if isbold else (128,304,552,400),(320,768)),('tbar','t',0x167,'tbar.glif',416 if isbold else 376,(24,248,392,344) if isbold else (32,288,344,352),(200,736) if isbold else (168,696))]
 for name,base,cp,filename,width,box,top in specs:
  assert name not in idx and filename.casefold() not in {f.casefold() for f in idx.values()}
  if name=='Tbar' and not isbold:top=(336,768)
  x0,y0,x1,y1=box;pts=[(x0+16,y0),(x1-16,y0),(x1,y0+16),(x1,y1-16),(x1-16,y1),(x0+16,y1),(x0,y1-16),(x0,y0+16)]
  points='\n'.join(f'\t\t\t<point x="{x}" y="{y}" type="line"/>' for x,y in pts)
  text=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
\t<unicode hex="{cp:04X}"/>
\t<advance width="{width}"/>
\t<outline>
\t\t<component base="{base}"/>
\t\t<contour>
{points}
\t\t</contour>
\t</outline>
\t<anchor name="top" x="{top[0]}" y="{top[1]}"/>
\t<anchor name="bottom" x="{top[0]}" y="0"/>
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
  stage(str((d/filename).relative_to(R)),text)
 p=d/'contents.plist';text=p.read_text();entries=''.join(f'\t<key>{n}</key>\n\t<string>{f}</string>\n' for n,_,_,f,_,_,_ in specs);stage(str(p.relative_to(R)),text.replace('</dict>',entries+'</dict>'))
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+''.join(f'\n\t\t<string>{n}</string>' for n,_,_,_,_,_,_ in specs)+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>'+''.join(f'\n\t\t<key>{n}</key>\n\t\t<string>base</string>' for n,_,_,_,_,_,_ in specs))
 stage(str(p.relative_to(R)),text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
