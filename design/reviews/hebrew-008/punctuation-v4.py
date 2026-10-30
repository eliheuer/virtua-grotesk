"""Retain Hebrew punctuation structures; bring weight and terminal construction in line."""
import hashlib,json,re
from pathlib import Path
from draw import P,contour
C=Path(__file__).resolve().parent;R=C.parents[2];changes=[];receipt=[]
for master in ['Regular','Bold']:
 b=master=='Bold'
 for name in ['yodyod-hb','geresh-hb','gershayim-hb']:
  p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif';old=p.read_bytes();s=old.decode()
  if name=='yodyod-hb':
   dx=288 if b else 192;w=624 if b else 432
   outline=f'\t<outline>\n\t\t<component base="yod-hb"/>\n\t\t<component base="yod-hb" xOffset="{dx}"/>\n\t</outline>'
  else:
   dx=48 if b else 0;w=176+dx
   pts=[P(32,432),P(96+dx,432),P(112+dx,448),P(160+dx,592),P(144+dx,608),P(80,608),P(64,592),P(16,448)]
   outline='\t<outline>\n'+contour(pts)
   if name=='gershayim-hb':
    offset=w+16;outline+=contour([(x+offset,y,t,sm) for x,y,t,sm in pts]);w=2*w+16
   outline+='\t</outline>'
  s=re.sub(r'\t<outline>.*?</outline>',lambda _:outline,s,flags=re.S)
  s=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{w}"/>',s)
  if name=='yodyod-hb':
   def anchor(m):
    n=m[1];x=72 if n=='hbCantAboveLeft' else w-72 if n=='hbCantAboveRight' else w//2
    return f'<anchor name="{n}" x="{x}" y="{m[3]}"/>'
   s=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,s)
  new=s.encode();h=lambda v:hashlib.sha256(v).hexdigest();changes.append((p,old,new));receipt.append(dict(path=str(p.relative_to(R)),before=h(old),after=h(new)))
if (C/'application-v4-punctuation.json').exists():raise RuntimeError('Already installed')
for p,old,new in changes:
 if p.read_bytes()!=old:raise RuntimeError('Concurrent edit')
for p,old,new in changes:
 for folder,blob in [('before-sources',old),('working-v4-sources',new)]:
  snap=C/folder/p.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True)
  if snap.exists():raise RuntimeError('Snapshot already exists')
  snap.write_bytes(blob)
 p.write_bytes(new)
(C/'application-v4-punctuation.json').write_text(json.dumps(receipt,indent=2)+'\n')
