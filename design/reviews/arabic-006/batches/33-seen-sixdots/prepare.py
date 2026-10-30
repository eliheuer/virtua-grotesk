from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,tempfile,re
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'candidate.json').exists()
S=Path(tempfile.mkdtemp(prefix='virtua-sixdots-',dir='/tmp'));(S/'sources').mkdir()
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
 # Transfer the round contour used in the earlier Tcheh donor, without editing it.
 donor=trees['threedotsdowncenter-ar'].find('outline/contour')
 xs=[float(p.get('x')) for p in donor];ys=[float(p.get('y')) for p in donor];dx=(min(xs)+max(xs))/2;dy=(min(ys)+max(ys))/2
 radius=40 if w=='Regular' else 56;half=56 if w=='Regular' else 72;rise=96 if w=='Regular' else 120
 for suffix in ['', '.init','.medi','.fina']:
  n='seenSixdots-ar'+suffix;base='seen-ar'+suffix;assert n not in dep;p=d/cs[n];rel=str(p.relative_to(R));t=trees[n];old=p.read_text();lib=list(t.find('lib/dict'));marks={lib[i].text:lib[i+1].text for i in range(0,len(lib),2)};assert marks['com.runebender.markLabel'] in ['orange','red','purple'];assert marks['public.markColor'] not in ['0,1,0,1','0.09,0.72,0.44,1']
  assert not [a for a,tt in trees.items() if any(x.get('base')==n for x in tt.findall('outline/component'))]
  bx=({'':1072,'.init':432,'.medi':432,'.fina':896} if w=='Regular' else {'':1008,'.init':464,'.medi':464,'.fina':1008})[suffix]
  crown=({'':432,'.init':304,'.medi':320,'.fina':320}[suffix] if w=='Regular' else 384)
  lower=crown+80+radius;below=-80-radius
  centers=[(bx-half,lower),(bx+half,lower),(bx,lower+rise),(bx-half,below),(bx+half,below),(bx,below-rise)]
  lines=['\t<outline>',f'\t\t<component base="{base}"/>']
  for cx,cy in centers:
   lines+=['\t\t<contour>']
   for pt in donor:
    attrs={'x':str(int(float(pt.get('x'))-dx+cx)),'y':str(int(float(pt.get('y'))-dy+cy))}
    for k in ['type','smooth']:
     if pt.get(k):attrs[k]=pt.get(k)
    lines+=['\t\t\t<point '+' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>']
   lines+=['\t\t</contour>']
  lines+=['\t</outline>']
  new=re.sub(r'\t<outline>.*?\t</outline>','\n'.join(lines),old,flags=re.S)
  width=trees[base].find('advance').get('width');new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  anchors=[dict(a.attrib) for a in trees[base].findall('anchor')]
  for a in anchors:
   if a['name']=='top':a.update(x=str(bx),y=str(lower+rise+radius+64))
   if a['name']=='bottom':a.update(x=str(bx),y=str(below-rise-radius-64))
  aa='\n'.join('\t<anchor '+' '.join(f'{k}="{v}"' for k,v in a.items())+'/>' for a in anchors)
  new=new.replace('\t<lib>',aa+'\n\t<lib>')
  new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new)
  new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  for stage,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  (S/rel).write_text(new);m['glyphs'].append({'name':n,'master':w,'path':rel,'base':base,'centers':centers,'radius':radius,'before_sha256':sha(p),'candidate_sha256':sha(S/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir();shutil.copy2(C.parent/'32-wrapper-joins/assets/after.ttf',C/'assets/before.ttf')
e=json.loads((C.parent/'32-wrapper-joins/evidence.json').read_text());e['description']='Six-dot Seen complete dot groups';e['study']={'id':'Arabic · First pass','language':'ar','readingDefault':'arabic','status':'Six-dot Seen · Candidate','note':'Seen bases unchanged; six round dots in both masters. Rubik/Readex lack U069C.','glyphs':[{'key':'sixdots','char':'ڜ','name':'Six-dot Seen'}],'presets':{'group':['ڜڜڜ ڜ','All four forms'],'forms':['ڜڜڜ ڜ','All four forms'],'join':['مڜ ڜم مڜم','Joining contexts'],'marks':['ڜَ ڜِ ڜُ','Marks']}}
e['reading']={'arabic':{'label':'Six-dot Seen','paragraphs':[{'lang':'ar','dir':'rtl','runs':[{'text':'ڜڜڜ ڜ  مڜ ڜم مڜم'}]}]}}
(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for f in ['proof.py','render.py']:shutil.copy2(C.parent/'32-wrapper-joins'/f,C/f)
p=C/'render.py';txt=p.read_text().replace("C/'detail.rs'","C.parent/'32-wrapper-joins/detail.rs'").replace('Arabic · Joining widths','Six-dot Seen · Complete forms');p.write_text(txt)
print(S,len(m['glyphs']))
