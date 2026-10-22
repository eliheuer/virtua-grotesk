from pathlib import Path
from fontTools.ttLib import TTFont
import shutil,hashlib
C=Path(__file__).resolve().parent;R=C.parents[4];D=R/'out/review-latin-d2513094/batch51';f=TTFont(C/'assets/after.ttf');cm=f.getBestCmap()
for n in ['after','before','rubik']:shutil.copy2(C/'assets'/f'{n}.ttf',D/f'{n}.ttf')
tag=hashlib.sha256((C/"assets/after.ttf").read_bytes()).hexdigest()[:16]
for w in [400,550,700]:
 gs=f.getGlyphSet(location={'wght':w});frags=[]
 for j,px in enumerate([48,144]):
  x=40;baseline=70+j*170;frags.append(f'<text x="20" y="{baseline-(125 if px==144 else 55)}" class="label">{px}px · diagnostic only</text>')
  for a,b in [('¹','⁴'),('¹','²'),('³','⁴')]:
   aw=gs[cm[ord(a)]].width*px/1024;sw=264*px/1024
   frags.extend([f'<text x="{x}" y="{baseline}" font-size="{px}">{a}</text>',f'<text x="{x+aw}" y="{baseline}" font-size="{px}">⁄</text>',f'<text x="{x+aw+sw}" y="{baseline+384*px/1024}" font-size="{px}">{b}</text>']);x+=aw+sw+gs[cm[ord(b)]].width*px/1024+65
 html=f'''<!doctype html><meta charset="utf-8"><title>Fraction scratch {w}</title><style>@font-face{{font-family:trial;src:url("after.ttf?sha={tag}");font-weight:400 700}}body{{font:14px system-ui;background:#ddd;color:#333;margin:20px}}p{{font:32px trial;font-weight:{w};margin:10px 0}}svg{{font-family:trial;font-weight:{w};background:#ccc}}.label{{font:11px system-ui}}</style><h2>Fraction slash scratch · {w} · not applied</h2><label>Actual default shaping: ordinary figures collide with the narrow overhanging slash.</label><p>1⁄4 1⁄2 3⁄4 · H⁄H · 12⁄345</p><label>Unchanged ordinary slash and green construction references</label><p>1/4 1/2 3/4 · x seven 7</p><label>Diagnostic assembled fractions only. Existing superior ink; denominator shifted down384.</label><svg width="760" height="320">{''.join(frags)}</svg><footer>No numr/dnom/frac feature or encoded fraction. Do not apply this narrow slash alone.</footer>'''
 (D/f'trial-{w}.html').write_text(html);(C/f'trial-{w}.html').write_text(html.replace('url("after.ttf?', 'url("assets/after.ttf?'))
