"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-fraction-forms-'));(S/'sources').mkdir()
 for p in (R/'sources').iterdir():
  if p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']:shutil.copytree(p,S/'sources'/p.name)
  elif p.is_file():shutil.copy2(p,S/'sources'/p.name)
 for n in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/n,S/n)
 shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv')
 (C/'assets').mkdir(exist_ok=True)
 for n,src in [('before',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parents[1]/'assets/rubik.ttf')]:shutil.copy2(src,C/'assets'/f'{n}.ttf')
 shutil.copytree(R/'fonts',C/'baseline-fonts')
 sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
 (C/'baseline.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'scratch':str(S),'sources':sources},indent=2)+'\n')

b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items())
changes=[];dependencies={}
def stage(rel,text):
 p=R/rel;before=sha(p) if p.exists() else None
 if before:
  assert before==b['sources'][rel]
  q=C/'before-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
 q=C/'candidate-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text);(S/rel).write_text(text)
 changes.append({'path':rel,'before':before,'after':sha(q)})
for master in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{master}.ufo';d=root/'glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{x.get('base') for x in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 donors={'one','two','three','four'};consumers=set(donors)
 while True:
  new=consumers|{n for n,v in deps.items() if v&consumers}
  if new==consumers:break
  consumers=new
 grades={}
 for n,r in rr.items():
  lib=r.find('lib/dict')
  if lib is None:continue
  g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>');rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):grades[n]=sha(d/idx[n])
 assert donors<=set(grades) and not consumers&arab
 names=['one.numr','two.dnom','three.numr','four.dnom','fraction.slash','onequarter','onehalf','threequarters'];assert not set(names)&set(idx)
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_reference_consumers':sorted(consumers),'green_hashes':grades,'targets':names,'existing_target_consumers':[]}
 for donor in donors:
  snap=C/'donor-sources'/str((d/idx[donor]).relative_to(R));snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes((d/idx[donor]).read_bytes())
 # Derive the protected figure skeleton at half scale; redraw exposed cuts at16.
 import math
 snap=lambda v:int(math.floor(v/8+0.5)*8)
 for name,cp,donor in [('one.numr',None,'one'),('two.dnom',None,'two'),('three.numr',None,'three')]:
  src=rr[donor].findall('outline/contour/point');points=[(snap(float(q.get('x'))/2+16),snap(float(q.get('y'))/2+384),q.get('type')) for q in src]
  bold=master=='Bold'
  if donor=='one':
   xy=([(128,384),(192,384),(208,400),(208,752),(192,768),(160,768),(144,752),(136,704),(80,688),(48,688),(32,672),(32,640),(48,624),(104,624),(112,616),(112,400)] if bold else [(128,384),(160,384),(176,400),(176,752),(160,768),(144,768),(128,752),(120,704),(72,696),(48,696),(32,680),(32,664),(48,648),(104,648),(112,640),(112,400)])
   edits=dict(enumerate(xy));advance=264 if bold else 232
  elif donor=='two':
   edits=({0:(56,384),1:(304,384),2:(320,400),3:(320,448),4:(304,464),5:(176,464),6:(168,472),7:(168,480),18:(40,640),19:(56,624),20:(112,624),21:(128,640),33:(40,408),34:(40,400)} if bold else {0:(48,384),1:(272,384),2:(288,400),3:(288,424),4:(272,440),5:(96,440),6:(88,448),7:(88,464),18:(40,648),19:(56,632),20:(80,632),21:(96,648),33:(32,408),34:(32,400)})
   advance=352 if bold else 328
  else:
   edits=({17:(56,656),18:(72,640),19:(120,640),20:(136,656),30:(176,624),31:(160,608),32:(160,576),33:(176,560),43:(120,504),44:(104,520),45:(56,520),46:(40,504),47:(40,488)} if bold else {17:(48,664),18:(64,648),19:(80,648),20:(96,664),30:(160,608),31:(144,592),32:(144,584),33:(160,568),43:(88,496),44:(72,512),45:(56,512),46:(40,496),47:(40,488)})
   advance=376 if bold else 352
  if donor=='two':edits.update({8:(184,496),10:(280,544),29:(216,584),31:(88,520)} if bold else {8:(128,488),10:(256,552),29:(224,584),31:(80,512)})
  points=[(*edits.get(i,(x,y)),t) for i,(x,y,t) in enumerate(points)]
  points=[(x+(8 if donor=='one' else 0),y-(384 if donor=='two' else 0),t) for x,y,t in points]
  if donor=='one':advance+=16
  contours=[points]
  outline=''.join('\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"'+(' smooth="yes"' if t=='curve' and (src[i].get('smooth')=='yes' or (donor=='two' and i in [9,30])) else '') if t else '')+'/>\n' for i,(x,y,t) in enumerate(contour))+'\t\t</contour>\n' for contour in contours)
  text=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
