"""HEB-008: preserve six existing skeletons, develop compatible master weights.
Dry-run by default; first installation freezes every input and checks for races.
"""
import argparse, hashlib, json, re
from pathlib import Path
R=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent
names=['tet-hb','ayin-hb','alef-hb','tsadi-hb','finaltsadi-hb','shin-hb']
def P(x,y,t='line',s=False):return (x,y,t,s)
def O(x,y):return P(x,y,'')
def S(x,y,t='curve'):return P(x,y,t,True)
def contour(ps):
 return '\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"' if t else '')+(' smooth="yes"' if s else '')+'/>\n' for x,y,t,s in ps)+'\t\t</contour>\n'
def tet(b):
 r=688 if b else 560; i=r-(192 if b else 96); c=368 if b else 304; l=240 if b else 144; bar=152 if b else 80
 top=504 if b else 400; cap=448 if b else 376; end=352 if b else 280; inner=424 if b else 496
 return [S(c,-16),O(r-96,-16),O(r,80),S(r,256),S(r,352,'line'),O(r,512),O(r-32,592),S(top,592),O(top-48,592),O(end+32,584),P(end,560,'curve'),P(end,inner-16),P(end+16,inner-32),O(end+32,inner-8),O(cap-48,inner),S(cap-32,inner),S(cap,inner,'line'),O(cap+48,inner),O(i,inner-32),S(i,352),S(i,256,'line'),O(i,bar+56),O(c+104,bar),S(c,bar),O(l+56,bar),O(l,bar+32),S(l,208),P(l,560),P(l-16,576),P(64,576),P(48,560),S(48,208,'line'),O(48,64),O(c-176,-16)],r+32

def ayin(b):
 r=640 if b else 512;i=r-(192 if b else 96)
 return [P(32,-16),S(64,-16,'line'),O(352 if b else 288,-16),O(r,64),S(r,320),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,320,'line'),O(i,264 if b else 224),O(432 if b else 368,232 if b else 160),P(408 if b else 304,208 if b else 128,'curve'),P(240 if b else 144,560),P(224 if b else 128,576),P(64,576),P(48,560),P(240 if b else 216,176 if b else 104),O(176 if b else 160,168 if b else 88),O(112 if b else 104,152 if b else 80),S(64,152 if b else 80),P(32,152 if b else 80),P(16,136 if b else 64),P(16,0)],r+32

def alef(b):
 r=672 if b else 544;i=r-(192 if b else 96)
 return [P(672 if b else 576,0),P(688 if b else 592,16),P(528 if b else 432,224),O(r-64,272),O(r,352),S(r,448),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,448,'line'),O(i,400 if b else 384),O(464 if b else 416,360 if b else 336),P(448 if b else 384,328 if b else 288,'curve'),P(272 if b else 176,560),P(256 if b else 160,576),P(64,576),P(48,560),P(184,384),O(128,368),O(96,320),S(80,256),P(24,32),P(24,16),P(40,0),P(200 if b else 104,0),P(216 if b else 120,16),S(256 if b else 176,176 if b else 240,'line'),O(264 if b else 184,208 if b else 272),O(280 if b else 200,216 if b else 304),P(304 if b else 232,224 if b else 320,'curve'),P(464,16),P(480,0)],720 if b else 624

def tsadi(b):
 r=640 if b else 480;i=r-(192 if b else 96);foot=592 if b else 496;bar=168 if b else 96
 return [P(foot-16,0),P(foot,16),P(foot,80),P(440 if b else 344,288),O(r-56,320),O(r,368),S(r,448),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,448,'line'),O(i,400),O(424 if b else 352,368),P(392 if b else 296,352,'curve'),P(240 if b else 144,560),P(224 if b else 128,576),P(32,576),P(16,560),P(320 if b else 368,bar),P(64,bar),P(48,bar-16),P(48,16),P(64,0)],foot+32

def finaltsadi(b):
 r=592 if b else 464;i=r-(192 if b else 96);stem=352 if b else 256
 return [P(176,-192),P(stem-16,-192),P(stem,-176),P(stem,240 if b else 224),O(r-128,264 if b else 248),O(r,320 if b else 304),S(r,432 if b else 416),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,432 if b else 416,'line'),O(i,400 if b else 352),O(376 if b else 328,384 if b else 304),P(344 if b else 248,368 if b else 288,'curve'),O(336 if b else 248,432 if b else 400),O(288 if b else 200,496 if b else 464),P(240 if b else 144,560,'curve'),P(224 if b else 128,576),P(32,576),P(16,560),S(128,336,'line'),O(144,304),O(160,288),S(160,256),P(160,-176)],r+32

def shin(b):
 r=816 if b else 640;i=r-(192 if b else 96);mid=528 if b else 400;mi=mid-(192 if b else 96);base=416 if b else 352;bar=168 if b else 96
 return [P(144,0),S(base,0,'line'),O(r-96,0),O(r,64),S(r,256),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,256,'line'),O(i,bar+48),O(base+128,bar),S(base,bar),P(304 if b else 208,bar),P(288 if b else 184,256 if b else 224),O(432 if b else 304,272 if b else 240),O(mid,304 if b else 288),S(mid,400),P(mid,560),P(mid-16,576),P(mi+16,576),P(mi,560),S(mi,448 if b else 400,'line'),O(mi,400 if b else 344),O(304 if b else 264,384 if b else 320),P(256 if b else 168,384 if b else 312,'curve'),P(224 if b else 128,560),P(208 if b else 112,576),P(48,576),P(32,560),P(128,16)],r+32

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();changes=[];receipt=[]
 for master in ['Regular','Bold']:
  for name,fn in zip(names,[tet,ayin,alef,tsadi,finaltsadi,shin]):
   p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif';old=p.read_bytes();ps,w=fn(master=='Bold')
   text=re.sub(r'\t<outline>.*?</outline>',lambda _:'\t<outline>\n'+contour(ps)+'\t</outline>',old.decode(),flags=re.S)
   text=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{w}"/>',text)
   def anchor(m):
    n,x,y=m.group(1),int(m.group(2)),int(m.group(3));x=round(x/8)*8;y=round(y/8)*8
    if n in ['hbBottom','hbMeteg','hbCantAbove','hbCantBelow','hbCantBelowRight','hbRafe']:x=round(w/16)*8
    if n=='hbCantAboveRight':x=w-32
    if n=='hbCenter':x=round(w/16)*8
    return f'<anchor name="{n}" x="{x}" y="{y}"/>'
   text=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,text)
   new=text.encode();h=lambda b:hashlib.sha256(b).hexdigest()
   changes.append((p,old,new));receipt.append(dict(path=str(p.relative_to(R)),before=h(old),after=h(new),points=len(ps),width=w))
 if args.write:
  if (C/'application-v1.json').exists():raise RuntimeError('Already installed. Do not overwrite later human edits.')
  for p,old,new in changes:
   if p.read_bytes()!=old:raise RuntimeError(f'Concurrent edit: {p}')
  for p,old,new in changes:
   for folder,blob in [('before-sources',old),('working-v1-sources',new)]:
    dest=C/folder/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob)
  for p,old,new in changes:
   if p.read_bytes()!=old:raise RuntimeError(f'Concurrent edit: {p}')
   p.write_bytes(new)
  (C/'application-v1.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
