from pathlib import Path
import subprocess,re,json,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch34/comparison'
cmd=[str(R/'.venv/bin/diff3proof'),str(C/'assets/virtua.ttf'),str(C/'assets/rubik.ttf'),'--sample-mode','cover','--output',str(D)]
subprocess.run(cmd,check=True)
s=(D/'diff3proof.html').read_text();text='extra\u00adordinary extraordinary co\u00adoperate cooperate of\u00adfice office · Extra\u00adordinary work needs careful comparison. Co\u00adoperate with the reader: no visible hyphen inside an unbroken word. București ģimene doğa Ŧŧ ﬁﬂ'
s,n=re.subn(r'<p>.*?</p>',f'<p>{text}</p>',s,count=1,flags=re.S);assert n==1
s=s.replace('Diffenator3 Proof','Diffenator3 · soft-hyphen supplement')
(D/'soft-hyphen.html').write_text(s)
(C/'diffenator.json').write_text(json.dumps({'command':cmd,'supplement_text':text,'note':'Stock controls, labeled substituted text. Does not exercise controlled wrapping; use the separate behavior fixture. Old Virtua/New Rubik.','html_sha256':hashlib.sha256(s.encode()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
