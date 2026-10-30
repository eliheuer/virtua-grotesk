from pathlib import Path
import subprocess,re,json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch37/comparison'
D.parent.mkdir(parents=True,exist_ok=True)
cmd=[str(R/'.venv/bin/diff3proof'),str(C/'assets/after.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(D)]
subprocess.run(cmd,check=True)
s=(D/'diff3proof.html').read_text();text='¤ ¤¤ H¤H O¤O 0¤0 · Total ¤100.00 · tax ¤8.00. Pay ¤10 or ¤20 today. USD $10 · EUR €10 · ¤10. București ģimene doğa Ŧŧ ﬁﬂ'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1
s=s.replace('Diffenator3 Proof','Diffenator3 · currency supplement')
(D/'currency.html').write_text(s)
(C/'diffenator.json').write_text(json.dumps({'command':cmd,'supplement_text':text,'note':'Stock controls, labeled substituted text. Old Virtua/New Rubik.','html_sha256':hashlib.sha256(s.encode()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
