"""Grid-system QA: per-glyph conformance to the blog-post design system.

Fontspector-style terminal report over the UFO sources. For every glyph
it checks the two-lattice contract and the powers-of-two aesthetic:

  GRID      every point on the 2-grid (the law); on-curve points on the
            8-grid, or consciously off it on the 2-grid (the
            self-labeling optical class: off-8 by 2, 4, or 6)
  ADVANCE   advance width and ink sidebearings on the 8-grid
  HANDLES   every off-curve handle axis-aligned to its on-curve neighbor
            (H/V), with a length that is a SHORT SUM of powers of two
  SPANS     structural proportions: gaps between adjacent on-curve
            x-columns / y-rows score as short power-of-two sums
            (n: 64 SB + 96 stem + 272 counter -> popcounts 1,2,2)

"Short sum of powers of two" is measured as binary popcount, with an
adjacency tiebreak inside each popcount class: set bits that form one
contiguous run (96 = 64+32, n + n/2) are cleaner than spread bits
(80 = 64+16, n + n/4), so ties rank by gap. Grades stay popcount-based
(272 = 256+16 is still GOOD):
  1 = a pure power (64, 128, 256)        PERFECT
  2 = elegant sum (96=64+32, 272=256+16) GOOD
  3 = acceptable (104=64+32+8)           OK
  4+ = review (154, 158, ...)            FLAG

Usage (from the repo root):
    make grid-qa                       # A-Z a-z 0-9 summary, both masters
    ./.venv/bin/python scripts/grid_qa.py --all
    ./.venv/bin/python scripts/grid_qa.py -v n o H O      # full detail
    ./.venv/bin/python scripts/grid_qa.py --master Bold --worst 15
    ./.venv/bin/python scripts/grid_qa.py --focus a       # one-glyph dashboard
    ./.venv/bin/python scripts/grid_qa.py -f U+0071 --watch
    make dash G=a                      # dashboard + auto-refresh on save
Focus mode (--focus/-f) takes a glyph name, a literal character, or a
codepoint (U+0071 / uni0071 / 0071) and prints a full design dashboard
for that one glyph across both masters. With --watch it stays open and
re-renders whenever the .glif files change (i.e. on every editor save),
showing a delta line of what improved or regressed since the last save.
Exit code 1 if any checked glyph has a hard failure (off-2 point,
off-8-not-4 on-curve, off-8 advance, diagonal handle).
"""

import argparse
import os
import plistlib
import re
import sys
import time

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


def adjacent(v):
    """True if the set bits form one contiguous run: the sum descends by
    halves (96 = 64+32) rather than skipping (80 = 64+16)."""
    v = int(abs(v))
    if v == 0:
        return True
    v >>= (v & -v).bit_length() - 1
    return v & (v + 1) == 0


