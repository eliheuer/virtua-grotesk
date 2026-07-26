#!/usr/bin/env python3
"""Render Virtua vs a shipped reference (Rubik) for the accented set, stacked,
so we can match Rubik's diacritic placement -- Rubik is our GF-onboarding
reference (Latin/Hebrew/Cyrillic/Arabic, proper anchors). This is the interim
visual compare until diffenator2 proof is fully wired (see
DEVELOPMENT_QA_CHECKLIST.md). Usage: python scripts/compare_diacritics.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

VIRTUA = "fonts/ttf/VirtuaGrotesk-Regular.ttf"
RUBIK = "/Users/eli/GH/repos/google-fonts/ofl/rubik/Rubik[wght].ttf"
LINES = [
    "áéíóúñ àèìòù âêîôû",
    "äëïöü ãõ çćč šžě",
    "ÁÉÍÓÚÑ ÀÈÌ ÄËÏÖ Ç",
]
SIZE = 96
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/diacritics-vs-rubik.png"

vf = ImageFont.truetype(VIRTUA, SIZE)
rf = ImageFont.truetype(RUBIK, SIZE)
rowh = SIZE + 40
img = Image.new("RGB", (1500, rowh * len(LINES) * 2 + 40), "white")
d = ImageDraw.Draw(img)
y = 20
for line in LINES:
    d.text((20, y), "V", fill="#bbb"); d.text((60, y), line, font=vf, fill="black")
    y += rowh
    d.text((20, y), "R", fill="#bbb"); d.text((60, y), line, font=rf, fill="black")
    y += rowh + 16
import os
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
img.save(OUT)
print("wrote", OUT)
