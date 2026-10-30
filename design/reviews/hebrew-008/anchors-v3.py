"""Move existing anchors to clear actual compiled ink; never edit mark outlines."""
import hashlib,json,re
from pathlib import Path
C=Path(__file__).resolve().parent;R=C.parents[2];changes=[];receipt=[]
for master in ['Regular','Bold']:
 b=master=='Bold'
 for name in ['tet','ayin','tsadi','finaltsadi','shin','samekh','qof','finalkaf']:
  p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}-hb.glif';old=p.read_bytes();s=old.decode()
  def update(m):
   n,x,y=m[1],int(m[2]),int(m[3]);bottom=n in ['hbBottom','hbMeteg','hbCantBelow','hbCantBelowRight']
   if bottom and name in ['tet','ayin','samekh']:y=-32
   if bottom and name=='finaltsadi':y=-192
   if bottom and name=='finalkaf':x=192
   if bottom and name=='qof':x=416 if b else 336;y=-32
   if n=='hbCenter':
    if name=='ayin':x,y=(384,464) if b else (320,400)
    if name=='tsadi':x,y=(176,280) if b else (176,224)
    if name=='finaltsadi':x,y=(432,160) if b else (336,128)
    if name=='shin':x,y=(568,352) if b else (464,240)
    if name=='qof':x,y=(304,352) if b else (280,352)
   if name=='ayin' and y==584:y=576
   return f'<anchor name="{n}" x="{x}" y="{y}"/>'
  new=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',update,s).encode();changes.append((p,old,new));h=lambda x:hashlib.sha256(x).hexdigest();receipt.append(dict(path=str(p.relative_to(R)),before=h(old),after=h(new),anchor_only=True))
if (C/'application-v3-anchors.json').exists():raise RuntimeError('Already installed; preserve later edits')
for p,old,new in changes:
 if p.read_bytes()!=old:raise RuntimeError('Concurrent edit')
for p,old,new in changes:
 before=C/'before-sources'/p.relative_to(R);before.parent.mkdir(parents=True,exist_ok=True)
 if not before.exists():before.write_bytes(old)
 p.write_bytes(new)
for master in ['Regular','Bold']:
 for name in ['tet','ayin','alef','tsadi','finaltsadi','shin','samekh','qof','finalkaf']:
  p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}-hb.glif';snap=C/'working-v3-sources'/p.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes(p.read_bytes())
(C/'application-v3-anchors.json').write_text(json.dumps(receipt,indent=2)+'\n')
