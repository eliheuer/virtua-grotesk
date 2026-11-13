#!/usr/bin/env python3
"""Evaluate a drafting method on green glyphs that it has not seen.

A drafting method is anything that draws glyphs: an agent, a model or a
script. The held-out glyphs and the tasks are in sources/held-out-glyphs.toml.

    evaluate_drafting.py prepare <task> <run>   copy the sources into
                                                <run>/sources and set the task
    evaluate_drafting.py score <run>            score the drafts in that copy
    evaluate_drafting.py compare <run> <run>    compare the scores of two runs

The tasks are redraw, bold, repair and relatives. Give the method only
<run>/sources, so that it cannot read the references. It edits the glyphs in
place. `score` reports for each glyph and master:

    iou         overlap of the filled shapes with Eli's drawing, 1.0 is equal
    distance    mean distance between the outlines, in font units
    advance     difference of the advance width
    moved       points that differ from Eli's drawing, when the point
                structure is the same
    compatible  the point structure matches the other master
    off 8       points off the 8-unit grid (new drafts use 8)
    curves      flags from curve_lint.py
    design      findings from check_design.py; needs Runebender

The last three columns show the draft, then Eli's drawing: "4/3". Eli's
drawings have intended off-grid points and findings, so compare the two.

The scores are written to <run>/scores.json. They measure the distance from
Eli's drawing and the project checks. They do not approve a glyph.
"""
from __future__ import annotations

import argparse
import functools
import json
import plistlib
import random
import re
import shutil
import sys
import tomllib
import zlib
from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
from PIL import Image, ImageChops, ImageDraw

import check_design
import source_inventory
from curve_lint import lint_glyph

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'sources/held-out-glyphs.toml'
CONTRACT = ROOT / 'sources/design.toml'
MASTERS = ['Regular', 'Bold']
TASKS = ['redraw', 'bold', 'repair', 'relatives']
RED = '1,0,0,1'
SCALE = 0.25          # raster pixels per font unit
ORIGIN = (512, 512)   # font units left of and below the glyph origin
OFFSETS = (-32, -24, -16, 16, 24, 32)


class Polygons(BasePen):
    """Flatten an outline to one polygon per contour."""

    def __init__(self):
        super().__init__(None)
        self.contours = []

    def addComponent(self, name, transform):
        pass

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
    return parse(path.read_text())


def parse(text):
    """Advance, flattened contours and source points of a GLIF. Components are ignored."""
    glyph, pen = Glyph(), Polygons()
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
    """Distance of a candidate outline from the reference outline."""
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


def glif_path(sources, master, name):
    ufo = sources / f'VirtuaGrotesk-{master}.ufo'
    contents = plistlib.loads((ufo / 'glyphs/contents.plist').read_bytes())
    return ufo / 'glyphs' / contents[name]


@functools.cache
def green_masters():
    """For each glyph, the masters in which it is green."""
    contract = tomllib.loads(CONTRACT.read_text())
    found = {}
    for master in MASTERS:
        for name, record in source_inventory.load_master(ROOT, master, contract).items():
            if record['color']['name'] == 'green':
                found.setdefault(name, []).append(master)
    return found


def cases(task):
    """The cases of a task: glyph, the masters it is hidden or changed in,
    the masters it is scored in, and the glyphs it is drawn from."""
    table = tomllib.loads(CASES.read_text())[task]
    green = green_masters()
    rows = table['cases'] if task == 'relatives' else [{'glyph': g} for g in table['glyphs']]
    out = []
    for row in rows:
        glyph = row['glyph']
        scored = green.get(glyph, [])
        if task == 'bold':
            scored = [m for m in scored if m == 'Bold']
        changed = scored if task in ('bold', 'repair') else MASTERS
        out.append(dict(glyph=glyph, changed=changed, scored=scored,
                        donors=row.get('from', [])))
    return out


def hide(path):
    """Remove the outline, anchors and advance of a glyph and mark it red."""
    text = path.read_text()
    text = re.sub(r'<advance width="[-\d.]+"', '<advance width="0"', text)
    text = re.sub(r'<outline>.*?</outline>', '<outline>\n\t</outline>', text, flags=re.S)
    text = re.sub(r'\t<anchor [^>]*/>\n', '', text)
    text = re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]*', rf'\g<1>{RED}', text)
    path.write_text(text)


