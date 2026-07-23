#!/usr/bin/env python3
"""Normalized metric comparison against reference fonts.

Measure a set of Virtua glyphs (default: H O n o) and the same glyphs in one
or more reference fonts (Inter, Geist, ...), then print *ratio* tables. Raw
font-unit sizes are meaningless across fonts with different UPMs and
proportions, so everything a designer actually tunes is expressed as a ratio
(contrast, cap-vs-lowercase weight, sidebearing openness, ...). Comparing a
Virtua ratio to Inter's tells you whether Virtua is heavier, tighter, more
open, etc. — independent of scale.

This is the reusable version of the ad-hoc measurement done during the n/o
design pass. See documentation/normalized-metrics-workflow.md for the how and
why, and for how to read the tables.

Usage:
    python3 scripts/normalize_metrics.py                 # H O n o vs Inter, Geist
    python3 scripts/normalize_metrics.py --glyphs H O n o
    python3 scripts/normalize_metrics.py --master Bold   # a different master
    python3 scripts/normalize_metrics.py --refs inter    # only Inter

Measurement method: cast a horizontal scan line across the glyph at a fixed
fraction of its reference height (x-height for lowercase, cap-height for
caps), and read the crossings. Two stems give 4 crossings (stem, counter,
stem); a round gives 4 (side, counter, side). A vertical scan at the center
gives the crown (top overshoot thickness). Everything is flattened to
polylines first so the same crossing code serves UFO cubics and TTF quads.
"""
import argparse
import os
import plistlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid_qa as gq  # noqa: E402
from fontTools.pens.recordingPen import RecordingPen  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.varLib.instancer import instantiateVariableFont  # noqa: E402

# glyph -> (case, kind, scan-height fraction of the reference height).
#   case: 'cap' scans against cap-height, 'lc' against x-height.
#   kind: 'stem' (two uprights: stem/counter/stem) or 'round' (side/counter/side).
#   hfrac: where to cast the horizontal scan — pick a band clear of crossbars
#          and arches (H's crossbar sits near mid, so scan its stems high).
GLYPH_SPEC = {
    "H": ("cap", "stem", 0.72),
    "O": ("cap", "round", 0.50),
    "I": ("cap", "stem", 0.50),
    "n": ("lc", "stem", 0.45),
    "o": ("lc", "round", 0.50),
    "l": ("lc", "stem", 0.50),
}

REF_FONTS = {
    "inter": "/Users/eli/GH/repos/google-fonts/ofl/inter/Inter[opsz,wght].ttf",
    "geist": "/Users/eli/GH/repos/google-fonts/ofl/geist/Geist[wght].ttf",
}


# ---------------------------------------------------------------- flattening
def _flatten_cubic(p0, c1, c2, p3, n=200):
    out = []
    for i in range(1, n + 1):
        t = i / n
        mt = 1 - t
        out.append((
            mt**3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t**3 * p3[0],
            mt**3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t**3 * p3[1],
        ))
    return out


def _flatten_quad(p0, c, p1, n=200):
    out = []
    for i in range(1, n + 1):
        t = i / n
        mt = 1 - t
        out.append((
            mt * mt * p0[0] + 2 * mt * t * c[0] + t * t * p1[0],
            mt * mt * p0[1] + 2 * mt * t * c[1] + t * t * p1[1],
        ))
    return out


def ufo_polys(contours):
    """Flatten UFO contours (from grid_qa.parse_glyph) to closed polylines."""
    polys = []
    for c in contours:
        n = len(c)
        on = [i for i, p in enumerate(c) if p["on"]]
        if len(on) < 2:
            continue
        poly = [(c[on[0]]["x"], c[on[0]]["y"])]
        for k in range(len(on)):
            a, b = on[k], on[(k + 1) % len(on)]
            offs = []
            i = (a + 1) % n
            while i != b:
                offs.append(i)
                i = (i + 1) % n
            pa = (c[a]["x"], c[a]["y"])
            pb = (c[b]["x"], c[b]["y"])
            if len(offs) == 0:
                poly.append(pb)
            elif len(offs) == 1:
                cc = (c[offs[0]]["x"], c[offs[0]]["y"])
                poly.extend(_flatten_quad(pa, cc, pb))
            elif len(offs) == 2:
                c1 = (c[offs[0]]["x"], c[offs[0]]["y"])
                c2 = (c[offs[1]]["x"], c[offs[1]]["y"])
                poly.extend(_flatten_cubic(pa, c1, c2, pb))
        polys.append(poly)
    return polys


def ttf_polys(rec):
    """Flatten a RecordingPen value to closed polylines."""
    polys = []
    cur = []
    for cmd, args in rec:
        if cmd == "moveTo":
            cur = [args[0]]
        elif cmd == "lineTo":
            cur.append(args[0])
        elif cmd == "qCurveTo":
            pts = list(args)
            p0 = cur[-1]
            if pts[-1] is None:
                pts[-1] = cur[0]
            on = pts[-1]
            offs = pts[:-1]
            impl = [((offs[i][0] + offs[i + 1][0]) / 2, (offs[i][1] + offs[i + 1][1]) / 2)
                    for i in range(len(offs) - 1)]
            ons = impl + [on]
            prev = p0
            for i, c in enumerate(offs):
                cur.extend(_flatten_quad(prev, c, ons[i]))
                prev = ons[i]
        elif cmd == "curveTo":
            p0 = cur[-1]
            c1, c2, p1 = args
            cur.extend(_flatten_cubic(p0, c1, c2, p1))
        elif cmd == "closePath":
            if cur:
                polys.append(cur)
            cur = []
    if cur:
        polys.append(cur)
    return polys


