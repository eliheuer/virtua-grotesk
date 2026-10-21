"""Scoped repair of the rejected Bold Feh/Qaf proof; preserve Regular bytes."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,sys
R=Path(__file__).resolve().parents[5];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Bounded head, counter and 64x64 return; outer and inner extrema are explicit.
counter=[(232,416),(192,440),(192,480),(192,520),(232,544),(272,544),(312,544),(352,520),(352,480),(352,424),(344,416),(272,416)]
head=[(512,480),(512,608),(416,704),(272,704),(128,704),(32,608),(32,480),(32,352),(128,256),(272,256)]
init=[(0,176),(-16,160),(-16,16),(0,0),(216,0),(384,0),(512,112),(512,248)]+head+[(344,256),(352,248),(352,240),(352,200),(328,176),(288,176)]
# Near-circular medial counter: radius 72 / handles 40; outer radius 232 / handles 128.
medi=[(568, 0), (568, 176), (472, 176), (472, 184), (488, 200), (504, 216), (504, 264), (504, 392), (400, 496), (272, 496), (144, 496), (40, 392), (40, 264), (40, 216), (56, 200), (72, 184), (72, 176), (0, 176), (-16, 160), (-16, 16), (0, 0)]
roundcounter=[(272, 192), (232, 192), (200, 224), (200, 264), (200, 304), (232, 336), (272, 336), (312, 336), (344, 304), (344, 264), (344, 224), (312, 192)]
isolated=[(736,0),(880,0),(960,96),(960,248)]+[(x+448,y) for x,y in head]+[(792,256),(800,248),(800,240),(800,200),(776,176),(736,176),(272,176),(224,176),(192,208),(192,256),(192,304),(176,320),(48,320),(32,304),(32,256),(32,112),(112,0),(272,0)]
final=[(272, 0), (552, 0), (600, 0), (640, 0), (680, 0), (688, 0), (736, 0), (800, 0), (848, 0), (1056, 0), (1056, 176), (920, 176), (920, 184), (936, 200), (952, 216), (952, 264), (952, 392), (848, 496), (720, 496), (592, 496), (488, 392), (488, 264), (488, 216), (504, 200), (520, 184), (520, 176), (272, 176), (224, 176), (192, 208), (192, 256), (192, 304), (176, 320), (48, 320), (32, 304), (32, 256), (32, 112), (112, 0)]
qaf=[(656,-256),(800,-256),(880,-160),(880,-8)]+[(x+368,y-256) for x,y in head]+[(712,0),(720,-8),(720,-16),(720,-56),(696,-80),(656,-80),(272,-80),(224,-80),(192,-48),(192,0),(192,112),(176,128),(48,128),(32,112),(32,0),(32,-144),(112,-256),(272,-256)]
qaffinal=[(264,-80),(192,-48),(192,0),(192,16),(176,32),(48,32),(32,16),(32,-32),(32,-176),(144,-256),(320,-256),(496,-256),(560,-176),(560,-8),(568,0),(688,0),(688,176),(568,176),(560,184),(560,384),(464,480),(320,480),(176,480),(80,384),(80,256),(80,128),(176,32),(320,32),(392,32),(400,24),(400,16),(400,-48),(376,-80),(320,-80)]
def circle(cx,cy):
 return [(cx,cy-112),(cx+64,cy-112),(cx+112,cy-64),(cx+112,cy),(cx+112,cy+64),(cx+64,cy+112),(cx,cy+112),(cx-64,cy+112),(cx-112,cy+64),(cx-112,cy),(cx-112,cy-64),(cx-64,cy-112)]
shapes={
 'fehDotless-ar.init':(544,counter+init),
 'fehDotless-ar.medi':(568,medi+roundcounter),
 'fehDotless-ar':(1024,[(x+448,y) for x,y in counter]+isolated),
 'fehDotless-ar.fina':(1056,final+[(x+448,y) for x,y in roundcounter]),
 'qafDotless-ar':(944,[(x+368,y-256) for x,y in counter]+qaf),
 'qafDotless-ar.fina':(688,[(x+48,y-224) for x,y in counter]+qaffinal),
 'twodotshorizontalabove-ar':(376,circle(24,768)+circle(280,768)),
 'threedotsupabove-ar':(536,circle(88,736)+circle(376,736)+circle(232,944))}
manifest=C/'candidate.json'
if not manifest.exists():
 m={'baseline_commit':'dfcb2bb0','source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'glyphs':[]}
 root=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes())
 deps=set(shapes)
 while True:
  added={n for n,f in cs.items() if any(c.get('base') in deps for c in E.parse(root/f).findall('outline/component'))}-deps
  if not added:break
  deps|=added
 for n in deps:assert '<string>green</string>' not in (root/cs[n]).read_text(),n
 # All direct head wrappers inherit the base's untransformed advance.
 widths={};placements={}
 heads={'fehDotless-ar.init':(272,704),'fehDotless-ar.medi':(272,496),'fehDotless-ar':(720,704),'fehDotless-ar.fina':(720,496),'qafDotless-ar':(640,448),'qafDotless-ar.fina':(320,480)}
 for n in deps-set(shapes):
  comps=E.parse(root/cs[n]).findall('outline/component')
  if not comps or comps[0].get('base') not in heads:continue
  base=comps[0].get('base');assert comps[0].attrib=={'base':base}
  widths[n]=shapes[base][0]
  if len(comps)>1 and comps[1].get('base') in ['dotabove-ar','twodotshorizontalabove-ar','threedotsupabove-ar']:
   x,top=heads[base];dot=comps[1].get('base');cx=232 if dot=='threedotsupabove-ar' else 152;bottom=624 if dot=='threedotsupabove-ar' else 656
   placements[n]={'base':dot,'xOffset':str(x-cx),'yOffset':str(top+48-bottom)}
 for n in sorted(shapes.keys()|widths.keys()):
  p=root/cs[n];rel=p.relative_to(R);old=p.read_text();new=old
  for master in ['Regular','Bold']:
   src=R/str(rel).replace('-Bold','-'+master);dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
  assert '<string>green</string>' not in old
  if n in shapes:
   width,pts=shapes[n];assert any(f'<string>{color}</string>' in old for color in ['red','purple'])
   it=iter(pts)
   def point(mat):
    x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
   new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None,n
   new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
  else:width=widths[n]
  if n=='qafDotless-ar.fina':
   for x,y in [(560,-8),(560,184)]:new=new.replace(f'<point x="{x}" y="{y}" type="curve" smooth="yes"/>',f'<point x="{x}" y="{y}" type="curve"/>').replace(f'<point x="{x}" y="{y}" type="line" smooth="yes"/>',f'<point x="{x}" y="{y}" type="line"/>')
  if n in placements:
   attrs=placements[n];new=re.sub(r'<component base="'+attrs['base']+r'"[^>]*/>',lambda _: '<component '+' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>',new)
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  if new==old:continue
  reg=E.parse(R/str(rel).replace('-Bold','-Regular'));draft=E.fromstring(new)
  assert [[x.get('type') for x in co] for co in reg.findall('outline/contour')]==[[x.get('type') for x in co] for co in draft.findall('outline/contour')],n
  dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
  m['glyphs'].append(dict(name=n,path=str(rel),drawing=n in shapes,before_sha256=sha(p),candidate_sha256=sha(dst)))
 m['placements']=placements;m['inherited_bold_glyphs']=sorted(deps-set(shapes));manifest.write_text(json.dumps(m,indent=2)+'\n')
 (C/'assets').mkdir(exist_ok=True);shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',C/'assets/before.ttf')
 print('Prepared',len(shapes),'outlines;',len(m['glyphs']),'source files;',len(deps),'total glyphs in closure; Regular unchanged.')
if '--apply' in sys.argv:
 m=json.loads(manifest.read_text());assert not (C/'applied.json').exists()
 for p,h in m['source_hashes'].items():assert sha(R/p)==h,('external source edit',p)
 for g in m['glyphs']:assert sha(C/'candidate-sources'/g['path'])==g['candidate_sha256']
 for g in m['glyphs']:(R/g['path']).write_bytes((C/'candidate-sources'/g['path']).read_bytes())
 (C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied exact hash-checked candidate.')
