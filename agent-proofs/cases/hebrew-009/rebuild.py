"""Reconcile the 29 explicitly authorized presentation forms; no whole-UFO saves."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,sys,unicodedata,xml.etree.ElementTree as E
import uharfbuzz as hb
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent; R=C.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=re.findall(r'\| U\+[0-9A-F]+ \| ([^ |]+) \|', (C/'README.md').read_text())
assert len(names)==29
if sys.argv[1:] == ['apply']:
 manifest=json.loads((C/'rebuild.json').read_text())
 for rel,digest in manifest['source_hashes'].items():
  assert sha(R/rel)==digest, f'Source changed since preparation: {rel}'
 for row in manifest['forms']:
  p=R/row['path']; q=C/'candidate-sources'/row['path']
  assert sha(q)==row['candidate_sha256']
  p.write_bytes(q.read_bytes())
 print('Applied 58 hash-guarded GLIFs');sys.exit()
assert not (C/'rebuild.json').exists(), 'Preserve existing evidence'
fontpath=R/'fonts/variable/VirtuaGrotesk[wght].ttf'
f=TTFont(fontpath); hf=hb.Font(hb.Face(fontpath.read_bytes()))
(C/'before-fonts').mkdir(exist_ok=True); shutil.copy2(fontpath,C/'before-fonts'/fontpath.name)
manifest={'authorization':'Eli explicitly approved all 29 named forms in Regular and Bold, 2026-10-20; preserve standalone marks and grades.', 'before_font_sha256':sha(fontpath),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'forms':[]}
for master,w in [('Regular',400),('Bold',700)]:
 folder=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs'
 contents=plistlib.loads((folder/'contents.plist').read_bytes()); roots={n:E.parse(folder/file).getroot() for n,file in contents.items()}
 cmap={int(u.get('hex'),16):n for n,e in roots.items() for u in e.findall('unicode')}
 # No target is used as a component by another source, and every donor is flat.
 dependents=[(n,c.get('base')) for n,e in roots.items() for c in e.findall('outline/component') if c.get('base') in names]
 assert not dependents, dependents
 hf.set_variations({'wght':w})
 for name in names:
  p=folder/contents[name]; rel=str(p.relative_to(R)); old=p.read_text(); root=roots[name]
  cp=int(root.find('unicode').get('hex'),16); text=unicodedata.normalize('NFD',chr(cp)); donors=[cmap[ord(c)] for c in text]
  assert len(donors)>=2 and all(not roots[n].findall('outline/component') for n in donors),donors
  base=roots[donors[0]]; anchors={a.get('name'):(int(a.get('x')),int(a.get('y'))) for a in base.findall('anchor')}
  parts=[(donors[0],0,0)]
  for donor in donors[1:]:
   mark=roots[donor];attach=[a for a in mark.findall('anchor') if a.get('name').startswith('_')];assert len(attach)==1
   a=attach[0]; ax,ay=anchors[a.get('name')[1:]];dx=ax-int(a.get('x'));dy=ay-int(a.get('y'));parts.append((donor,dx,dy))
   for a in mark.findall('anchor'):
    if not a.get('name').startswith('_'):anchors[a.get('name')]=(int(a.get('x'))+dx,int(a.get('y'))+dy)
  buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(hf,buf);cursor=0;placed=[]
  for i,pos in zip(buf.glyph_infos,buf.glyph_positions):
   placed.append((f.getGlyphName(i.codepoint),cursor+pos.x_offset,pos.y_offset));cursor+=pos.x_advance
  production={n:f.getBestCmap()[c] for c,n in cmap.items() if c in f.getBestCmap()}
  assert sorted(placed)==sorted((production[n],x,y) for n,x,y in parts),(name,parts,placed)
  outline='\t<outline>\n'+''.join(f'\t\t<component base="{n}" xOffset="{x}" yOffset="{y}"/>\n' for n,x,y in parts)+'\t</outline>'
  new=re.sub(r'\t<outline>.*?\t</outline>',lambda _:outline,old,flags=re.S)
  new=re.sub(r'<advance width="[^"]+"/>',lambda _:f'<advance width="{base.find("advance").get("width")}"/>',new)
  new=re.sub(r'\t<anchor [^\n]+\n','',new)
  anchorblock=''.join(f'\t<anchor name="{n}" x="{x}" y="{y}"/>\n' for n,(x,y) in anchors.items())
  new=new.replace('\t</outline>\n','\t</outline>\n'+anchorblock)
  for sub in ['before-sources','candidate-sources']:
   dest=C/sub/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(old if sub=='before-sources' else new)
  manifest['forms'].append(dict(master=master,glyph=name,codepoint=f'U+{cp:04X}',decomposition=text,path=rel,components=parts,before_sha256=sha(p),candidate_sha256=sha(C/'candidate-sources'/rel)))
(C/'rebuild.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Prepared 58 forms; all component placements equal existing HarfBuzz NFD positioning; no nested components or dependents')
