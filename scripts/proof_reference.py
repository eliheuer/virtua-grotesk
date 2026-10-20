#!/usr/bin/env python3
"""Render shaped samples beside reference fonts at a fixed em scale."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import freetype
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw

from proof_compare import PALETTE, mask_for, shaped_run
from specimen_layout import render_pages


def reference_sheet(fonts, samples, weights, size, output, title="Reference study", subtitle="Common origin / fixed em scale", grid=False, folio=None):
    rows, records, metadata = [], [], []
    for label, path in fonts:
        with TTFont(path) as font:
            axes = {axis.axisTag: [axis.minValue, axis.defaultValue, axis.maxValue]
                    for axis in font['fvar'].axes} if 'fvar' in font else {}
            for weight in weights:
                if 'wght' in axes:
                    if not axes['wght'][0] <= weight <= axes['wght'][2]:
                        raise ValueError(f'{label}: weight {weight} is outside its axis range')
                elif weight != font['OS/2'].usWeightClass:
                    raise ValueError(f'{label}: static font does not have weight {weight}')
            metadata.append({'label': label, 'path': str(path.resolve()),
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                             'family': font['name'].getDebugName(1), 'axes': axes,
                             'upm': font['head'].unitsPerEm})
    for sample in samples:
        for weight in weights:
            px = sample.get('size', size)
            runs = [shaped_run(path, sample['text'], weight, px) for _, path in fonts]
            bounds = [min(r[1][0] for r in runs), min(r[1][1] for r in runs),
                      max(r[1][2] for r in runs), max(r[1][3] for r in runs)]
            panels = []
            for (label, _), (tiles, _, shaping) in zip(fonts, runs):
                mask = mask_for(tiles, bounds)
                panel = Image.new('RGB', mask.size, PALETTE['background'])
                panel.paste(PALETTE['ink'], mask=mask)
                draw = ImageDraw.Draw(panel)
                y = 16 - bounds[1]
                draw.line((0, y, 10, y), fill=PALETTE['baseline'])
                draw.line((panel.width - 10, y, panel.width, y), fill=PALETTE['baseline'])
                panels.append(panel)
                records.append({'sample': sample['label'], 'text': sample['text'],
                                'font': label, 'weight': weight, 'size_px_per_em': px,
                                'shared_pixel_bounds': bounds, 'shaping': shaping,
                                'missing_glyph': any(p['gid'] == 0 for p in shaping)})
            row_label={400:'Regular',550:'Midpoint',700:'Bold'}.get(weight,sample['label']) if len(samples)==1 else sample['label']
            rows.append({'label':f"{weight:g}  /  {row_label}", 'note':f'{px:g} px/em', 'images':panels, 'baseline':16-bounds[1]})
    layout=render_pages(rows,[label for label,_ in fonts],output,title,subtitle,grid=grid,folio=folio)
    manifest = {'layout':layout, 'fonts': metadata, 'palette': PALETTE, 'samples': samples, 'rows': records,
                'tools': {p: importlib.metadata.version(p) for p in ['uharfbuzz', 'freetype-py', 'Pillow', 'fonttools']},
                'harfbuzz': hb.version_string(), 'freetype': freetype.version(),
                'note': 'Single-script shaped runs. Fixed em scale, no auto-fit or optical weight matching. References are not design approval.'}
    output.with_suffix('.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    if any(r['missing_glyph'] for r in records):
        raise ValueError('Missing glyphs in reference proof; inspect JSON before using the sheet')
    print(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', action='append', required=True, help='LABEL=PATH; repeat for each column')
    parser.add_argument('--samples', type=Path, required=True, help='JSON list of label/text with optional size')
    parser.add_argument('--weights', type=float, nargs='+', default=[400, 700])
    parser.add_argument('--size', type=float, default=80)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--title', default='Reference study')
    parser.add_argument('--subtitle', default='Common origin / fixed em scale')
    parser.add_argument('--grid', action='store_true')
    args = parser.parse_args()
    fonts = []
    for item in args.font:
        label, separator, path = item.partition('=')
        if not separator or not label or not path:
            parser.error('--font requires LABEL=PATH')
        fonts.append((label, Path(path)))
    samples = json.loads(args.samples.read_text())
    if not samples or args.size <= 0 or any(s.get('size', args.size) <= 0 for s in samples):
        parser.error('Samples must be nonempty and sizes positive')
    if args.output.suffix.lower() != '.png':
        parser.error('Output must be a PNG')
    inputs = {p.resolve() for _, p in fonts} | {args.samples.resolve()}
    if {args.output.resolve(), args.output.with_suffix('.json').resolve()} & inputs:
        parser.error('Output must not overwrite an input')
    reference_sheet(fonts, samples, args.weights, args.size, args.output, args.title, args.subtitle, args.grid)


if __name__ == '__main__':
    main()
