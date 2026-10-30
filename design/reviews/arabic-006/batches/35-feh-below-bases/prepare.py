from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,tempfile,re
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'candidate.json').exists()
S=Path(tempfile.mkdtemp(prefix='virtua-feh-below-',dir='/tmp'));(S/'sources').mkdir()
for p in R.glob('sources/VirtuaGrotesk-*.ufo'):shutil.copytree(p,S/'sources'/p.name)
for f in ['VirtuaGrotesk.designspace','config.yaml']:shutil.copy2(R/'sources'/f,S/'sources'/f)
for f in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/f,S/f)
shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv');(S/'documentation/proofs').mkdir(parents=True)
m={'status':'candidate','scratch':str(S),'source_hashes':{str(p.relative_to(R)):sha(p) for p in R.glob('sources/VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved':{},'glyphs':[]}
for w in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());trees={n:E.parse(d/f) for n,f in cs.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar','heh-ar','hehDoachashmee-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={x.get('base') for n in dep for x in trees[n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:m['reserved'][str((d/cs[n]).relative_to(R))]=sha(d/cs[n])
 for family in ['fehDotmovedbelow-ar','fehThreedotsbelow-ar']:
  for suffix in (['', '.init','.medi','.fina'] if 'Threedots' in family else ['', '.fina']):
   n=family+suffix;base='fehDotless-ar'+suffix;assert n not in dep;p=d/cs[n];rel=str(p.relative_to(R));t=trees[n];old=p.read_text();lib=list(t.find('lib/dict'));marks={lib[i].text:lib[i+1].text for i in range(0,len(lib),2)};assert marks['com.runebender.markLabel'] in ['orange','red','purple'];assert marks['public.markColor'] not in ['0,1,0,1','0.09,0.72,0.44,1']
   assert not [a for a,tt in trees.items() if any(x.get('base')==n for x in tt.findall('outline/component'))]
   cx=({'':704,'.fina':688,'.init':240,'.medi':256} if w=='Regular' else {'':720,'.fina':720,'.init':272,'.medi':272})[suffix]
   triple='Threedots' in family;donor='threedotsdowncenter-ar' if triple else 'dotbelow-ar'
   dx=cx-(232 if triple else (112 if w=='Regular' else 120));dy=(-504 if w=='Regular' else -520) if triple else 0
   outline=f'\t<outline>\n\t\t<component base="{base}"/>\n\t\t<component base="{donor}" xOffset="{dx}" yOffset="{dy}"/>\n\t</outline>'
   new=re.sub(r'\t<outline>.*?\t</outline>',outline,old,flags=re.S);width=trees[base].find('advance').get('width');new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
   top=({'':672,'.fina':488,'.init':704,'.medi':552} if w=='Regular' else {'':784,'.fina':664,'.init':784,'.medi':664})[suffix];bottom=-320 if w=='Regular' else (-376 if triple else -368)
   anchors=[dict(a.attrib) for a in trees[base].findall('anchor')]
   for a in anchors:
    if a['name'] in ['top','bottom']:a.update(x=str(cx),y=str(top if a['name']=='top' else bottom))
   aa='\n'.join('\t<anchor '+' '.join(f'{k}="{v}"' for k,v in a.items())+'/>' for a in anchors);new=new.replace('\t<lib>',aa+'\n\t<lib>')
   new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new);new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
   for stage,txt in [('before-sources',old),('candidate-sources',new)]:
    dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
   (S/rel).write_text(new);m['glyphs'].append({'name':n,'master':w,'path':rel,'base':base,'dot_donor':donor,'dot_offset':[dx,dy],'before_sha256':sha(p),'candidate_sha256':sha(S/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'34-extension-joins/assets/after.ttf',C/'assets/before.ttf')
e=json.loads((C.parent/'34-extension-joins/evidence.json').read_text());e['description']='Feh below-dot bases';e['study']={'id':'Arabic · First pass','language':'ar','readingDefault':'arabic','status':'Feh below dots · Candidate','note':'Isolated/final Feh bases replace incorrect Qaf; all shared donors unchanged.','glyphs':[{'key':'fehbelow','char':'ڢ','name':'Feh dot below'},{'key':'fehthreebelow','char':'ڥ','name':'Feh three dots below'}],'presets':{'group':['ڢڢڢ ڢ','Feh dot below'],'forms':['ڥڥڥ ڥ','Feh three dots below'],'join':['مڢ مڥ','Final joins'],'marks':['ڢَ ڥِ','Attachment']}}
e['reading']={'arabic':{'label':'Feh below-dot variants','paragraphs':[{'lang':'ar','dir':'rtl','runs':[{'text':'ڢڢڢ ڢ  ڥڥڥ ڥ  مڢ مڥ'}]}]}}
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for f in ['proof.py','render.py']:shutil.copy2(C.parent/'34-extension-joins'/f,C/f)
p=C/'render.py';p.write_text(p.read_text().replace('Arabic · Extension joins','Feh · Below-dot bases'))
s=p.read_text().replace("C.parent/'32-wrapper-joins/detail.rs'","C.parent/'33-seen-sixdots/large.rs'");(C/'render-large.py').write_text(s)
print(S,len(m['glyphs']))
