#!/usr/bin/env python3
"""Read-only, fixed-scale shaped comparison of two compiled fonts. See qa.md."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import freetype
import uharfbuzz as hb
from PIL import Image, ImageChops, ImageDraw
from specimen_layout import render_pages


PALETTE = {
    'background': '#dedede',
    'ink': '#444444',
    'baseline': '#999999',
    'removed': '#d02070',
    'added': '#008ba3',
}


def shaped_run(path, text, weight, size):
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    font.set_variations({'wght': weight})
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    face = freetype.Face(str(path))
    face.set_char_size(round(size * 64))
    if face.has_multiple_masters:
        face.set_var_design_coords([
            weight if axis.tag == 'wght' else axis.default
            for axis in face.get_variation_info().axes
        ])
    scale = size / face.units_per_EM
    x = y = 0
    tiles, records = [], []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        face.load_glyph(info.codepoint, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
        slot = face.glyph
        bitmap = slot.bitmap
        left = round((x + pos.x_offset) * scale) + slot.bitmap_left
        top = round(-(y + pos.y_offset) * scale) - slot.bitmap_top
        if bitmap.width and bitmap.rows:
            if bitmap.pixel_mode != freetype.FT_PIXEL_MODE_GRAY or bitmap.pitch < 0:
                raise ValueError('Only positive-pitch grayscale outlines are supported')
            pixels = bytes(bitmap.buffer)
            mask = Image.frombytes('L', (bitmap.width, bitmap.rows), pixels,
                                   'raw', 'L', bitmap.pitch)
            tiles.append((left, top, mask))
        records.append({'gid': info.codepoint, 'cluster': info.cluster,
                        'advance': [pos.x_advance, pos.y_advance],
                        'offset': [pos.x_offset, pos.y_offset]})
        x += pos.x_advance
        y += pos.y_advance
    bounds = [min([0] + [t[0] for t in tiles]),
              min([0] + [t[1] for t in tiles]),
              max([round(x * scale)] + [t[0] + t[2].width for t in tiles]),
              max([0] + [t[1] + t[2].height for t in tiles])]
    return tiles, bounds, records


def mask_for(tiles, bounds):
    x0, y0, x1, y1 = bounds
    mask = Image.new('L', (x1 - x0 + 32, y1 - y0 + 32))
    for x, y, tile in tiles:
        layer = Image.new('L', mask.size)
        layer.paste(tile, (x - x0 + 16, y - y0 + 16))
        mask = ImageChops.lighter(mask, layer)
    return mask


def compare(before, after, samples, weights, size, output, title="Revision study", subtitle="Before / after / difference", grid=False):
    rows, measurements = [], []
    for sample in samples:
        for weight in weights:
            a, ab, ar = shaped_run(before, sample['text'], weight, size)
            b, bb, br = shaped_run(after, sample['text'], weight, size)
            bounds = [min(ab[0], bb[0]), min(ab[1], bb[1]),
                      max(ab[2], bb[2]), max(ab[3], bb[3])]
            old, new = mask_for(a, bounds), mask_for(b, bounds)
            common = ImageChops.darker(old, new)
            removed = ImageChops.subtract(old, new)
            added = ImageChops.subtract(new, old)
            images = []
            for mask in (old, new):
                im = Image.new('RGB', mask.size, PALETTE['background'])
                im.paste(PALETTE['ink'], mask=mask)
                images.append(im)
            diff = Image.new('RGB', old.size, PALETTE['background'])
            for color, mask in [(PALETTE['ink'], common), (PALETTE['removed'], removed), (PALETTE['added'], added)]:
                diff.paste(color, mask=mask)
            images.append(diff)
            for im in images:
                # Same source origin and baseline in all three panels.
                draw = ImageDraw.Draw(im)
                baseline = 16 - bounds[1]
                draw.line((0, baseline, 10, baseline), fill=PALETTE['baseline'])
                draw.line((im.width - 10, baseline, im.width, baseline), fill=PALETTE['baseline'])
            rows.append({'label':f"{weight:g}  /  {sample['label']}", 'note':f'{size:g} px/em', 'images':images, 'baseline':16-bounds[1]})
            measurements.append({'label': sample['label'], 'text': sample['text'],
                                 'weight': weight, 'shared_pixel_bounds': bounds,
                                 'changed_pixels': old.width * old.height - ImageChops.difference(old, new).histogram()[0],
                                 'missing_glyph': any(r['gid'] == 0 for r in ar + br),
                                 'before_shaping': ar, 'after_shaping': br})
    layout=render_pages(rows,['Before','After','Difference'],output,title,subtitle,footnote='Magenta: removed ink. Cyan: added ink. Fixed scale; no optical fitting.',grid=grid)
    manifest = {'layout':layout, 'before': str(before.resolve()), 'after': str(after.resolve()),
                'sha256': {name: hashlib.sha256(path.read_bytes()).hexdigest()
                           for name, path in [('before', before), ('after', after)]},
                'size_px_per_em': size, 'weights': weights, 'palette': PALETTE,
                'tools': {p: importlib.metadata.version(p)
                          for p in ['uharfbuzz', 'freetype-py', 'Pillow']},
                'harfbuzz': hb.version_string(), 'freetype': freetype.version(),
                'rows': measurements,
                'note': 'Fixed scale and shared origin; raster differences are evidence, not an aesthetic score.'}
    output.with_suffix('.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(output)
    if any(row['missing_glyph'] for row in measurements):
        print('WARNING: a shaped run contains glyph 0; inspect the JSON and proof.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--samples', type=Path, required=True,
                        help='JSON list of {label, text} objects')
    parser.add_argument('--weights', type=float, nargs='+', default=[400, 550, 700])
    parser.add_argument('--size', type=float, default=96, help='Pixels per em; never auto-fitted')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--title', default='Revision study')
    parser.add_argument('--subtitle', default='Before / after / difference')
    parser.add_argument('--grid', action='store_true')
    args = parser.parse_args()
    samples = json.loads(args.samples.read_text())
    if not samples or args.size <= 0:
        parser.error('Use nonempty samples and a positive size')
    if args.output.suffix.lower() != '.png':
        parser.error('Output must be a PNG path')
    inputs = {args.before.resolve(), args.after.resolve(), args.samples.resolve()}
    if {args.output.resolve(), args.output.with_suffix('.json').resolve()} & inputs:
        parser.error('Output must not overwrite an input')
    compare(args.before, args.after, samples, args.weights, args.size, args.output, args.title, args.subtitle, args.grid)


if __name__ == '__main__':
    main()
