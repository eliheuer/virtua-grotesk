from pathlib import Path
import hashlib,json,os,datetime
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());changes=json.loads((C/'changes.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owned={x['path']:x for x in changes}
assert all(sha(R/p) in {h,owned[p]['after']} if p in owned else sha(R/p)==h for p,h in b['sources'].items()),'Source changed: preserve editor save and refresh baseline.'
for item in changes:
 p=R/item['path'];candidate=C/'candidate-sources'/item['path'];assert sha(p) in {item['before'],item['after']} and sha(candidate)==item['after']
for item in changes:
 p=R/item['path'];assert sha(p) in {item['before'],item['after']};tmp=p.with_suffix(p.suffix+'.pending');tmp.write_bytes((C/'candidate-sources'/item['path']).read_bytes());os.replace(tmp,p)
(C/'application.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'changes':changes},indent=2)+'\n')
print('Applied 62 guarded vowel wrapper advances')
