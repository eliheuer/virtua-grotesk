from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,tempfile,re
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'candidate.json').exists()
S=Path(tempfile.mkdtemp(prefix='virtua-wrapper-joins-',dir='/tmp'));(S/'sources').mkdir()
for p in R.glob('sources/VirtuaGrotesk-*.ufo'):shutil.copytree(p,S/'sources'/p.name)
for f in ['VirtuaGrotesk.designspace','config.yaml']:shutil.copy2(R/'sources'/f,S/'sources'/f)
for f in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/f,S/f)
shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv');(S/'documentation/proofs').mkdir(parents=True)
m={'status':'candidate','scratch':str(S),'source_hashes':{str(p.relative_to(R)):sha(p) for p in R.glob('sources/VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved':{},'glyphs':[]}
targets={'Regular': ['beeh-ar.init', 'beeh-ar.medi', 'fehDotmovedbelow-ar.fina', 'fehDotmovedbelow-ar.medi', 'fehThreedotsbelow-ar.fina', 'fehThreedotsbelow-ar.medi', 'qafDotabove-ar.fina', 'qafDotabove-ar.medi', 'qafThreedotsabove-ar.fina', 'qafThreedotsabove-ar.medi', 'tehRing-ar.init', 'tehRing-ar.medi', 'tehThreedotsdown-ar.init', 'tehThreedotsdown-ar.medi', 'tteh-ar.medi', 'tteheh-ar.init', 'tteheh-ar.medi', 'veh-ar.init', 'veh-ar.medi'], 'Bold': ['yeh-ar.init.ctr']}
for w,names in targets.items():
 d=R/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());trees={n:E.parse(d/f) for n,f in cs.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar','heh-ar','hehDoachashmee-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={x.get('base') for n in dep for x in trees[n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:m['reserved'][str((d/cs[n]).relative_to(R))]=sha(d/cs[n])
 for n in names:
  assert n not in dep;p=d/cs[n];rel=str(p.relative_to(R));t=trees[n];old=p.read_text();lib=list(t.find('lib/dict'));marks={lib[i].text:lib[i+1].text for i in range(0,len(lib),2)};assert marks['com.runebender.markLabel'] in ['orange','red','purple'];assert marks['public.markColor'] not in ['0,1,0,1','0.09,0.72,0.44,1']
  consumers=[a for a,tt in trees.items() if any(x.get('base')==n for x in tt.findall('outline/component'))];assert not consumers,(n,consumers)
  co=t.findall('outline/component');assert len(co)==2 and not t.findall('outline/contour');assert all(float(co[0].get(k,'0'))==0 for k in ['xOffset','yOffset'])
  base=co[0].get('base');width=trees[base].find('advance').get('width');new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',old);assert new!=old
  for stage,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  (S/rel).write_text(new);m['glyphs'].append({'name':n,'master':w,'path':rel,'base':base,'old_width':t.find('advance').get('width'),'new_width':width,'before_sha256':sha(p),'candidate_sha256':sha(S/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir();shutil.copy2(C.parent/'33-seen-sixdots/assets/after.ttf',C/'assets/before.ttf')
e=json.loads((C.parent/'33-seen-sixdots/evidence.json').read_text());e['description']='Extension joining widths';e['study']={'id':'Arabic · First pass','language':'ar','readingDefault':'arabic','status':'Extension joins · Candidate','note':'Only named wrapper advances change; all outlines and marks remain unchanged.','glyphs':[{'key':'extensionjoins','char':'ڢ','name':'Extension joins'}],'presets':{'group':['ڢڢڢ ڧڧڧ','Feh/Qaf variants'],'forms':['ڥڥڥ ڨڨڨ','Three-dot variants'],'join':['ٻٻٻ ٽٽٽ','Beh-type extensions'],'marks':['يآ يإ','Contextual Yeh joins']}}
e['reading']={'arabic':{'label':'Extension joins','paragraphs':[{'lang':'ar','dir':'rtl','runs':[{'text':'ڢڢڢ ڧڧڧ ڥڥڥ ڨڨڨ ٻٻٻ ٽٽٽ ٹٹٹ ٺٺٺ ڤڤڤ'}]}]}}
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for f in ['proof.py','render.py']:shutil.copy2(C.parent/'33-seen-sixdots'/f,C/f)
p=C/'render.py';p.write_text(p.read_text().replace('Six-dot Seen · Complete forms','Arabic · Extension joins'))
print(S,len(m['glyphs']))
