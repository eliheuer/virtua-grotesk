#!/usr/bin/env python3
"""Measure how Rubik's Arabic gains weight from Light to Black, so the
Virtua Arabic bold pass has a real reference for HOW the script embolden,
not just how much.

Rubik is UPM 1000; Virtua is 1024. All Rubik numbers are reported both raw
and scaled by 1024/1000 so they can be compared to Virtua directly.

The questions this answers:
  * does the outer contour stay put and the counter shrink (Virtua's Latin
    approach), or does the whole stroke grow outward?
  * how much does each stroke class grow?
  * how much do advances grow?
  * how much do the dots grow?

Usage:
    ./.venv/bin/python scripts/rubik_weight_deltas.py
"""

import pathlib
import plistlib
import xml.etree.ElementTree as ET

RUBIK = pathlib.Path.home() / "GH/repos/rubik/sources/designspace/masters"
LIGHT = RUBIK / "Rubik-Light.ufo"
BLACK = RUBIK / "Rubik-Black.ufo"
SCALE = 1024 / 1000


def load(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def flatten(ufo, cmap, name, steps=32, _seen=None):
    """Closed polylines for a glyph, components resolved, cubics sampled."""
    _seen = _seen or set()
    if name in _seen or name not in cmap:
        return []
    _seen = _seen | {name}
    root = ET.parse(ufo / "glyphs" / cmap[name]).getroot()
    polys = []
    for cont in root.iter("contour"):
        pts = [(float(p.get("x")), float(p.get("y")), p.get("type"))
               for p in cont.iter("point")]
        if not pts or not any(p[2] for p in pts):
            continue
        s = next(i for i, p in enumerate(pts) if p[2])
        pts = pts[s:] + pts[:s]
        poly = [(pts[0][0], pts[0][1])]
        prev, cur = pts[0], []
        for p in pts[1:] + [pts[0]]:
            if p[2]:
                if cur:
                    c1 = cur[0]
                    c2 = cur[-1]
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
        polys.append(poly)
    for comp in root.iter("component"):
        dx = float(comp.get("xOffset") or 0)
        dy = float(comp.get("yOffset") or 0)
        for poly in flatten(ufo, cmap, comp.get("base"), steps, _seen):
            polys.append([(x + dx, y + dy) for x, y in poly])
    return polys


def runs_h(polys, y):
    xs = []
    for poly in polys:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) / (y1 - y0) * (x1 - x0))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


def runs_v(polys, x):
    ys = []
    for poly in polys:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (x0 <= x < x1) or (x1 <= x < x0):
                ys.append(y0 + (x - x0) / (x1 - x0) * (y1 - y0))
    ys.sort()
    return [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]


def bbox(polys):
    xs = [x for p in polys for x, _ in p]
    ys = [y for p in polys for _, y in p]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def advance(ufo, cmap, name):
    a = ET.parse(ufo / "glyphs" / cmap[name]).getroot().find("advance")
    return float(a.get("width")) if a is not None else 0.0


# (glyph, probe kind, coordinate as a fraction of the glyph's own bbox)
PROBES = [
    ("alef-ar", "h", 0.5, "vertical stem"),
    ("lam-ar.init", "h", 0.6, "vertical stem"),
    ("behDotless-ar.init", "h", 0.35, "tooth"),
    ("behDotless-ar.init", "v", 0.5, "baseline bar"),
    ("behDotless-ar.medi", "v", 0.5, "baseline bar"),
    ("dal-ar", "v", 0.5, "horizontal stroke"),
    ("waw-ar", "h", 0.5, "round bowl"),
    ("heh-ar", "h", 0.5, "ring, both sides"),
    ("heh-ar", "v", 0.5, "ring, top+bottom"),
    ("meem-ar", "h", 0.6, "knot"),
    ("seen-ar.init", "v", 0.5, "baseline bar"),
    ("hah-ar.init", "v", 0.5, "bowl strokes"),
    ("ain-ar.init", "h", 0.5, "bowl strokes"),
]

WIDTH_GLYPHS = ["alef-ar", "behDotless-ar.init", "behDotless-ar.medi",
                "behDotless-ar", "dal-ar", "reh-ar", "waw-ar", "seen-ar",
                "seen-ar.init", "meem-ar", "heh-ar", "hah-ar", "ain-ar",
                "lam-ar", "kaf-ar", "sad-ar", "tah-ar", "qafDotless-ar",
                "noonghunna-ar", "fehDotless-ar.init"]

DOTS = ["dotabove-ar", "dotbelow-ar", "twodotshorizontalabove-ar",
        "threedotsupabove-ar", "hamzaabove-ar", "fatha-ar", "shadda-ar"]


