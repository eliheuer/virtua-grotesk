from pathlib import Path
import subprocess,re,json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch43/comparison'
D.parent.mkdir(parents=True,exist_ok=True)
cmd=[str(R/'.venv/bin/diff3proof'),str(C/'assets/after.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(D)]
subprocess.run(cmd,check=True)
s=(D/'diff3proof.html').read_text();text='⁶ ⁰ ¹ ² ³ ⁴ ⁵ · x⁶ x¹ x² x³ · 10⁶ 10¹ 10² 10³ · Powers: 2⁶ = 64. Text⁶ text¹ text² text³ · notes⁶¹²³ · 0⁶ 1¹ 2² 3³ · 0123 · București⁶ ģimene¹ doğa²'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1
s=s.replace('Diffenator3 Proof','Diffenator3 · superior-six supplement')
(D/'superior-six.html').write_text(s)
(C/'diffenator.json').write_text(json.dumps({'command':cmd,'supplement_text':text,'note':'Stock controls, labeled substituted text. Old Virtua/New Rubik.','html_sha256':hashlib.sha256(s.encode()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
