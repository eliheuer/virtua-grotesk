from pathlib import Path
import json,hashlib,io
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();geometry=0;checks=0
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x2264,0x2265}
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 for name in ['lessequal','greaterequal']:
  assert af['GDEF'].table.GlyphClassDef.classDefs.get(name,1)==1
  assert ag[name].width==600
  pen=DecomposingRecordingPen(ag);ag[name].draw(pen)
  contours=[]
  for op,pts in pen.value:
   if op=='moveTo':contours.append([pts[0]])
   elif op=='lineTo':contours[-1].append(pts[0])
  assert [len(p) for p in contours]==[16,8]
  for pts in contours:
   area=sum(x*pts[(i+1)%len(pts)][1]-y*pts[(i+1)%len(pts)][0] for i,(x,y) in enumerate(pts))/2
   assert area<0,(name,w,area)
   def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
   for i,(a,edge_end) in enumerate(zip(pts,pts[1:]+pts[:1])):
    for j,(d,e) in enumerate(zip(pts,pts[1:]+pts[:1])):
     if abs(i-j)<=1 or {i,j}=={0,len(pts)-1}:continue
     assert not (cross(a,edge_end,d)*cross(a,edge_end,e)<0 and cross(d,e,a)*cross(d,e,edge_end)<0),(name,w,i,j)
  assert min(y for x,y in contours[0])-max(y for x,y in contours[1])>=40
  checks+=5
 for base,encoded in [('≤','≰'),('≥','≱')]:
  assert shaped(af,ad,encoded,w)==shaped(af,ad,base+'̸',w)
  advance,boxes=shaped(af,ad,encoded,w);assert advance==600 and len(boxes)==2
  assert boxes[1][1]<boxes[0][1] and boxes[1][3]>boxes[0][3]
  checks+=3
 for text in ['= ≠ ≠ ≮ ≯','a̵ o̵ i̵ á̵̧́ fi̵ fl̵','a̷ o̷ i̷','a̸ o̸ i̸','≮ ≯ +̸ −̸','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1

(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+2264','U+2265'],'compiled_polygons_clockwise_no_proper_crossings_at_five_weights':True},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight comparisons')
