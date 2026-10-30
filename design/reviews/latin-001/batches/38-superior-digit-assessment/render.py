from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
import hashlib,json
C=Path(__file__).resolve().parent;records=[]
for w,size in [(400,48),(550,48),(700,48),(400,224),(700,224)]:
 im=Image.new('RGB',(1600,1800 if size==224 else 1200),(222,222,222));d=ImageDraw.Draw(im);ink=(68,68,68)
 ui=ImageFont.truetype(str(C/'assets/virtua.ttf'),26);ui.set_variation_by_axes([400])
 d.text((48,24),f'Superior digit assessment · {w} · {size}px · FreeType/RAQM',font=ui,fill=ink)
 for i,name in enumerate(['virtua','rubik']):
  f=ImageFont.truetype(str(C/'assets'/f'{name}.ttf'),size);f.set_variation_by_axes([w]);y=100+i*(850 if size==224 else 520)
  d.line((48,y,1552,y),fill=ink,width=1);d.text((48,y+12),name.title()+' · ordinary figures, encoded superiors, sups feature',font=ui,fill=ink)
  for j,(s,features) in enumerate([('123' if size==224 else '123 · 101 202 303 · H123H',[]),('¹²³' if size==224 else 'x¹ x² x³ · 10¹ 10² 10³',[]),('123',['sups'])]):
   pos=(64,y+250+j*235) if size==224 else (64,y+180+j*145)
   missing={ord(c) for c in s}-set(TTFont(C/'assets'/f'{name}.ttf').getBestCmap())
   if missing:
    d.text(pos,'Unavailable: U+00B9, U+00B2, U+00B3',font=ui,fill=ink,anchor='ls');continue
   box=d.textbbox(pos,s,font=f,features=features,anchor='ls');assert box[2]<1552 and box[3]<y+(850 if size==224 else 520),box
   d.text(pos,s,font=f,features=features,fill=ink,anchor='ls')
 out=C/f'{"detail" if size==224 else "forms"}-{w}.png';im.save(out);records.append({'path':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'weight':w,'size':size})
(C/'raster.json').write_text(json.dumps({'renderer':'Pillow FreeType/RAQM; absent cmap rows explicitly unavailable, no fallback','images':records},indent=2)+'\n')
