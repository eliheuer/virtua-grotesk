from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
import pathops,json,xml.etree.ElementTree as E
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;f=TTFont(C/'assets/after.ttf');rows=[]
S=Path(json.loads((C/'baseline.json').read_text())['scratch'])
for n in ['one.numr','two.dnom','three.numr','four.dnom','fraction.slash','onequarter','onehalf','threequarters']:
 roots=[E.parse(S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{n}.glif') for m in ['Regular','Bold']]
 assert [[[(p.tag,p.get('type')) for p in c] for c in r.findall('outline/contour')] for r in roots][0]==[[[(p.tag,p.get('type')) for p in c] for c in r.findall('outline/contour')] for r in roots][1]
for w in [400,475,550,625,700]:
 gs=f.getGlyphSet(location={'wght':w})
 for name,a,z in [('onequarter','one.numr','four.dnom'),('onehalf','one.numr','two.dnom'),('threequarters','three.numr','four.dnom')]:
  na=gs[a].width;paths=[]
  for n,dx in [(a,0),('fraction.slash',na-16),(z,na+232)]:
   p=pathops.Path();gs[n].draw(TransformPen(p.getPen(),(1,0,0,1,dx,0)));p.simplify();paths.append(p)
  areas=[abs(pathops.op(paths[i],paths[j],pathops.PathOp.INTERSECTION).area) for i,j in [(0,1),(1,2),(0,2)]]
  assert not any(areas),(w,name,areas)
  assert gs[name].width==na+232+gs[z].width
  rows.append({'weight':w,'glyph':name,'advance':gs[name].width,'intersections':areas,'bounds':[list(p.bounds) for p in paths]})
(C/'layout-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
for w in [400,700]:
 im=Image.new('RGB',(1600,1100),'#444');d=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/before.ttf'),26)
 for i,n in enumerate(['after','rubik']):
  y=40+i*520;d.text((40,y),f'{n} · {w} · 224px · encoded fraction trial',font=ui,fill='#dedede');ff=ImageFont.truetype(str(C/'assets'/f'{n}.ttf'),224);ff.set_variation_by_axes([w]);d.text((50,y+100),'¼ ½ ¾',font=ff,fill='#dedede')
 im.save(C/f'detail-{w}.png')
print('15 fraction layouts /45 pair intersections clear; compatible sources')
