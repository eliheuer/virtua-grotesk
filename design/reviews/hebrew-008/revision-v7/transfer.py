from pathlib import Path
import hashlib,json,shutil,re,sys,xml.etree.ElementTree as E
R=Path('/Users/eli/GH/repos/virtua-grotesk');C=R/'agent-proofs/cases/hebrew-008/revision-v7';C.mkdir(exist_ok=True)
sys.path.insert(0,str(C.parent));from draw import P,O,S,contour
human=R/'sources/VirtuaGrotesk-Regular.ufo/glyphs/finaltsadi-hb.glif'
assert not (C/'source-before.json').exists(),'Already frozen'
(C/'human-Regular-finaltsadi.glif').write_bytes(human.read_bytes())
shutil.copy2(C.parent/'revision-v6/after-sources/sources/VirtuaGrotesk-Regular.ufo/glyphs/finaltsadi-hb.glif',C/'agent-Regular-finaltsadi.glif')
(C/'source-before.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'sources').rglob('*') if p.is_file()},indent=2)+'\n')
notes={'human_sha256':hashlib.sha256(human.read_bytes()).hexdigest(),'old_points':20,'human_points':25,'width':560,'outer_turn':{'start':[328,240],'end':[528,448],'handles':[[456,240],[528,320]],'extent':[200,208],'handle_lengths':[128,128]},'inner_turn':{'start':[432,448],'end':[328,336],'handles':[[432,384],[392,336]],'extent':[104,112],'handle_lengths':[64,64]},'inner_landing':[[328,336],[256,336]],'lower_join':[[312,232],[320,240],[328,240]],'terminal_landings':[[[504,-176],[504,-160]],[[40,560],[40,544]]],'unchanged':['advance','anchors','Unicode','review color'],'interpretation':'Separate turns, tangent landings, junction cuts and terminal landings. Shared turn endpoint x and equal handle pairs are measured local construction, not a universal radius or proof of exact circularity.'}
(C/'manual-correction.json').write_text(json.dumps(notes,indent=2)+'\n')

def finalbold():
 return [P(416,-192),P(592,-192),P(608,-176),P(608,-160),P(416,232),P(424,240),S(432,240,'line'),O(560,240),O(672,320),S(672,448),P(672,560),P(656,576),P(496,576),P(480,560),S(480,448,'line'),O(480,416),O(464,400),P(432,400,'curve'),P(328,400),P(248,560),P(232,576),P(56,576),P(40,560),P(40,544),P(400,-176)]

def shin(b):
 r=816 if b else 640;i=r-(192 if b else 96);l=224 if b else 128;bottomR=r-256;bar=152 if b else 80;h=48 if b else 96
 mid=528 if b else 400;mi=mid-(192 if b else 96);end=288 if b else 200;upper=400 if b else 336;ih=32 if b else 64
 return [S(288,-16),S(bottomR,-16,'line'),O(bottomR+144,-16),O(r,96),S(r,240),P(r,560),P(r-16,576),P(i+16,576),P(i,560),S(i,240,'line'),O(i,240-h),O(bottomR+h,bar),S(bottomR,bar),S(288,bar,'line'),O(288-h,bar),O(l,224-h),S(l,224),P(l,232),P(l+8,240),S(end,240,'line'),O(end+128,240),O(mid,320),S(mid,448),P(mid,560),P(mid-16,576),P(mi+16,576),P(mi,560),S(mi,448,'line'),O(mi,448-ih),O(end+ih,upper),P(end,upper,'curve'),P(l+8,upper),P(l,upper+8),P(l,560),P(l-16,576),P(48,576),P(32,560),S(32,240,'line'),O(32,96),O(144,-16)]

scratch=R/'out/qa/hebrew-008-v7/sources';records=[]
for master in ['Regular','Bold']:
 src=R/f'sources/VirtuaGrotesk-{master}.ufo';dst=scratch/src.name;shutil.copytree(src,dst)
 for name in ['shin-hb','finaltsadi-hb']:
  if master=='Regular' and name=='finaltsadi-hb':continue
  p=src/'glyphs'/f'{name}.glif';old=p.read_bytes();pts=shin(master=='Bold') if name=='shin-hb' else finalbold()
  s=re.sub(r'\t<outline>.*?</outline>',lambda _:'\t<outline>\n'+contour(pts)+'\t</outline>',old.decode(),flags=re.S)
  new=s.encode();(dst/'glyphs'/p.name).write_bytes(new)
  snap=C/'before-sources'/p.relative_to(R);snap.parent.mkdir(parents=True,exist_ok=True);snap.write_bytes(old)
  records.append({'path':str(p.relative_to(R)),'before':hashlib.sha256(old).hexdigest(),'after':hashlib.sha256(new).hexdigest(),'points':len(pts)})
for name in ['shin-hb','finaltsadi-hb']:
 roots=[E.parse(scratch/f'VirtuaGrotesk-{m}.ufo/glyphs/{name}.glif').getroot() for m in ['Regular','Bold']]
 assert [p.get('type') for p in roots[0].findall('.//point')]==[p.get('type') for p in roots[1].findall('.//point')]
(C/'planned-changes.json').write_text(json.dumps(records,indent=2)+'\n')
shutil.copy2('/tmp/virtua-v7.py',C/'transfer.py')
print(records)
