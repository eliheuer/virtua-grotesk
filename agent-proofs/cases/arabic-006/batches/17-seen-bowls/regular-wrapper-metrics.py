"""Close inherited final-wrapper gaps without changing Regular drawings or grades."""
from pathlib import Path
import hashlib,json,plistlib,re,xml.etree.ElementTree as E
R=Path.cwd();C=Path(__file__).resolve().parent;m=json.loads((C/'applied.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=Path('sources/VirtuaGrotesk-Regular.ufo/glyphs');cs=plistlib.loads((r/'contents.plist').read_bytes())
for name in ['sheen-ar.fina','seenSixdots-ar.fina']:
 p=r/cs[name];old=p.read_text();assert sha(p)==m['source_hashes'][str(p)];assert str(p) not in m['reserved_beh_hashes']
 assert '<string>orange</string>' in old
 assert E.parse(r/cs['seen-ar.fina']).find('advance').get('width')=='1348'
 new=old.replace('<advance width="1632"/>','<advance width="1348"/>');assert new!=old
 dst=C/'candidate-sources'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=name,path=str(p),master='Regular',drawing=False,metrics_only=True,before_sha256=sha(p),candidate_sha256=sha(dst)))
for g in m['glyphs']:
 expected=g['before_sha256'] if g.get('metrics_only') else g['candidate_sha256'];assert sha(R/g['path'])==expected
for g in m['glyphs']:
 if g.get('metrics_only'):(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Corrected two Regular wrapper advances; drawings and human grades unchanged.')
