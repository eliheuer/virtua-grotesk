from pathlib import Path
import hashlib,json,os,xml.etree.ElementTree as E,plistlib,unicodedata,io
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',b['scratch']));changes=json.loads((C/'changes.json').read_text());dep=json.loads((C/'dependencies.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==owned[p]['after'] if p in owned else sha(S/p)==h,p
for x in changes:
 old=E.parse(C/'before-sources'/x['path']).getroot();new=E.parse(S/x['path']).getroot()
 assert float(new.find('advance').get('width'))%8==0
 old.find('advance').set('width',new.find('advance').get('width'));assert E.tostring(old)==E.tostring(new),x['path']
rr=[]
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr.append({n:E.parse(d/f).getroot() for n,f in idx.items()})
assert rr[0].keys()==rr[1].keys()
for n,a in rr[0].items():
 z=rr[1][n];assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in z.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in z.findall('outline/component')],n
bf=TTFont(C/'assets/before.ttf');af=TTFont(S/'fonts/variable/VirtuaGrotesk[wght].ttf');bd=(C/'assets/before.ttf').read_bytes();ad=(S/'fonts/variable/VirtuaGrotesk[wght].ttf').read_bytes();targets={**dep['Regular']['targets'],**dep['Bold']['targets']};allowed=set(targets);checks=0;metrics={};fallback_findings=[];tables={}
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w});wd=[]
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value,(w,n,'ink changed')
  if bg[n].width!=ag[n].width:wd.append(n)
 assert set(wd)<=allowed,(w,set(wd)-allowed)
 if w in [400,700]:assert set(wd)==set(dep['Regular' if w==400 else 'Bold']['targets'])
 for n,t in targets.items():
  base=t['base'];char=t['char'];assert ag[n].width==ag[base].width,(w,n)
  assert shaped(af,ad,char,w)==shaped(af,ad,unicodedata.normalize('NFD',char),w)
  assert shaped(af,ad,char,w)[0]==shaped(af,ad,base,w)[0]
  checks+=3
  if w in [400,700]:
   pen=BoundsPen(ag);ag[n].draw(pen);before=bg[n].width;after=ag[n].width
   tables[f'{w}:{n}']={'before_advance':before,'after_advance':after,'base':base,'bounds':pen.bounds,'left_bearing':pen.bounds[0],'right_bearing_before':before-pen.bounds[2],'right_bearing_after':after-pen.bounds[2],'advance_popcount':int(after).bit_count(),'right_bearing_on8':(after-pen.bounds[2])%8==0}
 for text in ['ģ ķ ļ ņ ŗ','ĽďľŤť','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
 metrics[str(w)]=wd
(C/'spacing-measurements.json').write_text(json.dumps(tables,indent=2)+'\n')
# Advances fix only; kerning tables and all compiled ink remain exact.
for tag in ['GPOS','GSUB','GDEF','cmap']:
 assert bf.getTableData(tag)==af.getTableData(tag),tag
out={'checks':checks,'unchanged_source_files':len(b['sources'])-len(owned),'changed_metrics':metrics,'all_compiled_ink_unchanged':True,'layout_tables_unchanged':True,'font_sha256':sha(S/'fonts/variable/VirtuaGrotesk[wght].ttf')}
(C/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,'checks; exact ink/layout/source preservation; all master topology compatible')

# Basic missing-cmap fallback: diagnose widths only, not mark placement equality.
result={}
for name,font,data in [('before',bf,bd),('after',af,ad)]:
 fallback=TTFont(io.BytesIO(data))
 for tab in fallback['cmap'].tables:
  if tab.isUnicode():
   for t in targets.values():tab.cmap.pop(ord(t['char']),None)
 stream=io.BytesIO();fallback.save(stream);fail=[]
 for w in [400,475,550,625,700]:
  for n,t in targets.items():
   x=shaped(font,data,t['char'],w)[0];y=shaped(fallback,stream.getvalue(),t['char'],w)[0]
   if x!=y:fail.append({'weight':w,'glyph':n,'full':x,'fallback':y})
 result[name]=fail
(C/'fallback-advance.json').write_text(json.dumps(result,indent=2)+'\n');assert not result['after'];print('Fallback advance differences', {k:len(v) for k,v in result.items()})
