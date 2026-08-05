#!/usr/bin/env python3
"""Embolden Arabic outlines from Regular into the Bold master.

Anisotropic (elliptical) outline offset: every point moves along its
outward-from-ink normal by dx horizontally and dy vertically. Point count,
point type and component list never change, so master compatibility holds
by construction.

The offset amounts come from Virtua's own Latin Regular -> Bold
(dx 48, dy 36 reproduces every Latin stroke class to within ~4 units);
see documentation/source/arabic-bold-contract.md.

Direction convention: contours are outer-CCW / holes-CW (enforced by
scripts/normalize_winding.py), so rotating the tangent by -90 degrees
always points away from the ink, for outer contours and holes alike.

Corners are mitered — the two adjacent offset edges are intersected —
so a right-angle corner keeps its full offset instead of collapsing to
0.707 of it.

Usage:
    ./.venv/bin/python scripts/embolden.py --dry-run
    ./.venv/bin/python scripts/embolden.py [glyph ...]
"""

import math
import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import MASTERS, contour_xml, fmt_num  # noqa: E402

REGULAR, BOLD = MASTERS

# Per-side offset. dx 48 / dy 36 reproduces Virtua's LATIN Regular -> Bold
# exactly, but the Arabic forms are about a quarter shorter than the Latin
# (tooth top 432 against x-height 576), so the same absolute offset closes
# their counters. The Arabic default is scaled by that ratio; override with
# --dx/--dy.
DX, DY = 36.0, 27.0

# Hard metric lines: a point sitting on one stays on it. The baseline
# matters most — ink that drops below it makes joined letters step.
PINNED_Y = (0.0, 768.0)
PIN_TOL = 2.0

# The font declares WinAscent 1094 / WinDescent 438; ink outside that fails
# family/win_ascent_and_descent, so the offset is capped to stay inside.
MIN_Y, MAX_Y = -438.0, 1094.0

# Canonical joining geometry (see the Arabic bold contract).
BAR_R, BAR_B = 104.0, 176.0          # baseline joining bar height
STUB_R = ((0.0, 0.0), (-16.0, 16.0), (-16.0, 88.0), (0.0, 104.0))
STUB_B = ((0.0, 0.0), (-16.0, 16.0), (-16.0, 160.0), (0.0, 176.0))


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def read(ufo, cmap, name):
    root = ET.parse(ufo / "glyphs" / cmap[name]).getroot()
    cs = []
    for cont in root.iter("contour"):
        cs.append([(float(p.get("x")), float(p.get("y")), p.get("type"),
                    p.get("smooth") == "yes")
                   for p in cont.iter("point")])
    adv = root.find("advance")
    return cs, (float(adv.get("width")) if adv is not None else 0.0)


def unit(vx, vy):
    n = math.hypot(vx, vy)
    return (vx / n, vy / n) if n > 1e-9 else (0.0, 0.0)


def offset_for(tx, ty, dy=DY, sign=1.0):
    """Elliptical displacement for an edge with unit tangent (tx, ty).

    `sign` selects which rotation of the tangent points AWAY FROM INK.
    Rotating -90 deg gives (ty, -tx); +90 gives the negation. Which one is
    correct depends on the contour's own winding and whether it is an outer
    contour or a hole — see `away_sign`. The green Arabic has inconsistent
    winding, so this cannot be assumed.
    """
    nx, ny = sign * ty, sign * -tx
    return (DX * nx, dy * ny)


def signed_area(contour):
    p = [(x, y) for x, y, t, s in contour]
    return sum(x0 * y1 - x1 * y0
               for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1])) / 2


def _inside(pt, poly):
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y):
            if x < x0 + (y - y0) / (y1 - y0) * (x1 - x0):
                hit = not hit
    return hit


def away_sign(i, contours, polys):
    """+1 if rotating the tangent -90 deg points away from ink, -1 if +90
    does. Outer contour and CCW, or hole and CW -> -90 (i.e. +1)."""
    probe = [(x, y) for x, y, t, s in contours[i] if t]
    depth = 0
    for j, other in enumerate(polys):
        if j == i or not probe:
            continue
        if all(_inside(p, other) for p in probe):
            depth += 1
    is_outer = depth % 2 == 0
    is_ccw = signed_area(contours[i]) > 0
    return 1.0 if is_outer == is_ccw else -1.0


