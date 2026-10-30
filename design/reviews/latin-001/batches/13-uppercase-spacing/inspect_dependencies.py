from pathlib import Path
import json,plistlib,xml.etree.ElementTree as E,unicodedata as U,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];out={}
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{c.get('base') for c in r.findall('outline/component')} for n,r in rr.items()}
 def grow(seeds,reverse=False):
  s=set(seeds)
  while True:
   new=s|({n for n,v in deps.items() if v&s} if reverse else set().union(*(deps[n] for n in s)))
   if s==new:return s
   s=new
 def grade(r):return plistlib.loads(b'<plist>'+E.tostring(r.find('lib/dict'))+b'</plist>') if r.find('lib/dict') is not None else {}
 def green(r):
  g=grade(r);rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')];return g.get('com.runebender.markLabel')=='green' or (rgba[1]>rgba[0] and rgba[1]>rgba[2] and rgba[1]>.6)
 arab=grow({n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))})
 targets={};equal=[]
 for n,r in rr.items():
  cs=r.findall('outline/component');us=r.findall('unicode')
  if len(cs)!=2 or not us:continue
  char=chr(int(us[0].get('hex'),16));decomp=U.normalize('NFD',char);base=cs[0].get('base')
  if len(decomp)<2 or decomp[0] not in 'ADGLNORSTUWYZ' or base!=decomp[0]:continue
  w=float(r.find('advance').get('width'));bw=float(rr[base].find('advance').get('width'))
  if w==bw:equal.append(n);continue
  assert cs[1].get('base')!='caroncomb.alt',n
  assert not green(r) and n not in arab and cs[0].attrib=={'base':base},n
  assert bw%8==0
  targets[n]={'path':str((d/idx[n]).relative_to(R)),'char':char,'base':base,'before_width':w,'after_width':bw,'grade':grade(r)}
 cons=grow(targets,True);assert not any(green(rr[n]) for n in cons) and not cons&arab
 out[m]={'targets':targets,'consumers':sorted(cons),'already_equal':equal,'arabic_reserved':{n:hashlib.sha256((d/idx[n]).read_bytes()).hexdigest() for n in sorted(arab)},'green':[],'arabic_intersection':[]}
(C/'dependencies.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print({m:(len(v['targets']),len(v['consumers']),len(v['arabic_reserved'])) for m,v in out.items()})
