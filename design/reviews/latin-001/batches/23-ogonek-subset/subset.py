from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
import io,json,unicodedata as U,uharfbuzz as hb
C=Path(__file__).resolve().parent
letters='ĄąĘęĮįŲų';suffixes=['','́','̀','̂','̃','̄','̆','̇','̈','̊','̋','̌','̨','́́','̧́']
def signature(f,data,text,w):
 h=hb.Font(hb.Face(data));h.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(h,b);adv=0;out=[]
 for g,p in zip(b.glyph_infos,b.glyph_positions):
  assert g.codepoint
  out.append((f.getGlyphName(g.codepoint),adv+p.x_offset,p.y_offset));adv+=p.x_advance
 return adv,sorted(out)
report={}
for n in ['before','after']:
 p=C/'assets'/f'{n}.ttf';f=TTFont(p);s=TTFont(p);o=subset.Options();o.layout_features=['*'];o.glyph_names=True;ss=subset.Subsetter(options=o);ss.populate(unicodes=set(f.getBestCmap())-set(map(ord,letters)));ss.subset(s);sp=C/'assets'/f'{n}-subset.ttf';s.save(sp);fails=[];count=0
 for w in [400,475,550,625,700]:
  for c in letters:
   for suffix in suffixes:
    for t in [c+suffix,U.normalize('NFD',c+suffix)]:
     a=signature(f,p.read_bytes(),t,w);b=signature(s,sp.read_bytes(),t,w);count+=1
     if a!=b:fails.append({'weight':w,'text':t,'full':a,'subset':b})
 report[n]={'comparisons':count,'failures':fails}
(C/'real-subset.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({n:len(x['failures']) for n,x in report.items()});assert not report['after']['failures']