def flatten_polys(contours, steps=16):
    """Sampled polylines, for the scanline test below."""
    out = []
    for pts in contours:
        if not pts or not any(p[2] for p in pts):
            continue
        s = next(i for i, p in enumerate(pts) if p[2])
        pts = pts[s:] + pts[:s]
        poly = [(pts[0][0], pts[0][1])]
        prev, cur = pts[0], []
        for p in pts[1:] + [pts[0]]:
            if p[2]:
                if cur:
                    c1, c2 = cur[0], cur[-1]
                    x0, y0 = prev[0], prev[1]
                    for i in range(1, steps + 1):
                        t = i / steps
                        mt = 1 - t
                        poly.append((
                            mt**3 * x0 + 3 * mt**2 * t * c1[0]
                            + 3 * mt * t**2 * c2[0] + t**3 * p[0],
                            mt**3 * y0 + 3 * mt**2 * t * c1[1]
                            + 3 * mt * t**2 * c2[1] + t**3 * p[1]))
                else:
                    poly.append((p[0], p[1]))
                prev, cur = p, []
            else:
                cur.append(p)
        out.append(poly)
    return out


def _vruns(polys, x):
    ys = []
    for poly in polys:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (x0 <= x < x1) or (x1 <= x < x0):
                ys.append(y0 + (x - x0) / (x1 - x0) * (y1 - y0))
    ys.sort()
    return [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]


def dy_at(polys, x, y):
    """The vertical growth this edge should take.

    A stroke with one edge on a hard metric line can only grow away from
    it, so the free edge takes the whole 2*DY. That is what Virtua's Latin
    does: the cap arm of `E` is 96 in Regular and 168 in Bold while the cap
    line itself never moves.
    """
    for lo, hi in _vruns(polys, x):
        if lo - PIN_TOL <= y <= hi + PIN_TOL:
            other = lo if abs(y - hi) < abs(y - lo) else hi
            if any(abs(other - pin) <= PIN_TOL for pin in PINNED_Y):
                return 2 * DY
            return DY
    return DY


def on_curve_indices(contour):
    return [i for i, p in enumerate(contour) if p[2]]


def embolden_contour(contour, polys=None, sign=1.0):
    """Displace every point. On-curve points are mitered against their two
    adjacent edges; off-curve points take their own segment's edge offset."""
    n = len(contour)
    if n < 3:
        return list(contour)

    def edge_tangent(i, j):
        """Tangent of the edge leaving point i toward point j, skipping
        coincident points."""
        for k in range(1, n):
            a = contour[i]
            b = contour[(j + k - 1) % n]
            t = unit(b[0] - a[0], b[1] - a[1])
            if t != (0.0, 0.0):
                return t
        return (1.0, 0.0)

    out = []
    for i, (x, y, typ, smooth) in enumerate(contour):
        t_out = edge_tangent(i, i + 1)
        # incoming tangent: direction arriving at i, skipping any coincident
        # points (several green Arabic glyphs repeat a point at notch
        # vertices, which would otherwise give a zero tangent)
        t_in = (0.0, 0.0)
        for k in range(1, n):
            p = contour[(i - k) % n]
            t_in = unit(x - p[0], y - p[1])
            if t_in != (0.0, 0.0):
                break
        if t_in == (0.0, 0.0):
            t_in = t_out
        dy_here = dy_at(polys, x, y) if polys else DY
        if typ is None:
            # off-curve: follow its own edge, no mitering
            ox, oy = offset_for(*t_out, dy=dy_here, sign=sign)
            out.append((x + ox, y + oy, typ, smooth))
            continue
        d_in = offset_for(*t_in, dy=dy_here, sign=sign)
        d_out = offset_for(*t_out, dy=dy_here, sign=sign)
        cross = t_in[0] * t_out[1] - t_in[1] * t_out[0]
        if abs(cross) < 1e-6:
            dx_, dy_ = (d_in[0] + d_out[0]) / 2, (d_in[1] + d_out[1]) / 2
        else:
            # intersect the offset incoming edge with the offset outgoing
            # edge: P + d_in + s*t_in  ==  P + d_out + u*t_out
            rx, ry = d_out[0] - d_in[0], d_out[1] - d_in[1]
            s = (rx * t_out[1] - ry * t_out[0]) / cross
            dx_, dy_ = d_in[0] + s * t_in[0], d_in[1] + s * t_in[1]
            # a miter longer than 3x the nominal offset is a spike: clamp
            lim = 3.0 * max(DX, DY)
            m = math.hypot(dx_, dy_)
            if m > lim:
                dx_, dy_ = dx_ * lim / m, dy_ * lim / m
        out.append((x + dx_, y + dy_, typ, smooth))
    return out


