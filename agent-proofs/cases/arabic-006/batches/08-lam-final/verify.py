from pathlib import Path
import json,hashlib,sys,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;R=C.parents[4];m=json.loads((C/'candidate.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/p)==h for p,h in m['source_hashes'].items()),'Active source changed; refresh baseline, never overwrite'
assert all(sha(R/p)==h for p,h in m['reserved_beh_hashes'].items())
for g in m['glyphs']:assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
a,b=[E.parse(C/'candidate-sources'/g['path']) for g in m['glyphs']]
assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
paths=[C/'assets/before.ttf',C/'assets/after.ttf'];fonts=[TTFont(p) for p in paths];order=fonts[0].getGlyphOrder();assert order==fonts[1].getGlyphOrder()
# Follow the actual production naming, rather than assuming Unicode names.
import plistlib
lib=plistlib.loads((R/'sources/VirtuaGrotesk-Bold.ufo/lib.plist').read_bytes());name=lib['public.postscriptNames']['lam-ar.fina'];out={'active_sources_unchanged':True,'reserved_beh_files':len(m['reserved_beh_hashes']),'changed_glyph':name,'weights':{},'shaping_checks':[]}
hfs=[hb.Font(hb.Face(p.read_bytes())) for p in paths]
texts=['للل ل','بلب ل','لل للل','بلا لا','لَ لُ لِ','ببب ب','ممم م','سلام','العربية','لأ لإ لآ']
def shape(f,t):
 b=hb.Buffer();b.add_str(t);b.guess_segment_properties();b.language='ar';hb.shape(f,b)
 return [(order[i.codepoint],i.cluster,p.x_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
for w in [400,450,500,550,600,650,700]:
 sets=[instantiateVariableFont(TTFont(p),{'wght':w}).getGlyphSet() for p in paths];diff=[]
 for n in order:
  vals=[]
  for gs in sets:
   p=DecomposingRecordingPen(gs);gs[n].draw(p);vals.append((p.value,gs[n].width))
  if vals[0]!=vals[1]:diff.append(n)
 assert diff==[name],diff
 out['weights'][str(w)]={'changed':diff,'advance':[gs[name].width for gs in sets]}
 for f in hfs:f.set_variations({'wght':w})
 for t in texts:
  old,new=[shape(f,t) for f in hfs];assert len(old)==len(new)
  for a,b in zip(old,new):
   assert a[:2]==b[:2] and a[3:]==b[3:] and b[0]!='.notdef',(w,t,a,b)
   delta=sets[1][b[0]].width-sets[0][a[0]].width
   assert abs(b[2]-a[2]-delta)<=1,(w,t,a,b,delta)
  out['shaping_checks'].append({'weight':w,'text':t,'candidate':new})
(C/'verification.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print('70 shaping comparisons; only final Lam differs; active source baseline intact.')
