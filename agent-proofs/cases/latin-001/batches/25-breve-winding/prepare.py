from pathlib import Path
import json,hashlib,shutil,tempfile,subprocess,plistlib,xml.etree.ElementTree as E,re
from fontTools.pens.pointPen import ReverseContourPointPen
from fontTools.pens.recordingPen import RecordingPointPen
R=Path.cwd();C=R/'agent-proofs/cases/latin-001/batches/25-breve-winding';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'baseline.json').exists()
S=Path(tempfile.mkdtemp(prefix='virtua-breve-winding-'));(S/'sources').mkdir()
for p in (R/'sources').iterdir():
 if p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']:shutil.copytree(p,S/'sources'/p.name)
 elif p.is_file():shutil.copy2(p,S/'sources'/p.name)
for n in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/n,S/n)
shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv')
sources={str(p.relative_to(R)):sha(p) for p in (S/'sources').rglob('*') if p.is_file() for p in [R/p.relative_to(S)]}
b={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'scratch':str(S),'sources':sources};(C/'baseline.json').write_text(json.dumps(b,indent=2)+'\n')
shutil.copytree(R/'fonts',C/'baseline-fonts');(C/'assets').mkdir();shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf');shutil.copy2(C.parents[1]/'assets/rubik.ttf',C/'assets/rubik.ttf')
changes=[];dependencies={}
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
 cons={'breve'}
 while True:
  new=cons|{n for n,ds in deps.items() if ds&cons}
  if new==cons:break
  cons=new
 assert not cons&(arab|set(green)),cons&(arab|set(green))
 dependencies[m]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green_hashes':green,'reverse_consumers':sorted(cons)}
 p=d/idx['breve'];rel=str(p.relative_to(R));old=p.read_text();cont=rr['breve'].find('outline/contour');rec=RecordingPointPen();rev=ReverseContourPointPen(rec);rev.beginPath()
 for pt in cont:rev.addPoint((int(pt.get('x')),int(pt.get('y'))),segmentType=pt.get('type'),smooth=pt.get('smooth')=='yes')
 rev.endPath();lines=[]
 for method,args,kw in rec.value:
  if method!='addPoint':continue
  (x,y),typ,smooth,name=args;line=f'\t\t\t<point x="{x}" y="{y}"'
  if typ:line+=f' type="{typ}"'
  if smooth:line+=' smooth="yes"'
  lines.append(line+'/>')
 new=re.sub(r'(?<=<contour>)\n.*?\n\t\t(?=</contour>)','\n'+'\n'.join(lines)+'\n\t\t',old,flags=re.S)
 for folder,data in [('before-sources',old),('candidate-sources',new)]:
  q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(data)
 (S/rel).write_text(new);changes.append({'path':rel,'before':sha(p),'after':sha(S/rel)})
 print(m,len(cons),'consumers',len(arab),'reserved',len(green),'green')
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
