"""HEB-007 bounded, hash-guarded working drawings. Dry-run unless --write."""
import argparse,hashlib,json,re,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[3]; C=Path(__file__).resolve().parent
names=['gimel-hb','lamed-hb','qof-hb']
def P(x,y,t='line',s=False):return (x,y,t,s)
def O(x,y):return P(x,y,'')
def contour(points):
 return '\t\t<contour>\n'+''.join('\t\t\t<point x="%s" y="%s"%s%s/>\n'%(x,y,' type="'+t+'"' if t else '', ' smooth="yes"' if s else '') for x,y,t,s in points)+'\t\t</contour>\n'
def rect(l,b,r,t):
 return [P(l+16,b),P(r-16,b),P(r,b+16),P(r,t-16),P(r-16,t),P(l+16,t),P(l,t-16),P(l,b+16)]
def hook(bold,lamed):
 right=560 if bold else 464; bottom=408 if bold else 480
 # Shared compact upper shoulder; lower sweeping stroke retains existing structure.
 if lamed:
  pts=[P(96,0),P(112,-16),O(256,32),O(right,176),P(right,400,'curve',True)]
 else:pts=[P(176,16),P(192,0),O(320,48),O(right,176),P(right,400,'curve',True)]
 pts += [O(right,512),O(right-64,576),P(right-160,576,'curve',True)]
 if lamed:
  stem=224 if bold else 128
  pts += [P(stem,576),P(stem,752),P(stem-16,768),P(48,768),P(32,752),P(32,bottom+16),P(48,bottom)]
 else:pts += [P(32,576),P(16,560),P(16,bottom+16),P(32,bottom)]
 pts += [P(312 if bold else 288,bottom,'line',True),O(352 if bold else 344,bottom),O(368,392 if bold else 448),P(368,352 if bold else 384,'curve',True)]
 if lamed:
  pts += [O(368,288 if bold else 264),O(256 if bold else 248,232 if bold else 144),P(112,184 if bold else 96,'curve'),P(96,168 if bold else 80)]
 else:pts += [O(368,288 if bold else 264),O(280 if bold else 272,240 if bold else 152),P(192,200 if bold else 112,'curve'),P(176,184 if bold else 96)]
 result=[pts]
 if not lamed:result.append(rect(40,-192,232 if bold else 136,304 if bold else 384))
 return result,592 if bold else 496

def gimel(b):
 dx=96 if b else 0
 p=[P(352+dx,0),P(368+dx,16),P(256+dx,464,'line',True),O(240+dx,528),O(208+dx,576),P(128+dx,576,'curve',True),P(48,576),P(32,560),P(32,424 if b else 496),P(48,408 if b else 480),P(96,408 if b else 480,'line',True),O(144,408 if b else 480),O(160,376 if b else 448),P(176,312 if b else 384,'curve',True),P(208,184 if b else 256),P(160,168 if b else 240),O(80,144 if b else 216),O(48,208 if b else 176),P(32,128 if b else 96,'curve',True),P(16,48 if b else 16),P(32,0),P(176 if b else 96,0),P(192 if b else 112,16),P(208 if b else 128,96,'line',True),O(216 if b else 144,136 if b else 176),O(232 if b else 176,144 if b else 192),P(256 if b else 224,144 if b else 192,'curve'),P(288 if b else 272,16),P(304 if b else 288,0)]
 return [p],488 if b else 392

def refine(contours, name, bold):
 if not bold:return contours
 changes={'qof-hb':{(176,16):(272,16),(192,0):(288,0),(320,48):(416,48),(280,240):(344,240),(192,200):(288,200),(176,184):(272,184)},'gimel-hb':{(208,184):(184,280),(160,168):(144,264),(80,144):(80,240)}}.get(name,{})
 return [[(*changes.get((x,y),(x,y)),t,s) for x,y,t,s in points] for points in contours]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
 receipt=[]; changes=[]
 for master in ['Regular','Bold']:
  for name in names:
   path=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif';old=path.read_text();b=master=='Bold'
   contours,width=gimel(b) if name=='gimel-hb' else hook(b,name=='lamed-hb')
   contours=refine(contours,name,b)
   source='\t<outline>\n'+''.join(map(contour,contours))+'\t</outline>'
   new=re.sub(r'\t<outline>.*?</outline>',lambda _:source,old,flags=re.S)
   new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
   # Preserve all anchor names, migrate positions to the intended 8-unit geometry.
   def anchor(m):
    name,x,y=m.group(1),int(m.group(2)),int(m.group(3))
    x=round(x/8)*8;y=round(y/8)*8
    if 'Right' in name and 'Above' in name:x=width-24 if 'gimel' in path.name else width-32
    elif name in ['hbBottom','hbMeteg','hbCantAbove','hbCantBelow','hbCantBelowRight','hbRafe']:x=(width//16)*8
    if 'lamed' in path.name:
     if y==784:y=768
     if y==880:y=864
    return f'<anchor name="{name}" x="{x}" y="{y}"/>'
   new=re.sub(r'<anchor name="([^"]+)" x="(-?\d+)" y="(-?\d+)"/>',anchor,new)
   changes.append((path,old,new));receipt.append(dict(path=str(path.relative_to(R)),before=digest(path),after=hashlib.sha256(new.encode()).hexdigest()))
 if args.write:
  for path,old,new in changes:
   if path.read_text()!=old:raise RuntimeError(f'Concurrent change: {path}')
  for path,old,new in changes:
   before=C/'before-sources'/path.relative_to(R);before.parent.mkdir(parents=True,exist_ok=True)
   if before.exists():raise RuntimeError('Baseline already exists; do not replace it')
   before.write_text(old)
  for path,old,new in changes:
   path.write_text(new)
   snap=C/'working-v2-sources'/path.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_text(new)
  (C/'application-v2-regenerated.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
