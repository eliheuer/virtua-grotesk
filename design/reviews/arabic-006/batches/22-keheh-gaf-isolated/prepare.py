"""Isolated Keheh/Gaf: local adaptation of batch21; preserve shared Gaf donor."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
import ufoLib2
from ufo2ft.filters.propagateAnchors import PropagateAnchorsFilter
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'applied.json').exists()
names={'keheh-ar','gaf-ar','kehehThreedotsabove-ar'}; roots={};contents={};reserved={};closures={};oldanchors={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 trees={n:E.parse(rr/f) for n,f in cc.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in dep for co in trees[n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
 closure=set(names)
 while True:
  add={n for n,t in trees.items() if any(co.get('base') in closure for co in t.findall('outline/component'))}-closure
  if not add:break
  closure|=add
 assert closure==names,closure
 assert not closure&dep
 for n in closure:
  assert '<string>green</string>' not in (rr/cc[n]).read_text()
 closures[master]=sorted(closure)
 f=ufoLib2.Font.open(rr.parent);PropagateAnchorsFilter()(f)
 oldanchors[master]=[(a.name,int(a.x),int(a.y)) for a in f['gaf-ar'].anchors]
# Bottom-right bowl returns directly into the descending diagonal. Both cubic
# joins are tangent; the right extremum is explicit. Head/inner cuts from batch21.
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(names),'placements':{},'closure':closures,'gaf_preserved_propagated_anchors':oldanchors}
for master in roots:
 final=E.parse(roots[master]/contents[master]['keheh-ar.fina']).find('outline/contour')
 pts=[(int(p.get('x')),int(p.get('y')),p.get('type',''),p.get('smooth')) for p in final]
 if master=='Regular':start=[(576,0,'line'),(704,0,''),(800,16,''),(800,96,'curve'),(800,128,''),(784,144,''),(768,160,'curve')]
 else:start=[(576,0,'line'),(720,0,''),(864,32,''),(864,128,'curve'),(864,168,''),(840,200,''),(816,224,'curve')]
 points=[(x,y,t,'yes' if i in [0,3,6] else None) for i,(x,y,t) in enumerate(start)]+pts[5:]
 def contour(points):
  lines=['\t\t<contour>']
  for x,y,t,s in points:
   attrs=(f' type="{t}"' if t else '')+(' smooth="yes"' if s else '')
   lines.append(f'\t\t\t<point x="{x}" y="{y}"{attrs}/>')
  return '\n'.join(lines+['\t\t</contour>'])
 base=contour(points)
 bar=E.parse(roots[master]/contents[master]['gaf-ar.fina']).findall('outline/contour')[1]
 bar=contour([(int(p.get('x')),int(p.get('y')),p.get('type',''),None) for p in bar])
 for n in sorted(names):
  p=roots[master]/contents[master][n];rel=str(p.relative_to(R));old=p.read_text();grade='orange' if master=='Regular' else 'red';assert f'<string>{grade}</string>' in old
  new=re.sub(r'<advance width="[^"]+"/>','<advance width="960"/>',old)
  drawing=n!='kehehThreedotsabove-ar'
  if drawing:
   out=base if n=='keheh-ar' else '\t\t<component base="keheh-ar"/>\n'+bar
   new=re.sub(r'\t<outline>.*?\t</outline>','\t<outline>\n'+out+'\n\t</outline>',new,flags=re.S)
   if n=='gaf-ar':
    anchorxml=''.join(f'\t<anchor name="{name}" x="{x}" y="{y}"/>\n' for name,x,y in oldanchors[master])
    new=new.replace('\t<lib>',anchorxml+'\t<lib>')
   color='1,0.5,0,1' if master=='Regular' else '1,0,0,1'
   new=new.replace(f'<string>{grade}</string>','<string>purple</string>').replace(f'<string>{color}</string>','<string>0.54,0.44,0.88,1</string>')
  for folder,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  m['glyphs'].append(dict(name=n,path=rel,master=master,drawing=drawing,metrics_only=not drawing,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
for n in names:
 a=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Regular.ufo/glyphs/{contents["Regular"][n]}');b=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{contents["Bold"][n]}');assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Prepared six sources; isolated closure only; Beh18 and shared donors reserved.')
