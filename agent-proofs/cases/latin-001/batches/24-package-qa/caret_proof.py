from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import json,hashlib
C=Path(__file__).resolve().parent;out=Image.new('RGB',(1600,1000),(68,68,68));d=ImageDraw.Draw(out);ui=ImageFont.truetype(str(C/'assets/after.ttf'),28);ui.set_variation_by_axes([400]);ink=(222,222,222);d.text((64,32),'Ligature caret positions · compiled GDEF · diagnostic lines',font=ui,fill=ink);data=[]
for col,w in enumerate([400,550,700]):
 f=ImageFont.truetype(str(C/'assets/after.ttf'),224);f.set_variation_by_axes([w]);b=ImageFont.truetype(str(C/'assets/before.ttf'),224);b.set_variation_by_axes([w]);inst=instantiateVariableFont(TTFont(C/'assets/after.ttf'),{'wght':w},inplace=False);lc=inst['GDEF'].table.LigCaretList;x=88+col*500
 d.text((x,100),f'Weight {w} · 224px',font=ui,fill=ink)
 for row,(g,t) in enumerate([('fi','ﬁ'),('fl','ﬂ')]):
  y=380+row*380;caret=lc.LigGlyph[lc.Coverage.glyphs.index(g)].CaretValue[0].Coordinate;d.text((x,y),t,font=f,anchor='ls',fill=ink);cx=x+caret*224/1024;d.line((cx,y-184,cx,y+20),fill=(104,204,216),width=2);d.text((x,y+45),f'{g}: x{caret}',font=ui,fill=ink)
  ia=Image.new('L',(400,280));ib=ia.copy();ImageDraw.Draw(ia).text((20,210),t,font=f,anchor='ls',fill=255);ImageDraw.Draw(ib).text((20,210),t,font=b,anchor='ls',fill=255);assert ImageChops.difference(ia,ib).getbbox() is None
  data.append({'weight':w,'glyph':g,'caret':caret,'before_after_pixels_equal':True})
out.save(C/'caret-map.png');(C/'caret-proof.json').write_text(json.dumps({'renderer':'FreeType/RAQM with explicit diagnostic GDEF lines; not a native text-editor cursor test','records':data,'image_sha256':hashlib.sha256((C/'caret-map.png').read_bytes()).hexdigest()},indent=2)+'\n')
