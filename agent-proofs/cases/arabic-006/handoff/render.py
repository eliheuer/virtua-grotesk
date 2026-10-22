from pathlib import Path
import json,sys,hashlib,subprocess
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;r=C.parent/'batches/36-tteh/working';m=json.loads((r/'live-fonts.json').read_text());w=int(sys.argv[1]);kind=sys.argv[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
alphabet='ابتثجحخدذرزسشصضطظعغفقكلمنهوي'
if kind=='alphabet':
 lines=[' '.join(alphabet[:14]),' '.join(alphabet[14:])];title='Arabic alphabet · Isolated forms';size=88
elif kind.startswith('forms'):
 ix=int(kind[-1])-1;chars=alphabet[ix*7:(ix+1)*7];samples=[('م'+c+' '+c) if c in 'ادذرزو' else c*3+' '+c for c in chars];lines=['   '.join(samples[:4]),'   '.join(samples[4:])];title=f'Arabic joining forms · {ix+1} of 4';size=64
elif kind=='words':lines=['العربية جميلة  مرحبا بالعالم','كتاب قلم مدرسة  الشمس والقمر'];title='Arabic · Words';size=88
elif kind=='marks':lines=['بَ بِ بُ بّ  سَ شِ عَ غُ','أ إ آ ؤ ئ ء  ة ى لا'];title='Arabic · Marks and composites';size=72
elif kind=='digits':lines=['٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩','۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹'];title='Arabic and Persian digits';size=88
elif kind=='extensions':lines=['پ چ ژ ک گ ں ے','ٹ ڈ ڑ ھ ہ ۂ ۃ'];title='Arabic extensions · Manual review';size=88
else:raise ValueError(kind)
recipe=C/('digits.rs' if kind=='digits' else 'alphabet.rs')
cmd=['designbot','--raw',str(recipe),'--output',str(C/f'{kind}-{w}.png'),'--',str(w),str(size),title,*lines,'reserved'];inputs=[]
for role in ['after','rubik','noto','plex','readex']:
 f=m[role];face=min(f['faces'],key=lambda x:abs(int(x['weight'])-w)) if f.get('faces') else f;p=(r/face['url']).resolve();assert sha(p)==face['sha256'];cmap=TTFont(p).getBestCmap();missing=sorted({ord(ch) for ch in ''.join(lines) if not ch.isspace()}-set(cmap));assert not missing or role!='after';actual=w if 'wght' in face.get('axes',{}) else int(face['weight']);label='Virtua Grotesk · Working' if role=='after' else f['family'];label+=(' · Persian digits unavailable' if kind=='digits' and missing and all(0x6f0<=cp<=0x6f9 for cp in missing) else ' [unavailable]') if missing else '';label+=f' · {actual} (nearest supplied weight)' if actual!=w else '';cmd += [str(p),f['family'],label];inputs.append(dict(role=role,path=str(p),sha256=sha(p),rendered_weight=actual,missing=missing))
subprocess.run(cmd,check=True);(C/f'{kind}-{w}.json').write_text(json.dumps(dict(fonts=inputs,lines=lines,weight=w,size=size,image_sha256=sha(C/f'{kind}-{w}.png'),recipe_sha256=sha(recipe)),ensure_ascii=False,indent=2)+'\n')
