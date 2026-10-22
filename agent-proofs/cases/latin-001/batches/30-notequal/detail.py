from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent
for w in [400,700]:
 im=Image.new('RGB',(1600,1140),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222);ui=ImageFont.truetype(str(C/'assets/before.ttf'),28)
 d.text((64,24),f'U+2260 not equal · {w} · 224px · FreeType/RAQM',font=ui,fill=ink)
 for i,n in enumerate(['after','rubik']):
  y=110+i*500;d.text((64,y),n.title(),font=ui,fill=ink);f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);f.set_variation_by_axes([w]);t='= ≠ ≠'
  d.text((64,y+330),t,font=f,fill=ink,anchor='ls');d.text((1080,y+330),'≠',font=f,fill=ink,anchor='ls')
 im.save(C/f'detail-{w}.png')
