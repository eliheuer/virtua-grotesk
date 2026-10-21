"""Second trial: compact dots in constrained counters and compound vowels."""
from pathlib import Path
import json,hashlib,re
C=Path(__file__).resolve().parent;R=C.parents[2]
def dot(x,y):return [(x,y-40),(x+24,y-40),(x+40,y-24),(x+40,y),(x+40,y+24),(x+24,y+40),(x,y+40),(x-24,y+40),(x-40,y+24),(x-40,y),(x-40,y-24),(x-24,y-40)]
shapes={
'dagesh-hb':[dot(64,328)],
'hatafsegol-hb':[dot(56,-48),dot(112,-160),dot(168,-48),dot(264,-160),dot(264,-48)],
'hatafpatah-hb':[[(192,-88),(192,-24),(32,-24),(32,-88)],dot(264,-48),dot(264,-160)],
'hatafqamats-hb':[[(144,-152),(144,-88),(192,-88),(192,-24),(32,-24),(32,-88),(80,-88),(80,-152)],dot(264,-48),dot(264,-160)]}
m=json.loads((C/'bold-candidate.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row in m['glyphs']:
 p=R/row['path'];assert sha(p)==row['candidate_sha256'],p
 old=p.read_text();pts=iter(pt for contour in shapes.get(row['glyph'],[]) for pt in contour)
 def replace(match):
  x,y=next(pts);return f'<point x="{x}" y="{y}"'+match[1]
 new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',replace,old) if row['glyph'] in shapes else old
 q=C/'candidate-v2'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_text(new);p.write_text(new);row['candidate_sha256']=sha(q)
(C/'bold-candidate-v2.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied v2 refinement to four Bold marks; other 12 retained')
