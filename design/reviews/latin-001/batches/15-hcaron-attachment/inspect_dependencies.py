from pathlib import Path
import json,plistlib,xml.etree.ElementTree as E
R=Path.cwd();C=R/'agent-proofs/cases/latin-001/batches/15-hcaron-attachment';C.mkdir(exist_ok=True)
out={}
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());roots={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{c.get('base') for c in r.findall('outline/component')} for n,r in roots.items()}
 arab={n for n,r in roots.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 cons={'hcaron'}
 while True:
  new=cons|{n for n in deps if deps[n]&cons}
  if new==cons:break
  cons=new
 grades={n:plistlib.loads(b'<?xml version="1.0"?><plist version="1.0">'+E.tostring(roots[n].find('lib/dict'))+b'</plist>') if roots[n].find('lib/dict') is not None else {} for n in cons}
 green=[n for n,g in grades.items() if g.get('com.runebender.markLabel')=='green' or g.get('public.markColor') in ['0,1,0,1','0.3,0.85,0.39,1','0.09,0.72,0.44,1']]
 # Include any remaining color that could represent green for manual review.
 suspicious=[(n,g) for n,g in grades.items() if g.get('public.markColor','') not in ['1,0,0,1','1,0.5,0,1','0.54,0.44,0.88,1','1,0.29,0.24,1','0,0.5,1,1','1,0.5,1,1','0,0,1,1','1,0,1,1']]
 out[m]={'consumers':sorted(cons),'green':green,'arabic_intersection':sorted(cons&arab),'arabic_reserved_count':len(arab),'grades':grades,'suspicious':suspicious};assert not green and not cons&arab
(C/'dependencies.json').write_text(json.dumps(out,indent=2)+'\n');print({m:{k:v for k,v in x.items() if k!='grades'} for m,x in out.items()})
