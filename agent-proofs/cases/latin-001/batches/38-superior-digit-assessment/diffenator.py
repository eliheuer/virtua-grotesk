from pathlib import Path
import subprocess,re,json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch38/comparison';D.parent.mkdir(parents=True,exist_ok=True)
cmd=[str(R/'.venv/bin/diff3proof'),str(C/'assets/virtua.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(D)]
subprocess.run(cmd,check=True)
s=(D/'diff3proof.html').read_text();text='123 101 202 303 · x¹ x² x³ · 10¹ 10² 10³ · ¹²³ · Note: Virtua has no encoded superior digits; any displayed superior ink in Old is browser fallback, not Virtua coverage. New is Rubik. București ģimene doğa Ŧŧ ﬁﬂ'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1
s=s.replace('Diffenator3 Proof','Diffenator3 · superior-digit assessment')
(D/'superiors.html').write_text(s)
(C/'diffenator.json').write_text(json.dumps({'command':cmd,'supplement_text':text,'note':'Stock controls and coverage proof plus labeled same-text supplement. Old Virtua/New Rubik; missing coverage explicitly labeled. No new candidate.','html_sha256':hashlib.sha256(s.encode()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
