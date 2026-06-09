#!/usr/bin/env python3
"""Build a focused HTML proof for Arabic visual-risk rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import html
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
RISK_REPORT = ROOT / "documentation/glyph-review/arabic-visual-risk-audit.md"
OUTPUT_DEFAULT = ROOT / "documentation/glyph-review/arabic-visual-risk-proof.html"
FONT_PATHS = [
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf"),
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf"),
]
REVIEW_CONTEXTS = (
    ("isolated", "{char}"),
    ("repeated", "{char}{char}{char}"),
    ("right-join context", "ا{char}ا"),
    ("joining texture", "ب{char}ب"),
    ("word rhythm", "س{char}س"),
)


@dataclass(frozen=True)
class RiskRow:
    font: str
    codepoint: int
    character: str
    name: str
    glyph: str
    advance: str
    bounds: str
    risks: str


def display_path(path: str) -> str:
    return str((ROOT / path).resolve().relative_to(ROOT))


def html_path(path: str) -> str:
    return "../" + display_path(path)


def parse_risk_rows(text: str) -> list[RiskRow]:
    rows: list[RiskRow] = []
    for line in text.splitlines():
        if not line.startswith("| `fonts/"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        match = re.search(r"U\+([0-9A-Fa-f]{4,6})", cells[1])
        if not match:
            continue
        rows.append(
            RiskRow(
                font=cells[0].strip("`"),
                codepoint=int(match.group(1), 16),
                character=cells[2],
                name=cells[3],
                glyph=cells[4].strip("`"),
                advance=cells[5],
                bounds=cells[6],
                risks=cells[7],
            )
        )
    return rows


def unique_codepoints(rows: list[RiskRow]) -> list[int]:
    return sorted({row.codepoint for row in rows})


def rows_for_codepoint(rows: list[RiskRow], codepoint: int) -> list[RiskRow]:
    return [row for row in rows if row.codepoint == codepoint]


def name_for_codepoint(codepoint: int) -> str:
    return unicodedata.name(chr(codepoint), "UNKNOWN")


def font_faces() -> str:
    faces = []
    for label, path in FONT_PATHS:
        family = f"VirtuaRisk{label}"
        faces.append(
            "@font-face {"
            f" font-family: '{family}';"
            f" src: url('{html.escape(html_path(path))}') format('truetype');"
            " font-weight: 400 700;"
            " font-style: normal;"
            " font-display: block;"
            "}"
        )
    return "\n".join(faces)


def sample_text(template: str, codepoint: int) -> str:
    return template.format(char=chr(codepoint))


def codepoint_card(codepoint: int, rows: list[RiskRow]) -> str:
    risk_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row.font)}</td>"
        f"<td>{html.escape(row.glyph)}</td>"
        f"<td>{html.escape(row.advance)}</td>"
        f"<td>{html.escape(row.bounds)}</td>"
        f"<td>{html.escape(row.risks)}</td>"
        "</tr>"
        for row in rows_for_codepoint(rows, codepoint)
    )
    specimens = []
    for label, _path in FONT_PATHS:
        family = f"VirtuaRisk{label}"
        sample_cells = []
        for context_label, template in REVIEW_CONTEXTS:
            text = sample_text(template, codepoint)
            sample_cells.append(
                "<div class='sample-cell'>"
                f"<div class='sample-label'>{html.escape(context_label)}</div>"
                f"<div class='sample-text' dir='rtl' lang='ar' style=\"font-family: '{family}'\">"
                f"{html.escape(text)}"
                "</div>"
                "</div>"
            )
        specimens.append(
            "<section class='font-row'>"
            f"<h4>{html.escape(label)}</h4>"
            f"<div class='sample-grid'>{''.join(sample_cells)}</div>"
            "</section>"
        )

    return (
        "<article class='card'>"
        f"<h2>U+{codepoint:04X} {html.escape(name_for_codepoint(codepoint))}</h2>"
        "<table>"
        "<thead><tr><th>Font</th><th>Glyph</th><th>Advance</th><th>Bounds</th><th>Risk</th></tr></thead>"
        f"<tbody>{risk_rows}</tbody>"
        "</table>"
        f"{''.join(specimens)}"
        "</article>"
    )


def markdown_summary(rows: list[RiskRow]) -> str:
    codepoints = unique_codepoints(rows)
    labels = ", ".join(f"U+{codepoint:04X}" for codepoint in codepoints) or "none"
    return (
        f"Risk rows: {len(rows)}. "
        f"Unique codepoints: {len(codepoints)} ({labels}). "
        "Review sidebearings in isolated and shaped RTL contexts before editing."
    )


def html_report(rows: list[RiskRow]) -> str:
    cards = "\n".join(codepoint_card(codepoint, rows) for codepoint in unique_codepoints(rows))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Virtua Grotesk Arabic Visual Risk Proof</title>
<style>
{font_faces()}
:root {{
  color-scheme: light;
  --ink: #171717;
  --muted: #666;
  --line: #d7d7d7;
  --paper: #fff;
  --note: #f6f1df;
}}
body {{
  margin: 0;
  background: #f3f3f0;
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.4;
}}
main {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 32px 24px 56px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 650;
}}
.summary {{
  margin: 0 0 24px;
  max-width: 780px;
  color: var(--muted);
}}
.card {{
  margin: 0 0 28px;
  padding: 20px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
}}
h2 {{
  margin: 0 0 16px;
  font-size: 20px;
}}
h4 {{
  margin: 18px 0 8px;
  font-size: 13px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 12px;
  font-size: 13px;
}}
th, td {{
  text-align: left;
  border-bottom: 1px solid var(--line);
  padding: 6px 8px;
  vertical-align: top;
}}
.sample-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 10px;
}}
.sample-cell {{
  min-height: 112px;
  border: 1px solid var(--line);
  background:
    linear-gradient(to bottom, transparent 47%, #e2e2dd 47%, #e2e2dd 48%, transparent 48%),
    var(--paper);
  overflow: hidden;
}}
.sample-label {{
  padding: 6px 8px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}}
.sample-text {{
  height: 76px;
  padding: 2px 12px 0;
  font-size: 56px;
  line-height: 76px;
  white-space: nowrap;
  text-align: center;
}}
.note {{
  margin: 0 0 22px;
  padding: 10px 12px;
  background: var(--note);
  border: 1px solid #ded5b0;
  border-radius: 6px;
  font-size: 14px;
}}
</style>
</head>
<body>
<main>
<h1>Arabic Visual Risk Proof</h1>
<p class="summary">{html.escape(markdown_summary(rows))}</p>
<p class="note">This proof is generated from <code>documentation/glyph-review/arabic-visual-risk-audit.md</code>. It is a fast triage aid for sidebearing and spacing review, not a substitute for the full Google Fonts proof or native-reader review.</p>
{cards}
</main>
</body>
</html>
"""


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: build_arabic_visual_risk_proof.py [output.html]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = parse_risk_rows(RISK_REPORT.read_text(encoding="utf-8"))
    output_path.write_text(html_report(rows), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
