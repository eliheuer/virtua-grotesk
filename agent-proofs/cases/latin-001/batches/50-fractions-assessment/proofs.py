from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch50'
rows=[('Encoded fractions / Virtua unavailable','¼ ½ ¾',[]),('U2044 / Virtua slash unavailable','1⁄4 1⁄2 3⁄4',[]),('ASCII slash / default','1/4 1/2 3/4',[]),('ASCII slash / frac requested','1/4 1/2 3/4',['frac']),('numr requested / Virtua absent','01234',['numr']),('dnom requested / Virtua absent','01234',['dnom']),('Encoded superiors / position comparison','⁰¹²³⁴',[]),('frac whole run / context hazards','H1/2 12/345 1/2/3',['frac'])]
css=''.join(f'@font-face{{font-family:{n};src:url("{n}.ttf");font-weight:400 700;}}' for n in ['virtua','rubik'])
for w in [400,550,700]:
 cards=''
 for n in ['virtua','rubik']:
  cards+=f'<section style="font-family:{n};font-weight:{w}"><h2>{n} · {w}</h2>'
  for label,text,features in rows:
   settings=', '.join('"'+f+'" 1' for f in features) or 'normal';cards+=f'<label>{label}</label><p style=\'font-feature-settings:{settings}\'>{text}</p>'
  cards+='</section>'
 html=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Fraction assessment {w}</title><style>{css}body{{background:#dedede;color:#444;font-family:system-ui;margin:16px}}h1{{font-size:18px}}main{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}h2{{font:16px system-ui}}label{{font:11px system-ui}}p{{font-size:28px;margin:3px 0 10px;line-height:1.15}}footer{{font:11px system-ui}}</style><h1>Fraction coverage and feature assessment · {w}</h1><main>{cards}</main><footer>Unchanged fonts. Virtua lacks ¼½¾⁄; any browser ink there is unidentified fallback. No CSS scaling/raising.</footer></html>'
 (D/f'comparison-{w}.html').write_text(html);(C/f'comparison-{w}.html').write_text(html.replace('src:url("','src:url("assets/'))
 im=Image.new('RGB',(1600,1600),'#444');draw=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/virtua.ttf'),23)
 for i,n in enumerate(['virtua','rubik']):
  x=64+i*780;f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),48);f.set_variation_by_axes([w]);draw.text((x,32),f'{n} · {w} · 48px',font=ui,fill='#dedede')
  for j,(label,text,features) in enumerate(rows):
   y=100+j*180;draw.text((x,y),label,font=ui,fill='#dedede');draw.text((x,y+50),text,font=f,fill='#dedede',features=features)
 im.save(C/f'fractions-{w}.png')
for w in [400,700]:
 im=Image.new('RGB',(1800,1550),'#444');draw=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/virtua.ttf'),28)
 for j,(n,label,text,features) in enumerate([('virtua','Virtua ordinary donor /','1/4',[]),('virtua','Virtua encoded superiors','¹²³⁴',[]),('rubik','Rubik encoded fractions','¼ ½ ¾',[]),('rubik','Rubik fraction slash / numr+dnom','1⁄4 1⁄2',[])]):
  y=30+j*380;draw.text((64,y),f'{label} · {w} · 224px',font=ui,fill='#dedede');f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);f.set_variation_by_axes([w]);draw.text((64,y+85),text,font=f,fill='#dedede',features=features)
 im.save(C/f'detail-{w}.png')
comp=D/'comparison';subprocess.run([str(R/'.venv/bin/diff3proof'),str(C/'assets/virtua.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(comp)],check=True)
s=(comp/'diff3proof.html').read_text();text='¼ ½ ¾ · 1⁄4 1⁄2 3⁄4 · 1/4 1/2 3/4 · ¹²³⁴ · 12⁄345 · H¼ H½ H¾ · ¼́ ½̧'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1;s=s.replace('Diffenator3 Proof','Diffenator3 · fractions');(comp/'fractions.html').write_text(s)
(C/'proofs.json').write_text(json.dumps({'weights':[400,550,700],'fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['virtua','rubik']},'raster_images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in C.glob('*.png')},'supplement':text,'scope':'No font/source changes. Pillow FreeType RAQM feature controls; actual browser review recorded separately. Missing cmap in Virtua may invoke unidentified browser fallback.'},ensure_ascii=False,indent=2)+'\n')
