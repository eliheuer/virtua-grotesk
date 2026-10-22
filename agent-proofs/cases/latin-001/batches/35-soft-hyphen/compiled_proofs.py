from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
import hashlib,json
C=Path(__file__).resolve().parent
pages={'forms':['H-H H\uE000H H-H','extra\u00adordinary extraordinary','co\u00adoperate cooperate','of\u00adfice office','a-b a\u00adb a-b','\uE000 \uE000 \uE000'], 'words':['extraordinary · extra\u00adordinary','cooperate · co\u00adoperate','office · of\u00adfice','work-flow · work\u00adflow','București ģimene doğa','București ģimene doğa Ŧŧ ﬁﬂ']}
# PUA only in diagnostic display copies: expose encoded U+00AD ink without the
# default-ignorable suppression. Normal soft-hyphen rows keep normal shaping.
for n in ['before','after','rubik']:
 f=TTFont(C/'assets'/f'{n}.ttf');g=f.getBestCmap().get(0xad)
 for t in f['cmap'].tables:
  if t.isUnicode():
   t.cmap.pop(0xE000,None)
   if g:t.cmap[0xE000]=g
 f.save(C/'assets'/f'{n}-display.ttf')
receipt=[]
for kind,rows in pages.items():
 for w in [400,550,700]:
  im=Image.new('RGB',(1600,1840),(68,68,68));d=ImageDraw.Draw(im);ink=(222,222,222)
  ui=ImageFont.truetype(str(C/'assets/before.ttf'),30);ui.set_variation_by_axes([400]);d.text((64,28),f'Soft hyphen · {kind} · {w} · FreeType/RAQM',font=ui,fill=ink)
  for i,n in enumerate(['before','after','rubik']):
   p=C/'assets'/f'{n}-display.ttf';y=110+i*570;d.line((64,y,1536,y),fill=ink,width=2);d.text((64,y+8),n.title()+' · PUA diagnostic = visible U+00AD',font=ui,fill=ink);f=ImageFont.truetype(str(p),48);f.set_variation_by_axes([w]);cmap=TTFont(p).getBestCmap()
   for j,t in enumerate(rows):
    pos=(88,y+125+j*80);missing=sorted({ord(c) for c in t}-set(cmap)-{0xAD})
    if missing:
     d.text(pos,'Unavailable in '+n.title()+': '+', '.join(('U+00AD visible diagnostic' if c==0xE000 else f'U+{c:04X}') for c in missing)+' (this row)',font=ui,fill=ink,anchor='ls');continue
    box=d.textbbox(pos,t,font=f,anchor='ls',direction='ltr');assert box[2]<1536 and box[3]<y+568,box
    d.text(pos,t,font=f,fill=ink,anchor='ls',direction='ltr')
  out=C/f'{kind}-{w}.png';im.save(out);receipt.append({'weight':w,'kind':kind,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(C/'compiled-proofs.json').write_text(json.dumps({'renderer':'Pillow FreeType/RAQM','pages':pages,'images':receipt,'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['before','after','rubik']}},ensure_ascii=False,indent=2)+'\n')
