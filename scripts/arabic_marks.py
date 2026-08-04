#!/usr/bin/env python3
"""Small-mark constructions (harakat, dot clusters, hamza) for the Arabic
completion pass. Same conventions as arabic_skeletons.py: written to both
masters, marked blue.

Zones (from the green set): dot-above band 688..848, dot-below -272..-112,
hamza-above 832..1024.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import write_glyph, read_points  # noqa: E402


def rect(x0, y0, x1, y1, ch=0):
    """Rectangle, optionally with chamfered corners."""
    if not ch:
        return [(x0, y0, "line", False), (x1, y0, "line", False),
                (x1, y1, "line", False), (x0, y1, "line", False)]
    return [(x0 + ch, y0, "line", False), (x1 - ch, y0, "line", False),
            (x1, y0 + ch, "line", False), (x1, y1 - ch, "line", False),
            (x1 - ch, y1, "line", False), (x0 + ch, y1, "line", False),
            (x0, y1 - ch, "line", False), (x0, y0 + ch, "line", False)]


def parallelogram(x0, y0, dx, dy, thickness):
    """Slanted bar from (x0,y0) rising dx,dy with vertical thickness."""
    return [(x0, y0, "line", False), (x0 + dx, y0 + dy, "line", False),
            (x0 + dx, y0 + dy + thickness, "line", False),
            (x0, y0 + thickness, "line", False)]


def scaled(contours, s, tx, ty):
    out = []
    for c in contours:
        out.append([(round((x * s + tx) / 2) * 2, round((y * s + ty) / 2) * 2,
                     t, sm) for x, y, t, sm in c])
    return out


def translated(contours, tx, ty):
    return [[(x + tx, y + ty, t, s) for x, y, t, s in c] for c in contours]


def flipped_y(contours, about):
    """Mirror vertically about y=about, reversing point order per contour."""
    out = []
    for c in contours:
        pts = [(x, 2 * about - y, t, s) for x, y, t, s in c]
        # reverse via segment-aware reversal
        from arabic_build import reverse_contour
        out.append(reverse_contour(pts))
    return out


def build_all():
    # --- slanted bars -----------------------------------------------------
    write_glyph("fatha-ar", 224,
                contours=[parallelogram(0, 704, 224, 64, 72)])
    write_glyph("kasra-ar", 224,
                contours=[parallelogram(0, -240, 224, 64, 72)])

    # --- madda: flat wide bar with slanted ends ---------------------------
    write_glyph("madda-ar", 288, contours=[[
        (32, 712, "line", False), (288, 712, "line", False),
        (256, 776, "line", False), (0, 776, "line", False)]])

    # --- sukun: small ring ------------------------------------------------
    def ring(cx, cy, r_out, r_in):
        h_out = round(0.55 * r_out)
        h_in = round(0.55 * r_in)
        outer = [(cx, cy + r_out, "curve", True),
                 (cx + h_out, cy + r_out, None, False),
                 (cx + r_out, cy + h_out, None, False),
                 (cx + r_out, cy, "curve", True),
                 (cx + r_out, cy - h_out, None, False),
                 (cx + h_out, cy - r_out, None, False),
                 (cx, cy - r_out, "curve", True),
                 (cx - h_out, cy - r_out, None, False),
                 (cx - r_out, cy - h_out, None, False),
                 (cx - r_out, cy, "curve", True),
                 (cx - r_out, cy + h_out, None, False),
                 (cx - h_out, cy + r_out, None, False)]
        inner = [(cx, cy + r_in, "curve", True),
                 (cx - h_in, cy + r_in, None, False),
                 (cx - r_in, cy + h_in, None, False),
                 (cx - r_in, cy, "curve", True),
                 (cx - r_in, cy - h_in, None, False),
                 (cx - h_in, cy - r_in, None, False),
                 (cx, cy - r_in, "curve", True),
                 (cx + h_in, cy - r_in, None, False),
                 (cx + r_in, cy - h_in, None, False),
                 (cx + r_in, cy, "curve", True),
                 (cx + r_in, cy + h_in, None, False),
                 (cx + h_in, cy + r_in, None, False)]
        return [outer, inner]

    write_glyph("sukun-ar", 224, contours=ring(112, 768, 80, 28))

    # --- shadda: mini sheen comb -----------------------------------------
    write_glyph("shadda-ar", 224, contours=[[
        (0, 688, "line", False), (224, 688, "line", False),
        (224, 848, "line", False), (184, 848, "line", False),
        (184, 744, "line", False), (132, 744, "line", False),
        (132, 848, "line", False), (92, 848, "line", False),
        (92, 744, "line", False), (40, 744, "line", False),
        (40, 848, "line", False), (0, 848, "line", False)]])

    # --- wasla: small flat loop (mini sad head) ---------------------------
    wasla = ring(112, 760, 88, 32)
    # squash horizontally into a flat oval look by widening: keep simple ring
    write_glyph("wasla-ar", 224, contours=wasla)

    # --- damma: scaled waw ------------------------------------------------
    waw = read_points("waw-ar")
    write_glyph("damma-ar", 320, contours=scaled(waw, 0.5, 128, 788))
    # flip about the damma's own vertical centre so it keeps the same band
    write_glyph("invertedDamma-ar", 320,
                contours=flipped_y(scaled(waw, 0.5, 128, 788), 826))

    # --- hamza isolated: scaled hamzaabove on the baseline ----------------
    hz = read_points("hamzaabove-ar")
    write_glyph("hamza-ar", 400, contours=scaled(hz, 1.6, 20, -1331))

    # --- alef miniatures --------------------------------------------------
    write_glyph("alefabove-ar", 224, contours=[rect(88, 688, 136, 880)])
    write_glyph("alefbelow-ar", 224, contours=[rect(88, -304, 136, -112)])

    # --- dot clusters from the green dots ---------------------------------
    dotA = read_points("dotabove-ar")     # 72..232 x, 688..848 y
    dotB = read_points("dotbelow-ar")     # 40..200 x, -272..-112 y
    threeup = read_points("threedotsupabove-ar")

    twoup = read_points("twodotshorizontalabove-ar")
    write_glyph("twodotshorizontalbelow-ar", 304,
                contours=translated(twoup, 0, -960))
    write_glyph("twodotsverticalabove-ar", 304,
                contours=translated(dotA, 0, -64) + translated(dotA, 0, 128))
    # stacked below-dots must fit the -438 WinDescent envelope, so the pair
    # is tightened rather than using two full band offsets
    write_glyph("twodotsverticalbelow-ar", 240,
                contours=translated(dotB, 0, 16) + translated(dotB, 0, -160))
    down3 = flipped_y(threeup, 840)
    write_glyph("threedotsdownabove-ar", 464, contours=down3)
    write_glyph("threedotsdownbelow-ar", 464,
                contours=translated(down3, 0, -1092))
    write_glyph("threedotsdowncenter-ar", 464,
                contours=translated(down3, 0, -560))
    write_glyph("threedotsupbelow-ar", 464,
                contours=translated(threeup, 0, -1092))
    write_glyph("dotcenter-ar", 304, contours=translated(dotA, 0, -488))

    # --- gaf sarkash marks (from green kaf-ar.fina) -----------------------
    sark = read_points("kaf-ar.fina")[1:2]
    write_glyph("gafsarkashabove-ar", 304,
                contours=scaled(sark, 0.75, -178, 408))
    write_glyph("gafsarkashcenter-ar", 304,
                contours=scaled(sark, 0.75, -178, 32))
    write_glyph("miniKeheh-ar", 304, contours=scaled(sark, 0.75, -178, 408))

    # --- noonGhunna isolated (U+06BA) = noon cup, no dot ------------------
    write_glyph("noonGhunna-ar", 680,
                components=[("noonghunna-ar", 0, 0)])


if __name__ == "__main__":
    build_all()
