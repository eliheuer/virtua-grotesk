from pathlib import Path
from fontTools.ttLib import TTFont
import json,hashlib,xml.etree.ElementTree as E,plistlib
R=Path.cwd();C=R/'agent-proofs/cases/latin-001/batches/29-long-slash';b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);ch=json.loads((C/'changes.json').read_text());owned={x['path']:x for x in ch};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in b['sources'].items():assert sha(R/p)==(owned[p]['after'] if p in owned else h),p
for x in ch:assert sha(R/x['path'])==x['after']
font_hashes={}
for p in (R/'fonts').rglob('*.ttf'):
 rel=p.relative_to(R);a=TTFont(p);s=TTFont(S/rel);assert a.keys()==s.keys();assert all(a.getTableData(k)==s.getTableData(k) for k in a.keys() if k not in ['GlyphOrder','head']),p;font_hashes[str(rel)]=sha(p)
greens={}
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());protected={}
 for n,f in idx.items():
  root=E.parse(d/f).getroot();lib=root.find('lib/dict')
  if lib is None:continue
  g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>');rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):
   rel=str((d/f).relative_to(R));assert sha(d/f)==b['sources'][rel];protected[n]=sha(d/f)
 greens[m]=protected
images=[f'{k}-{w}.png' for k in ['forms','words'] for w in [400,550,700]]+['detail-400.png','detail-700.png']
(C/'final-identity.json').write_text(json.dumps({'source_baseline_head':b['head'],'sources':{x['path']:x['after'] for x in ch},'active_fonts':font_hashes,'active_scratch_tables_identical_except_head':True,'inspected_images':{n:sha(C/n) for n in images},'green_sources_preserved':greens},indent=2)+'\n')
print('Identity verified; green counts', {m:len(v) for m,v in greens.items()})
