from pathlib import Path
import shutil, re, hashlib, json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[3]
out=root/'out/qa/2026-10-20/hebrew-006-v3'
assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={str(p.relative_to(root)):sha(p) for p in (root/'sources').rglob('*') if p.is_file() and 'archive' not in p.parts}
out.mkdir(parents=True)
shutil.copytree(root/'sources',out/'sources',ignore=shutil.ignore_patterns('archive','instance_ufos','build.ninja','.ninja_log','*.png'))
shutil.copytree(out/'sources',out/'before-sources')
for d in ['scripts','tests']:shutil.copytree(root/d,out/d)
for n in ['build.sh','Makefile','requirements.txt','OFL.txt','README.md','AUTHORS.txt']:
 if (root/n).exists():shutil.copy2(root/n,out/n)
(out/'.venv').symlink_to(root/'.venv',target_is_directory=True)
shutil.copytree(root/'documentation',out/'documentation',ignore=shutil.ignore_patterns('*.png','*.pdf','*.ttf','*.woff2','social-assets'))
rel='sources/VirtuaGrotesk-Bold.ufo/glyphs/zayin-hb.glif'
p=out/rel;s=p.read_text()
replacements=[
 ('x="328" y="304" type="line"','x="328" y="328" type="line"'),
 ('x="328" y="368"','x="328" y="392"'),
 ('x="336" y="400"','x="336" y="432"'),
 ('x="352" y="432" type="curve"','x="384" y="432" type="curve"'),
 ('<point x="160" y="432" type="line"/>','<point x="152" y="432" type="line"/>\n\t\t\t<point x="160" y="424" type="line"/>'),
 ('x="144" y="400"','x="136" y="392"')]
for old,new in replacements:
 assert s.count(old)==1,old
 s=s.replace(old,new)
p.write_text(s)
reg=out/'sources/VirtuaGrotesk-Regular.ufo/glyphs/zayin-hb.glif'
assert sha(reg)==hashes[str(reg.relative_to(out))]
a=ET.parse(reg).getroot();b=ET.parse(p).getroot()
assert [x.get('type') for x in a.findall('.//point')]==[x.get('type') for x in b.findall('.//point')]
assert len(b.findall('.//point'))==21
scope={'status':'Candidate only; not applied','source_hashes':hashes,'changed_files':[rel], 'regular_sha256':sha(reg),'bold_candidate_sha256':sha(p),'lesson':'HEB-006 manual correction 01; preserve tangent/cut distinction and relative neck geometry'}
(out/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
print(out)
