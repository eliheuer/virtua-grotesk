"""Snap glyphs onto the 8-unit grid (the Virtua design system).

For the freshly-swapped Bezy Arabic (or any glyphs): snap on-curve
points to the nearest 8-grid, carrying their handles so curve shapes
translate rather than distort; then tidy handles (2-grid + straighten
near-axis handles to true H/V); then snap the advance width to 8.

    ./.venv/bin/python scripts/grid_snap.py --arabic --dry     # report only
    ./.venv/bin/python scripts/grid_snap.py --arabic           # apply
    ./.venv/bin/python scripts/grid_snap.py beh-ar seen-ar     # specific glyphs

Reversible: nothing is committed. Review in the editor, then commit or
`git checkout -- sources/`.
"""

import argparse
import os
import plistlib
import re

HANDLE_HV_TOL = 6  # straighten handles within this of axis-aligned


def snap8(v):
    return round(v / 8) * 8


def snap2(v):
    return round(v / 2) * 2


POINT_RE = re.compile(
    r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
    r'((?: type="(\w+)")?(?: smooth="yes")?[^/]*)/>')


def snap_contour(pts):
    """pts: list of dicts {x,y,on}. Returns new coords in place."""
    n = len(pts)
    on_idx = [i for i, p in enumerate(pts) if p['on']]
    # 1) snap on-curves to nearest 8, carry adjacent handles by the delta
    for i in on_idx:
        dx = snap8(pts[i]['x']) - pts[i]['x']
        dy = snap8(pts[i]['y']) - pts[i]['y']
        pts[i]['x'] += dx
        pts[i]['y'] += dy
        for j in (i - 1, i + 1):  # incoming + outgoing handle
            q = pts[j % n]
            if not q['on']:
                q['x'] += dx
                q['y'] += dy
    # 2) tidy handles: 2-grid, then straighten near-axis to its anchor
    for j, p in enumerate(pts):
        if p['on']:
            continue
        # anchor = the on-curve this handle is the tangent at
        nxt, prv = pts[(j + 1) % n], pts[(j - 1) % n]
        anchor = nxt if nxt['on'] else (prv if prv['on'] else None)
        p['x'], p['y'] = snap2(p['x']), snap2(p['y'])
        if anchor:
            if abs(p['x'] - anchor['x']) <= HANDLE_HV_TOL:
                p['x'] = anchor['x']
            elif abs(p['y'] - anchor['y']) <= HANDLE_HV_TOL:
                p['y'] = anchor['y']
    return pts


def process_glif(src):
    changed = False
    out = src

    def do_contour(cm):
        nonlocal changed
        body = cm.group(1)
        matches = list(POINT_RE.finditer(body))
        pts = [{'x': float(m.group(1)), 'y': float(m.group(2)),
                'on': bool(m.group(4))} for m in matches]  # g4 = type word
        if not pts:
            return cm.group(0)
        snap_contour(pts)
        # rewrite each point's x/y in order
        new_body, last = [], 0
        for m, p in zip(matches, pts):
            new_body.append(body[last:m.start()])
            x = f'{p["x"]:g}'
            y = f'{p["y"]:g}'
            new_body.append(f'<point x="{x}" y="{y}"{m.group(3)}/>')  # g3=attrs
            last = m.end()
        new_body.append(body[last:])
        changed = True
        return '<contour>' + ''.join(new_body) + '</contour>'

    out = re.sub(r'<contour>(.*?)</contour>', do_contour, out, flags=re.S)
    # advance width -> nearest 8
    am = re.search(r'<advance[^>]*width="([\d.]+)"', out)
    if am:
        w = float(am.group(1))
        sw = snap8(w)
        if sw != w:
            out = out.replace(am.group(0),
                              am.group(0).replace(f'width="{am.group(1)}"',
                                                  f'width="{sw:g}"'))
            changed = True
    return out, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('glyphs', nargs='*')
    ap.add_argument('--arabic', action='store_true')
    ap.add_argument('--master', choices=['Regular', 'Bold'], default=None)
    ap.add_argument('--dry', action='store_true', help='report, do not write')
    a = ap.parse_args()
    masters = [a.master] if a.master else ['Regular', 'Bold']
    total = 0
    for master in masters:
        gdir = f'sources/VirtuaGrotesk-{master}.ufo/glyphs'
        contents = plistlib.load(open(f'{gdir}/contents.plist', 'rb'))
        if a.glyphs:
            names = a.glyphs
        elif a.arabic:
            names = sorted(n for n in contents
                           if n.endswith('-ar') or '-ar.' in n)
        else:
            names = []
        for name in names:
            fn = contents.get(name)
            if not fn:
                continue
            path = os.path.join(gdir, fn)
            src = open(path).read()
            if '<contour' not in src:
                continue
            new, changed = process_glif(src)
            if changed and not a.dry:
                open(path, 'w').write(new)
            if changed:
                total += 1
        print(f'{master}: {"would snap" if a.dry else "snapped"} '
              f'{total} glyphs so far', flush=True)
    print(f'done: {total} glyph-writes')


if __name__ == '__main__':
    main()
