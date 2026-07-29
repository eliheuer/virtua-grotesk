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
        for x, y in pts:
            fx = str(int(x)) if float(x) == int(x) else str(x)
            fy = str(int(y)) if float(y) == int(y) else str(y)
            L.append(f'\t\t\t<point x="{fx}" y="{fy}" type="line"/>')
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


def mirror(pts, adv):
    """Mirror a contour horizontally inside its advance, preserving winding."""
    return [(adv - x, y) for x, y in pts][::-1]


def write(master, name, uni, adv, contours):
    for pts in contours:  # outer contours must wind CCW (UFO ink convention)
        s = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
        assert s > 0, f"{name}: contour wound backwards (signed area {s/2:.0f})"
    p = REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs/{name}.glif"
    p.write_text(glif(name, uni, adv, contours))
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


GENERATORS = {"less": gen_less_greater, "greater": gen_less_greater, "equal": gen_equal,
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
