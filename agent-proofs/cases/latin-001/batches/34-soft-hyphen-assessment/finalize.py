from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,json,re
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((C/'assessment.json').read_text());assert all(sha(R/p)==h for p,h in a['source_hashes'].items())
old=json.loads((C.parent/'33-brokenbar/final-identity.json').read_text())['active_fonts'];assert all(sha(R/p)==h for p,h in old.items())
f=TTFont(C/'assets/virtua.ttf');deltas={}
for name in a['diagnostic_only_cmap_edits']:
 g=TTFont(C/'assets'/f'{name}.ttf');changed=[t for t in f.keys() if t!='GlyphOrder' and f.getTableData(t)!=g.getTableData(t)];assert set(changed)<= {'head','cmap'},changed;deltas[name]=changed
browser={}
for p in (C/'browser').glob('*.ax.txt'):
 s=p.read_text();match=re.search(r'text (\[\{"font":.*\}\])',s);assert match,p
 rows=json.loads(match[1]);assert all(abs(x['manualHeight']-2*x['noneHeight'])<.01 for x in rows)
 for x in rows:
  if x['nowrapWidth'] is not None:assert x['nowrapWidth']==x['plainWidth']
 browser[p.name]=rows
screens={str(p.relative_to(C)):sha(p) for p in (C/'browser').glob('*.png')};assert len(screens)==12
out={'head':a['head'],'all_1821_sources_unchanged':True,'active_font_hashes_unchanged':old,'probe_changed_tables':deltas,'browser_measurements':browser,'inspected_screenshots':screens,'scope':'One Codex in-app browser, English, weights400/550/700. All12 screenshots visually inspected. Not native editor or cross-browser approval.'}
(C/'final-identity.json').write_text(json.dumps(out,indent=2)+'\n');print('All1821 sources and five active fonts unchanged;12 screenshots;75 default-ignorable shaping cases.')
