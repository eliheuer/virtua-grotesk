from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;R=C.parents[3]
paths=[('Before',C.parent/'working-v5/fonts/after-e38a34944099.ttf'),('Working',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('Rubik',next((C.parent/'working-v5/fonts').glob('rubik*.ttf')))]
im=Image.new('RGB',(1800,1350),'#181818');d=ImageDraw.Draw(im);label=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24)
for row,w in enumerate([400,550,700]):
 for col,(title,p) in enumerate(paths):
  x=32+col*600;y=340+row*450
  d.text((x,24+row*450),f'{title} · {w}',font=label,fill='#dedede')
  f=ImageFont.truetype(str(p),300);f.set_variation_by_axes([w])
  for ox,ch in [(0,'ש'),(304,'ץ')]:d.text((x+ox,y),ch,font=f,anchor='ls',fill='#dedede')
im.save(C/'compiled-comparison.png')
# Running-text evidence in three equal columns at each master.
im=Image.new('RGB',(1800,660),'#181818');d=ImageDraw.Draw(im)
for row,w in enumerate([400,700]):
 for col,(title,p) in enumerate(paths):
  x=32+col*600;y=24+row*330;d.text((x,y),f'{title} · {w}',font=label,fill='#dedede')
  f=ImageFont.truetype(str(p),42);f.set_variation_by_axes([w])
  for i,s in enumerate(['שמש שקט שישה שירים','עץ ארץ קיץ חוץ קיבוץ','שָׁלוֹם שֶׁמֶשׁ אֶרֶץ קַיִץ']):d.text((x+530,y+90+i*70),s,font=f,anchor='rs',fill='#dedede')
im.save(C/'compiled-text.png')
