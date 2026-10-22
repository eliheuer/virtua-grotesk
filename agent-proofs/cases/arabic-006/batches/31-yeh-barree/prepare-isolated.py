from pathlib import Path
import json,plistlib,xml.etree.ElementTree as E,re,hashlib
R=Path('/Users/eli/GH/repos/virtua-grotesk');C=R/'agent-proofs/cases/arabic-006/batches/31-yeh-barree';m=json.loads((C/'candidate.json').read_text());S=Path(m['scratch']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for w in ['Regular','Bold']:
 d=R/f'sources/VirtuaGrotesk-{w}.ufo/glyphs';cs=plistlib.loads((d/'contents.plist').read_bytes());p=d/cs['yehBarree-ar'];rel=str(p.relative_to(R));old=p.read_text();assert sha(p)==m['source_hashes'][rel];assert rel not in m['reserved'];t=E.fromstring(old);lib=list(t.find('lib/dict'));marks={lib[i].text:lib[i+1].text for i in range(0,len(lib),2)};assert marks['com.runebender.markLabel'] in ['orange','red']
 b=w=='Bold';bar=128 if b else 96;end=352 if b else 224
 coords=[(880,0,'line'),(896,16,'line'),(896,bar-16,'line'),(880,bar,'line'),(end,bar,'line')]
 coords+=([(288,128,None),(256,144,None),(256,176,'curve'),(256,208,None),(280,240,None),(304,264,'curve'),(488,448,'line'),(488,464,'line')] if b else [(184,96,None),(160,112,None),(160,144,'curve'),(160,192,None),(184,232,None),(216,264,'curve'),(440,488,'line'),(440,504,'line')])
 coords += [(392,560,'line'),(376,560,'line'),(128,312,'line'),(88,272,None),(64,240,None),(64,176,'curve'),(64,80,None),(128,0,None),(224,0,'curve')]
 lines=['\t<outline>','\t\t<contour>']
 for i,(x,y,typ) in enumerate(coords):
  att=f'x="{x}" y="{y}"'+(f' type="{typ}"' if typ else '')+(' smooth="yes"' if i in [4,7,10,18,21] else '')
  lines.append('\t\t\t<point '+att+'/>')
 lines+=['\t\t</contour>','\t</outline>'];new=re.sub(r'\t<outline>.*?</outline>','\n'.join(lines),old,flags=re.S);new=re.sub(r'<advance width="[^"]+"/>','<advance width="960"/>',new);new=new.replace('<string>'+marks['com.runebender.markLabel']+'</string>','<string>purple</string>').replace('<string>'+marks['public.markColor']+'</string>','<string>0.54,0.44,0.88,1</string>')
 for stage,txt in [('before-sources',old),('candidate-sources',new)]:
  dst=C/stage/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(txt)
 (S/rel).write_text(new);m['glyphs'].append({'path':rel,'name':'yehBarree-ar','master':w,'before_sha256':sha(p),'candidate_sha256':sha(S/rel)})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
