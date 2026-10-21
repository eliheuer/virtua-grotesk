"""Prepare and install only Bold Alef's two approved-scope forms, hash guarded."""
from pathlib import Path
import hashlib,json,re,shutil,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'applied.json').exists(),'Preserve existing correction evidence'
(C/'before-fonts').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'before-fonts/VirtuaGrotesk.ttf')
shapes={'alef-ar':[(64,16),(80,0),(216,0),(232,16),(232,752),(216,768),(80,768),(64,752)],'alef-ar.fina':[(336,0),(336,176),(272,176),(240,208),(240,272),(240,752),(224,768),(88,768),(72,752),(72,264),(72,88),(160,0)]}
m={'baseline_commit':'4318e7a1','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
for name,points in shapes.items():
 rel=f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{name}.glif';p=R/rel;old=p.read_text();assert '<string>red</string>' in old
 it=iter(points)
 def pt(match):
  x,y=next(it);return f'<point x="{x}" y="{y}"'+match[1]
 new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',pt,old)
 if name.endswith('.fina'):new=new.replace('<advance width="292"/>','<advance width="336"/>')
 # Recenter only top attachments; final bottom attachments remain unchanged.
 for anchor in (['top','topDots','bottom','bottomDots'] if name=='alef-ar' else ['top','topDots']):
  x=152 if name=='alef-ar' else 160
  new=re.sub(r'(<anchor name="'+anchor+r'" x=")[^"]+',lambda m:m[1]+str(x),new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 regular=E.parse(R/rel.replace('-Bold','-Regular'));draft=E.fromstring(new)
 assert [[x.get('type') for x in c] for c in regular.findall('outline/contour')]==[[x.get('type') for x in c] for c in draft.findall('outline/contour')]
 m['glyphs'].append(dict(name=name,path=rel,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
for row in m['glyphs']:assert sha(R/row['path'])==row['before_sha256']
for row in m['glyphs']:(R/row['path']).write_bytes((C/'candidate-sources'/row['path']).read_bytes())
assert {p for p,h in m['source_hashes'].items() if sha(R/p)!=h}=={r['path'] for r in m['glyphs']}
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Installed two Bold Alef forms; all other source bytes preserved.')
