from pathlib import Path
import json,hashlib,io
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(ap.read_bytes());bf=TTFont(C/'assets/before.ttf');af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();geometry=0;checks=0;subset_records=[]
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0xad}
def run(f,data,t,w,flags=0):
 h=hb.Font(hb.Face(data));h.set_variations({'wght':w});buf=hb.Buffer();buf.add_str(t);buf.guess_segment_properties();buf.flags=flags;hb.shape(h,buf)
 return [(f.getGlyphName(i.codepoint),p.x_advance,p.x_offset,p.y_offset) for i,p in zip(buf.glyph_infos,buf.glyph_positions)]
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n);geometry+=1
 for text in ['extra\u00adordinary','co\u00adoperate','of\u00adfice','\u00ad','A\u00adB','a\u00ad́b','= ≠ ≠ ≮ ≯','a̵ o̵ i̵ á̵̧́ fi̵ fl̵','a̷ o̷ i̷','a̸ o̸ i̸','≮ ≯ +̸ −̸','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','Ą́ ą́ Į́ į́','fi fl ﬁ ﬂ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
for path in [ap,*sorted((S/'fonts/ttf').glob('*.ttf'))]:
 f=TTFont(path);data=path.read_bytes();sf=TTFont(path);sub=subset.Subsetter();sub.populate(text='extra\u00adordinary co\u00adoperate of\u00adfice -');sub.subset(sf);original_order=sf.getGlyphOrder();stream=io.BytesIO();sf.save(stream);sd=stream.getvalue();sf=TTFont(io.BytesIO(sd));name_map=dict(zip(sf.getGlyphOrder(),original_order))
 for w in ([400,475,550,625,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
  gs=f.getGlyphSet(location={'wght':w} if 'fvar' in f else None)
  a=DecomposingRecordingPen(gs);z=DecomposingRecordingPen(gs);gs['softhyphen'].draw(a);gs['hyphen'].draw(z);assert a.value==z.value and gs['softhyphen'].width==440;checks+=1
  for text in ['extra\u00adordinary','co\u00adoperate','of\u00adfice','\u00ad']:
   for flag in [0,hb.BufferFlags.PRESERVE_DEFAULT_IGNORABLES]:
    expected=run(f,data,text,w,flag);actual=run(sf,sd,text,w,flag);assert [(name_map[n],adv,x,y) for n,adv,x,y in actual]==expected,(path.name,w,text,flag,actual,expected);(subset_records.append({'font':path.name,'weight':w,'text':text,'flags':int(flag),'output':actual}));checks+=1
  sg=sf.getGlyphSet(location={'wght':w} if 'fvar' in sf else None);sp=DecomposingRecordingPen(sg);sg[sf.getBestCmap()[0xad]].draw(sp);assert sp.value==a.value;checks+=1
  assert run(f,data,'\u00ad',w,hb.BufferFlags.PRESERVE_DEFAULT_IGNORABLES)==[('softhyphen',440,0,0)];checks+=1
(C/'subset-checks.json').write_text(json.dumps(subset_records,indent=2)+'\n')
(C/'verification.json').write_text(json.dumps({'checks':checks,'existing_glyph_geometry_comparisons':geometry,'all_existing_ink_advances_unchanged':True,'unchanged_existing_sources':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+00AD'],'preserved_ignorable_glyph_matches_existing_hyphen':True},indent=2)+'\n');print(checks,'checks;',geometry,'old glyph/weight comparisons')
