"""Grid-system QA: per-glyph conformance to the blog-post design system.

Fontspector-style terminal report over the UFO sources. For every glyph
it checks the two-lattice contract and the powers-of-two aesthetic:

  GRID      every point on the 2-grid (the law); on-curve points on the
            8-grid, or off by EXACTLY 4 (the self-labeling optical class)
  ADVANCE   advance width and ink sidebearings on the 8-grid
  HANDLES   every off-curve handle axis-aligned to its on-curve neighbor
            (H/V), with a length that is a SHORT SUM of powers of two
  SPANS     structural proportions: gaps between adjacent on-curve
            x-columns / y-rows score as short power-of-two sums
            (n: 64 SB + 96 stem + 272 counter -> popcounts 1,2,2)

"Short sum of powers of two" is measured as binary popcount:
  1 = a pure power (64, 128, 256)        PERFECT
  2 = elegant sum (96=64+32, 272=256+16) GOOD
  3 = acceptable (104=64+32+8)           OK
  4+ = review (154, 158, ...)            FLAG

Usage (from the repo root):
    make grid-qa                       # A-Z a-z 0-9 summary, both masters
    ./.venv/bin/python scripts/grid_qa.py --all
    ./.venv/bin/python scripts/grid_qa.py -v n o H O      # full detail
    ./.venv/bin/python scripts/grid_qa.py --master Bold --worst 15
Exit code 1 if any checked glyph has a hard failure (off-2 point,
off-8-not-4 on-curve, off-8 advance, diagonal handle).
"""

import argparse
import os
import plistlib
import re
import sys

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"
BOLD = "\033[1m"
END = "\033[0m"

LATIN = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine"]
DEFAULT_SET = LATIN + DIGITS


def popcount(v):
    return bin(int(abs(v))).count("1") if v else 0


def nice(v):
    """Classify a dimension as a short sum of powers of two."""
    p = popcount(v)
    if p <= 1:
        return p, "power"
    if p == 2:
        return p, "elegant"
    if p == 3:
        return p, "ok"
    return p, "REVIEW"


def parse_glyph(path):
    src = open(path).read()
    adv = float(re.search(r'width="([\d.]+)"', src).group(1))
    contours = []
    for cm in re.finditer(r"<contour>(.*?)</contour>", src, re.S):
        pts = []
        for m in re.finditer(
            r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
            r"((?: type=\"(\w+)\")?( smooth=\"yes\")?)/>",
            cm.group(1),
        ):
            pts.append(
                dict(x=float(m.group(1)), y=float(m.group(2)),
                     on=bool(m.group(4)), smooth=bool(m.group(5)))
            )
        contours.append(pts)
    return adv, contours


def qa_glyph(adv, contours):
    """Returns dict of findings."""
    r = dict(off2=[], off8bad=[], opt4=0, handles_diag=[], handles=[],
             spans_x=[], spans_y=[], adv_ok=adv % 8 == 0, adv=adv,
             sb=None, n_pts=0)
    xs_on, ys_on = set(), set()
    all_x = []
    for cont in contours:
        n = len(cont)
        for i, p in enumerate(cont):
            r["n_pts"] += 1
            all_x.append(p["x"])
            if p["x"] % 2 or p["y"] % 2:
                r["off2"].append((p["x"], p["y"]))
            if p["on"]:
                mx, my = p["x"] % 8, p["y"] % 8
                if mx not in (0, 4) or my not in (0, 4):
                    r["off8bad"].append((p["x"], p["y"]))
                elif mx == 4 or my == 4:
                    r["opt4"] += 1
                xs_on.add(p["x"])
                ys_on.add(p["y"])
            else:
                # handle: vector from nearest on-curve neighbor. The H/V
                # convention binds SMOOTH points (extrema); handles into
                # corner points (seams, joints) may be diagonal by design.
                for j in (i - 1, i + 1):
                    q = cont[j % n]
                    if q["on"]:
                        dx, dy = p["x"] - q["x"], p["y"] - q["y"]
                        if abs(dx) > 0.01 and abs(dy) > 0.01:
                            if q["smooth"]:
                                r["handles_diag"].append(
                                    (q["x"], q["y"], round(dx), round(dy)))
                        else:
                            length = abs(dx) if abs(dx) > 0.01 else abs(dy)
                            if length > 0.01:
                                r["handles"].append(int(round(length)))
                        break
    if all_x:
        r["sb"] = (min(all_x), adv - max(all_x))
    for vals, key in ((sorted(xs_on), "spans_x"), (sorted(ys_on), "spans_y")):
        for a, b in zip(vals, vals[1:]):
            d = int(round(b - a))
            if d >= 24:  # chamfers/seam micro-gaps are not proportions
                r[key].append(d)
    return r


