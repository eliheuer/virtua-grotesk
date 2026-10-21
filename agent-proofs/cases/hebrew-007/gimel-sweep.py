"""Left-sweeping Gimel foot trial; only the two Gimel outlines change."""
from pathlib import Path
import re,json,hashlib,argparse
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
records=[];changes=[]
for master in ['Regular','Bold']:
 p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/gimel-hb.glif';old=p.read_text()
 saved=C/f'working-v2-sources/sources/VirtuaGrotesk-{master}.ufo/glyphs/gimel-hb.glif'
 if old!=saved.read_text():raise RuntimeError(f'{master} changed since v2; preserve manual edits')
 points=re.findall(r'\t\t\t<point[^\n]+\n',old)
 bold=master=='Bold'
 tail=[(152,216,None),(96,208,None),(32,192,'curve'),(16,176,'line'),(16,16,'line'),(32,0,'line'),(128,0,None),(208,56,None),(256,144,'curve'),(288,16,'line'),(304,0,'line')] if bold else [(176,192,None),(112,128,None),(32,96,'curve'),(16,80,'line'),(16,16,'line'),(32,0,'line'),(128,0,None),(192,64,None),(240,128,'curve'),(272,16,'line'),(288,0,'line')]
 lines=points[:15]+['\t\t\t<point x="%d" y="%d"%s/>\n'%(x,y,' type="'+t+'"' if t else '') for x,y,t in tail]
 new=re.sub(r'\t\t<contour>.*?</contour>',lambda _: '\t\t<contour>\n'+''.join(lines)+'\t\t</contour>',old,flags=re.S)
 records.append({'path':str(p.relative_to(R)),'before':hashlib.sha256(old.encode()).hexdigest(),'after':hashlib.sha256(new.encode()).hexdigest()})
 changes.append((p,old,new))
if args.write:
 for p,old,new in changes:
  if p.read_text()!=old:raise RuntimeError('Concurrent source edit')
 for p,old,new in changes:
  p.write_text(new);snap=C/'working-v3-sources'/p.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_text(new)
 (C/'application-v3.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
