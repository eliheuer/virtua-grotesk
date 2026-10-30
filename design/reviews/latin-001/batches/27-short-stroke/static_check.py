from pathlib import Path
import json,hashlib,io
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.varLib.instancer import instantiateVariableFont,OverlapMode
from PIL import Image,ImageDraw,ImageFont
C=Path(__file__).resolve().parent;S=Path(json.loads((C/'baseline.json').read_text())['scratch']);vf=TTFont(S/'fonts/variable/VirtuaGrotesk[wght].ttf');report=[]
for p in sorted((S/'fonts/ttf').glob('*.ttf')):
 af=TTFont(p);w=af['OS/2'].usWeightClass;bf=TTFont(C/'baseline-fonts/ttf'/p.name);inst=instantiateVariableFont(vf,{'wght':w},inplace=False,overlap=OverlapMode.REMOVE);stream=io.BytesIO();inst.save(stream);stream.seek(0);inst=TTFont(stream);ags=af.getGlyphSet();bgs=bf.getGlyphSet();igs=inst.getGlyphSet();changed=[];widths=[]
 for n in bgs:
  a=DecomposingRecordingPen(ags);b=DecomposingRecordingPen(bgs);ags[n].draw(a);bgs[n].draw(b)
  if a.value!=b.value:changed.append(n)
  if ags[n].width!=bgs[n].width:widths.append([n,bgs[n].width,ags[n].width])
 for n in ags:
  a=DecomposingRecordingPen(ags);b=DecomposingRecordingPen(igs);ags[n].draw(a);igs[n].draw(b)
  assert a.value==b.value and ags[n].width==igs[n].width,(p,n)
 report.append({'font':p.name,'weight':w,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'old_static_segment_differences':changed,'old_static_width_differences':widths,'new_static_matches_serialized_overlap_removed_variable':True})
 im=Image.new('RGB',(1600,980),'#444444');d=ImageDraw.Draw(im);ui=ImageFont.truetype(str(C/'assets/before.ttf'),26)
 d.text((40,20),f'Static build comparison {w} · Before / VF-derived After',font=ui,fill='#dddddd')
 texts=['Hamburgefonts Oops áéóú Ąą Ŧŧ fi fl','București ģimene doğa ĽďľŤť ḩ̌́','مرحبا بالعالم ببب ب ھھھ ھ','שָׁלוֹם עוֹלָם']
 for row,t in enumerate(texts):
  for j,path in enumerate([C/'baseline-fonts/ttf'/p.name,p]):
   f=ImageFont.truetype(str(path),48);d.text((60,90+row*215+j*80),t,font=f,fill='#dddddd',direction='rtl' if row>=2 else 'ltr')
 im.save(C/f'static-{w}.png')
(C/'static-build-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print([(x['font'],len(x['old_static_segment_differences']),len(x['old_static_width_differences'])) for x in report])