def unify_coincident(original, moved):
    """Points that share a position in Regular must share it in Bold.

    Several green Arabic glyphs (ain-ar.medi, seen-ar.init, reh-ar) repeat
    a point at a notch vertex. Offsetting the copies independently turns
    the zero-length segment between them into a reversed one, which reads
    as an open corner and gets erased at build time.
    """
    n = len(original)
    groups, seen = [], [False] * n
    for i in range(n):
        if seen[i]:
            continue
        run = [i]
        j = (i + 1) % n
        while j != i and original[j][:2] == original[i][:2]:
            run.append(j)
            seen[j] = True
            j = (j + 1) % n
        seen[i] = True
        if len(run) > 1:
            groups.append(run)
    out = list(moved)
    for run in groups:
        ax = sum(out[k][0] for k in run) / len(run)
        ay = sum(out[k][1] for k in run) / len(run)
        for k in run:
            out[k] = (ax, ay, out[k][2], out[k][3])
    return out


def guard_reversals(original, moved, iters=12):
    """Stop the offset from making a segment double back on itself.

    Offsetting a tight concave corner can push its two points past each
    other. The resulting little loop is an "open corner", which ufo2ft's
    EraseOpenCornersFilter then DELETES — silently changing the Bold's
    point count and breaking master compatibility. Cheaper to never make
    one: back off the displacement at any corner whose segment would
    reverse.
    """
    n = len(original)
    disp = [(m[0] - o[0], m[1] - o[1]) for o, m in zip(original, moved)]
    scale = [1.0] * n
    for _ in range(iters):
        bad = False
        for i in range(n):
            j = (i + 1) % n
            ox = original[j][0] - original[i][0]
            oy = original[j][1] - original[i][1]
            if ox * ox + oy * oy < 1e-9:
                continue
            nx = (original[j][0] + disp[j][0] * scale[j]) \
                - (original[i][0] + disp[i][0] * scale[i])
            ny = (original[j][1] + disp[j][1] * scale[j]) \
                - (original[i][1] + disp[i][1] * scale[i])
            if ox * nx + oy * ny < 0.1 * (ox * ox + oy * oy):
                scale[i] *= 0.65
                scale[j] *= 0.65
                bad = True
        if not bad:
            break
    return [(o[0] + d[0] * s, o[1] + d[1] * s, o[2], o[3])
            for o, d, s in zip(original, disp, scale)]


def has_open_corners(contours):
    """True if ufo2ft's EraseOpenCorners pass would change this outline.

    That filter runs during the build and DELETES the offending points, so
    a Bold with open corners silently stops matching the Regular's point
    count. Asking the real filter is more reliable than guessing which
    corners are unsafe.
    """
    import defcon
    from glyphsLib.filters.eraseOpenCorners import EraseOpenCornersPen
    from fontTools.pens.recordingPen import RecordingPen

    g = defcon.Glyph()
    pen = g.getPointPen()
    for c in contours:
        pen.beginPath()
        for x, y, t, s in c:
            pen.addPoint((x, y), t, s)
        pen.endPath()
    rec = RecordingPen()
    p = EraseOpenCornersPen(rec)
    for contour in list(g):
        contour.draw(p)
    return bool(p.affected)


def apply_pins(original, moved):
    """Restore coordinates that sat on a hard metric line."""
    out = []
    for (ox, oy, t, s), (mx, my, _t, _s) in zip(original, moved):
        ny = my
        for pin in PINNED_Y:
            if abs(oy - pin) <= PIN_TOL:
                ny = pin
                break
        out.append((mx, ny, t, s))
    return out


def snap(contours):
    return [[(round(x / 2) * 2, round(y / 2) * 2, t, s) for x, y, t, s in c]
            for c in contours]


def canonicalize_joins(original, moved):
    """Rebuild the joining stub to the Bold canon.

    The stub is located in the ORIGINAL contour by its Regular signature
    (four points at x 0/−16 with y 0,16,88,104, in either direction); the
    same indices in the emboldened contour are then set to the Bold stub.
    Joining geometry must agree to the unit across every joining glyph, so
    it is replaced outright rather than offset.
    """
    out = []
    for c_o, c_m in zip(original, moved):
        pts = list(c_m)
        n = len(c_o)
        for i in range(n):
            run = tuple(c_o[(i + k) % n][:2] for k in range(4))
            if run == STUB_R:
                canon = STUB_B
            elif tuple(reversed(run)) == STUB_R:
                canon = tuple(reversed(STUB_B))
            else:
                continue
            for k in range(4):
                j = (i + k) % n
                x, y = canon[k]
                pts[j] = (x, y, pts[j][2], pts[j][3])
        out.append(pts)
    return out


