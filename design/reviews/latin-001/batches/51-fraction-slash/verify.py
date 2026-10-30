from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from tests.test_latin_diacritics import shaped
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();geometry=0;checks=0
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x2044};assert not any(r.FeatureTag in ['frac','numr','dnom','sups'] for r in af['GSUB'].table.FeatureList.FeatureRecord)
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 assert ag['fraction'].width==264
 pen=DecomposingRecordingPen(ag);ag['fraction'].draw(pen);pts=[p[0] for op,p in pen.value if op in ['moveTo','lineTo']];assert len(pts)==8
 cross=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 cs=[cross(pts[i],pts[(i+1)%8],pts[(i+2)%8]) for i in range(8)];assert all(v>0 for v in cs) or all(v<0 for v in cs)
 assert min(y for x,y in pts)==0 and max(y for x,y in pts)==768;checks+=4
 for text in ['⁄','⁄⁄⁄','1⁄4','1⁄2','3⁄4','H⁄H','⁄́','⁄̧','12⁄345']:
  advance,boxes=shaped(af,ad,text,w);assert advance>0 and all(x is not None for x in boxes);checks+=1
 for text in ['1/4 1/2 3/4','¹²³⁴ ⁰⁵⁶⁷⁸⁹','µm µ̧́','¦ ¤ ± ¬','= ≠ ≠ ≮ ≯','a̵ o̵ i̵ á̵̧́ fi̵ fl̵','a̷ o̷ i̷','a̸ o̸ i̸','≮ ≯ +̸ −̸','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+2044'],'convex_8_point_polygon_at_five_weights':True,'feature_scope':'No frac/numr/dnom/sups added; full-size digit contexts are not fraction shaping.'},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight comparisons')
