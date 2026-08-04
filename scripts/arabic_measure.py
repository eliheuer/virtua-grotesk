#!/usr/bin/env python3
"""Measure the green (approved) Arabic glyphs in both masters.

Read-only: loads the UFOs with defcon but never saves them. Emits the
measurements that become the Arabic grammar constants: stroke weights,
dot geometry, vertical zones, advances. Ray-casting is done on flattened
outlines (cubics sampled densely), accurate well inside the 2-unit grid.

Usage:
    ./.venv/bin/python scripts/arabic_measure.py [--json build/arabic-measure.json]
"""

import argparse
import json
import pathlib
import sys

import defcon

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = {
    "Regular": REPO / "sources" / "VirtuaGrotesk-Regular.ufo",
    "Bold": REPO / "sources" / "VirtuaGrotesk-Bold.ufo",
}

GREEN_PREFIX = "0.09,"


def flatten(glyph, font, steps=48):
    """Return list of closed polylines (lists of (x, y)) for a glyph,
    components resolved, cubics sampled."""
    polys = []
    for contour in glyph:
        pts = list(contour)
        if not pts:
            continue
        # build segment list: each segment ends at an on-curve point
        segs = []
        # rotate so we start at an on-curve point
        start = next((i for i, p in enumerate(pts) if p.segmentType), None)
        if start is None:
            continue
        pts = pts[start:] + pts[:start]
        cur = []
        for p in pts[1:] + [pts[0]]:
            cur.append(p)
            if p.segmentType:
                segs.append(cur)
                cur = []
        poly = [(pts[0].x, pts[0].y)]
        prev = (pts[0].x, pts[0].y)
        for seg in segs:
            end = (seg[-1].x, seg[-1].y)
            offs = [(q.x, q.y) for q in seg[:-1]]
            if not offs:
                poly.append(end)
            else:
                # cubic (2 offcurves) or quad — sample
                if len(offs) == 1:
                    c1 = c2 = offs[0]
                else:
                    c1, c2 = offs[0], offs[-1]
                x0, y0 = prev
                for i in range(1, steps + 1):
                    t = i / steps
                    mt = 1 - t
                    x = (mt**3 * x0 + 3 * mt**2 * t * c1[0]
                         + 3 * mt * t**2 * c2[0] + t**3 * end[0])
                    y = (mt**3 * y0 + 3 * mt**2 * t * c1[1]
                         + 3 * mt * t**2 * c2[1] + t**3 * end[1])
                    poly.append((x, y))
            prev = end
        polys.append(poly)
    for comp in glyph.components:
        base = font[comp.baseGlyph]
        xx, xy, yx, yy, dx, dy = comp.transformation
        for poly in flatten(base, font, steps):
            polys.append([(xx * x + yx * y + dx, xy * x + yy * y + dy)
                          for x, y in poly])
    return polys


def ink_runs_h(polys, y):
    """X-intervals of ink along horizontal line at y (even-odd)."""
    xs = []
    for poly in polys:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (y0 <= y < y1) or (y1 <= y < y0):
                t = (y - y0) / (y1 - y0)
                xs.append(x0 + t * (x1 - x0))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


def ink_runs_v(polys, x):
    """Y-intervals of ink along vertical line at x (even-odd)."""
    ys = []
    for poly in polys:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (x0 <= x < x1) or (x1 <= x < x0):
                t = (x - x0) / (x1 - x0)
                ys.append(y0 + t * (y1 - y0))
    ys.sort()
    return [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]


def bbox(polys):
    xs = [x for poly in polys for x, _ in poly]
    ys = [y for poly in polys for _, y in poly]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def runs_str(runs):
    return ", ".join(f"{a:.0f}..{b:.0f} ({b - a:.0f})" for a, b in runs)