def lift_bar_tops(original, moved):
    """Any point that sat exactly on the Regular bar top (y = 104) becomes
    the Bold bar top (y = 176), so every joining glyph agrees."""
    out = []
    for (ox, oy, t, s), (mx, my, _t, _s) in zip(original, moved):
        out.append((mx, BAR_B if abs(oy - BAR_R) <= PIN_TOL else my, t, s))
    return out


def regenerate_bold(name, contours, advance, cmap_r, cmap_b):
    """Write a complete Bold glif from the emboldened contours.

    Needed when the Regular's structure has changed under us — a glyph
    redrawn from components into outlines, say — so the Bold has no
    matching contour blocks to patch. Unicodes and anchors are carried
    over from the Regular so nothing is lost.
    """
    src = ET.parse(REGULAR / "glyphs" / cmap_r[name]).getroot()
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            f'<glyph name="{name}" format="2">']
    for u in src.iter("unicode"):
        body.append(f'\t<unicode hex="{u.get("hex")}"/>')
    body.append(f'\t<advance width="{fmt_num(advance)}"/>')
    body.append("\t<outline>")
    for c in contours:
        body.append(contour_xml(c))
    body.append("\t</outline>")
    for a in src.iter("anchor"):
        body.append(f'\t<anchor name="{a.get("name")}" '
                    f'x="{a.get("x")}" y="{a.get("y")}"/>')
    body += ["\t<lib>", "\t\t<dict>",
             "\t\t\t<key>public.markColor</key>",
             "\t\t\t<string>0,0.67,0.91,1</string>",
             "\t\t</dict>", "\t</lib>", "</glyph>", ""]
    (BOLD / "glyphs" / cmap_b[name]).write_text("\n".join(body))


def write_bold(name, contours, advance, cmap_b, cmap_r=None):
    path = BOLD / "glyphs" / cmap_b[name]
    text = path.read_text()
    blocks = re.findall(r"\t\t<contour>.*?\t\t</contour>", text, re.S)
    if len(blocks) != len(contours):
        if cmap_r is not None:
            regenerate_bold(name, contours, advance, cmap_r, cmap_b)
            return
        raise AssertionError(f"{name}: {len(blocks)} blocks vs "
                             f"{len(contours)} contours")
    for old, new in zip(blocks, contours):
        text = text.replace(old, contour_xml(new), 1)
    text = re.sub(r'<advance width="[-\d.]+"/>',
                  f'<advance width="{fmt_num(advance)}"/>', text, count=1)
    path.write_text(text)


def is_arabic(name):
    return "-ar" in name or name.startswith("arabic")


def _resolved_bbox(ufo, cmap, name, _seen=None):
    _seen = _seen or set()
    if name in _seen or name not in cmap:
        return None
    _seen = _seen | {name}
    root = ET.parse(ufo / "glyphs" / cmap[name]).getroot()
    ys = [float(p.get("y")) for p in root.iter("point")]
    for comp in root.iter("component"):
        sub = _resolved_bbox(ufo, cmap, comp.get("base"), _seen)
        if sub:
            dy = float(comp.get("yOffset") or 0)
            ys += [sub[0] + dy, sub[1] + dy]
    return (min(ys), max(ys)) if ys else None


def refit_composites(cmap_b):
    """Nudge Bold composites back inside the vertical envelope.

    Component offsets were computed from the Regular geometry; the Bold
    marks are larger, so a stacked mark can drop below the descent limit.
    Component offsets are free to differ between masters, so this only
    moves the mark, never the skeleton.
    """
    fixed = []
    for name, fn in sorted(cmap_b.items()):
        if not is_arabic(name):
            continue
        path = BOLD / "glyphs" / fn
        text = path.read_text()
        if "<component" not in text:
            continue
        bb = _resolved_bbox(BOLD, cmap_b, name)
        if not bb:
            continue
        shift = 0.0
        if bb[0] < MIN_Y:
            shift = MIN_Y - bb[0]
        elif bb[1] > MAX_Y:
            shift = MAX_Y - bb[1]
        if not shift:
            continue
        shift = round(shift / 2) * 2
        comps = re.findall(r"\t\t<component [^/]*/>", text)
        if len(comps) < 2:
            continue
        last = comps[-1]                       # the mark rides last
        cur = re.search(r'yOffset="([-\d.]+)"', last)
        new_dy = (float(cur.group(1)) if cur else 0.0) + shift
        if cur:
            fixed_tag = re.sub(r'yOffset="[-\d.]+"',
                               f'yOffset="{fmt_num(new_dy)}"', last)
        else:
            fixed_tag = last.replace("/>", f' yOffset="{fmt_num(new_dy)}"/>')
        path.write_text(text.replace(last, fixed_tag, 1))
        fixed.append((name, shift))
    return fixed


