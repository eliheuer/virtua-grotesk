from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;R=C.parents[4]
im=Image.new('RGB',(1600,1200),'#444444');d=ImageDraw.Draw(im);ui=ImageFont.truetype(str(R/'fonts/variable/VirtuaGrotesk[wght].ttf'),24)
for i,w in enumerate([400,550,700]):
 y=40+i*380;d.text((40,y),f'Figure-family reference · {w} · actual Virtua ordinary figures / Rubik superiors',font=ui,fill='#dddddd')
 for j,(p,t,size) in enumerate([(R/'fonts/variable/VirtuaGrotesk[wght].ttf','0 4 5 6 7 8 9',112),(C.parent/'39-superior-digits/assets/rubik.ttf','⁰ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹',224)]):
  f=ImageFont.truetype(str(p),size);f.set_variation_by_axes([w]);d.text((60,y+145+j*215),t,font=f,fill='#dddddd',anchor='ls')
im.save(C/'reference.png')