# ---------------------------------------------------------------- scanning
def hcross(polys, y):
    xs = []
    for pl in polys:
        for (x0, y0), (x1, y1) in zip(pl, pl[1:] + pl[:1]):
            if (y0 - y) * (y1 - y) < 0 and y0 != y1:
                xs.append(x0 + (y - y0) / (y1 - y0) * (x1 - x0))
    return sorted(xs)


def vcross(polys, x):
    ys = []
    for pl in polys:
        for (x0, y0), (x1, y1) in zip(pl, pl[1:] + pl[:1]):
            if (x0 - x) * (x1 - x) < 0 and x0 != x1:
                ys.append(y0 + (x - x0) / (x1 - x0) * (y1 - y0))
    return sorted(ys)


def dedup(vs, tol=3.0):
    out = []
    for v in vs:
        if not out or v - out[-1] > tol:
            out.append(v)
    return out


def robust(cross, polys, coord, want):
    """Scan at `coord`, nudging off it by up to +/-12 units if the line grazes
    an extremum (a vertex sitting exactly on the line yields no crossing). A
    stroke's thickness is near-constant next to its extremum, so a few units'
    offset gives the true value while dodging the tangency."""
    best = dedup(cross(polys, coord))
    if len(best) >= want:
        return best
    for off in (2, -2, 4, -4, 6, -6, 8, -8, 12, -12):
        c = dedup(cross(polys, coord + off))
        if len(c) >= want:
            return c
        if len(c) > len(best):
            best = c
    return best


def bbox(polys):
    xs = [p[0] for pl in polys for p in pl]
    ys = [p[1] for pl in polys for p in pl]
    return min(xs), max(xs), min(ys), max(ys)


def measure(polys, advance, kind, scan_h):
    """Return the metric dict for one glyph from its polylines."""
    xmin, xmax, ymin, ymax = bbox(polys)
    xs = robust(hcross, polys, scan_h, 4)
    m = dict(width=xmax - xmin, height=ymax - ymin, sbL=xmin, sbR=advance - xmax)
    if len(xs) >= 4:
        # stem/side = first stroke; counter = the gap to the next stroke.
        m["weight"] = xs[1] - xs[0]
        m["counter"] = xs[2] - xs[1]
    else:
        m["weight"] = m["counter"] = float("nan")
    if kind == "round":
        ys = robust(vcross, polys, (xmin + xmax) / 2, 4)
        m["crown"] = (ys[-1] - ys[-2]) if len(ys) >= 4 else float("nan")
    return m


# ---------------------------------------------------------------- sources
def measure_ufo(master, glyphs):
    root = f"sources/VirtuaGrotesk-{master}.ufo"
    fi = plistlib.load(open(f"{root}/fontinfo.plist", "rb"))
    xh, cap = fi["xHeight"], fi["capHeight"]
    out = {"_xheight": xh, "_capheight": cap}
    gdir = f"{root}/glyphs"
    # UFO glyph filenames uppercase-suffix caps: H -> H_.glif, O -> O_.glif.
    names = {g: (f"{g}_.glif" if g.isupper() else f"{g}.glif") for g in glyphs}
    for g in glyphs:
        case, kind, hfrac = GLYPH_SPEC[g]
        adv, cont = gq.parse_glyph(f"{gdir}/{names[g]}")
        polys = ufo_polys(cont)
        ref = cap if case == "cap" else xh
        out[g] = measure(polys, adv, kind, hfrac * ref)
    return out


def measure_ttf(path, glyphs):
    f = TTFont(path)
    if "fvar" in f:
        instantiateVariableFont(f, {"wght": 400}, inplace=True)
    os2 = f["OS/2"]
    xh = os2.sxHeight
    cap = getattr(os2, "sCapHeight", 0) or 0
    gs = f.getGlyphSet()
    hm = f["hmtx"]
    cmap = f.getBestCmap()
    if not cap:  # fall back to the top of 'H'
        rec = RecordingPen()
        gs[cmap[ord("H")]].draw(rec)
        cap = bbox(ttf_polys(rec.value))[3]
    out = {"_xheight": xh, "_capheight": cap}
    for g in glyphs:
        case, kind, hfrac = GLYPH_SPEC[g]
        gn = cmap[ord(g)]
        rec = RecordingPen()
        gs[gn].draw(rec)
        polys = ttf_polys(rec.value)
        ref = cap if case == "cap" else xh
        out[g] = measure(polys, hm[gn][0], kind, hfrac * ref)
    return out


# ---------------------------------------------------------------- reporting
def sb(m):
    return (m["sbL"] + m["sbR"]) / 2


