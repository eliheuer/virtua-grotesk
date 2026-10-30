from pathlib import Path
import json,xml.etree.ElementTree as E,copy,subprocess,sys
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'applied.json').read_text());(C/'diagnostics').mkdir(exist_ok=True)
def resolve(master,name,stage,dx=0,dy=0):
 import plistlib
 root=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes());p=root/cs[name];local=C/(stage+'-sources')/p.relative_to(R);t=E.parse(local if local.exists() else p);out=[]
 for c in t.findall('outline/contour'):
  c=copy.deepcopy(c)
  for p in c:p.set('x',str(float(p.get('x'))+dx));p.set('y',str(float(p.get('y'))+dy))
  out.append(c)
 for co in t.findall('outline/component'):
  assert set(co.attrib)<={'base','xOffset','yOffset'}
  out+=resolve(master,co.get('base'),stage,dx+float(co.get('xOffset','0')),dy+float(co.get('yOffset','0')))
 return out
for g in m['glyphs']:
 if not g['drawing']:continue
 for stage in ['before','candidate']:
  t=E.parse(C/(stage+'-sources')/g['path']);o=t.find('outline');o.clear();o.extend(resolve(g['master'],g['name'],stage));p=C/'diagnostics'/f'{stage}-{g["master"]}-{g["name"]}.glif';t.write(p)
 stem=g['master']+'-'+g['name'];subprocess.run([sys.executable,str(R/'scripts/curve_profile.py'),str(C/'diagnostics'/('before-'+stem+'.glif')),str(C/'diagnostics'/('candidate-'+stem+'.glif')),'--json',str(C/(stem+'-curves.json')),'--svg',str(C/(stem+'-comb.svg'))],check=True)
