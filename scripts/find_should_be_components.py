#!/usr/bin/env python3
"""Find glyphs that draw a shape another glyph already owns.

yeh-ar.init drew its own tooth instead of placing behDotless-ar.init. Same
point count, same advance, but the tooth had drifted to 304 where beh's is
432 — a copy that stopped tracking its original, and nothing to say so. A
component would have made that impossible.

Two kinds of finding:

  EXACT     identical contours to another glyph, drawn rather than placed.
            Harmless today, drifts tomorrow.
  CONTAINS  a glyph whose contours include another glyph's whole outline,
            plus more — the classic base + dots that never became a composite.

Detecting drift — a copy whose coordinates have wandered — was tried and
removed. Matching on outline similarity pairs every round thing in the font
with every other round thing across three scripts, and still missed
yeh-ar.init. Exact matches are worth acting on; near matches are not evidence.

Usage:
    ./.venv/bin/python scripts/find_should_be_components.py [--master Regular]
"""

import pathlib
import plistlib
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def contours_of(root):
    """Each contour as a tuple of (x, y, type), so it can be compared."""
    out = []
    for contour in root.iter("contour"):
        pts = tuple(
            (float(p.get("x")), float(p.get("y")), p.get("type") or "off")
            for p in contour.iter("point")
        )
        if pts:
            out.append(pts)
    return out


def structure(contour):
    """Point count and types — what has to match for two contours to be the
    same drawing at different coordinates."""
    return tuple(t for _, _, t in contour)


def canonical(contour):
    """Rotations of a closed contour are the same shape; compare the smallest."""
    n = len(contour)
    return min(tuple(contour[i:] + contour[:i]) for i in range(n))


def main():
    master = "Regular"
    if "--master" in sys.argv:
        master = sys.argv[sys.argv.index("--master") + 1]
    ufo = pathlib.Path(f"sources/VirtuaGrotesk-{master}.ufo")
    cmap = plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())

    drawn = {}
    for name, fn in cmap.items():
        root = ET.parse(ufo / "glyphs" / fn).getroot()
        cs = contours_of(root)
        if cs:
            drawn[name] = cs

    by_canonical = defaultdict(list)
    by_structure = defaultdict(list)
    for name, cs in drawn.items():
        for c in cs:
            by_canonical[canonical(c)].append(name)
            by_structure[structure(c)].append((name, canonical(c)))

    exact, contains = [], []

    # a glyph drawn identically to another, or containing another whole
    for name, cs in sorted(drawn.items()):
        mine = {canonical(c) for c in cs}
        for other, ocs in drawn.items():
            if other == name or len(ocs) > len(cs):
                continue
            theirs = {canonical(c) for c in ocs}
            if not theirs <= mine:
                continue
            if len(theirs) == len(mine):
                if name < other:
                    exact.append((name, other))
            else:
                contains.append((name, other, len(mine) - len(theirs)))

    print(f"{master}: {len(drawn)} glyphs with drawn contours\n")
    print(f"EXACT — drawn identically to another glyph ({len(exact)}):")
    for a, b in exact[:20]:
        print(f"   {a:28s} == {b}")
    print(f"\nCONTAINS — draws another glyph whole, plus {'{n}'} more contours "
          f"({len(contains)}):")
    for a, b, n in sorted(contains)[:20]:
        print(f"   {a:28s} contains {b:24s} (+{n})")


if __name__ == "__main__":
    sys.exit(main())
