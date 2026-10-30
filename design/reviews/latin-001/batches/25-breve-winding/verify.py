from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as E
from fontTools.pens.pointPen import ReverseContourPointPen
from fontTools.pens.recordingPen import RecordingPointPen
from fontTools.pens.areaPen import AreaPen
from fontTools.ufoLib import UFOReader
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changes=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in changes};checks=0;areas={};patterns=[]
def recording(text):
 p=RecordingPointPen();p.beginPath()
 for pt in E.fromstring(text).find('outline/contour'):p.addPoint((int(pt.get('x')),int(pt.get('y'))),segmentType=pt.get('type'),smooth=pt.get('smooth')=='yes')
 p.endPath();return p
for p,h in b['sources'].items():assert sha(S/p)==(owned[p]['after'] if p in owned else h),p
for x in changes:
 old=(C/'before-sources'/x['path']).read_text();new=(S/x['path']).read_text();a=recording(old);z=recording(new);reversed_again=RecordingPointPen();z.replay(ReverseContourPointPen(reversed_again));assert a.value==reversed_again.value
 outside=lambda t:re.sub(r'<contour>.*?</contour>','',t,flags=re.S)
 assert outside(old)==outside(new);checks+=2
 patterns.append([pt.get('type') for pt in E.fromstring(new).find('outline/contour')])
assert patterns[0]==patterns[1]
for m in ['Regular','Bold']:
 areas[m]={}
 for label,root in [('before',R),('after',S)]:
  gs=UFOReader(root/f'sources/VirtuaGrotesk-{m}.ufo').getGlyphSet();p=AreaPen(gs);gs['breve'].draw(p);areas[m][label]=p.value
 assert abs(areas[m]['before']+areas[m]['after'])<1e-8 and areas[m]['after']>0;checks+=1
p=S/'fonts/variable/VirtuaGrotesk[wght].ttf';(C/'assets/after.ttf').write_bytes(p.read_bytes());before=TTFont(C/'assets/before.ttf');after=TTFont(p);changed=[k for k in before.keys() if k!='GlyphOrder' and before.getTableData(k)!=after.getTableData(k)]
for k in ['GPOS','GSUB','GDEF','cmap','hmtx','hhea','OS/2']:assert before.getTableData(k)==after.getTableData(k),k
cons=set(json.loads((C/'dependencies.json').read_text())['Regular']['reverse_consumers']);compiled=set(cons)
# Production names vary; select by unicode or matching source name.
idx=UFOReader(R/'sources/VirtuaGrotesk-Regular.ufo').getGlyphSet();import plistlib
contents=plistlib.loads((R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/contents.plist').read_bytes())
for n in cons:
 for u in E.parse(R/'sources/VirtuaGrotesk-Regular.ufo/glyphs'/contents[n]).getroot().findall('unicode'):
  cp=int(u.get('hex'),16)
  if cp in before.getBestCmap():compiled.add(before.getBestCmap()[cp])
changed_glyphs=[]
for n in before.getGlyphOrder():
 if before['glyf'][n].compile(before['glyf'])!=after['glyf'][n].compile(after['glyf']):changed_glyphs.append(n)
assert set(changed_glyphs)<=compiled,(changed_glyphs,compiled)
texts=['Ă Ĕ Ĭ Ŏ Ŭ ă ĕ ĭ ŏ ŭ Ğ ğ','ă ĕ ĭ ŏ ŭ ğ','Ắ ắ Ğ̈ ğ̈','ắ ĕ̈ ĭ̌ ŏ̦ ŭ̧','ğ g̦ ģ','fine office fi fl','ببب ب ھھھ ھ','שָׁלוֹם עוֹלָם']
for p in [p]+sorted((S/'fonts/ttf').glob('*.ttf')):
 f=TTFont(p);bp=C/'baseline-fonts'/p.relative_to(S/'fonts');bf=TTFont(bp)
 for w in ([400,475,550,625,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
  for text in texts:assert shaped(bf,bp.read_bytes(),text,w)==shaped(f,p.read_bytes(),text,w),(text,w);checks+=1
(C/'verification.json').write_text(json.dumps({'checks':checks,'source_signed_areas':areas,'exact_reverse_twice':True,'unchanged_source_files':len(b['sources'])-2,'changed_vf_tables':changed,'changed_compiled_glyphs':changed_glyphs,'layout_metrics_tables_unchanged':True,'source_patterns_compatible':True},indent=2)+'\n');print(checks,'checks; tables',changed,'glyphs',changed_glyphs)
