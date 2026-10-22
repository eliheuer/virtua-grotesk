from pathlib import Path
import hashlib,json,os,plistlib,xml.etree.ElementTree as E,unicodedata,io
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];base=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',base['scratch']));changes=json.loads((C/'changes.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();allowed={x['path'] for x in changes}
assert all(sha(S/p)==h for p,h in base['sources'].items() if p not in allowed)
for x in changes:assert sha(S/x['path'])==x['after']
roots={}
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());roots[m]={n:E.parse(d/f).getroot() for n,f in idx.items()}
assert roots['Regular'].keys()==roots['Bold'].keys()
for n,a in roots['Regular'].items():
 b=roots['Bold'][n];assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in b.findall('outline/component')],n
for x in changes:
 if 'glyph' not in x:continue
 old=E.parse(C/'before-sources'/x['path']).getroot();new=E.parse(S/x['path']).getroot()
 assert E.tostring(old.find('lib'))==E.tostring(new.find('lib'))
 assert old.find('outline/component').attrib==new.find('outline/component').attrib
 assert float(new.find('advance').get('width'))%8==0
 for comp in new.findall('outline/component'):
  assert all(float(comp.get(k,'0'))%8==0 for k in ['xOffset','yOffset'])
 for a in new.findall('anchor'):assert all(float(a.get(k))%8==0 for k in ['x','y'])
before=C/'assets/before.ttf';after=S/'fonts/variable/VirtuaGrotesk[wght].ttf';bf=TTFont(before);af=TTFont(after);bd=before.read_bytes();ad=after.read_bytes();checks=0;geometry=[]
fallback=TTFont(after)
for t in fallback['cmap'].tables:
 if t.isUnicode():t.cmap.pop(0x21f,None)
stream=io.BytesIO();fallback.save(stream)
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w});diff=[]
 for n in bg:
  a=DecomposingRecordingPen(bg);b=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(b)
  if a.value!=b.value:diff.append(n)
 assert diff==['hcaron'],diff
 t=(w-400)/300;offset=-96*(1-t)-48*t
 hp=BoundsPen(ag);cp=BoundsPen(ag);ag['h'].draw(hp);ag['caron'].draw(cp);gap=cp.bounds[1]+192-hp.bounds[3];assert gap>=62
 geometry.append({'weight':w,'stem_clearance':gap,'mark_bounds':[cp.bounds[0]+offset,cp.bounds[1]+192,cp.bounds[2]+offset,cp.bounds[3]+192],'advance':ag['hcaron'].width})
 for text in ['ȟ','ȟ́','ȟ̌','ḩ̌','aȟa','ȟȟ','hȟh']:
  expected=shaped(af,ad,text,w)
  assert expected==shaped(af,ad,unicodedata.normalize('NFD',text),w),(w,text,'nfd')
  assert expected==shaped(fallback,stream.getvalue(),text,w),(w,text,'fallback');checks+=2
 for text in ['ȟ́','ȟ̌']:
  _,bb=shaped(af,ad,text,w);assert bb[-1][1]-bb[0][3]>=32,(w,text,bb)
  assert max(b[3] for b in bb)<=af['OS/2'].usWinAscent;checks+=1
 assert shaped(af,ad,'ȟ',w)[0]==shaped(af,ad,'h',w)[0];checks+=1
 for text in ['ĽďľŤť','Ģ ģ Ķ ķ Ļ ļ Ņ ņ Ŗ ŗ','Ą ą Ę ę Į į Ų ų','Ç ç Ş ş Ţ ţ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇','ĥ Ĥ h H']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'unchanged_source_files':len(base['sources'])-len(allowed),'changed_compiled_ink':['hcaron'],'geometry':geometry,'after_sha256':sha(after)},indent=2)+'\n');print(checks,'checks; topology and source preservation passed',geometry)
