#!/usr/bin/env python3
"""Measure how VIRTUA's own Latin gains weight from Regular to Bold.

The design philosophy says weight comes from counter reduction with the
outer contour often unchanged. This checks that against the sources, so
the Arabic bold pass follows the font's own rule rather than Rubik's.

Usage:
    ./.venv/bin/python scripts/latin_weight_deltas.py
"""

import pathlib
import plistlib
import sys
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
R = REPO / "sources" / "VirtuaGrotesk-Regular.ufo"
B = REPO / "sources" / "VirtuaGrotesk-Bold.ufo"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from rubik_weight_deltas import flatten, runs_h, runs_v, bbox  # noqa: E402


def load(u):
    return plistlib.loads((u / "glyphs" / "contents.plist").read_bytes())


def advance(u, cmap, n):
    a = ET.parse(u / "glyphs" / cmap[n]).getroot().find("advance")
    return float(a.get("width")) if a is not None else 0.0


PROBES = [
    ("n", "h", 300, "lc stem"),
    ("o", "h", 288, "lc round, both sides"),
    ("o", "v", 300, "lc round, top+bottom"),
    ("H", "h", 400, "cap stem"),
    ("H", "v", 300, "cap crossbar"),
    ("E", "v", 300, "cap horizontals"),
    ("l", "h", 400, "lc stem"),
    ("m", "h", 300, "lc stems"),
]

GLYPHS = ["n", "o", "H", "O", "E", "l", "m", "a", "e", "s", "period"]


def main():
    cr, cb = load(R), load(B)

    print("--- STROKE THICKNESS: Virtua Regular vs Bold (Latin) ---")
    print(f"{'glyph / probe':30s} {'Regular':>18s} {'Bold':>18s}  ratio")
    for name, kind, coord, label in PROBES:
        pr, pb = flatten(R, cr, name), flatten(B, cb, name)
        if not pr or not pb:
            continue
        rr = runs_h(pr, coord) if kind == "h" else runs_v(pr, coord)
        rb = runs_h(pb, coord) if kind == "h" else runs_v(pb, coord)
        wr = [b - a for a, b in rr]
        wb = [b - a for a, b in rb]
        if not wr or not wb:
            continue
        mr, mb = min(wr), min(wb)
        print(f"{name + ' ' + label:30s} "
              f"{','.join(f'{w:.0f}' for w in wr[:3]):>18s} "
              f"{','.join(f'{w:.0f}' for w in wb[:3]):>18s}  "
              f"{mb/mr if mr else 0:.2f}")

    print("\n--- OUTER BOUNDS: does the silhouette move? ---")
    print(f"{'glyph':10s} {'Regular bbox':>26s} {'Bold bbox':>26s}   verdict")
    for name in GLYPHS:
        br = bbox(flatten(R, cr, name))
        bb_ = bbox(flatten(B, cb, name))
        if not br or not bb_:
            continue
        same = all(abs(a - b) <= 2 for a, b in zip(br, bb_))
        print(f"{name:10s} "
              f"{f'{br[0]:.0f},{br[1]:.0f}..{br[2]:.0f},{br[3]:.0f}':>26s} "
              f"{f'{bb_[0]:.0f},{bb_[1]:.0f}..{bb_[2]:.0f},{bb_[3]:.0f}':>26s}"
              f"   {'IDENTICAL' if same else 'grows'}")

    print("\n--- ADVANCE GROWTH ---")
    print(f"{'glyph':10s} {'Regular':>8s} {'Bold':>8s}  ratio  delta")
    for name in GLYPHS:
        ar, ab = advance(R, cr, name), advance(B, cb, name)
        if not ar:
            continue
        print(f"{name:10s} {ar:8.0f} {ab:8.0f}  {ab/ar:.3f}  {ab-ar:+.0f}")


if __name__ == "__main__":
    main()
