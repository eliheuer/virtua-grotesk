from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil
R=Path.cwd();C=R/'agent-proofs/cases/arabic-006/batches/06-medial-loop';C.mkdir(exist_ok=True)
assert not (C/'candidate.json').exists(), 'Do not overwrite a saved batch; create a new trial snapshot.'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
root=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes())
reserved={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());names={'beh-ar'+s for s in ['', '.init','.medi','.fina']}
 while True:
  added={co.get('base') for n in names for co in E.parse(rr/cc[n]).findall('outline/component')}-names
  if not added:break
  names|=added
 for n in names:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
name='fehDotless-ar.medi';deps={name}
while True:
 add={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
for n in deps:assert '<string>green</string>' not in (root/cs[n]).read_text(),n
pts=[(568,0),(568,176),(328,176),(328,184),(416,184),(504,224),(504,352),(504,480),(400,584),(272,584),(144,584),(40,480),(40,352),(40,224),(128,184),(216,184),(216,176),(0,176),(-16,160),(-16,16),(0,0), (272,176),(232,176),(200,312),(200,352),(200,392),(232,424),(272,424),(312,424),(344,392),(344,352),(344,312),(312,176)]
m={'baseline_commit':'239a8d1e','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'placements':{},'inherited_bold_glyphs':sorted(deps-{name})}
for n in sorted(deps):
 p=root/cs[n];rel=str(p.relative_to(R));old=p.read_text();new=old
 if n==name:
  it=iter(pts)
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:
  co=E.fromstring(old).findall('outline/component')
  if len(co)>1 and co[1].get('base') in ['dotabove-ar','twodotshorizontalabove-ar','threedotsupabove-ar']:
   attrs=dict(co[1].attrib);attrs['yOffset']=str(int(attrs.get('yOffset','0'))+88)
   new=re.sub('<component base="'+attrs['base']+'"[^>]*/>',lambda _: '<component '+' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>',new);m['placements'][n]=attrs
 if new==old:continue
 assert rel not in reserved,(n,'human reservation')
 for master in ['Regular','Bold']:
  src=R/rel.replace('-Bold','-'+master);dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,drawing=n==name,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'agent-proofs/cases/arabic-006/batches/05-feh-qaf-repair/assets/after.ttf',C/'assets/before.ttf')
for g in m['glyphs']: assert sha(R/g['path'])==g['before_sha256']
for p,h in reserved.items():assert sha(R/p)==h
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied',len(m['glyphs']),'files; affected',sorted(deps),'reserved',len(reserved),'Beh/component files.')