def tidiness(v):
    """Sort key for least-tidy values: popcount first, spread bits rank
    half a grade worse inside the same popcount class."""
    return popcount(v) + (0.0 if adjacent(v) else 0.5)


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
    m = re.search(r'<advance[^>]*width="([\d.]+)"', src)
    adv = float(m.group(1)) if m else 0.0  # some glyphs have no advance
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
    r = dict(off2=[], opt4=0, handles_diag=[], handles=[],
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
                # off the 8-grid but on the 2-grid = the optical class;
                # odd coordinates are already hard failures via off2.
                mx, my = p["x"] % 8, p["y"] % 8
                if (mx or my) and mx % 2 == 0 and my % 2 == 0:
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
    if r["off2"] or not r["adv_ok"] or r["handles_diag"]:
        return "FAIL", f"{RED}FAIL{END}"
    hp = [popcount(h) for h in r["handles"]]
    worst = max(hp + [0])
    if worst <= 2:
        return "PERFECT", f"{GREEN}PERFECT{END}"
    if worst <= 3:
        return "GOOD", f"{GREEN}GOOD{END}"
    return "OK", f"{YELLOW}OK{END}"


def fmt_nice(values):
    """'nice/total (worst 158)' — nice = short sum (popcount <= 2)."""
    if not values:
        return "-", DIM
    nice_n = sum(1 for v in values if popcount(v) <= 2)
    total = len(values)
    if nice_n == total:
        return f"{nice_n}/{total}", GREEN
    worst = max(values, key=tidiness)
    frac = nice_n / total
    color = GREEN if frac >= 0.8 else (YELLOW if frac >= 0.5 else RED)
    return f"{nice_n}/{total} (worst {worst})", color


def fail_reason(r):
    parts = []
    if r["off2"]:
        parts.append(f"{len(r['off2'])} pts off the 2-grid")
    if not r["adv_ok"]:
        parts.append(f"advance {r['adv']:g} off-8")
    if r["handles_diag"]:
        parts.append(f"{len(r['handles_diag'])} diagonal handles")
    return "; ".join(parts)


def detail(name, master, r):
    print(f"\n{BOLD}{master} {name}{END}  adv {r['adv']:g}"
          f"{'' if r['adv_ok'] else RED + ' OFF-8' + END}"
          f"  sb {r['sb'][0]:g}/{r['sb'][1]:g}" if r["sb"] else "")
    if r["off2"]:
        print(f"  {RED}off-2 points:{END} {r['off2']}")
    if r["opt4"]:
        print(f"  {DIM}optical (on-2, off-8) on-curves: {r['opt4']}{END}")
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


# ------------------------------------------------------------------ focus
# One-glyph design dashboard (--focus/-f), optionally live (--watch).

ZONES_Y = (("baseline", 0), ("x-height", 576), ("cap", 768),
           ("ascender", 832), ("descender", -256))
MARK_NAMES = {"0.09,0.72,0.44,1": "green/done",
              "1,0.5,0,1": "orange/polish",
              "1,0,0,1": "red/broken",
              "0.27,0.44,1,1": "blue/AI-ungraded"}
NICE2 = [v for v in range(8, 1026, 2) if popcount(v) <= 2]


def parse_full(path):
    src = open(path).read()
    adv = float(re.search(r'width="([\d.]+)"', src).group(1))
    uni = re.search(r'unicode hex="([0-9A-Fa-f]+)"', src)
    mark = re.search(r"public\.markColor</key>\s*<string>([^<]+)</string>", src)
    contours = []
    for cm in re.finditer(r"<contour>(.*?)</contour>", src, re.S):
        pts = []
        for m in re.finditer(
            r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
            r"((?: type=\"(\w+)\")?( smooth=\"yes\")?)/>",
            cm.group(1),
        ):
            pts.append(dict(x=float(m.group(1)), y=float(m.group(2)),
                            on=bool(m.group(4)), smooth=bool(m.group(5))))
        contours.append(pts)
    return dict(adv=adv, uni=uni.group(1).upper() if uni else None,
                mark=mark.group(1).strip() if mark else None,
                contours=contours)


def resolve_focus(query):
    """Glyph name, literal character, or codepoint (U+0071/uni0071/0071)."""
    gdir = "sources/VirtuaGrotesk-Regular.ufo/glyphs"
    contents = plistlib.load(open(f"{gdir}/contents.plist", "rb"))
    if query in contents:
        return query
    cp = None
    m = re.fullmatch(r"(?:U\+|u\+|uni|0x)?([0-9A-Fa-f]{4,6})", query)
    if len(query) == 1:
        cp = ord(query)
    elif m:
        cp = int(m.group(1), 16)
    if cp is not None:
        for name, fn in contents.items():
            um = re.search(r'unicode hex="([0-9A-Fa-f]+)"',
                           open(os.path.join(gdir, fn)).read())
            if um and int(um.group(1), 16) == cp:
                return name
    sys.exit(f"grid-qa: cannot resolve {query!r} to a glyph")


def handle_desc(p, q):
    """(axis, length) of handle p against on-curve q: 'H'/'V'/'diag'."""
    dx, dy = p["x"] - q["x"], p["y"] - q["y"]
    if abs(dx) > 0.01 and abs(dy) > 0.01:
        return "diag", (dx * dx + dy * dy) ** 0.5
    if abs(dx) > 0.01:
        return "H", abs(dx)
    if abs(dy) > 0.01:
        return "V", abs(dy)
    return "0", 0.0


def segment_pairs(contours):
    """[(h1desc, h2desc)] for every cubic segment, in contour order."""
    pairs = []
    for cont in contours:
        n = len(cont)
        for i in range(n):
            p0, p1, p2, p3 = (cont[i], cont[(i + 1) % n],
                              cont[(i + 2) % n], cont[(i + 3) % n])
            if p0["on"] and not p1["on"] and not p2["on"] and p3["on"]:
                pairs.append((handle_desc(p1, p0), handle_desc(p2, p3)))
    return pairs


def chamfers(contours):
    """45-degree line segments (both ends on-curve) up to 48u."""
    out = []
    for cont in contours:
        n = len(cont)
        for i in range(n):
            a, b = cont[i], cont[(i + 1) % n]
            if a["on"] and b["on"]:
                dx, dy = abs(b["x"] - a["x"]), abs(b["y"] - a["y"])
                if dx == dy and 0 < dx <= 48:
                    out.append((int(dx), a, b))
    return out


def suggest_nice(L):
    c = min(NICE2, key=lambda v: abs(v - L))
    return c if c != L and abs(c - L) <= max(6, 0.07 * L) else None


def zone_note(y):
    zname, zy = min(ZONES_Y, key=lambda z: abs(y - z[1]))
    d = y - zy
    if abs(d) <= 32:
        return zname if d == 0 else f"{zname}{d:+g}"
    return f"{y:g}"


def color_len(v):
    p = popcount(int(round(v)))
    col = GREEN if p <= 2 else (YELLOW if p == 3 else RED)
    return f"{col}{int(round(v))}{END}"


def dash_collect(master, name):
    gdir = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
    contents = plistlib.load(open(f"{gdir}/contents.plist", "rb"))
    fn = contents.get(name)
    if fn is None:
        return None
    path = os.path.join(gdir, fn)
    g = parse_full(path)
    r = qa_glyph(g["adv"], g["contours"])
    grade, colored = glyph_grade(r)
    import curve_lint
    d = dict(g=g, r=r, grade=grade, colored=colored, path=path,
             lint=curve_lint.lint_glyph(path, name),
             pairs=segment_pairs(g["contours"]),
             chamfers=chamfers(g["contours"]))
    on = [p for c in g["contours"] for p in c if p["on"]]
    d["n_on"] = len(on)
    d["n_pts"] = sum(len(c) for c in g["contours"])
    d["structure"] = tuple(
        tuple("1" if p["on"] else "0" for p in c) for c in g["contours"])
    if on:
        d["xmin"] = min(p["x"] for p in on)
        d["xmax"] = max(p["x"] for p in on)
        d["ymin"] = min(p["y"] for p in on)
        d["ymax"] = max(p["y"] for p in on)
    d["opt4"] = [(p["x"], p["y"]) for c in g["contours"] for p in c
                 if p["on"] and (p["x"] % 8, p["y"] % 8) != (0, 0)
                 and p["x"] % 2 == 0 and p["y"] % 2 == 0]
    return d


def dash_think(data):
    """The 'things to think about' list, worst first."""
    items = []
    for master in ("Regular", "Bold"):
        d = data.get(master)
        if d is None:
            items.append(f"{RED}{master}: glyph missing{END}")
            continue
        r = d["r"]
        if r["off2"]:
            items.append(f"{RED}{master}: {len(r['off2'])} points off the "
                         f"2-grid: {r['off2'][:6]}{END}")
        if not r["adv_ok"]:
            items.append(f"{RED}{master}: advance {r['adv']:g} not on the "
                         f"8-grid{END}")
        for x, y, dx, dy in r["handles_diag"]:
            items.append(f"{RED}{master}: diagonal handle at smooth "
                         f"({x:g},{y:g}) vector ({dx:+},{dy:+}){END}")
        bad = sorted(set(int(v) for v in r["handles"] if popcount(v) > 2),
                     key=popcount, reverse=True)
        if bad:
            sug = ", ".join(
                f"{v}→{suggest_nice(v)}?" if suggest_nice(v) else f"{v}"
                for v in bad[:8])
            items.append(f"{YELLOW}{master}: handle lengths not nice: "
                         f"{sug}{END}")
        for (a1, L1), (a2, L2) in d["pairs"]:
            if a1 in "HV" and a2 in "HV" and min(L1, L2) > 0:
                if max(L1, L2) / min(L1, L2) > 2.2:
                    items.append(
                        f"{YELLOW}{master}: uneven pair {a1}{L1:g}/{a2}{L2:g}"
                        f" ({max(L1,L2)/min(L1,L2):.1f}:1){END}")
        for size, a, b in d["chamfers"]:
            if size != 16:
                items.append(f"{YELLOW}{master}: {size}u chamfer at "
                             f"({a['x']:g},{a['y']:g})–({b['x']:g},"
                             f"{b['y']:g}) — contract is 16{END}")
        for issue in d["lint"]:
            items.append(f"{YELLOW}{master} lint: {issue}{END}")
    dr, db = data.get("Regular"), data.get("Bold")
    if dr and db and dr["structure"] != db["structure"]:
        items.insert(0, f"{RED}masters structurally INCOMPATIBLE — "
                     f"variable build will fail{END}")
    return items


def dash_render(name, prev):
    data = {m: dash_collect(m, name) for m in ("Regular", "Bold")}
    d0 = data["Regular"] or data["Bold"]
    uni = d0["g"]["uni"]
    char = chr(int(uni, 16)) if uni else "?"
    stamp = time.strftime("%H:%M:%S")
    W = 78
    head = f" {name} · U+{uni or '????'} · “{char}” "
    print(f"{BOLD}──{head}{END}" + DIM
          + "─" * max(0, W - len(head) - 12) + f" {stamp} " + END)

    # summary table
    print(f"\n  {BOLD}{'master':<9}{'grade':<9}{'mark':<18}{'advance':<9}"
          f"{'sb':<11}{'bounds (on-curve)':<24}{END}")
    for master in ("Regular", "Bold"):
        d = data[master]
        if d is None:
            print(f"  {master:<9}{RED}missing{END}")
            continue
        r = d["r"]
        mark = MARK_NAMES.get(d["g"]["mark"], d["g"]["mark"] or "-")
        sb = f"{r['sb'][0]:g}/{r['sb'][1]:g}" if r["sb"] else "-"
        bounds = (f"{d['xmin']:g}..{d['xmax']:g}  "
                  f"{zone_note(d['ymin'])}..{zone_note(d['ymax'])}")
        gcol = {"FAIL": RED, "OK": YELLOW}.get(d["grade"], GREEN)
        print(f"  {master:<9}{gcol}{d['grade']:<9}{END}{mark:<18}"
              f"{r['adv']:<9g}{sb:<11}{bounds:<24}")
    dr, db = data["Regular"], data["Bold"]
    if dr and db:
        comp = (f"{GREEN}✓ compatible{END}"
                if dr["structure"] == db["structure"]
                else f"{RED}✗ INCOMPATIBLE{END}")
        print(f"  {DIM}masters: {dr['n_pts']}/{db['n_pts']} pts · "
              f"structure {END}{comp}")

    # handle pairs
    print(f"\n  {BOLD}HANDLE PAIRS{END} {DIM}(per cubic segment: "
          f"axis+length, colored by tidiness){END}")
    for master in ("Regular", "Bold"):
        d = data[master]
        if d is None or not d["pairs"]:
            continue
        cells = []
        for (a1, L1), (a2, L2) in d["pairs"]:
            c1 = color_len(L1) if a1 in "HV" else f"{DIM}{a1}{END}"
            c2 = color_len(L2) if a2 in "HV" else f"{DIM}{a2}{END}"
            t1 = a1 if a1 in "HV" else ""
            t2 = a2 if a2 in "HV" else ""
            cells.append(f"{t1}{c1}/{t2}{c2}")
        print(f"  {master:<9}" + "  ".join(cells))

    # spans
    print(f"\n  {BOLD}SPANS{END} {DIM}(stems, counters, "
          f"sidebearing-to-stem){END}")
    for master in ("Regular", "Bold"):
        d = data[master]
        if d is None:
            continue
        r = d["r"]
        xs = " ".join(color_len(v) for v in sorted(set(r["spans_x"])))
        ys = " ".join(color_len(v) for v in sorted(set(r["spans_y"])))
        print(f"  {master:<9}x: {xs}   {DIM}|{END}   y: {ys}")

    # optical corrections
    any_opt = any(d and d["opt4"] for d in data.values())
    if any_opt:
        print(f"\n  {BOLD}OPTICAL{END} {DIM}(on 2-grid off 8 — "
              f"deliberate corrections; confirm each){END}")
        for master in ("Regular", "Bold"):
            d = data[master]
            if d is None or not d["opt4"]:
                continue
            pts = " ".join(f"({x:g},{y:g})" for x, y in d["opt4"][:10])
            more = f" +{len(d['opt4'])-10}" if len(d["opt4"]) > 10 else ""
            print(f"  {master:<9}{DIM}{pts}{more}{END}")

    # think-about list
    items = dash_think(data)
    print(f"\n  {BOLD}THINK ABOUT{END}")
    if items:
        for it in items:
            print(f"  • {it}")
    else:
        print(f"  {GREEN}✓ nothing flagged — both masters clean"
              f"{END}")

    # delta vs previous render
    snap = {}
    for master in ("Regular", "Bold"):
        d = data[master]
        if d:
            snap[master] = (d["grade"], len(d["r"]["off2"]),
                            len(d["r"]["handles_diag"]),
                            sum(1 for v in d["r"]["handles"]
                                if popcount(v) > 2), len(d["lint"]))
    if prev and prev != snap:
        parts = []
        labels = ("grade", "off-grid", "diag-handles", "untidy-handles",
                  "lint")
        for master, cur in snap.items():
            old = prev.get(master)
            if old and old != cur:
                for lab, a, b in zip(labels, old, cur):
                    if a != b:
                        parts.append(f"{master} {lab} {a}→{b}")
        if parts:
            print(f"\n  {BOLD}Δ since last save:{END} "
                  + " · ".join(parts))
    return snap


def focus_main(args):
    name = resolve_focus(args.focus)
    paths = []
    for master in ("Regular", "Bold"):
        gdir = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
        fn = plistlib.load(open(f"{gdir}/contents.plist", "rb")).get(name)
        if fn:
            paths.append(os.path.join(gdir, fn))
    prev = None
    try:
        while True:
            if args.watch:
                print("\033[2J\033[H", end="")
            prev = dash_render(name, prev)
            if not args.watch:
                return
            print(f"\n{DIM}  watching — save in your editor to "
                  f"refresh · Ctrl+C to quit{END}")
            sys.stdout.flush()
            mt = [os.path.getmtime(p) for p in paths]
            while True:
                time.sleep(0.5)
                nmt = [os.path.getmtime(p) if os.path.exists(p) else 0
                       for p in paths]
                if nmt != mt:
                    time.sleep(0.15)  # let the editor finish writing
                    break
    except KeyboardInterrupt:
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glyphs", nargs="*", help="glyph names (default: A-Z a-z 0-9)")
    ap.add_argument("--master", choices=["Regular", "Bold"], default=None)
    ap.add_argument("--all", action="store_true", help="every glyph in the UFO")
    ap.add_argument("--arabic", action="store_true",
                    help="check the Arabic (-ar) glyphs (isolated + "
                         "positional forms) with contours")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="full detail per glyph")
    ap.add_argument("--worst", type=int, default=0,
                    help="show detail for the N worst glyphs")
    ap.add_argument("-f", "--focus", metavar="GLYPH",
                    help="one-glyph dashboard: name, character, or U+XXXX")
    ap.add_argument("-w", "--watch", action="store_true",
                    help="with --focus: re-render whenever the glif "
                         "files change (editor save)")
    args = ap.parse_args()

    if args.focus:
        focus_main(args)
        return

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
        elif args.arabic:
            names = sorted(n for n in contents
                           if n.endswith("-ar") or "-ar." in n)
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
            badness = (len(r["off2"]) * 100
                       + len(r["handles_diag"]) * 30
                       + (0 if r["adv_ok"] else 40)
                       + sum(max(0, popcount(v) - 2)
                             for v in r["handles"] + r["spans_x"] + r["spans_y"]))
            rows.append((badness, master, name, r, grade, colored))
            if args.verbose:
                detail(name, master, r)

    if not args.verbose:
        rows.sort(key=lambda t: (-t[0], t[2], t[1]))
        GRADE_COLOR = {"FAIL": RED, "OK": YELLOW, "GOOD": GREEN,
                       "PERFECT": GREEN}
        hdr = (f"{'glyph':<10} {'master':<8} {'grade':<8} "
               f"{'handles nice':<22} {'spans nice':<22} problem")
        print(f"{BOLD}{hdr}{END}")
        print(DIM + "-" * len(hdr) + END)
        for badness, master, name, r, grade, colored in rows:
            htxt, hcol = fmt_nice(r["handles"])
            stxt, scol = fmt_nice(r["spans_x"] + r["spans_y"])
            reason = fail_reason(r) if grade == "FAIL" else ""
            gcol = GRADE_COLOR[grade]
            print(f"{name:<10} {master:<8} {gcol}{grade:<8}{END} "
                  f"{hcol}{htxt:<22}{END} {scol}{stxt:<22}{END} "
                  f"{RED}{reason}{END}")
        if args.worst:
            for badness, master, name, r, grade, colored in rows[: args.worst]:
                detail(name, master, r)

    total = len(rows)
    perfect = sum(1 for row in rows if row[4] == "PERFECT")
    good = sum(1 for row in rows if row[4] in ("PERFECT", "GOOD"))
    print(f"\n{BOLD}{total} glyph-masters checked: "
          f"{GREEN}{perfect} PERFECT{END}{BOLD}, {good} at GOOD or better, "
          f"{RED if fails else GREEN}{fails} FAIL{END}")
    print(f"""{DIM}
terms:
  handle   distance from an on-curve point to its off-curve handle
           (curve tension); the design system wants these axis-aligned
           and in tidy lengths
  span     gap between neighboring on-curve x-columns / y-rows (>=24u):
           stems, bars, counters, sidebearing-to-stem distances
  nice     value is a sum of at most TWO powers of two (64, 96=64+32,
           272=256+16); 'worst N' = the least-tidy value found
  optical  on-curve point on the 2-grid but off the 8 — a deliberate
           optical correction (never penalized)
grades:
  FAIL     breaks a hard rule (see problem column)   OK    handles have
  GOOD     all handles tidy to 3 terms                     4+ term values
  PERFECT  hard rules pass and every handle is nice{END}""")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
