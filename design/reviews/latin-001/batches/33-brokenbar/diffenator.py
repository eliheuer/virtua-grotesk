from pathlib import Path
import subprocess,json,hashlib,re
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch33';D.mkdir(parents=True,exist_ok=True)
commands=[]
for name,args in [('virtua',[]),('comparison',[str(C/'assets/rubik.ttf'),'--sample-mode','cover'])]:
 cmd=[str(R/'.venv/bin/diff3proof'),str(C/'assets/after.ttf'),*args,'--output',str(D/name)];subprocess.run(cmd,check=True);commands.append(cmd)
# Preserve stock reports. A separately named supplement changes only the sample
# text and heading; original Diffenator font switching and axis UI remain intact.
text='alpha ¦ beta ¦ gamma · one¦two left¦right · H|H H¦H I|I I¦I · a¦b c¦d 0¦1 · ¦¦ ¦| |¦ · București ¦ ģimene ¦ doğa Ŧŧ ﬁﬂ'
p=D/'comparison/diff3proof.html';s=p.read_text();s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1
s=s.replace('Diffenator3 Proof','Diffenator3 · broken-bar supplement').replace('Font before:', 'Virtua:').replace('Font after:', 'Reference:')
(D/'comparison/brokenbar.html').write_text(s)
(C/'diffenator/generated.json').write_text(json.dumps({'tool':'diff3proof 1.1.4','commands':commands,'supplement_text':text,'supplement':'Stock HTML font controls with explicitly replaced sample text and heading; original stock reports unchanged.','fonts':{n:hashlib.sha256((C/'assets'/f'{n}.ttf').read_bytes()).hexdigest() for n in ['after','rubik']},'reports':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in D.rglob('*.html')}},ensure_ascii=False,indent=2)+'\n')
