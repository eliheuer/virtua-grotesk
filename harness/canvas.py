#!/usr/bin/env python
"""Canvas toolchain for the AI glyph-completion harness — ANALYSIS half.

STATUS: the rendering modes here (template/sheet/ghost) are SUPERSEDED by the
designbot script `harness/designbot/glyph_canvas.rs` (Rust is the house
toolchain — use that for all image *generation*). The active subcommands in
this file are `extract` and `check` (image analysis / source verification),
interim until they are ported to img2bez. Keep the constants here in
lockstep with the designbot script.

One coordinate frame, implemented once, used everywhere. Agents call these
subcommands; they never do pixel<->font-unit math themselves.

Template spec (plans/ai-font-completion-harness.md §4b, revised 2026-07-07):
  1536 x 1536 px, 1 font unit = 1 px.
  Drawing band = 768..-256 (asc/cap ceiling to descender), 256 px margins.
  Metric rows: asc/cap 256, x-height 448, baseline 1024, descender 1280.
  row = MARGIN + (BAND_TOP - y).
  Machine-facing graphics: pure green #00ff00 (chroma-key), ink black,
  ghost light gray. Extraction keeps dark desaturated pixels only.

Subcommands:
  template  Blank template PNG (lines, labels, fiducials).
  sheet     Style sheet: named glyphs from a master UFO at 1:1 on the frame.
  ghost     Target canvas: a sketch/draft registered into a band as a light
            gray ghost + the drawing-band mask for masked edits.
  extract   Pull clean b/w ink out of a generated image; verify fiducials;
            report ink bbox in font units + the exact img2bez --fit band +
            stroke-width estimate vs the master's stem ladder.
  check     Report a source glyph's vertical extents, zones, sidebearings,
            and odd-coordinate count (post-adjust verification).
"""

import argparse
import json
import math
import plistlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import skia
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
SOURCES = REPO / "sources"
MASTERS = {
    "Regular": SOURCES / "VirtuaGrotesk-Regular.ufo",
    "Bold": SOURCES / "VirtuaGrotesk-Bold.ufo",
}
# Per DESIGN.md "Dimensions": x-height stems 96 (Regular) / 192 (Bold).
STEM_LADDER = {"Regular": 96, "Bold": 192}

W, H, MARGIN = 1536, 1536, 256
# Ascender (832) is capped to the 768 ceiling on the template (square canvas,
# no VG glyph draws above cap). Keep both names resolvable for band specs.
BAND_TOP = 768
CAP, XHEIGHT, BASELINE, DESCENDER = 768, 576, 0, -256
ASCENDER = BAND_TOP
ZONES = {
    "ascender": BAND_TOP,
    "cap": CAP,
    "xheight": XHEIGHT,
    "baseline": BASELINE,
    "descender": DESCENDER,
}
GREEN = (0, 255, 0)
GHOST_GRAY = (200, 200, 200)
FIDUCIAL = 16


def unit_to_row(y: float) -> float:
    return MARGIN + (BAND_TOP - y)


def row_to_unit(row: float) -> float:
    return BAND_TOP - (row - MARGIN)


def parse_band(spec: str):
    """'baseline:cap' or '-16:784' -> (y_lo, y_hi) in font units."""
    lo, hi = spec.split(":")
    lo = ZONES.get(lo, None) if not _is_num(lo) else float(lo)
    hi = ZONES.get(hi, None) if not _is_num(hi) else float(hi)
    if lo is None or hi is None:
        sys.exit(f"bad band spec {spec!r}: use zone names {list(ZONES)} or numbers")
    return (min(lo, hi), max(lo, hi))


def _is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------- glif I/O

def glif_path(master: str, glyph: str) -> Path:
    ufo = MASTERS[master]
    contents = plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())
    if glyph not in contents:
        sys.exit(f"{glyph!r} not in {master} contents.plist")
    return ufo / "glyphs" / contents[glyph]