\t<advance width="{advance}"/>
\t<outline>
{outline}\t</outline>
\t<lib>
\t\t<dict>
\t\t\t<key>com.runebender.markLabel</key>
\t\t\t<string>purple</string>
\t\t\t<key>public.markColor</key>
\t\t\t<string>0.54,0.44,0.88,1</string>
\t\t</dict>
\t</lib>
</glyph>
'''
  stage(str((d/(name+'.glif')).relative_to(R)),text)
 # Closed four is reconstructed from the green-four recipe; denominator alignment.
 bold=master=='Bold';advance=384 if bold else 352
 outer=([(224,384),(280,384),(296,400),(296,456),(304,464),(336,464),(352,480),(352,520),(336,536),(304,536),(296,544),(296,752),(280,768),(208,768),(32,536),(32,480),(48,464),(200,464),(208,456),(208,400)] if bold else [(224,384),(248,384),(264,400),(264,464),(272,472),(304,472),(320,488),(320,504),(304,520),(272,520),(264,528),(264,752),(248,768),(232,768),(32,512),(32,488),(48,472),(200,472),(208,464),(208,400)])
 inner=([(136,536),(136,544),(200,640),(208,640),(208,544),(200,536)] if bold else [(104,520),(104,528),(200,664),(208,664),(208,528),(200,520)])
 outline=''.join('\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y-384}" type="line"/>\n' for x,y in contour)+'\t\t</contour>\n' for contour in [outer,inner])
 def glif(name,advance,outline,cp=None):
  uni=f'\t<unicode hex="{cp}"/>\n' if cp else ''
  return f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
{uni}\t<advance width="{advance}"/>
\t<outline>
{outline}\t</outline>
\t<lib>
\t\t<dict>
\t\t\t<key>com.runebender.markLabel</key>
\t\t\t<string>purple</string>
\t\t\t<key>public.markColor</key>
\t\t\t<string>0.54,0.44,0.88,1</string>
\t\t</dict>
\t</lib>
</glyph>
'''
 stage(str((d/'four.dnom.glif').relative_to(R)),glif('four.dnom',advance,outline))
 q=C.parent/'51-fraction-slash/candidate-sources'/str((d/'fraction.glif').relative_to(R))
 text=q.read_text().replace('name="fraction"','name="fraction.slash"').replace('\t<unicode hex="2044"/>\n','')
 stage(str((d/'fraction.slash.glif').relative_to(R)),text)
 for name,cp,a,z in [('onequarter','00BC','one.numr','four.dnom'),('onehalf','00BD','one.numr','two.dnom'),('threequarters','00BE','three.numr','four.dnom')]:
  def aw(n):return int(E.parse(S/str((d/(n+'.glif')).relative_to(R))).find('advance').get('width'))
  na=aw(a); da=aw(z); outline=f'\t\t<component base="{a}"/>\n\t\t<component base="fraction.slash" xOffset="{na-16}"/>\n\t\t<component base="{z}" xOffset="{na+232}"/>\n'
  stage(str((d/(name+'.glif')).relative_to(R)),glif(name,na+232+da,outline,cp))
 p=d/'contents.plist';text=p.read_text().replace('</dict>',''.join('\t<key>'+n+'</key>\n\t<string>'+n+'.glif</string>\n' for n in names)+'</dict>');stage(str(p.relative_to(R)),text)
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+''.join('\n\t\t<string>'+n+'</string>' for n in names)+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>'+''.join('\n\t\t<key>'+n+'</key>\n\t\t<string>base</string>' for n in names));stage(str(p.relative_to(R)),text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
