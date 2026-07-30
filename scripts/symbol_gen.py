#!/usr/bin/env python3
"""Parametric generator for Virtua Grotesk line-grammar glyphs.

Symbols (math, punctuation, arrows, PUA icons) are not traced — they are
GENERATED from parameters using the house grammar, so system compliance is
guaranteed by construction and both masters share point structure for free.

The grammar (see .agents/skills/anchor-sheet-glyphs/ for the workflow and
the running lessons log):
  - 2-unit grid, every value even
  - 16-unit 45-degree bevels on terminals and corners
  - 8-unit flats on notches/crotches (4 each side of the meet point)
  - TIP RULE (Eli, 2026-07-28): diagonal-arm tips land on a 16-unit
    axis-aligned flat before the bevel — never a bare bevel-to-face point.
    Anatomy: outer edge -> 16u flat -> 16u bevel -> face. Same as V/W/v
    baseline terminals.
  - stroke weights snap to the class palette; symbol (math) class:
    Regular 72, Bold 132 (hyphen class: 88 / TBD-bold)
  - math axis 352 (set from the n<=> anchor sheet, 2026-07-28)

Use as a library or run to (re)generate specific glyphs:
    ./.venv/bin/python scripts/symbol_gen.py equal
"""
import pathlib, plistlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = ("Regular", "Bold")
BLUE = "0.27,0.44,1,1"

MATH_AXIS = 352
MATH_STROKE = {"Regular": 72, "Bold": 132}
BEVEL = 16
TIP_FLAT = 16
NOTCH_FLAT = 8  # total; half each side of the meet line


def glif(name, uni, adv, contours, color=BLUE):
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<glyph name="{name}" format="2">']
    if uni:
        L.append(f'\t<unicode hex="{uni}"/>')
    L += [f'\t<advance width="{adv}"/>', '\t<outline>']
    for pts in contours:
        L.append('\t\t<contour>')
        for pt in pts:
            x, y = pt[0], pt[1]
            typ = pt[2] if len(pt) > 2 else "line"
            fx = str(int(x)) if float(x) == int(x) else str(x)
            fy = str(int(y)) if float(y) == int(y) else str(y)
            if typ is None:
                L.append(f'\t\t\t<point x="{fx}" y="{fy}"/>')
            elif typ.endswith("-smooth"):
                L.append(f'\t\t\t<point x="{fx}" y="{fy}" type="{typ[:-7]}" smooth="yes"/>')
            else:
                L.append(f'\t\t\t<point x="{fx}" y="{fy}" type="{typ}"/>')
        L.append('\t\t</contour>')
    L += ['\t</outline>', '\t<lib>', '\t\t<dict>', '\t\t\t<key>public.markColor</key>',
          f'\t\t\t<string>{color}</string>', '\t\t</dict>', '\t</lib>', '</glyph>', '']
    return "\n".join(L)


def bar(x0, y0, x1, y1):
    """Chamfered bar (hyphen anatomy): 16u bevels on all four corners."""
    return [(x0, y0 + BEVEL), (x0 + BEVEL, y0), (x1 - BEVEL, y0), (x1, y0 + BEVEL),
            (x1, y1 - BEVEL), (x1 - BEVEL, y1), (x0 + BEVEL, y1), (x0, y1 - BEVEL)]


def chevron_left(x0, x1, y_bot, y_top, tv, axis, apex_flat=48, notch_x=None):
    """'<' pointing left: apex face at x0, tip faces at x1.

    tv is the VERTICAL thickness of an arm at the tip face. Tips follow the
    TIP RULE: edge -> 16u horizontal flat -> 16u bevel -> vertical face.
    notch_x may be given explicitly (optical override) else computed so the
    inner edges parallel the outers.
    """
    f = apex_flat / 2
    if notch_x is None:
        slope = (axis - f - BEVEL - y_bot) / ((x1 - TIP_FLAT - BEVEL) - (x0 + BEVEL))
        notch_x = round(((x1 - BEVEL) - (axis - NOTCH_FLAT / 2 - y_bot - tv) / slope) / 2) * 2
    n = NOTCH_FLAT / 2
    return [
        (x1 - BEVEL - TIP_FLAT, y_bot),            # tip flat start (outer)
        (x1 - BEVEL, y_bot),                       # tip flat end
        (x1, y_bot + BEVEL),                       # bevel into face
        (x1, y_bot + tv - BEVEL),                  # face
        (x1 - BEVEL, y_bot + tv),                  # bevel out of face
        (notch_x, axis - n),                       # inner lower edge -> notch
        (notch_x, axis + n),                       # notch flat
        (x1 - BEVEL, y_top - tv),                  # inner upper edge
        (x1, y_top - tv + BEVEL),                  # bevel into face
        (x1, y_top - BEVEL),                       # face
        (x1 - BEVEL, y_top),                       # bevel out
        (x1 - BEVEL - TIP_FLAT, y_top),            # tip flat
        (x0 + BEVEL, axis + f + BEVEL),            # outer upper edge -> apex
        (x0, axis + f),                            # apex bevel
        (x0, axis - f),                            # apex face
        (x0 + BEVEL, axis - f - BEVEL),            # apex bevel -> close
    ]


