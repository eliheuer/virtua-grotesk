"""Check exact source scope, compatible masters and compiled Arabic contexts."""
from pathlib import Path
import hashlib,json,shutil,plistlib,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.basePen import BasePen
import numpy as np
class SamplePen(BasePen):
 def __init__(self,gs):super().__init__(gs);self.lines=[];self.last=None;self.start=None
 def _moveTo(self,p):self.last=p;self.start=p
 def _lineTo(self,p):self.lines.append((self.last,p));self.last=p
 def _qCurveToOne(self,p1,p2):
  p0=self.last
  for t in np.linspace(0,1,65)[1:]:self._lineTo(tuple((1-t)**2*a+2*(1-t)*t*b+t*t*c for a,b,c in zip(p0,p1,p2)))
 def _curveToOne(self,p1,p2,p3):
  p0=self.last
  for t in np.linspace(0,1,65)[1:]:self._lineTo(tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3)))
 def _closePath(self):self._lineTo(self.start)
 def _endPath(self):pass
def distance(gs1,gs2,name):
 pens=[SamplePen(gs) for gs in [gs1,gs2]]
 for p,gs in zip(pens,[gs1,gs2]):gs[name].draw(p)
 def directed(a,b):
  lines=np.array(b.lines);u=lines[:,0];v=lines[:,1]-u;den=(v*v).sum(axis=1);den=np.maximum(den,1e-15);worst=0
  for point in np.array(a.lines).reshape(-1,2):
   t=np.clip(((point-u)*v).sum(axis=1)/den,0,1);worst=max(worst,float(np.sqrt(((u+t[:,None]*v-point)**2).sum(axis=1)).min()))
  return worst
 return max(directed(*pens),directed(*pens[::-1]))
R=Path(__file__).resolve().parents[4];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text());targets={g['path'] for g in m['glyphs']}
assert {p for p,h in m['source_hashes'].items() if sha(R/p)!=h}==targets
for g in m['glyphs']:
 assert sha(R/g['path'])==g['candidate_sha256']
 a=E.parse(R/g['path']);b=E.parse(R/g['path'].replace('-Bold','-Regular'))
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 old=E.parse(C/'before-sources'/g['path'])
 assert [E.tostring(x) for x in a.findall('anchor')]==[E.tostring(x) for x in old.findall('anchor')]
shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/after.ttf')
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths];orders=[f.getGlyphOrder() for f in fonts];assert orders[0]==orders[1]
lib=plistlib.load(open(R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist','rb'));mapping=lib.get('public.postscriptNames',{})
allowed={mapping.get(n,n.replace('-','')) for n in m['dependency_closure']}
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['ننن ن','ز ز','ذ ذ','غغغ غ','ففف ف','ببب ب','ب ب ب','بب','باب','بطل','كتاب','سبب','تتت ت','ثثث ث','ننن ن','ييي ي','پپپ پ','ههه ه','للل ل','ممم م','أً ؤً ئً']
report={'source_changes':sorted(targets),'font_hashes':dict(zip(['before','working'],map(sha,paths))),'compiled_changes':{},'shape_checks':[]}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [dict(name=orders[0][i.codepoint],cluster=i.cluster,advance=p.x_advance,offset=[p.x_offset,p.y_offset]) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[];widths=[]
 for name in sets[0]:
  vals=[]
  for gs in sets:
   p=DecomposingRecordingPen(gs);gs[name].draw(p);vals.append((p.value,gs[name].width))
  if vals[0]!=vals[1]:diff.append(name)
  if vals[0][1]!=vals[1][1]:widths.append(name)
 assert set(diff)<=allowed,sorted(set(diff)-allowed)
 if w==400:
  deviations={mapping.get(g['name'],g['name'].replace('-','')):distance(*sets,mapping.get(g['name'],g['name'].replace('-',''))) for g in m['glyphs']}
  assert max(deviations.values())<1.5,deviations
  report['regular_quadratic_approximation_deviation']=deviations
  assert not widths,widths
 assert not widths,widths
 report['compiled_changes'][str(w)]={'outlines_or_widths':diff,'widths':widths}
 for f in hfonts:f.set_variations({'wght':w})
 for text in samples:
  a,b=[shape(f,text) for f in hfonts];assert a==b,(w,text,a,b)
  assert all(x['name']!='.notdef' for x in b)
  if text=='ببب ب':assert len({x['name'] for x in b if x['name']!='space'})==4,b
  report['shape_checks'].append(dict(weight=w,text=text,working=b))
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(report['shape_checks']),'shaping comparisons; advances and placements unchanged; changes confined to single-dot dependency closure.')
