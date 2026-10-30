"""Read-only Arabic source inventory; colors do not establish visual completion."""
from pathlib import Path
import json,plistlib,hashlib,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
rows=[]
for master in ['Regular','Bold']:
 p=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cs=plistlib.loads((p/'contents.plist').read_bytes())
 for name,f in sorted(cs.items()):
  if '-ar' not in name and not name.startswith('arabic'):continue
  path=p/f;r=E.parse(path);lib=r.find('lib/dict');d=plistlib.loads(b'<plist><dict>'+b''.join(E.tostring(c) for c in lib)+b'</dict></plist>') if lib is not None else {}
  label=d.get('com.runebender.glyph.color')
  # Editor label is preferred; retain raw RGBA because earlier files use it alone.
  labels={x.text for x in r.findall('lib/dict/string')};label=next((x for x in ['green','purple','red','orange','yellow','blue','pink'] if x in labels),None)
  rgba=d.get('public.markColor');frozen=label=='green' or rgba in ['0,1,0,1','0.09,0.72,0.44,1']
  rows.append(dict(master=master,name=name,path=str(path.relative_to(R)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),color=label,rgba=rgba,frozen=frozen,unicode=[u.get('hex') for u in r.findall('unicode')],contours=[len(c) for c in r.findall('outline/contour')],components=[c.attrib for c in r.findall('outline/component')]))
(C/'inventory.json').write_text(json.dumps({'note':'Snapshot only; rerun before selecting or applying. Human review is separate.','glyphs':rows},indent=2)+'\n')
for m in ['Regular','Bold']:
 a=[x for x in rows if x['master']==m];print(m,len(a),'Arabic glyphs;',sum(x['frozen'] for x in a),'green;',sum(bool(x['contours']) for x in a),'with contours')
