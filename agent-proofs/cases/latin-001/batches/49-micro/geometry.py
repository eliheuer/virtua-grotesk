from pathlib import Path
import json,xml.etree.ElementTree as E,copy,sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import pathops
C=Path(__file__).resolve().parent;R=C.parents[4];S=Path(json.loads((C/'baseline.json').read_text())['scratch']);D=C/'decomposed';D.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'scripts'));from curve_profile import profile
profiles={};roots=[]
for m in ['Regular','Bold']:
 d=S/f'sources/VirtuaGrotesk-{m}.ufo/glyphs';r=E.parse(d/'mu.glif').getroot();o=r.find('outline');o.remove(o.find('component'));u=E.parse(d/'u.glif').getroot()
 for c in u.findall('outline/contour'):o.append(copy.deepcopy(c))
 p=D/f'{m}.glif';E.ElementTree(r).write(p);profiles[m]=profile(p);roots.append(r)
 assert [p.get('type') for p in roots[0].findall('outline/contour/point')]==[p.get('type') for p in r.findall('outline/contour/point')]
f=TTFont(C/'assets/after.ttf');rows=[]
for w in [400,475,550,625,700]:
 gs=f.getGlyphSet(location={'wght':w});p=pathops.Path();gs['mu'].draw(p.getPen());p.simplify();assert len(list(p.contours))==1
 r=copy.deepcopy(roots[0]);t=(w-400)/300
 for q,a,b in zip(r.findall('outline/contour/point'),roots[0].findall('outline/contour/point'),roots[1].findall('outline/contour/point')):
  for k in ['x','y']:q.set(k,str(float(a.get(k))*(1-t)+float(b.get(k))*t))
 out=D/f'mu-{w}.glif';E.ElementTree(r).write(out);v=profile(out)
 rows.append({'weight':w,'diagnostic_union_contours':len(list(p.contours)),'profile_warnings':v['warnings'],'note':'One contour, no enclosed counter; open top retained. New extension is straight; all cubic geometry inherited unchanged from green u.'})
(C/'geometry.json').write_text(json.dumps({'master_profiles':profiles,'five_weights':rows,'scope':'Scratch decomposition only; no donor curve edits. Original overlapping contours kept in variable font; statics follow canonical overlap removal.'},indent=2)+'\n')
print(rows)
