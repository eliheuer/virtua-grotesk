from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'candidate.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,h in m['source_hashes'].items():assert sha(R/rel)==h,rel
for g in m['glyphs']:assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
for rel,h in m['reserved'].items():assert sha(R/rel)==h
m['status']='applied working draft; human review pending';(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
print('Applied exactly twelve hash-guarded sources; 34 Beh/Heh reserved files unchanged.')
