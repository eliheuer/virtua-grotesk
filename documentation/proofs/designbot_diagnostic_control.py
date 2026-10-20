#!/usr/bin/env python3
"""Freeze old Pillow captions as controls for designbot_diagnostic.rs."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--font', type=Path, required=True)
p.add_argument('--output-dir', type=Path, required=True)
a = p.parse_args()
a.output_dir.mkdir(parents=True, exist_ok=True)
lines = [('Individual Glyphs / Equal Em Scale', 40, 20),
         ('Equal Em Scale And Baseline', 80, 18), ('E I H T / E I H T', 160, 40)]
for mode, paper, ink in [('light', '#dedede', '#444444'), ('dark', '#444444', '#dedede')]:
    im = Image.new('RGBA', (640, 200), paper)
    draw = ImageDraw.Draw(im)
    for text, baseline, size in lines:
        font = ImageFont.truetype(str(a.font), size, index=0)
        draw.text((0, baseline), text, font=font, fill=ink, anchor='ls')
    (a.output_dir / f'pillow-{mode}.rgba').write_bytes(im.tobytes())
    im.save(a.output_dir / f'pillow-{mode}.png')
metrics = {str(size): {c: ImageFont.truetype(str(a.font), size, index=0).getbbox(c, anchor='ls')
                      for c in 'EIHT'} for size in [18, 20, 40]}
manifest = {'font': str(a.font.resolve()), 'font_sha256': hashlib.sha256(a.font.read_bytes()).hexdigest(),
            'face': ImageFont.truetype(str(a.font), 20, index=0).getname(), 'pillow': pillow_version,
            'lines': lines, 'bounds': metrics, 'palette': ['#dedede', '#444444']}
(a.output_dir / 'control.json').write_text(json.dumps(manifest, indent=2) + '\n')
