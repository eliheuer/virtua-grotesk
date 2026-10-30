"""Goal raster: retain six panels and mark missing Rubik/Readex coverage explicitly."""
from pathlib import Path
import json,subprocess,hashlib,sys
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;r=C/'working';m=json.loads((r/'live-fonts.json').read_text());w=int(sys.argv[1]);text=sys.argv[2] if len(sys.argv)>2 else 'ہ بہ';size=int(sys.argv[3]) if len(sys.argv)>3 else 80;name=sys.argv[4] if len(sys.argv)>4 else f'goal-{w}';cmd=['designbot','--raw',str(C/'detail.rs'),'--output',str(C/(name+'.png')),'--',str(w),str(size),text,'Heh Doachashmee · Four forms'];inputs=[]
for role in ['before','after','rubik','noto','plex','readex']:
 f=m[role];face=min(f['faces'],key=lambda x:abs(int(x['weight'])-w)) if f.get('faces') else f;p=r/face['url'];h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==face['sha256'];missing=sorted({ord(ch) for ch in text if not ch.isspace() and ord(ch) not in [8204,8205]}-set(TTFont(p).getBestCmap()));assert not missing or (role in ['rubik','readex'] and set(missing)<= {1726,1662})
 actual=w if 'wght' in face.get('axes',{}) else int(face['weight']);label=f['label'] if role in ['before','after'] else f['family'];label+=f' · {actual} (nearest supplied weight)' if actual!=w else '';cmd += [str(p),f['family'],label];inputs.append(dict(role=role,sha256=h,rendered_weight=actual,missing=missing))
subprocess.run(cmd,check=True);(C/(name+'.json')).write_text(json.dumps(dict(fonts=inputs,text=text,weight=w,size=size,image_sha256=hashlib.sha256((C/(name+'.png')).read_bytes()).hexdigest(),recipe_sha256=hashlib.sha256((C/'detail.rs').read_bytes()).hexdigest(),notes='Rubik and Readex Pro lack U+06BE; their panels are explicitly unavailable.'),indent=2)+'\n')
