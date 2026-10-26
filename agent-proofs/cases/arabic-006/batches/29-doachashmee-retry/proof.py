from pathlib import Path
import json,hashlib,shutil,subprocess
C=Path(__file__).resolve().parent;old=C.parent/'27-doachashmee'
e=json.loads((old/'evidence.json').read_text())
for role in ['before','after']:e['fonts'][role]['sha256']=hashlib.sha256((C/'assets'/f'{role}.ttf').read_bytes()).hexdigest()
e['fonts']['after']['label']='Candidate · Not applied'
e['description']='Doachashmee whole-form retry · Scratch candidate'
e['study']['status']='Scratch candidate · Not applied'
e['study']['note']='Whole-form retry. Both weights are a separate experiment; active sources are unchanged. Regular medial needs named green approval before application.'
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for f in ['detail.rs','render.py']:shutil.copy2(old/f,C/f)
p=C/'detail.rs';p.write_text(p.read_text().replace('Working drawings','Scratch candidate'))
subprocess.run(['.venv/bin/python','agent-proofs/app/prepare.py','--evidence',str(C/'evidence.json'),'--output-dir',str(C/'working')],check=True)
