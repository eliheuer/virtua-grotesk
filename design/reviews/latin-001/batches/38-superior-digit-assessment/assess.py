"""Read-only encoded superior-digit and feature assessment. No candidate fonts."""
from pathlib import Path
import hashlib,json,shutil,subprocess,plistlib,unicodedata as U,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from defcon import Font
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];A=C/'assets';D=R/'out/review-latin-d2513094/batch38'
for p in [A,D,C/'browser']:p.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
if (C/'assessment.json').exists():assert sources==json.loads((C/'assessment.json').read_text())['source_hashes']
for name,p in [('virtua',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parent/'37-currency/assets/rubik.ttf')]:
 shutil.copy2(p,A/(name+'.ttf'));shutil.copy2(p,D/(name+'.ttf'))
assert sha(A/'virtua.ttf')==json.loads((C.parent/'37-currency/final-identity.json').read_text())['active_fonts']['fonts/variable/VirtuaGrotesk[wght].ttf']
masters={}
for m in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{m}.ufo';d=root/'glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};f=Font(root)
 deps={n:{c.get('base') for c in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 consumers={'one','two','three'}
 while True:
  new=consumers|{n for n,dep in deps.items() if dep&consumers}
  if new==consumers:break
  consumers=new
 green={};donors={}
 for n,r in rr.items():
  lib=dict(f[n].lib);rgba=[float(x) for x in lib.get('public.markColor','0,0,0,0').split(',')]
  if lib.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
  if n in consumers:
   g=f[n];donors[n]={'grade':lib,'hash':sha(d/idx[n]),'components':sorted(deps[n]),'advance':g.width,'bounds':g.bounds,'contours':[[{'x':q.x,'y':q.y,'type':q.segmentType,'smooth':q.smooth} for q in c] for c in g]}
   q=C/'donor-sources'/m/idx[n];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(d/idx[n],q)
 masters[m]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green':green,'figure_reverse_closure':donors,'closure_intersects_arabic':sorted(consumers&arab),'superior_name_matches':[n for n in idx if any(s in n.lower() for s in ['superior','sups','numr','numerator','inferior','dnom'])]}
 assert not consumers&arab
fonts={};tests=[];bounds=[]
def shape(path,w,text,features):
 t=TTFont(path);f=hb.Font(hb.Face(path.read_bytes()));f.set_variations({'wght':w});b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,features)
 return [{'glyph':t.getGlyphName(i.codepoint),'cluster':i.cluster,'advance':p.x_advance,'x':p.x_offset,'y':p.y_offset} for i,p in zip(b.glyph_infos,b.glyph_positions)]
for name in ['virtua','rubik']:
 p=A/(name+'.ttf');t=TTFont(p);cm=t.getBestCmap();tags=sorted({r.FeatureTag for r in t['GSUB'].table.FeatureList.FeatureRecord})
 fonts[name]={'sha256':sha(p),'upm':t['head'].unitsPerEm,'cmap':{f'U+{cp:04X}':cm.get(cp) for cp in [0xb9,0xb2,0xb3,0x2070,0x2074,0x2081]},'GSUB_tags':tags}
 for w in [400,475,550,625,700]:
  gs=t.getGlyphSet(location={'wght':w})
  for cp in [49,50,51,0xb9,0xb2,0xb3]:
   n=cm.get(cp)
   if n:
    pen=BoundsPen(gs);gs[n].draw(pen);bounds.append({'font':name,'weight':w,'cp':cp,'glyph':n,'advance':gs[n].width,'bounds':pen.bounds,'normalized_1024_bounds':[v*1024/t['head'].unitsPerEm for v in pen.bounds]})
  for text in ['¹²³','x¹ x² x³','10¹ 10² 10³','123','x123','123/123']:
   modes={label:shape(p,w,text,feat) for label,feat in [('default',{}),('sups',{'sups':1}),('tnum',{'tnum':1}),('numr',{'numr':1})]}
   if name=='virtua':assert modes['default']==modes['sups']==modes['numr']
   if '¹' in text:assert any(q['glyph']=='.notdef' for q in modes['default'])==(name=='virtua')
   tests.append({'font':name,'weight':w,'text':text,'modes':modes})
normalization={c:{'name':U.name(c),'decomposition':U.decomposition(c),'NFD':U.normalize('NFD',c),'NFKD':U.normalize('NFKD',c)} for c in '¹²³'}
assert all(v['NFD']==c and v['NFKD'] in '123' for c,v in normalization.items())
out={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'source_hashes':sources,'active_fonts':{str(p.relative_to(R)):sha(p) for p in (R/'fonts').rglob('*.ttf')},'masters':masters,'fonts':fonts,'unicode_version':U.unidata_version,'normalization':normalization,'harfbuzz_version':hb.version_string(),'tests':tests,'bounds':bounds,'sources':['https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt#tag-sups','https://www.unicode.org/charts/PDF/U0080.pdf','https://googlefonts.github.io/gf-guide/qa.html']}
(C/'assessment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
css=''.join(f'@font-face{{font-family:{n};src:url("{n}.ttf");font-weight:400 700;}}' for n in fonts)
for w in [400,550,700]:
 cards=''
 for n in fonts:
  cards+=f'<section data-font="{n}" style="font-family:{n};font-weight:{w}"><h2>{n} · {w}</h2><label>Ordinary figures · supported in both fonts</label><p>123 · 101 202 303 · H123H</p><label>Encoded U+00B9/U+00B2/U+00B3 · '+('absent: browser fallback may supply ink; not Virtua coverage' if n=='virtua' else 'actual Rubik cmap coverage')+'</label><p>x¹ x² x³ · 10¹ 10² 10³</p><label>OpenType sups on ordinary 123 · '+('absent: remains ordinary figures' if n=='virtua' else 'present: uses designed superior figures')+'</label><p style="font-feature-settings:\'sups\' 1">123 101 202 303</p></section>'
 html=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Superior figures {w}</title><style>{css}body{{font-family:system-ui;margin:24px;background:#dedede;color:#444}}h1{{font-size:22px}}h2{{font:18px system-ui;margin:0 0 16px}}label{{font:12px system-ui}}section{{border-top:1px solid;padding:18px 0}}p{{font-size:40px;line-height:1.2;margin:8px 0 18px}}footer{{font:11px system-ui}}</style><h1>Superior digit assessment · {w} · unchanged fonts</h1>{cards}<footer>Encoded coverage and feature support are separate. No CSS size/position synthesis is used.</footer></html>'
 (D/f'comparison-{w}.html').write_text(html);(C/f'comparison-{w}.html').write_text(html.replace('src:url("','src:url("assets/'))
print(len(sources),'sources;',len(tests),'cases x4 feature modes;', {m:(len(v['figure_reverse_closure']),len(v['arabic_reserved']),len(v['green'])) for m,v in masters.items()})
