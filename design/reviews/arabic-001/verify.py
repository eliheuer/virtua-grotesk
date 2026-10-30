"""Focused source, interpolation and compiled Arabic shaping evidence."""
from pathlib import Path
import hashlib,json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont
root=Path(__file__).resolve().parents[3];case=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((case/'applied.json').read_text())
changed=[p for p,h in manifest['source_hashes'].items() if sha(root/p)!=h]
assert set(changed)=={'sources/VirtuaGrotesk-Bold.ufo/glyphs/alef-ar.glif','sources/VirtuaGrotesk-Bold.ufo/glyphs/alef-ar.fina.glif'},changed
samples=['ا','ـا','با','اب','باب','بابا','كتاب','بَاب','اَ','اِ','اُ','اْ','أ','إ','آ','ٱ','سلام']
results=[];outline_changes={}
fonts={r:case/'assets'/f'{r}.ttf' for r in ['before','after','rubik','noto']}
def shape(p,text,w):
 f=hb.Font(hb.Face(p.read_bytes()));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 order=TTFont(p).getGlyphOrder()
 return [{'name':order[i.codepoint],'cluster':i.cluster,'advance':p.x_advance,'offset':[p.x_offset,p.y_offset]} for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,550,700]:
 for text in samples:
  shaped={r:shape(p,text,w) for r,p in fonts.items()}
  assert all(g['name']!='.notdef' for run in shaped.values() for g in run),(w,text)
  assert [(g['name'],g['cluster']) for g in shaped['before']]==[(g['name'],g['cluster']) for g in shaped['after']],(w,text)
  results.append({'weight':w,'text':text,'fonts':shaped})
 pairs=[instantiateVariableFont(TTFont(fonts[r]),{'wght':w},inplace=False).getGlyphSet() for r in ['before','after']]
 changed_outlines=[]
 for n in pairs[0].keys():
  ps=[]
  for gs in pairs:
   pen=DecomposingRecordingPen(gs);gs[n].draw(pen);ps.append((pen.value,gs[n].width))
  if ps[0]!=ps[1]:changed_outlines.append(n)
 outline_changes[str(w)]=changed_outlines
 allowed={'uni0627','uni0627.fina','uni0623','uni0623.fina','uni0625','uni0625.fina','uni0622','uni0622.fina','uni0671','uni0671.fina','uni06440627.fina','uni06440623.fina','uni06440625.fina','uni06440622.fina','uni06440671.fina'}
 assert set(changed_outlines)<=allowed
 if w==400:
  for n in changed_outlines:
   bounds=[]
   for gs in pairs:
    pen=BoundsPen(gs);gs[n].draw(pen);bounds.append((pen.bounds,gs[n].width))
   assert bounds[0]==bounds[1],(n,bounds)
report={'changed_source_files':changed,'compiled_outline_or_width_changes':outline_changes,'shaping':results,'limitations':['Regular GLIF bytes, compiled bounds and advances are unchanged. Joint cubic-to-quadratic conversion changes the Regular final-Alef approximation and its dependent composites; compiled outlines are not byte-identical.','Derived Alef composites retain old component placements and advances; their inherited changes need a separate repair loop. No release approval.']}
(case/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_files_changed':len(changed),'shaping_runs':len(results)*4,'outline_changes':outline_changes},indent=2))
