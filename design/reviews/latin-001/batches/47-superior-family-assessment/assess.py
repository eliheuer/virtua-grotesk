"""Read-only complete-family/feature assessment; no candidate fonts or source changes."""
from pathlib import Path
import json,hashlib,shutil,subprocess,plistlib,xml.etree.ElementTree as E,io,unicodedata
from collections import Counter
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools import subset
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];A=C/'assets';D=R/'out/review-latin-d2513094/batch47'
for p in [A,D,C/'browser']:p.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
fonts={str(p.relative_to(R)):sha(p) for p in (R/'fonts').rglob('*.ttf')}
assert fonts==json.loads((C.parent/'46-superior-eight/final-identity.json').read_text())['active_fonts']
if (C/'assessment.json').exists():assert sources==json.loads((C/'assessment.json').read_text())['source_hashes']
for n,p in [('virtua',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parent/'46-superior-eight/assets/rubik.ttf')]:
 shutil.copy2(p,A/f'{n}.ttf');shutil.copy2(p,D/f'{n}.ttf')
names='zero one two three four five six seven eight nine'.split();sup='⁰¹²³⁴⁵⁶⁷⁸⁹';families={}
for m in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{p.get('base') for p in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  more=arab|set().union(*(deps[n] for n in arab))
  if more==arab:break
  arab=more
 closure=set(names+[n+'.tf' for n in names]+[n+'superior' for n in names])
 while True:
  more=closure|{n for n,v in deps.items() if v&closure}
  if more==closure:break
  closure=more
 grades={};green={}
 for n,r in rr.items():
  x=r.find('lib/dict');lib=plistlib.loads(b'<plist>'+E.tostring(x)+b'</plist>') if x is not None else {};rgba=list(map(float,lib.get('public.markColor','0,0,0,0').split(',')))
  if n in closure:grades[n]={'sha256':sha(d/idx[n]),'label':lib.get('com.runebender.markLabel'),'rgba':rgba,'advance':r.find('advance').get('width')}
  if lib.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
 assert not closure&arab
 families[m]={'reverse_closure':sorted(closure),'intersection_with_arabic':sorted(closure&arab),'grades':grades,'green_hashes':green,'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)}}

def shape(data,t,w,text,feat):
 f=hb.Font(hb.Face(data));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,feat)
 return [{'glyph':t.getGlyphName(i.codepoint),'advance':p.x_advance,'x':p.x_offset,'y':p.y_offset} for i,p in zip(b.glyph_infos,b.glyph_positions)]
modes={'default':{},'sups':{'sups':1},'tnum':{'tnum':1},'tnum_sups':{'tnum':1,'sups':1},'pnum_sups':{'pnum':1,'sups':1},'numr':{'numr':1},'frac':{'frac':1},'subs':{'subs':1}}
texts=['0123456789',sup,'101 202 303 404 505 606 707 808 909','x12 H34 fi56','1/2 3/4','1\u0301 2\u0327']
tests=[];bounds=[];metadata={};subsets=[]
for n in ['virtua','rubik']:
 path=A/f'{n}.ttf';data=path.read_bytes();t=TTFont(path);cm=t.getBestCmap();gs=t['GSUB'].table
 metadata[n]={'sha256':sha(path),'upm':t['head'].unitsPerEm,'features':{r.FeatureTag:r.Feature.LookupListIndex for r in gs.FeatureList.FeatureRecord},'cmap':{f'U+{ord(c):04X}':cm.get(ord(c)) for c in sup}}
 for w in [400,475,550,625,700]:
  glyphs=t.getGlyphSet(location={'wght':w})
  for c in '0123456789'+sup:
   name=cm[ord(c)];pen=BoundsPen(glyphs);glyphs[name].draw(pen);bounds.append({'font':n,'weight':w,'character':c,'glyph':name,'advance':glyphs[name].width,'bounds':pen.bounds,'normalized_1024_bounds':[v*1024/t['head'].unitsPerEm for v in pen.bounds]})
  for text in texts:
   results={label:shape(data,t,w,text,f) for label,f in modes.items()}
   if n=='virtua':assert results['default']==results['sups']==results['numr']==results['frac']==results['subs'];assert results['tnum']==results['tnum_sups']
   assert not any(g['glyph']=='.notdef' for row in results.values() for g in row)
   tests.append({'font':n,'weight':w,'text':text,'modes':results})
  if n=='rubik':
   assert shape(data,t,w,'0123456789',{'sups':1})==shape(data,t,w,sup,{})
 for text in ['0123456789',sup,'1/2 3/4']:
  for policy in ['default','sups-tnum','all']:
   f=TTFont(path);o=subset.Options();o.glyph_names=True
   if policy=='sups-tnum':o.layout_features+=['sups','tnum']
   if policy=='all':o.layout_features=['*']
   ss=subset.Subsetter(options=o);ss.populate(text=text);ss.subset(f);buf=io.BytesIO();f.save(buf);sd=buf.getvalue();f=TTFont(io.BytesIO(sd))
   for w in [400,475,550,625,700]:
    results={label:shape(sd,f,w,text,feat) for label,feat in modes.items()}
    assert results['default']==shape(data,t,w,text,{})
    subsets.append({'font':n,'text':text,'weight':w,'policy':policy,'features_retained':o.layout_features,'modes':results})
report={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source_hashes':sources,'active_fonts':fonts,'families':families,'fonts':metadata,'harfbuzz':hb.version_string(),'modes':modes,'shaping':tests,'bounds':bounds,'subsets':subsets,'normalization':{'NFD':unicodedata.normalize('NFD',sup),'NFKD':unicodedata.normalize('NFKD',sup)},'limits':'Read-only. No feature or drawing applied. Encoded coverage is distinct from OpenType sups and serving sets.'}
(C/'assessment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(sources),'sources;',len(tests),'full-font cases x',len(modes),'modes;',len(subsets),'subset cases x',len(modes),'modes')
for n in metadata:
 print(n,metadata[n]['features'].keys())
 for mode in ['default','sups','tnum_sups']:
  row=next(x for x in tests if x['font']==n and x['weight']==400 and x['text']=='0123456789');print(mode,[(x['glyph'],x['advance']) for x in row['modes'][mode]])
