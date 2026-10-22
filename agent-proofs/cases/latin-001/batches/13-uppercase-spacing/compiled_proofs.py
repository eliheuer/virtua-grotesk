from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
import hashlib,json
C=Path(__file__).resolve().parent
pages={'capitals1':['A Á Ă Â Ä À Ā Ą Å Ã A','D Ď D   G Ğ Ģ Ġ G','L Ĺ Ļ L   N Ń Ň Ņ Ñ N','O Ó Ô Ö Ò Ő Õ O','NANA NÁNA NONO NÓNO','LÁLA LALA   OOO ÓÓÓ'],
'capitals2':['R Ŕ Ř R   S Ś Š Ş Ș S','T Ţ Ț T   U Ú Û Ü Ù Ű Ū Ų Ů U','W Ẃ Ŵ Ẅ Ẁ W','Y Ý Ŷ Ÿ Ỳ Y   Z Ź Ž Ż Z','YAYA YÁYÁ  RARA ŔAŔA','UUU ÚÚÚ  SSS ŚŚŚ  WWW ŴŴŴ']}
receipt=[]
for kind,rows in pages.items():
 for w in [400,550,700]:
  im=Image.new('RGB',(1600,1840),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222)
  ui=ImageFont.truetype(str(C/'assets/before.ttf'),30);ui.set_variation_by_axes([400]);d.text((64,28),f'Uppercase spacing · {kind} · {w} · FreeType/RAQM',font=ui,fill=ink)
  for i,n in enumerate(['before','after','rubik']):
   p=C/'assets'/f'{n}.ttf';y=110+i*570;d.line((64,y,1536,y),fill=ink,width=2);d.text((64,y+8),n.title(),font=ui,fill=ink);f=ImageFont.truetype(str(p),48);f.set_variation_by_axes([w]);cmap=TTFont(p).getBestCmap()
   for j,t in enumerate(rows):
    pos=(88,y+125+j*80);missing=sorted({ord(c) for c in t}-set(cmap))
    if missing:
     assert n=='rubik';d.text(pos,'Unavailable in Rubik: '+', '.join(f'U+{c:04X}' for c in missing)+' (this row)',font=ui,fill=ink,anchor='ls');continue
    box=d.textbbox(pos,t,font=f,anchor='ls',direction='ltr');assert box[2]<1536 and box[3]<y+568,box
    d.text(pos,t,font=f,fill=ink,anchor='ls',direction='ltr')
  out=C/f'{kind}-{w}.png';im.save(out);receipt.append({'weight':w,'kind':kind,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(C/'compiled-proofs.json').write_text(json.dumps({'renderer':'Pillow FreeType/RAQM','pages':pages,'images':receipt,'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['before','after','rubik']}},ensure_ascii=False,indent=2)+'\n')
