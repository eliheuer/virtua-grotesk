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
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:
 assert sha(R/g['path'])==g['candidate_sha256']
 a=E.parse(R/g['path']);b=E.parse(R/g['path'].replace('-Bold','-Regular'));old=E.parse(C/'before-sources'/g['path'])
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for tag in ['anchor','outline/component']:
  if tag=='outline/component' and g['name'] in m['placements']:
   before=old.findall(tag);after=a.findall(tag);assert before[0].attrib==after[0].attrib
   assert after[1].attrib==m['placements'][g['name']]
  else:assert [E.tostring(x) for x in a.findall(tag)]==[E.tostring(x) for x in old.findall(tag)]
# Keep the proof snapshot stable across timestamp-only preflight rebuilds.
a,b=TTFont(C/'assets/after.ttf'),TTFont(R/'fonts/variable/VirtuaGrotesk[wght].ttf')
assert a.keys()==b.keys()
for tag in a.keys():
 if tag not in ['GlyphOrder','head']:assert a.getTableData(tag)==b.getTableData(tag),tag
for key,value in vars(a['head']).items():
 if key not in ['modified','checkSumAdjustment']:assert value==vars(b['head'])[key],key
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths];orders=[f.getGlyphOrder() for f in fonts];assert orders[0]==orders[1]
lib=plistlib.load(open(R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist','rb'));mapping=lib.get('public.postscriptNames',{})
allowed={mapping.get(n,n.replace('-','')) for n in m['inherited_bold_glyphs']+[g['name'] for g in m['glyphs']]}
placement_deltas={}
for g in m['glyphs']:
 if g['name'] not in m['placements']:continue
 old=E.parse(C/'before-sources'/g['path']).findall('outline/component')[1]
 new=m['placements'][g['name']]
 placement_deltas[mapping.get(g['name'],g['name'].replace('-',''))]=[int(new.get(k,'0'))-int(old.get(k,'0')) for k in ['xOffset','yOffset']]
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['ععع ع','غغغ غ','عب عبب','غب غبب','عَ عُ عِ','غَ غُ غِ','علم عمل عمر غيم غار','ححح ح','ججج ج','خخخ خ','چچچ چ','بحب بجب بخب','حَ جُ خِ','حج خرج حجج', '\u200dم\u200d','\u200cم','ممم م','بمب م','مهم تمام مسلم','مَ مُ مِ','للل ل','بلا لا','بأ بلأ','بلإ بلآ','لَ لُ لِ','لل للل','ففف ف','ققق ق','فقف قفق','بفب بقب','ڤڤڤ ڤ','ڨڨڨ ڨ','فَ فُ فِ','قَ قُ قِ','ننن ن','بنب نون نور','ں بں','نَ نُ نِ', 'بو و','ووو و','ؤ ؤؤ بوؤ','نور ورود دور','وَ وُ وِ', 'بد د بر ر','بذ ذ بز ز','بژ ژ بڑ ڑ','دار درب برد ورد','ددد د ررر ر','ببب ب','دَرْب بَدْر','دد در رد رر','أً ؤً ئً','ووو و','ممم م','ههه ه','سلام','العربية']
# Exercise every encoded descendant, including dot-donor consumers outside Feh/Qaf.
for n in m['inherited_bold_glyphs']+[g['name'] for g in m['glyphs']]:
 root=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes())
 for u in E.parse(root/cs[n]).findall('unicode'):
  ch=chr(int(u.get('hex'),16));samples.append(ch*3+' '+ch)
samples=list(dict.fromkeys(samples))
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
   assert old['name']==new['name'] and old['cluster']==new['cluster'],(w,text,old,new)
   if old['offset']!=new['offset']:
    bases=[x for x in a if x['cluster']==old['cluster'] and x['name'] in placement_deltas]
    assert len(bases)==1,(w,text,old,new,bases)
    dxdy=placement_deltas[bases[0]['name']]
    assert all(abs((new['offset'][i]-old['offset'][i])-dxdy[i]*(w-400)/300)<=1 for i in [0,1]),(w,text,old,new,dxdy)
   assert new['name']!='.notdef'
   delta=sets[1][new['name']].width-sets[0][new['name']].width
   assert abs(new['advance']-old['advance']-delta)<=1,(w,text,old,new,delta)
  report['shape_checks'].append(dict(weight=w,text=text,working=b))
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(report['shape_checks']),'shaping comparisons; only declared width and interpolated component-placement deltas. Source edits and compiled changes scoped to family.')
