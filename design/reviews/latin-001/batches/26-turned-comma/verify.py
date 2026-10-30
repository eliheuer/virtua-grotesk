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
for m in ['Regular','Bold']:
 p=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/commaturnedabovecomb.glif';r=E.parse(p).getroot();points=r.findall('outline/contour/point');orig=E.parse(S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs/commaaccent.glif').getroot().findall('outline/contour/point')
 assert len(points)==8 and all(pt.get('type')=='line' for pt in points)
 for x,z in zip(points,orig):assert int(x.get('x'))==288-int(z.get('x')) and int(x.get('y'))==576-int(z.get('y'))
 assert all(int(pt.get('x'))%8==int(pt.get('y'))%8==0 for pt in points+r.findall('anchor'));rr.append([pt.get('type') for pt in points])
assert rr[0]==rr[1]
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();checks=0;geometry=0;records=[]
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x312};name=af.getBestCmap()[0x312];assert af['GDEF'].table.GlyphClassDef.classDefs[name]==3
for cp,n in bf.getBestCmap().items():assert af.getBestCmap()[cp]==n
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 p=AreaPen(ag);ag[name].draw(p);assert p.value<0 # TrueType outer direction
 assert ag[name].width==0
 for base in ['A','a','g','h','l','f','i','j','į']:
  adv,boxes=shaped(af,ad,base+'\u0312',w);assert len(boxes)==2,(base,w,boxes);gap=boxes[1][1]-boxes[0][3];assert gap>=24,(base,w,gap)
  h=hb.Font(hb.Face(ad));h.set_variations({'wght':w});buf=hb.Buffer();buf.add_str(base+'\u0312');buf.guess_segment_properties();hb.shape(h,buf);names=[af.getGlyphName(v.codepoint) for v in buf.glyph_infos]
  if base in ['i','j','į']:assert names[0] in ['idotless','jdotless','dotlessiogonek'],names
  adv2,bb=shaped(af,ad,base+'\u0312\u0301',w);assert adv==adv2 and bb[-1][1]-bb[-2][3]>=24,(base,w,bb)
  records.append({'weight':w,'base':base,'gap':gap,'advance':adv,'glyphs':names});checks+=2
 for text in ['i̧̒','j̦̒','g̒̒','ģ̒́']:
  advance,bb=shaped(af,ad,text,w);assert all(z is not None for z in bb);checks+=1
 for text in ['ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoint':'U+0312','compiled_glyph_name':name,'sampled_placements':records},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight preservation comparisons')
