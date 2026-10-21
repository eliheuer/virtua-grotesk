"""Check detached v3 scope, compatible source structure and compiled dependents."""
from pathlib import Path
import json,hashlib,argparse,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[2];m=json.loads((C/'chamfer-v3.json').read_text());e=json.loads((C/'evidence-chamfer-v3.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--applied',action='store_true');args=parser.parse_args()
expected=dict(m['source_hashes'])
if args.applied:
 expected=dict(json.loads((C/'chamfer-v3-applied.json').read_text())['source_hashes_before'])
 expected.update({r['path']:r['candidate_sha256'] for r in m['glyphs']})
for rel,h in expected.items():assert sha(R/rel)==h,rel
for row in m['glyphs']:
 p=C/'candidate-chamfer-v3'/row['path'];assert sha(p)==row['candidate_sha256']
 a=E.parse(C/'before-chamfer-v3'/row['path']).getroot();b=E.parse(p).getroot()
 for tag in ['anchor','advance','unicode','lib']:assert [E.tostring(x) for x in a.findall(tag)]==[E.tostring(x) for x in b.findall(tag)]
 for pt in b.findall('outline/contour/point'):assert int(pt.get('x'))%8==int(pt.get('y'))%8==0
for name in {r['glyph'] for r in m['glyphs']}:
 roots=[E.parse(C/f'candidate-chamfer-v3/sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif') for master in ['Regular','Bold']]
 assert [[p.get('type') for p in c] for c in roots[0].findall('outline/contour')]==[[p.get('type') for p in c] for c in roots[1].findall('outline/contour')]
fs={r:TTFont(C/e['fonts'][r]['path']) for r in ['before','after']};cm=fs['after'].getBestCmap();allowed={cm[int(E.parse(R/r['path']).find('unicode').get('hex'),16)] for r in m['glyphs']}
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
 changes[weight]=diff
out=dict(active_sources_match_applied_candidate=args.applied,active_sources_unchanged=not args.applied,metadata_unchanged=True,compatible=True,new_points_on_8=True,compiled_advance_changes=0,compiled_outline_changes=changes,font_hashes={k:sha(C/e['fonts'][k]['path']) for k in fs})
(C/('chamfer-applied-validation.json' if args.applied else 'chamfer-validation.json')).write_text(json.dumps(out,indent=2)+'\n');print('PASS: source hashes match expected state, compatible pair, compiled changes confined to marks and dependents.')
