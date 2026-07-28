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
import pathlib, sys

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


GENERATORS = {"less": gen_less_greater, "greater": gen_less_greater, "equal": gen_equal}

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
