from pathlib import Path
import io,json
from fontTools.ttLib import TTFont
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent
out={}
for name in ['before','after']:
 p=C/'assets'/f'{name}.ttf';font=TTFont(p);fallback=TTFont(p)
 for t in fallback['cmap'].tables:
  if t.isUnicode():
   for ch in 'ĄąĘęĮįŲų':t.cmap.pop(ord(ch),None)
 stream=io.BytesIO();fallback.save(stream);fail=[]
 for w in [400,475,550,625,700]:
  for char in 'ĄąĘęĮįŲų':
   sample=char+'́';a=shaped(font,p.read_bytes(),sample,w);b=shaped(fallback,stream.getvalue(),sample,w)
   if a!=b:fail.append({'weight':w,'text':sample,'full':a,'subset':b})
 out[name]=fail
out['finding']='Existing missing-cmap plus above-acute normalization selects accented base + generic ogonek. Basic ogonek canonical fallback repaired, this broader stacked subset case is not. Requires a normalization/serving-subset pass; no green base changes.'
(C/'subset-accent-followup.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({n:len(v) for n,v in out.items() if isinstance(v,list)})
