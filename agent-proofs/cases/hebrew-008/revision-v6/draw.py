"""Rubik-structure trial for Shin and Final Tsadi. Scratch first; exact four-file promotion."""
from pathlib import Path
import sys, hashlib, json, re, shutil
import xml.etree.ElementTree as ET
C=Path(__file__).resolve().parent; ROOT=C.parents[3]
sys.path.insert(0,str(C.parent));from draw import P,O,S,contour
TARGETS=['shin-hb','finaltsadi-hb']
def shin(b):
 r=816 if b else 640; i=r-(192 if b else 96); l=224 if b else 128; center=(r+32)//2
 mid=528 if b else 400;mi=mid-(192 if b else 96);bar=152 if b else 80
 join=240;upper=408 if b else 336
 return [S(center,-16),O(r-112,-16),O(r,64),S(r,256),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,256,'line'),O(i,bar+48),O(center+128,bar),S(center,bar),O(l+64,bar),O(l,bar+32),P(l,join,'curve'),O(mid-96,join),O(mid,288 if not b else 320),S(mid,416 if not b else 456),P(mid,560),P(mid-16,576),P(mi+16,576),P(mi,560),S(mi,416 if not b else 472,'line'),O(mi,upper+16),O(l+64,upper),P(l,upper,'curve'),P(l,560),P(l-16,576),P(48,576),P(32,560),S(32,256,'line'),O(32,64),O(144,-16)],r+32

def finaltsadi(b):
 r=672 if b else 528;i=r-(192 if b else 96);dx=104 if b else 0
 # Long edges share a 1:2 diagonal. The arm joins that edge; no vertical tail.
 return [P(416,-192),P(496+dx,-192),P(512+dx,-176),P(456 if b else 304,144 if b else 240),O(r-64,160 if b else 256),O(r,288 if b else 320),S(r,448),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,448,'line'),O(i,384),O(432 if b else 352,336),P(360 if b else 256,336,'curve'),P(144+dx,560),P(128+dx,576),P(48,576),P(32,560),P(400,-176)],r+32

def run():
 scratch=ROOT/'out/qa/hebrew-008-v6/sources'; changes=[]
 if (C/'source-before.json').exists():raise RuntimeError('Frozen revision already exists; do not regenerate over edits.')
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'sources').rglob('*') if p.is_file()}
 (C/'source-before.json').write_text(json.dumps(hashes,indent=2)+'\n')
 for master in ['Regular','Bold']:
  src=ROOT/f'sources/VirtuaGrotesk-{master}.ufo';dst=scratch/src.name
  shutil.copytree(src,dst)
  for name,fn in [('shin-hb',shin),('finaltsadi-hb',finaltsadi)]:
   p=src/'glyphs'/f'{name}.glif';data=p.read_bytes();s=data.decode();pts,w=fn(master=='Bold')
   s=re.sub(r'\t<outline>.*?</outline>',lambda _:'\t<outline>\n'+contour(pts)+'\t</outline>',s,flags=re.S)
   s=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{w}"/>',s)
   b=master=='Bold'
   for m in re.finditer(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',s):
    n,x,y=m[1],int(m[2]),int(m[3])
    if n in ['hbBottom','hbMeteg','hbCantBelow','hbCantBelowRight']:
     x=(424 if b else 336) if name=='shin-hb' else (512 if b else 456)
     y=-32 if name=='shin-hb' else -192
    if n in ['hbCantAbove','hbRafe']:x=w//16*8
    if n=='hbCantAboveRight':x=w-32
    if n=='hbCenter':x,y=((568 if b else 464),352 if b else 240) if name=='shin-hb' else (248 if b else 208,0)
    s=s.replace(m[0],f'<anchor name="{n}" x="{x}" y="{y}"/>')
   out=dst/'glyphs'/p.name;out.write_text(s)
   snap=C/'before-sources'/p.relative_to(ROOT);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes(data)
   changes.append({'path':str(p.relative_to(ROOT)),'before':hashlib.sha256(data).hexdigest(),'after':hashlib.sha256(s.encode()).hexdigest(),'points':len(pts),'width':w})
 for name in TARGETS:
  roots=[ET.parse(scratch/f'VirtuaGrotesk-{m}.ufo/glyphs/{name}.glif').getroot() for m in ['Regular','Bold']]
  assert [[p.get('type') for p in r.findall('.//point')] for r in roots][0]==[[p.get('type') for p in r.findall('.//point')] for r in roots][1]
 (C/'planned-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 print(scratch)
if __name__=='__main__':run()
