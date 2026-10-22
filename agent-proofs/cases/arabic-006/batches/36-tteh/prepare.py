from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,tempfile,re
R=Path.cwd();C=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not(C/'candidate.json').exists()
S=Path(tempfile.mkdtemp(prefix='virtua-tteh-',dir='/tmp'));(S/'sources').mkdir()
for p in R.glob('sources/VirtuaGrotesk-*.ufo'):shutil.copytree(p,S/'sources'/p.name)
for f in ['VirtuaGrotesk.designspace','config.yaml']:shutil.copy2(R/'sources'/f,S/'sources'/f)
for f in ['build.sh','Makefile','OFL.txt']:shutil.copy2(R/f,S/f)
shutil.copytree(R/'scripts',S/'scripts');(S/'.venv').symlink_to(R/'.venv');(S/'documentation/proofs').mkdir(parents=True)
m={'status':'candidate','scratch':str(S),'source_hashes':{str(p.relative_to(R)):sha(p) for p in R.glob('sources/VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved':{},'glyphs':[]}
# Local small Tah: upright at left, open rounded bowl at right. No external outlines.
# Off-curves have no type; explicit smooth extrema only.
for w in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());trees={n:E.parse(d/f) for n,f in cs.items()}
 dep={n+s for n in ['beh-ar','behDotless-ar','heh-ar','hehDoachashmee-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={x.get('base') for n in dep for x in trees[n].findall('outline/component')}-dep
  if not add:break
  dep|=add
 for n in dep:m['reserved'][str((d/cs[n]).relative_to(R))]=sha(d/cs[n])
 bold=w=='Bold';right=256 if bold else 240;stem=88 if bold else 80;floor=56 if bold else 48;crown=160 if bold else 136;cap=240 if bold else 224;mid=80 if bold else 64;innerRight=200;innerTop=104 if bold else 96;ic=80 if bold else 72
 outer=[(8,0,'line',False),(168,0,'line',True),(224 if bold else 208,0,None,False),(right,32 if bold else 24,None,False),(right,mid,'curve',True),(right,128 if bold else 104,None,False),(224 if bold else 216,crown,None,False),(168,crown,'curve',True),(stem,crown,'line',False),(stem,cap-8,'line',False),(stem-8,cap,'line',False),(40,cap,'line',False),(32,cap-8,'line',False),(32,floor,'line',False),(8,floor,'line',False),(0,floor-8,'line',False),(0,8,'line',False)]
 inner=[(stem,floor,'line',False),(stem,innerTop,'line',False),(168,innerTop,'line',True),(192,innerTop,None,False),(innerRight,ic+16,None,False),(innerRight,ic,'curve',True),(innerRight,ic-16,None,False),(192,floor,None,False),(168,floor,'curve',True)]
 for suffix in ['', '.init','.medi','.fina']:
  n='tteh-ar'+suffix;base='behDotless-ar'+suffix;p=d/cs[n];rel=str(p.relative_to(R));t=trees[n];old=p.read_text();lib=list(t.find('lib/dict'));marks={lib[i].text:lib[i+1].text for i in range(0,len(lib),2)};assert n not in dep;assert marks['com.runebender.markLabel'] in ['orange','red','purple'];assert marks['public.markColor'] not in ['0,1,0,1','0.09,0.72,0.44,1']
  assert not [a for a,tt in trees.items() if any(x.get('base')==n for x in tt.findall('outline/component'))]
  cx={'':472,'.fina':496,'.init':144 if bold else 136,'.medi':208}[suffix];dx=cx-right//2;dy=({'':408,'.fina':408,'.init':504,'.medi':408} if bold else {'':352,'.fina':400,'.init':496,'.medi':400})[suffix]
  outline=f'\t<outline>\n\t\t<component base="{base}"/>'
  for pts in [outer,inner]:
   outline+='\n\t\t<contour>'
   for x,y,typ,smooth in pts:
    outline+=f'\n\t\t\t<point x="{x+dx}" y="{y+dy}"'+(f' type="{typ}"' if typ else '')+(' smooth="yes"' if smooth else '')+'/>'
   outline+='\n\t\t</contour>'
  outline+='\n\t</outline>';new=re.sub(r'\t<outline>.*?\t</outline>',outline,old,flags=re.S);width=trees[base].find('advance').get('width');new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{width}"/>',new)
  new=re.sub(r'\t<anchor [^>]+/>\n','',new);anchors=[dict(a.attrib) for a in trees[base].findall('anchor')]
  for a in anchors:
   if a['name'] in ['top','topDots']:a.update(x=str(cx),y=str(dy+cap+(48 if a['name']=='top' else 0)))
  aa='\n'.join('\t<anchor '+' '.join(f'{k}="{v}"' for k,v in a.items())+'/>' for a in anchors);new=new.replace('\t<lib>',aa+'\n\t<lib>')
  new=re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',r'\g<1>purple',new);new=re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',r'\g<1>0.54,0.44,0.88,1',new)
  for stage,txt in [('before-sources',old),('candidate-sources',new)]:
   dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
  (S/rel).write_text(new);m['glyphs'].append({'name':n,'master':w,'path':rel,'base':base,'mark_offset':[dx,dy],'before_sha256':sha(p),'candidate_sha256':sha(S/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir(exist_ok=True);shutil.copy2(C.parent/'35-feh-below-bases/assets/after.ttf',C/'assets/before.ttf')
e=json.loads((C.parent/'35-feh-below-bases/evidence.json').read_text());e['description']='Tteh small Tah';e['study']={'id':'Arabic · First pass','language':'ar','readingDefault':'arabic','status':'Tteh · Candidate','note':'Small Tah replaces ordinary dots; Beh base donors unchanged.','glyphs':[{'key':'tteh','char':'ٹ','name':'Tteh'}],'presets':{'group':['ٹٹٹ ٹ','Tteh · All four forms'],'forms':['ٹٹٹ ٹ','Tteh · All four forms'],'join':['مٹ ٹم','Joining contexts'],'marks':['ٹَٹِٹُ ٹ','Attachment']}}
e['reading']={'arabic':{'label':'Tteh','paragraphs':[{'lang':'ar','dir':'rtl','runs':[{'text':'ٹٹٹ ٹ  مٹ ٹم'}]}]}};(C/'evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
for f in ['render.py','render-large.py']:
 p=C/f;p.write_text(p.read_text().replace('Feh · Below-dot bases','Tteh · Small Tah'))
print(S,len(m['glyphs']))