def _split_type(typ):
    if typ is None:
        return None, False
    if typ.endswith("-smooth"):
        return typ[:-7], True
    return typ, False


def _join_type(base, smooth):
    if base is None:
        return None
    return base + ("-smooth" if smooth else "")


def reverse_contour(pts):
    """Reverse traversal, shifting segment types incoming->outgoing."""
    pts = [_norm(pt) for pt in pts]
    onc = [i for i, pt in enumerate(pts) if pt[2] is not None]
    outgoing = {}
    for k, i in enumerate(onc):
        nxt = onc[(k + 1) % len(onc)]
        outgoing[i] = _split_type(pts[nxt][2])[0]
    out = []
    for i in range(len(pts) - 1, -1, -1):
        x, y, typ = pts[i]
        base, smooth = _split_type(typ)
        nb = outgoing[i] if base is not None else None
        out.append((x, y, _join_type(nb, smooth)))
    return out


def mirror(pts, adv):
    """Mirror a contour horizontally inside its advance, preserving winding.

    Reversal moves segment types (line/curve) from incoming to outgoing
    segments; smooth flags stay with their points."""
    pts = [_norm(pt) for pt in pts]
    onc = [i for i, pt in enumerate(pts) if pt[2] is not None]
    outgoing = {}
    for k, i in enumerate(onc):
        nxt = onc[(k + 1) % len(onc)]
        outgoing[i] = _split_type(pts[nxt][2])[0]
    out = []
    for i in range(len(pts) - 1, -1, -1):
        x, y, typ = pts[i]
        base, smooth = _split_type(typ)
        nb = outgoing[i] if base is not None else None
        out.append((adv - x, y, _join_type(nb, smooth)))
    return out


def _norm(pt):
    return pt if len(pt) > 2 else (pt[0], pt[1], "line")


def normalize_start(pts):
    """START RULE (Eli, 2026-07-28): contour starts at the lower-LEFT
    on-curve point — leftmost first, lowest as tiebreak (min x, then min y).
    (min-y-first put the tilde's start at its trough: wrong corner.)"""
    pts = [_norm(pt) for pt in pts]
    onc = [i for i, pt in enumerate(pts) if pt[2] is not None]
    best = min(onc, key=lambda i: (pts[i][0], pts[i][1]))
    return pts[best:] + pts[:best]


def _bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def write(master, name, uni, adv, contours, normalize=True):
    """Outer contours must wind CCW (positive); counters (contours whose
    bbox sits inside another contour's bbox) must wind CW (negative).

    normalize=False keeps the given point order — REQUIRED for contours
    copied from a donor glyph: rotating each master to its own lower-left
    point can pick different indices and break master compatibility
    (dollar's S copy, 2026-07-29)."""
    fixed, areas, boxes = [], [], []
    for pts in contours:
        pts = normalize_start(pts) if normalize else [_norm(pt) for pt in pts]
        s = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))
        fixed.append(pts); areas.append(s); boxes.append(_bbox(pts))
    def _pip(pt, poly):
        # even-odd point-in-polygon on the control polygon (fine for nesting)
        x, y = pt[0], pt[1]
        inside = False
        for a, b in zip(poly, poly[1:] + poly[:1]):
            if (a[1] > y) != (b[1] > y):
                xi = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                if xi > x:
                    inside = not inside
        return inside

    def _contained(inner, outer):
        # true nesting: EVERY on-curve point inside (overlapping ink shares
        # only some points — euro's bars cross the C without nesting)
        onc = [pt for pt in inner if pt[2] is not None] or inner
        return all(_pip(pt, outer) for pt in onc)

    for i, (pts, s, bb) in enumerate(zip(fixed, areas, boxes)):
        depth = sum(1 for j in range(len(fixed))
                    if j != i and _contained(pts, fixed[j]))
        want_pos = depth % 2 == 0  # even nesting = ink (CCW), odd = counter (CW)
        assert (s > 0) == want_pos, (
            f"{name}: contour {i} winding wrong (signed area {s/2:.0f}, depth {depth})")
    p = REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif"
    p.write_text(glif(name, uni, adv, fixed))
    return p


