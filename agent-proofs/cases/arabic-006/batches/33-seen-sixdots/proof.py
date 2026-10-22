from pathlib import Path
import json,hashlib,shutil,subprocess
C=Path(__file__).resolve().parent;m=json.loads((C/'candidate.json').read_text());s=Path(m['scratch'])
shutil.copy2(s/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/after.ttf')
e=json.loads((C/'evidence.json').read_text())
for role in ['before','after']:e['fonts'][role]['sha256']=hashlib.sha256((C/'assets'/f'{role}.ttf').read_bytes()).hexdigest()
e['fonts']['after']['label']='Candidate'
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['.venv/bin/python','agent-proofs/app/prepare.py','--evidence',str(C/'evidence.json'),'--output-dir',str(C/'working')],check=True)
