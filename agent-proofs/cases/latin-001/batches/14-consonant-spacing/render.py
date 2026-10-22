from pathlib import Path
import json,hashlib,subprocess,sys
from fontTools.ttLib import TTFont
C=Path(__file__).resolve().parent;w=int(sys.argv[1]);kind=sys.argv[2];size=224 if kind=='large' else 48
lines=('mañana. señor. rząd. dzień.','Yağmur. Žilina. Řeřicha.') if kind=='reading' else ('n ñ g ģ i į','reserved')
raw=C.parent/('02-straight-accents/proof.rs' if kind!='large' else '11-alternate-carons/large.rs')
cmd=['designbot','--raw',str(raw),'--output',str(C/f'{kind}-{w}.png'),'--',str(w),str(size),'Lowercase advance repair · '+kind.title(),*lines,'reserved'];inputs=[]
for n,family,label in [('before','Virtua Grotesk','Before'),('after','Virtua Grotesk','Working'),('rubik','Rubik','Rubik')]:
 p=C/'assets'/f'{n}.ttf';missing=sorted({ord(c) for c in ''.join(lines)}-set(TTFont(p).getBestCmap()));assert not missing,(n,missing)
 cmd.extend([str(p),family,label]);inputs.append({'role':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'missing_cmap':missing})
subprocess.run(cmd,check=True);(C/f'{kind}-{w}.json').write_text(json.dumps({'weight':w,'size':size,'texts':lines,'fonts':inputs,'image_sha256':hashlib.sha256((C/f'{kind}-{w}.png').read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