def main():
    global DX, DY
    dry = "--dry-run" in sys.argv
    for i, a in enumerate(sys.argv):
        if a == "--dx":
            DX = float(sys.argv[i + 1])
        if a == "--dy":
            DY = float(sys.argv[i + 1])
    skip = set()
    for i, a in enumerate(sys.argv):
        if a in ("--dx", "--dy"):
            skip.add(i)
            skip.add(i + 1)
    names = [a for i, a in enumerate(sys.argv[1:], 1)
             if not a.startswith("--") and i not in skip]
    cr, cb = contents(REGULAR), contents(BOLD)
    done, skipped, reduced = 0, [], []

    for name in sorted(cr):
        if names:
            if name not in names:
                continue
        elif not is_arabic(name):
            continue
        cs_r, adv_r = read(REGULAR, cr, name)
        if not cs_r:
            continue                      # composite or empty: nothing to do
        polys = flatten_polys(cs_r)
        signs = [away_sign(ci, cs_r, polys) for ci in range(len(cs_r))]

        def build(scale):
            out = []
            for c, sign in zip(cs_r, signs):
                m = embolden_contour(c, polys, sign)
                if scale != 1.0:
                    m = [(o[0] + (p[0] - o[0]) * scale,
                          o[1] + (p[1] - o[1]) * scale, p[2], p[3])
                         for o, p in zip(c, m)]
                m = unify_coincident(c, m)
                m = guard_reversals(c, m)
                m = apply_pins(c, m)
                m = lift_bar_tops(c, m)
                out.append(m)
            return canonicalize_joins(cs_r, snap(out))

        def fits_envelope(cs):
            ys = [p[1] for c in cs for p in c]
            return not ys or (min(ys) >= MIN_Y and max(ys) <= MAX_Y)

        # Back the offset off for this glyph until the real EraseOpenCorners
        # pass leaves it alone (otherwise the build silently drops points)
        # and the result still fits the font's vertical envelope.
        moved, used = None, 1.0
        for scale in (1.0, 0.85, 0.7, 0.55, 0.4, 0.28, 0.18, 0.1, 0.0):
            cand = build(scale)
            if not has_open_corners(cand) and fits_envelope(cand):
                moved, used = cand, scale
                break
        if moved is None:
            moved, used = build(0.0), 0.0
        if used < 1.0:
            reduced.append((name, used))

        def span(cs):
            xs = [x for c in cs for x, y, t, s in c]
            return (min(xs), max(xs)) if xs else (0.0, 0.0)
        lo_r, hi_r = span(cs_r)
        lo_m, hi_m = span(moved)
        if adv_r == 0:
            advance = 0.0             # combining marks stay zero-width
        elif abs(adv_r - hi_r) <= PIN_TOL:
            # a joining bar that terminates exactly at the advance: keep it
            # there, or the seam with the next letter opens up
            advance = round(hi_m / 2) * 2
        else:
            # preserve sidebearings: the advance absorbs the ink growth
            advance = adv_r + (hi_m - hi_r) - (lo_m - lo_r)
            advance = round(advance / 2) * 2
        if dry:
            print(f"{name:32s} adv {adv_r:5.0f} -> {advance:5.0f}   "
                  f"ink {lo_r:.0f}..{hi_r:.0f} -> {lo_m:.0f}..{hi_m:.0f}")
        else:
            try:
                write_bold(name, moved, advance, cb, cr)
                done += 1
            except AssertionError as e:
                skipped.append(str(e))
    if not dry:
        moved_comps = refit_composites(cb)
        print(f"emboldened {done} glyphs into the Bold master "
              f"(dx {DX:.0f}, dy {DY:.0f})")
        if moved_comps:
            print(f"  {len(moved_comps)} composite(s) had their mark nudged "
                  f"back inside the vertical envelope")
        for s in skipped:
            print("  SKIP " + s)
        if reduced:
            print(f"  {len(reduced)} glyph(s) took a reduced offset to avoid "
                  f"open corners:")
            for n, s in sorted(reduced, key=lambda r: r[1]):
                print(f"    {n:32s} x{s:.2f}")


if __name__ == "__main__":
    main()
