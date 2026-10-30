"""Read-only compiled scope and Hebrew mark-overlap evidence, not visual approval."""
import hashlib,json,unicodedata,xml.etree.ElementTree as E
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
import pathops,uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[2]
paths={'before':C/'before.ttf','working':R/'fonts/variable/VirtuaGrotesk[wght].ttf'}
fonts={k:TTFont(p) for k,p in paths.items()};hf={k:hb.Font(hb.Face(p.read_bytes())) for k,p in paths.items()}
changes={};collisions=[];samples=0;scope=[]
for weight in range(400,701,50):
 sets={k:f.getGlyphSet(location={'wght':weight}) for k,f in fonts.items()}
 names=fonts['working'].getGlyphOrder();diff=[];widths=[]
 for name in names:
  records=[]
  for k in paths:
   pen=DecomposingRecordingPen(sets[k]);sets[k][name].draw(pen);records.append(pen.value)
  if records[0]!=records[1]:diff.append(name)
  if sets['before'][name].width!=sets['working'][name].width:widths.append(name)
 changes[weight]={'outlines':diff,'widths':widths}
 for role,h in hf.items():
  h.set_variations({'wght':weight})
  for base in map(chr,range(0x5d0,0x5eb)):
   for mark in '\u05b0\u05b1\u05b2\u05b3\u05b4\u05b5\u05b6\u05b7\u05b8\u05b9\u05ba\u05bb\u05bc\u05bd\u05bf\u05c1\u05c2\u05c7':
    if mark in '\u05c1\u05c2' and base!='ש':continue
    buf=hb.Buffer();buf.add_str(base+mark);buf.guess_segment_properties();hb.shape(h,buf);ps=[];cursor=0;glyphnames=[]
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
     name=fonts[role].getGlyphName(info.codepoint);glyphnames.append(name);p=pathops.Path();pen=TransformPen(p.getPen(),(1,0,0,1,cursor+pos.x_offset,pos.y_offset));sets[role][name].draw(pen);ps.append(p);cursor+=pos.x_advance
    if len(ps)==2:
     area=abs(pathops.op(ps[0],ps[1],pathops.PathOp.INTERSECTION).area)
     if area>.01:collisions.append(dict(role=role,weight=weight,text=base+mark,area=round(area,2),glyphs=glyphnames))
    samples+=1
for p in (C/'before-sources').rglob('*.glif'):
 rel=p.relative_to(C/'before-sources');before=E.parse(p).getroot();after=E.parse(R/rel).getroot()
 assert E.tostring(before.find('lib'))==E.tostring(after.find('lib')),rel
 assert E.tostring(before.find('unicode'))==E.tostring(after.find('unicode')),rel
 scope.append(str(rel))
result=dict(fonts={k:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in paths.items()},source_scope=scope,colors_and_unicode_preserved=True,compiled_changes=changes,mark_pairs=samples,collisions=collisions)
(C/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Compiled changed glyphs:',changes[400]);print('Mark pairs:',samples)
from collections import Counter
print('Working overlap cases by base:',Counter(r['text'][0] for r in collisions if r['role']=='working'))
print('Previous overlap cases by base:',Counter(r['text'][0] for r in collisions if r['role']=='before'))
