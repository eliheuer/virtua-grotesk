#!/usr/bin/env python3
"""Anchor-sheet calibration: measure a multi-glyph reference image in font units.

A sheet is an image of glyphs on one baseline that includes at least one
ANCHOR — a glyph that already exists (green) in the sources. The anchor's
known ink-bbox height calibrates px -> font units and locates the baseline,
making the sheet self-calibrating (no --target-height guessing; wrong scale
is the #1 historical cause of bad traces).

    ./.venv/bin/python scripts/anchor_sheet.py SHEET.png n less equal greater
    ./.venv/bin/python scripts/anchor_sheet.py SHEET.png --anchor 1 n ...

Output: calibration + per-glyph boxes and stroke scans, in font units,
as text and JSON (--json FILE). Feed the numbers to scripts/symbol_gen.py
for line-grammar glyphs, or use them as exact --fit values for img2bez on
organic glyphs. Workflow + lessons: .agents/skills/anchor-sheet-glyphs/.
"""
import argparse, json, pathlib, sys

import numpy as np
from PIL import Image

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import grid_qa as gq  # noqa: E402
import normalize_metrics as nm  # noqa: E402


def anchor_bbox_units(glyph, master="Regular"):
    fn = f"{glyph}_.glif" if glyph[0].isupper() else f"{glyph}.glif"
    adv, cont = gq.parse_glyph(str(REPO / f"sources/VirtuaGrotesk-{master}.ufo/glyphs/{fn}"))
    xmin, xmax, ymin, ymax = nm.bbox(nm.ufo_polys(cont))
    return xmin, xmax, ymin, ymax, adv


def segment(ink):
    """Split the sheet into glyph boxes by blank columns; merge x-overlaps."""
    W = ink.shape[1]
    colink = ink.any(axis=0)
    spans, inr = [], False
    for x in range(W):
        if colink[x] and not inr:
            s, inr = x, True
        elif not colink[x] and inr:
            spans.append((s, x - 1)); inr = False
    if inr:
        spans.append((s, W - 1))
    boxes = []
    for x0, x1 in spans:
        ys = np.where(ink[:, x0:x1 + 1].any(axis=1))[0]
        boxes.append((x0, x1, int(ys.min()), int(ys.max())))
    return boxes


def vruns(ink, x, y0, y1, scale):
    """Vertical ink runs at column x, as (thickness_u, center_u_from_top)."""
    col = ink[:, x]
    runs, inr = [], False
    for yy in range(y0, y1 + 1):
        if col[yy] and not inr:
            st, inr = yy, True
        elif not col[yy] and inr:
            runs.append((st, yy - 1)); inr = False
    if inr:
        runs.append((st, y1))
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("names", nargs="+", help="glyph names left to right")
    ap.add_argument("--anchor", type=int, default=0, help="index of the anchor glyph")
    ap.add_argument("--threshold", type=int, default=128)
    ap.add_argument("--json", help="write result JSON here")
    a = ap.parse_args()

    ink = np.array(Image.open(a.sheet).convert("L")) < a.threshold
    boxes = segment(ink)
    if len(boxes) != len(a.names):
        sys.exit(f"segmented {len(boxes)} glyphs but {len(a.names)} names given")

    ax0, ax1, ay0, ay1 = boxes[a.anchor]
    uxmin, uxmax, uymin, uymax, _ = anchor_bbox_units(a.names[a.anchor])
    scale = (uymax - uymin) / (ay1 - ay0)
    base_py = ay1 + uymin / scale  # image y of font baseline (y=0)

    def fu_y(py):
        return round((base_py - py) * scale, 1)

    out = {"sheet": a.sheet, "anchor": a.names[a.anchor], "scale_u_per_px": round(scale, 4),
           "glyphs": {}}
    print(f"anchor {a.names[a.anchor]}: {ay1-ay0}px = {uymax-uymin:.0f}u -> "
          f"scale {scale:.4f} u/px, baseline at py {base_py:.1f}")
    for name, (x0, x1, y0, y1) in zip(a.names, boxes):
        g = {"width_u": round((x1 - x0 + 1) * scale, 1),
             "top_u": fu_y(y0), "bottom_u": fu_y(y1),
             "center_u": round((fu_y(y0) + fu_y(y1)) / 2, 1)}
        cuts = [round((b - c + 1) * scale, 1)
                for c, b in vruns(ink, (x0 + x1) // 2, y0, y1, scale)]
        g["vcuts_mid_u"] = cuts
        out["glyphs"][name] = g
        print(f"  {name:12s} w {g['width_u']:6.1f}  y {g['bottom_u']:6.1f}..{g['top_u']:6.1f}"
              f"  center {g['center_u']:6.1f}  vcuts {cuts}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print("wrote", a.json)


if __name__ == "__main__":
    main()
