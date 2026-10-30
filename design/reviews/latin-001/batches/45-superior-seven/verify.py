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
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x2077}
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 for name in ['sevensuperior']:
  assert af['GDEF'].table.GlyphClassDef.classDefs.get(name,1)==1
  assert 0<ag[name].width<440
  pen=DecomposingRecordingPen(ag);ag[name].draw(pen)
  checks+=2
 for text in ['⁷','x⁷ x¹ x² x³','10⁷ 10¹','⁷⁷⁷','⁷́','⁷̧']:
  advance,boxes=shaped(af,ad,text,w);assert len([b for b in boxes if b])==len(text.replace(" ",""));checks+=1
 assert not any(r.FeatureTag=='sups' for r in af['GSUB'].table.FeatureList.FeatureRecord)
 for text in ['123 101 202 303','= ≠ ≠ ≮ ≯','a̵ o̵ i̵ á̵̧́ fi̵ fl̵','a̷ o̷ i̷','a̸ o̸ i̸','≮ ≯ +̸ −̸','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1

(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+2077'],'new_encoded_superior_shaping_checked':True},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight comparisons')
