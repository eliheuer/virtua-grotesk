"""Source scope and compiled dependency/shaping regression checks for ARB-003."""
from pathlib import Path
import hashlib,json,plistlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((C/'applied.json').read_text());changed=[p for p,h in m['source_hashes'].items() if sha(R/p)!=h]
assert set(changed)=={g['path'] for g in m['glyphs']}
for g in m['glyphs']:assert sha(R/g['path'])==g['candidate_sha256']
assert sha(R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif')==m['regular_sha256']
post=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes())['public.postscriptNames']
allowed={post.get(n,n.replace('-','')) for n in m['dependent_source_glyphs']}
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];orders=[TTFont(p).getGlyphOrder() for p in paths];assert orders[0]==orders[1]
fonts=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
samples=['أ','ـأ','بأ','أب','بأب','تأ','فأ','لأ','بلأ','أَ','أُ','أٌ','أً','أْ','أِ','أٍ','أ','بأ','ؤ','بؤ','ؤ','بؤ','ئ','ئ','ئب','بئ','بئب','ۂ','بۂ','ۂب','بۂب','بٔ','بَٔ','بُٔ','بٌٔ','بًٔ','بْٔ','بِٔ','بَأْس','سُؤَال','بِئْر','رَئِيس']
report={'source_changes':changed,'font_hashes':dict(zip(['before','working'],map(sha,paths))),'allowed_compiled_dependencies':sorted(allowed),'compiled_changes':{},'checks':[]}
def shape(f,text):
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [{'name':orders[0][i.codepoint],'cluster':i.cluster,'advance':p.x_advance,'offset':[p.x_offset,p.y_offset]} for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 gs=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[]
 for n in gs[0]:
  values=[]
  for font in gs:
   pen=DecomposingRecordingPen(font);font[n].draw(pen);values.append((pen.value,font[n].width))
  assert values[0][1]==values[1][1],(w,n,'advance changed')
  if values[0]!=values[1]:diff.append(n)
 assert set(diff)<=allowed,(w,set(diff)-allowed)
 report['compiled_changes'][str(w)]=diff
 for f in fonts:f.set_variations({'wght':w})
 for text in samples:
  a,b=[shape(f,text) for f in fonts];assert all(x['name']!='.notdef' for x in a+b)
  assert [(x['name'],x['cluster'],x['advance']) for x in a]==[(x['name'],x['cluster'],x['advance']) for x in b],(w,text)
  if w==400:assert a==b
  report['checks'].append({'weight':w,'text':text,'before':a,'working':b})
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(report['checks']),'shaping contexts. Only donor dependencies changed; every compiled advance unchanged.')
print('Regular compiled differences (joint quadratic conversion):',report['compiled_changes']['400'])
