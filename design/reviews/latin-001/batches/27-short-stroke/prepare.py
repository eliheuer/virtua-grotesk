"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-short-stroke-'));(S/'sources').mkdir()
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
 consumers={'macron'}
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
 assert 'strokeshortcomb' not in idx
 dependencies[master]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'unchanged_donor_consumers':sorted(consumers),'green_hashes':grades,'targets':['strokeshortcomb'],'existing_target_consumers':[]}
 for donor in ['macron']:
  snap=C/'donor-sources'/str((d/idx[donor]).relative_to(R));snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes((d/idx[donor]).read_bytes())
 # New bar uses the existing macron's 64/96 weight and 16-unit terminal cuts.
 h=32 if master=='Regular' else 48
 pts=[(-240,-h),(240,-h),(256,-h+16),(256,h-16),(240,h),(-240,h),(-256,h-16),(-256,-h+16)]
 lines=['\t\t\t<point x="'+str(x)+'" y="'+str(y)+'" type="line"/>' for x,y in pts]
 text=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="strokeshortcomb" format="2">
\t<unicode hex="0335"/>
\t<advance width="0"/>
\t<outline>
\t\t<contour>
{chr(10).join(lines)}
\t\t</contour>
\t</outline>
\t<anchor name="_overlay" x="0" y="0"/>
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
 stage(str((d/'strokeshortcomb.glif').relative_to(R)),text)
 narrow=text.replace('name="strokeshortcomb"','name="strokeshortcomb.narrow"').replace('\t<unicode hex="0335"/>\n','')
 for a,z in [(240,112),(256,128)]:
  narrow=narrow.replace(f'x="{a}"',f'x="{z}"').replace(f'x="-{a}"',f'x="-{z}"')
 stage(str((d/'strokeshortcomb.narrow.glif').relative_to(R)),narrow)

 # Overlay anchors live in explicit GPOS, leaving frozen source anchors intact.
 # Resolve an accented letter to its unaccented body for horizontal placement.
 from fontTools.ttLib import TTFont
 from fontTools.unicodedata import script
 from fontTools.pens.boundsPen import BoundsPen
 import unicodedata as U
 f=TTFont(C/'assets/before.ttf');gs=f.getGlyphSet(location={'wght':400 if master=='Regular' else 700});cmap=f.getBestCmap()
 mapping={}
 for n,r in rr.items():
  for u in r.findall('unicode'):
   cp=int(u.get('hex'),16)
   if script(cp)=='Latn' and U.category(chr(cp)).startswith('L'):
    base=U.normalize('NFD',chr(cp))[0];bn=cmap.get(ord(base),n)
    if bn not in gs:bn=n
    pen=BoundsPen(gs);gs[bn].draw(pen)
    if pen.bounds:
     x=8*round((pen.bounds[0]+pen.bounds[2])/16);y=384 if U.category(chr(cp)) in ['Lu','Lt'] else 288
     mapping[n]=(x,y)
 for n,base in [('idotless','i'),('jdotless','j'),('dotlessiogonek','i')]:
  pen=BoundsPen(gs);gs[base].draw(pen);mapping[n]=(8*round((pen.bounds[0]+pen.bounds[2])/16),288)
 # Include unencoded designspace alternates such as a.bold.
 for n in rr:
  base=n.split('.')[0]
  if '.' in n and base in mapping and n in gs:
   pen=BoundsPen(gs);gs[n].draw(pen)
   if pen.bounds:mapping[n]=(8*round((pen.bounds[0]+pen.bounds[2])/16),mapping[base][1])
 mapping['dottedCircle']=(304,432)
 # GDEF ligatures need component anchors; preserve each component's top x.
 ligs={}
 for n in ['fi','fl']:
  aa={a.get('name'):int(a.get('x')) for a in rr[n].findall('anchor')}
  ligs[n]=[(aa['top_1'],288),(aa['top_2'],288)];mapping.pop(n,None)
 narrow_bases=[n for n in mapping if min(f.getGlyphSet(location={'wght':w})[n].width for w in [400,700])<512]+['fi','fl']
 code='\n# Short-stroke overlay: body centers, independent of top/bottom accents.\nmarkClass [strokeshortcomb strokeshortcomb.narrow] <anchor 0 0> @LATIN_STROKE_OVERLAY;\nfeature mark {\n\t# Automatic Code\n\tlookup LATIN_STROKE_BASES {\n\t\tlookupflag UseMarkFilteringSet [strokeshortcomb strokeshortcomb.narrow];\n'
 for n,(x,y) in sorted(mapping.items()):code+=f'\t\tpos base {n} <anchor {x} {y}> mark @LATIN_STROKE_OVERLAY;\n'
 code+='\t} LATIN_STROKE_BASES;\n\tlookup LATIN_STROKE_LIGATURES {\n\t\tlookupflag UseMarkFilteringSet [strokeshortcomb strokeshortcomb.narrow];\n'
 for n,anchors in ligs.items():code+=f'\t\tpos ligature {n} '+ ' ligComponent '.join(f'<anchor {x} {y}> mark @LATIN_STROKE_OVERLAY' for x,y in anchors)+';\n'
 code+='\t} LATIN_STROKE_LIGATURES;\n} mark;\n'
 narrow_code='\n# Short bars on narrow letters prevent collisions with following text.\n@LATIN_NARROW_OVERLAY_BASES = ['+' '.join(sorted(narrow_bases))+'];\nfeature ccmp {\n\tlookup LATIN_NARROW_OVERLAY {\n\t\tlookupflag UseMarkFilteringSet [strokeshortcomb strokeshortcomb.narrow];\n\t\tsub @LATIN_NARROW_OVERLAY_BASES strokeshortcomb\' by strokeshortcomb.narrow;\n\t} LATIN_NARROW_OVERLAY;\n} ccmp;\n'
 p=root/'features.fea';stage(str(p.relative_to(R)),p.read_text()+narrow_code+code)
 dependencies[master]['overlay_positions']={'bases':mapping,'ligatures':ligs,'narrow_bases':narrow_bases}
 p=d/'contents.plist';stage(str(p.relative_to(R)),p.read_text().replace('</dict>','\t<key>strokeshortcomb</key>\n\t<string>strokeshortcomb.glif</string>\n\t<key>strokeshortcomb.narrow</key>\n\t<string>strokeshortcomb.narrow.glif</string>\n</dict>'))
 p=root/'lib.plist';text=p.read_text();match=re.search(r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)',text,re.S);assert match
 text=text[:match.end(2)]+'\n\t\t<string>strokeshortcomb</string>\n\t\t<string>strokeshortcomb.narrow</string>'+text[match.end(2):]
 text=text.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>\n\t\t<key>strokeshortcomb</key>\n\t\t<string>mark</string>\n\t\t<key>strokeshortcomb.narrow</key>\n\t\t<string>mark</string>');stage(str(p.relative_to(R)),text)
# Cut named statics from the VF so varying GPOS anchors are interpolated too.
p=R/'sources/config.yaml';text=p.read_text();assert 'instances:' not in text
text+='\n# Keep static layout and outline interpolation consistent with the variable font.\ninstances:\n'
for style,w in [('Regular',400),('Medium',500),('SemiBold',600),('Bold',700)]:
 text+=f'  - familyName: "Virtua Grotesk"\n    styleName: "{style}"\n    coordinates: {{wght: {w}}}\n'
stage('sources/config.yaml',text)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S)
