from pathlib import Path
import hashlib,json,os,plistlib,xml.etree.ElementTree as E,unicodedata,io
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];base=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',base['scratch']));changes=json.loads((C/'changes.json').read_text());closure=json.loads((C/'dependencies.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
allowed={x['path'] for x in changes}
assert all(sha(S/p)==h for p,h in base['sources'].items() if p not in allowed)
for x in changes:assert sha(S/x['path'])==x['after']
roots={}
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());roots[m]={n:E.parse(d/f).getroot() for n,f in idx.items()}
assert roots['Regular'].keys()==roots['Bold'].keys()
for n,a in roots['Regular'].items():
 b=roots['Bold'][n]
 assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in b.findall('outline/component')],n
for x in changes:
 if 'glyph' not in x:continue
 old=E.parse(C/'before-sources'/x['path']).getroot();new=E.parse(S/x['path']).getroot()
 assert old.find('advance').attrib==new.find('advance').attrib
 assert old.find('outline/component').attrib==new.find('outline/component').attrib
 assert not new.findall('outline/contour')
 mark=new.find("outline/component[@base='commaaccent']")
 assert all(float(mark.get(a,'0'))%8==0 for a in ['xOffset','yOffset'])
 assert all(float(a.get(k))%8==0 for a in new.findall('anchor') for k in ['x','y'])
 assert 'purple' in (S/x['path']).read_text()
before=C/'assets/before.ttf';after=S/'fonts/variable/VirtuaGrotesk[wght].ttf';bf=TTFont(before);af=TTFont(after);bd=before.read_bytes();ad=after.read_bytes();ink={};checks=0
letters='ĢģĶķĻļŅņŖŗ';fallback=TTFont(after)
for table in fallback['cmap'].tables:
 if table.isUnicode():
  for c in letters:table.cmap.pop(ord(c),None)
stream=io.BytesIO();fallback.save(stream)
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w});diff=[]
 for n in bg:
  a=DecomposingRecordingPen(bg);b=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(b)
  if a.value!=b.value:diff.append(n)
 allowed_ink=set(closure['Bold']['consumers']);assert set(diff)==allowed_ink,(w,set(diff)^allowed_ink);ink[str(w)]=diff
 for c in letters:
  result=shaped(af,ad,c,w)
  assert result==shaped(af,ad,unicodedata.normalize('NFD',c),w)
  assert result==shaped(fallback,stream.getvalue(),c,w)
  assert result[0]==shaped(bf,bd,c,w)[0]
  checks+=3
 for text in ['Ç ç Ş ş Ţ ţ Ș ș Ț ț','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
 for text in ['ģ́','ģ̦','Ņ̦','ķ́','ņ́']:
  _,bb=shaped(af,ad,text,w);gap=bb[0][1]-bb[1][3] if text in ['ģ̦','Ņ̦'] else bb[1][1]-bb[0][3]
  assert gap>=16,(w,text,bb);checks+=1
out={'shaping_checks':checks,'changed_compiled_ink':ink,'unchanged_source_files':len(base['sources'])-len(allowed),'after_sha256':sha(after),'notes':['Twenty non-green composites and two Latin feature files only. All Arabic recursive sources, green bases and donors unchanged.','Advances and base components unchanged; new component offsets and explicit anchors on 8.','Latvian NFC/NFD and missing-cmap fallback agree at five weights. Above/below stacks clear.','Existing comma donor is light at Bold and remains a separate drawing follow-up.']};(C/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,'checks; full master compatibility and non-target preservation passed')
