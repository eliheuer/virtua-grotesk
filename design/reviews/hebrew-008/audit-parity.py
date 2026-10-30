"""Inventory frozen Rubik coverage, source permissions and unchanged-weight forms."""
import json,hashlib,unicodedata as U,xml.etree.ElementTree as E,plistlib
from pathlib import Path
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;R=C.parents[2]
rubik=next((C/'working-v2/fonts').glob('rubik*.ttf'));ref=TTFont(rubik);font=TTFont(R/'fonts/variable/VirtuaGrotesk[wght].ttf');cm=font.getBestCmap()
refs=sorted(c for c in ref.getBestCmap() if 0x590<=c<=0x5ff or 0xfb1d<=c<=0xfb4f)
masters={};donors={}
for m in ['Regular','Bold']:
 gs=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';index={}
 for p in gs.glob('*.glif'):
  e=E.parse(p).getroot()
  for cp in e.findall('unicode'):index[int(cp.get('hex'),16)]=(p,e)
 masters[m]=index
 for n in ['H','n','o','O','gimel-hb','zayin-hb','yod-hb']:
  # Map actual case-sensitive source filename via contents.plist.
  file=plistlib.loads((gs/'contents.plist').read_bytes())[n];p=gs/file;donors[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for cp in refs:
 rec=dict(codepoint=f'U+{cp:04X}',name=U.name(chr(cp)),covered=cp in cm,sources={})
 outlines=[]
 for m,idx in masters.items():
  p,e=idx[cp];lib=e.find('lib/dict');d={}
  if lib is not None:
   es=list(lib);d={es[i].text:es[i+1].text for i in range(0,len(es),2)}
  outline=E.tostring(e.find('outline'));outlines.append(outline)
  rec['sources'][m]=dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),label=d.get('com.runebender.markLabel'),color=d.get('public.markColor'),contours=len(e.findall('outline/contour')),components=[c.get('base') for c in e.findall('outline/component')])
 rec['same_master_outline']=outlines[0]==outlines[1]
 decomp=U.normalize('NFD',chr(cp));rec['canonical_decomposition']=[f'U+{ord(c):04X}' for c in decomp] if decomp!=chr(cp) else []
 records.append(rec)
out=dict(reference=dict(path=str(rubik.relative_to(R)),sha256=hashlib.sha256(rubik.read_bytes()).hexdigest(),codepoints=len(refs)),missing=[x['codepoint'] for x in records if not x['covered']],source_records=records,reference_and_manual_hashes=donors,protected_work='Purple Hebrew marks/presentation forms and uncolored Bold equivalents remain untouched; explicit exception requested and pending.')
(C/'parity-inventory.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(len(refs),'Rubik codepoints;',len(out['missing']),'missing')
print('Same master outlines:',[(r['codepoint'],r['sources']['Regular']['path'].split('/')[-1]) for r in records if r['same_master_outline']])
