#!/usr/bin/env python3
"""Build isolated scratch OTF/browser panels for adapter examples, not a font release."""
import argparse,hashlib,html,json
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.pointPen import PointToSegmentPen

def draw(record,pen):
 p=PointToSegmentPen(pen)
 for contour in record['contours']:
  p.beginPath()
  for n in contour:p.addPoint((float(n['x']),float(n['y'])),segmentType=n.get('type'),smooth=n.get('smooth')=='yes')
  p.endPath()

def render(examples_path,out):
 examples=json.loads(Path(examples_path).read_text());out=Path(out);out.mkdir(parents=True,exist_ok=True)
 names=['.notdef'];chars={};metrics={'.notdef':(1024,0)};cm={};panels=[]
 pen=T2CharStringPen(1024,None);chars['.notdef']=pen.getCharString()
 for i,e in enumerate(examples):
  cps=[]
  for j,key in enumerate(('input','target')):
   name=f'g{i}_{j}';cp=0xe000+i*2+j;r=e[key];pen=T2CharStringPen(r['advance'],None);draw(r,pen)
   names.append(name);chars[name]=pen.getCharString();metrics[name]=(int(r['advance']),0);cm[cp]=name;cps.append(chr(cp))
  # Mask is a diagram at common em scale, using the actual input contour.
  from fontTools.pens.svgPathPen import SVGPathPen
  pen=SVGPathPen(None);draw(e['input'],pen);nodes=[];idx=0
  for contour in e['input']['contours']:
   for p in contour:
    if e['editable_mask'][idx]:nodes.append(f'<circle cx="{p["x"]}" cy="{p["y"]}" r="10"/>')
    idx+=1
  svg='<svg viewBox="-64 -832 1152 1088"><g transform="scale(1,-1)"><path d="'+pen.getCommands()+'"/>'+''.join(nodes)+'</g></svg>'
  panels.append(f'<section data-mode="{e["mode"]}"><h2>{html.escape(e["glyph"])} · {e["mode"]}</h2><p>{html.escape(e["description"])}</p><div class="row"><article><h3>Synthetic input</h3><div class="glyph">{cps[0]}</div><div class="smallglyph">{cps[0]*3}</div></article><article><h3>Editable points · both boundaries</h3>{svg}</article><article><h3>Frozen green target · not model output</h3><div class="glyph">{cps[1]}</div><div class="smallglyph">{cps[1]*3}</div></article></div></section>')
 fb=FontBuilder(1024,isTTF=False);fb.setupGlyphOrder(names);fb.setupCharacterMap(cm);fb.setupCFF('VirtuaRepairSmoke',{},chars,{});fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=832,descent=-256);fb.setupNameTable({'familyName':'Virtua Repair Smoke','styleName':'Regular','uniqueFontIdentifier':'scratch-only','fullName':'Virtua Repair Smoke','psName':'VirtuaRepairSmoke'});fb.setupOS2(sTypoAscender=832,sTypoDescender=-256,usWinAscent=832,usWinDescent=256);fb.setupPost()
 font=out/'smoke.otf';fb.save(font);digest=hashlib.sha256(font.read_bytes()).hexdigest();font.rename(out/f'smoke-{digest[:12]}.otf')
 page='''<!doctype html><meta charset="utf-8"><title>Masked repair smoke — data only</title><style>
@font-face{font-family:Smoke;src:url('FONT')}body{background:#222;color:#ddd;font:16px system-ui;margin:24px}h1{font-size:26px}h2{font-size:20px}h3{font-size:14px;height:40px;margin:12px 0}p{max-width:95ch}section{border-top:1px solid #666;margin-top:24px}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}article{min-width:0}.glyph{font:224px Smoke;line-height:1.12;height:250px;white-space:nowrap}.smallglyph{font:48px Smoke;line-height:1.2;white-space:nowrap}svg{width:100%;height:250px}svg path{fill:#777}svg circle{fill:#ddd;stroke:#222;stroke-width:3}select{font:inherit;background:#ddd;color:#222;padding:6px}section[hidden]{display:none}</style>
<h1>Masked repair smoke sample — training data, not a repair</h1><p>Regular-only. Three frozen TRAIN glyphs; nine examples including no-op. Compiled scratch font at224px and48px, isolated forms (no Arabic shaping claim). Targets preserve the original green geometry and optical variation. No model or optimizer has run; nothing is applied.</p>
<label>Example mode <select id="mode"><option value="pinch">Pinch</option><option value="bulge">Bulge</option><option value="noop">No change</option></select></label>
<p>White dots mark editable points. Everything else—including stems, terminals, spacing and topology—is locked. These hand-selected masks illustrate the adapter; they are not automatic bowl detection.</p>'''.replace('FONT',f'smoke-{digest[:12]}.otf')+''.join(panels)+'''<script>const select=document.querySelector('#mode');function show(){document.querySelectorAll('section').forEach(s=>s.hidden=s.dataset.mode!==select.value)}select.addEventListener('change',show);show();</script>'''
 (out/'index.html').write_text(page);return digest
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('examples');ap.add_argument('--out',required=True);a=ap.parse_args();print(render(a.examples,a.out))
