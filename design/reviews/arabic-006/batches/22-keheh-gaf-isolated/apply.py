from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((C/'applied.json').read_text())
for p,h in m['source_hashes'].items():assert sha(R/p)==h,p
for g in m['glyphs']:assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
print('Applied six guarded isolated-family files; Beh and protected sources unchanged.')
