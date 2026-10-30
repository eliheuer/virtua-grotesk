from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((C/'applied.json').read_text())
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
g=next(g for g in m['glyphs'] if g['master']=='Bold' and g['name']=='tcheh-ar.fina');p=R/g['path'];t=p.read_text();assert 'xOffset="192" yOffset="-328"' in t;t=t.replace('xOffset="192" yOffset="-328"','xOffset="168" yOffset="-352"');p.write_text(t);(C/'candidate-sources'/g['path']).write_text(t);g['candidate_sha256']=sha(p);(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
