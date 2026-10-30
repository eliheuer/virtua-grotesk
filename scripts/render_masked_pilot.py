#!/usr/bin/env python3
"""Render saved learned residual predictions, independently verify reconstruction."""
import argparse
import hashlib
import html
import json
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib import TTFont

import masked_repair as mr
from render_masked_smoke import draw


def render(run_dir, out):
    run_dir, out = Path(run_dir), Path(out)
    report = json.loads((run_dir / 'report.json').read_text())
    predictions = json.loads((run_dir / 'predictions.json').read_text())
    evaluation = report.get('evaluation_only', False)
    checkpoint_path = Path(report['checkpoint_path']) if evaluation else run_dir/'checkpoint.pt'
    checkpoint_hash = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
    if checkpoint_hash != report['checkpoint_sha256']:
        raise ValueError('Checkpoint hash mismatch')
    out.mkdir(parents=True, exist_ok=True)
    names = ['.notdef']
    pen = T2CharStringPen(1024, None)
    chars = {'.notdef': pen.getCharString()}
    metrics, cmap, panels = {'.notdef': (1024, 0)}, {}, []
    for i, result in enumerate(predictions):
        ex = result['example']
        if mr.reconstruct(ex, result['predicted_deltas']) != result['prediction']:
            raise ValueError('Saved prediction differs from checked reconstruction')
        columns = []
        for j, (label, record) in enumerate([
            ('Clean input' if not any(any(d) for d in ex['target_deltas']) else 'Synthetic input', ex['input']),
            ('Learned prediction · rounded to 2 units', result['prediction']),
            ('Frozen green target', ex['target']),
        ]):
            name, cp = f'g{i}_{j}', 0xe000 + i * 3 + j
            pen = T2CharStringPen(record['advance'], None)
            draw(record, pen)
            names.append(name)
            chars[name] = pen.getCharString()
            metrics[name], cmap[cp] = (int(record['advance']), 0), name
            columns.append(f'<article><h3>{label}</h3><div class="glyph">{chr(cp)}</div>'
                           f'<div class="smallglyph">{chr(cp)*3}</div></article>')
        metric = report['metrics'][i]
        if (metric['glyph'], metric['mode']) != (ex['glyph'], ex['mode']):
            raise ValueError('Metric ordering mismatch')
        panels.append(f'<section data-mode="{ex["mode"]}" data-glyph="{ex["glyph"]}"><h2>{html.escape(ex["glyph"])} · {ex["mode"]}</h2>'
                      f'<p>Masked coordinate error: {metric["unchanged_input_masked_mae"]:g} → '
                      f'{metric["masked_mae"]:g} units. Locked points preserved: {metric["locked_deltas_zero"]}.</p>'
                      '<div class="row">'+''.join(columns)+'</div></section>')
    fb = FontBuilder(1024, isTTF=False)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap(cmap)
    fb.setupCFF('VirtuaRepairPilot', {}, chars, {})
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=832, descent=-512)
    fb.setupNameTable({'familyName': 'Virtua Repair Pilot', 'styleName': 'Regular',
                      'uniqueFontIdentifier': checkpoint_hash, 'fullName': 'Virtua Repair Pilot',
                      'psName': 'VirtuaRepairPilot'})
    fb.setupOS2(sTypoAscender=832, sTypoDescender=-512, usWinAscent=832, usWinDescent=512)
    fb.setupPost()
    temporary = out / 'pilot.otf'
    fb.save(temporary)
    digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
    font_path = out / f'pilot-{digest[:12]}.otf'
    temporary.rename(font_path)
    # Check the *compiled* prediction vs target, not merely the reported losses.
    font = TTFont(font_path)
    glyphs = font.getGlyphSet()
    matches = []
    for i in range(len(predictions)):
        a, b = RecordingPen(), RecordingPen()
        glyphs[f'g{i}_1'].draw(a)
        glyphs[f'g{i}_2'].draw(b)
        matches.append(a.value == b.value and glyphs[f'g{i}_1'].width == glyphs[f'g{i}_2'].width)
        if matches[-1] != report['metrics'][i]['exact_after_quantization']:
            raise ValueError('Compiled outline differs from coordinate metric')
    font.close()
    page = '''<!doctype html><meta charset="utf-8"><title>Regular repair pilot — learned predictions</title>
<style>@font-face{font-family:Pilot;src:url('FONT')}body{background:#222;color:#ddd;font:16px system-ui;margin:24px}
h1{font-size:26px}h2{font-size:20px}h3{font-size:14px;height:40px;margin:12px 0}p{max-width:100ch}
section{border-top:1px solid #666;margin-top:24px}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
article{min-width:0}.glyph{font:224px Pilot;line-height:1.12;height:250px;white-space:nowrap}
.smallglyph{font:48px Pilot;line-height:1.2;white-space:nowrap}select{font:inherit;background:#ddd;color:#222;padding:6px}
section[hidden]{display:none}a{color:inherit}</style>
<h1>Regular-only repair pilot · learned predictions</h1>
<p>RESULTS after 250 optimizer steps. Nine TRAIN examples from three green drawings. This is a memorization test;
no validation or test glyphs were used. The middle column is output from the saved and reloaded model, rounded to the 2-unit grid.</p>
<p>Original optical variation is the target. Locked geometry, spacing and topology are preserved by the adapter.
Scratch font at 224px and 48px; isolated forms, no Arabic shaping claim. Active font unchanged. No overnight run started.</p>
<label>Example mode <select id="mode"><option value="pinch">Pinch</option><option value="bulge">Bulge</option><option value="noop">No change</option></select></label>
'''.replace('FONT', font_path.name).replace('RESULTS', f'{sum(matches)}/{len(matches)} exact green recoveries')
    page += ''.join(panels) + '''<script>const select=document.querySelector('#mode');
function show(){document.querySelectorAll('section').forEach(s=>s.hidden=s.dataset.mode!==select.value)}
select.addEventListener('change',show);show();</script>'''
    # Keep the run length truthful if the same renderer is reused for another run.
    page = page.replace('after 250 optimizer steps', f'after {report["steps"]} optimizer steps')
    if evaluation:
        title = 'Frozen checkpoint evaluation · failures included'
        variable = report.get('model_kind') == 'virtua-variable-repair-v1'
        if variable:
            title = 'Variable-length pilot · clean-input and held-out checks'
        page = page.replace('Regular repair pilot — learned predictions', title)
        page = page.replace('Regular-only repair pilot · learned predictions', title)
        start = page.index('<p>')
        end = page.index('<label>Example mode')
        summary = '<p>No training or checkpoint updates. Three familiar TRAIN glyphs with new corruptions; one held-out Hah family. Initial Hah fits the model; medial Hah (44 points) and final Hah (50 points) exceed its 36-point limit and were refused without clipping.</p>'
        summary += '<p>Known glyphs: 12/18 new corruptions recovered exactly; six vertical/one-sided errors did not improve. Held-out initial Hah: all 7 outputs worse, including the clean green drawing. This checkpoint is not ready for an overnight run.</p>'
        summary += '<p>Columns show input → actual model prediction (rounded to 2 units) → green target. Hard mask preserves other points; it does not guarantee a good curve. 224px and 48px isolated forms. Active sources and built fonts unchanged.</p>'
        if variable:
            a=report['aggregates'];h=a['hah-probes'];c=a['hah-clean-wide'];t=a['train-clean-wide'];new=a['new-corruption-draw']
            summary=f'<p>{report["steps"]} steps on 33 green Regular Arabic drawings / 9 family groups. Hah stayed out of training; Seen/test unused. All three Hah forms fit without truncation. Last checkpoint evaluated once; no overnight run.</p>'
            summary+=f'<p>Clean drawings preserved: TRAIN {t["exact"]}/{t["count"]}, held-out Hah {c["exact"]}/{c["count"]}. Hah probes: {h["improved"]} improved, {h["worse"]} worse, {h["tied"]} tied. New corruption draws: {new["improved"]}/{new["count"]} improved.</p>'
            summary+='<p>Input → raw model proposal rounded to 2 units → frozen green target. No confidence filter or hidden fallback. Synthetic recovery is not design approval. 224px/48px isolated forms. Font sources and active binaries unchanged.</p>'
        page = page[:start]+summary+page[end:]
        start=page.index('<label>Example mode');end=page.index('</label>',start)+len('</label>')
        modes=list(dict.fromkeys(p['example']['mode'] for p in predictions))
        glyph_names=list(dict.fromkeys(p['example']['glyph'] for p in predictions))
        controls='<label>Example mode <select id="mode">'+''.join(f'<option value="{m}"'+(' selected' if variable and m=='clean-wide' else '')+f'>{html.escape(m)}</option>' for m in modes)+'</select></label> '
        controls+='<label>Glyph <select id="glyph"><option value="all">All supported glyphs</option>'+''.join(f'<option value="{g}"'+(' selected' if g=='hah-ar.init' else '')+f'>{g}</option>' for g in glyph_names)+'</select></label>'
        page=page[:start]+controls+page[end:]
        page=page[:page.index('<script>')]+'''<script>const select=document.querySelector('#mode'),glyph=document.querySelector('#glyph');
function show(){document.querySelectorAll('section').forEach(s=>s.hidden=s.dataset.mode!==select.value||(glyph.value!=='all'&&s.dataset.glyph!==glyph.value))}
function chooseGlyph(){const rows=[...document.querySelectorAll('section')];
for(const option of select.options)option.disabled=!rows.some(s=>s.dataset.mode===option.value&&(glyph.value==='all'||s.dataset.glyph===glyph.value));
if(select.selectedOptions[0].disabled)select.value=[...select.options].find(o=>!o.disabled).value;show()}
select.addEventListener('change',show);glyph.addEventListener('change',chooseGlyph);chooseGlyph();</script>'''
    (out / 'index.html').write_text(page)
    receipt = {'font_sha256': digest, 'checkpoint_sha256': checkpoint_hash,
               'predictions_sha256': hashlib.sha256((run_dir/'predictions.json').read_bytes()).hexdigest(),
               'compiled_outline_and_advance_matches': matches}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dir')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.run_dir, args.out), indent=2))
