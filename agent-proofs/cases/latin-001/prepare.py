"""Guarded scratch repair: displaced combining marks and missing Latin composites."""
from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,re
from fontTools.ufoLib import UFOReader
from fontTools.pens.boundsPen import BoundsPen
C=Path(__file__).resolve().parent;R=C.parents[2];m=json.loads((C/'baseline.json').read_text());S=Path(m['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changes=[]
def stage(rel,new):
 p=R/rel
 if p.exists():
  assert sha(p)==m['sources'][rel],f'Human save: {rel}'
  q=C/'before-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
  before=sha(p)
 else:before=None
 q=C/'candidate-sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(new);(S/rel).write_text(new)
 changes.append(dict(path=rel,before=before,after=sha(q)))
marks='grave acute circumflex macron breve dotaccent dieresis ring hungarumlaut caron cedilla ogonek commaaccent'.split()
newglyphs=[('Ccircumflex',0x108,'C','circumflex'),('ccircumflex',0x109,'c','circumflex'),('Gcircumflex',0x11c,'G','circumflex'),('gcircumflex',0x11d,'g','circumflex'),('Hcircumflex',0x124,'H','circumflex'),('hcircumflex',0x125,'h','circumflex'),('Jcircumflex',0x134,'J','circumflex'),('jcircumflex',0x135,'jdotless','circumflex'),('AEacute',0x1fc,'AE','acute'),('aeacute',0x1fd,'ae','acute')]
for w in ['Regular','Bold']:
 relbase=f'sources/VirtuaGrotesk-{w}.ufo';d=R/relbase/'glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());trees={n:E.parse(d/f).getroot() for n,f in cs.items()};gs=UFOReader(str(R/relbase)).getGlyphSet()
 if w=='Regular':
  for mark in marks:
   n=mark+'comb';p=d/cs[n];old=p.read_text();assert not any(x.get('base')==n for t in trees.values() for x in t.findall('outline/component'))
   new,count=re.subn(r'(<component base="'+mark+r'") yOffset="-?\d+"',r'\1',old);assert count==1
   if mark=='dotaccent':new=new.replace('<anchor name="_hbNunDot" x="120" y="720"/>','<anchor name="_hbNunDot" x="120" y="544"/>')
   stage(str(p.relative_to(R)),new)
 # Spacing donors need the same outgoing stack anchors as their combining forms.
 # This changes attachment, never their outlines, component placements or grades.
 for mark in marks+['tilde']:
  donor=trees[mark];comb=trees[mark+'comb'];p=d/cs[mark];old=p.read_text();new=old
  for anchor in comb.findall('anchor'):
   an=anchor.get('name')
   if an.startswith('_') or an.startswith('hb'):continue
   assert donor.find("anchor[@name='"+an+"']") is None
   line='\t<anchor '+' '.join(f'{k}="{v}"' for k,v in anchor.attrib.items())+'/>\n'
   new=new.replace('\t<lib>',line+'\t<lib>')
  if new!=old:stage(str(p.relative_to(R)),new)
 for name,cp,base,mark in newglyphs:
  assert name not in cs
  bt=trees[base];mt=trees[mark];anc=bt.find("anchor[@name='top']")
  if anc is not None:bx,by=float(anc.get('x')),float(anc.get('y'))
  else:
   pen=BoundsPen(gs);gs[base].draw(pen);bx=(pen.bounds[0]+pen.bounds[2])/2;by=768 if base=='AE' else 576
  if base in ['J','h']:
   cap=[float(p.get('x')) for p in bt.findall('outline/contour/point') if float(p.get('y'))==768];assert cap;bx=(min(cap)+max(cap))/2;by=768
  ma=mt.find("anchor[@name='_top']");dx=round((bx-float(ma.get('x')))/8)*8;dy=round((by-float(ma.get('y')))/8)*8
  width=bt.find('advance').get('width');filename=name.replace('C','C_').replace('G','G_').replace('H','H_').replace('J','J_').replace('AE','A_E_')+'.glif'
  assert filename not in cs.values()
  base_xml=f'\t\t<component base="{base}"/>'
  if base in ['AE','ae']:
   assert not bt.findall('outline/contour')
   base_xml='\n'.join('\t\t<component '+' '.join(f'{k}="{v}"' for k,v in comp.attrib.items())+'/>' for comp in bt.findall('outline/component'))
  stack=trees[mark+'comb'].find("anchor[@name='top']");tx=float(stack.get('x'))+dx;ty=float(stack.get('y'))+dy
  bottom=bt.find("anchor[@name='bottom']");bottom_x=round((float(bottom.get('x')) if bottom is not None else bx)/8)*8
  outanchors=f'\t<anchor name="top" x="{round(tx/8)*8}" y="{round(ty/8)*8}"/>\n\t<anchor name="bottom" x="{bottom_x}" y="0"/>'
  new=f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="{name}" format="2">
\t<unicode hex="{cp:04X}"/>
\t<advance width="{width}"/>
\t<outline>
{base_xml}
\t\t<component base="{mark}" xOffset="{dx}" yOffset="{dy}"/>
\t</outline>
{outanchors}
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
  stage(f'{relbase}/glyphs/{filename}',new);cs[name]=filename
 cp=d/'contents.plist';txt=cp.read_text();entries=''.join(f'\t<key>{n}</key>\n\t<string>{cs[n]}</string>\n' for n,_,_,_ in newglyphs);stage(str(cp.relative_to(R)),txt.replace('</dict>',entries+'</dict>'))
 lp=R/relbase/'lib.plist';txt=lp.read_text();pattern=r'(<key>public.glyphOrder</key>\s*<array>)(.*?)(\n\t</array>)';match=re.search(pattern,txt,re.S);assert match
 insertion=''.join(f'\n\t\t<string>{n}</string>' for n,_,_,_ in newglyphs);new=txt[:match.end(2)]+insertion+txt[match.end(2):]
 cat=''.join(f'\n\t\t<key>{n}</key>\n\t\t<string>base</string>' for n,_,_,_ in newglyphs)
 new=new.replace('<key>public.openTypeCategories</key>\n\t<dict>','<key>public.openTypeCategories</key>\n\t<dict>'+cat)
 stage(str(lp.relative_to(R)),new)
 ip=R/relbase/'fontinfo.plist';it=ip.read_text();it,count=re.subn(r'(<key>openTypeOS2WinAscent</key>\s*<integer>)1152',r'\g<1>1488',it);assert count==1;stage(str(ip.relative_to(R)),it)
 # Preserve the ten composites through web subset layout closure. The j rule
 # follows the existing dot-removal lookup and uses its dotless result.
 fp=R/relbase/'features.fea';ft=fp.read_text();lookup='\tlookup ccmp_latin_extended {\n\t\tlookupflag 0;\n'
 for name,cp,base,mark in newglyphs:lookup+=f'\t\tsub {base} {mark}comb by {name};\n'
 lookup+='\t\tsub j circumflexcomb by jcircumflex;\n\t} ccmp_latin_extended;\n\n'
 ft=ft.replace('feature ccmp {\n# automatic\n','feature ccmp {\n# automatic\n'+lookup)
 ft=ft.replace('lookup ccmp_latin_tilde;\n','lookup ccmp_latin_tilde;\nlookup ccmp_latin_extended;\n')
 stage(str(fp.relative_to(R)),ft)
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(len(changes),'scratch changes; active untouched')
