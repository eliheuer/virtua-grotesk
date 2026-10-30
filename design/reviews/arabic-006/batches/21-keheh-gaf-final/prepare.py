"""Bounded Keheh/Gaf final repair; retain bowls/joins, correct upper construction."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'applied.json').exists()
roots={};contents={};reserved={};names={'keheh-ar.fina','gaf-ar.fina'}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 dep={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in dep for co in E.parse(rr/cc[n]).findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
 assert not [(n,co.attrib) for n,f in cc.items() for co in E.parse(rr/f).findall('.//component') if co.get('base') in names]
# Explicit endpoints and handles; no borrowed reference outlines.
regular=[(960,0,'line'),(960,104,'line'),(864,104,''),(800,128,''),(768,160,'curve'),(512,416,'line'),(512,432,'line'),(880,648,'line'),(896,664,'line'),(896,752,'line'),(880,768,'line'),(368,456,'line'),(368,424,'line'),(616,176,'line'),(656,136,'line'),(656,112,'line'),(648,104,'line'),(224,104,'line'),(160,104,''),(128,136,''),(128,200,'curve'),(128,304,'line'),(112,320,'line'),(48,320,'line'),(32,304,'line'),(32,200,'line'),(32,80,''),(88,0,''),(224,0,'curve')]
bold=[(960,0,'line'),(960,176,'line'),(888,176,''),(848,192,''),(816,224,'curve'),(608,432,'line'),(608,448,'line'),(880,608,'line'),(896,624,'line'),(896,752,'line'),(880,768,'line'),(352,464,'line'),(352,432,'line'),(576,208,'line'),(592,192,'line'),(592,184,'line'),(584,176,'line'),(224,176,'line'),(184,176,''),(160,200,''),(160,240,'curve'),(160,336,'line'),(144,352,'line'),(16,352,'line'),(0,336,'line'),(0,240,'line'),(0,96,''),(80,0,''),(224,0,'curve')]
# Parallel secondary Gaf bar is part of the letter, not a reused hamza-like donor.
bars={'Regular':[(464,592),(880,832),(896,848),(896,864),(880,880),(464,640),(448,624),(448,608)],'Bold':[(464,592),(880,832),(896,848),(896,896),(880,912),(464,672),(448,656),(448,608)]}
def contour(points):
 lines=['\t\t<contour>']
 for i,(x,y,t) in enumerate(points):
  attrs=f' type="{t}"' if t else ''
  if len(points)==29 and i in [4,17,20,25,28]:attrs+=' smooth="yes"'
  lines.append(f'\t\t\t<point x="{x}" y="{y}"{attrs}/>')
 return '\n'.join(lines+['\t\t</contour>'])
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':[],'placements':{}}
for master in roots:
 for n in sorted(names):
  p=roots[master]/contents[master][n];rel=str(p.relative_to(R));old=p.read_text();assert rel not in reserved
  grade='orange' if master=='Regular' else 'red';color='1,0.5,0,1' if master=='Regular' else '1,0,0,1';assert f'<string>{grade}</string>' in old
  co=[contour(regular if master=='Regular' else bold)]
  if n=='gaf-ar.fina':co.append(contour([(x,y,'line') for x,y in bars[master]]))
  new=re.sub(r'\t<outline>.*?\t</outline>','\t<outline>\n'+'\n'.join(co)+'\n\t</outline>',old,flags=re.S)
  new=re.sub(r'<advance width="[^"]+"/>','<advance width="960"/>',new)
  new=new.replace(f'<string>{grade}</string>','<string>purple</string>').replace(f'<string>{color}</string>','<string>0.54,0.44,0.88,1</string>')
  for folder,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  m['glyphs'].append(dict(name=n,path=rel,master=master,drawing=True,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
for n in names:
 a=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Regular.ufo/glyphs/{contents["Regular"][n]}');b=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{contents["Bold"][n]}');assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared four files; 18 Beh sources reserved; no descendants.')
