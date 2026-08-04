#!/usr/bin/env python3
"""Lane-4: Arabic-Indic digits, Farsi digit variants, and Arabic
punctuation / signs.

Digits are drawn parametrically in the Virtua grammar (stroke 96, rounds
112, chamfer 16, grid 2) at digit height 640 on the Arabic baseline, using
Rubik only for proportion and shape identity. Punctuation reuses Latin
donors mirrored or copied where the Unicode chart says the shapes match.

Usage:
    ./.venv/bin/python scripts/arabic_symbols.py [names...]
"""

import sys
import pathlib
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import (write_glyph, read_points, glif_path,  # noqa: E402
                          reverse_contour, MASTERS)

UFO = MASTERS[0]

H = 640           # Arabic digit height
S = 96            # straight stroke
R = 112           # round stroke
CH = 16           # chamfer


def latin(name):
    return read_points(name)


def latin_advance(name):
    return float(ET.parse(glif_path(UFO, name)).getroot()
                 .find("advance").get("width"))


def mirror(contours, axis):
    """Mirror about the vertical line x=axis, keeping winding."""
    return [reverse_contour([(2 * axis - x, y, t, s) for x, y, t, s in c])
            for c in contours]


def move(contours, dx=0, dy=0):
    return [[(x + dx, y + dy, t, s) for x, y, t, s in c] for c in contours]


def scale(contours, f, cx=0, cy=0):
    return [[(round((cx + (x - cx) * f) / 2) * 2,
              round((cy + (y - cy) * f) / 2) * 2, t, s)
             for x, y, t, s in c] for c in contours]


def bar(x0, y0, x1, y1, ch=CH):
    """Axis-aligned bar with chamfered corners."""
    return [(x0 + ch, y0, "line", False), (x1 - ch, y0, "line", False),
            (x1, y0 + ch, "line", False), (x1, y1 - ch, "line", False),
            (x1 - ch, y1, "line", False), (x0 + ch, y1, "line", False),
            (x0, y1 - ch, "line", False), (x0, y0 + ch, "line", False)]


def ring(cx, cy, rx, ry, t):
    """Chamfer-free monolinear ring of thickness t."""
    k = 0.5523
    def loop(rx, ry, rev):
        pts = [(cx, cy + ry, "curve", True),
               (cx + k * rx, cy + ry, None, False),
               (cx + rx, cy + k * ry, None, False),
               (cx + rx, cy, "curve", True),
               (cx + rx, cy - k * ry, None, False),
               (cx + k * rx, cy - ry, None, False),
               (cx, cy - ry, "curve", True),
               (cx - k * rx, cy - ry, None, False),
               (cx - rx, cy - k * ry, None, False),
               (cx - rx, cy, "curve", True),
               (cx - rx, cy + k * ry, None, False),
               (cx - k * rx, cy + ry, None, False)]
        pts = [(round(x / 2) * 2, round(y / 2) * 2, ty, sm)
               for x, y, ty, sm in pts]
        return reverse_contour(pts) if rev else pts
    return [loop(rx, ry, False), loop(rx - t, ry - t, True)]


# --- digits ---------------------------------------------------------------

