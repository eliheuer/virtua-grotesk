#!/usr/bin/env python3
"""Read-only 8-grid gate for explicitly selected machine-draft UFO glyphs.

Checks source points (including handles), anchors, advances, component offsets
and actual curve bounds/sidebearings. Popcounts describe measurements; they
never fail this gate and never assign a human review color. Not a curve-quality,
master-compatibility, shaping or release-readiness check.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib import UFOReader
from fontTools.ufoLib.glifLib import readGlyphFromString


def on_grid(value):
    return math.isfinite(value) and math.isclose(value / 8, round(value / 8), abs_tol=1e-9, rel_tol=0)


def inspect_glif(xml, glyph_set=None):
    root = ET.fromstring(xml)
    failures, measurements = [], []

    def check(label, value):
        value = float(value)
        if not on_grid(value):
            failures.append({'field': label, 'value': value})
        return value

    def measure(label, value):
        value = abs(float(value))
        measurements.append({'name': label, 'value': value,
                             'popcount': int(value).bit_count() if value.is_integer() else None})

    advance = root.find('advance')
    width = check('advance.width', advance.get('width', '0') if advance is not None else 0)
    measure('advance', width)
    if advance is not None and advance.get('height') is not None:
        check('advance.height', advance.get('height'))
    contours = root.findall('./outline/contour')
    for ci, contour in enumerate(contours):
        points = list(contour)
        for pi, p in enumerate(points):
            for axis in ('x', 'y'):
                check(f'contour[{ci}].point[{pi}].{axis}', p.get(axis))
            if p.get('type') is None:
                for neighbor in (points[(pi-1) % len(points)], points[(pi+1) % len(points)]):
                    if neighbor.get('type'):
                        for axis in ('x', 'y'):
                            delta = float(p.get(axis))-float(neighbor.get(axis))
                            if delta:
                                measure(f'handle.{axis}', delta)
                        break
        for axis in ('x', 'y'):
            positions = sorted(set(float(p.get(axis)) for p in points if p.get('type')))
            for a, b in zip(positions, positions[1:]):
                measure(f'adjacent_oncurve_span.{axis}', b-a)
    for i, anchor in enumerate(root.findall('anchor')):
        for axis in ('x', 'y'):
            check(f'anchor[{anchor.get("name", str(i))}].{axis}', anchor.get(axis))
    for i, component in enumerate(root.findall('./outline/component')):
        for axis in ('xOffset', 'yOffset'):
            check(f'component[{i}].{axis}', component.get(axis, '0'))
        # Scaling/rotation can move a compliant donor off grid. Require a
        # decomposed audit rather than silently certify such a component.
        for field, default in [('xScale', 1), ('yScale', 1), ('xyScale', 0), ('yxScale', 0)]:
            if float(component.get(field, default)) != default:
                failures.append({'field': f'component[{i}].{field}', 'value': float(component.get(field)),
                                 'reason': 'Transformed component requires decomposed review'})
        if glyph_set is not None:
            donor = inspect_glif(glyph_set.getGLIF(component.get('base')), glyph_set)
            failures.extend({'field': f'component[{i}].{f["field"]}', **{k:v for k,v in f.items() if k != 'field'}} for f in donor['failures'])
    pen = BoundsPen(glyph_set or {})
    readGlyphFromString(xml, SimpleNamespace(), PointToSegmentPen(pen))
    bounds = pen.bounds
    if bounds:
        for label, value in [('left_sidebearing', bounds[0]), ('right_sidebearing', width-bounds[2])]:
            measure(label, check(label, value))
    return {'glyph': root.get('name'), 'points': sum(len(c) for c in contours),
            'advance': width, 'bounds': bounds, 'failures': failures,
            'measurements': measurements,
            'popcount_histogram': dict(Counter(str(m['popcount']) for m in measurements)),
            'passed': not failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ufo', type=Path, action='append', required=True)
    parser.add_argument('--glyphs', nargs='+', required=True)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    records = []
    for ufo in args.ufo:
        with UFOReader(ufo) as reader:
            glyphs = reader.getGlyphSet()
            for name in args.glyphs:
                xml = glyphs.getGLIF(name)
                result = inspect_glif(xml, glyphs)
                result.update(ufo=str(ufo.resolve()), sha256=hashlib.sha256(xml).hexdigest())
                records.append(result)
    report = {'policy': 'Machine drafts on 8; popcount descriptive; no grading or mutation',
              'glyph_masters': len(records), 'passed': all(r['passed'] for r in records), 'results': records}
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2)+'\n')
    print(f'{len(records)} glyph-masters; {sum(len(r["failures"]) for r in records)} off-grid/transform findings')
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
