"""Curve normalizer: re-fit off-curve handles to canonical tension.

The design system fixes on-curve extrema (stems, bowls, horizontals on
the quanta ladder). This tool makes the HANDLES just as systematic:
for every cubic segment whose end tangents are axis-aligned (the
system's smooth-extremum convention), recompute each handle as

    handle = on_curve + tangent_dir * round_to_grid(kappa * span)

where span is the segment's extent along the tangent axis and kappa
is the canonical tension constant. On-curve points NEVER move.

    ./.venv/bin/python scripts/curve_normalize.py Bold d --kappa 0.58
    ./.venv/bin/python scripts/curve_normalize.py Bold d --dry

Writes glif XML surgically (repo style preserved). Marks nothing;
grading colors are untouched.
"""
import argparse, re, sys

HANDLE_GRID = 4  # handle lengths snap here (prefer 8 via rounding bias)

def snap(v, grid=HANDLE_GRID):
    return int(round(v / grid)) * grid

def parse(src):
    pts = []
    for m in re.finditer(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
                         r'((?: type="(\w+)")?(?: smooth="yes")?)/>', src):
        pts.append(dict(x=float(m.group(1)), y=float(m.group(2)),
                        raw=m.group(0), typ=m.group(4) or 'offcurve'))
    return pts

def contours(src):
    return [parse(c.group(1)) for c in
            re.finditer(r'<contour>(.*?)</contour>', src, re.S)]

def normalize(src, kappa):
    edits = {}  # old raw -> (new_x, new_y)
    for cont in contours(src):
        n = len(cont)
        ons = [i for i, p in enumerate(cont) if p['typ'] != 'offcurve']
        for k in range(len(ons)):
            i0, i1 = ons[k], ons[(k + 1) % len(ons)]
            seg = []
            j = (i0 + 1) % n
            while j != i1:
                seg.append(j); j = (j + 1) % n
            if len(seg) != 2:
                continue  # not a cubic
            a, b = cont[i0], cont[i1]
            h1, h2 = cont[seg[0]], cont[seg[1]]
            # tangent axes: handle collinear with its on-curve point
            for on, h in ((a, h1), (b, h2)):
                dx, dy = h['x'] - on['x'], h['y'] - on['y']
                if abs(dx) > 0.01 and abs(dy) > 0.01:
                    break  # diagonal tangent: leave this segment alone
            else:
                span_x = abs(b['x'] - a['x']); span_y = abs(b['y'] - a['y'])
                for on, h in ((a, h1), (b, h2)):
                    dx, dy = h['x'] - on['x'], h['y'] - on['y']
                    if abs(dy) <= 0.01 and abs(dx) > 0.01:   # horizontal tangent
                        L = snap(kappa * span_x)
                        new = (on['x'] + (L if dx > 0 else -L), on['y'])
                    elif abs(dx) <= 0.01 and abs(dy) > 0.01:  # vertical tangent
                        L = snap(kappa * span_y)
                        new = (on['x'], on['y'] + (L if dy > 0 else -L))
                    else:
                        continue
                    if (new[0], new[1]) != (h['x'], h['y']):
                        edits[h['raw']] = new
    out = src
    for raw, (nx, ny) in edits.items():
        rest = re.match(r'<point x="-?[\d.]+" y="-?[\d.]+"(.*?)/>', raw).group(1)
        out = out.replace(raw, f'<point x="{nx:g}" y="{ny:g}"{rest}/>')
    return out, edits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('master', choices=['Regular', 'Bold'])
    ap.add_argument('glyph')
    ap.add_argument('--kappa', type=float, default=0.58)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    fn = args.glyph if args.glyph.islower() else args.glyph + '_'
    path = f'sources/VirtuaGrotesk-{args.master}.ufo/glyphs/{fn}.glif'
    src = open(path).read()
    out, edits = normalize(src, args.kappa)
    for raw, new in edits.items():
        old = re.match(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"', raw).groups()
        print(f'  ({old[0]},{old[1]}) -> {new}')
    print(f'{len(edits)} handles re-fitted (kappa={args.kappa})')
    if not args.dry and edits:
        open(path, 'w').write(out)
        print('written:', path)

if __name__ == '__main__':
    main()
