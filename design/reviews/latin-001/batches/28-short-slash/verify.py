from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,plistlib
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.areaPen import AreaPen
from tests.test_latin_diacritics import shaped
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
for x in changes:assert sha(S/x['path'])==x['after']
rr=[]
for glyph in ['slashshortcomb','slashshortcomb.narrow']:
 rr=[]
 for m in ['Regular','Bold']:
  r=E.parse(S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/{glyph}.glif').getroot();points=r.findall('outline/contour/point')
  assert len(points)==8 and all(pt.get('type')=='line' for pt in points)
  assert all(int(pt.get('x'))%8==int(pt.get('y'))%8==0 for pt in points+r.findall('anchor'));rr.append([pt.get('type') for pt in points])
  xy=[(int(pt.get('x')),int(pt.get('y'))) for pt in points]
  cross=[(xy[(i+1)%8][0]-xy[i][0])*(xy[(i+2)%8][1]-xy[(i+1)%8][1])-(xy[(i+1)%8][1]-xy[i][1])*(xy[(i+2)%8][0]-xy[(i+1)%8][0]) for i in range(8)]
  assert all(c>0 for c in cross) or all(c<0 for c in cross)
 assert rr[0]==rr[1]
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();checks=0;geometry=0;records=[]
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x337};name=af.getBestCmap()[0x337];assert af['GDEF'].table.GlyphClassDef.classDefs[name]==3
for cp,n in bf.getBestCmap().items():assert af.getBestCmap()[cp]==n
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 p=AreaPen(ag);ag[name].draw(p);assert p.value<0 # TrueType outer direction
 assert ag[name].width==0
 for base in ['A','O','a','o','g','h','i','j','į','á','ā','Ą','ȟ','ſ','ƒ','ŉ','ĸ','ŧ','◌']:
  adv,boxes=shaped(af,ad,base+'\u0335',w);assert len(boxes)==2,(base,w,boxes)
  ba,bb=shaped(af,ad,base,w);assert adv==ba and boxes[0]==bb[0],(base,w,boxes,bb)
  y=432 if base=='◌' else (384 if base.isupper() else 288)
  assert abs((boxes[1][1]+boxes[1][3])/2-y)<1,(base,w,boxes)
  assert boxes[1][0]<boxes[0][2] and boxes[1][2]>boxes[0][0],(base,w,boxes)
  # Existing accents must stay on their original base positions with an overlay inserted.
  for marks in ['́','̧','̧́','̒','̒́']:
   _,marked=shaped(af,ad,base+'\u0335'+marks,w);_,ordinary=shaped(bf,bd,base+marks,w)
   assert sorted(marked[:1]+marked[2:])==sorted(ordinary),(base,marks,w,marked,ordinary)
   checks+=1
  records.append({'weight':w,'base':base,'overlay_bounds':boxes[1],'body_bounds':boxes[0]});checks+=2
 for text in ['fi̷','fl̷','ﬁ̷','ﬂ̷','f̷i','f̷l','í̷̧','j̷̦','o̷̷']:
  advance,bb=shaped(af,ad,text,w);assert all(z is not None for z in bb);checks+=1
 for text in ['a̵ o̵ i̵ á̵̧́ fi̵ fl̵','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoint':'U+0337','compiled_glyph_name':name,'sampled_placements':records},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight preservation comparisons')
