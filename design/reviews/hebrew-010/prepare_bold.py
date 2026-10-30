"""Bounded Bold mark repair: preserve Regular, topology, anchors and review colors."""
from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dot(x,y):
 # 96-unit round dot, equal 32-unit axis-tangent handles; original cyclic order.
 return [(x,y-48),(x+32,y-48),(x+48,y-32),(x+48,y),(x+48,y+32),(x+32,y+48),(x,y+48),(x-32,y+48),(x-48,y+32),(x-48,y),(x-48,y-32),(x-32,y-48)]
def bar(x0,x1,top,bottom):return [(x1,bottom),(x1,top),(x0,top),(x0,bottom)]
def qamats(x0,x1,l,r,top,cross,bottom):return [(r,bottom),(r,cross),(x1,cross),(x1,top),(x0,top),(x0,cross),(l,cross),(l,bottom)]
shapes={
 'sheva-hb':[dot(56,-56),dot(56,-168)],
 'hatafsegol-hb':[dot(32,-56),dot(96,-168),dot(160,-56),dot(288,-168),dot(288,-56)],
 'hatafpatah-hb':[bar(0,192,-24,-88),dot(272,-56),dot(272,-168)],
 'hatafqamats-hb':[qamats(0,192,64,128,-24,-88,-152),dot(272,-56),dot(272,-168)],
 'hiriq-hb':[dot(72,-128)],'tsere-hb':[dot(64,-128),dot(192,-128)],
 'segol-hb':[dot(48,-56),dot(112,-168),dot(176,-56)],
 'patah-hb':[bar(16,208,-56,-120)],'qamats-hb':[qamats(16,208,80,144,-48,-112,-176)],
 'holam-hb':[dot(72,720)],'holamhaser-hb':[dot(72,720)],
 'qubuts-hb':[dot(32,-56),dot(128,-120),dot(224,-184)],
 'dagesh-hb':[dot(72,336)],'shindot-hb':[dot(72,720)],'sindot-hb':[dot(72,720)],
 'qamatsqatan-hb':[[(176,-200),(168,-104),(264,-104),(264,-40),(8,-40),(8,-104),(104,-104),(96,-200)]]}
assert not (C/'bold-candidate.json').exists(),'Preserve candidate evidence'
manifest={'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
for name,contours in shapes.items():
 rel=f'sources/VirtuaGrotesk-Bold.ufo/glyphs/{name}.glif';p=R/rel;old=p.read_text();e=E.fromstring(old)
 assert '0.27,0.44,1,1' in old,name
 assert [len(c) for c in e.findall('outline/contour')]==[len(c) for c in contours],name
 pts=iter(p for c in contours for p in c)
 def replace(m):
  x,y=next(pts);assert x%8==0 and y%8==0;return f'<point x="{x}" y="{y}"'+m[1]
 new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',replace,old)
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 manifest['glyphs'].append(dict(glyph=name,path=rel,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
(C/'bold-candidate.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared 16 Bold marks; Regular, point topology, anchors and colors unchanged.')
