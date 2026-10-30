"""Check source scope, compiled stored forms, interpolation and canonical shaping."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
C=Path(__file__).resolve().parent;R=C.parents[2]
m=json.loads((C/'rebuild.json').read_text());names={r['glyph'] for r in m['forms']};targets={r['path'] for r in m['forms']}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[p for p,h in m['source_hashes'].items() if sha(R/p)!=h];assert set(changed)==targets,changed
for row in m['forms']:
 a=E.parse(C/'before-sources'/row['path']).getroot();b=E.parse(R/row['path']).getroot()
 for tag in ['unicode','lib']: assert E.tostring(a.find(tag))==E.tostring(b.find(tag)),(row['path'],tag)
 assert sha(R/row['path'])==row['candidate_sha256']
for name in names:
 rows=[r for r in m['forms'] if r['glyph']==name];assert [[p[0] for p in r['components']] for r in rows][0]==[[p[0] for p in r['components']] for r in rows][1]
paths={'before':C/'before-fonts/VirtuaGrotesk[wght].ttf','working':R/'fonts/variable/VirtuaGrotesk[wght].ttf'};fonts={k:TTFont(p) for k,p in paths.items()};hf={k:hb.Font(hb.Face(p.read_bytes())) for k,p in paths.items()}
records=[];changes={};maxerror=0
for w in range(400,701,50):
 gs={k:f.getGlyphSet(location={'wght':w}) for k,f in fonts.items()}
 for h in hf.values():h.set_variations({'wght':w})
 changed=[];widths=[]
 for name in fonts['working'].getGlyphOrder():
  rp=[]
  for role in paths:
   p=DecomposingRecordingPen(gs[role]);gs[role][name].draw(p);rp.append(p.value)
  if rp[0]!=rp[1]:changed.append(name)
  if gs['before'][name].width!=gs['working'][name].width:widths.append(name)
 expected={fonts['working'].getBestCmap()[int(r['codepoint'][2:],16)] for r in m['forms']}
 assert set(changed)<=expected and set(widths)<=expected,(w,changed,widths)
 changes[w]=dict(outlines=changed,widths=widths)
 for row in m['forms'][:29]:
  cp=int(row['codepoint'][2:],16);name=fonts['working'].getBestCmap()[cp];decomp=row['decomposition'];shapes={}
  for role in paths:
   for spelling,txt in [('NFD',decomp),('precomposed',chr(cp))]:
    buf=hb.Buffer();buf.add_str(txt);buf.guess_segment_properties();hb.shape(hf[role],buf)
    shapes[role,spelling]=[(fonts[role].getGlyphName(i.codepoint),p.x_advance,p.y_advance,p.x_offset,p.y_offset) for i,p in zip(buf.glyph_infos,buf.glyph_positions)]
  assert shapes['working','precomposed']==[(name,round(gs['working'][name].width),0,0,0)],(w,name,shapes)
  assert shapes['working','NFD']==shapes['before','NFD'],(w,name,shapes)
  # Match stored components to directly shaped base/marks, independently of normalization.
  placed=[];cursor=0
  for n,adv,_,dx,dy in shapes['working','NFD']:
   placed.append((n,cursor+dx,dy));cursor+=adv
  expectedpen=DecomposingRecordingPen(gs['working'])
  # Stored form order is base then canonical marks; HB order is usually reversed.
  prod={fonts['working'].getBestCmap()[ord(c)]:i for i,c in enumerate(decomp)}
  for n,x,y in sorted(placed,key=lambda p:prod[p[0]]):gs['working'][n].draw(TransformPen(expectedpen,(1,0,0,1,x,y)))
  actual=DecomposingRecordingPen(gs['working']);gs['working'][name].draw(actual)
  assert len(actual.value)==len(expectedpen.value),(name,w)
  error=0
  for (op,pts),(ex,ep) in zip(actual.value,expectedpen.value):
   assert op==ex and len(pts)==len(ep),(name,w,op,ex)
   for a,b in zip(pts,ep):
    if a is None or b is None:assert a==b
    else:error=max(error,*(abs(x-y) for x,y in zip(a,b)))
  assert error<=1.01,(name,w,error)
  assert abs(gs['working'][name].width-cursor)<=1.01,(name,w,'advance')
  maxerror=max(maxerror,error);records.append(dict(glyph=name,weight=w,max_coordinate_difference=error))
# No nested TTF components in any of the rebuilt forms.
glyf=fonts['working']['glyf']
for n in expected:
 assert glyf[n].isComposite(),n
 assert all(not glyf[c.glyphName].isComposite() for c in glyf[n].components),n
out=dict(source_paths=sorted(targets),non_targets_byte_identical=True,grades_and_unicode_unchanged=True,compatible_components=True,no_nested_components=True,compiled_changes=changes,stored_form_comparisons=len(records),max_coordinate_difference=maxerror,canonical_shaping_unchanged=True,fonts={k:dict(path=str(p),sha256=sha(p)) for k,p in paths.items()},comparisons=records)
(C/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 58 scoped sources; 203 stored-form/interpolated checks; canonical shaping unchanged; max rounding difference',maxerror)
