"""Verify source scope, protected masters, compiled closure and Arabic shaping."""
from pathlib import Path
import hashlib,json,shutil,plistlib,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text());targets={g['path'] for g in m['glyphs']}
assert {p for p,h in m['source_hashes'].items() if sha(R/p)!=h}==targets
for g in m['glyphs']:
 assert sha(R/g['path'])==g['candidate_sha256']
 a=E.parse(R/g['path']);b=E.parse(R/g['path'].replace('-Bold','-Regular'));old=E.parse(C/'before-sources'/g['path'])
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for tag in ['anchor','outline/component']:
  if tag=='outline/component' and g['name'] not in ('fehDotless-ar.init','fehDotless-ar.medi') and 'below' not in g['name']:
   before=old.findall(tag);after=a.findall(tag);assert before[0].attrib==after[0].attrib
   expected=dict(before[1].attrib);dx,dy=(32,64) if g['name'].endswith('.init') else (-32,104)
   expected['xOffset']=str(int(expected.get('xOffset','0'))+dx);expected['yOffset']=str(int(expected.get('yOffset','0'))+dy)
   assert after[1].attrib==expected
  else:assert [E.tostring(x) for x in a.findall(tag)]==[E.tostring(x) for x in old.findall(tag)]
shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/after.ttf')
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths];orders=[f.getGlyphOrder() for f in fonts];assert orders[0]==orders[1]
lib=plistlib.load(open(R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist','rb'));mapping=lib.get('public.postscriptNames',{})
allowed={mapping.get(n,n.replace('-','')) for n in m['inherited_bold_glyphs']+[g['name'] for g in m['glyphs']]}
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['ففف ف','ققق ق','فقف قفق','بفب بقب','ڤڤڤ ڤ','ڨڨڨ ڨ','فَ فُ فِ','قَ قُ قِ','ننن ن','بنب نون نور','ں بں','نَ نُ نِ', 'بو و','ووو و','ؤ ؤؤ بوؤ','نور ورود دور','وَ وُ وِ', 'بد د بر ر','بذ ذ بز ز','بژ ژ بڑ ڑ','دار درب برد ورد','ددد د ررر ر','ببب ب','دَرْب بَدْر','دد در رد رر','أً ؤً ئً','ووو و','ممم م','ههه ه','سلام','العربية']
report={'source_changes':sorted(targets),'regular_sources_unchanged':True,'manual_hamza_unchanged':True,'font_hashes':dict(zip(['before','working'],map(sha,paths))),'compiled_changes':{},'shape_checks':[]}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [dict(name=orders[0][i.codepoint],cluster=i.cluster,advance=p.x_advance,offset=[p.x_offset,p.y_offset]) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[];widths={}
 for name in sets[0]:
  vals=[]
  for gs in sets:
   p=DecomposingRecordingPen(gs);gs[name].draw(p);vals.append((p.value,gs[name].width))
  if vals[0]!=vals[1]:diff.append(name)
  if vals[0][1]!=vals[1][1]:widths[name]=[vals[0][1],vals[1][1]]
 assert set(diff)<=allowed,sorted(set(diff)-allowed)
 if w==400:assert not widths
 report['compiled_changes'][str(w)]={'outlines_or_widths':diff,'widths':widths}
 for f in hfonts:f.set_variations({'wght':w})
 for text in samples:
  a,b=[shape(f,text) for f in hfonts]
  assert len(a)==len(b)
  for old,new in zip(a,b):
   assert old['name']==new['name'] and old['cluster']==new['cluster'] and old['offset']==new['offset'],(w,text,old,new)
   assert new['name']!='.notdef'
   delta=sets[1][new['name']].width-sets[0][new['name']].width
   assert abs(new['advance']-old['advance']-delta)<=1,(w,text,old,new,delta)
  report['shape_checks'].append(dict(weight=w,text=text,working=b))
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(report['shape_checks']),'shaping comparisons; only declared width deltas. Source edits and compiled changes scoped to family.')
