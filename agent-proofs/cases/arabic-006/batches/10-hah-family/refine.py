"""Local crest refinement, guarded against editor saves; retain first candidate."""
from pathlib import Path
import json,hashlib,re
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text())
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
for g in m['glyphs']:
 if not g['drawing']:continue
 p=R/g['path'];t=p.read_text();v=C/'rejected-v1'/p.name;v.parent.mkdir(exist_ok=True);v.write_text(t)
 t=t.replace('<point x="208" y="336"/>','<point x="240" y="336"/>').replace('<point x="240" y="336" type="curve" smooth="yes"/>','<point x="288" y="336" type="curve" smooth="yes"/>').replace('<point x="352" y="336"/>','<point x="360" y="336"/>')
 # Eight-unit branch cut is a deliberate corner, not a smooth node.
 t=t.replace('<point x="496" y="176" type="line" smooth="yes"/>','<point x="496" y="176" type="line"/>')
 p.write_text(t);(C/'candidate-sources'/g['path']).write_text(t);g['candidate_sha256']=sha(p)
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
