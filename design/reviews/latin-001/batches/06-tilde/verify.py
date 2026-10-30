from pathlib import Path
import hashlib,json,os,plistlib,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];base=json.loads((C/'baseline.json').read_text());S=Path(os.environ.get('VERIFY_ROOT',base['scratch']));changes=json.loads((C/'changes.json').read_text());closure=json.loads((C/'dependencies.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
allowed={x['path'] for x in changes}
assert all(sha(S/p)==h for p,h in base['sources'].items() if p not in allowed)
for x in changes:assert sha(S/x['path'])==x['after']
roots={}
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());roots[m]={n:E.parse(d/f).getroot() for n,f in idx.items()}
assert roots['Regular'].keys()==roots['Bold'].keys()
for n,a in roots['Regular'].items():
 b=roots['Bold'][n]
 assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in b.findall('outline/component')],n
for x in changes:
 old=E.parse(C/'before-sources'/x['path']).getroot();new=E.parse(S/x['path']).getroot()
 assert old.find("anchor[@name='_top']").attrib==new.find("anchor[@name='_top']").attrib
 assert old.find("anchor[@name='top']").get('x')==new.find("anchor[@name='top']").get('x')
 assert [(a.tag,a.attrib) for a in old.findall('advance')]==[(a.tag,a.attrib) for a in new.findall('advance')]
 assert all(float(p.get(c))%8==0 for p in new.findall('.//point') for c in ['x','y'])

def shape(font,data,text,w):
 f=hb.Font(hb.Face(data));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b)
 gs=font.getGlyphSet(location={'wght':w});cursor=0;bb=[];seq=[]
 for g,p in zip(b.glyph_infos,b.glyph_positions):
  assert g.codepoint,text
  name=font.getGlyphName(g.codepoint);pen=BoundsPen(gs);gs[name].draw(TransformPen(pen,(1,0,0,1,cursor+p.x_offset,p.y_offset)));bb.append(pen.bounds);cursor+=p.x_advance;seq.append((name,p.x_advance,p.y_advance,p.x_offset,p.y_offset))
 return seq,bb
before=C/'assets/before.ttf';after=S/'fonts/variable/VirtuaGrotesk[wght].ttf';bf=TTFont(before);af=TTFont(after);bd=before.read_bytes();ad=after.read_bytes();ink={};checks=0
for w in [400,475,550,625,700]:
 bg=bf.getGlyphSet(location={'wght':w});ag=af.getGlyphSet(location={'wght':w});diff=[]
 for n in bg:
  a=DecomposingRecordingPen(bg);b=DecomposingRecordingPen(ag);bg[n].draw(a);ag[n].draw(b)
  if a.value!=b.value:diff.append(n)
 allowed_ink=set(closure['Bold']['consumers']);assert set(diff)<=allowed_ink,(w,set(diff)-allowed_ink);ink[str(w)]=diff
 for sample in ['ã́','ṹ','b̃́','b̃̃','ū́','ǘ','á́','b̄́','ḇ','V̱','Mañana','São João','Ã Ẽ Ĩ Ñ Õ Ũ','ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:
  bs,bb=shape(bf,bd,sample,w);as_,ab=shape(af,ad,sample,w)
  assert [x[:3] for x in bs]==[x[:3] for x in as_],(w,sample,'sequence/advance changed')
  if sample not in ['ã́','ṹ','b̃́','b̃̃']:assert bs==as_,(w,sample,'positions changed')
  if sample in ['ã́','ṹ','b̃́','b̃̃','ū́','ǘ','á́','b̄́']:assert ab[-1][1]-ab[-2][3]>=16,(w,sample,ab)
  if sample in ['ḇ','V̱']:assert ab[0][1]-ab[1][3]>=16,(w,sample,ab)
  if sample in ['ببب ب','ھھھ ھ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','׆̇']:assert bb==ab,(w,sample)
  checks+=1
out={'shaping_checks':checks,'changed_compiled_ink':ink,'unchanged_source_files':len(base['sources'])-len(allowed),'after_sha256':sha(after),'notes':['All non-target source bytes preserved, including Arabic recursive donors and green sources.','Incoming anchors and advances unchanged; outgoing tilde stack anchors adjusted. All new points on 8.','Shape/position equality, stack and below-mark clearance at five weights.']};(C/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,'checks; full master compatibility and non-target preservation passed')