def load_glyph(master: str, glyph: str, _depth=0):
    """-> (advance_width, contours, mark_color). Components resolved flat.

    A contour is a list of (x, y, type) with type in {move,line,curve,offcurve}.
    """
    if _depth > 4:
        sys.exit(f"component nesting too deep at {glyph!r}")
    root = ET.parse(glif_path(master, glyph)).getroot()
    adv = root.find("advance")
    width = float(adv.get("width", 0)) if adv is not None else 0.0
    contours = []
    outline = root.find("outline")
    if outline is not None:
        for el in outline:
            if el.tag == "contour":
                pts = [
                    (
                        float(p.get("x")),
                        float(p.get("y")),
                        p.get("type", "offcurve"),
                    )
                    for p in el.findall("point")
                ]
                if pts:
                    contours.append(pts)
            elif el.tag == "component":
                base = el.get("base")
                xs = float(el.get("xScale", 1))
                xy = float(el.get("xyScale", 0))
                yx = float(el.get("yxScale", 0))
                ys = float(el.get("yScale", 1))
                dx = float(el.get("xOffset", 0))
                dy = float(el.get("yOffset", 0))
                _, sub, _ = load_glyph(master, base, _depth + 1)
                for c in sub:
                    contours.append(
                        [
                            (x * xs + y * yx + dx, x * xy + y * ys + dy, t)
                            for (x, y, t) in c
                        ]
                    )
    mark = None
    for key in root.iter("key"):
        if key.text == "public.markColor":
            nxt = key.getnext() if hasattr(key, "getnext") else None
    # ElementTree lacks getnext(); walk lib dict pairwise instead.
    lib = root.find("lib")
    if lib is not None:
        d = lib.find("dict")
        if d is not None:
            kids = list(d)
            for i, el in enumerate(kids):
                if el.tag == "key" and el.text == "public.markColor":
                    if i + 1 < len(kids):
                        mark = (kids[i + 1].text or "").strip()
    return width, contours, mark


def contours_to_skia(contours, x_origin_px: float) -> skia.Path:
    """Build a y-flipped skia path on the template frame."""
    path = skia.Path()
    for pts in contours:
        # rotate so we start on an on-curve point
        start = next((i for i, p in enumerate(pts) if p[2] != "offcurve"), None)
        if start is None:
            continue  # all-offcurve (TrueType style) not expected here
        seq = pts[start:] + pts[:start]
        x0, y0, _ = seq[0]
        path.moveTo(x_origin_px + x0, unit_to_row(y0))
        pending = []
        for x, y, t in seq[1:] + [seq[0]]:
            px, py = x_origin_px + x, unit_to_row(y)
            if t == "offcurve":
                pending.append((px, py))
            elif t == "line":
                path.lineTo(px, py)
                pending = []
            else:  # curve / qcurve / move-as-line
                if len(pending) == 2:
                    path.cubicTo(*pending[0], *pending[1], px, py)
                elif len(pending) == 0:
                    path.lineTo(px, py)
                else:
                    sys.exit(f"unsupported segment ({len(pending)} offcurves)")
                pending = []
        path.close()
    path.setFillType(skia.PathFillType.kWinding)
    return path


def rasterize(paths, width, height):
    """skia paths -> boolean ink mask (True where ink)."""
    surface = skia.Surface(width, height)
    canvas = surface.getCanvas()
    canvas.clear(skia.Color4f(0, 0, 0, 0))
    paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)
    paint.setStyle(skia.Paint.kFill_Style)
    for p in paths:
        canvas.drawPath(p, paint)
    arr = surface.makeImageSnapshot().toarray()  # H x W x 4 (BGRA/RGBA)
    return arr[:, :, 3] > 127


# ------------------------------------------------------------- frame paint

def paint_frame(img: Image.Image, label=True):
    d = ImageDraw.Draw(img)
    w = img.width
    for name, y in ZONES.items():
        row = unit_to_row(y)
        d.line([(0, row), (w, row)], fill=GREEN, width=2)
        if label:
            short = {"ascender": "asc", "descender": "desc"}.get(name, name)
            d.text((40, row - 16), short, fill=GREEN)
    for fx in (8, w - FIDUCIAL - 8):
        for fy in (8, H - FIDUCIAL - 8):
            d.rectangle([fx, fy, fx + FIDUCIAL, fy + FIDUCIAL], fill=GREEN)


def blank_template(width=W) -> Image.Image:
    img = Image.new("RGB", (width, H), "white")
    paint_frame(img)
    return img


def stamp_ink(img: Image.Image, mask: np.ndarray, color=(0, 0, 0)):
    arr = np.array(img)
    arr[mask] = color
    return Image.fromarray(arr)


# ------------------------------------------------------------- subcommands

