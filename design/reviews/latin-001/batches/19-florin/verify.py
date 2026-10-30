from pathlib import Path
import hashlib,json,os,xml.etree.ElementTree as E,plistlib
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',b['scratch']));changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
for x in changes:assert sha(S/x['path'])==x['after']
rr=[];measure={}
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr.append({n:E.parse(d/f).getroot() for n,f in idx.items()})
 r=rr[-1]['florin'];f=rr[-1]['f'];p=r.findall('outline/contour/point');fp=f.findall('outline/contour/point')
 assert len(p)==40
 shift=16 if m=='Bold' else 32
 # Both upper cubics are the donor's exact controls under translation.
 for i in range(12,24):
  actual=p[i+8];expected=fp[i]
  assert float(actual.get('x'))==float(expected.get('x'))+shift and actual.get('y')==expected.get('y')
  assert actual.get('type')==expected.get('type')
 # Descending cubics are180-degree copies; Bold inner turn moves8 left.
 for i,actual in enumerate(p[:12]):
  expected=fp[i+12];dx=-8 if m=='Bold' and i<4 else 0
  assert float(actual.get('x'))==(408 if m=='Bold' else 320)-float(expected.get('x'))+shift+dx
  assert float(actual.get('y'))==512-float(expected.get('y'))
 assert not r.findall('outline/component')
 assert all(float(x.get('x'))%8==float(x.get('y'))%8==0 for x in p+r.findall('anchor'))
 width=int(r.find('advance').get('width'));assert width%8==0
 measure[f'{m}:florin']={'advance':width,'advance_popcount':width.bit_count(),'points':40,'green_f_curves_unchanged':True,'descending_rotated_hook':True}
assert rr[0].keys()==rr[1].keys()
for n,a in rr[0].items():
 z=rr[1][n];assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in z.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in z.findall('outline/component')],n
bf=TTFont(C/'assets/before.ttf');ap=S/'fonts/variable/VirtuaGrotesk[wght].ttf';af=TTFont(ap);bd=(C/'assets/before.ttf').read_bytes();ad=ap.read_bytes();checks=0
assert set(af.getBestCmap())-set(bf.getBestCmap())=={0x192}
for cp,n in bf.getBestCmap().items():assert af.getBestCmap()[cp]==n
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w})
 assert set(ag)-set(bg)=={'florin'}
 for n in bg:
  a=DecomposingRecordingPen(bg);z=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(z);assert a.value==z.value and bg[n].width==ag[n].width,(w,n)
 for char,name,base in [('ƒ','florin','f')]:
  assert af['GDEF'].table.GlyphClassDef.classDefs.get(name)==1
  pen=BoundsPen(ag);ag[name].draw(pen);bp=BoundsPen(ag);ag[base].draw(bp)
  assert pen.bounds[1:4:2]==(-256,768)
  assert shaped(af,ad,'ƒ',w)!=shaped(af,ad,'s',w)
  assert len(shaped(af,ad,char,w)[1])==1;checks+=2
  for mark in ['\u0301','\u0308','\u030c','\u0326','\u0302\u0301','\u0327\u0301']:
   advance,bb=shaped(af,ad,char+mark,w);assert advance==round(ag[name].width)
   assert len(bb)>=2
   if mark=='\u0326':assert bb[0][1]-bb[1][3]>=16
   elif mark=='\u0327\u0301':assert bb[-1][1]-bb[0][3]>=16
   else:assert bb[1][1]-bb[0][3]>=16
   checks+=1
  if w in [400,700]:measure[f'{"Regular" if w==400 else "Bold"}:{name}'].update({'bounds':pen.bounds,'left_bearing':pen.bounds[0],'right_bearing':ag[name].width-pen.bounds[2]})
 for text in ['ſa ſi ſſ','ģ ļ ŗ','áéóú ÁÉÓÚ','ĽďľŤť','ḩ̌́','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇','TAT tata tot']:
  assert shaped(bf,bd,text,w)==shaped(af,ad,text,w),(w,text);checks+=1
(C/'measurements.json').write_text(json.dumps(measure,indent=2)+'\n')
(C/'verification.json').write_text(json.dumps({'checks':checks,'all_existing_compiled_ink_advances_unchanged':True,'unchanged_existing_source_files':len(b['sources'])-sum(x['before'] is not None for x in changes),'new_codepoints':['U+0192'],'master_compatible':True,'font_sha256':sha(ap)},indent=2)+'\n');print(checks,'scoped checks; all previous glyph ink/metrics exact')
