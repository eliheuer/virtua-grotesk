from pathlib import Path
import json,sys,xml.etree.ElementTree as E,subprocess
C=Path(__file__).resolve().parent;R=Path.cwd();m=json.loads((C/'candidate.json').read_text());S=Path(m['scratch']);sys.path.insert(0,str(R/'scripts'))
from curve_profile import profile
rows={}
for w in ['Regular','Bold']:
 g=next(g for g in m['glyphs'] if g['master']==w and g['name']=='tteh-ar');t=E.parse(S/g['path']);o=t.find('outline');o.remove(o.find('component'));p=C/f'{w}-local-mark.glif';t.write(p);row=profile(p);rows[w]=row
 assert not row['warnings'],row['warnings']
 for j in row['joins']:
  assert j['classification']!='kink',j
 result=subprocess.run([str(R/'.venv/bin/python'),str(S/'scripts/curve_lint.py'),w,'tteh-ar','tteh-ar.init','tteh-ar.medi','tteh-ar.fina','--joins'],cwd=S,capture_output=True,text=True)
 (C/f'{w}-lint.txt').write_text(result.stdout+result.stderr)
(C/'curves.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Local mark signed curvature and tangent profiles checked.')
