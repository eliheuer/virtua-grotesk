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
 if x['glyph']=='caroncomb.alt':
  assert old.find('advance').attrib==new.find('advance').attrib
  pts=[(float(p.get('x')),float(p.get('y'))) for p in new.findall('.//point')]
  assert len(pts)==8 and all(v%8==0 for p in pts for v in p)
  assert 'purple' in (S/x['path']).read_text()
 else:
  assert E.tostring(old.find('lib'))==E.tostring(new.find('lib'))
  assert old.find('outline/component').attrib==new.find('outline/component').attrib
  assert float(new.find('advance').get('width'))%8==0
  for comp in new.findall('outline/component'):
   assert all(float(comp.get(k,'0'))%8==0 for k in ['xOffset','yOffset'])
# Linear interpolation of convex corresponding polygons remains convex here;
# check every test instance explicitly, and measure the upper-stem clearances.
geometry=[]
ra=roots['Regular']['caroncomb.alt'];rb=roots['Bold']['caroncomb.alt']
for w in [400,475,550,625,700]:
 t=(w-400)/300;pts=[tuple(float(a.get(k))*(1-t)+float(b.get(k))*t for k in ['x','y']) for a,b in zip(ra.findall('.//point'),rb.findall('.//point'))]
 assert all((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])>0 for a,b,c in zip(pts,pts[1:]+pts[:1],pts[2:]+pts[:2]))
 gaps={}
 for n,stem in {'Lcaron':(180,272),'dcaron':(568,648),'lcaron':(168,248),'tcaron':(208,296)}.items():
  offsets=[float(roots[m][n].find("outline/component[@base='caroncomb.alt']").get('xOffset')) for m in ['Regular','Bold']]
  gap=min(p[0] for p in pts)+offsets[0]*(1-t)+offsets[1]*t-stem[0]*(1-t)-stem[1]*t
  assert gap>=32,(w,n,gap);gaps[n]=gap
 geometry.append({'weight':w,'convex':True,'upper_stem_gaps':gaps,'mark_y_bounds':[min(p[1] for p in pts),max(p[1] for p in pts)]})
(C/'geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
before=C/'assets/before.ttf';after=S/'fonts/variable/VirtuaGrotesk[wght].ttf';bf=TTFont(before);af=TTFont(after);bd=before.read_bytes();ad=after.read_bytes();ink={};checks=0
letters='ĽďľŤť';fallback=TTFont(after)
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
  checks+=2
 for text in ['Ģ ģ Ķ ķ Ļ ļ Ņ ņ Ŗ ŗ','Ą ą Ę ę Į į Ų ų','Ç ç Ş ş Ţ ţ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
 for text in ['Ľ́','ľ́','ď́','ť́','Ť́','Ľ̌','ľ̌','ď̌','ť̌']:
  _,bb=shaped(af,ad,text,w);gap=bb[-1][1]-bb[0][3];assert gap>=16,(w,text,bb);checks+=1
out={'shaping_checks':checks,'changed_compiled_ink':ink,'unchanged_source_files':len(base['sources'])-len(allowed),'after_sha256':sha(after),'geometry':geometry,'notes':['Twelve GLIFs and two Latin feature files only; all base/green/Arabic source bytes unchanged.','64/96-unit clipped alternate marks; upper-stem clearance at least32. All new points/offsets/widths on8.','Corrected uppercase T to ordinary caron; NFC/NFD/basic missing-cmap agree. Above stacks clear. Whole images reviewed separately.']};(C/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,'checks; full master compatibility and non-target preservation passed')