def cmd_template(args):
    blank_template().save(args.out)
    print(f"template -> {args.out}")


def cmd_sheet(args):
    names = [g.strip() for g in args.glyphs.split(",") if g.strip()]
    gap, x = 48, 64.0
    entries = []
    for name in names:
        width, contours, mark = load_glyph(args.master, name)
        if mark != "0.09,0.72,0.44,1":
            print(f"warning: {name} is not marked green (markColor={mark})",
                  file=sys.stderr)
        entries.append((name, x, width, contours))
        x += width + gap
    sheet_w = int(math.ceil(x + 64 - gap))
    paths = [contours_to_skia(c, xo) for (_, xo, _, c) in entries]
    ink = rasterize(paths, sheet_w, H)
    img = Image.new("RGB", (sheet_w, H), "white")
    paint_frame(img)
    img = stamp_ink(img, ink)
    img.save(args.out)
    print(f"style sheet ({args.master}: {', '.join(names)}) -> {args.out}")


def cmd_ghost(args):
    src = Image.open(args.image).convert("L")
    a = np.array(src)
    ink = a < 128
    if not ink.any():
        sys.exit("no dark pixels found in sketch image")
    rows = np.any(ink, axis=1)
    cols = np.any(ink, axis=0)
    top, bot = np.argmax(rows), len(rows) - np.argmax(rows[::-1]) - 1
    left, right = np.argmax(cols), len(cols) - np.argmax(cols[::-1]) - 1
    crop = ink[top : bot + 1, left : right + 1]

    y_lo, y_hi = parse_band(args.band)
    band_px = y_hi - y_lo  # 1 unit = 1 px
    scale = band_px / crop.shape[0]
    new_w = max(1, int(round(crop.shape[1] * scale)))
    ghost = np.array(
        Image.fromarray((crop * 255).astype(np.uint8)).resize(
            (new_w, int(band_px)), Image.LANCZOS
        )
    ) > 127

    row_top = int(unit_to_row(y_hi))
    col_left = int(round((W - new_w) / 2))
    img = blank_template()
    arr = np.array(img)
    region = arr[row_top : row_top + ghost.shape[0],
                 col_left : col_left + ghost.shape[1]]
    region[ghost] = GHOST_GRAY
    arr[row_top : row_top + ghost.shape[0],
        col_left : col_left + ghost.shape[1]] = region
    Image.fromarray(arr).save(args.out)

    mask = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    md = ImageDraw.Draw(mask)
    md.rectangle([32, MARGIN, W - 32, H - MARGIN], fill=(0, 0, 0, 0))
    mask.save(args.mask)
    print(json.dumps({
        "ghost": args.out, "mask": args.mask,
        "band_units": [y_lo, y_hi],
        "ghost_px": {"rowTop": row_top, "colLeft": col_left,
                     "w": int(new_w), "h": int(band_px)},
    }, indent=2))


def measure_stroke(ink: np.ndarray):
    """Median black-run length across rows in the drawing band (px=units)."""
    runs = []
    for r in range(MARGIN + 32, H - MARGIN - 32, 8):
        row = ink[r]
        n = 0
        for v in row:
            if v:
                n += 1
            elif n:
                if 12 <= n <= 300:
                    runs.append(n)
                n = 0
        if n and 12 <= n <= 300:
            runs.append(n)
    return float(np.median(runs)) if runs else None