# ---------------------------------------------------------------- glyphs
def gen_less_greater(master):
    t = MATH_STROKE[master]
    tv = {"Regular": 80, "Bold": 146}[master]          # t / cos(arm angle)
    notch = {"Regular": 182, "Bold": 322}[master]      # optical (see lessons)
    less = chevron_left(72, 528, 112, 592, tv, MATH_AXIS, notch_x=notch)
    write(master, "less", "003C", 600, [less])
    write(master, "greater", "003E", 600, [mirror(less, 600)])


def gen_equal(master):
    t = MATH_STROKE[master]
    off = {"Regular": 100, "Bold": 132}[master]        # bar center offset from axis
    bars = []
    for c in (MATH_AXIS - off, MATH_AXIS + off):
        bars.append(bar(48, int(c - t / 2), 552, int(c + t / 2)))
    write(master, "equal", "003D", 600, bars)


def _mirror_of_source(master, src, dst, dst_uni, about="adv"):
    """dst := src mirrored (backslash<-slash, grave<-acute).
    Family/mirror-partner rule: when the partner exists green, derive it.
    about="adv" mirrors inside the advance (spacing glyphs); about="ink"
    mirrors about the ink center — REQUIRED for mark components (grave),
    so composites that position the mark by xOffset stay aligned."""
    g = REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs/{src}.glif"
    txt = g.read_text()
    adv = int(float(re.search(r'<advance width="([\d.]+)"', txt).group(1)))
    pts = [(float(m.group(1)), float(m.group(2))) for m in
           re.finditer(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"', txt)]
    if about == "ink":
        xs = [x for x, _ in pts]
        axis = min(xs) + max(xs)          # reflect: x' = axis - x
        out = [(axis - x, y) for x, y in pts][::-1]
    else:
        out = mirror(pts, adv)
    write(master, dst, dst_uni, adv, [out], normalize=False)


def gen_backslash(master):
    _mirror_of_source(master, "slash", "backslash", "005C")


def gen_grave(master):
    _mirror_of_source(master, "acute", "grave", "0060", about="ink")


def gen_brackets(master):
    s = {"Regular": 72, "Bold": 128}[master]           # stroke (HN B/R ratio 1.78)
    reach = {"Regular": 288, "Bold": 368}[master]      # arm right extent
    adv = {"Regular": 320, "Bold": 400}[master]        # sb 80 stem-side / 32 open
    y0, y1 = -128, 848
    x0 = 80
    left = [
        (x0 + BEVEL, y0), (reach - BEVEL, y0), (reach, y0 + BEVEL),
        (reach, y0 + s - BEVEL), (reach - BEVEL, y0 + s),
        (x0 + s + 8, y0 + s), (x0 + s, y0 + s + 8),
        (x0 + s, y1 - s - 8), (x0 + s + 8, y1 - s),
        (reach - BEVEL, y1 - s), (reach, y1 - s + BEVEL),
        (reach, y1 - BEVEL), (reach - BEVEL, y1),
        (x0 + BEVEL, y1), (x0, y1 - BEVEL), (x0, y0 + BEVEL),
    ]
    write(master, "bracketleft", "005B", adv, [left])
    write(master, "bracketright", "005D", adv, [mirror(left, adv)])


def gen_asciicircum(master):
    # chevron pointing up: apex flat on top, tips follow the TIP RULE rotated
    # (vertical 16u flat -> bevel -> horizontal face). Box 40..520 x 480..800.
    if master == "Regular":
        face_in, notch_y = 116, 704
    else:
        face_in, notch_y = 204, 594
    fl = face_in - 16                                  # inner bevel start x (left)
    pts = [
        (40, 512), (240, 784), (256, 800), (304, 800), (320, 784),
        (520, 512), (520, 496), (504, 480),
        (560 - fl, 480), (560 - face_in, 496),
        (284, notch_y), (276, notch_y),
        (face_in, 496), (fl, 480),
        (56, 480), (40, 496),
    ]
    pts = pts[::-1]  # wind CCW like every other contour (UFO ink convention)
    write(master, "asciicircum", "005E", 560, [pts])


def gen_underscore(master):
    # same both masters (HN precedent: underscore does not bolden)
    write(master, "underscore", "005F", 600, [bar(68, -188, 532, -116)])




def _read_glyph(master, name):
    """Parse a glif into (adv, [contours of (x, y, type) tuples])."""
    glyphs = REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
    with (glyphs / "contents.plist").open("rb") as f:
        filename = plistlib.load(f)[name]
    txt = (glyphs / filename).read_text()
    adv = int(float(re.search(r'<advance width="([\d.]+)"', txt).group(1)))
    contours = []
    for cm in re.finditer(r"<contour>(.*?)</contour>", txt, re.S):
        pts = []
        for pm in re.finditer(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"(?: type="(\w+)")?( smooth="yes")?', cm.group(1)):
            x, y, typ, sm = float(pm.group(1)), float(pm.group(2)), pm.group(3), pm.group(4)
            pts.append((x, y, _join_type(typ, bool(sm)) if typ else None))
        contours.append(pts)
    return adv, contours


def _union_contours(contours):
    """Cubic-aware boolean union, preserving typed points in the result."""
    from booleanOperations.booleanOperationManager import BooleanOperationManager
    from defcon import Glyph

    source = Glyph()
    pen = source.getPointPen()
    for pts in contours:
        pen.beginPath()
        for x, y, typ in [_norm(pt) for pt in pts]:
            segment_type, smooth = _split_type(typ)
            pen.addPoint((x, y), segmentType=segment_type, smooth=smooth)
        pen.endPath()

    result = Glyph()
    BooleanOperationManager.union(list(source), result.getPointPen())
    out = []
    for contour in result:
        pts = []
        for point in contour:
            typ = _join_type(point.segmentType, point.smooth)
            pts.append((round(point.x / 2) * 2,
                        round(point.y / 2) * 2,
                        typ))
        out.append(pts)
    return out


def _reconcile_dollar_union(master, contours):
    """Remove Bold-only union slivers so dollar masters share topology."""
    outer = contours[0]
    if master == "Regular":
        upper = next(i for i, pt in enumerate(outer)
                     if pt[:2] == (392, 448))
        assert outer[upper] == (392, 448, "curve-smooth")
        outer[upper] = (392, 448, "curve")
        return contours

    upper = next(i for i, pt in enumerate(outer)
                 if pt[:2] == (440, 464))
    assert outer[upper:upper + 4] == [
        (440, 464, "curve"),
        (426, 466, None),
        (414, 470, None),
        (400, 472, "curve"),
    ]
    outer[upper:upper + 4] = [
        (440, 464, "curve"),
        (400, 472, "line"),
    ]

    lower = next(i for i, pt in enumerate(outer)
                 if pt[:2] == (288, 328))
    assert outer[lower:lower + 3] == [
        (288, 328, "curve"),
        (296, 326, "line"),
        (296, 146, "line"),
    ]
    del outer[lower + 1]
    return contours


def gen_bar(master):
    s = {"Regular": 80, "Bold": 144}[master]  # sheet 79; Bold via bracket ratio
    x0 = (320 - s) // 2
    write(master, "bar", "007C", 320, [bar(x0, -128, x0 + s, 848)])


def gen_exclamdown(master):
    """exclamdown := exclam rotated 180 degrees, top aligned at 656."""
    adv, cont = _read_glyph(master, "exclam")
    # 180-degree rotation preserves orientation: transform in order, no reversal.
    out = []
    for pts in cont:
        out.append([(adv - pt[0], 656 - pt[1], _norm(pt)[2]) for pt in pts])
    write(master, "exclamdown", "00A1", adv, out, normalize=False)


def gen_cent(master):
    """cent := c + vertical bar through the ink center (sheet: -96..656)."""
    adv, cont = _read_glyph(master, "c")
    xs = [pt[0] for pts in cont for pt in pts]
    cx = (min(xs) + max(xs)) / 2
    s = {"Regular": 96, "Bold": 192}[master]  # lc stem class
    x0 = int(round((cx - s / 2) / 2) * 2)
    cont.append(bar(x0, -96, x0 + s, 656))
    write(master, "cent", "00A2", adv, cont, normalize=False)


def gen_asciitilde(master):
    """Tilde per Eli's graded Regular (2026-07-29): terminals are
    face + 16u bevel + 16u flat, the curve LEAVES the flat at a corner and
    ENTERS the opposite terminal's 45-degree bevel tangentially; crest and
    trough projections are on-curve G2 smooths with horizontal tangents.
    Bold = same skeleton, bottom side -30 / top side +30 (stroke 72->132).
    Verify with scripts/curve_continuity.py (targets: G2, no kinks)."""
    # (x, y, type, side) — side: -1 bottom path, +1 top path
    P = [(80,320,"line",-1),(96,304,"line",-1),(112,304,"line",-1),
         (128,338,None,-1),(160,362,None,-1),(192,362,"curve-smooth",-1),
         (240,362,None,-1),(264,306,None,-1),(328,306,"curve-smooth",-1),
         (366,306,None,-1),(382,326,None,-1),(416,360,"curve-smooth",-1),
         (432,376,"line",-1),(432,416,"line",+1),(416,432,"line",+1),
         (400,432,"line",+1),(368,392,None,+1),(346,378,None,+1),
         (328,378,"curve-smooth",+1),(292,378,None,+1),(254,432,None,+1),
         (192,432,"curve-smooth",+1),(164,432,None,+1),(141,421,None,+1),
         (96,376,"curve-smooth",+1),(80,360,"line",+1)]
    d = {"Regular": 0, "Bold": 30}[master]
    pts = [(x, (y - d) if s < 0 else (y + d), typ) for (x, y, typ, s) in P]
    write(master, "asciitilde", "007E", 520, [pts])


def gen_braces(master):
    """{ : chevron-style beak + curved hooks + stem runs. Box -128..848."""
    t_ = {"Regular": 72, "Bold": 128}[master]
    xo = {"Regular": 200, "Bold": 176}[master]   # stem outer x
    xi = xo + t_                                  # stem inner x
    tipx = {"Regular": 360, "Bold": 392}[master]  # tip face x
    adv = {"Regular": 400, "Bold": 432}[master]
    nx = {"Regular": 176, "Bold": 232}[master]    # inner notch x
    mid = 360
    pts = [
        # beak face (lower-left start comes from normalize_start)
        (88, 336), (88, 384), (104, 400),
        # outer: beak -> stem -> top tip
        (148, 404, None), (xo, 432, None), (xo, 480, "curve-smooth"),
        (xo, 680, "line-smooth"),
        (xo, 772, None), (xo + 56, 848, None), (tipx - 16, 848, "curve"),
        (tipx, 832), (tipx, 792), (tipx - 16, 776),
        # inner: top tip -> stem -> notch
        (xi + 16, 776, None), (xi, 732, None), (xi, 672, "curve-smooth"),
        (xi, 488, "line-smooth"),
        (xi, 432, None), (nx + 40, 396, None), (nx, 364, "curve"),
        (nx, 356),
        # mirror half (bottom): notch -> stem -> bottom tip -> beak
        (nx + 40, 324, None), (xi, 288, None), (xi, 232, "curve-smooth"),
        (xi, 48, "line-smooth"),
        (xi, -12, None), (xi + 16, -56, None), (tipx - 16, -56, "curve"),
        (tipx, -72), (tipx, -112), (tipx - 16, -128),
        (xo + 56, -128, None), (xo, -52, None), (xo, 40, "curve-smooth"),
        (xo, 240, "line-smooth"),
        (xo, 288, None), (148, 316, None), (104, 320, "curve"),
    ]
    pts = reverse_contour(pts)
    write(master, "braceleft", "007B", adv, [pts])
    write(master, "braceright", "007D", adv, [mirror(pts, adv)])




def harmonize_g2(pts, passes=6):
    """Auto-harmonize: at every smooth curve-curve joint, scale the two
    adjacent handle lengths so endpoint curvatures match (kappa = 2/3 d/l^2)
    — symbol_gen's version of Runebender's harmonize->G2. Tangents are
    untouched; only handle lengths change. Grid-rounds at the end."""
    import math
    pts = [_norm(pt) for pt in pts]
    n = len(pts)
    for _ in range(passes):
        onc = [i for i, pt in enumerate(pts) if pt[2] is not None]
        for i in onc:
            if not (pts[i][2] or "").startswith("curve-smooth") and pts[i][2] != "curve-smooth":
                continue
            ip, iN = (i - 1) % n, (i + 1) % n
            if pts[ip][2] is not None or pts[iN][2] is not None:
                continue  # need curves on both sides
            i2, i3 = (i - 2) % n, (i + 2) % n
            P = pts[i]
            def kappa(cadj, csec):
                l = math.hypot(cadj[0] - P[0], cadj[1] - P[1])
                if l == 0: return None, 0
                ux, uy = (P[0] - cadj[0]) / l, (P[1] - cadj[1]) / l
                d = abs((csec[0] - P[0]) * uy - (csec[1] - P[1]) * ux)
                return (2.0 / 3.0) * d / (l * l), l
            k_in, l_in = kappa(pts[ip], pts[i2])
            k_out, l_out = kappa(pts[iN], pts[i3])
            if not k_in or not k_out or min(k_in, k_out) <= 0:
                continue
            kt = math.sqrt(k_in * k_out)
            for j, l, k in ((ip, l_in, k_in), (iN, l_out, k_out)):
                f = math.sqrt(k / kt)
                x, y, typ = pts[j]
                pts[j] = (P[0] + (x - P[0]) * f, P[1] + (y - P[1]) * f, typ)
    return [(round(x / 2) * 2, round(y / 2) * 2, typ) for x, y, typ in pts]


def _scale_translate(contours, s, dx, dy):
    out = []
    for pts in contours:
        out.append([(round((x * s + dx) / 2) * 2, round((y * s + dy) / 2) * 2, typ)
                    for x, y, typ in [_norm(pt) for pt in pts]])
    return out


def _circle(cx, cy, r, ccw=True):
    """Circle contour from four cubic quadrants (kappa 0.5523)."""
    k = round(r * 0.5523 / 2) * 2
    P = [(cx + r, cy, "curve-smooth"), (cx + r, cy + k, None), (cx + k, cy + r, None),
         (cx, cy + r, "curve-smooth"), (cx - k, cy + r, None), (cx - r, cy + k, None),
         (cx - r, cy, "curve-smooth"), (cx - r, cy - k, None), (cx - k, cy - r, None),
         (cx, cy - r, "curve-smooth"), (cx + k, cy - r, None), (cx + r, cy - k, None)]
    return P if ccw else reverse_contour(P)


def gen_dieresis(master):
    """Two i-tittles (family donor); ink center kept at 180 for composites."""
    _, cont = _read_glyph(master, "i")
    tittle = max(cont, key=lambda pts: min(pt[1] for pt in pts))
    tittle = [_norm(pt) for pt in tittle]
    x0 = min(pt[0] for pt in tittle)
    w = max(pt[0] for pt in tittle) - x0
    gap = {"Regular": 88, "Bold": 64}[master]
    dl = (180 - gap / 2 - w) - x0
    dr = (180 + gap / 2) - x0
    left = [(x + dl, y, typ) for x, y, typ in tittle]
    right = [(x + dr, y, typ) for x, y, typ in tittle]
    write(master, "dieresis", "00A8", 360, [left, right], normalize=False)


def gen_ordfeminine(master):
    """Superior a: the a scaled 0.87 (sheet), bottom seated at 256."""
    _, cont = _read_glyph(master, "a")
    xs = [pt[0] for pts in cont for pt in pts]
    ys = [pt[1] for pts in cont for pt in pts]
    s = 0.87
    dy = 256 - min(ys) * s
    dx = (616 - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    write(master, "ordfeminine", "00AA", 616, _scale_translate(cont, s, dx, dy), normalize=False)


def gen_copyright(master):
    """Ring (outer dia 832, stroke 44/80) + c scaled 0.74 at ring center."""
    ring_s = {"Regular": 44, "Bold": 80}[master]
    cx, cy, R = 464, 384, 416
    _, cont = _read_glyph(master, "c")
    xs = [pt[0] for pts in cont for pt in pts]
    ys = [pt[1] for pts in cont for pt in pts]
    s = 0.74
    dx = cx - (min(xs) + max(xs)) / 2 * s
    dy = cy - (min(ys) + max(ys)) / 2 * s
    contours = [_circle(cx, cy, R), _circle(cx, cy, R - ring_s, ccw=False)]
    contours += _scale_translate(cont, s, dx, dy)
    write(master, "copyright", "00A9", 928, contours, normalize=False)


def gen_yen(master):
    """V-arms + stem + two bars (sheet: bars at 294/186 R, arms to 768)."""
    stem = {"Regular": 100, "Bold": 192}[master]
    cx = 332
    x0, x1 = cx - stem // 2, cx + stem // 2
    # topology mirrors the green Y: stem -> right arm LOWER edge -> tip ->
    # right arm upper edge -> notch -> left arm upper edge -> tip -> left
    # arm lower edge -> stem. (v1 routed the outer edge into the notch and
    # the arms crossed like a bowtie.)
    ypart = [
        (x0, 16), (x0 + 16, 0), (x1 - 16, 0), (x1, 16),
        (x1, 430), (632, 704), (632, 752), (616, 768), (564, 768), (548, 752),
        (cx + 4, 470), (cx - 4, 470),
        (116, 752), (100, 768), (48, 768), (32, 752), (32, 704), (x0, 430),
    ]
    if master == "Regular":
        bars = [bar(84, 294, 580, 366), bar(84, 186, 580, 258)]
    else:
        bars = [bar(84, 274, 580, 386), bar(84, 130, 580, 242)]
    write(master, "yen", "00A5", 664, [ypart] + bars)


def gen_sterling(master):
    """v1: straight base + stem + hook with G2 apex extrema + crossbar.
    (The sheet has a gentle wave base - flagged as an upgrade candidate.)"""
    st = {"Regular": 100, "Bold": 176}[master]
    xs0 = 120
    xs1 = xs0 + st
    base = bar(32, 0, 600, 88)
    crossbar = bar(40, 348, 376, 420)
    hook_t = {"Regular": 96, "Bold": 172}[master]
    apex_o, apex_i = 784, 784 - hook_t
    main = [
        (xs0, 88), (xs0, 560, "line-smooth"),
        (xs0, 688, None), (196, apex_o, None), (312, apex_o, "curve-smooth"),
        (452, apex_o, None), (600, 726, None), (600, 640, "curve"),
        (600, 612), (584, 596), (568, 612),
        (568, 640, None), (460, apex_i, None), (320, apex_i, "curve-smooth"),
        (236, apex_i, None), (xs1, 656, None), (xs1, 560, "curve-smooth"),
        (xs1, 88),
    ]
    main = harmonize_g2(reverse_contour(main))  # CCW + auto-G2
    write(master, "sterling", "00A3", 632, [base, crossbar, main])




def _translate(contours, dx, dy):
    return [[(x + dx, y + dy, typ) for x, y, typ in [_norm(pt) for pt in pts]]
            for pts in contours]


def _rotate180(contours, adv, top):
    """Rotate 180 degrees about the advance center, seating the result's top
    at `top` (the exclamdown/questiondown convention)."""
    out = []
    for pts in contours:
        out.append([(adv - pt[0], top - pt[1], _norm(pt)[2]) for pt in pts])
    return out


def gen_plus(master):
    """Cross: math class. Arms 72/132, extent 480 square on axis 352,
    bar-end bevels 16, concave junction fillets 8 (H-crossbar anatomy)."""
    s = MATH_STROKE[master]
    h = s // 2
    cx, cy, ext = 300, MATH_AXIS, 240
    x0, x1 = cx - ext, cx + ext
    y0, y1 = cy - ext, cy + ext
    vl, vr = cx - h, cx + h
    hb, ht = cy - h, cy + h
    pts = [
        (vl, y0 + 16), (vl + 16, y0), (vr - 16, y0), (vr, y0 + 16),
        (vr, hb - 8), (vr + 8, hb),
        (x1 - 16, hb), (x1, hb + 16), (x1, ht - 16), (x1 - 16, ht),
        (vr + 8, ht), (vr, ht + 8),
        (vr, y1 - 16), (vr - 16, y1), (vl + 16, y1), (vl, y1 - 16),
        (vl, ht + 8), (vl - 8, ht),
        (x0 + 16, ht), (x0, ht - 16), (x0, hb + 16), (x0 + 16, hb),
        (vl - 8, hb), (vl, hb - 8),
    ]
    write(master, "plus", "002B", 600, [pts])


def gen_periodcentered(master):
    """period raised to the math axis."""
    adv, cont = _read_glyph(master, "period")
    ys = [pt[1] for pts in cont for pt in pts]
    dy = MATH_AXIS - (min(ys) + max(ys)) / 2
    write(master, "periodcentered", "00B7", adv, _translate(cont, 0, round(dy / 2) * 2), normalize=False)


def gen_ordmasculine(master):
    """Superior o: twin of ordfeminine (o scaled 0.87, seated at 256)."""
    _, cont = _read_glyph(master, "o")
    xs = [pt[0] for pts in cont for pt in pts]
    ys = [pt[1] for pts in cont for pt in pts]
    s = 0.87
    dy = 256 - min(ys) * s
    dx = (616 - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    write(master, "ordmasculine", "00BA", 616, _scale_translate(cont, s, dx, dy), normalize=False)


def gen_questiondown(master):
    """question rotated 180, top seated at 656 (exclamdown convention)."""
    adv, cont = _read_glyph(master, "question")
    write(master, "questiondown", "00BF", adv, _rotate180(cont, adv, 656), normalize=False)


def gen_dollar(master):
    """Uppercase S + centered bar, flattened per the FLAT RULE."""
    adv, cont = _read_glyph(master, "S")
    xs = [pt[0] for pts in cont for pt in pts]
    cx = round((min(xs) + max(xs)) / 4) * 2
    bw = {"Regular": 64, "Bold": 104}[master]
    cont.append(bar(int(cx - bw / 2), -96, int(cx + bw / 2), 848))
    united = _reconcile_dollar_union(master, _union_contours(cont))
    write(master, "dollar", "0024", adv, united, normalize=False)


def gen_euro(master):
    """C + two crossbars (the cent construction at cap scale)."""
    adv, cont = _read_glyph(master, "C")
    s = MATH_STROKE[master]
    off = {"Regular": 60, "Bold": 90}[master]  # Bold bars at +-60 overlap
    for c0 in (384 + off, 384 - off):
        cont.append(bar(8, int(c0 - s / 2), 400, int(c0 + s / 2)))
    write(master, "euro", "20AC", adv, cont, normalize=False)


def gen_registered(master):
    """copyright's ring + R scaled 0.60 at the ring center."""
    ring_s = {"Regular": 44, "Bold": 80}[master]
    cx, cy, R = 464, 384, 416
    _, cont = _read_glyph(master, "R")
    xs = [pt[0] for pts in cont for pt in pts]
    ys = [pt[1] for pts in cont for pt in pts]
    s = 0.68
    dx = cx - (min(xs) + max(xs)) / 2 * s
    dy = cy - (min(ys) + max(ys)) / 2 * s
    contours = [_circle(cx, cy, R), _circle(cx, cy, R - ring_s, ccw=False)]
    contours += _scale_translate(cont, s, dx, dy)
    write(master, "registered", "00AE", 928, contours, normalize=False)


GENERATORS = {"plus": gen_plus, "periodcentered": gen_periodcentered,
              "ordmasculine": gen_ordmasculine, "questiondown": gen_questiondown,
              "dollar": gen_dollar, "euro": gen_euro, "registered": gen_registered,
              "dieresis": gen_dieresis, "ordfeminine": gen_ordfeminine,
              "copyright": gen_copyright, "yen": gen_yen, "sterling": gen_sterling,
              "bar": gen_bar, "exclamdown": gen_exclamdown, "cent": gen_cent,
              "asciitilde": gen_asciitilde, "braceleft": gen_braces, "braceright": gen_braces,
              "less": gen_less_greater, "greater": gen_less_greater, "equal": gen_equal,
              "bracketleft": gen_brackets, "bracketright": gen_brackets,
              "backslash": gen_backslash, "grave": gen_grave,
              "asciicircum": gen_asciicircum, "underscore": gen_underscore}

if __name__ == "__main__":
    targets = sys.argv[1:] or sorted(set(GENERATORS))
    done = set()
    for g in targets:
        fn = GENERATORS[g]
        if fn in done:
            continue
        done.add(fn)
        for m in MASTERS:
            fn(m)
        print(f"generated {g} (both masters)")
