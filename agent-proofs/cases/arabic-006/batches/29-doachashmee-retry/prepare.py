"""Separate four-form study. Never writes active sources; green exception pending."""
from pathlib import Path
import re,json,hashlib,shutil,tempfile,plistlib,xml.etree.ElementTree as E,subprocess
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.pens.recordingPen import RecordingPointPen
R=Path.cwd();C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=C/'candidate.json'
if manifest.exists():m=json.loads(manifest.read_text());scratch=Path(m['scratch'])
else:
 scratch=Path(tempfile.mkdtemp(prefix='virtua-heh-retry-',dir='/tmp'));(scratch/'sources').mkdir()
 for p in R.glob('sources/VirtuaGrotesk-*.ufo'):shutil.copytree(p,scratch/'sources'/p.name)
 shutil.copy2(R/'sources/VirtuaGrotesk.designspace',scratch/'sources/VirtuaGrotesk.designspace')
 shutil.copy2(R/'sources/config.yaml',scratch/'sources/config.yaml')
 m={'status':'scratch only; no approval to replace green Regular medial','scratch':str(scratch),'source_hashes':{str(p.relative_to(R)):sha(p) for p in R.glob('sources/VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':{},'glyphs':[],'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()}
 for master in ['Regular','Bold']:
  root=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes());names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
  while True:
   add={x.get('base') for n in names for x in E.parse(root/cs[n]).findall('outline/component')}-names
   if not add:break
   names|=add
  for n in names:m['reserved_beh_hashes'][str((root/cs[n]).relative_to(R))]=sha(root/cs[n])
 assert len(m['reserved_beh_hashes'])==18
m['glyphs']=[]
def outline(paths):
 out=[]
 for index,ops in enumerate(paths):
  a=AreaPen()
  for op,coords in ops:getattr(a,op)(*coords)
  p=RecordingPointPen();s=SegmentToPointPen(p,guessSmooth=True)
  dest=ReverseContourPen(s) if (a.value>0)!=(index==0) else s
  for op,coords in ops:getattr(dest,op)(*coords)
  lines=['\t\t<contour>']
  for op,args,kwargs in p.value:
   if op!='addPoint':continue
   (x,y),typ,smooth,name=args
   attrs=f'x="{int(x)}" y="{int(y)}"'+(f' type="{typ}"' if typ else '')+(' smooth="yes"' if smooth else '')
   lines.append('\t\t\t<point '+attrs+'/>')
  lines.append('\t\t</contour>');out.append('\n'.join(lines))
 return '\t<outline>\n'+'\n'.join(out)+'\n\t</outline>'
def path(start,seq):
 out=[('moveTo',(start,))]
 for item in seq:out.append(('lineTo' if len(item)==1 else 'curveTo',tuple(item)))
 out.append(('closePath',()));return out
def ellipse(x0,y0,x1,y1,hx,hy):
 cx=(x0+x1)//2;cy=(y0+y1)//2
 return path((cx,y0),[[(cx-hx,y0),(x0,cy-hy),(x0,cy)],[(x0,cy+hy),(cx-hx,y1),(cx,y1)],[(cx+hx,y1),(x1,cy+hy),(x1,cy)],[(x1,cy-hy),(cx+hx,y0),(cx,y0)]])
for master in ['Regular','Bold']:
 bold=master=='Bold';bar=176 if bold else 104
 # The two-eye construction: a bounded left loop under an angled returning arm.
 # Counter control follows the tall inner oval of green o, not a round disk.
 for form in ['', '.init','.medi','.fina']:
  n='hehDoachashmee-ar'+form;root=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cs=plistlib.loads((root/'contents.plist').read_bytes());src=root/cs[n];rel=src.relative_to(R)
  consumers=[a for a,f in cs.items() if any(co.get('base')==n for co in E.parse(root/f).findall('outline/component'))];assert not consumers,consumers
  assert str(rel) not in m['reserved_beh_hashes']
  if form in ['', '.init']:
   left=32 if not form else -16
   outer=path((left,0),[[(left,bar)],[(48,bar)],[(64,bar+16)],[(64,272)],[(64,400),(144,496),(288,496)],[(248,528)],[(248,544)],[(304,624)],[(320,624)],[(664,384)],[(744,328),(784,264),(784,176)],[(784,48),(696,0),(568,0)],[(left,0)]])
   if bold:
    eye=ellipse(240,144,384,368,40,64)
    second=path((480,144),[[(528,184),(552,256),(520,328)],[(576,288)],[(632,248),(648,224),(648,192)],[(648,160),(632,144),(568,144)],[(480,144)]])
   else:
    eye=ellipse(160,104,400,408,64,88)
    second=path((432,104),[[(488,168),(504,304),(440,408)],[(608,296)],[(656,264),(696,232),(696,176)],[(696,128),(664,104),(568,104)],[(432,104)]])
   paths=[outer,eye,second];width=816
  else:
   # Draft matching topology in both masters; Regular medial is protected and
   # this experiment remains in scratch until a named approval, if wanted.
   if bold:
    outer=path((0,0),[[(48,0)],[(64,-16)],[(64,-160),(176,-288),(336,-288)],[(456,-288),(544,-208),(544,-96)],[(544,-16)],[(560,0)],[(608,0)],[(608,176)],[(544,176)],[(528,192)],[(528,304)],[(528,416),(448,496),(352,496)],[(248,496),(144,400),(104,288)],[(64,176)],[(0,176)],[(-16,160)],[(-16,16)],[(0,0)]])
    upper=path((248,176),[[(240,184)],[(256,264),(280,368),(344,368)],[(384,368),(400,328),(400,288)],[(400,224),(360,176),(288,176)],[(248,176)]])
    lower=path((240,0),[[(224,-16)],[(224,-96),(288,-144),(336,-144)],[(384,-144),(400,-96),(400,-64)],[(400,-32),(384,0),(336,0)],[(240,0)]])
   else:
    outer=path((0,0),[[(48,0)],[(64,-16)],[(64,-144),(152,-256),(288,-256)],[(392,-256),(464,-192),(464,-96)],[(464,-16)],[(480,0)],[(528,0)],[(528,104)],[(464,104)],[(448,120)],[(448,272)],[(448,384),(376,448),(280,448)],[(168,448),(112,360),(88,232)],[(64,104)],[(0,104)],[(-16,88)],[(-16,16)],[(0,0)]])
    upper=path((168,104),[[(160,112)],[(176,232),(216,360),(280,360)],[(312,360),(360,328),(360,272)],[(360,200),(280,104),(216,104)],[(168,104)]])
    lower=path((168,0),[[(152,-16)],[(152,-104),(224,-168),(288,-168)],[(344,-168),(376,-120),(376,-80)],[(376,-40),(344,0),(288,0)],[(168,0)]])
   # Final has the same two-loop skeleton with its small exiting tail retained.
   paths=[outer,upper,lower];width=608 if bold else 528
  old=src.read_text();new=re.sub(r'\t<outline>.*?\t</outline>',lambda _:outline(paths),old,flags=re.S)
  new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
  new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  for stage,text in [('before-sources',old),('candidate-sources',new)]:
   dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True)
   if stage=='before-sources' and dst.exists():assert dst.read_text()==old
   else:dst.write_text(text)
  (scratch/rel).write_text(new)
  m['glyphs'].append({'name':n,'master':master,'path':str(rel),'before_sha256':sha(src),'candidate_sha256':sha(scratch/rel),'green_exception_required':master=='Regular' and form=='.medi'})
for rel,h in m['source_hashes'].items():assert sha(R/rel)==h,rel
manifest.write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir(exist_ok=True)
shutil.copy2(C.parent/'27-doachashmee/assets/after.ttf',C/'assets/before.ttf')
print(scratch)