def build_rows(glyphs):
    """(section, label, fn) ratio rows — only those whose glyphs were measured."""
    has = set(glyphs)
    rows = []

    def add(section, label, need, fn):
        if need <= has:
            rows.append((section, label, fn))

    # Weight: how heavy caps are vs lowercase, and each case's own contrast.
    add("WEIGHT", "H stem / n stem  (cap vs lc upright)", {"H", "n"},
        lambda d: d["H"]["weight"] / d["n"]["weight"])
    add("WEIGHT", "O side / o side  (cap vs lc round)", {"O", "o"},
        lambda d: d["O"]["weight"] / d["o"]["weight"])
    add("WEIGHT", "O side / H stem  (cap contrast)", {"O", "H"},
        lambda d: d["O"]["weight"] / d["H"]["weight"])
    add("WEIGHT", "o side / n stem  (lc contrast)", {"o", "n"},
        lambda d: d["o"]["weight"] / d["n"]["weight"])
    add("WEIGHT", "O crown / O side  (round overshoot)", {"O"},
        lambda d: d["O"]["crown"] / d["O"]["weight"])
    add("WEIGHT", "o crown / o side  (round overshoot)", {"o"},
        lambda d: d["o"]["crown"] / d["o"]["weight"])

    # Spacing: cap vs lowercase sidebearings, and openness within each case.
    add("SPACING", "H sb / n sb  (cap vs lc spacing)", {"H", "n"},
        lambda d: sb(d["H"]) / sb(d["n"]))
    add("SPACING", "O sb / o sb  (cap vs lc spacing)", {"O", "o"},
        lambda d: sb(d["O"]) / sb(d["o"]))
    add("SPACING", "H sb / H counter", {"H"}, lambda d: sb(d["H"]) / d["H"]["counter"])
    add("SPACING", "n sb / n counter", {"n"}, lambda d: sb(d["n"]) / d["n"]["counter"])
    add("SPACING", "O sb / O side", {"O"}, lambda d: sb(d["O"]) / d["O"]["weight"])
    add("SPACING", "o sb / o side", {"o"}, lambda d: sb(d["o"]) / d["o"]["weight"])

    # Proportion: relative heights and widths.
    add("PROPORTION", "cap height / x-height", set(),
        lambda d: d["_capheight"] / d["_xheight"])
    add("PROPORTION", "O width / o width", {"O", "o"},
        lambda d: d["O"]["width"] / d["o"]["width"])
    add("PROPORTION", "H width / n width", {"H", "n"},
        lambda d: d["H"]["width"] / d["n"]["width"])
    add("PROPORTION", "O counter / o counter", {"O", "o"},
        lambda d: d["O"]["counter"] / d["o"]["counter"])
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glyphs", nargs="+", default=["H", "O", "n", "o"],
                    help="glyphs to measure (must be in GLYPH_SPEC)")
    ap.add_argument("--master", default="Regular", help="UFO master (Regular, Bold, ...)")
    ap.add_argument("--refs", nargs="+", default=list(REF_FONTS),
                    help="reference fonts: " + ", ".join(REF_FONTS))
    args = ap.parse_args()

    unknown = [g for g in args.glyphs if g not in GLYPH_SPEC]
    if unknown:
        ap.error(f"no scan spec for {unknown}; add them to GLYPH_SPEC")

    data = {"Virtua": measure_ufo(args.master, args.glyphs)}
    for r in args.refs:
        if r not in REF_FONTS:
            print(f"[skip unknown ref '{r}']", file=sys.stderr)
            continue
        try:
            data[r.capitalize()] = measure_ttf(REF_FONTS[r], args.glyphs)
        except Exception as e:  # noqa: BLE001
            print(f"[{r} failed: {e}]", file=sys.stderr)

    cols = list(data)
    rows = build_rows(args.glyphs)
    w = 40
    print(f"\nVirtua {args.master}  vs  {', '.join(cols[1:])}   glyphs: {' '.join(args.glyphs)}")
    print(f"{'RATIO':{w}}" + "".join(f"{c:>9}" for c in cols))
    print("-" * (w + 9 * len(cols)))
    section = None
    for sec, label, fn in rows:
        if sec != section:
            print(f"[{sec}]")
            section = sec
        cells = ""
        for c in cols:
            try:
                cells += f"{fn(data[c]):9.2f}"
            except Exception:  # noqa: BLE001
                cells += f"{'--':>9}"
        print(f"  {label:{w - 2}}" + cells)

    print("\nRAW (font units; sizes not comparable across fonts, ratios are):")
    for c in cols:
        d = data[c]
        print(f"  {c}  cap/xh {d['_capheight']:.0f}/{d['_xheight']:.0f}")
        for g in args.glyphs:
            m = d[g]
            extra = f"  crown {m['crown']:.0f}" if "crown" in m else ""
            print(f"     {g}: weight {m['weight']:.0f}  counter {m['counter']:.0f}  "
                  f"width {m['width']:.0f}  sb {sb(m):.0f} (L{m['sbL']:.0f}/R{m['sbR']:.0f}){extra}")


if __name__ == "__main__":
    main()
