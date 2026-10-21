"""Keheh/Gaf joining forms; account for the full shared-bar donor closure."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,subprocess
import ufoLib2
from ufo2ft.filters.propagateAnchors import PropagateAnchorsFilter
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'applied.json').exists()
names={n+s for n in ['keheh-ar','gaf-ar','kehehThreedotsabove-ar'] for s in ['.init','.medi']}|{'gafsarkashabove-ar'}
roots={};contents={};reserved={};closures={};oldanchors={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc;trees={n:E.parse(rr/f) for n,f in cc.items()}
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
 assert closure==names,closure;assert not closure&dep
 for n in closure:assert '<string>green</string>' not in (rr/cc[n]).read_text()
 closures[master]=sorted(closure)
 f=ufoLib2.Font.open(rr.parent);PropagateAnchorsFilter()(f)
 oldanchors[master]={n:[(a.name,int(a.x),int(a.y)) for a in f[n].anchors] for n in ['gaf-ar.init','gaf-ar.medi']}
def points(c):return [(int(p.get('x')),int(p.get('y')),p.get('type',''),p.get('smooth')) for p in c]
def contour(pp):
 lines=['\t\t<contour>']
 for x,y,t,s in pp:
  attrs=(f' type="{t}"' if t else '')+(' smooth="yes"' if s else '')
  lines.append(f'\t\t\t<point x="{x}" y="{y}"{attrs}/>')
 return '\n'.join(lines+['\t\t</contour>'])
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(names),'placements':{},'closure':closures,'gaf_preserved_propagated_anchors':oldanchors}
for master in roots:
 rr=roots[master];cc=contents[master];join=104 if master=='Regular' else 176
 iso=points(E.parse(rr/cc['keheh-ar']).find('outline/contour'));final=points(E.parse(rr/cc['keheh-ar.fina']).find('outline/contour'))
 forms={'.init':[(x-256,y,t,s) for x,y,t,s in iso[:19]],'.medi':[(x-128,y,t,s) for x,y,t,s in final[:17]]}
 for ss in forms:forms[ss]+=[(0,join,'line',None),(-16,join-16,'line',None),(-16,16,'line',None),(0,0,'line',None)]
 bar=points(E.parse(rr/cc['gaf-ar.fina']).findall('outline/contour')[1]);bar=[(x-448,y,t,s) for x,y,t,s in bar]
 for n in sorted(names):
  p=rr/cc[n];rel=str(p.relative_to(R));old=p.read_text();grade='orange' if master=='Regular' else 'red';assert f'<string>{grade}</string>' in old
  ss='.init' if n.endswith('.init') else '.medi';width=448 if n=='gafsarkashabove-ar' else 704 if ss=='.init' else 832
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',old)
  metrics=n.startswith('kehehThreedots');drawing=n.startswith('keheh-ar') or n=='gafsarkashabove-ar'
  if drawing:
   co=bar if n=='gafsarkashabove-ar' else forms[ss]
   new=re.sub(r'\t<outline>.*?\t</outline>','\t<outline>\n'+contour(co)+'\n\t</outline>',new,flags=re.S)
  elif n.startswith('gaf-ar'):
   dx=192 if ss=='.init' else 320
   new=re.sub(r'<component base="gafsarkashabove-ar"[^>]*/>',f'<component base="gafsarkashabove-ar" xOffset="{dx}" yOffset="0"/>',new)
   anchorxml=''.join(f'\t<anchor name="{name}" x="{x}" y="{y}"/>\n' for name,x,y in oldanchors[master][n]);new=new.replace('\t<lib>',anchorxml+'\t<lib>')
  if not metrics:
   color='1,0.5,0,1' if master=='Regular' else '1,0,0,1';new=new.replace(f'<string>{grade}</string>','<string>purple</string>').replace(f'<string>{color}</string>','<string>0.54,0.44,0.88,1</string>')
  for folder,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/folder/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  m['glyphs'].append(dict(name=n,path=rel,master=master,drawing=drawing,metrics_only=metrics,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
for n in names:
 a=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Regular.ufo/glyphs/{contents["Regular"][n]}');b=E.parse(C/'candidate-sources'/f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{contents["Bold"][n]}');assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared14 sources; full donor closure checked; Beh18 reserved.')