def cmd_extract(args):
    img = Image.open(args.image).convert("RGB")
    if img.size != (W, H):
        print(f"warning: generated image is {img.size}, resizing to {(W, H)}",
              file=sys.stderr)
        img = img.resize((W, H), Image.LANCZOS)
    arr = np.array(img).astype(np.int16)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mx, mn = arr.max(axis=2), arr.min(axis=2)
    saturated = (mx - mn) > 60
    dark = mx < 128
    ink = dark & ~saturated

    fid_ok = []
    for fx in (8, W - FIDUCIAL - 8):
        for fy in (8, H - FIDUCIAL - 8):
            patch_g = g[fy : fy + FIDUCIAL, fx : fx + FIDUCIAL]
            patch_r = r[fy : fy + FIDUCIAL, fx : fx + FIDUCIAL]
            fid_ok.append(bool(((patch_g > 180) & (patch_r < 120)).mean() > 0.5))

    out = Image.new("L", (W, H), 255)
    out_arr = np.array(out)
    out_arr[ink] = 0
    Image.fromarray(out_arr).save(args.out)

    report = {"ink": args.out, "fiducials_ok": fid_ok,
              "fiducials_pass": all(fid_ok)}
    if ink.any():
        rows = np.any(ink, axis=1)
        cols = np.any(ink, axis=0)
        top = int(np.argmax(rows))
        bot = int(len(rows) - np.argmax(rows[::-1]) - 1)
        left = int(np.argmax(cols))
        right = int(len(cols) - np.argmax(cols[::-1]) - 1)
        y_hi, y_lo = row_to_unit(top), row_to_unit(bot)
        stroke = measure_stroke(ink)
        expected = STEM_LADDER.get(args.master)
        report.update({
            "ink_bbox_px": [left, top, right, bot],
            "ink_units": {"yMin": y_lo, "yMax": y_hi,
                          "xMin": left, "xMax": right,
                          "width": right - left, "height": y_hi - y_lo},
            "fit_band": f"{y_lo:g}:{y_hi:g}",
            "img2bez_fit_flag": f"--fit {y_lo:g}:{y_hi:g}",
            "stroke_px": stroke,
            "expected_stem": expected,
        })
        if stroke and expected:
            dev = (stroke - expected) / expected
            report["stroke_deviation"] = round(dev, 3)
            report["stroke_pass"] = bool(abs(dev) <= 0.15)
            if not report["stroke_pass"]:
                pct = int(round(abs(dev) * 100))
                fix = "thicker" if dev < 0 else "thinner"
                report["correction_prompt"] = (
                    f"same glyph, same skeleton, strokes ~{pct}% {fix}"
                )
    else:
        report["error"] = "no ink found after keying"
    print(json.dumps(report, indent=2))
    if not report.get("fiducials_pass") or report.get("stroke_pass") is False:
        sys.exit(2)


def cmd_check(args):
    width, contours, mark = load_glyph(args.master, args.glyph)
    pts = [(x, y) for c in contours for (x, y, t) in c]
    if not pts:
        print(json.dumps({"glyph": args.glyph, "master": args.master,
                          "empty": True, "advance": width}))
        return
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    y_min, y_max = min(ys), max(ys)
    x_min, x_max = min(xs), max(xs)
    odd = sum(1 for x, y in pts if x % 2 or y % 2)

    def near(v):
        hits = [(n, z) for n, z in ZONES.items() if abs(v - z) <= 20]
        over = [(n + "+overshoot", z) for n, z in ZONES.items()
                if abs(abs(v - z) - 16) <= 4]
        return hits + over

    print(json.dumps({
        "glyph": args.glyph, "master": args.master, "advance": width,
        "markColor": mark,
        "yMin": y_min, "yMax": y_max,
        "yMin_near": [n for n, _ in near(y_min)],
        "yMax_near": [n for n, _ in near(y_max)],
        "lsb": x_min, "rsb": width - x_max,
        "odd_coordinates": odd,
        "zones": ZONES,
    }, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("template", help="blank canvas template")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_template)

    p = sub.add_parser("sheet", help="style sheet from master glyphs")
    p.add_argument("--master", choices=MASTERS, required=True)
    p.add_argument("--glyphs", required=True,
                   help="comma-separated glyph names (green references)")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_sheet)

    p = sub.add_parser("ghost", help="target canvas + mask from a sketch")
    p.add_argument("--image", required=True, help="shape-intent image")
    p.add_argument("--band", required=True,
                   help="vertical band, e.g. baseline:cap or -16:784")
    p.add_argument("--out", required=True, help="target canvas PNG")
    p.add_argument("--mask", required=True, help="mask PNG (RGBA)")
    p.set_defaults(fn=cmd_ghost)

    p = sub.add_parser("extract", help="ink + gates from a generated image")
    p.add_argument("--image", required=True)
    p.add_argument("--master", choices=MASTERS, required=True)
    p.add_argument("--out", required=True, help="clean b/w ink PNG")
    p.set_defaults(fn=cmd_extract)

    p = sub.add_parser("check", help="verify a source glyph's metrics")
    p.add_argument("--glyph", required=True)
    p.add_argument("--master", choices=MASTERS, required=True)
    p.set_defaults(fn=cmd_check)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
