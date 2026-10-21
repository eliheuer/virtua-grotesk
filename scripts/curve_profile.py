#!/usr/bin/env python3
"""Read-only signed curvature report and common-scale SVG comb for GLIF snapshots.

Supports closed explicit cubic/line contours. Components, quadratics and open
paths fail explicitly: resolve them on scratch first. Sampling is diagnostic,
not a proof that no cusp, inflection or intersection exists between samples.
No source rewriting, harmonization, grading or geometry optimization occurs.

  .venv/bin/python scripts/curve_profile.py before.glif after.glif \
      --json curve-profile.json --svg curve-comb.svg
"""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from curve_lint import all_segments, bez, join_audit


def read_contours(path):
    root = ET.parse(path).getroot()
    if root.find('.//component') is not None:
        raise ValueError(f'{path}: components require a decomposed scratch snapshot')
    contours = []
    for contour in root.findall('./outline/contour'):
        points = []
        for point in contour.findall('point'):
            typ = point.get('type')
            if typ not in (None, 'line', 'curve'):
                raise ValueError(f'{path}: unsupported point type {typ!r}')
            x, y = float(point.attrib['x']), float(point.attrib['y'])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError(f'{path}: nonfinite coordinate')
            points.append(dict(x=x, y=y, on=typ is not None,
                               smooth=point.get('smooth') == 'yes', type=typ))
        ons = [i for i, point in enumerate(points) if point['on']]
        if len(ons) < 2:
            raise ValueError(f'{path}: contour has fewer than two explicit on-curves')
        for j, start in enumerate(ons):
            end = ons[(j + 1) % len(ons)]
            off_count = (end - start - 1) % len(points)
            expected = 2 if points[end]['type'] == 'curve' else 0
            if off_count != expected:
                raise ValueError(f'{path}: invalid explicit cubic/line segment at point {end}')
        contours.append(points)
    if not contours:
        raise ValueError(f'{path}: no contours to inspect')
    return contours


def sample(segment, t):
    p0, p1, p2, p3 = segment[:4]
    u = 1 - t
    d = tuple(3*u*u*(p1[i]-p0[i]) + 6*u*t*(p2[i]-p1[i])
              + 3*t*t*(p3[i]-p2[i]) for i in range(2))
    dd = tuple(6*u*(p2[i]-2*p1[i]+p0[i])
               + 6*t*(p3[i]-2*p2[i]+p1[i]) for i in range(2))
    speed = math.hypot(*d)
    k = (d[0]*dd[1]-d[1]*dd[0])/speed**3 if speed > 1e-9 else None
    # Match native RuneBender's right-normal comb convention.
    normal = [d[1]/speed, -d[0]/speed] if speed > 1e-9 else None
    return dict(t=t, point=bez(p0,p1,p2,p3,t), curvature=k, normal=normal)


def profile(path, samples=96):
    if samples < 8:
        raise ValueError('use at least eight samples per segment')
    contours = read_contours(path)
    curves, warnings = [], []
    for ci, contour in enumerate(contours):
        for si, segment in enumerate(all_segments(contour)):
            if segment[4]:
                continue
            values = [sample(segment, i/samples) for i in range(samples + 1)]
            ks = [v['curvature'] for v in values if v['curvature'] is not None]
            signs = [1 if k > 0 else -1 for k in ks if abs(k) > 1e-10]
            flips = sum(a != b for a,b in zip(signs, signs[1:]))
            if len(ks) != len(values):
                warnings.append(f'c{ci} segment {si}: zero-speed sample; curvature undefined')
            if flips:
                warnings.append(f'c{ci} segment {si}: {flips} sampled curvature sign change(s); inspect intent')
            curves.append(dict(contour=ci, segment=si, controls=segment[:4],
                               samples=values, sampled_sign_changes=flips,
                               max_abs_curvature=max(map(abs,ks), default=None)))
    joins = join_audit(contours)
    # The old join classifier substitutes chord tangents for zero handles.
    # Expose undefined endpoints explicitly rather than certifying them smooth.
    for row in joins:
        segments = all_segments(contours[row['contour']])
        for i, outgoing in enumerate(segments):
            if outgoing[0] != row['point']:
                continue
            incoming = segments[i-1]
            if sample(incoming,1)['curvature'] is None or sample(outgoing,0)['curvature'] is None:
                row.update(classification='undefined', curvature_in=None,
                           curvature_out=None, relative_jump=None)
                break
    return dict(path=str(Path(path).resolve()), sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                samples_per_segment=samples, contours=contours, curves=curves,
                joins=joins, warnings=warnings)


