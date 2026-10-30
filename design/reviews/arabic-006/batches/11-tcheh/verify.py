"""Verify exclusive scope, master structures, compiled closure and shaping."""
from pathlib import Path
import json,hashlib,plistlib,shutil,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text());targets={g['path'] for g in m['glyphs']}
assert {p for p,h in m['source_hashes'].items() if sha(R/p)!=h}==targets
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:
 assert sha(R/g['path'])==g['candidate_sha256']
 a=E.parse(R/g['path']);b=E.parse(C/'before-sources'/g['path']);assert [x.attrib for x in a.findall('anchor')]==([g['added_top_anchor']] if 'added_top_anchor' in g else [x.attrib for x in b.findall('anchor')])
for n in set(g['name'] for g in m['glyphs']):
 a,b=[E.parse(R/g['path']) for g in m['glyphs'] if g['name']==n]
 assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 assert [x.get('base') for x in a.findall('.//component')]==[x.get('base') for x in b.findall('.//component')]
# Preserve the raster-bound snapshot across timestamp-only preflight rebuilds.
proof_font=TTFont(C/'assets/after.ttf');built_font=TTFont(R/'fonts/variable/VirtuaGrotesk[wght].ttf')
assert proof_font.keys()==built_font.keys()
for tag in proof_font.keys():
 if tag not in ['GlyphOrder','head']:assert proof_font.getTableData(tag)==built_font.getTableData(tag),tag
for key,value in vars(proof_font['head']).items():
 if key not in ['modified','checkSumAdjustment']:assert value==vars(built_font['head'])[key],key
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];order=TTFont(paths[0]).getGlyphOrder();assert TTFont(paths[1]).getGlyphOrder()==order
mapping=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes()).get('public.postscriptNames',{});allowed={mapping.get(g['name'],g['name'].replace('-','')) for g in m['glyphs']}
samples=list(dict.fromkeys([r['text'] for r in json.loads((C.parent/'10-hah-family/verification.json').read_text())['shape_checks']]+['چچچ چ','بچب چ','چَ چُ چِ','چچ چچچ','حج چرخ خرج']))
hfonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths];out={'source_changes':sorted(targets),'reserved_beh_hashes':m['reserved_beh_hashes'],'font_hashes':dict(zip(['before','after'],map(sha,paths))),'compiled_changes':{},'shape_checks':[]}
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b);return [dict(name=order[i.codepoint],cluster=i.cluster,advance=p.x_advance,offset=[p.x_offset,p.y_offset]) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];changes=[];widths={}
 for n in sets[0]:
  vals=[]
  for gs in sets:
   p=DecomposingRecordingPen(gs);gs[n].draw(p);vals.append((p.value,gs[n].width))
  if vals[0]!=vals[1]:changes.append(n)
  if vals[0][1]!=vals[1][1]:widths[n]=[vals[0][1],vals[1][1]]
 assert set(changes)<=allowed,set(changes)-allowed;out['compiled_changes'][str(w)]=dict(glyphs=changes,widths=widths)
 for f in hfonts:f.set_variations({'wght':w})
 for t in samples:
  a,b=[shape(f,t) for f in hfonts];assert len(a)==len(b)
  for old,new in zip(a,b):
   assert old['name']==new['name'] and old['cluster']==new['cluster'] and new['name']!='.notdef'
   if old['offset']!=new['offset']:
    assert new['advance']==0 and any(v['name'] in allowed and v['cluster']==new['cluster'] for v in b),(w,t,old,new)
    out.setdefault('tcheh_mark_offset_changes',[]).append(dict(weight=w,text=t,before=old,after=new))
   delta=sets[1][new['name']].width-sets[0][new['name']].width
   assert abs(new['advance']-old['advance']-delta)<=1,(w,t,old,new)
  out['shape_checks'].append(dict(weight=w,text=t,working=b))
(C/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Passed',len(out['shape_checks']),'shaping comparisons; compiled changes exclusive to Tcheh and its dot donor.')
