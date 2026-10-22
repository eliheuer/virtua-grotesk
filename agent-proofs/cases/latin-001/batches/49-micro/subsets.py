from pathlib import Path
import json,io,unicodedata,hashlib
from fontTools import subset
from fontTools.ttLib import TTFont
from tests.test_latin_diacritics import shaped
C=Path(__file__).resolve().parent;S=Path(json.loads((C/'baseline.json').read_text())['scratch']);rows=[]
texts=['µµµ','10 µm 25 µg','5 µs 4 µF','Micro: 10 µm','uµ pµ µu µp','µ́ µ̧ µ']
for p in sorted((S/'fonts').rglob('*.ttf')):
 data=p.read_bytes();f=TTFont(p)
 for text in texts:
  sf=TTFont(p);o=subset.Options();ss=subset.Subsetter(options=o);ss.populate(text=text);ss.subset(sf);s=io.BytesIO();sf.save(s);sd=s.getvalue();sf=TTFont(io.BytesIO(sd))
  for w in ([400,475,550,625,700] if 'fvar' in f else [f['OS/2'].usWeightClass]):
   expected=shaped(f,data,text,w)
   assert shaped(sf,sd,text,w)==expected,(p,w,text)
   assert shaped(f,data,unicodedata.normalize('NFD',text),w)==expected
   rows.append({'font':p.name,'sha256':hashlib.sha256(data).hexdigest(),'weight':w,'text':text,'subset_and_NFD_equal':True})
 assert unicodedata.normalize('NFKD','µ')=='μ'
 assert not any(r.FeatureTag=='sups' for r in f['GSUB'].table.FeatureList.FeatureRecord)
(C/'subset-checks.json').write_text(json.dumps({'cases':len(rows),'rows':rows,'scope':'Encoded glyphs survive text subsets and NFD. NFKD maps to unsupported Greek mu; no normalization repair or alias added.'},indent=2)+'\n')
print(len(rows),'real subset and NFD cases passed')
