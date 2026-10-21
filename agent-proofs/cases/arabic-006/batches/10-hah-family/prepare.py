"""Bounded Bold Hah family repair; preserve green Regular and Beh dependency closure."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent
assert not (C/'candidate.json').exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
roots={};contents={};reserved={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in names for co in E.parse(rr/cc[n]).findall('outline/component')}-names
  if not add:break
  names|=add
 for n in names:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
root=roots['Bold'];cs=contents['Bold']
# Shared wave head: 160-unit left terminal, 144-unit crown, 160-unit nose.
head=[(736,208),(752,224),(752,352),(736,368),(656,368),(456,368),(368,480),(240,480),(104,480),(32,408),(32,296),(32,280),(48,264),(176,264),(192,280),(192,312),(208,336),(240,336),(352,336),(448,288),(560,288),(560,280)]
iso=[(640,-352),(656,-336),(656,-192),(640,-176),(472,-176),(312,-176),(208,-144),(208,-48),(208,104),(448,208),(656,208)]+head+[(240,248),(48,112),(48,-64),(48,-256),(232,-352),(472,-352)]
init=[(136,0),(344,0),(488,208),(656,208)]+head+[(400,256),(304,176),(136,176),(0,176),(-16,160),(-16,16),(0,0)]
medi=[(136,0),(312,0),(392,136),(488,184),(496,176),(496,48),(640,0),(800,0),(832,0),(832,176),(800,176),(704,176),(648,176),(648,200),(656,208)]+head+[(400,256),(304,176),(136,176),(0,176),(-16,160),(-16,16),(0,0)]
fina=[(576,-352),(592,-336),(592,-192),(576,-176),(408,-176),(264,-176),(192,-152),(192,-72),(192,48),(328,152),(488,184),(496,176),(496,48),(640,0),(800,0),(832,0),(832,176),(800,176),(704,176),(648,176),(648,200),(656,208)]+head+[(240,248),(32,88),(32,-88),(32,-280),(200,-352),(408,-352)]
points={'hah-ar':iso,'hah-ar.init':init,'hah-ar.medi':medi,'hah-ar.fina':fina}
widths={'hah-ar':784,'hah-ar.init':784,'hah-ar.medi':832,'hah-ar.fina':832}
placements={}
for n in cs:
 if n.startswith('jeem-ar'):
  suffix=n[len('jeem-ar'):];x,y=({'':(360,200),'.fina':(312,200),'.init':(216,0),'.medi':(216,0)})[suffix]
  placements[n]=dict(base='dotbelow-ar',xOffset=str(x),yOffset=str(y))
 if n.startswith('khah-ar'):placements[n]=dict(base='dotabove-ar',xOffset='200',yOffset='-48')

deps=set(points)
while True:
 add={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
for n in deps:
 t=(root/cs[n]).read_text()
 assert '<string>green</string>' not in t and '<string>0.09,0.72,0.44,1</string>' not in t and '<string>0,1,0,1</string>' not in t,n
 assert str((root/cs[n]).relative_to(R)) not in reserved,n
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'placements':placements,'inherited_bold_glyphs':sorted(deps-set(points))}
for n in sorted(deps):
 p=root/cs[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 if n in points:
  it=iter(points[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[n]}"/>',new)
 if n not in points:
  base=E.fromstring(old).find('outline/component').get('base')
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[base]}"/>',new)
 if n in placements:
  co=E.fromstring(new).findall('outline/component')[1]
  new=re.sub(r'<component base="'+co.get('base')+r'"[^>]*/>', '<component '+' '.join(f'{k}="{v}"' for k,v in placements[n].items())+'/>',new)
 if new==old:continue
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 # Topology must match the protected master without altering it.
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n])
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')],n
 for master in ['Regular','Bold']:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,drawing=n in points,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'09-meem/assets/after.ttf',C/'assets/before.ttf')
for g in m['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied',len(m['glyphs']),'files; affected',sorted(deps),'reserved',len(reserved),'Beh/component files.')
