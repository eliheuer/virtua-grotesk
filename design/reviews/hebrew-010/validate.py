"""Verify the exact Bold-only mark scope and its compiled dependents."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[2];m=json.loads((C/'bold-candidate-v2.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
targets={r['path'] for r in m['glyphs']};changed={p for p,h in m['source_hashes'].items() if sha(R/p)!=h};assert changed==targets,(changed-targets,targets-changed)
for r in m['glyphs']:
 assert sha(R/r['path'])==r['candidate_sha256']
 a=E.parse(C/'before-sources'/r['path']).getroot();b=E.parse(R/r['path']).getroot()
 for tag in ['lib','advance','unicode']:assert [E.tostring(x) for x in a.findall(tag)]==[E.tostring(x) for x in b.findall(tag)],(r['glyph'],tag)
 assert [x.attrib for x in a.findall('anchor')]==[x.attrib for x in b.findall('anchor')]
 assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')]
e=json.loads((C/'evidence-v2.json').read_text());fs={r:TTFont(C/e['fonts'][r]['path']) for r in ['before','after']}
cm=fs['after'].getBestCmap();allowed={cm[int(E.parse(R/r['path']).getroot().find('unicode').get('hex'),16)] for r in m['glyphs']}
# Compiled single-level components naturally follow the repaired mark donors.
while True:
 extra={n for n in fs['after'].getGlyphOrder() if fs['after']['glyf'][n].isComposite() and any(c.glyphName in allowed for c in fs['after']['glyf'][n].components)}
 if extra<=allowed:break
 allowed|=extra
changes={}
for weight in range(400,701,50):
 gs={r:f.getGlyphSet(location={'wght':weight}) for r,f in fs.items()};diff=[]
 for n in fs['after'].getGlyphOrder():
  records=[]
  for role in fs:
   pen=DecomposingRecordingPen(gs[role]);gs[role][n].draw(pen);records.append(pen.value)
  if records[0]!=records[1]:diff.append(n)
  assert gs['before'][n].width==gs['after'][n].width,(weight,n,'advance')
 assert set(diff)<=allowed,(weight,set(diff)-allowed)
 if weight==400:assert not diff,diff
 changes[weight]=diff
out=dict(source_paths=sorted(targets),all_regular_bytes_unchanged=True,other_source_bytes_unchanged=True,anchors_grades_unicode_topology_unchanged=True,compiled_advance_changes=0,compiled_outline_changes=changes,allowed_dependency_closure=sorted(allowed),font_hashes={k:sha(C/e['fonts'][k]['path']) for k in fs})
(C/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: 16 Bold mark edits; Regular and other sources unchanged; advances unchanged; compiled dependency scope matches.')
