from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
import pathops,json
C=Path(__file__).resolve().parent;rows=[]
fnt=TTFont(C/'assets/after.ttf');cm=fnt.getBestCmap()
for w in [400,475,550,625,700]:
 gs=fnt.getGlyphSet(location={'wght':w})
 for a,b in [('¹','⁴'),('¹','²'),('³','⁴')]:
  paths=[];x=0
  for n,dx,dy in [(cm[ord(a)],0,0),('fraction',gs[cm[ord(a)]].width,0),(cm[ord(b)],gs[cm[ord(a)]].width+264,-384)]:
   p=pathops.Path();gs[n].draw(TransformPen(p.getPen(),(1,0,0,1,dx,dy)));p.simplify();paths.append(p)
  overlap=[]
  for i,j in [(0,1),(1,2),(0,2)]:
   z=pathops.op(paths[i],paths[j],pathops.PathOp.INTERSECTION);overlap.append(abs(z.area))
  rows.append({'weight':w,'diagnostic_pair':a+b,'denominator_y_offset':-384,'intersection_areas':overlap})
(C/'layout-trials.json').write_text(json.dumps({'not_release_forms':True,'note':'Existing purple superior ink assembled only in proof; no new numerator/denominator or features. Exact intersection areas, not optical approval.','rows':rows},indent=2)+'\n');print(rows)
for w in [400,550,700]:
 im=Image.new('RGB',(1600,1100),'#444');d=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/before.ttf'),26);d.text((50,30),f'Diagnostic fraction layout only · {w} · no installed fraction forms',font=ui,fill='#dedede')
 for idx,px in enumerate([48,224]):
  f=ImageFont.truetype(str(C/'assets/after.ttf'),px);f.set_variation_by_axes([w]);baseline=230+idx*430;x=64
  for a,b in [('¹','⁴'),('¹','²'),('³','⁴')]:
   d.text((x,baseline),a,font=f,fill='#dedede',anchor='ls');aw=f.getlength(a);d.text((x+aw,baseline),'⁄',font=f,fill='#dedede',anchor='ls');d.text((x+aw+264*px/1024,baseline+384*px/1024),b,font=f,fill='#dedede',anchor='ls');x+=aw+264*px/1024+f.getlength(b)+100
 d.text((50,850),'Superior 1/3 unchanged; denominator 2/4 shifted down384 only in this proof.',font=ui,fill='#dedede');d.text((50,900),'Not approved fraction numerators/denominators; assess slash nesting and weight.',font=ui,fill='#dedede');im.save(C/f'layout-{w}.png')
 if w==550:continue
 im=Image.new('RGB',(1600,1300),'#444');d=ImageDraw.Draw(im)
 for i,n in enumerate(['after','rubik']):
  y=80+i*580;d.text((64,y),f'{n} · {w} · 224px · slash and ordinary figures',font=ui,fill='#dedede');f=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);f.set_variation_by_axes([w]);d.text((180,y+100),'⁄ 1⁄4',font=f,fill='#dedede')
 im.save(C/f'detail-{w}.png')
