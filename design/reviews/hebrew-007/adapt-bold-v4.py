"""Adapt Bold to Eli's saved Regular construction; preserve Regular bytes."""
import argparse,hashlib,json,re,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
reg=R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/gimel-hb.glif';bold=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs/gimel-hb.glif'
a=reg.read_bytes();b=bold.read_bytes();snap=C/'hand-edit-01-Regular-gimel.glif'
if snap.exists() and snap.read_bytes()!=a:raise RuntimeError('Regular differs from saved correction; stop')
if not snap.exists() and args.write:snap.write_bytes(a)
old=(C/'working-v3-sources/sources/VirtuaGrotesk-Bold.ufo/glyphs/gimel-hb.glif').read_bytes()
if b!=old:raise RuntimeError('Bold has changed since v3; preserve concurrent edits')
pts=E.fromstring(a).findall('outline/contour/point');assert len(pts)==30
xy=[(32,0),(64,0),(160,0),(224,56),(248,144),(256,144),(288,16),(304,0),(448,0),(464,16),(464,32),(352,464),(336,528),(304,576),(224,576),(48,576),(32,560),(32,424),(48,408),(96,408),(144,408),(160,376),(176,312),(184,280),(200,216),(152,168),(64,168),(32,168),(16,152),(16,16)]
lines=[]
for pt,(x,y) in zip(pts,xy):
 line=f'\t\t\t<point x="{x}" y="{y}"'
 for attr in ['type','smooth']:
  if attr in pt.attrib:line+=f' {attr}="{pt.get(attr)}"'
 lines.append(line+'/>\n')
new=re.sub(r'\t\t<contour>.*?</contour>',lambda _: '\t\t<contour>\n'+''.join(lines)+'\t\t</contour>',b.decode(),flags=re.S).encode()
h=lambda v:hashlib.sha256(v).hexdigest()
record={'regular_preserved':h(a),'bold_before':h(b),'bold_after':h(new),'point_count':30,'status':'Working transfer test; not human-approved'}
if args.write:
 if reg.read_bytes()!=a or bold.read_bytes()!=b:raise RuntimeError('Concurrent edit')
 bold.write_bytes(new)
 for master,blob in [('Regular',a),('Bold',new)]:
  dest=C/f'working-v4-sources/sources/VirtuaGrotesk-{master}.ufo/glyphs/gimel-hb.glif';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob)
 (C/'application-v4.json').write_text(json.dumps(record,indent=2)+'\n')
 assert reg.read_bytes()==a
print(json.dumps(record,indent=2))
