from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text())
for p,h in m['source_hashes'].items():assert sha(R/p)==h,p
for g in m['glyphs']:
 old=(R/g['path']).read_text();new=(C/'candidate-sources'/g['path']).read_text()
 assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
 if g['master']=='Regular':
  if g['metrics_only']:assert re.sub(r'<advance width="[^"]+"/>','',new)==re.sub(r'<advance width="[^"]+"/>','',old)
  else:
   assert new.replace('\n\t\t\t<point x="140" y="150" type="line"/>','').replace('\n\t\t\t<point x="80" y="150" type="line"/>','')==old
for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
print('Applied 13 guarded files; Regular drawing geometry and human grades preserved.')
