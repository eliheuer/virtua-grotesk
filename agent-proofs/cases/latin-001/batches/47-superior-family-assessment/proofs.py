from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch47';sup='⁰¹²³⁴⁵⁶⁷⁸⁹'
rows=[('Encoded superior0–9',sup,[]),('Ordinary figures','0123456789',[]),('sups requested · Virtua absent','0123456789',['sups']),('tnum + sups requested','0123456789',['tnum','sups']),('Repeated encoded pairs','⁰⁰ ¹¹ ²² ³³ ⁴⁴ ⁵⁵ ⁶⁶ ⁷⁷ ⁸⁸ ⁹⁹',[]),('Fractions: frac requested','1/2 3/4',['frac'])]
css=''.join(f'@font-face{{font-family:{n};src:url("{n}.ttf");font-weight:400 700;}}' for n in ['virtua','rubik'])
for w in [400,550,700]:
 cards=''
 for n in ['virtua','rubik']:
  cards+=f'<section style="font-family:{n};font-weight:{w}"><h2>{n} · {w}</h2>'
  for label,text,features in rows:
   settings=', '.join('"'+f+'" 1' for f in features) or 'normal';cards+=f'<label>{label}</label><p style=\'font-feature-settings:{settings}\'>{text}</p>'
  cards+='</section>'
 html=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Superior family {w}</title><style>{css}body{{background:#dedede;color:#444;font-family:system-ui;margin:20px}}h1{{font-size:20px}}main{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}h2{{font:18px system-ui}}label{{font:11px system-ui}}p{{font-size:28px;margin:6px 0 18px;line-height:1.35}}footer{{font:12px system-ui}}</style><h1>Complete superior-family assessment · {w}</h1><main>{cards}</main><footer>Actual unchanged fonts. No CSS scaling/raising. Encoded glyphs and feature access are separate.</footer></html>'
 (D/f'comparison-{w}.html').write_text(html);(C/f'comparison-{w}.html').write_text(html.replace('src:url("','src:url("assets/'))
 im=Image.new('RGB',(1600,1400),'#444');draw=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/virtua.ttf'),26)
 for i,n in enumerate(['virtua','rubik']):
  x=64+i*780;f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),48);f.set_variation_by_axes([w]);draw.text((x,32),f'{n} · {w} · 48px',font=ui,fill='#dedede')
  for j,(label,text,features) in enumerate(rows):
   y=110+j*190;draw.text((x,y),label,font=ui,fill='#dedede');draw.text((x,y+55),text,font=f,fill='#dedede',features=features)
 im.save(C/f'family-{w}.png')
for w in [400,700]:
 im=Image.new('RGB',(1600,1100),'#444');draw=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/virtua.ttf'),28)
 for i,n in enumerate(['virtua','rubik']):
  y=40+i*530;draw.text((64,y),f'{n} · {w} · 224px · encoded family',font=ui,fill='#dedede');f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);f.set_variation_by_axes([w]);draw.text((64,y+180),sup,font=f,fill='#dedede')
 im.save(C/f'detail-{w}.png')
comp=D/'comparison';subprocess.run([str(R/'.venv/bin/diff3proof'),str(C/'assets/virtua.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(comp)],check=True)
s=(comp/'diff3proof.html').read_text();text=sup+' · ⁰⁰ ¹¹ ²² ³³ ⁴⁴ ⁵⁵ ⁶⁶ ⁷⁷ ⁸⁸ ⁹⁹ · H⁰ H¹ H² H³ H⁴ H⁵ H⁶ H⁷ H⁸ H⁹ · 0123456789 · Text¹ notes² powers³'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1;s=s.replace('Diffenator3 Proof','Diffenator3 · superior family');(comp/'superior-family.html').write_text(s)
(C/'proofs.json').write_text(json.dumps({'weights':[400,550,700],'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['virtua','rubik']},'raster_images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in C.glob('*.png')},'supplement':text,'scope':'No font/source changes. Pillow FreeType RAQM feature controls; actual browser review recorded separately.'},ensure_ascii=False,indent=2)+'\n')