def main():
    cl, cb = load(LIGHT), load(BLACK)

    print("=" * 74)
    print("RUBIK ARABIC — Light vs Black  (raw units, UPM 1000)")
    print("=" * 74)

    print("\n--- STROKE THICKNESS (ink runs across the stroke) ---")
    print(f"{'glyph / probe':38s} {'Light':>16s} {'Black':>16s}  ratio")
    ratios = []
    for name, kind, frac, label in PROBES:
        if name not in cl or name not in cb:
            print(f"{name:38s} (missing)")
            continue
        pl, pb = flatten(LIGHT, cl, name), flatten(BLACK, cb, name)
        if not pl or not pb:
            continue
        bl, bb_ = bbox(pl), bbox(pb)
        if kind == "h":
            y1 = bl[1] + (bl[3] - bl[1]) * frac
            y2 = bb_[1] + (bb_[3] - bb_[1]) * frac
            rl, rb = runs_h(pl, y1), runs_h(pb, y2)
        else:
            x1 = bl[0] + (bl[2] - bl[0]) * frac
            x2 = bb_[0] + (bb_[2] - bb_[0]) * frac
            rl, rb = runs_v(pl, x1), runs_v(pb, x2)
        wl = [b - a for a, b in rl]
        wb = [b - a for a, b in rb]
        if not wl or not wb:
            continue
        # compare the thinnest run on each side: that is the stroke
        ml, mb = min(wl), min(wb)
        r = mb / ml if ml else 0
        ratios.append(r)
        print(f"{name + ' ' + label:38s} "
              f"{','.join(f'{w:.0f}' for w in wl[:3]):>16s} "
              f"{','.join(f'{w:.0f}' for w in wb[:3]):>16s}  {r:.2f}")
    if ratios:
        ratios.sort()
        print(f"\nstroke ratio: median {ratios[len(ratios)//2]:.2f}  "
              f"range {ratios[0]:.2f}–{ratios[-1]:.2f}")

    print("\n--- OUTER BOUNDS: does the silhouette grow or stay put? ---")
    print(f"{'glyph':24s} {'Light bbox':>26s} {'Black bbox':>26s}")
    for name in WIDTH_GLYPHS[:10]:
        if name not in cl or name not in cb:
            continue
        bl, bb_ = bbox(flatten(LIGHT, cl, name)), bbox(flatten(BLACK, cb, name))
        if not bl or not bb_:
            continue
        print(f"{name:24s} "
              f"{f'{bl[0]:.0f},{bl[1]:.0f}..{bl[2]:.0f},{bl[3]:.0f}':>26s} "
              f"{f'{bb_[0]:.0f},{bb_[1]:.0f}..{bb_[2]:.0f},{bb_[3]:.0f}':>26s}")

    print("\n--- ADVANCE GROWTH ---")
    print(f"{'glyph':24s} {'Light':>8s} {'Black':>8s}  ratio  delta")
    aratios, adeltas = [], []
    for name in WIDTH_GLYPHS:
        if name not in cl or name not in cb:
            continue
        al, ab = advance(LIGHT, cl, name), advance(BLACK, cb, name)
        if not al:
            continue
        aratios.append(ab / al)
        adeltas.append(ab - al)
        print(f"{name:24s} {al:8.0f} {ab:8.0f}  {ab/al:.3f}  {ab-al:+.0f}")
    if aratios:
        aratios.sort()
        adeltas.sort()
        print(f"\nadvance ratio: median {aratios[len(aratios)//2]:.3f}  "
              f"median delta {adeltas[len(adeltas)//2]:+.0f} "
              f"({adeltas[len(adeltas)//2]*SCALE:+.0f} at Virtua UPM)")

    print("\n--- DOTS AND MARKS ---")
    print(f"{'glyph':30s} {'Light w x h':>16s} {'Black w x h':>16s}  ratio")
    for name in DOTS:
        if name not in cl or name not in cb:
            continue
        bl, bb_ = bbox(flatten(LIGHT, cl, name)), bbox(flatten(BLACK, cb, name))
        if not bl or not bb_:
            continue
        wl, hl = bl[2] - bl[0], bl[3] - bl[1]
        wb, hb = bb_[2] - bb_[0], bb_[3] - bb_[1]
        print(f"{name:30s} {f'{wl:.0f} x {hl:.0f}':>16s} "
              f"{f'{wb:.0f} x {hb:.0f}':>16s}  {wb/wl:.2f}")

    print("\n--- VERTICAL ZONES: do heights move? ---")
    for name in ("alef-ar", "behDotless-ar.init", "lam-ar.init", "hah-ar.init",
                 "seen-ar.init", "heh-ar"):
        if name not in cl or name not in cb:
            continue
        bl, bb_ = bbox(flatten(LIGHT, cl, name)), bbox(flatten(BLACK, cb, name))
        if not bl or not bb_:
            continue
        print(f"{name:24s} top {bl[3]:6.0f} -> {bb_[3]:6.0f} "
              f"({bb_[3]-bl[3]:+.0f})   bottom {bl[1]:6.0f} -> {bb_[1]:6.0f} "
              f"({bb_[1]-bl[1]:+.0f})")


if __name__ == "__main__":
    main()
