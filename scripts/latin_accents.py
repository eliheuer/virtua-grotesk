#!/usr/bin/env python3
"""Rebuild the Latin accent family so it is one consistent system.

Three things were wrong (measured by scripts/latin_diacritics_audit.py and
against Rubik):

1. **Band.** grave/acute/hungarumlaut sit at 638..832 and read correctly.
   circumflex sat at 440..744, caron at 504..808, tilde at 380..548 —
   below x-height. Every accent now starts from the same band.

2. **Height.** circumflex and caron were 304 tall against the family's
   194. That matters beyond looks: a 304-tall accent cannot clear a
   capital (top anchor 768) without passing WinAscent 1094, which is
   exactly why Acircumflex was hand-placed at +337 and ended up the
   tallest glyph in the font.

3. **Chamfers.** grave/acute/hungarumlaut carry the house 16-unit bevel;
   circumflex, caron and tilde had bare sharp corners. DESIGN.md: every
   sharp junction gets a 45-degree bevel.

Rubik was the reference for proportion only: its accents all live in one
tight band (604..758 scaled to this UPM) and its circumflex is the same
height as its acute. Virtua's own grave/acute give the band and the
16-unit language.

Usage:
    ./.venv/bin/python scripts/latin_accents.py [--dry-run]
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import write_glyph, read_points  # noqa: E402

# --- the band, taken from the accents that already read correctly --------
BAND_BOT = 638          # grave / acute / hungarumlaut ink bottom
BAND_TOP = 832          # ... and ink top
CH = 16                 # house chamfer
# output is marked BLUE (arabic_build default) — awaiting grading


def chamfer_rect(x0, y0, x1, y1, ch=CH):
    return [(x0 + ch, y0, "line", False), (x1 - ch, y0, "line", False),
            (x1, y0 + ch, "line", False), (x1, y1 - ch, "line", False),
            (x1 - ch, y1, "line", False), (x0 + ch, y1, "line", False),
            (x0, y1 - ch, "line", False), (x0, y0 + ch, "line", False)]


def chevron(cx, half, y_bot, y_top, slope, up=True, ch=CH):
    """A chevron in the house language: constant-width legs, 16-unit
    chamfers on the apex and both feet.

    `up` draws ^ (circumflex); False draws v (caron), the exact mirror, so
    the two stay a matched pair by construction.

    Geometry: with half-width `half` and leg slope `slope`, the rise from
    foot to apex is half*slope and the vertical offset between the outer
    and inner edge is the perpendicular stroke times sqrt(1+slope^2) — so
    picking the slope sets the stroke for a given overall height.
    """
    apex_half = 32                       # half of the 64-wide apex flat
    run = half - apex_half
    rise = round(run * slope)
    outer_foot = y_top - rise            # outer edge at the feet
    inner_foot = y_bot                   # inner edge at the feet
    inner_apex = y_bot + rise

    pts = [
        (cx - half, outer_foot - ch),          # left foot, outer
        (cx - half + ch, outer_foot + ch // 2),
        (cx - apex_half, y_top - ch),
        (cx - apex_half + ch, y_top),          # apex flat
        (cx + apex_half - ch, y_top),
        (cx + apex_half, y_top - ch),
        (cx + half - ch, outer_foot + ch // 2),
        (cx + half, outer_foot - ch),          # right foot, outer
        (cx + half, inner_foot + ch),
        (cx + half - ch, inner_foot),          # right foot, inner
        (cx + apex_half + ch, inner_apex - ch // 2),
        (cx + apex_half, inner_apex),
        (cx - apex_half, inner_apex),
        (cx - apex_half - ch, inner_apex - ch // 2),
        (cx - half + ch, inner_foot),          # left foot, inner
        (cx - half, inner_foot + ch),
    ]
    if not up:                                  # mirror vertically for caron
        mid = (y_bot + y_top)
        pts = [(x, mid - y) for x, y in pts][::-1]
    return [(round(x / 2) * 2, round(y / 2) * 2, "line", False)
            for x, y in pts]


def build_circumflex():
    # slope 0.75 gives a ~90 stroke over the 194-high band — the family
    # weight, and low enough to clear a capital inside WinAscent.
    c = chevron(cx=212, half=140, y_bot=BAND_BOT, y_top=BAND_TOP, slope=0.75)
    write_glyph("circumflex", 420, contours=[c],
                anchors=[("_top", 212, 576)])


def build_caron():
    c = chevron(cx=212, half=140, y_bot=BAND_BOT, y_top=BAND_TOP,
                slope=0.75, up=False)
    write_glyph("caron", 420, contours=[c],
                anchors=[("_top", 212, 576)])


def build_tilde():
    """Tilde kept at its own 168 height but lifted into the band, and given
    chamfered ends. Shape follows the original: a flat S wave."""
    y0 = BAND_BOT                       # 638
    h = 88                              # stroke thickness of the wave
    c = [
        (72, y0 + 12, "line", False),
        (88, y0, "line", False),        # chamfer, left end
        (184, y0 + 68, "line", False),
        (296, y0 - 12, "line", False),
        (392, y0 + 44, "line", False),
        (408, y0 + 56, "line", False),  # chamfer, right end
        (408, y0 + 56 + h - 12, "line", False),
        (392, y0 + 56 + h, "line", False),
        (296, y0 + h, "line", False),
        (184, y0 + 68 + h, "line", False),
        (88, y0 + h, "line", False),
        (72, y0 + h - 12, "line", False),
    ]
    c = [(round(x / 2) * 2, round(y / 2) * 2, t, s) for x, y, t, s in c]
    write_glyph("tilde", 520, contours=[c],
                anchors=[("_top", 240, 576)])


BUILDERS = {
    "circumflex": build_circumflex,
    "caron": build_caron,
    "tilde": build_tilde,
}


def main():
    for name, fn in BUILDERS.items():
        fn()


if __name__ == "__main__":
    main()
