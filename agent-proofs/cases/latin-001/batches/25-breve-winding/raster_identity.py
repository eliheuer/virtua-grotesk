from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from fontTools.ttLib import TTFont
import json,hashlib,numpy as np
C=Path(__file__).resolve().parent;checks=0;diff=[]
texts=['˘','Ă Ĕ Ĭ Ŏ Ŭ Ğ','ă ĕ ĭ ŏ ŭ ğ','ắ ĕ̈ ĭ̌ ŏ́ ŭ̈ ğ̌','pădure · dağ doğa yağmur']
for w in [400,475,550,625,700]:
 for px in [32,48,224]:
  for text in texts:
   images=[]
   for n in ['before','after']:
    im=Image.new('L',(3600,520),0);d=ImageDraw.Draw(im);f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),px);f.set_variation_by_axes([w]);d.text((64,340),text,font=f,fill=255,anchor='ls',direction='ltr');images.append(im)
   bbox=ImageChops.difference(*images).getbbox()
   if bbox:
    ar=np.array(images[0],dtype=int);br=np.array(images[1],dtype=int);delta=np.abs(ar-br);diff.append({'w':w,'px':px,'text':text,'bbox':bbox,'changed_pixels':int(np.count_nonzero(delta)),'max_alpha_delta':int(delta.max()),'threshold128_changed_pixels':int(np.count_nonzero((ar>=128)!=(br>=128)))})
   checks+=1
for w in [400,700]:
 im=Image.new('RGB',(1600,1700),(68,68,68));d=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/before.ttf'),28);ui.set_variation_by_axes([400]);d.text((48,24),f'Breve · {w} · 224px/em · FreeType/RAQM',font=ui,fill='white')
 for i,n in enumerate(['before','after','rubik']):
  y=100+i*520;d.line((48,y,1552,y),fill='white');d.text((48,y+12),n.title(),font=ui,fill='white');f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);f.set_variation_by_axes([w]);d.text((80,y+320),'Ă ă Ğ ğ',font=f,fill=(222,222,222),anchor='ls',direction='ltr');d.text((1080,y+320),'˘',font=f,fill=(222,222,222),anchor='ls',direction='ltr')
 im.save(C/f'detail-{w}.png')
(C/'raster-identity.json').write_text(json.dumps({'checks':checks,'pixel_differences':diff,'method':'FreeType/RAQM same font size, baseline and fill at five weights and 32/48/224px; complete lines fit canvas.'},ensure_ascii=False,indent=2)+'\n');print(checks,'raster comparisons, differences',len(diff))
