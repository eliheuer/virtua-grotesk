"""Keep double-Yod geometry exact, avoiding nested TT composites in FB1F."""
import json,re,hashlib,xml.etree.ElementTree as E
from pathlib import Path
from draw import contour
C=Path(__file__).resolve().parent;R=C.parents[2];records=[];changes=[]
expected={v['path']:v['after'] for v in json.loads((C/'application-v4-punctuation.json').read_text())}
for m in ['Regular','Bold']:
 p=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/yodyod-hb.glif';old=p.read_bytes();assert hashlib.sha256(old).hexdigest()==expected[str(p.relative_to(R))]
 donor=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/yod-hb.glif';tree=E.parse(donor).getroot();offset=288 if m=='Bold' else 192;cs=[]
 for dx in [0,offset]:
  for c in tree.findall('outline/contour'):
   cs.append(contour([(int(pt.get('x'))+dx,int(pt.get('y')),pt.get('type',''),pt.get('smooth')=='yes') for pt in c]))
 new=re.sub(r'\t<outline>.*?</outline>',lambda _:'\t<outline>\n'+''.join(cs)+'\t</outline>',old.decode(),flags=re.S).encode();changes.append((p,old,new));records.append(dict(path=str(p.relative_to(R)),before=hashlib.sha256(old).hexdigest(),after=hashlib.sha256(new).hexdigest(),donor=str(donor.relative_to(R)),donor_sha256=hashlib.sha256(donor.read_bytes()).hexdigest()))
for p,old,new in changes:
 assert p.read_bytes()==old;p.write_bytes(new);(C/'final-sources'/p.relative_to(R)).write_bytes(new)
(C/'application-v5-double-yod.json').write_text(json.dumps(records,indent=2)+'\n')
