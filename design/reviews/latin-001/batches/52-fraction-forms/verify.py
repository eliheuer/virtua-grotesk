from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from tests.test_latin_diacritics import shaped
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();geometry=0;checks=0
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0xBC,0xBD,0xBE};assert not any(r.FeatureTag in ['frac','numr','dnom','sups'] for r in af['GSUB'].table.FeatureList.FeatureRecord)
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 for text in ['¼','½','¾','¼½¾','¼́','½̧','¾̈','A¼m','1½ kg']:
  advance,boxes=shaped(af,ad,text,w);assert advance>0 and any(x is not None for x in boxes) and all(ord(c) in af.getBestCmap() for c in text);checks+=1
 for text in ['1/4 1/2 3/4','¹²³⁴ ⁰⁵⁶⁷⁸⁹','µm µ̧́','¦ ¤ ± ¬','= ≠ ≠ ≮ ≯','a̵ o̵ i̵ á̵̧́ fi̵ fl̵','a̷ o̷ i̷','a̸ o̸ i̸','≮ ≯ +̸ −̸','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+00BC','U+00BD','U+00BE'],'U2044_absent':0x2044 not in af.getBestCmap(),'feature_scope':'No frac/numr/dnom/sups or U2044; encoded fraction wrappers only on scratch.'},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight comparisons')

assert 0x2044 not in af.getBestCmap()