def digits():
    # ٠ zero — a small filled diamond/square dot
    write_glyph("zero-ar", 320, contours=[bar(112, 224, 208, 320, ch=32)])

    # ١ one — plain vertical stroke
    write_glyph("one-ar", 288, contours=[bar(96, 0, 192, H)])

    # ٢ two — hook: horizontal top, down-left, small curl
    write_glyph("two-ar", 480, contours=[[
        (384, H, "line", False), (384, 168, "line", True),
        (384, 64, None, False), (312, 0, None, False),
        (208, 0, "curve", True),
        (96, 0, "line", False), (96, 96, "line", False),
        (208, 96, "line", True), (256, 96, None, False),
        (288, 128, None, False), (288, 176, "curve", True),
        (288, H, "line", False)]])

    # ٣ three — two prongs over the two-hook
    write_glyph("three-ar", 640, contours=[[
        (544, H, "line", False), (544, 168, "line", True),
        (544, 64, None, False), (472, 0, None, False),
        (368, 0, "curve", True),
        (96, 0, "line", False), (96, 96, "line", False),
        (368, 96, "line", True), (416, 96, None, False),
        (448, 128, None, False), (448, 176, "curve", True),
        (448, H, "line", False)]] + [
        bar(256, 264, 352, H), bar(96, 264, 192, H)])

    # ٤ four — reversed-3 form: open bowl on a stem
    write_glyph("four-ar", 544, contours=[[
        (448, 0, "line", False), (448, 424, "line", True),
        (448, 544, None, False), (368, H, None, False),
        (248, H, "curve", True),
        (128, H, None, False), (48, 544, None, False),
        (48, 424, "curve", True),
        (48, 320, "line", False), (144, 320, "line", False),
        (144, 424, "line", True), (144, 488, None, False),
        (184, 528, None, False), (248, 528, "curve", True),
        (312, 528, None, False), (352, 488, None, False),
        (352, 424, "curve", True),
        (352, 0, "line", False)]])

    # ٥ five — a small closed ring sitting on the baseline
    write_glyph("five-ar", 448, contours=ring(224, 176, 176, 176, R))

    # ٦ six — vertical stroke with a bowl swinging left at the bottom
    write_glyph("six-ar", 512, contours=[[
        (416, H, "line", False), (416, 240, "line", True),
        (416, 96, None, False), (320, 0, None, False),
        (192, 0, "curve", True),
        (96, 0, None, False), (48, 56, None, False),
        (48, 128, "curve", True),
        (48, 224, "line", False), (144, 224, "line", False),
        (144, 144, "line", True), (144, 116, None, False),
        (160, 96, None, False), (192, 96, "curve", True),
        (264, 96, None, False), (320, 152, None, False),
        (320, 240, "curve", True),
        (320, H, "line", False)]])

    # ٧ seven — V
    write_glyph("seven-ar", 512, contours=[[
        (96, H, "line", False), (192, H, "line", False),
        (256, 176, "line", False), (320, H, "line", False),
        (416, H, "line", False), (304, 0, "line", False),
        (208, 0, "line", False)]])

    # ٨ eight — inverted V
    write_glyph("eight-ar", 512, contours=[[
        (96, 0, "line", False), (192, 0, "line", False),
        (256, 464, "line", False), (320, 0, "line", False),
        (416, 0, "line", False), (304, H, "line", False),
        (208, H, "line", False)]])

    # ٩ nine — ring with a stem dropping from its right extreme. Drawn as
    # one flat outline (FLAT RULE) rather than overlaid ring + bar.
    inner = ring(240, 432, 192, 192, R)[1]
    nine = [
        (240, 624, "curve", True),
        (346, 624, None, False), (432, 538, None, False),
        (432, 432, "curve", True),
        (432, 0, "line", False),
        (320, 0, "line", False),
        (320, 258, "line", False),
        (300, 246, None, False), (272, 240, None, False),
        (240, 240, "curve", True),
        (134, 240, None, False), (48, 326, None, False),
        (48, 432, "curve", True),
        (48, 538, None, False), (134, 624, None, False),
    ]
    write_glyph("nine-ar", 528, contours=[nine, inner])

    # Farsi variants that match the Arabic-Indic shapes
    for a, b in (("zero", "zeroFarsi"), ("one", "oneFarsi"),
                 ("two", "twoFarsi"), ("three", "threeFarsi"),
                 ("seven", "sevenFarsi"), ("eight", "eightFarsi"),
                 ("nine", "nineFarsi")):
        write_glyph(f"{b}-ar", latin_advance(f"{a}-ar"),
                    components=[(f"{a}-ar", 0, 0)])

    # ۴ Farsi four — open-topped bowl with a flat foot
    write_glyph("fourFarsi-ar", 544, contours=[[
        (448, 0, "line", False), (448, H, "line", False),
        (352, H, "line", False), (352, 320, "line", True),
        (352, 288, None, False), (320, 256, None, False),
        (272, 256, "curve", True),
        (176, 256, "line", True), (128, 256, None, False),
        (96, 288, None, False), (96, 320, "curve", True),
        (96, H, "line", False), (0, H, "line", False),
        (0, 320, "line", True), (0, 216, None, False),
        (72, 160, None, False), (176, 160, "curve", True),
        (272, 160, "line", True), (312, 160, None, False),
        (336, 152, None, False), (352, 136, "curve", False),
        (352, 0, "line", False)]])

    # ۵ Farsi five — heart-ish open bowl
    write_glyph("fiveFarsi-ar", 544, contours=[[
        (64, 320, "line", True),
        (64, 200, None, False), (152, 96, None, False),
        (272, 96, "curve", True),
        (392, 96, None, False), (480, 200, None, False),
        (480, 320, "curve", True),
        (480, 424, "line", False), (384, 424, "line", False),
        (384, 320, "line", True),
        (384, 248, None, False), (336, 192, None, False),
        (272, 192, "curve", True),
        (208, 192, None, False), (160, 248, None, False),
        (160, 320, "curve", True),
        (160, 424, "line", False), (64, 424, "line", False)]])

    # ۶ Farsi six — like six with a taller upper hook
    write_glyph("sixFarsi-ar", 512, components=[("six-ar", 0, 0)])


