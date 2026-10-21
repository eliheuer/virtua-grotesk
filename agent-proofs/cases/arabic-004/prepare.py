"""One-shot snapshot and bounded component-offset candidate; --apply checks hashes."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,xml.etree.ElementTree as ET,plistlib
R=Path(__file__).resolve().parents[3];C=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true');args=a.parse_args()
if args.apply:
 m=json.loads((C/'candidate.json').read_text())
 assert all(sha(R/p)==h for p,h in m['source_hashes'].items()),'Sources changed; inspect before applying'
 for g in m['glyphs']:
  candidate=C/'candidate-sources'/g['path'];assert sha(candidate)==g['candidate_sha256']
 for g in m['glyphs']:shutil.copy2(C/'candidate-sources'/g['path'],R/g['path'])
 (C/'applied.json').write_text(json.dumps(m,indent=2)+'\n');print('Applied two helpers; donor drawings unchanged');raise SystemExit
assert not (C/'candidate.json').exists(),'Existing evidence must not be overwritten'
prev=R/'agent-proofs/cases/arabic-003/manual-correction-01'
font=R/'fonts/variable/VirtuaGrotesk[wght].ttf';assert sha(font)==sha(prev/'assets/after.ttf')
(C/'assets').mkdir(exist_ok=True);shutil.copy2(font,C/'assets/before.ttf');shutil.copy2(prev/'assets/Virtua-OFL.txt',C/'assets/Virtua-OFL.txt')
m={'baseline_commit':'d23f1bed','source_hashes':{str(p.relative_to(R)):sha(p) for p in sorted((R/'sources').glob('VirtuaGrotesk-*.ufo/**/*')) if p.is_file()},'glyphs':[]}
for master,offsets in [('Regular',[464,352]),('Bold',[608,432])]:
 rel=Path(f'sources/VirtuaGrotesk-{master}.ufo/glyphs/hamzaaboveF_athatan-ar.glif');p=R/rel
 before=p.read_text();assert 'green' not in before and '0.09,0.72,0.44,1' not in before
 root=ET.fromstring(before);assert [c.get('base') for c in root.findall('outline/component')]==['hamzaabove-ar','fatha-ar','fatha-ar']
 it=iter(offsets)
 after=re.sub(r'(<component base="fatha-ar" yOffset=")[^"]+("/>)',lambda x:x[1]+str(next(it))+x[2],before)
 for state,text in [('before-sources',before),('candidate-sources',after)]:
  q=C/state/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 for donor in ['hamzaabove-ar','fatha-ar']:
  source=R/rel.parent/f'{donor}.glif';q=C/'donors'/master/source.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,q)
 m['glyphs'].append({'master':master,'name':'hamzaaboveFathatan-ar','path':str(rel),'before_sha256':sha(p),'candidate_sha256':sha(C/'candidate-sources'/rel),'offsets':offsets})
(C/'candidate.json').write_text(json.dumps(m,indent=2)+'\n')
print('Prepared two compatible component-placement candidates; active sources unchanged')
