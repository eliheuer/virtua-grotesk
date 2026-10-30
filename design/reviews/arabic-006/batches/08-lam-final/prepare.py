from pathlib import Path
import json,hashlib,plistlib,xml.etree.ElementTree as E,shutil,re,tempfile
R=Path.cwd();C=R/'agent-proofs/cases/arabic-006/batches/08-lam-final';C.mkdir(exist_ok=True)
assert not (C/'candidate.json').exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();scratch=Path(tempfile.mkdtemp(prefix='virtua-lam-final-',dir='/tmp'))
(scratch/'sources').mkdir();shutil.copy2(R/'sources/VirtuaGrotesk.designspace',scratch/'sources/VirtuaGrotesk.designspace');shutil.copy2(R/'sources/config.yaml',scratch/'sources/config.yaml')
m={'status':'scratch candidate only; Regular green exception required before active application','scratch':str(scratch),'source_hashes':{str(p.relative_to(R)):sha(p) for p in (R/'sources').glob('VirtuaGrotesk-*.ufo/**/*') if p.is_file()},'reserved_beh_hashes':{},'glyphs':[]}
for master in ['Regular','Bold']:
 r=R/f'sources/VirtuaGrotesk-{master}.ufo';shutil.copytree(r,scratch/'sources'/r.name);cs=plistlib.loads((r/'glyphs/contents.plist').read_bytes());rr=r/'glyphs';names={n+s for n in ['beh-ar','behDotless-ar'] for s in ['', '.init','.medi','.fina']}
 while True:
  add={co.get('base') for n in names for co in E.parse(rr/cs[n]).findall('outline/component')}-names
  if not add:break
  names|=add
 for n in names:m['reserved_beh_hashes'][str((rr/cs[n]).relative_to(R))]=sha(rr/cs[n])
 # Check inherited users; none may be green or reserved.
 descendants={'lam-ar.fina'}
 while True:
  add={n for n,f in cs.items() if any(co.get('base') in descendants for co in E.parse(rr/f).findall('outline/component'))}-descendants
  if not add:break
  descendants|=add
 assert descendants=={'lam-ar.fina'},descendants
 p=rr/cs['lam-ar.fina'];old=p.read_text();iso=E.parse(rr/cs['lam-ar']).find('outline/contour')
 pts=[dict(q.attrib) for q in iso]
 # Keep the reviewed isolated bowl and stem. Add a separate, bounded incoming arm.
 pts[6]['y']='-8';pts[6].pop('smooth',None)
 right=584 if master=='Regular' else 672;bar=96 if master=='Regular' else 176;advance=736 if master=='Regular' else 824
 def pt(x,y,t=None,s=False):
  d={'x':str(x),'y':str(y)}
  if t:d['type']=t
  if s:d['smooth']='yes'
  return d
 arm=[pt(right+8,0,'line'),pt(advance,0,'line'),pt(advance+16,16,'line'),pt(advance+16,bar-16,'line'),pt(advance,bar,'line'),pt(right+96,bar,'line',True),pt(right+40,bar),pt(right,bar+40),pt(right,bar+96,'curve',True)]
 pts=pts[:7]+arm+pts[7:]
 contour='\t\t<contour>\n'+''.join('\t\t\t<point '+' '.join(f'{k}="{v}"' for k,v in q.items())+'/>\n' for q in pts)+'\t\t</contour>'
 new=re.sub(r'\t\t<contour>.*?\t\t</contour>',lambda _:contour,old,flags=re.S)
 new=re.sub(r'<advance width="[^"]+"/>',f'<advance width="{advance}"/>',new)
 new=new.replace('<string>green</string>','<string>purple</string>').replace('<string>red</string>','<string>purple</string>').replace('<string>0.09,0.72,0.44,1</string>','<string>0.54,0.44,0.88,1</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 rel=p.relative_to(R)
 for folder,content in [('before-sources',old),('candidate-sources',new)]:
  q=C/folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(content)
 (scratch/rel).write_text(new)
 m['glyphs'].append({'name':'lam-ar.fina','master':master,'path':str(rel),'before_sha256':sha(p),'candidate_sha256':sha(scratch/rel),'points':len(pts)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n');(C/'assets').mkdir();shutil.copy2(C.parent/'07-lam/assets/after.ttf',C/'assets/before.ttf')
print(scratch)