# --- punctuation & signs ---------------------------------------------------

def punctuation():
    aw = latin_advance("comma")
    write_glyph("comma-ar", aw, contours=mirror(latin("comma"), aw / 2))
    aw = latin_advance("semicolon")
    write_glyph("semicolon-ar", aw, contours=mirror(latin("semicolon"), aw / 2))
    aw = latin_advance("question")
    write_glyph("question-ar", aw, contours=mirror(latin("question"), aw / 2))

    # RTL parens: the Latin shapes swap roles
    write_glyph("parenleft-ar", latin_advance("parenright"),
                components=[("parenright", 0, 0)])
    write_glyph("parenright-ar", latin_advance("parenleft"),
                components=[("parenleft", 0, 0)])

    write_glyph("fullStop-ar", latin_advance("period"),
                components=[("period", 0, 0)])
    write_glyph("percent-ar", latin_advance("percent"),
                components=[("percent", 0, 0)])

    # ؉ per-mille: percent plus a third ring, built from percent's own zero
    write_glyph("perMille-ar", latin_advance("percent") + 288,
                components=[("percent", 0, 0), ("zero-ar", 936, 0)])

    # ٭ five-pointed Arabic star, drawn on the math axis
    cx, cy, ro, ri = 288, 480, 224, 96
    import math
    star = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        r = ro if i % 2 == 0 else ri
        star.append((round((cx + r * math.cos(a)) / 2) * 2,
                     round((cy - r * math.sin(a)) / 2) * 2, "line", False))
    write_glyph("asterisk-ar", 576, contours=[star])

    # ـ tatweel / kashida: plain joining bar, no chamfers (it must tile)
    write_glyph("kashida-ar", 320, contours=[[
        (0, 0, "line", False), (320, 0, "line", False),
        (320, 104, "line", False), (0, 104, "line", False)]])

    # separators: small marks in the Unicode chart
    write_glyph("decimalseparator-ar", 256, contours=[bar(80, 0, 176, 128)])
    write_glyph("thousandseparator-ar", 256,
                contours=[bar(80, 512, 176, 640)])
    write_glyph("dateSeparator-ar", 256, contours=[bar(96, 0, 160, 640,
                                                       ch=0)])
    write_glyph("doublestroke-ar", 320, contours=[bar(48, 512, 112, 768,
                                                      ch=0),
                                                  bar(208, 512, 272, 768,
                                                      ch=0)])

    # small high marks
    write_glyph("smallHighTah-ar", 288, contours=[[
        (96, 688, "line", False), (192, 688, "line", False),
        (192, 848, "line", False), (96, 848, "line", False)],
        bar(48, 848, 240, 912, ch=0)])
    write_glyph("smallHighZain-ar", 288, contours=[
        bar(96, 688, 192, 848), bar(112, 880, 176, 944, ch=0)])
    write_glyph("smallHighThreeDots-ar", 464,
                components=[("threedotsupabove-ar", 0, 0)])


def main():
    names = sys.argv[1:]
    digits()
    punctuation()


if __name__ == "__main__":
    main()
