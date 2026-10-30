"""Bounded Bold Sad/Dad family; preserve Regular geometry and Beh."""
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
rr=roots['Bold'];cc=contents['Bold'];drawings={'sad-ar'+s for s in ['', '.init','.medi','.fina']};deps=set(drawings)
while True:
 add={n for n,f in cc.items() if any(co.get('base') in deps for co in E.parse(rr/f).findall('outline/component'))}-deps
 if not add:break
 deps|=add
assert deps=={n+s for n in ['sad-ar','dad-ar'] for s in ['', '.init','.medi','.fina']},deps
init=[(312,176),(240,176),(232,184),(232,368),(216,384),(88,384),(72,368),(72,184),(64,176),(0,176),(-16,160),(-16,16),(0,0),(736,0),(880,0),(960,80),(960,224),(960,368),(880,448),(736,448),(544,448),(400,448),(320,368),(320,224),(320,184)]
counter=[(480,168),(480,224),(480,264),(504,288),(544,288),(736,288),(776,288),(800,264),(800,224),(800,184),(776,160),(736,160),(488,160)]
medi=init[:14]+[(784,0),(816,0),(848,0),(864,0),(880,0),(896,0),(912,0),(928,0),(1056,0),(1056,176),(976,176),(960,192),(960,224),(960,368),(880,448),(736,448),(544,448),(400,448),(320,368),(320,224),(320,184)]
# Shared head translated 568 units in the bowl forms.
shift=lambda ps:[(x+568,y) for x,y in ps]
iso=[(880,176),(808,176),(800,184),(800,368),(784,384),(656,384),(640,368),(640,24),(640,-48),(592,-96),(480,-96),(288,-96),(248,-96),(224,-48),(224,32),(224,160),(208,176),(80,176),(64,160),(64,32),(64,-144),(144,-256),(288,-256),(480,-256),(672,-256),(800,-192),(800,-24),(800,-16),(800,-8),(808,0)]+shift(init[13:])
final=[(64,32),(64,-144),(176,-256),(320,-256),(480,-256),(672,-256),(800,-192),(800,-16),(800,-8),(808,0)]+shift(medi[13:27])+shift(medi[27:])+[(880,176),(808,176),(800,184),(800,368),(784,384),(656,384),(640,368),(640,48),(640,-48),(592,-96),(480,-96),(352,-96),(272,-96),(224,-64),(224,32),(224,160),(208,176),(80,176),(64,160)]
# Above concatenation includes medial's shoulder end; final has one extra inner-floor point.
coords={'sad-ar.init':init+counter,'sad-ar.medi':medi+counter,'sad-ar':iso+shift(counter),'sad-ar.fina':final+[(1056,160),(1048,168)]+shift(counter[1:12])+[(1056,160)]}
# Final counter order differs: floor, inside cut, then the common head, ending at floor.
placements={n:{'base':'dotabove-ar','xOffset':str(488 if n.endswith(('.init','.medi')) else 1056),'yOffset':'-128'} for n in deps-drawings}
widths={'.init':1024,'.medi':1056,'.fina':1624,'':1592}
m={'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':reserved,'glyphs':[],'inherited_bold_glyphs':sorted(deps-drawings),'placements':placements}
for n in sorted(deps):
 p=rr/cc[n];old=p.read_text();rel=str(p.relative_to(R));assert rel not in reserved
 assert all(x not in old for x in ['<string>green</string>','<string>0,1,0,1</string>','<string>0.09,0.72,0.44,1</string>'])
 new=old
 if n=='sad-ar':
  # Two extra on-curve points on the Regular's top edge preserve its exact drawing.
  new=new.replace('<point x="192" y="176" type="line"/>','<point x="192" y="176" type="line"/>\n\t\t\t<point x="176" y="176" type="line"/>\n\t\t\t<point x="44" y="176" type="line"/>')
 if n in drawings:
  it=iter(coords[n])
  def point(mat):
   x,y=next(it);return f'<point x="{x}" y="{y}"'+mat[1]
  new=re.sub(r'<point x="[^"]+" y="[^"]+"([^>]*>)',point,new);assert next(it,None) is None
 else:
  co=placements[n];new=re.sub(r'<component base="'+co['base']+r'"[^>]*/>',f'<component base="{co["base"]}" xOffset="{co["xOffset"]}" yOffset="{co["yOffset"]}"/>',new)
 width=widths[next((x for x in ['.init','.medi','.fina'] if n.endswith(x)), '')]
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 new=new.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 a=E.fromstring(new);reg=(roots['Regular']/contents['Regular'][n]).read_text()
 if n=='sad-ar':reg=reg.replace('<point x="156" y="150" type="line"/>','<point x="156" y="150" type="line"/>\n\t\t\t<point x="140" y="150" type="line"/>\n\t\t\t<point x="80" y="150" type="line"/>')
 b=E.ElementTree(E.fromstring(reg));assert [[p.get('type') for p in c] for c in a.findall('.//contour')]==[[p.get('type') for p in c] for c in b.findall('.//contour')]
 for master in roots:
  src=roots[master]/contents[master][n];dst=C/'before-sources'/src.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Bold',drawing=n in drawings,before_sha256=sha(p),candidate_sha256=sha(dst)))
# Exact geometry-neutral Regular insertion and wrapper metrics repairs.
for n in ['sad-ar','dad-ar','dad-ar.init','dad-ar.medi','dad-ar.fina']:
 p=roots['Regular']/contents['Regular'][n];rel=str(p.relative_to(R));old=p.read_text();new=old
 assert '<string>orange</string>' in old and rel not in reserved
 if n=='sad-ar':
  new=new.replace('<point x="156" y="150" type="line"/>','<point x="156" y="150" type="line"/>\n\t\t\t<point x="140" y="150" type="line"/>\n\t\t\t<point x="80" y="150" type="line"/>')
 else:
  base=E.fromstring(old).find('outline/component').get('base')
  width=E.parse(roots['Regular']/contents['Regular'][base]).find('advance').get('width')
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 dst=C/'candidate-sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(new)
 m['glyphs'].append(dict(name=n,path=rel,master='Regular',drawing=False,metrics_only=n!='sad-ar',collinear_only=n=='sad-ar',before_sha256=sha(p),candidate_sha256=sha(dst)))
(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'17-seen-bowls/assets/after.ttf',C/'assets/before.ttf')
# Recheck entire source baseline, including inherited green and manual sources.
for p,h in m['source_hashes'].items():assert sha(R/p)==h
# Application follows candidate geometry checks.
(C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared',len(m['glyphs']),'files; preserved',len(reserved),'Beh files.')
