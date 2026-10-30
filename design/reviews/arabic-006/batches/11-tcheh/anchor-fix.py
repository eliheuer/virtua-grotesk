"""Keep below-dot component anchors from overriding the letter's top attachment."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((C/'applied.json').read_text())
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
for g in m['glyphs']:
 if g['name'] in ['tcheh-ar.init','threedotsdowncenter-ar']:continue
 p=R/g['path'];t=p.read_text();src=E.fromstring(t);base=src.find('outline/component').get('base');rr=p.parent;cs=plistlib.loads((rr/'contents.plist').read_bytes());anchor=next(a.attrib for a in E.parse(rr/cs[base]).findall('anchor') if a.get('name')=='top')
 assert not src.findall('anchor');s='<anchor '+' '.join(f'{k}="{v}"' for k,v in anchor.items())+'/>';t=t.replace('\t<lib>','\t'+s+'\n\t<lib>');p.write_text(t);(C/'candidate-sources'/g['path']).write_text(t);g['candidate_sha256']=sha(p);g['added_top_anchor']=anchor
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
