"""Read-only micro-sign compatibility, donor closure and reference assessment."""
from pathlib import Path
import hashlib,json,shutil,subprocess,plistlib,xml.etree.ElementTree as E,unicodedata as U,io
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools import subset
from defcon import Font
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];A=C/'assets';D=R/'out/review-latin-d2513094/batch48'
for p in [A,D,C/'browser']:p.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and not {'archive','instance_ufos'}.intersection(p.parts)}
active={str(p.relative_to(R)):sha(p) for p in (R/'fonts').rglob('*.ttf')}
assert active==json.loads((C.parent/'46-superior-eight/final-identity.json').read_text())['active_fonts']
if (C/'assessment.json').exists():assert sources==json.loads((C/'assessment.json').read_text())['source_hashes']
for n,p in [('virtua',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parent/'46-superior-eight/assets/rubik.ttf')]:shutil.copy2(p,A/f'{n}.ttf');shutil.copy2(p,D/f'{n}.ttf')
masters={}
for m in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{m}.ufo';d=root/'glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};font=Font(root);deps={n:{p.get('base') for p in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  more=arab|set().union(*(deps[n] for n in arab))
  if more==arab:break
  arab=more
 consumers={'u','p'}
 while True:
  more=consumers|{n for n,v in deps.items() if v&consumers}
  if more==consumers:break
  consumers=more
 green={};donors={}
 for n,r in rr.items():
  lib=dict(font[n].lib);rgba=list(map(float,lib.get('public.markColor','0,0,0,0').split(',')))
  if lib.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
  if n in ['u','p']:
   g=font[n];donors[n]={'grade':lib,'hash':sha(d/idx[n]),'advance':g.width,'bounds':g.bounds,'anchors':[{k:a[k] for k in ['name','x','y']} for a in g.anchors],'contours':[[{'x':p.x,'y':p.y,'type':p.segmentType,'smooth':p.smooth} for p in cc] for cc in g]}
   target=C/'donor-sources'/m/idx[n];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(d/idx[n],target)
 assert not consumers&arab
 masters[m]={'donors':donors,'reverse_closure':sorted(consumers),'arabic_intersection':sorted(consumers&arab),'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green_hashes':green,'micro_mu_candidates':[n for n,r in rr.items() if n.lower() in ['mu','micro','microcomb','uni00b5','uni03bc'] or any(int(u.get('hex'),16) in [0xb5,0x3bc] for u in r.findall('unicode'))]}
def shape(data,t,w,text):
 f=hb.Font(hb.Face(data));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b)
 return [{'glyph':t.getGlyphName(i.codepoint),'advance':p.x_advance,'x':p.x_offset,'y':p.y_offset} for i,p in zip(b.glyph_infos,b.glyph_positions)]
texts=['µ','μ','µm µg µs µF','10 µm 25 µg','10 μm 25 μg','µ\u0301 µ\u0327','u p µ μ'];reports=[];subsets=[];bounds=[];fonts={}
for n in ['virtua','rubik']:
 path=A/f'{n}.ttf';data=path.read_bytes();t=TTFont(path);cm=t.getBestCmap();fonts[n]={'sha256':sha(path),'upm':t['head'].unitsPerEm,'cmap':{f'U+{cp:04X}':cm.get(cp) for cp in [0xb5,0x3bc,0x39c]}}
 for w in [400,475,550,625,700]:
  gs=t.getGlyphSet(location={'wght':w})
  for c in 'upµμ':
   name=cm.get(ord(c))
   if name:
    pen=BoundsPen(gs);gs[name].draw(pen);bounds.append({'font':n,'weight':w,'character':c,'glyph':name,'advance':gs[name].width,'bounds':pen.bounds,'normalized_1024_bounds':[v*1024/t['head'].unitsPerEm for v in pen.bounds]})
  for text in texts:
   results={mode:shape(data,t,w,transform(text)) for mode,transform in [('raw',lambda s:s),('NFD',lambda s:U.normalize('NFD',s)),('NFKD',lambda s:U.normalize('NFKD',s)),('casefold',lambda s:s.casefold())]}
   reports.append({'font':n,'weight':w,'text':text,'modes':results})
 for text in ['10 µm','10 μm','µ\u0301 µ\u0327']:
  f=TTFont(path);opts=subset.Options();opts.glyph_names=True;ss=subset.Subsetter(options=opts);ss.populate(text=text);ss.subset(f);buf=io.BytesIO();f.save(buf);sd=buf.getvalue();sf=TTFont(io.BytesIO(sd))
  for w in [400,475,550,625,700]:
   row=shape(sd,sf,w,text);assert row==shape(data,t,w,text);subsets.append({'font':n,'weight':w,'text':text,'result':row,'matches_full':True})
report={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':sources,'active_fonts':active,'masters':masters,'fonts':fonts,'shaping':reports,'subsets':subsets,'bounds':bounds,'unicode_version':U.unidata_version,'harfbuzz_version':hb.version_string(),'normalization':{c:{'name':U.name(c),'decomposition':U.decomposition(c),'NFD':U.normalize('NFD',c),'NFKD':U.normalize('NFKD',c),'casefold':c.casefold()} for c in 'µμ'},'limits':'Read-only; compatibility mapping is not canonical fallback. No aliases or substitute ordinary u.'}
(C/'assessment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(sources),'unchanged sources;',len(reports),'shaping cases x4 modes;',len(subsets),'subsets;')
print({m:(len(v['reverse_closure']),len(v['arabic_reserved']),len(v['green_hashes'])) for m,v in masters.items()})