def svg(reports, gain=600):
    """One world scale AND curvature gain for every panel; no clipping ribs."""
    if not math.isfinite(gain) or gain <= 0:
        raise ValueError('comb gain must be positive and finite')
    extents = []
    for report in reports:
        extents += [(p['x'],p['y']) for c in report['contours'] for p in c]
        for curve in report['curves']:
            for v in curve['samples']:
                if v['curvature'] is not None:
                    extents.append(tuple(v['point'][i]+v['normal'][i]*v['curvature']*gain for i in range(2)))
    left, right = min(p[0] for p in extents), max(p[0] for p in extents)
    bottom, top = min(p[1] for p in extents), max(p[1] for p in extents)
    scale = min(440/max(right-left,1), 530/max(top-bottom,1))
    height = math.ceil((top-bottom)*scale) + 160
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{520*len(reports)}" height="{height}" viewBox="0 0 {520*len(reports)} {height}">',
           '<rect width="100%" height="100%" fill="#eee"/>',
           '<style>text{font:16px sans-serif;fill:#222}path,line,circle{vector-effect:non-scaling-stroke}</style>']
    for index, report in enumerate(reports):
        offset = index*520
        title = html.escape(Path(report['path']).stem)
        out += [f'<text x="{offset+24}" y="30">{title} · {report["sha256"][:10]}</text>',
                f'<text x="{offset+24}" y="55">Same outline scale · comb gain {gain:g}</text>',
                f'<g transform="translate({offset+40-left*scale},{90+top*scale}) scale({scale}, {-scale})">']
        commands=[]
        for contour in report['contours']:
            segments = all_segments(contour)
            commands.append(f'M {segments[0][0][0]} {segments[0][0][1]}')
            for s in segments:
                commands.append(f'L {s[3][0]} {s[3][1]}' if s[4] else 'C '+' '.join(f'{x} {y}' for x,y in s[1:4]))
            commands.append('Z')
        out.append(f'<path d="{" ".join(commands)}" fill="#bbb" stroke="#222" stroke-width="1.4"/>')
        for curve in report['curves']:
            for v in curve['samples']:
                if v['curvature'] is None:
                    continue
                x,y=v['point']; nx,ny=v['normal']; k=v['curvature']
                out.append(f'<line x1="{x}" y1="{y}" x2="{x+nx*k*gain}" y2="{y+ny*k*gain}" stroke="#555" stroke-width="0.6"/>')
        for row in report['joins']:
            x,y=row['point']
            out.append(f'<circle cx="{x}" cy="{y}" r="{3/scale}" fill="#eee" stroke="#222" stroke-width="1"/>')
        out += ['</g>', f'<text x="{offset+24}" y="{height-24}">Signed sampled curvature; diagnostic, not a grade.</text>']
    return '\n'.join(out+['</svg>'])


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('glifs', nargs='+', type=Path)
    ap.add_argument('--samples', type=int, default=96)
    ap.add_argument('--gain', type=float, default=600, help='shared comb displacement per inverse font unit')
    ap.add_argument('--json', type=Path)
    ap.add_argument('--svg', type=Path)
    args=ap.parse_args()
    inputs={p.resolve() for p in args.glifs}
    outputs=[p.resolve() for p in (args.json,args.svg) if p]
    if inputs.intersection(outputs) or len(outputs)!=len(set(outputs)):
        ap.error('outputs must be distinct and must not overwrite input GLIFs')
    try:
        reports=[profile(path,args.samples) for path in args.glifs]
        drawing=svg(reports,args.gain) if args.svg else None
    except (ValueError, OSError, ET.ParseError) as exc:
        ap.error(str(exc))
    result=dict(method='signed cubic curvature, shared SVG scale; sampled interior, analytic endpoints', reports=reports)
    if args.json:
        args.json.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    if args.svg:
        args.svg.write_text(drawing+'\n')
    for report in reports:
        print(f'{report["path"]}: {len(report["curves"])} curves; {len(report["warnings"])} sampling warnings')
        for row in report['joins']:
            print(f'  c{row["contour"]} {row["point"]}: {row["classification"]}; κ {row["curvature_in"]} -> {row["curvature_out"]}')
        for warning in report['warnings']:
            print('  '+warning)


if __name__ == '__main__':
    main()
