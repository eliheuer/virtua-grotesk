"""Verify this composite-only loop against its exact preceding working font."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text());changed=[p for p,h in m['source_hashes'].items() if sha(R/p)!=h]
assert set(changed)=={g['path'] for g in m['glyphs']}
for g in m['glyphs']:
 assert sha(R/g['path'])==g['candidate_sha256']
 node=ET.parse(R/g['path']).getroot();width=int(node.find('advance').get('width'));offset=int(node.findall('outline/component')[1].get('xOffset'));assert width%8==offset%8==0
before=C/'assets/before.ttf';after=C/'assets/after.ttf'
samples=['أ','ـأ','بأ','أب','بأب','تأ','فأ','أَ','أُ','أِ','أْ','بَأْس','أَب','رَأْس','لأ','بلأ','أ','بأ']
def shape(path,w,text):
 t=TTFont(path);order=t.getGlyphOrder();f=hb.Font(hb.Face(path.read_bytes()));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [{'name':order[i.codepoint],'cluster':i.cluster,'advance':p.x_advance,'offset':[p.x_offset,p.y_offset]} for i,p in zip(b.glyph_infos,b.glyph_positions)]
report={'source_changes':changed,'font_hashes':{'before':sha(before),'working':sha(after)},'checks':[],'compiled_changes':{}}
for w in [400,450,500,550,600,650,700]:
 gs=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in [before,after]]
 outlines=[]
 for n in gs[0]:
  values=[]
  for font in gs:
   p=DecomposingRecordingPen(font);font[n].draw(p);values.append((p.value,font[n].width))
  if values[0]!=values[1]:outlines.append(n)
 assert set(outlines)<={'uni0623','uni0623.fina','uni06440623.fina'},outlines
 if w==400:assert not outlines
 report['compiled_changes'][str(w)]=outlines
 for text in samples:
  a,b=shape(before,w,text),shape(after,w,text)
  assert all(x['name']!='.notdef' for x in a+b)
  assert [(x['name'],x['cluster']) for x in a]==[(x['name'],x['cluster']) for x in b]
  if w==400:assert a==b
  report['checks'].append({'weight':w,'text':text,'before':a,'working':b})
 if w==700:
  assert shape(after,w,'أ')[0]['advance']==296
  assert shape(after,w,'بأ')[0]['advance']==336
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed:',len(report['checks']),'before/working contexts; all Regular compiled outlines/advances unchanged; source scope exact.')
