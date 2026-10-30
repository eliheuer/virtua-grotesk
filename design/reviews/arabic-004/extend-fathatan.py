"""Preserve the helper-only trial and extend scope to its encoded Fathatan pair."""
from pathlib import Path
import hashlib,json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'candidate.json').read_text());assert len(m['glyphs'])==2
expected=dict(m['source_hashes']);expected.update({g['path']:g['candidate_sha256'] for g in m['glyphs']})
assert all(sha(R/p)==h for p,h in expected.items()),'Concurrent source change'
for master,offsets,bottom,top in [('Regular',[112,0],704,1000),('Bold',[176,0],664,1104)]:
 rel=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/fathatan-ar.glif');p=R/rel;before=p.read_text()
 assert 'green' not in before and '0.09,0.72,0.44,1' not in before
 it=iter(offsets)
 after=re.sub(r'(<component base="fatha-ar" yOffset=")[^"]+("/>)',lambda x:x[1]+str(next(it))+x[2],before)
 for name,y in [('bottom',bottom),('top',top)]:
  after=re.sub(rf'(<anchor name="{name}" x="112" y=")[^"]+("/>)',lambda x:x[1]+str(y)+x[2],after)
 for state,text in [('before-sources',before),('candidate-sources',after)]:
  q=C/state/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 m['glyphs'].append(dict(master=master,name='fathatan-ar',path=str(rel),before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel),offsets=offsets,anchors={'bottom':bottom,'top':top}))
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
for g in m['glyphs']:
 src=C/'candidate-sources'/g['path'];assert sha(src)==g['candidate_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied Fathatan and hamza/Fathatan placements in both masters; all donor outlines preserved')
