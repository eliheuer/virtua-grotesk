#!/usr/bin/env python3
"""Lane-2 derivations: glyphs obtained from an existing (usually green)
donor by copying, splicing off a joining bar, or reusing a sibling form.

Every derivation is a deterministic edit on donor points, so both masters
stay structurally identical by construction.

Usage:
    ./.venv/bin/python scripts/arabic_derive.py [names...]
"""

import sys
import pathlib
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import write_glyph, read_points, glif_path, MASTERS  # noqa

UFO = MASTERS[0]


def anchors_of(name):
    root = ET.parse(glif_path(UFO, name)).getroot()
    return [(a.get("name"), float(a.get("x")), float(a.get("y")))
            for a in root.iter("anchor")]


def idx(contour, x, y):
    for i, p in enumerate(contour):
        if p[0] == x and p[1] == y:
            return i
    raise ValueError(f"({x},{y}) not found")


# --- heh-goal / doachashmee ------------------------------------------------

def _goal_isol(donor, out, advance):
    """Isolated 'a'-form: drop the right entry bar, close the bowl."""
    cs = read_points(donor)
    body = next(c for c in cs if len(c) > 20)
    other = [c for c in cs if c is not body]
    i_bowl = idx(body, 224, 0)        # bottom of the bowl
    i_up = idx(body, 416, 208)        # right wall, above the bar
    c = body[:i_bowl + 1] + [
        (332, 0, None, False),
        (416, 90, None, False),
        (416, 208, "curve", True),
    ] + body[i_up + 1:]
    write_glyph(out, advance, contours=[c] + other,
                anchors=[("top", 224, 432), ("bottom", 224, -16)])


def _goal_init(donor, out, advance):
    """Initial two-story form: medial minus the right entry bar."""
    cs = read_points(donor)
    body = max(cs, key=len)
    other = [c for c in cs if c is not body]
    i_exit = idx(body, 432, -8)       # lower loop leaves here
    i_rise = idx(body, 432, 176)      # right wall control, above the bar
    c = body[:i_exit + 1] + [(432, 60, None, False)] + body[i_rise:]
    write_glyph(out, advance, contours=[c] + other,
                anchors=[("top", 248, 464), ("bottom", 248, -312)])


def build_hehGoal_isol():
    _goal_isol("hehGoal-ar.fina", "hehGoal-ar", 448)


def build_hehGoal_init():
    _goal_init("hehGoal-ar.medi", "hehGoal-ar.init", 464)


def build_hehDoachashmee_isol():
    _goal_isol("hehDoachashmee-ar.fina", "hehDoachashmee-ar", 448)


def build_hehDoachashmee_init():
    _goal_init("hehDoachashmee-ar.medi", "hehDoachashmee-ar.init", 464)


# --- simple copies ---------------------------------------------------------

def copy_of(src, out, advance=None, contours_slice=None):
    root = ET.parse(glif_path(UFO, src)).getroot()
    adv = advance if advance is not None else float(
        root.find("advance").get("width"))
    cs = read_points(src)
    if contours_slice is not None:
        cs = cs[contours_slice]
    write_glyph(out, adv, contours=cs, anchors=anchors_of(src))


DERIVATIONS = {
    "hehGoal-ar": build_hehGoal_isol,
    "hehGoal-ar.init": build_hehGoal_init,
    "hehDoachashmee-ar": build_hehDoachashmee_isol,
    "hehDoachashmee-ar.init": build_hehDoachashmee_init,
    # dotless yeh teeth: identical to the beh tooth
    "alefMaksura-ar.init": lambda: copy_of("behDotless-ar.init",
                                           "alefMaksura-ar.init"),
    "alefMaksura-ar.medi": lambda: copy_of("behDotless-ar.medi",
                                           "alefMaksura-ar.medi"),
    # the tehRing ring part: reuse the sukun ring, sized for a dot slot
    "ring-ar": lambda: copy_of("sukun-ar", "ring-ar"),
}


def main():
    names = sys.argv[1:] or list(DERIVATIONS)
    for n in names:
        DERIVATIONS[n]()


if __name__ == "__main__":
    main()
