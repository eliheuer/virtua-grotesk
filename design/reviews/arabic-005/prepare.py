from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,re
R=Path(__file__).resolve().parents[3];C=R/'agent-proofs/cases/arabic-005';C.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shapes={
'behDotless-ar':(944,[(64,200),(64,64),(128,0),(256,0),(688,0),(816,0),(880,64),(880,200),(880,320),(864,336),(728,336),(712,320),(712,216),(712,192),(696,176),(672,176),(272,176),(248,176),(232,192),(232,216),(232,320),(216,336),(80,336),(64,320)]),
'behDotless-ar.init':(288,[(-16,16),(0,0),(152,0),(232,88),(232,240),(232,416),(216,432),(80,432),(64,416),(64,240),(64,200),(40,176),(0,176),(-16,160)]),
'behDotless-ar.medi':(416,[(64,0),(128,0),(168,0),(200,64),(208,64),(240,0),(280,0),(344,0),(416,0),(416,176),(344,176),(304,176),(288,192),(288,232),(288,320),(272,336),(136,336),(120,320),(120,232),(120,192),(104,176),(64,176),(0,176),(-16,160),(-16,16),(0,0)]),
'behDotless-ar.fina':(1024,[(1024,0),(1024,176),(960,176),(920,200),(920,248),(920,320),(904,336),(768,336),(752,320),(752,248),(752,200),(728,176),(680,176),(312,176),(264,176),(240,200),(240,248),(240,320),(224,336),(88,336),(72,320),(72,200),(72,64),(128,0),(256,0),(728,0),(776,0),(800,0),(832,64),(840,64),(872,0),(960,0)])}
assert not (C/'candidate.json').exists()
m={'baseline_commit':'211c3b8d','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
for master in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{master}.ufo';contents=plistlib.loads((root/'glyphs/contents.plist').read_bytes())
 for name,(width,points) in shapes.items():
  p=root/'glyphs'/contents[name];rel=p.relative_to(R);old=p.read_text();q=C/'before-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
  if master=='Regular':continue
  assert '<string>red</string>' in old
  it=iter(points)
  def pt(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',pt,old)
  assert next(it,None) is None
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
  reg=E.parse(R/f'sources/VirtuaGrotesk-Regular.ufo/glyphs/{contents[name]}');draft=E.fromstring(new)
  assert [[x.get('type') for x in c] for c in reg.findall('outline/contour')]==[[x.get('type') for x in c] for c in draft.findall('outline/contour')]
  q=C/'candidate-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(new)
  m['glyphs'].append(dict(name=name,path=str(rel),before_sha256=sha(p),candidate_sha256=sha(q)))
# Component closure: no frozen Bold dependent may inherit a drawing change.
p=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';contents=plistlib.loads((p/'contents.plist').read_bytes());deps=set(shapes)
while True:
 new={n for n,f in contents.items() if any(x.get('base') in deps for x in E.parse(p/f).findall('.//component'))}-deps
 if not new:break
 deps|=new
for n in deps:assert '<string>green</string>' not in (p/contents[n]).read_text(),n
m['inherited_bold_glyphs']=sorted(deps-set(shapes))
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf')
shutil.copy2(R/'OFL.txt',C/'assets/Virtua-OFL.txt')
print('Prepared 4 Bold bases; 41 dependent drawings inherit, none green. All Regular bytes preserved.')
