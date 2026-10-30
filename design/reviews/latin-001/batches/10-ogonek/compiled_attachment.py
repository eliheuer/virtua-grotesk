"""Independent FreeType/RAQM whole-text check for deep below marks."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
C=Path(__file__).resolve().parent
texts=['Ą ą Ę ę Į į Ų ų','Ą ą Ę ę Į į Ų ų']
for w in [400,550,700]:
 im=Image.new('RGB',(1600,1440),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222)
 ui=ImageFont.truetype(str(C/'assets/before.ttf'),30);ui.set_variation_by_axes([400])
 d.text((64,30),f'Compiled ogonek canonical forms · {w} · FreeType/RAQM',font=ui,fill=ink)
 for i,name in enumerate(['before','after','rubik']):
  y=120+i*420;d.line((64,y,1536,y),fill=ink,width=2);d.text((64,y+12),name.title(),font=ui,fill=ink)
  f=ImageFont.truetype(str(C/'assets'/f'{name}.ttf'),92);f.set_variation_by_axes([w])
  for j,t in enumerate(texts):d.text((88,y+175+j*140),t,font=f,fill=ink,anchor='ls',direction='ltr')
 p=C/f'compiled-attachment-{w}.png';im.save(p)
(C/'compiled-attachment.json').write_text(json.dumps({'renderer':'Pillow FreeType/RAQM','weights':[400,550,700],'text':texts,'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['before','after','rubik']}},ensure_ascii=False,indent=2)+'\n')
