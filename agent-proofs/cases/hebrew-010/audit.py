"""Read-only modern Hebrew marks and adjacent-letter clearance audit; not grading."""
from pathlib import Path
import argparse,hashlib,json,plistlib,xml.etree.ElementTree as E
from itertools import combinations,product
import pathops,uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
C=Path(__file__).resolve().parent;R=C.parents[2];previous=C.parent/'hebrew-009'
e=json.loads((previous/'evidence-v1.json').read_text());paths={k:previous/e['fonts'][k]['path'] for k in ['after','rubik','noto']}
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--font',type=Path);parser.add_argument('--output',type=Path,default=C/'audit.json');args=parser.parse_args()
if args.font:paths['after']=args.font.resolve()
marks=list(range(0x5b0,0x5be))+[0x5bf,0x5c1,0x5c2,0x5c7];letters=list(map(chr,range(0x5d0,0x5eb)))
records=[]
for role,p in paths.items():
 f=TTFont(p);upm=f['head'].unitsPerEm
 for w in [400,700]:
  gs=f.getGlyphSet(location={'wght':w});cm=f.getBestCmap()
  for cp in marks:
   if cp not in cm:continue
   pen=BoundsPen(gs);gs[cm[cp]].draw(pen);b=pen.bounds
   records.append(dict(role=role,weight=w,codepoint=f'U+{cp:04X}',bounds_1024=[round(x*1024/upm,2) for x in b] if b else None))
sources={}
for master in ['Regular','Bold']:
 folder=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';idx={}
 for p in folder.glob('*.glif'):
  root=E.parse(p).getroot()
  for u in root.findall('unicode'):
   cp=int(u.get('hex'),16)
   if cp in marks:
    lib=root.find('lib');d=plistlib.loads(('<plist>'+E.tostring(lib[0],encoding='unicode')+'</plist>').encode()) if lib is not None else {}
    idx[f'U+{cp:04X}']=dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),color=d.get('public.markColor'),label=d.get('com.runebender.markLabel'))
 sources[master]=idx
f=TTFont(paths['after']);h=hb.Font(hb.Face(paths['after'].read_bytes()));collisions=[];checks={};minpair=[]
for w in [400,550,700]:
 h.set_variations({'wght':w});gs=f.getGlyphSet(location={'wght':w});count=0;nearest=[]
 samples=[('pair',a+b) for a,b in product(letters,repeat=2)]
 samples += [('mark',base+chr(cp)) for base in letters for cp in marks if cp not in [0x5c1,0x5c2] or base=='ש']
 samples += [('stack',b+s) for b in letters for s in ['\u05b0\u05bc','\u05b4\u05bc','\u05b7\u05bd','\u05b8\u05bf']]
 samples += [('stack',s) for s in ['שָּׁ','שִּׂ','שְׁ','שָׁ֑','שָׂ֑','בַֽ','בָֽ','בִּ֑']]
 for kind,txt in samples:
  buf=hb.Buffer();buf.add_str(txt);buf.guess_segment_properties();hb.shape(h,buf);shapes=[];cursor=0;gn=[];bb=[]
  for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
   name=f.getGlyphName(info.codepoint);gn.append(name);shape=pathops.Path();gs[name].draw(TransformPen(shape.getPen(),(1,0,0,1,cursor+pos.x_offset,pos.y_offset)));shapes.append(shape);bb.append(shape.bounds);cursor+=pos.x_advance
  for i,j in combinations(range(len(shapes)),2):
   area=abs(pathops.op(shapes[i],shapes[j],pathops.PathOp.INTERSECTION).area)
   if area>.01:collisions.append(dict(weight=w,kind=kind,text=txt,glyphs=[gn[i],gn[j]],area=round(area,3)))
  if kind=='pair' and len(bb)==2:nearest.append(dict(text=txt,bbox_gap=round(bb[1][0]-bb[0][2],2)))
  count+=1
 checks[w]=count;minpair.append(dict(weight=w,closest_by_bbox=sorted(nearest,key=lambda r:r['bbox_gap'])[:12]))
out=dict(fonts={k:dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in paths.items()},marks=records,source_permissions=sources,shaped_sequences=checks,outline_intersections=collisions,spacing_screen=minpair,note='Bounds gaps and outline intersections are diagnostics, not optical spacing grades. Audit does not modify sources.')
args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Shaped sequences',checks,'intersections',len(collisions));print(collisions[:12])
