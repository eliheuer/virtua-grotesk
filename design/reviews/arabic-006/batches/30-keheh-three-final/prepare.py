from pathlib import Path
import re,json,hashlib,shutil,tempfile,plistlib,xml.etree.ElementTree as E,subprocess
R=Path.cwd(); C=Path(__file__).resolve().parent; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'candidate.json').exists()
scratch=Path(tempfile.mkdtemp(prefix='virtua-keheh-three-',dir='/tmp'));(scratch/'sources').mkdir()
for p in R.glob('sources/VirtuaGrotesk-*.ufo'):shutil.copytree(p,scratch/'sources'/p.name)
for f in ['VirtuaGrotesk.designspace','config.yaml']:shutil.copy2(R/'sources'/f,scratch/'sources'/f)
for f in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/f,scratch/f)
shutil.copytree(R/'scripts',scratch/'scripts');(scratch/'.venv').symlink_to(R/'.venv')
m={'status':'candidate','scratch':str(scratch),'source_hashes':{str(p.relative_to(R)):sha(p) for p in R.glob('sources/VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved':{},'glyphs':[]}
for master in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{master}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());trees={n:E.parse(d/f) for n,f in cs.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar','heh-ar','hehDoachashmee-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={x.get('base') for n in dep for x in trees[n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:m['reserved'][str((d/cs[n]).relative_to(R))]=sha(d/cs[n])
 n='kehehThreedotsabove-ar.fina';p=d/cs[n];rel=p.relative_to(R);old=p.read_text();assert n not in dep
 assert not [a for a,t in trees.items() if any(x.get('base')==n for x in t.findall('outline/component'))]
 lib=trees[n].find('lib/dict'); vals=list(lib);marks={vals[i].text:vals[i+1].text for i in range(0,len(vals),2)}
 assert marks['com.runebender.markLabel'] in ['orange','red']; assert marks['public.markColor'] in ['1,0.5,0,1','1,0,0,1']
 new=re.sub(r'\t<outline>.*?</outline>', '\t<outline>\n\t\t<component base="keheh-ar.fina"/>\n\t\t<component base="threedotsupabove-ar" xOffset="216" yOffset="'+('40' if master=='Bold' else '72')+'"/>\n\t</outline>',old,flags=re.S)
 new=re.sub(r'<advance width="[^"]+"/>','<advance width="960"/>',new)
 new=new.replace('<string>'+marks['com.runebender.markLabel']+'</string>','<string>purple</string>').replace('<string>'+marks['public.markColor']+'</string>','<string>0.54,0.44,0.88,1</string>')
 for stage,txt in [('before-sources',old),('candidate-sources',new)]:
  dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
 (scratch/rel).write_text(new)
 m['glyphs'].append({'path':str(rel),'name':n,'master':master,'before_sha256':sha(p),'candidate_sha256':sha(scratch/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir(exist_ok=True)
shutil.copy2(C.parent/'27-doachashmee/assets/after.ttf',C/'assets/before.ttf')
e=json.loads((C.parent/'23-keheh-gaf-joining/evidence.json').read_text())
e['description']='Final three-dot Keheh · both masters';e['study']={'id':'Arabic · Focused repair','language':'ar','readingDefault':'arabic','status':'Final three-dot Keheh · Candidate','note':'Final U+0763 in both weights. Rubik and Readex do not cover U+0763; unavailable panels are explicit. Heh and Beh reserved.','glyphs':[{'key':'keheh-three','char':'ݣ','name':'Three-dot Keheh'}],'presets':{'group':['بݣ','Final in joined context'],'forms':['ݣݣݣ ݣ','All four forms'],'join':['بݣ بݣب','Final and medial'],'marks':['بݣَ','Marked final']}}
e['reading']={'arabic':{'label':'Final contexts','paragraphs':[{'lang':'ar','dir':'rtl','runs':[{'text':'بݣ  لݣ  مݣ  ݣݣݣ ݣ'}]}]}}
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print(scratch)
