from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
import hashlib,json,unicodedata
C=Path(__file__).resolve().parent
rows=['a á ă â ä à ā ą å ã a','e é ě ê ë ė è ē ę e','o ó ô ö ò ő õ o','u ú û ü ù ű ū ų ů u','na ná ne né no nó nu nú','nana nána nene néne nono nóno nunu núnu']
receipt=[]
for w in [400,550,700]:
 im=Image.new('RGB',(1600,1840),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222)
 ui=ImageFont.truetype(str(C/'assets/before.ttf'),30);ui.set_variation_by_axes([400]);d.text((64,28),f'Accented vowel spacing · {w} · FreeType/RAQM',font=ui,fill=ink)
 for i,n in enumerate(['before','after','rubik']):
  p=C/'assets'/f'{n}.ttf';y=110+i*570;d.line((64,y,1536,y),fill=ink,width=2);d.text((64,y+8),n.title(),font=ui,fill=ink);f=ImageFont.truetype(str(p),56);f.set_variation_by_axes([w])
  assert set(ord(c) for c in ''.join(rows))<=set(TTFont(p).getBestCmap())
  for j,t in enumerate(rows):
   pos=(88,y+125+j*80);box=d.textbbox(pos,t,font=f,anchor='ls',direction='ltr');assert box[2]<1536 and box[3]<y+568,box
   d.text(pos,t,font=f,fill=ink,anchor='ls',direction='ltr')
 out=C/f'whole-{w}.png';im.save(out);receipt.append({'weight':w,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(C/'compiled-proofs.json').write_text(json.dumps({'renderer':'Pillow FreeType/RAQM','rows':rows,'images':receipt,'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['before','after','rubik']}},ensure_ascii=False,indent=2)+'\n')
