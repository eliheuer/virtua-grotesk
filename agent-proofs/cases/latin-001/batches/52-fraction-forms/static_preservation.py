from pathlib import Path
import json
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
C=Path(__file__).resolve().parent;S=Path(json.loads((C/'baseline.json').read_text())['scratch']);checks={}
for p in (S/'fonts/ttf').glob('*.ttf'):
 a=TTFont(p);b=TTFont(C/'baseline-fonts/ttf'/p.name);ag=a.getGlyphSet();bg=b.getGlyphSet();count=0
 for n in bg:
  x=DecomposingRecordingPen(ag);y=DecomposingRecordingPen(bg);ag[n].draw(x);bg[n].draw(y);assert x.value==y.value and ag[n].width==bg[n].width,(p.name,n);count+=1
 checks[p.name]=count
(C/'static-preservation.json').write_text(json.dumps({'old_static_ink_and_advances_exact':True,'glyph_checks':checks},indent=2)+'\n');print(checks)