def displace(path, seed):
    """Move about one fifth of the on-curve points of each contour, with their
    handles, by 16 to 32 units on one axis. The same seed moves the same points."""
    rng = random.Random(seed)
    text = path.read_text()

    def move(match):
        tags = re.findall(r'<point [^>]*/>', match.group(0))
        points = [dict(tag=tag, on='type=' in tag) for tag in tags]
        ons = [i for i, p in enumerate(points) if p['on']]
        shifts = {}
        for i in rng.sample(ons, max(1, len(ons) // 5)):
            axis, offset = rng.choice('xy'), rng.choice(OFFSETS)
            for j in ((i - 1) % len(points), i, (i + 1) % len(points)):
                if j == i or not points[j]['on']:
                    shifts[j] = (axis, offset)
        index = iter(range(len(points)))

        def shift(tag_match):
            tag = tag_match.group(0)
            j = next(index)
            if j not in shifts:
                return tag
            axis, offset = shifts[j]
            value = float(re.search(rf' {axis}="([-\d.]+)"', tag)[1]) + offset
            return re.sub(rf' {axis}="[-\d.]+"', f' {axis}="{value:g}"', tag)

        return re.sub(r'<point [^>]*/>', shift, match.group(0))

    text = re.sub(r'<contour>.*?</contour>', move, text, flags=re.S)
    text = re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]*', rf'\g<1>{RED}', text)
    path.write_text(text)


def prepare(task, run):
    if run.exists():
        sys.exit(f'{run} exists. Name a new directory.')
    sources = run / 'sources'
    for master in MASTERS:
        name = f'VirtuaGrotesk-{master}.ufo'
        shutil.copytree(ROOT / 'sources' / name, sources / name)
    shutil.copy(ROOT / 'sources/VirtuaGrotesk.designspace', sources)
    rows = cases(task)
    for row in rows:
        for master in row['changed']:
            path = glif_path(sources, master, row['glyph'])
            if task == 'repair':
                displace(path, zlib.crc32(f"{row['glyph']}/{master}".encode()))
            else:
                hide(path)
    (run / 'evaluation.json').write_text(json.dumps(dict(task=task, cases=rows), indent=1) + '\n')
    print(f'{task}: {len(rows)} glyphs prepared in {sources}')


def checks(root, data, master, glyph, contract, design):
    """Grid, curve and design counts of one glyph; None where it has no outline."""
    record = data[master][glyph]
    if not record['contours']:
        return dict(off_8=None, curves=None, design=None)
    found = None
    if design:
        findings = check_design.check_contour(glyph, data, contract.get('targets', {}),
                                              root=root, masters=[master])
        found = len([f for f in findings if not f.startswith('masters:')])
    return dict(off_8=record['off_8_points'],
                curves=len(lint_glyph(glif_path(root / 'sources', master, glyph), glyph)),
                design=found)


def score(run):
    setup = json.loads((run / 'evaluation.json').read_text())
    contract = tomllib.loads(CONTRACT.read_text())
    data = {m: source_inventory.load_master(run, m, contract) for m in MASTERS}
    reference = {m: source_inventory.load_master(ROOT, m, contract) for m in MASTERS}
    design = check_design.find_runebender() is not None
    rows = []
    for case in setup['cases']:
        for master in case['scored']:
            glyph = case['glyph']
            row = dict(glyph=glyph, master=master,
                       **compare(read(glif_path(ROOT / 'sources', master, glyph)),
                                 read(glif_path(run / 'sources', master, glyph))))
            other = data['Bold' if master == 'Regular' else 'Regular'].get(glyph)
            row['compatible'] = (bool(data[master][glyph]['contours']) and bool(other)
                                 and data[master][glyph]['point_types'] == other['point_types'])
            row['draft'] = checks(run, data, master, glyph, contract, design)
            row['reference'] = checks(ROOT, reference, master, glyph, contract, design)
            rows.append(row)
    drawn = [r for r in rows if r['distance'] is not None]
    summary = dict(task=setup['task'], scored=len(rows), drawn=len(drawn),
                   mean_iou=round(sum(r['iou'] for r in rows) / len(rows), 3) if rows else None,
                   mean_distance=round(sum(r['distance'] for r in drawn) / len(drawn), 1)
                   if drawn else None,
                   compatible=sum(r['compatible'] for r in rows))
    (run / 'scores.json').write_text(json.dumps(dict(summary=summary, rows=rows), indent=1) + '\n')
    dash = lambda v: '-' if v is None else v
    pair = lambda r, key: f"{dash(r['draft'][key])}/{dash(r['reference'][key])}"
    print(f"{'glyph':<20}{'master':<9}{'iou':>6}{'distance':>10}{'advance':>9}"
          f"{'compatible':>12}{'off 8':>8}{'curves':>8}{'design':>8}  moved")
    for r in rows:
        print(f"{r['glyph']:<20}{r['master']:<9}{r['iou']:>6}{dash(r['distance']):>10}"
              f"{r['advance']:>9g}{'yes' if r['compatible'] else 'no':>12}"
              f"{pair(r, 'off_8'):>8}{pair(r, 'curves'):>8}{pair(r, 'design'):>8}  {r['moved']}")
    print(summary)
    if not design:
        print('Runebender was not found, so the design column is empty.')


def compare_runs(first, second):
    a, b = (json.loads((run / 'scores.json').read_text()) for run in (first, second))
    if a['summary']['task'] != b['summary']['task']:
        sys.exit('The two runs are different tasks.')
    later = {(r['glyph'], r['master']): r for r in b['rows']}
    print(f"{'glyph':<20}{'master':<9}{'iou':>14}{'distance':>16}")
    for r in a['rows']:
        s = later.get((r['glyph'], r['master']))
        if s:
            print(f"{r['glyph']:<20}{r['master']:<9}{r['iou']:>6} -> {s['iou']:<5}"
                  f"{str(r['distance']):>8} -> {s['distance']}")
    for key in ('mean_iou', 'mean_distance', 'compatible'):
        print(f"{key}: {a['summary'][key]} -> {b['summary'][key]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('task', choices=TASKS)
    p.add_argument('run', type=Path)
    sub.add_parser('score').add_argument('run', type=Path)
    c = sub.add_parser('compare')
    c.add_argument('first', type=Path)
    c.add_argument('second', type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.task, args.run)
    elif args.command == 'score':
        score(args.run)
    else:
        compare_runs(args.first, args.second)


if __name__ == '__main__':
    main()
