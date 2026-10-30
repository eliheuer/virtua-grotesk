from pathlib import Path
import shutil,json,hashlib,plistlib,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert all(sha(R/p)==h for p,h in b['sources'].items())
if 'scratch' not in b:
 S=Path(tempfile.mkdtemp(prefix='virtua-ligature-carets-'));(S/'sources').mkdir()
 for p in (R/'sources').iterdir():
  if p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']:shutil.copytree(p,S/'sources'/p.name)
  elif p.is_file():shutil.copy2(p,S/'sources'/p.name)
 for n in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/n,S/n)
 shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv');shutil.copytree(R/'fonts',C/'baseline-fonts');(C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf');shutil.copy2(C.parents[1]/'assets/rubik.ttf',C/'assets/rubik.ttf');b['scratch']=str(S);(C/'baseline.json').write_text(json.dumps(b,indent=2)+'\n')
S=Path(b['scratch']);changes=[];dependencies={}
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{x.get('base') for x in r.findall('outline/component')} for n,r in rr.items()};arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 green={}
 for n,r in rr.items():
  lib=r.find('lib/dict')
  if lib is None:continue
  g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>');rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
 cons={'fi','fl'}
 while True:
  new=cons|{n for n,ds in deps.items() if ds&cons}
  if new==cons:break
  cons=new
 assert not cons & (set(green)|arab)
 dependencies[m]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green_hashes':green,'reverse_consumers':sorted(cons)}
 for n in ['fi','fl']:
  p=d/idx[n];rel=str(p.relative_to(R));old=p.read_text();assert 'caret_' not in old
  x=(344 if n=='fi' else 360) if m=='Bold' else 288
  new=old.replace('\t<lib>',f'\t<anchor name="caret_1" x="{x}" y="0"/>\n\t<lib>')
  for folder,data in [('before-sources',old),('candidate-sources',new)]:
   q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(data)
  (S/rel).write_text(new);changes.append({'path':rel,'before':sha(p),'after':sha(S/rel),'caret':x})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
