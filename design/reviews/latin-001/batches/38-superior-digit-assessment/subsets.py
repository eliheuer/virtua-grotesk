"""Real in-memory subsets; none becomes a source or release input."""
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
import io,json,uharfbuzz as hb
C=Path(__file__).resolve().parent;rows=[]
for name in ['virtua','rubik']:
 for text in ['x¹ x² x³','123']:
  for policy in ['default','all-features']:
   f=TTFont(C/'assets'/f'{name}.ttf');o=subset.Options();o.glyph_names=True
   if policy=='all-features':o.layout_features=['*']
   s=subset.Subsetter(options=o);s.populate(text=text);s.subset(f);buf=io.BytesIO();f.save(buf);data=buf.getvalue();f=TTFont(io.BytesIO(data))
   for w in [400,475,550,625,700]:
    modes={}
    for feat in [{},{'sups':1}]:
     hf=hb.Font(hb.Face(data));hf.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(hf,b,feat)
     modes['sups' if feat else 'default']=[{'glyph':f.getGlyphName(i.codepoint),'advance':p.x_advance,'x':p.x_offset,'y':p.y_offset} for i,p in zip(b.glyph_infos,b.glyph_positions)]
    assert any(q['glyph']=='.notdef' for q in modes['default'])==(name=='virtua' and '¹' in text)
    rows.append({'font':name,'text':text,'weight':w,'layout_policy':policy,'features_requested':o.layout_features,'modes':modes})
(C/'subset-assessment.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'real subset cases, two feature modes each')
for r in rows:
 if r['font']=='rubik' and r['text']=='123' and r['weight']==400:print(r['layout_policy'],r['modes'])
