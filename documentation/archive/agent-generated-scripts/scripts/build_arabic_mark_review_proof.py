#!/usr/bin/env python3
"""Build a focused proof for Arabic mark attachment review."""

from __future__ import annotations

from pathlib import Path
import html
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-mark-review-proof.html"
FONTS = [
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf", "400"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf", "500"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf", "600"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf", "700"),
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf", "400 700"),
]

SECTIONS = [
    (
        "mark-base+fatha",
        "Base plus fatha",
        "Top mark position clears base strokes and keeps a consistent angle.",
        ["بَ", "تَ", "جَ", "سَ", "صَ", "طَ", "مَ", "هَ"],
    ),
    (
        "mark-base+damma",
        "Base plus damma",
        "Damma position and scale remain readable across weight gain.",
        ["بُ", "تُ", "جُ", "سُ", "صُ", "طُ", "مُ", "هُ"],
    ),
    (
        "mark-base+kasra",
        "Base plus kasra",
        "Bottom mark clears descenders and remains centered under the base.",
        ["بِ", "تِ", "جِ", "سِ", "صِ", "طِ", "مِ", "هِ"],
    ),
    (
        "mark-shadda+sukun",
        "Shadda and sukun stacking",
        "Stacked top marks remain clear and do not merge in Bold.",
        ["بّ", "بْ", "بُّ", "بَّ", "بّْ", "مّ", "هّ", "سْ"],
    ),
    (
        "mark-tanween",
        "Tanween",
        "Double marks retain spacing and do not collapse into one shape.",
        ["بً", "بٌ", "بٍ", "مً", "مٌ", "مٍ", "هً", "هٍ"],
    ),
    (
        "mark-hamza-above-below",
        "Hamza above and below",
        "Hamza marks attach cleanly above and below real bases.",
        ["بٔ", "بٕ", "أ", "إ", "ؤ", "ئ", "مٔ", "هٔ"],
    ),
    (
        "mark-dotted-circle",
        "Dotted circle",
        "Dotted circle stays readable with top, bottom, and stacked marks.",
        ["◌َ", "◌ُ", "◌ِ", "◌ّ", "◌ْ", "◌ٔ", "◌ٕ", "◌ً", "◌ٌ", "◌ٍ"],
    ),
    (
        "class-mark-combinations",
        "Required mark inventory",
        "All required Arabic Core combining marks are visible on dotted circle.",
        ["◌ؕ", "◌ً", "◌ٌ", "◌ٍ", "◌َ", "◌ُ", "◌ِ", "◌ّ", "◌ْ", "◌ٓ", "◌ٔ", "◌ٕ", "◌ٖ", "◌٘", "◌ٰ", "◌ۛ"],
    ),
]


def font_faces() -> str:
    faces = []
    for label, path, weight in FONTS:
        faces.append(
            "@font-face {"
            f"font-family: 'VirtuaMark{label}';"
            f"src: url('../{html.escape(path)}') format('truetype');"
            f"font-weight: {weight};"
            "font-style: normal;"
            "font-display: block;"
            "}"
        )
    return "\n".join(faces)


def section_html(section_id: str, title: str, note: str, samples: list[str]) -> str:
    rows = []
    for label, _path, _weight in FONTS:
        cells = "".join(
            "<span class='sample' dir='rtl' lang='ar' "
            f"style=\"font-family: 'VirtuaMark{label}'\">{html.escape(sample)}</span>"
            for sample in samples
        )
        rows.append(
            "<div class='font-row'>"
            f"<h3>{html.escape(label)}</h3>"
            f"<div class='samples'>{cells}</div>"
            "</div>"
        )
    return (
        f"<section class='card' id='{html.escape(section_id)}'>"
        f"<h2>{html.escape(title)}</h2>"
        f"<p>{html.escape(note)}</p>"
        f"{''.join(rows)}"
        "</section>"
    )


def html_report() -> str:
    sections = "\n".join(
        section_html(section_id, title, note, samples)
        for section_id, title, note, samples in SECTIONS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virtua Grotesk Arabic Mark Review Proof</title>
<style>
{font_faces()}
:root {{
  color-scheme: light;
  --ink: #191919;
  --muted: #666;
  --line: #d8d8d8;
  --paper: #fff;
  --bg: #f4f4f0;
}}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
main {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 20px 56px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 28px;
}}
.summary {{
  max-width: 860px;
  margin: 0 0 22px;
  color: var(--muted);
  line-height: 1.45;
}}
.card {{
  margin: 0 0 22px;
  padding: 18px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  scroll-margin-top: 12px;
}}
h2 {{
  margin: 0 0 6px;
  font-size: 20px;
}}
p {{
  margin: 0 0 14px;
  color: var(--muted);
}}
.font-row {{
  display: grid;
  grid-template-columns: 112px 1fr;
  gap: 14px;
  align-items: start;
  padding: 10px 0;
  border-top: 1px solid var(--line);
}}
h3 {{
  margin: 8px 0 0;
  font-size: 13px;
  color: var(--muted);
  text-transform: uppercase;
}}
.samples {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}}
.sample {{
  min-width: 58px;
  min-height: 58px;
  padding: 8px 10px;
  background: #fafafa;
  border: 1px solid #e4e4e4;
  border-radius: 6px;
  font-size: 42px;
  line-height: 1.1;
  text-align: center;
}}
</style>
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const id = decodeURIComponent(window.location.hash.slice(1));
  if (!id) {{
    return;
  }}
  for (const section of document.querySelectorAll("section.card")) {{
    if (section.id !== id) {{
      section.remove();
    }}
  }}
  const target = document.getElementById(id);
  if (target) {{
    target.scrollIntoView();
  }}
}});
</script>
</head>
<body>
<main>
<h1>Virtua Grotesk Arabic Mark Review Proof</h1>
<p class="summary">
Focused proof for Arabic visual-review batch 3. Use this with
<code>documentation/glyph-review/arabic-mark-readiness.md</code> to record
<code>mark-base+fatha</code>, <code>mark-base+damma</code>,
<code>mark-base+kasra</code>, <code>mark-shadda+sukun</code>,
<code>mark-tanween</code>, <code>mark-hamza-above-below</code>,
<code>mark-dotted-circle</code>, and <code>class-mark-combinations</code>.
</p>
{sections}
</main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else OUTPUT_DEFAULT
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_report(), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
