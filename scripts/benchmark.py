#!/usr/bin/env python3
"""Score a drafting pipeline on green glyphs that it has not seen.

The cases are in tests/benchmark.toml. Each case is a green glyph in one
master. The drawing in sources/ is the reference.

    benchmark.py prepare out/benchmark/run-1    copy the sources without the
                                                held-out drawings
    benchmark.py score out/benchmark/run-1      compare the redrawn glyphs in
                                                that copy with the references

`prepare` writes a copy of both masters in which each held-out glyph has no
outline, no anchors and a red mark. Give a pipeline that directory only, so
that it cannot read the reference. `score` reports for each case:

    iou        overlap of the filled shapes, 1.0 is identical
    distance   mean distance between the outlines, in font units
    advance    difference of the advance width
    moved      points that differ from the reference, when the point
               structure is the same (otherwise "structure differs")

The numbers measure distance from Eli's drawing. They do not measure quality.
"""
from __future__ import annotations

import argparse
import json
import plistlib
import re
import shutil
import sys
import tomllib
from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'tests/benchmark.toml'
RED = '1,0,0,1'
SCALE = 0.25          # raster pixels per font unit
ORIGIN = (512, 512)   # font units left of and below the glyph origin


class Polygons(BasePen):
    """Flatten an outline to one polygon per contour."""

    def __init__(self):
        super().__init__(None)
        self.contours = []

    def _moveTo(self, pt):
        self.contours.append([pt])

    def _lineTo(self, pt):
        self.contours[-1].append(pt)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.contours[-1][-1]
        for step in range(1, 17):
            t = step / 16
            a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
            self.contours[-1].append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                                      a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))


class Glyph:
    pass


def read(path):
    """Advance, flattened contours and source points of a GLIF. Components are ignored."""
    glyph, pen = Glyph(), Polygons()
    text = path.read_text()
    readGlyphFromString(text, glyph, PointToSegmentPen(pen))
    structure, points = [], []
    for contour in re.findall(r'<contour>(.*?)</contour>', text, re.S):
        tags = re.findall(r'<point [^>]*/>', contour)
        structure.append([(re.search(r'type="(\w+)"', tag) or [None, 'offcurve'])[1]
                          for tag in tags])
        points += [(float(re.search(r' x="([-\d.]+)"', tag)[1]),
                    float(re.search(r' y="([-\d.]+)"', tag)[1])) for tag in tags]
    return dict(advance=getattr(glyph, 'width', 0), contours=pen.contours,
                points=points, structure=structure)


def raster(contours):
    """Fill by the even-odd rule, which matches these sources (no overlaps)."""
    size = int(2048 * SCALE)
    image = Image.new('1', (size, size), 0)
    for contour in contours:
        if len(contour) < 3:
            continue
        layer = Image.new('1', (size, size), 0)
        ImageDraw.Draw(layer).polygon(
            [((x + ORIGIN[0]) * SCALE, size - (y + ORIGIN[1]) * SCALE) for x, y in contour],
            fill=1)
        image = ImageChops.logical_xor(image, layer)
    return np.asarray(image, dtype=bool)


def samples(contours, step=8.0):
    """Points along the outline, about one for each `step` font units."""
    out = []
    for contour in contours:
        ring = contour + contour[:1]
        for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
            count = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / step))
            for i in range(count):
                out.append((x0 + (x1 - x0) * i / count, y0 + (y1 - y0) * i / count))
    return np.array(out)


def compare(reference, candidate):
    advance = candidate['advance'] - reference['advance']
    if not candidate['contours']:
        return dict(iou=0.0, distance=None, advance=advance, moved='no outline')
    a, b = raster(reference['contours']), raster(candidate['contours'])
    union = (a | b).sum()
    p, q = samples(reference['contours']), samples(candidate['contours'])
    gaps = np.sqrt(((p[:, None, :] - q[None, :, :]) ** 2).sum(axis=2))
    distance = (gaps.min(axis=1).mean() + gaps.min(axis=0).mean()) / 2
    if reference['structure'] == candidate['structure']:
        moved = sum(1 for m, n in zip(reference['points'], candidate['points']) if m != n)
        moved = f"{moved} of {len(reference['points'])}"
    else:
        moved = 'structure differs'
    return dict(iou=round(float((a & b).sum() / union), 3) if union else 1.0,
                distance=round(float(distance), 1), advance=advance, moved=moved)


def glif_path(ufo, name):
    contents = plistlib.loads((ufo / 'glyphs/contents.plist').read_bytes())
    return ufo / 'glyphs' / contents[name]


def cases():
    return tomllib.loads(CASES.read_text())['cases']


def prepare(out):
    if out.exists():
        sys.exit(f'{out} exists. Name a new directory.')
    for master in ['Regular', 'Bold']:
        name = f'VirtuaGrotesk-{master}.ufo'
        shutil.copytree(ROOT / 'sources' / name, out / name)
    shutil.copy(ROOT / 'sources/VirtuaGrotesk.designspace', out)
    for case in cases():
        path = glif_path(out / f"VirtuaGrotesk-{case['master']}.ufo", case['glyph'])
        text = path.read_text()
        text = re.sub(r'<outline>.*?</outline>', '<outline>\n\t</outline>', text, flags=re.S)
        text = re.sub(r'\t<anchor [^>]*/>\n', '', text)
        text = re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]*', rf'\g<1>{RED}', text)
        path.write_text(text)
    print(f'{len(cases())} held-out glyphs are empty in {out}')


def score(directory, as_json):
    rows = []
    for case in cases():
        ufo = f"VirtuaGrotesk-{case['master']}.ufo"
        reference = read(glif_path(ROOT / 'sources' / ufo, case['glyph']))
        candidate = read(glif_path(directory / ufo, case['glyph']))
        rows.append({**case, **compare(reference, candidate)})
    drawn = [row for row in rows if row['distance'] is not None]
    summary = dict(cases=len(rows), drawn=len(drawn),
                   mean_iou=round(sum(row['iou'] for row in rows) / len(rows), 3),
                   mean_distance=round(sum(row['distance'] for row in drawn) / len(drawn), 1)
                   if drawn else None)
    if as_json:
        print(json.dumps(dict(summary=summary, cases=rows), indent=1))
        return
    print(f"{'glyph':<16}{'master':<9}{'iou':>6}{'distance':>10}{'advance':>9}  moved")
    for row in rows:
        distance = '-' if row['distance'] is None else row['distance']
        print(f"{row['glyph']:<16}{row['master']:<9}{row['iou']:>6}{distance:>10}"
              f"{row['advance']:>9g}  {row['moved']}")
    print(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('command', choices=['prepare', 'score'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.directory)
    else:
        score(args.directory, args.json)


if __name__ == '__main__':
    main()
