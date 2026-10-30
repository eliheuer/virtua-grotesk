from pathlib import Path
import json,plistlib,xml.etree.ElementTree as E,hashlib,unicodedata
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
C=Path(__file__).resolve().parent;R=C.parents[4];names='zero four five six seven eight nine'.split();chars='⁰⁴⁵⁶⁷⁸⁹';rows=[]
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes())
 for n in names:
  p=d/idx[n];r=E.parse(p).getroot();lib=plistlib.loads(b'<plist>'+E.tostring(r.find('lib/dict'))+b'</plist>')
  rows.append({'master':m,'glyph':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'advance':r.find('advance').get('width'),'contour_points':[len(c) for c in r.findall('outline/contour')],'label':lib.get('com.runebender.markLabel'),'rgba':lib.get('public.markColor'),'components':[c.attrib for c in r.findall('outline/component')]})
f=TTFont(C/'assets/before.ttf');rf=TTFont(C/'assets/rubik.ttf');beforecmap=f.getBestCmap();rcmap=rf.getBestCmap();rubik=[]
for w in [400,550,700]:
 gs=rf.getGlyphSet(location={'wght':w})
 for c in chars:
  assert ord(c) not in beforecmap and ord(c) in rcmap
  p=BoundsPen(gs);g=gs[rcmap[ord(c)]];g.draw(p);rubik.append({'weight':w,'char':c,'bounds':p.bounds,'advance':g.width})
(C/'family-assessment.json').write_text(json.dumps({'baseline_head':json.loads((C/'baseline.json').read_text())['head'],'donors':rows,'normalization':[{'char':c,'NFD':unicodedata.normalize('NFD',c),'NFKD':unicodedata.normalize('NFKD',c),'decomposition':unicodedata.decomposition(c)} for c in chars],'rubik_measurements':rubik,'visual_reference':'reference.png actual rendered fonts, ordinary Virtua at112px and Rubik superiors224px; sizes explicitly differ to compare small-form construction. Initial overlap in fixture corrected before final review.','decision':'Bounded zero first. All seven ordinary donors green; preserve them. Zero retains Virtua oval rather than Rubik flatter side construction. Remaining4–9 need separate counter/terminal adaptation; no full sups feature now.'},ensure_ascii=False,indent=2)+'\n')
