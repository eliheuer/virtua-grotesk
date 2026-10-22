from pathlib import Path
import json,shutil,plistlib,unicodedata
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
C=Path('agent-proofs/cases/latin-001/batches/50-fractions-assessment');d=json.loads((C/'assessment.json').read_text());out={'unicode_version':unicodedata.unidata_version,'decompositions':{c:unicodedata.decomposition(c) for c in '¼½¾⁄/∕'},'feature_default_subset_policy':{},'subsets_mode_equivalence':{},'reference_bounds':[]}
from fontTools.subset import Options
out['feature_default_subset_policy']=Options().layout_features
for family in ['virtua','rubik']:
 t=TTFont(C/'assets'/f'{family}.ttf');upm=t['head'].unitsPerEm
 out[family+'_feature_lookup_indices']={tag:sorted({i for r in t['GSUB'].table.FeatureList.FeatureRecord if r.FeatureTag==tag for i in r.Feature.LookupListIndex}) for tag in ['frac','numr','dnom','sups','tnum']}
 for w in [400,700]:
  gs=t.getGlyphSet(location={'wght':w});names={g['glyph'] for row in d['shaping'] if row['font']==family and row['weight']==w for glyphs in row['modes'].values() for g in glyphs if g['glyph']!='.notdef'}
  for name in sorted(names):
   if not any(x in name for x in ['numr','dnom','superior','fraction','slash','quarter','half']):continue
   p=BoundsPen(gs);gs[name].draw(p);out['reference_bounds'].append({'font':family,'weight':w,'glyph':name,'advance_1024':gs[name].width*1024/upm,'bounds_1024':[round(x*1024/upm,3) for x in p.bounds] if p.bounds else None})
 for policy in ['default','fraction-features','all']:
  eq={m:0 for m in d['modes']};total=0
  for row in d['subsets']:
   if row['font']!=family or row['policy']!=policy:continue
   full=next((s for s in d['shaping'] if s['font']==family and s['weight']==row['weight'] and s['text']==row['text']),None)
   if full is None:continue
   total+=1
   for m in eq:eq[m]+=row['modes'][m]==full['modes'][m]
  out['subsets_mode_equivalence'][family+' '+policy]={'samples':total,'equal_counts':eq}
for m in ['Regular','Bold']:
 root=Path(f'sources/VirtuaGrotesk-{m}.ufo/glyphs');idx=plistlib.loads((root/'contents.plist').read_bytes());dst=C/'before-sources'/m;dst.mkdir(parents=True,exist_ok=True)
 for n in ['one','two','three','four','slash','backslash','onesuperior','twosuperior','threesuperior','foursuperior']:
  shutil.copy2(root/idx[n],dst/idx[n])
(C/'fraction-details.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
# Extra bounded probes distinguish HarfBuzz's U2044 treatment from global frac.
import uharfbuzz as hb,hashlib,xml.etree.ElementTree as E
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
out['fraction_slash_feature_probes']=[];out['rubik_superior_numerator_identity']=[]
def sh(data,t,w,text,feat):
 f=hb.Font(hb.Face(data));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,feat)
 return [{'glyph':t.getGlyphName(i.codepoint),'advance':p.x_advance,'x':p.x_offset,'y':p.y_offset} for i,p in zip(b.glyph_infos,b.glyph_positions)]
for family in ['virtua','rubik']:
 path=C/'assets'/f'{family}.ttf';data=path.read_bytes();t=TTFont(path)
 for w in [400,475,550,625,700]:
  out['fraction_slash_feature_probes'].append({'font':family,'weight':w,'text':'1⁄4','modes':{label:sh(data,t,w,'1⁄4',feat) for label,feat in {'default':{},'frac_off':{'frac':0},'all_three_off':{'frac':0,'numr':0,'dnom':0}}.items()}})
 if family=='rubik':
  cm=t.getBestCmap()
  for w in [400,475,550,625,700]:
   gs=t.getGlyphSet(location={'wght':w})
   for char,num in zip('⁰¹²³⁴⁵⁶⁷⁸⁹','zero one two three four five six seven eight nine'.split()):
    p=DecomposingRecordingPen(gs);q=DecomposingRecordingPen(gs);gs[cm[ord(char)]].draw(p);gs[num+'.numr'].draw(q)
    out['rubik_superior_numerator_identity'].append({'weight':w,'character':char,'outline_equal':p.value==q.value,'advance_equal':gs[cm[ord(char)]].width==gs[num+'.numr'].width})
 # Every subset mode, including the extra 12/345-only subset, compared to its full font.
 for policy in ['default','fraction-features','all']:
  eq={m:0 for m in d['modes']};total=0
  for row in d['subsets']:
   if row['font']!=family or row['policy']!=policy:continue
   total+=1
   for m,feat in d['modes'].items():eq[m]+=row['modes'][m]==sh(data,t,row['weight'],row['text'],feat)
  out['subsets_mode_equivalence'][family+' '+policy]={'samples':total,'equal_counts':eq}
out['diagonal_reference_guards']={}
for m in ['Regular','Bold']:
 root=Path(f'sources/VirtuaGrotesk-{m}.ufo/glyphs');idx=plistlib.loads((root/'contents.plist').read_bytes());rr={n:E.parse(root/f).getroot() for n,f in idx.items()};deps={n:{v.get('base') for v in r.findall('outline/component')} for n,r in rr.items()};closure={'X','x','seven'}
 while True:
  more=closure|{n for n,v in deps.items() if v&closure}
  if more==closure:break
  closure=more
 assert not closure & set(d['families'][m]['arabic_reserved'])
 refs={}
 for n in ['X','x','seven']:
  r=rr[n];lib=plistlib.loads(b'<plist>'+E.tostring(r.find('lib/dict'))+b'</plist>');refs[n]={'label':lib.get('com.runebender.markLabel'),'rgba':lib.get('public.markColor'),'sha256':hashlib.sha256((root/idx[n]).read_bytes()).hexdigest()};shutil.copy2(root/idx[n],C/'before-sources'/m/idx[n])
 out['diagonal_reference_guards'][m]={'references':refs,'reverse_closure':sorted(closure),'arabic_intersection':[]}
(C/'fraction-details.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('numr/superior exact',sum(x['outline_equal'] and x['advance_equal'] for x in out['rubik_superior_numerator_identity']),'/50')
print('off probes',out['fraction_slash_feature_probes'][-5])
print('diagonal grades',out['diagonal_reference_guards'])
