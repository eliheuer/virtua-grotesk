"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-ogonek-'));(S/'sources').mkdir()
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
closure=json.loads((C/'dependencies.json').read_text());assert all(not v['green'] and not v['arabic_intersection'] for v in closure.values())
changes=[]
for master in ['Regular','Bold']:
 # Preserve the leftward attachment/right-opening hook skeleton, replacing
 # polygonal turns with explicit diagonal landings and axis-tangent bowls.
 if master=='Regular':
  pts=[(128,0,'line'),(112,-16,'line'),(80,-48,None),(64,-80,None),(64,-112,'curve'),(64,-168,None),(104,-208,None),(160,-208,'curve'),(208,-208,'line'),(224,-192,'line'),(224,-176,'line'),(208,-160,'line'),(160,-160,'line'),(128,-160,None),(112,-144,None),(112,-112,'curve'),(112,-80,None),(128,-64,None),(144,-48,'curve'),(192,0,'line')]
  bottom=-240
 else:
  pts=[(96,0,'line'),(80,-16,'line'),(56,-40,None),(48,-80,None),(48,-112,'curve'),(48,-176,None),(96,-224,None),(160,-224,'curve'),(208,-224,'line'),(224,-208,'line'),(224,-176,'line'),(208,-160,'line'),(160,-160,'line'),(128,-160,None),(112,-144,None),(112,-112,'curve'),(112,-80,None),(128,-64,None),(144,-48,'curve'),(192,0,'line')]
  bottom=-256
 for name in ['ogonek','ogonekcomb']:
  p=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif');old=(R/p).read_text();new=old
  if name=='ogonek':
   outline='\t<outline>\n\t\t<contour>\n'+''.join(f'\t\t\t<point x="{x}" y="{y}"'+(f' type="{t}"' if t else '')+(' smooth="yes"' if i in [1,4,7,12,15,18] else '')+'/>\n' for i,(x,y,t) in enumerate(pts))+'\t\t</contour>\n\t</outline>'
   new=re.sub(r'\t<outline>.*?</outline>',outline,new,flags=re.S)
   new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
   new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  new=new.replace('name="bottom" x="120" y="-200"',f'name="bottom" x="120" y="{bottom}"')
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p)})
# Whole-letter inspection exposed an inherited detached A hook and centered
# end-stem hooks. Move only local ogonek components, keeping all base bytes.
placements={'Regular':{'Aogonek':480,'Eogonek':432,'aogonek':368,'uogonek':312,'Iogonek':-48,'iogonek':-40,'dotlessiogonek':-40},'Bold':{'Aogonek':544,'Eogonek':464,'aogonek':384,'uogonek':440,'Iogonek':64,'iogonek':56,'dotlessiogonek':40}}
for master,targets in placements.items():
 d=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs');idx=plistlib.loads((R/d/'contents.plist').read_bytes())
 for name,offset in targets.items():
  p=d/idx[name];old=(R/p).read_text();new=re.sub(r'<component base="ogonek"[^>]*/>',f'<component base="ogonek" xOffset="{offset}"/>',old);assert old!=new
  for folder,text in [('before-sources',old),('candidate-sources',new)]:
   t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
  (S/p).write_text(new);changes.append({'path':str(p),'glyph':name,'master':master,'before':sha(R/p),'after':sha(S/p),'kind':'local component placement; original grade/base/advance retained'})
# Explicit canonical composition keeps the same local hook in renderers and
# web subsets that do not perform Unicode recomposition themselves.
for master in ['Regular','Bold']:
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/features.fea');old=(R/p).read_text()
 rules=''.join(f'\t\tsub {base} ogonekcomb by {base}ogonek;\n' for base in 'AaEeIiUu')
 new=old.replace('\t} ccmp_latin_extended;',rules+'\t} ccmp_latin_extended;',1);assert new!=old
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'master':master,'before':sha(R/p),'after':sha(S/p),'kind':'eight Latin ogonek canonical composition rules'})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
