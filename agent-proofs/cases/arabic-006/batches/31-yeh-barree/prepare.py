from pathlib import Path
import re,json,hashlib,shutil,tempfile,plistlib,xml.etree.ElementTree as E,subprocess
R=Path.cwd(); C=Path(__file__).resolve().parent; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'candidate.json').exists()
scratch=Path(tempfile.mkdtemp(prefix='virtua-barree-',dir='/tmp'));(scratch/'sources').mkdir()
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
 n='yehBarree-ar.fina';p=d/cs[n];rel=p.relative_to(R);old=p.read_text();assert n not in dep
 assert not [a for a,t in trees.items() if any(x.get('base')==n for x in t.findall('outline/component'))]
 lib=trees[n].find('lib/dict'); vals=list(lib);marks={vals[i].text:vals[i+1].text for i in range(0,len(vals),2)}
 assert marks['com.runebender.markLabel'] in ['orange','red']; assert marks['public.markColor'] in ['1,0.5,0,1','1,0,0,1']
 coords=([(704,0,'line'),(704,104,'line'),(352,104,'line'),(160,104,None),(64,48,None),(64,-64,'curve'),(64,-176,None),(160,-224,None),(352,-224,'curve'),(624,-224,'line'),(640,-208,'line'),(640,-136,'line'),(624,-120,'line'),(352,-120,'line'),(224,-120,None),(160,-104,None),(160,-64,'curve'),(160,-24,None),(224,0,None),(352,0,'curve')] if master=='Regular' else [(704,0,'line'),(704,176,'line'),(352,176,'line'),(176,176,None),(64,80,None),(64,-64,'curve'),(64,-208,None),(176,-288,None),(352,-288,'curve'),(624,-288,'line'),(640,-272,'line'),(640,-128,'line'),(624,-112,'line'),(352,-112,'line'),(280,-112,None),(224,-104,None),(224,-64,'curve'),(224,-24,None),(280,0,None),(352,0,'curve')])
 lines=['\t<outline>','\t\t<contour>']
 for i,(x,y,typ) in enumerate(coords):
  att=f'x="{x}" y="{y}"'+(f' type="{typ}"' if typ else '')+(' smooth="yes"' if i in [2,5,8,13,16,19] else '')
  lines.append('\t\t\t<point '+att+'/>')
 lines+=['\t\t</contour>','\t</outline>']
 new=re.sub(r'\t<outline>.*?</outline>','\n'.join(lines),old,flags=re.S)
 new=re.sub(r'<advance width="[^"]+"/>','<advance width="704"/>',new)
 new=new.replace('<string>'+marks['com.runebender.markLabel']+'</string>','<string>purple</string>').replace('<string>'+marks['public.markColor']+'</string>','<string>0.54,0.44,0.88,1</string>')
 for stage,txt in [('before-sources',old),('candidate-sources',new)]:
  dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
 (scratch/rel).write_text(new)
 m['glyphs'].append({'path':str(rel),'name':n,'master':master,'before_sha256':sha(p),'candidate_sha256':sha(scratch/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');print(scratch)
