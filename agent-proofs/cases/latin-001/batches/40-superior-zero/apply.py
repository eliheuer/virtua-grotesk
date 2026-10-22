from pathlib import Path
import hashlib,json,os,datetime
C=Path(__file__).resolve().parent;R=C.parents[4];b=json.loads((C/'baseline.json').read_text());changes=json.loads((C/'changes.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();owned={x['path']:x for x in changes}
assert all(sha(R/p) in {h,owned[p]['after']} if p in owned else sha(R/p)==h for p,h in b['sources'].items()),'Preserve editor save and refresh baseline.'
for x in changes:
 p=R/x['path'];assert (sha(p) if p.exists() else None) in {x['before'],x['after']};assert sha(C/'candidate-sources'/x['path'])==x['after']
for x in changes:
 p=R/x['path'];assert (sha(p) if p.exists() else None) in {x['before'],x['after']};tmp=p.with_suffix(p.suffix+'.pending');tmp.write_bytes((C/'candidate-sources'/x['path']).read_bytes());os.replace(tmp,p)
(C/'application.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'changes':changes},indent=2)+'\n')
print('Applied guarded superior-digit drawings and registrations; all previous GLIFs unchanged')
