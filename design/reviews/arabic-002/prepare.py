"""One-time guarded component repair; preserve donor and Regular bytes."""
from pathlib import Path
import hashlib,json,re,shutil,plistlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (C/'applied.json').exists(),'Existing snapshot must not be overwritten'
previous=R/'agent-proofs/cases/arabic-001'
# Verify active sources still match the previously checked Alef trial.
old=json.loads((previous/'applied.json').read_text());expected=dict(old['source_hashes'])
expected.update({g['path']:g['candidate_sha256'] for g in old['glyphs']})
assert all(sha(R/p)==h for p,h in expected.items()),'Sources changed since ARB-001; inspect before preparing'
font=R/'fonts/variable/VirtuaGrotesk[wght].ttf'
assert sha(font)==sha(previous/'assets/after.ttf')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(font,C/'assets/before.ttf')
manifest={'baseline_case':'arabic-001','baseline_commit':'4318e7a1','source_hashes':expected,'glyphs':[]}
for name,base in [('alefHamzaabove-ar','alef-ar'),('alefHamzaabove-ar.fina','alef-ar.fina')]:
 folder=R/'sources/VirtuaGrotesk-Bold.ufo/glyphs';contents=plistlib.loads((folder/'contents.plist').read_bytes());p=folder/contents[name]
 before=p.read_text();assert '<string>red</string>' in before
 b=ET.parse(folder/contents[base]).getroot();mark=ET.parse(folder/contents['hamzaabove-ar']).getroot()
 anchor=b.find("anchor[@name='top']");attach=mark.find("anchor[@name='_top']")
 dx=int(anchor.get('x'))-int(attach.get('x'));dy=int(anchor.get('y'))-int(attach.get('y'));width=int(b.find('advance').get('width'))
 assert all(v%8==0 for v in [dx,dy,width])
 after=re.sub(r'<advance width="\d+"/>',f'<advance width="{width}"/>',before)
 after=after.replace('<component base="hamzaabove-ar"/>',f'<component base="hamzaabove-ar" xOffset="{dx}"/>')
 after=after.replace('<string>red</string>','<string>purple</string>').replace('<string>1,0,0,1</string>','<string>0.54,0.44,0.88,1</string>')
 rel=p.relative_to(R)
 for state,text in [('before-sources',before),('candidate-sources',after)]:
  q=C/state/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 regfolder=R/'sources/VirtuaGrotesk-Regular.ufo/glyphs';regnames=plistlib.loads((regfolder/'contents.plist').read_bytes());reg=ET.parse(regfolder/regnames[name]).getroot()
 assert [c.get('base') for c in reg.findall('outline/component')]==[c.get('base') for c in ET.fromstring(after).findall('outline/component')]
 manifest['glyphs'].append({'name':name,'path':str(rel),'before_sha256':sha(p),'candidate_sha256':sha(C/'candidate-sources'/rel),'advance':width,'hamza_offset':[dx,dy]})
for g in manifest['glyphs']:assert sha(R/g['path'])==g['before_sha256']
for g in manifest['glyphs']:shutil.copyfile(C/'candidate-sources'/g['path'],R/g['path'])
assert {p for p,h in expected.items() if sha(R/p)!=h}=={g['path'] for g in manifest['glyphs']}
(C/'applied.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Installed only two Bold Alef-with-Hamza composites; all other sources unchanged.')
