from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,json,re
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((C/'assessment.json').read_text());assert all(sha(R/p)==h for p,h in a['source_hashes'].items());assert all(sha(R/p)==h for p,h in a['active_fonts'].items())
f=TTFont(C/'assets/virtua.ttf');delta={}
for name in a['diagnostic_only_cmap_edits']:
 g=TTFont(C/'assets'/f'{name}.ttf');changed=[t for t in f.keys() if t!='GlyphOrder' and f.getTableData(t)!=g.getTableData(t)];assert set(changed)<={'head','cmap'};delta[name]=changed
browser={}
for p in (C/'browser').glob('*.ax.txt'):
 s=p.read_text();m=re.search(r'text (\[\{"font":.*\}\])',s);assert m,p
 rows=json.loads(m[1]);assert all(abs(x['breakingHeight']-2*x['nbHeight'])<.01 and abs(x['asciiHeight']-2*x['nbHeight'])<.01 for x in rows)
 for x in rows:
  if x['font']!='probe-2011-H':assert x['nbWidth']==x['hyWidth']
  else:assert x['nbWidth']>x['hyWidth']
 browser[p.name]=rows
screens={str(p.relative_to(C)):sha(p) for p in (C/'browser').glob('*.png')};assert len(screens)==12
(C/'final-identity.json').write_text(json.dumps({'head':a['head'],'source_count_unchanged':len(a['source_hashes']),'active_font_hashes_unchanged':a['active_fonts'],'probe_changed_tables':delta,'browser_measurements':browser,'inspected_screenshots':screens,'scope':'One Codex in-app browser; English; weights400/550/700. Twelve screenshots inspected. Controlled fixture28px/160px; six actual Diffenator supplement views. No cross-platform/native-reader approval.'},indent=2)+'\n');print('1823 sources and five active fonts unchanged; twelve screenshots; 80 shaping and30 subset samples.')
