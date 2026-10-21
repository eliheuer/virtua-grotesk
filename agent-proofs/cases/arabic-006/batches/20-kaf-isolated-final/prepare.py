"""Repair two Bold Kaf forms; all Regular and Beh sources remain byte-identical."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re,shutil,subprocess
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'applied.json').exists()
roots={};contents={};reserved={}
for master in ['Regular','Bold']:
 rr=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cc=plistlib.loads((rr/'contents.plist').read_bytes());roots[master]=rr;contents[master]=cc
 names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in names for co in E.parse(rr/cc[n]).findall('outline/component')}-names
  if not add:break
  names|=add
 for n in names:reserved[str((rr/cc[n]).relative_to(R))]=sha(rr/cc[n])
rr=roots['Bold'];cc=contents['Bold'];drawings={'kaf-ar','kaf-ar.fina'}
assert not [(n,co.get('base')) for n,f in cc.items() for co in E.parse(rr/f).findall('outline/component') if co.get('base') in drawings]
iso=[(800,96),(800,240),(800,752),(784,768),(656,768),(640,752),(640,240),(640,200),(616,176),(576,176),(224,176),(184,176),(160,200),(160,240),(160,336),(144,352),(16,352),(0,336),(0,240),(0,96),(80,0),(224,0),(560,0),(704,0)]
final=[(896,0),(896,176),(840,176),(800,200),(800,240),(800,752),(784,768),(656,768),(640,752),(640,240),(640,200),(616,176),(576,176),(224,176),(184,176),(160,200),(160,240),(160,336),(144,352),(16,352),(0,336),(0,240),(0,96),(80,0),(224,0),(576,0),(640,0),(720,0),(784,0),(800,0),(832,0),(864,0)]
sign=[(312, 304), (448, 304), (504, 304), (536, 336), (536, 392), (536, 448), (504, 480), (448, 480), (392, 480), (376, 480), (368, 488), (368, 504), (368, 520), (376, 528), (392, 528), (496, 528), (512, 544), (512, 576), (496, 592), (384, 592), (328, 592), (296, 560), (296, 504), (296, 448), (328, 416), (384, 416), (440, 416), (456, 416), (464, 408), (464, 392), (464, 376), (456, 368), (440, 368), (312, 368), (296, 352), (296, 320)]
coords={'kaf-ar':iso+sign,'kaf-ar.fina':final+sign};widths={'kaf-ar':864,'kaf-ar.fina':896}
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':[],'placements':{}}
for n in sorted(drawings):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved and '<string>red</string>' in old
 it=iter(coords[n])
 def point(mat):
  x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
 new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,old);assert next(it,None) is None
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{widths[n]}"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);b=E.parse(roots['Regular']/contents['Regular'][n]);assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=True,before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'19-tah-zah/assets/after.ttf',C/'assets/before.ttf')
for p,h in m['source_hashes'].items():assert sha(R/p)==h
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared 2 Bold files; preserved',len(reserved),'Beh files.')
