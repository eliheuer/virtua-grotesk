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
import pathlib, re, sys

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


def write(master, name, uni, adv, contours):
    fixed = []
    for pts in contours:
        pts = normalize_start(pts)
        s = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))
        assert s > 0, f"{name}: contour wound backwards (signed area {s/2:.0f})"
        fixed.append(pts)
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
    write(master, dst, dst_uni, adv, [out])


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
    txt = (REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif").read_text()
    adv = int(float(re.search(r'<advance width="([\d.]+)"', txt).group(1)))
    contours = []
    for cm in re.finditer(r"<contour>(.*?)</contour>", txt, re.S):
        pts = []
        for pm in re.finditer(r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"(?: type="(\w+)")?( smooth="yes")?', cm.group(1)):
            x, y, typ, sm = float(pm.group(1)), float(pm.group(2)), pm.group(3), pm.group(4)
            pts.append((x, y, _join_type(typ, bool(sm)) if typ else None))
        contours.append(pts)
    return adv, contours


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
    write(master, "exclamdown", "00A1", adv, out)


def gen_cent(master):
    """cent := c + vertical bar through the ink center (sheet: -96..656)."""
    adv, cont = _read_glyph(master, "c")
    xs = [pt[0] for pts in cont for pt in pts]
    cx = (min(xs) + max(xs)) / 2
    s = {"Regular": 96, "Bold": 192}[master]  # lc stem class
    x0 = int(round((cx - s / 2) / 2) * 2)
    cont.append(bar(x0, -96, x0 + s, 656))
    write(master, "cent", "00A2", adv, cont)


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


GENERATORS = {"bar": gen_bar, "exclamdown": gen_exclamdown, "cent": gen_cent,
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
