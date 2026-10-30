"""Read-only source assessment; diagnostic cmap probes are never build inputs."""
from pathlib import Path
import hashlib,json,shutil,subprocess,plistlib,xml.etree.ElementTree as E
from fontTools.ttLib import TTFont
import uharfbuzz as hb
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch34';A=C/'assets'
for p in [D,A,C/'browser']:p.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
if (C/'assessment.json').exists():
 assert sources==json.loads((C/'assessment.json').read_text())['source_hashes'], 'Sources changed; preserve the original assessment and start a new one.'
shutil.copy2(R/'fonts/variable/VirtuaGrotesk[wght].ttf',A/'virtua.ttf');shutil.copy2(C.parent/'33-brokenbar/assets/rubik.ttf',A/'rubik.ttf')
receipt=json.loads((C.parent/'33-brokenbar/final-identity.json').read_text())
assert sha(A/'virtua.ttf')==receipt['active_fonts']['fonts/variable/VirtuaGrotesk[wght].ttf']
probes={'probe-ad-hyphen':{0xad:'hyphen'},'probe-ad-H':{0xad:'H'},'probe-2010-H':{0x2010:'H'}}
for name,mapping in probes.items():
 f=TTFont(A/'virtua.ttf',recalcTimestamp=False)
 for t in f['cmap'].tables:
  if t.isUnicode():t.cmap.update(mapping)
 f.save(A/(name+'.ttf'))
for p in A.glob('*.ttf'):shutil.copy2(p,D/p.name)
masters={}
for master in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{c.get('base') for c in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 consumers={'hyphen','uni2010'}
 while True:
  new=consumers|{n for n,dep in deps.items() if dep&consumers}
  if new==consumers:break
  consumers=new
 green={};donors={}
 for n,r in rr.items():
  lib=r.find('lib/dict');g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>') if lib is not None else {};rgba=[float(x) for x in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
  if n in consumers:donors[n]={'grade':g,'hash':sha(d/idx[n]),'components':sorted(deps[n]),'advance':r.find('advance').attrib}
 for n in ['hyphen','uni2010']:
  q=C/'donor-sources'/master/idx[n];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(d/idx[n],q)
 masters[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green':green,'hyphen_reverse_closure':donors,'closure_intersects_arabic':sorted(consumers&arab)}
fonts={};tests=[]
for name in ['virtua','rubik',*probes]:
 p=A/(name+'.ttf');f=TTFont(p);cm=f.getBestCmap();fonts[name]={'sha256':sha(p),'cmap':{f'U+{cp:04X}':cm.get(cp) for cp in [0xad,0x2d,0x2010,0x2011]}}
 for w in [400,475,550,625,700]:
  font=hb.Font(hb.Face(p.read_bytes()));font.set_variations({'wght':w})
  def shape(text,flag=0):
   b=hb.Buffer();b.add_str(text);b.guess_segment_properties();b.flags=flag;hb.shape(font,b)
   return [{'glyph':f.getGlyphName(i.codepoint),'cluster':i.cluster,'advance':v.x_advance,'x':v.x_offset,'y':v.y_offset} for i,v in zip(b.glyph_infos,b.glyph_positions)]
  for word in ['cooperate','extraordinary','office']:
   pos=2 if word!='extraordinary' else 5;soft=word[:pos]+'\u00ad'+word[pos:];plain=shape(word);normal=shape(soft);preserved=shape(soft,hb.BufferFlags.PRESERVE_DEFAULT_IGNORABLES)
   visible=lambda rows:[{k:v for k,v in x.items() if k!='cluster'} for x in rows if not(x['glyph']=='space' and x['advance']==0)]
   # Default ignorables may affect ligature cluster bookkeeping, not the ink stream.
   assert visible(normal)==visible(plain),(name,w,word)
   tests.append({'font':name,'weight':w,'text':soft,'default':normal,'preserve_ignorables':preserved,'plain':plain,'default_visible_equal':True})
(C/'assessment.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'source_hashes':sources,'masters':masters,'fonts':fonts,'diagnostic_only_cmap_edits':probes,'harfbuzz_version':hb.version_string(),'tests':tests},indent=2)+'\n')
# Purpose-built line-break fixture; this is separate from unchanged stock Diffenator.
css=''.join(f'@font-face{{font-family:"{name}";src:url("{name}.ttf");font-weight:400 700;}}' for name in fonts)
for w in [400,550,700]:
 for mode,names in [('comparison',['virtua','rubik']),('diagnostic',list(probes))]:
  cards=''
  for name in names:
   cards+=f'''<section data-font="{name}" style="font-family:{name};font-weight:{w}"><h2>{name}</h2><div class="row"><div><label>Manual wrap, U+00AD (160px)</label><p class="manual sample">extra&shy;ordinary</p></div><div><label>Hyphens none, same U+00AD</label><p class="none sample">extra&shy;ordinary</p></div><div><label>Explicit hyphen + hard break</label><p class="explicit sample">extra-<br>ordinary</p></div></div><div class="row"><div><label>No wrap, U+00AD</label><span class="nowrap sample">extra&shy;ordinary</span></div><div><label>No wrap, plain control</label><span class="plain sample">extraordinary</span></div></div></section>'''
  html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Soft hyphen {mode} {w}</title><style>{css}body{{font-family:system-ui;margin:24px;color:#111;background:white}}h1{{font-size:22px}}h2{{font:16px system-ui;margin:0 0 10px}}label{{display:block;font:12px system-ui;color:#555;margin-bottom:8px}}section{{border-top:1px solid #999;padding:16px 0}}.row{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-bottom:18px}}.row>div{{min-width:0}}.sample{{font-size:32px;line-height:1.3;margin:0}}p.sample{{width:160px;border-right:1px dotted #aaa;overflow-wrap:normal;word-break:normal}}.manual{{hyphens:manual}}.none{{hyphens:none}}.nowrap,.plain{{white-space:nowrap}}footer{{font:10px system-ui;overflow-wrap:anywhere}}</style><h1>U+00AD behavior · {w} · {mode}</h1><p>Frozen Virtua 9359e981 and pinned Rubik. English, manual hyphenation. Diagnostic fonts change cmap only and are not candidates.</p>{cards}<footer>Loading font evidence…</footer><script>Promise.all([...document.querySelectorAll('section')].map(s=>document.fonts.load('{w} 32px "'+s.dataset.font+'"'))).then(()=>{{let data=[...document.querySelectorAll('section')].map(s=>({{font:s.dataset.font,manualHeight:s.querySelector('.manual').getBoundingClientRect().height,noneHeight:s.querySelector('.none').getBoundingClientRect().height,nowrapWidth:s.querySelector('.nowrap')?.getBoundingClientRect().width ?? null,plainWidth:s.querySelector('.plain')?.getBoundingClientRect().width ?? null}}));document.querySelector('footer').textContent=JSON.stringify(data);}})</script></html>'''
  if mode=='diagnostic':
   import re
   html=re.sub(r'<div class="row"><div><label>No wrap, U\+00AD</label>.*?</section>', '</section>', html, flags=re.S)
  (D/f'{mode}-{w}.html').write_text(html);(C/f'{mode}-{w}.html').write_text(html.replace('src:url("','src:url("assets/'))
print('Assessment saved:',len(tests),'shaping cases;',len(sources),'source hashes;', {m:(len(v['arabic_reserved']),len(v['green']))for m,v in masters.items()})
