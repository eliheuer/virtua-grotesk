from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
C=Path(__file__).resolve().parent;receipt=[]
for w,size in [(400,48),(550,48),(700,48),(400,160),(700,160)]:
 large=size==160;rows=['Ą́ Ę́ Į́ Ų́','ą́ ę́ į́ ų́'] if large else ['Ą́ ą́ Ę́ ę́ Į́ į́ Ų́ ų́','Ą̂ ą̈ Ę̀ ę̄ Į̌ į̃ Ų̊ ų̆','aą́a eę́e iį́i uų́u','Ą̧́ ą̧́  į̇ į̈  Ų́́ ų́́']
 height=550 if large else 440;im=Image.new('RGB',(1600,120+4*height),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222);ui=ImageFont.truetype(str(C/'assets/after.ttf'),28);ui.set_variation_by_axes([400]);d.text((64,28),f'Ogonek subset normalization · {w} · {size}px · FreeType/RAQM',font=ui,fill=ink)
 for i,(n,label) in enumerate([('before-subset','Before: ogonek cmap absent'),('after-subset','Working: ogonek cmap absent'),('after','Working: full cmap'),('rubik','Rubik reference: full cmap')]):
  y=100+i*height;d.line((64,y,1536,y),fill=ink,width=2);d.text((64,y+8),label,font=ui,fill=ink);f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),size);f.set_variation_by_axes([w])
  for j,t in enumerate(rows):
   pos=(88,y+(235 if large else 115)+j*(235 if large else 90));bb=d.textbbox(pos,t,font=f,anchor='ls',direction='ltr');assert bb[2]<1536 and bb[3]<y+height,(n,w,bb);d.text(pos,t,font=f,fill=ink,anchor='ls',direction='ltr')
 fn=f'{"large" if large else "forms"}-{w}.png';im.save(C/fn);receipt.append({'file':fn,'weight':w,'px_per_em':size,'sha256':hashlib.sha256((C/fn).read_bytes()).hexdigest()})
(C/'proofs.json').write_text(json.dumps({'renderer':'FreeType/RAQM','images':receipt,'fonts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (C/'assets').glob('*.ttf')}},indent=2)+'\n')
