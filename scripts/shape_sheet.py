#!/usr/bin/env python3
"""Render lines of shaped text into one review sheet.

hb-view does the shaping and rasterising, so what you see is what HarfBuzz
produces from the built font — features, mark attachment and all. This just
stacks the lines with labels.

Usage:
    ./.venv/bin/python scripts/shape_sheet.py OUT.png [--font PATH] [--size N] \\
        "label::text" "label::text" ...
"""

import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

BG = (26, 26, 26)
INK = "CCCCCC"
LABEL = (120, 120, 120)
PAD = 28
LABEL_W = 190

LABEL_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def label_font(size=17):
    for p in LABEL_FONT_CANDIDATES:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def render_line(font_path, text, size, tmpdir, i):
    out = pathlib.Path(tmpdir) / f"line{i}.png"
    subprocess.run(
        ["hb-view", f"--font-file={font_path}", f"--font-size={size}",
         "--margin=10", f"--output-file={out}", f"--foreground={INK}",
         "--background=1A1A1A", text],
        check=True, capture_output=True)
    return Image.open(out).convert("RGB")


def main():
    args = [a for a in sys.argv[1:]]
    out_path = args.pop(0)
    font = "fonts/ttf/VirtuaGrotesk-Regular.ttf"
    size = 120
    while args and args[0].startswith("--"):
        flag = args.pop(0)
        if flag == "--font":
            font = args.pop(0)
        elif flag == "--size":
            size = int(args.pop(0))
    lines = [a.split("::", 1) if "::" in a else ("", a) for a in args]

    with tempfile.TemporaryDirectory() as td:
        imgs = [(lab, render_line(font, txt, size, td, i))
                for i, (lab, txt) in enumerate(lines)]
        w = max(im.width for _, im in imgs) + LABEL_W + PAD * 2
        h = sum(im.height for _, im in imgs) + PAD * (len(imgs) + 1)
        sheet = Image.new("RGB", (w, h), BG)
        d = ImageDraw.Draw(sheet)
        f = label_font()
        y = PAD
        for lab, im in imgs:
            # lines are right-aligned: Arabic reads from the right edge
            sheet.paste(im, (w - PAD - im.width, y))
            if lab:
                d.text((PAD, y + im.height // 2 - 9), lab, fill=LABEL, font=f)
            y += im.height + PAD
        sheet.save(out_path)
    print(f"wrote {out_path} ({w}x{h})")


if __name__ == "__main__":
    sys.exit(main())
