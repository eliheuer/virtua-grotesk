import draw,hashlib,json,re
from pathlib import Path
C=Path(__file__).resolve().parent;R=C.parents[2];old=json.loads((C/'application-v1.json').read_text());receipt=[]
for rec in old:
 p=R/rec['path'];data=p.read_bytes()
 if hashlib.sha256(data).hexdigest()!=rec['after']:raise RuntimeError(f'Concurrent edit: {p}')
changes=[]
for rec in old:
 p=R/rec['path'];data=p.read_bytes();s=data.decode();b='Bold' in str(p)
 if p.stem in ['tet-hb','tsadi-hb']:
  pts,w=getattr(draw,p.stem.split('-')[0])(b)
  s=re.sub(r'\t<outline>.*?</outline>',lambda _:'\t<outline>\n'+draw.contour(pts)+'\t</outline>',s,flags=re.S)
  if p.stem=='tsadi-hb' and b:
   w=672
   s=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{w}"/>',s)
   s=re.sub(r'(<anchor name="hbCantAboveRight" x=")\d+',r'\g<1>640',s)
   s=re.sub(r'(<anchor name="(?:hbBottom|hbMeteg|hbCantAbove|hbCantBelow|hbCantBelowRight|hbRafe|hbCenter)" x=")\d+',r'\g<1>336',s)
 # New upright Shin now ends at 576; top mark anchors follow the new stem centres.
 if p.stem=='shin-hb':
  s=s.replace('y="584"','y="576"').replace('y="680"','y="672"')
  s=re.sub(r'(<anchor name="hbShin" x=")\d+',r'\g<1>'+str(720 if b else 592),s)
  s=re.sub(r'(<anchor name="hbSin" x=")\d+',r'\g<1>'+str(128 if b else 80),s)
 new=s.encode();changes.append((p,data,new));receipt.append(dict(path=str(p.relative_to(R)),before=rec['after'],after=hashlib.sha256(new).hexdigest()))
for p,data,new in changes:
 if p.read_bytes()!=data:raise RuntimeError('Concurrent edit')
for p,data,new in changes:
 p.write_bytes(new);snap=C/'working-v2-sources'/p.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes(new)
(C/'application-v2.json').write_text(json.dumps(receipt,indent=2)+'\n')
