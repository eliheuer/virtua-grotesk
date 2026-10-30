from pathlib import Path
import io,json,unicodedata as U,hashlib,os
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];base=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',base['scratch']));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();owned={x['path']:x for x in json.loads((C/'changes.json').read_text())}
for p,h in base['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
before=TTFont(C/'assets/before.ttf');after=TTFont(S/'fonts/variable/VirtuaGrotesk[wght].ttf');bd=(C/'assets/before.ttf').read_bytes();ad=(S/'fonts/variable/VirtuaGrotesk[wght].ttf').read_bytes();(C/'assets/after.ttf').write_bytes(ad)
letters='ĄąĘęĮįŲų';suffixes=['','́','̀','̂','̃','̄','̆','̇','̈','̊','̋','̌','̨','́́','̧́'];records={};checks=0
for name,font,data in [('before',before,bd),('after',after,ad)]:
 fallback=TTFont(io.BytesIO(data))
 for t in fallback['cmap'].tables:
  if t.isUnicode():
   for c in letters:t.cmap.pop(ord(c),None)
 stream=io.BytesIO();fallback.save(stream);(C/'assets'/f'{name}-fallback.ttf').write_bytes(stream.getvalue());fail=[]
 for w in [400,475,550,625,700]:
  for c in letters:
   for suffix in suffixes:
    t=c+suffix;expected=shaped(font,data,t,w);actual=shaped(fallback,stream.getvalue(),t,w)
    if (expected[0],sorted(expected[1]))!=(actual[0],sorted(actual[1])):fail.append({'weight':w,'text':t,'full':expected,'fallback':actual})
    checks+=1
 records[name]=fail
# Every original glyph and non-GSUB/GDEF layout table stays exact.
assert before.getBestCmap()==after.getBestCmap()
# Adding a mark-filter set reindexes GPOS references without changing positioning.
for lookup in after['GPOS'].table.LookupList.Lookup:
 if hasattr(lookup,'MarkFilteringSet'):
  glyphs=after['GDEF'].table.MarkGlyphSetsDef.Coverage[lookup.MarkFilteringSet].glyphs
  lookup.MarkFilteringSet=next(i for i,cov in enumerate(before['GDEF'].table.MarkGlyphSetsDef.Coverage) if cov.glyphs==glyphs)
assert before.getTableData('GPOS')==after.getTableData('GPOS')
for table in ['glyf','gvar','hmtx','cmap','OS/2','hhea']:assert before.getTableData(table)==after.getTableData(table),table
# Full-font existing canonical ogonek and other source characters must not regress.
unchanged=0;changed=[]
for w in [400,475,550,625,700]:
 for c in letters:
  for s in suffixes:
   t=c+s
   if shaped(before,bd,t,w)!=shaped(after,ad,t,w):changed.append({'weight':w,'text':t})
   unchanged+=1
 for cp in before.getBestCmap():
  if cp<32 or 0x7f<=cp<0xa0:continue
  t=chr(cp)
  assert shaped(before,bd,t,w)==shaped(after,ad,t,w),(w,t)
  unchanged+=1
 for t in ['ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇','fine flow office','ģ ļ ŗ','ḩ̌́']:
  assert shaped(before,bd,t,w)==shaped(after,ad,t,w),(w,t);unchanged+=1
report={'fallback_comparisons':checks,'before_failures':records['before'],'after_failures':records['after'],'full_font_ogonek_changes':changed,'unchanged_checks':unchanged,'unchanged_source_files':len(base['sources'])-2,'font_sha256':sha(S/'fonts/variable/VirtuaGrotesk[wght].ttf')};(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('fallback failures',len(records['before']),len(records['after']),'full font changes',len(changed),'unchanged checks',unchanged)
assert not records['after'] and not changed
