from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
import uharfbuzz as hb,json,io
C=Path(__file__).resolve().parent;rows=[]
for name in ['virtua','rubik']:
 for extra in [[],[0x2010],[0x2010,0x2d]]:
  f=TTFont(C/'assets'/f'{name}.ttf');s=subset.Subsetter();s.populate(unicodes=[ord(c) for c in 'extra\u2011ordinary']+extra);s.subset(f);buf=io.BytesIO();f.save(buf);data=buf.getvalue();f=TTFont(io.BytesIO(data))
  for w in [400,475,550,625,700]:
   hf=hb.Font(hb.Face(data));hf.set_variations({'wght':w});b=hb.Buffer();b.add_str('extra\u2011ordinary');b.guess_segment_properties();hb.shape(hf,b)
   glyphs=[f.getGlyphName(i.codepoint) for i in b.glyph_infos];rows.append({'font':name,'weight':w,'extra_requested':extra,'cmap_2010':f.getBestCmap().get(0x2010),'cmap_2011':f.getBestCmap().get(0x2011),'glyphs':glyphs,'has_notdef':'.notdef' in glyphs})
   assert ('.notdef' in glyphs)==(name=='rubik' or not extra)
(C/'subset-assessment.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'real subset samples; missing-glyph cases',sum(r['has_notdef']for r in rows))
