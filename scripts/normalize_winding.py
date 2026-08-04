#!/usr/bin/env python3
"""Normalize contour winding on the blue (AI-authored) Arabic glyphs:
outer contours counter-clockwise, holes clockwise, by nesting parity.

This is the repo convention and what the Google Fonts `outline_direction`
check expects after the UFO -> TTF direction flip. It is a purely
mechanical edit: the rendered shape does not change.

By default it only touches BLUE glyphs, so green (Eli-approved) sources
are left exactly as they are — several of those are CW today, which is a
separate decision for Eli (see documentation/source/arabic-grammar.md).

Usage:
    ./.venv/bin/python scripts/normalize_winding.py [--check] [glyph ...]
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import MASTERS, BLUE, reverse_contour, contour_xml  # noqa

SAMPLES = 24


def sample(contour):
    """Polygon approximation of a contour (on-curve points plus sampled
    cubics) for area and containment tests."""
    pts = [(x, y) for x, y, t, s in contour]
    return pts


def area(contour):
    p = sample(contour)
    return sum(x0 * y1 - x1 * y0
               for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1])) / 2


def inside(pt, poly):
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y):
            xt = x0 + (y - y0) / (y1 - y0) * (x1 - x0)
            if x < xt:
                hit = not hit
    return hit


def depth_of(i, contours):
    """How many other contours contain this one. ALL on-curve points must
    be inside (a single probe misreads overlapping shapes)."""
    probe = [(x, y) for x, y, t, s in contours[i] if t]
    d = 0
    for j, other in enumerate(contours):
        if j == i:
            continue
        poly = sample(other)
        if probe and all(inside(p, poly) for p in probe):
            d += 1
    return d


def process(path, check_only):
    text = path.read_text()
    root = ET.fromstring(text)
    contours = []
    for c in root.iter("contour"):
        contours.append([(float(p.get("x")), float(p.get("y")),
                          p.get("type"), p.get("smooth") == "yes")
                         for p in c.iter("point")])
    if not contours:
        return None
    fixed, changed = [], False
    for i, c in enumerate(contours):
        want_ccw = depth_of(i, contours) % 2 == 0
        is_ccw = area(c) > 0
        if is_ccw != want_ccw:
            fixed.append(reverse_contour(c))
            changed = True
        else:
            fixed.append(c)
    if not changed or check_only:
        return changed
    # splice the rebuilt contours back into the original XML text so the
    # rest of the file (anchors, lib, unicodes) is untouched
    blocks = re.findall(r"\t\t<contour>.*?\t\t</contour>", text, re.S)
    assert len(blocks) == len(fixed), f"{path}: contour block mismatch"
    for old, new in zip(blocks, fixed):
        text = text.replace(old, contour_xml(new), 1)
    path.write_text(text)
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv
    touched = []
    for m in MASTERS:
        cmap = plistlib.loads(
            (m / "glyphs" / "contents.plist").read_bytes())
        for name, fn in sorted(cmap.items()):
            if args and name not in args:
                continue
            path = m / "glyphs" / fn
            body = path.read_text()
            if BLUE not in body:
                continue          # green / red / untouched: leave alone
            if process(path, check_only):
                touched.append(f"{m.name.split('-')[-1][:-4]} {name}")
    verb = "would fix" if check_only else "fixed"
    print(f"{verb} winding on {len(touched)} glyph files")
    for t in touched[:40]:
        print("  " + t)
    if len(touched) > 40:
        print(f"  ... and {len(touched) - 40} more")


if __name__ == "__main__":
    main()
