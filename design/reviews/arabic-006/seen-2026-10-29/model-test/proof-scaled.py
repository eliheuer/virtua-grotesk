import sys,json,hashlib,plistlib,shutil,html
from pathlib import Path
sys.path.insert(0,'scripts');import construction_review as cr
root=Path.cwd();out=root/'out/seen-model-test/scaled';rows=[]
for rev in (4,6):
 for master in ('Regular','Bold'):
  paths=[out/f'v{rev}-{master}-input.glif',out/f'v{rev}-{master}-identity.glif',out/f'v{rev}-{master}-faithful.glif'];labels=['Rejected input','Sketch: identity','Sketch: faithful']
  if master=='Regular':
   u=out/f'v{rev}-bolden.ufo';layers=plistlib.loads((u/'layercontents.plist').read_bytes());folder=dict(layers)['com.runebender.proposal.bolden'];cs=plistlib.loads((u/folder/'contents.plist').read_bytes());p=out/f'v{rev}-bolden.glif';shutil.copyfile(u/folder/cs['seen-ar'],p);
   import xml.etree.ElementTree as E
   d=E.parse(p)
   for n in d.findall('.//point'):
    for k in ('x','y'): n.set(k,str(float(n.get(k))/.75))
   a=d.find('advance');a.set('width',str(float(a.get('width'))/.75));d.write(p)
   paths.append(p);labels.append('Bolden: target Bold, from Regular')
  rows.append(f'<h2>Rejected v{rev} · {master}</h2><section>'+''.join(f'<article><h3>{l}</h3>{cr.svg(p)}<small>{p.name}</small></article>' for p,l in zip(paths,labels))+'</section>')
proof='''<!doctype html><meta charset="utf-8"><title>Seen local-model scratch test</title><style>body{background:#222;color:#ddd;font:16px system-ui;margin:24px}section{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}svg{width:100%;fill:#ddd}.nodes{display:none}h3{font-size:15px}article{min-width:0}small{overflow-wrap:anywhere}</style><h1>Seen local-model test — scratch only</h1><p>Range-controlled test: inputs uniformly scaled to 75%, snapped to model 2-unit tokens, outputs restored to original scale. Greedy decoding. Not a native-size quality benchmark. No model output is approved or applied. Bolden is weight transfer, not same-weight repair.</p>'''+''.join(rows)
(root/'out/live-proof/seen-model-test.html').write_text(proof)
receipt=json.loads((out/'receipt.json').read_text());m=Path.home()/'.runebender/models/virtua-12m-bolden';receipt['bolden_model_files']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in m.iterdir() if p.is_file()};receipt['bolden_runs']=[json.loads((out/f'bolden-v{r}.json').read_text()) for r in (4,6)];(out/'receipt.json').write_text(json.dumps(receipt,indent=2))
print([(r['revision'],r['master'],r['mode'],round(r['input_iou'],3)) for r in receipt['runs']])