def measure_master(name, path):
    font = defcon.Font(str(path))
    out = {"master": name, "glyphs": {}}
    green = []
    for g in font:
        if "-ar" not in g.name:
            continue
        color = g.lib.get("public.markColor", "")
        if color.startswith(GREEN_PREFIX):
            green.append(g.name)
    out["green"] = sorted(green)

    for gname in sorted(green):
        g = font[gname]
        polys = flatten(g, font)
        bb = bbox(polys)
        rec = {
            "advance": g.width,
            "bbox": [round(v, 1) for v in bb] if bb else None,
            "contours": len(g),
            "components": [c.baseGlyph for c in g.components],
        }
        out["glyphs"][gname] = rec

    # targeted stroke probes on canonical forms
    probes = {}

    def probe(gname, kind, coord, label):
        if gname not in font:
            return
        polys = flatten(font[gname], font)
        runs = ink_runs_h(polys, coord) if kind == "h" else ink_runs_v(polys, coord)
        probes.setdefault(gname, []).append(
            {"label": label, "kind": kind, "at": coord,
             "runs": [[round(a, 1), round(b, 1)] for a, b in runs]})

    # vertical stems: horizontal ray at a given y
    probe("alef-ar", "h", 400, "stem width @y=400")
    probe("lam-ar.init", "h", 500, "stem width @y=500")
    probe("beh-ar.init", "h", 150, "tooth width @y=150")
    probe("noon-ar.init", "h", 150, "tooth width @y=150")
    probe("seen-ar.init", "h", 120, "teeth widths @y=120")
    # horizontal strokes: vertical ray at a given x
    for gname in ("beh-ar.init", "beh-ar.medi", "lam-ar.medi", "seen-ar.init"):
        if gname in font:
            g = font[gname]
            probe(gname, "v", g.width / 2, "baseline bar @x=mid")
    # round/bowl strokes
    probe("waw-ar", "v", 0, None)  # placeholder replaced below
    probes.pop("waw-ar", None)
    for gname in ("waw-ar", "ain-ar.init", "hah-ar.init", "heh-ar.medi",
                  "dal-ar", "reh-ar.fina", "yeh-ar.fina", "lam-ar.fina",
                  "ghain-ar.init", "farsiYeh-ar.fina", "kaf-ar.fina"):
        if gname in font:
            polys = flatten(font[gname], font)
            bb = bbox(polys)
            if bb is None:
                continue
            midy = (bb[1] + bb[3]) / 2
            midx = (bb[0] + bb[2]) / 2
            probe(gname, "h", round(midy), f"h-ink @y={round(midy)} (bbox mid)")
            probe(gname, "v", round(midx), f"v-ink @x={round(midx)} (bbox mid)")
    # dots
    for gname in ("dotabove-ar", "dotbelow-ar", "twodotshorizontalabove-ar",
                  "threedotsupabove-ar", "hamzaabove-ar", "hamzabelow-ar"):
        if gname in font:
            polys = flatten(font[gname], font)
            bb = bbox(polys)
            if bb:
                probes.setdefault(gname, []).append(
                    {"label": "bbox", "bbox": [round(v, 1) for v in bb]})

    out["probes"] = probes
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=pathlib.Path,
                    default=REPO / "build" / "arabic-measure.json")
    args = ap.parse_args()

    results = {}
    for name, path in MASTERS.items():
        results[name] = measure_master(name, path)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(results, indent=1))
    print(f"wrote {args.json}")

    # console summary
    for master, data in results.items():
        print(f"\n=== {master} — {len(data['green'])} green Arabic glyphs ===")
        for gname, plist in data["probes"].items():
            for p in plist:
                if "bbox" in p:
                    x0, y0, x1, y1 = p["bbox"]
                    print(f"{gname:34s} bbox {x0:6.0f},{y0:6.0f} .. {x1:6.0f},{y1:6.0f}"
                          f"  (w {x1 - x0:.0f}, h {y1 - y0:.0f})")
                else:
                    runs = ", ".join(f"{a:.0f}..{b:.0f} ({b - a:.0f})"
                                     for a, b in p["runs"])
                    print(f"{gname:34s} {p['label'] or '':28s} {runs}")


if __name__ == "__main__":
    sys.exit(main())
