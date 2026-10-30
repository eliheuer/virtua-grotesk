"""Apply only the verified Latin candidate, refusing editor-save conflicts."""
from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[2];m=json.loads((C/'baseline.json').read_text());changes=json.loads((C/'changes.json').read_text());v=json.loads((C/'verification.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(C/'assets/after.ttf')==v['after_sha256']
for path,h in m['sources'].items():assert sha(R/path)==h,f'Source changed; preserve and refresh: {path}'
for item in changes:
 p=R/item['path'];q=C/'candidate-sources'/item['path'];assert sha(q)==item['after']
 assert (sha(p) if p.exists() else None)==item['before'],str(p)
for item in changes:
 p=R/item['path'];assert (sha(p) if p.exists() else None)==item['before'],str(p)
 p.write_bytes((C/'candidate-sources'/item['path']).read_bytes())
paths={x['path'] for x in changes}
assert all(sha(R/path)==h for path,h in m['sources'].items() if path not in paths)
(C/'application.json').write_text(json.dumps({'status':'applied','files':changes,'unchanged_existing_files':len(m['sources'])-sum(x['before'] is not None for x in changes),'review':'Applied working correction; no human visual approval implied'},indent=2)+'\n')
print('Applied',len(changes),'files; all other source bytes preserved')
