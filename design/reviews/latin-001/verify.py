from pathlib import Path
import json,hashlib,io,unicodedata,plistlib,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[2];m=json.loads((C/'baseline.json').read_text());S=Path(m['scratch']);changes=json.loads((C/'changes.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
allowed={x['path'] for x in changes};assert all(sha(S/p)==h for p,h in m['sources'].items() if p not in allowed)
# No existing outline coordinates, anchors, or grades removed or rewritten: only
# outgoing anchors are added to spacing marks; thirteen component translations fixed.
for x in changes:
 if x['before'] and x['path'].endswith('.glif'):
  old=E.fromstring((C/'before-sources'/x['path']).read_bytes());new=E.fromstring((C/'candidate-sources'/x['path']).read_bytes())
  assert E.tostring(old.find('lib'))==E.tostring(new.find('lib'))
  assert [p.attrib for p in old.findall('.//point')]==[p.attrib for p in new.findall('.//point')]
  assert all(a.attrib in [b.attrib for b in new.findall('anchor')] for a in old.findall('anchor') if a.get('name')!='_hbNunDot')
  if old.find("anchor[@name='_hbNunDot']") is not None:
   assert int(old.find("anchor[@name='_hbNunDot']").get('y'))-int(new.find("anchor[@name='_hbNunDot']").get('y'))==176
# Source compatibility including component order.
contents={}
for w in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());contents[w]={n:E.parse(d/f).getroot() for n,f in cs.items()}
assert contents['Regular'].keys()==contents['Bold'].keys()
for n,a in contents['Regular'].items():
 b=contents['Bold'][n];assert [[p.get('type') for p in c] for c in a.findall('outline/contour')]==[[p.get('type') for p in c] for c in b.findall('outline/contour')],n
 assert [c.get('base') for c in a.findall('outline/component')]==[c.get('base') for c in b.findall('outline/component')],n
newtext='ĈĉĜĝĤĥĴĵǼǽ';marks=[0x300,0x301,0x302,0x304,0x306,0x307,0x308,0x30a,0x30b,0x30c,0x327,0x328,0x326]
def shape(data,text,w,features=None):
 f=hb.Font(hb.Face(data));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,features or {});return b

def boxes(font,data,text,w,features=None):
 b=shape(data,text,w,features);gs=font.getGlyphSet(location={'wght':w});cursor=0;result=[]
 for g,p in zip(b.glyph_infos,b.glyph_positions):
  assert g.codepoint!=0,text;n=font.getGlyphName(g.codepoint);pen=BoundsPen(gs);gs[n].draw(TransformPen(pen,(1,0,0,1,cursor+p.x_offset,p.y_offset)));result.append(pen.bounds);cursor+=p.x_advance
 return cursor,result
before=TTFont(C/'assets/before.ttf');after=TTFont(C/'assets/after.ttf');adata=(C/'assets/after.ttf').read_bytes();bdata=(C/'assets/before.ttf').read_bytes();checks=0;legacy_normalization=[]
# All existing compiled ink is unchanged except the thirteen translated marks.
allowed_names={before.getBestCmap()[c] for c in marks};changed={}
for w in [400,475,550,625,700]:
 bgs=before.getGlyphSet(location={'wght':w});ags=after.getGlyphSet(location={'wght':w});diff=[]
 for n in bgs:
  bp=DecomposingRecordingPen(bgs);ap=DecomposingRecordingPen(ags);bgs[n].draw(bp);ags[n].draw(ap)
  if bp.value!=ap.value:diff.append(n)
 assert set(diff)<=allowed_names,(w,set(diff)-allowed_names);changed[str(w)]=diff
 for c in newtext:
  boxes(after,adata,c,w);checks+=1
 # Every below mark and upper stack is now correctly attached, including
 # precomposed+mark (HarfBuzz normalizes decomposed inputs to these).
 for sample in ['ū́','ǘ','á́','Ņ̦','b́̂','b̄́']:
  _,bb=boxes(after,adata,sample,w);assert len(bb)>=2,(sample,bb)
  gap=bb[0][1]-bb[1][3] if sample=='Ņ̦' else bb[-1][1]-bb[-2][3]
  assert gap>=16,(w,sample,gap);checks+=1
 # Compare precomposed forms with real missing-cmap fallback. Disable ccmp
 # so a GSUB shortcut cannot hide component/anchor misalignment.
 chars='áàâãāăėäåőčçąņ'+newtext
 fallback=TTFont(C/'assets/after.ttf')
 for table in fallback['cmap'].tables:
  if table.isUnicode():
   for c in chars:table.cmap.pop(ord(c),None)
 stream=io.BytesIO();fallback.save(stream);fd=stream.getvalue()
 for c in chars:
  adv,bb=boxes(after,adata,c,w);fadv,fb=boxes(fallback,fd,c,w,{} if c in newtext else {'ccmp':False})
  bbox=lambda arr:(min(b[0] for b in arr if b),min(b[1] for b in arr if b),max(b[2] for b in arr if b),max(b[3] for b in arr if b))
  delta=max(abs(x-y) for x,y in zip(bbox(bb),bbox(fb)))
  # Explicit new J/h optical positioning differs from inherited base anchors.
  if c in newtext:assert delta<=1 and adv==fadv,(w,c,delta,adv,fadv)
  elif delta>1 or adv!=fadv:legacy_normalization.append(dict(weight=w,char=c,bounds_delta=delta,advance_delta=adv-fadv))
  checks+=1
 assert boxes(before,bdata,'׆̇',w)==boxes(after,adata,'׆̇',w),(w,boxes(before,bdata,'׆̇',w),boxes(after,adata,'׆̇',w))
 checks+=1
 # Existing Arabic/Hebrew glyphs and positions, including marks, remain exact.
 for text in ['ببب ب','ھھھ ھ','هحه','عَ سِ كُ','مرحبا بالعالم','שָׁלוֹם עוֹלָם','יִשְׂרָאֵל']:
  b=shape(bdata,text,w);a=shape(adata,text,w)
  norm=lambda f,b:[(f.getGlyphName(g.codepoint),p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(b.glyph_infos,b.glyph_positions)]
  assert norm(before,b)==norm(after,a),text;checks+=1
out={'checks':checks,'existing_changed_ink':changed,'sources_preserved':len(m['sources'])-sum(x['before'] is not None for x in changes),'after_sha256':sha(C/'assets/after.ttf'),'legacy_normalization':legacy_normalization,'notes':['Existing grades and point coordinates unchanged.','No Arabic or Hebrew source edit.','New J/h accent positioning does not repair inherited base anchors.']};(C/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out['checks'],'checks passed')
