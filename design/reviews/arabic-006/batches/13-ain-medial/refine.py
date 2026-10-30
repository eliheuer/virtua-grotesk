"""Remove the two unintended counter-shoulder reversals on the 8-unit grid."""
from pathlib import Path
import json,hashlib,re,shutil
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((C/'applied.json').read_text())
for p,h in m['reserved_beh_hashes'].items():assert sha(R/p)==h
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
g=next(g for g in m['glyphs'] if g['drawing']);p=R/g['path'];old=p.read_text();(C/'counter-v1.glif').write_text(old)
for suffix in ['json','svg']:
 src=C/('ain-ar.medi-'+('curves' if suffix=='json' else 'comb')+'.'+suffix);shutil.copy2(src,C/('counter-v1.'+suffix))
pts=[(360,192),(352,184),(344,192),(280,288),(264,312),(256,328),(256,336),(256,344),(272,352),(288,352),(416,352),(432,352),(448,344),(448,336),(448,328),(440,312),(424,288)]
i=iter(pts);parts=old.split('<contour>');assert len(parts)==3
parts[2]=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',lambda match:'<point x="%s" y="%s"'%next(i)+match[1],parts[2]);assert next(i,None) is None
new='<contour>'.join(parts);p.write_text(new);(C/'candidate-sources'/g['path']).write_text(new);g['candidate_sha256']=sha(p);(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n')