def glyph_grade(r):
    """(grade, colored_grade). Hard rules + handle niceness grade the
    glyph; spans are informational (they include composite distances).
    Optical off-8-by-4 on-curves are a FEATURE and never penalized."""
    if r["off2"] or r["off8bad"] or not r["adv_ok"] or r["handles_diag"]:
        return "FAIL", f"{RED}FAIL{END}"
    hp = [popcount(h) for h in r["handles"]]
    worst = max(hp + [0])
    if worst <= 2:
        return "PERFECT", f"{GREEN}PERFECT{END}"
    if worst <= 3:
        return "GOOD", f"{GREEN}GOOD{END}"
    return "OK", f"{YELLOW}OK{END}"


def fmt_hist(values):
    from collections import Counter
    c = Counter(popcount(v) for v in values)
    parts = []
    for p in sorted(c):
        color = GREEN if p <= 2 else (YELLOW if p == 3 else RED)
        parts.append(f"{color}p{p}×{c[p]}{END}")
    return " ".join(parts) if parts else f"{DIM}-{END}"


def detail(name, master, r):
    print(f"\n{BOLD}{master} {name}{END}  adv {r['adv']:g}"
          f"{'' if r['adv_ok'] else RED + ' OFF-8' + END}"
          f"  sb {r['sb'][0]:g}/{r['sb'][1]:g}" if r["sb"] else "")
    if r["off2"]:
        print(f"  {RED}off-2 points:{END} {r['off2']}")
    if r["off8bad"]:
        print(f"  {RED}on-curve off-8-not-4:{END} {r['off8bad']}")
    if r["opt4"]:
        print(f"  {DIM}optical (off-8-by-4) on-curves: {r['opt4']}{END}")
    if r["handles_diag"]:
        print(f"  {RED}diagonal handles:{END}")
        for x, y, dx, dy in r["handles_diag"]:
            print(f"    at ({x:g},{y:g}) vector ({dx:+},{dy:+})")
    if r["handles"]:
        lens = sorted(set(r["handles"]))
        pretty = ", ".join(
            f"{(GREEN if popcount(v) <= 2 else (YELLOW if popcount(v) == 3 else RED))}{v}{END}"
            for v in lens)
        print(f"  handle lengths: {pretty}")
    for key, label in (("spans_x", "x-spans"), ("spans_y", "y-spans")):
        vals = sorted(set(r[key]))
        if vals:
            pretty = ", ".join(
                f"{(GREEN if popcount(v) <= 2 else (YELLOW if popcount(v) == 3 else RED))}{v}{END}"
                for v in vals)
            print(f"  {label}: {pretty}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glyphs", nargs="*", help="glyph names (default: A-Z a-z 0-9)")
    ap.add_argument("--master", choices=["Regular", "Bold"], default=None)
    ap.add_argument("--all", action="store_true", help="every glyph in the UFO")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="full detail per glyph")
    ap.add_argument("--worst", type=int, default=0,
                    help="show detail for the N worst glyphs")
    args = ap.parse_args()

    masters = [args.master] if args.master else ["Regular", "Bold"]
    fails = 0
    rows = []

    for master in masters:
        gdir = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
        contents = plistlib.load(open(f"{gdir}/contents.plist", "rb"))
        if args.glyphs:
            names = args.glyphs
        elif args.all:
            names = sorted(contents)
        else:
            names = DEFAULT_SET
        for name in names:
            fn = contents.get(name)
            if fn is None:
                continue
            path = os.path.join(gdir, fn)
            adv, contours = parse_glyph(path)
            if not contours or not any(c for c in contours):
                continue
            r = qa_glyph(adv, contours)
            grade, colored = glyph_grade(r)
            if grade == "FAIL":
                fails += 1
            badness = (len(r["off2"]) * 100 + len(r["off8bad"]) * 50
                       + len(r["handles_diag"]) * 30
                       + (0 if r["adv_ok"] else 40)
                       + sum(max(0, popcount(v) - 2)
                             for v in r["handles"] + r["spans_x"] + r["spans_y"]))
            rows.append((badness, master, name, r, grade, colored))
            if args.verbose:
                detail(name, master, r)

    if not args.verbose:
        rows.sort(key=lambda t: -t[0])
        print(f"{BOLD}{'glyph':>10} {'master':>8} {'grade':>16} "
              f"{'handles':>18} {'spans':>22}{END}")
        for badness, master, name, r, grade, colored in rows:
            print(f"{name:>10} {master:>8} {colored:>25} "
                  f"{fmt_hist(r['handles']):>28} "
                  f"{fmt_hist(r['spans_x'] + r['spans_y']):>34}")
        if args.worst:
            for badness, master, name, r, grade, colored in rows[: args.worst]:
                detail(name, master, r)

    total = len(rows)
    perfect = sum(1 for row in rows if row[4] == "PERFECT")
    good = sum(1 for row in rows if row[4] in ("PERFECT", "GOOD"))
    print(f"\n{BOLD}{total} glyph-masters checked: "
          f"{GREEN}{perfect} PERFECT{END}{BOLD}, {good} at GOOD or better, "
          f"{RED if fails else GREEN}{fails} FAIL{END}")
    print(f"{DIM}popcount legend: p1 pure power of two · p2 elegant sum "
          f"(96=64+32) · p3 ok (104) · p4+ review{END}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
