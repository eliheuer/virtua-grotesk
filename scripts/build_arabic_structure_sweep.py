#!/usr/bin/env python3
"""Build a focused Arabic codepoint sweep for structure review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import html
import sys
import unicodedata

from fontTools.ttLib import TTFont
import glyphsets


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "documentation/arabic-structure-sweep.html"
GLYPHSET_NAME = "GF_Arabic_Core"
EXTRA_CODEPOINTS = {0x25CC}
FONTS = [
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf", "400"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf", "500"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf", "600"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf", "700"),
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf", "400 700"),
]


@dataclass
class FontInfo:
    label: str
    path: str
    weight: str
    cmap: dict[int, str]


def load_fonts() -> list[FontInfo]:
    fonts: list[FontInfo] = []
    for label, path, weight in FONTS:
        font = TTFont(ROOT / path)
        fonts.append(FontInfo(label, path, weight, font.getBestCmap() or {}))
        font.close()
    return fonts


def codepoints() -> list[int]:
    return sorted(set(glyphsets.unicodes_per_glyphset(GLYPHSET_NAME)) | EXTRA_CODEPOINTS)


def category_label(codepoint: int) -> str:
    category = unicodedata.category(chr(codepoint))
    if category.startswith("L"):
        return "letter"
    if category.startswith("M"):
        return "mark"
    if category.startswith("N"):
        return "number"
    if category.startswith("P"):
        return "punctuation"
    if category.startswith("S"):
        return "symbol"
    if category.startswith("C"):
        return "control"
    return "other"


def sample_text(codepoint: int) -> str:
    char = chr(codepoint)
    category = category_label(codepoint)
    if category == "letter":
        return f"{char}  ب{char}ب  ا{char}ا"
    if category == "mark":
        return f"\u25cc{char}  ب{char}  بّ{char}"
    if codepoint == 0x25CC:
        return "\u25ccَ \u25ccُ \u25ccِ \u25ccّ"
    if category in {"control", "other"}:
        return f"ب{char}ب"
    return f"{char} {char}{char}{char}"


def font_faces() -> str:
    faces = []
    for label, path, weight in FONTS:
        faces.append(
            "@font-face {"
            f"font-family: 'VirtuaStructure{label}';"
            f"src: url('../{html.escape(path)}') format('truetype');"
            f"font-weight: {weight};"
            "font-style: normal;"
            "font-display: block;"
            "}"
        )
    return "\n".join(faces)


def glyph_name(font: FontInfo, codepoint: int) -> str:
    return font.cmap.get(codepoint, ".notdef")


def row_html(codepoint: int, fonts: list[FontInfo]) -> str:
    char = chr(codepoint)
    name = unicodedata.name(char, "UNKNOWN")
    category = category_label(codepoint)
    samples = []
    for font in fonts:
        sample = sample_text(codepoint)
        glyph = glyph_name(font, codepoint)
        state = "missing" if glyph == ".notdef" else ""
        samples.append(
            "<td>"
            f"<div class='sample {state}' dir='rtl' lang='ar' "
            f"style=\"font-family: 'VirtuaStructure{font.label}'\">"
            f"{html.escape(sample)}"
            "</div>"
            f"<div class='glyph'>{html.escape(glyph)}</div>"
            "</td>"
        )
    return (
        "<tr>"
        f"<th scope='row'>U+{codepoint:04X}<br><span>{html.escape(char if category != 'control' else '')}</span></th>"
        f"<td><strong>{html.escape(name)}</strong><br><span>{category}</span></td>"
        f"{''.join(samples)}"
        "</tr>"
    )


def html_report(fonts: list[FontInfo]) -> str:
    rows = "\n".join(row_html(codepoint, fonts) for codepoint in codepoints())
    headings = "".join(f"<th>{html.escape(font.label)}</th>" for font in fonts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virtua Grotesk Arabic Structure Sweep</title>
<style>
{font_faces()}
:root {{
  color-scheme: light;
  --ink: #191919;
  --muted: #666;
  --line: #d8d8d8;
  --paper: #fff;
  --bg: #f4f4f0;
  --warn: #fff4cf;
}}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
main {{
  max-width: 1480px;
  margin: 0 auto;
  padding: 28px 20px 56px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 28px;
}}
.summary {{
  max-width: 900px;
  margin: 0 0 20px;
  color: var(--muted);
  line-height: 1.45;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--paper);
  border: 1px solid var(--line);
}}
th, td {{
  border: 1px solid var(--line);
  padding: 9px 10px;
  vertical-align: top;
}}
thead th {{
  position: sticky;
  top: 0;
  z-index: 2;
  background: #eeeae2;
  text-align: left;
}}
tbody th {{
  width: 92px;
  text-align: left;
  font-weight: 650;
}}
tbody th span, td span, .glyph {{
  color: var(--muted);
  font-size: 12px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}}
.sample {{
  min-width: 130px;
  min-height: 56px;
  font-size: 36px;
  line-height: 1.25;
  white-space: nowrap;
}}
.sample.missing {{
  background: var(--warn);
}}
.glyph {{
  margin-top: 6px;
  overflow-wrap: anywhere;
}}
</style>
</head>
<body>
<main>
<h1>Virtua Grotesk Arabic Structure Sweep</h1>
<p class="summary">
Generated from <code>{GLYPHSET_NAME}</code> plus U+25CC dotted circle.
Use this for the batch-2 structure and wrong-glyph sweep before broader spacing review.
Each cell shows the current rendered sample and cmap glyph name for that font.
Mark <code>fix-needed</code> only for specific source issues; otherwise record pass/defer in
<code>documentation/arabic-visual-review-log.md</code>.
</p>
<table>
<thead><tr><th>Codepoint</th><th>Name</th>{headings}</tr></thead>
<tbody>
{rows}
</tbody>
</table>
</main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_report(load_fonts()), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
