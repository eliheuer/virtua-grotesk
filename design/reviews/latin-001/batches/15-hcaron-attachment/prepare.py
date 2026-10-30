"""Reproduce this bounded draft only against its frozen pre-edit hashes."""
from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E
C=Path(__file__).resolve().parent;R=C.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-hcaron-'));(S/'sources').mkdir()
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
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/hcaron.glif');old=(R/p).read_text()
 x=-96 if master=='Regular' else -48;top=120 if master=='Regular' else 160;bottom=296 if master=='Regular' else 336;width=584 if master=='Regular' else 672
 new=re.sub(r'<component base="caron"[^>]*/>',f'<component base="caron" xOffset="{x}" yOffset="192"/>',old)
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
 new=new.replace('\t<lib>',f'\t<anchor name="top" x="{top}" y="1056"/>\n\t<anchor name="bottom" x="{bottom}" y="0"/>\n\t<lib>')
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'glyph':'hcaron','master':master,'before':sha(R/p),'after':sha(S/p),'kind':'local mark over ascender, explicit stack anchors, base advance; preserve geometry and grade'})
 p=Path(f'sources/VirtuaGrotesk-{master}.ufo/features.fea');old=(R/p).read_text()
 new=old.replace('\t} ccmp_latin_extended;','\t} ccmp_latin_extended;\n\n\tlookup ccmp_hcaron {\n\t\tlookupflag UseMarkFilteringSet [caroncomb];\n\t\tsub h caroncomb by hcaron;\n\t} ccmp_hcaron;',1)
 new=new.replace('lookup ccmp_latin_extended;','lookup ccmp_latin_extended;\nlookup ccmp_hcaron;')
 for folder,text in [('before-sources',old),('candidate-sources',new)]:
  t=C/folder/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_text(text)
 (S/p).write_text(new);changes.append({'path':str(p),'master':master,'before':sha(R/p),'after':sha(S/p),'kind':'canonical hcaron fallback'})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');print(S)
