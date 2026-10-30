from pathlib import Path
import hashlib,json,plistlib,re,shutil,subprocess,tempfile,xml.etree.ElementTree as E,unicodedata as U
C=Path(__file__).resolve().parent;R=C.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not (C/'baseline.json').exists():
 S=Path(tempfile.mkdtemp(prefix='virtua-latin-ogonek-subset-'));(S/'sources').mkdir()
 for p in (R/'sources').iterdir():
  if p.name in ['VirtuaGrotesk-Regular.ufo','VirtuaGrotesk-Bold.ufo']:shutil.copytree(p,S/'sources'/p.name)
  elif p.is_file():shutil.copy2(p,S/'sources'/p.name)
 for n in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/n,S/n)
 shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv');(C/'assets').mkdir(exist_ok=True)
 for n,src in [('before',R/'fonts/variable/VirtuaGrotesk[wght].ttf'),('rubik',C.parents[1]/'assets/rubik.ttf')]:shutil.copy2(src,C/'assets'/f'{n}.ttf')
 shutil.copytree(R/'fonts',C/'baseline-fonts')
 sources={str(p.relative_to(R)):sha(p) for p in (R/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts and 'instance_ufos' not in p.parts}
 (C/'baseline.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'scratch':str(S),'sources':sources},indent=2)+'\n')
b=json.loads((C/'baseline.json').read_text());S=Path(b['scratch']);assert all(sha(R/p)==h for p,h in b['sources'].items());changes=[];dependencies={}
for m in ['Regular','Bold']:
 root=R/f'sources/VirtuaGrotesk-{m}.ufo';d=root/'glyphs';idx=plistlib.loads((d/'contents.plist').read_bytes());rr={n:E.parse(d/f).getroot() for n,f in idx.items()};deps={n:{x.get('base') for x in r.findall('outline/component')} for n,r in rr.items()}
 arab={n for n,r in rr.items() if '-ar' in n or any(0x600<=int(u.get('hex'),16)<=0x6ff or 0xfb50<=int(u.get('hex'),16)<=0xfeff for u in r.findall('unicode'))}
 while True:
  new=arab|set().union(*(deps[n] for n in arab))
  if new==arab:break
  arab=new
 green={}
 for n,r in rr.items():
  lib=r.find('lib/dict')
  if lib is None:continue
  g=plistlib.loads(b'<plist>'+E.tostring(lib)+b'</plist>');rgba=[float(v) for v in g.get('public.markColor','0,0,0,0').split(',')]
  if g.get('com.runebender.markLabel')=='green' or (rgba[1]>.6 and rgba[1]>rgba[0] and rgba[1]>rgba[2]):green[n]=sha(d/idx[n])
 cmap={int(u.get('hex'),16):n for n,r in rr.items() for u in r.findall('unicode')}
 rules=[]
 for cp,n in sorted(cmap.items()):
  dec=U.normalize('NFD',chr(cp))
  if len(dec)>1 and dec[0] in 'AaEeIiUu' and all(U.combining(c)==230 and ord(c) in cmap for c in dec[1:]):rules.append((n,[cmap[ord(c)] for c in dec]))
 dependencies[m]={'arabic_reserved':{n:sha(d/idx[n]) for n in sorted(arab)},'green_hashes':green,'decomposition_rules':rules,'all_glifs_unchanged':True}
 standalone='''# Restore canonical ogonek construction after cmap-limited normalization.
# This helper is invoked only when an ogonek follows an accented vowel.
lookup LATIN_OGONEK_DECOMPOSE {
\tlookupflag 0;
'''+''.join(f'\tsub {n} by '+ ' '.join(seq)+';\n' for n,seq in rules)+'''} LATIN_OGONEK_DECOMPOSE;

'''
 prefix='''	lookup ccmp_ogonek_normalize {
		lookupflag UseMarkFilteringSet [ogonekcomb];
'''+''.join(f'\t\tsub {n}\' lookup LATIN_OGONEK_DECOMPOSE ogonekcomb;\n' for n,_ in rules)+'''	} ccmp_ogonek_normalize;
	lookup ccmp_ogonek_restore {
		lookupflag UseMarkFilteringSet [ogonekcomb];
'''+''.join(f'\t\tsub {base} ogonekcomb by {base}ogonek;\n' for base in 'AaEeIiUu')+'''	} ccmp_ogonek_restore;

'''
 rel=str((root/'features.fea').relative_to(R));old=(R/rel).read_text();new=old.replace('feature ccmp {\n# automatic\n',standalone+'feature ccmp {\n# automatic\n'+prefix)
 new=new.replace('lookup ccmp_soft_dotted_ligature_0;','lookup ccmp_ogonek_normalize;\nlookup ccmp_ogonek_restore;\nlookup ccmp_soft_dotted_ligature_0;')
 for folder,data in [('before-sources',old),('candidate-sources',new)]:
  q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(data)
 (S/rel).write_text(new);changes.append({'path':rel,'before':sha(R/rel),'after':sha(S/rel)})
(C/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(C/'dependencies.json').write_text(json.dumps(dependencies,indent=2)+'\n');print(S);print('Contextual decomposition rules',len(rules))
