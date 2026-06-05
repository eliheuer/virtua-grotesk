#!/usr/bin/env python3
"""Build a compact Arabic manual-review dashboard for current fonts."""

from __future__ import annotations

from pathlib import Path
import html
import os
import re
import sys
import xml.etree.ElementTree as ET

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation/glyph-review/arabic-manual-review-dashboard.html"
NEXT_BATCH_OUTPUT = ROOT / "documentation/glyph-review/arabic-next-review-batch.html"
VISUAL_LOG = ROOT / "documentation/glyph-review/arabic-visual-review-log.md"
CONTOUR_LOG = ROOT / "documentation/glyph-review/contour-cleanup/contour-cleanup-decision-log.md"
RISK_AUDIT = ROOT / "documentation/glyph-review/arabic-visual-risk-audit.md"
STRUCTURE_TRIAGE = ROOT / "documentation/glyph-review/arabic-structure-triage.md"
MARK_TRIAGE = ROOT / "documentation/glyph-review/arabic-mark-triage.md"
PROOF_DIR = ROOT / "documentation/google-fonts/gftools-qa/Proof"
SOURCE_UFOS = [
    ROOT / "sources/VirtuaGrotesk-Regular.ufo",
    ROOT / "sources/VirtuaGrotesk-Bold.ufo",
]
REFERENCE_CANDIDATES = [
    Path("/Users/eli/GH/forks/fonts/ofl/rubik/Rubik[wght].ttf"),
    Path("/Users/eli/GH/repos/google-fonts/ofl/rubik/Rubik[wght].ttf"),
]

FONTS = [
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf", "400"),
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf", "400"),
    ("Medium", "fonts/ttf/VirtuaGrotesk-Medium.ttf", "500"),
    ("SemiBold", "fonts/ttf/VirtuaGrotesk-SemiBold.ttf", "600"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf", "700"),
]

PREVIEW_FONTS = [
    ("Regular", "fonts/ttf/VirtuaGrotesk-Regular.ttf"),
    ("Bold", "fonts/ttf/VirtuaGrotesk-Bold.ttf"),
    ("Variable", "fonts/variable/VirtuaGrotesk[wght].ttf"),
]

SAMPLES = [
    ("Smoke: salaam", "سلام"),
    ("Smoke: arabic", "العربية"),
    ("Smoke: bismillah", "بسم الله"),
    ("Smoke: lam-alef", "لا لأ لإ لآ"),
    ("Letter structures", "ص ض ط ظ م ه و ؤ"),
    ("Joining texture", "بثجحخ سشصض طظ فقكلمنهي"),
    ("Persian/Urdu letters", "پ چ ژ گ ک ی ے ں"),
    ("Arabic marks", "بَ بُ بِ بّ بْ بً بٌ بٍ بٔ بٕ"),
    ("Dotted circle marks", "◌َ ◌ُ ◌ِ ◌ّ ◌ْ ◌ٔ ◌ٕ"),
    ("Arabic-Indic digits", "٠١٢٣٤٥٦٧٨٩"),
    ("Eastern Arabic digits", "۰۱۲۳۴۵۶۷۸۹"),
    ("Arabic punctuation", "، ؛ ؟ ٪ ٫ ٬ ۔"),
]

SAMPLE_IDS = {
    "Smoke: salaam": "smoke-salaam",
    "Smoke: arabic": "smoke-arabic",
    "Smoke: bismillah": "smoke-bismillah",
    "Smoke: lam-alef": "smoke-lam-alef",
    "Persian/Urdu letters": "class-dot-stack-helpers",
    "Arabic-Indic digits": "class-arabic-farsi-numerals",
    "Arabic punctuation": "class-arabic-punctuation",
}

NEXT_BATCH_VISUAL_KEYS = {
    "proof-regular-glyphs",
    "proof-medium-glyphs",
    "proof-semibold-glyphs",
    "proof-bold-glyphs",
    "class-letter-structures",
}


class FontRenderer:
    def __init__(self, path: Path):
        self.path = path
        self.font = TTFont(path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap() or {}
        self.upm = self.font["head"].unitsPerEm

    def glyph_for_codepoint(self, codepoint: int) -> str | None:
        return self.cmap.get(codepoint)

    def has_glyph(self, glyph_name: str) -> bool:
        return glyph_name in self.glyph_set

    def svg_for_glyph(self, glyph_name: str) -> str:
        if glyph_name not in self.glyph_set:
            return "<div class='missing'>missing</div>"
        glyph = self.glyph_set[glyph_name]
        bounds_pen = BoundsPen(self.glyph_set)
        glyph.draw(bounds_pen)
        bounds = bounds_pen.bounds
        advance = getattr(glyph, "width", 0) or 0

        if bounds is None:
            x_min, y_min, x_max, y_max = 0, -120, max(advance, 160), 120
        else:
            x_min, y_min, x_max, y_max = bounds
            x_min = min(x_min, 0)
            x_max = max(x_max, advance, 0)

        pad = 80
        view_x = x_min - pad
        view_y = -(y_max + pad)
        view_w = max(120, (x_max - x_min) + (pad * 2))
        view_h = max(160, (y_max - y_min) + (pad * 2))

        path_pen = SVGPathPen(self.glyph_set)
        glyph.draw(path_pen)
        data = path_pen.getCommands()
        baseline = -view_y
        origin_x = -view_x
        advance_x = origin_x + advance
        return (
            f"<svg viewBox='{view_x} {view_y} {view_w} {view_h}' role='img' "
            f"aria-label='{html.escape(glyph_name)}'>"
            f"<line class='metric' x1='{view_x}' y1='{baseline}' x2='{view_x + view_w}' y2='{baseline}'/>"
            f"<line class='sidebearing' x1='{origin_x}' y1='{view_y}' x2='{origin_x}' y2='{view_y + view_h}'/>"
            f"<line class='sidebearing' x1='{advance_x}' y1='{view_y}' x2='{advance_x}' y2='{view_y + view_h}'/>"
            "<g transform='scale(1,-1)'>"
            f"<path d='{html.escape(data)}'/>"
            "</g>"
            "</svg>"
        )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def reference_path() -> Path | None:
    for path in REFERENCE_CANDIDATES:
        if path.exists():
            return path
    return None


def pending_count(path: Path) -> int:
    text = read_text(path)
    match = re.search(r"^- Pending: (\d+)$", text, flags=re.MULTILINE)
    return int(match.group(1)) if match else 0


def contour_rows() -> list[tuple[str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str]] = []
    for line in read_text(CONTOUR_LOG).splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 9:
            continue
        source = cells[0].strip("`")
        fontspector = cells[1].strip("`")
        batch = cells[2]
        category = cells[3]
        command = cells[4].strip("`")
        rows.append((source, fontspector, batch, category, command, review_step(category)))
    return rows


def visual_review_rows() -> list[tuple[str, str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for line in read_text(VISUAL_LOG).splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 9:
            continue
        key = cells[0].strip("`")
        rows.append((key, cells[1], cells[2], cells[3], cells[4], cells[5], cells[6]))
    return rows


def review_step(category: str) -> str:
    if category == "Arabic mark or mark combination":
        return "Check dotted circle, real base attachment, and stacking clarity before changing contours."
    if category == "Arabic dot-stack helper":
        return "Check Bold/variable dot separation first; fix only if dots merge or spacing breaks."
    if category == "Arabic letter or positional form":
        return "Judge skeleton, joins, counters, and chamfers; do not chase the heuristic alone."
    if category == "shared punctuation":
        return "Check Latin and Arabic text rhythm; accept if the shape is intentional and interpolates cleanly."
    return "Inspect source and rendered proof together; record fix, accept, or defer."


def risk_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for line in read_text(RISK_AUDIT).splitlines():
        if not line.startswith("| `fonts/"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 8:
            continue
        rows.append((cells[0].strip("`"), cells[1], cells[3], cells[7].replace("`", "")))
    return rows


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_cell_html(value: str) -> str:
    parts = value.split("<br>")
    escaped_parts = []
    for part in parts:
        escaped = html.escape(part.strip())
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        escaped_parts.append(escaped)
    return "<br>".join(escaped_parts)


def codepoint_int(value: str) -> int | None:
    match = re.search(r"U\+([0-9A-Fa-f]{4,6})", value)
    return int(match.group(1), 16) if match else None


def source_targets_html(codepoint_cell: str) -> str:
    codepoint = codepoint_int(codepoint_cell)
    if codepoint is None:
        return "unknown"
    targets: list[str] = []
    for ufo in SOURCE_UFOS:
        for glif_path in sorted((ufo / "glyphs").glob("*.glif")):
            try:
                root = ET.parse(glif_path).getroot()
            except ET.ParseError:
                continue
            for unicode_element in root.findall("unicode"):
                hex_value = unicode_element.attrib.get("hex", "")
                if hex_value and int(hex_value, 16) == codepoint:
                    targets.append(
                        "<code>{}</code> <code>{}</code><br><code>{}</code>".format(
                            html.escape(ufo.name),
                            html.escape(root.attrib.get("name", glif_path.stem)),
                            html.escape(str(glif_path.relative_to(ROOT))),
                        )
                    )
    return "<br>".join(targets) if targets else "none found"


def grouped_structure_prompt_rows() -> list[tuple[str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str]] = []
    in_section = False
    for line in read_text(STRUCTURE_TRIAGE).splitlines():
        if line == "## Grouped Review Prompts":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("| `"):
            continue
        cells = markdown_cells(line)
        if len(cells) != 6:
            continue
        rows.append(tuple(cells))  # type: ignore[arg-type]
    return rows


def grouped_structure_prompt_table_rows() -> list[tuple[str, str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    for row in grouped_structure_prompt_rows():
        codepoint, glyphs, category, fonts, risk_summary, prompt = row
        rows.append(
            (
                markdown_cell_html(codepoint),
                markdown_cell_html(glyphs),
                markdown_cell_html(category),
                markdown_cell_html(fonts),
                markdown_cell_html(risk_summary),
                markdown_cell_html(prompt),
                source_targets_html(codepoint),
            )
        )
    return rows


def markdown_table_rows(path: Path, heading: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_section = False
    for line in read_text(path).splitlines():
        if line == heading:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        cells = markdown_cells(line)
        if not cells or cells[0] == "---" or cells[0].startswith("Review row"):
            continue
        rows.append(cells)
    return rows


def mark_prompt_summary_table_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for cells in markdown_table_rows(MARK_TRIAGE, "## No-Offset Review Prompt Summary"):
        if len(cells) != 4:
            continue
        rows.append(tuple(markdown_cell_html(cell) for cell in cells))  # type: ignore[arg-type]
    return rows


def mark_prompt_detail_table_rows() -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    for cells in markdown_table_rows(MARK_TRIAGE, "## No-Offset Review Prompt Rows"):
        if len(cells) < 4:
            continue
        if len(cells) == 4:
            cells.append("none")
        rows.append(tuple(markdown_cell_html(cell) for cell in cells[:5]))  # type: ignore[arg-type]
    return rows


def proof_links(output_path: Path) -> list[tuple[str, str]]:
    if not PROOF_DIR.exists():
        return []
    links: list[tuple[str, str]] = []
    for path in sorted(PROOF_DIR.glob("*.html")):
        label = path.name
        href = os.path.relpath(path, output_path.parent)
        links.append((label, str(href)))
    return links


def next_batch_proof_links(output_path: Path) -> list[tuple[str, str]]:
    return [(label, href) for label, href in proof_links(output_path) if "diffbrowsers_glyphs" in label]


def css() -> str:
    faces = []
    for label, path, weight in FONTS:
        faces.append(
            "@font-face {"
            f"font-family: 'Virtua Review {label}';"
            f"src: url('../{path}') format('truetype');"
            f"font-weight: {weight};"
            "font-style: normal;"
            "}"
        )
    return "\n".join(
        [
            *faces,
            ":root { color-scheme: light; font-family: system-ui, sans-serif; }",
            "body { margin: 0; padding: 32px; background: #f7f5ef; color: #191714; }",
            "main { max-width: 1180px; margin: 0 auto; }",
            "h1 { font-size: 28px; margin: 0 0 8px; }",
            "h2 { font-size: 18px; margin: 32px 0 12px; }",
            "p, li { line-height: 1.5; }",
            ".summary { display: flex; gap: 12px; flex-wrap: wrap; margin: 20px 0; }",
            ".pill { border: 1px solid #c9c1b2; padding: 8px 10px; background: #fffdf8; }",
            ".sample { border-top: 1px solid #d8d0c2; padding: 18px 0; }",
            ".sample { scroll-margin-top: 12px; }",
            ".sample h3 { margin: 0 0 10px; font-size: 14px; color: #5d5548; }",
            ".row { display: grid; grid-template-columns: 110px 1fr; gap: 14px; align-items: baseline; margin: 6px 0; }",
            ".label { color: #6b6256; font-size: 13px; }",
            ".arabic { direction: rtl; unicode-bidi: plaintext; font-size: 44px; line-height: 1.35; background: white; padding: 10px 14px; border: 1px solid #ddd4c6; overflow: visible; }",
            ".small .arabic { font-size: 24px; }",
            "table { width: 100%; border-collapse: collapse; background: #fffdf8; }",
            "th, td { text-align: left; vertical-align: top; border: 1px solid #d8d0c2; padding: 8px; font-size: 13px; }",
            "th { background: #ece5d8; }",
            "a { color: #125c79; }",
            ".proofs { columns: 2; }",
            ".glyph-preview { display: flex; gap: 8px; flex-wrap: wrap; min-width: 260px; }",
            ".glyph-card { width: 86px; background: white; border: 1px solid #ddd4c6; padding: 6px; }",
            ".reference-card { border-color: #9f8d6d; background: #fff8e8; }",
            ".glyph-card svg { display: block; width: 100%; height: 84px; overflow: visible; }",
            ".glyph-card path { fill: #191714; }",
            ".glyph-card .metric { stroke: #d6a15b; stroke-width: 8; }",
            ".glyph-card .sidebearing { stroke: #7ca6b8; stroke-width: 8; stroke-dasharray: 16 16; }",
            ".preview-label { margin-top: 4px; color: #6b6256; font-size: 11px; }",
            ".reference-note { color: #7b5b20; font-size: 12px; margin: 0 0 12px; }",
            ".missing { color: #9a3a2c; font-size: 12px; padding: 32px 0; text-align: center; }",
        ]
    )


def sample_block(label: str, text: str) -> str:
    rows = []
    for font_label, _, _ in FONTS:
        rows.append(
            "<div class='row'>"
            f"<div class='label'>{html.escape(font_label)}</div>"
            f"<div class='arabic' style=\"font-family: 'Virtua Review {html.escape(font_label)}';\">{html.escape(text)}</div>"
            "</div>"
        )
    sample_id = SAMPLE_IDS.get(label)
    id_attribute = f" id='{html.escape(sample_id)}'" if sample_id else ""
    return f"<section class='sample'{id_attribute}><h3>{html.escape(label)}</h3>{''.join(rows)}</section>"


def table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def visual_review_command(key: str) -> str:
    command = (
        f"make arabic-visual-review-update REVIEW_KEY={key} REVIEW_STATUS=pass "
        'REVIEWER="Name YYYY-MM-DD" NOTES="reviewed"'
    )
    return f"<code>{html.escape(command)}</code>"


def contour_decision_commands(source: str) -> str:
    fix = (
        f"make contour-decision-update GLYPH={source} STATUS=fix-now "
        'DECISION="needs source edit" REVIEWED="Name YYYY-MM-DD"'
    )
    accept = (
        f"make contour-decision-update GLYPH={source} STATUS=accepted "
        'DECISION="reviewed style divergence" REVIEWED="Name YYYY-MM-DD"'
    )
    defer = (
        f"make contour-decision-update GLYPH={source} STATUS=deferred "
        'DECISION="needs Arabic review" REVIEWED="Name YYYY-MM-DD"'
    )
    commands = [fix, accept, defer]
    return "<br>".join(f"<code>{html.escape(command)}</code>" for command in commands)


def preview_renderers() -> list[tuple[str, FontRenderer]]:
    renderers = []
    for label, relative_path in PREVIEW_FONTS:
        path = ROOT / relative_path
        if path.exists():
            renderers.append((label, FontRenderer(path)))
    return renderers


def codepoint_for_glyph_name(glyph_name: str) -> int | None:
    base = glyph_name.split(".", 1)[0]
    if base.startswith("uni") and len(base) >= 7:
        try:
            return int(base[3:7], 16)
        except ValueError:
            return None
    return None


def reference_name_candidates(source_name: str, glyph_name: str) -> list[str]:
    source_ar = source_name.replace("-ar.", "ar.").replace("-ar", "ar")
    candidates = [
        glyph_name,
        source_name,
        source_ar,
        f"{glyph_name}.1",
        f"{source_ar}.1",
    ]
    if source_name.startswith("lam_alef") and not source_ar.endswith(".fina"):
        candidates.append(f"{source_ar}.fina")
    return list(dict.fromkeys(candidates))


def reference_glyph(source_name: str, glyph_name: str, renderer: FontRenderer | None) -> str | None:
    if not renderer:
        return None
    codepoint = codepoint_for_glyph_name(glyph_name)
    if codepoint is not None:
        cmap_glyph = renderer.glyph_for_codepoint(codepoint)
        if cmap_glyph:
            return cmap_glyph
    for candidate in reference_name_candidates(source_name, glyph_name):
        if renderer.has_glyph(candidate):
            return candidate
    return None


def reference_renderer() -> tuple[str, FontRenderer] | None:
    path = reference_path()
    if not path:
        return None
    return (str(path), FontRenderer(path))


def contour_preview(
    source_name: str,
    glyph_name: str,
    renderers: list[tuple[str, FontRenderer]],
    reference: tuple[str, FontRenderer] | None,
) -> str:
    if not renderers:
        return "<span class='missing'>build fonts first</span>"
    cards = []
    for label, renderer in renderers:
        cards.append(
            "<div class='glyph-card'>"
            f"{renderer.svg_for_glyph(glyph_name)}"
            f"<div class='preview-label'>{html.escape(label)}</div>"
            "</div>"
        )
    if reference:
        ref_path, ref_renderer = reference
        ref_glyph = reference_glyph(source_name, glyph_name, ref_renderer)
        cards.append(
            "<div class='glyph-card reference-card'>"
            f"{ref_renderer.svg_for_glyph(ref_glyph or '')}"
            f"<div class='preview-label'>Rubik ref: {html.escape(ref_glyph or 'none')}</div>"
            f"<div class='preview-label'>{html.escape(ref_path)}</div>"
            "</div>"
        )
    return "<div class='glyph-preview'>" + "".join(cards) + "</div>"


def next_batch_html(output_path: Path) -> str:
    contours = contour_rows()
    visual_rows = [row for row in visual_review_rows() if row[0] in NEXT_BATCH_VISUAL_KEYS]
    links = next_batch_proof_links(output_path)
    renderers = preview_renderers()
    reference = reference_renderer()
    contour_table = table(
        ["Source glyph", "Fontspector glyph", "Preview", "Batch", "Category", "Review step", "Record decision"],
        [
            (
                f"<code>{html.escape(source)}</code>",
                f"<code>{html.escape(fontspector)}</code>",
                contour_preview(source, fontspector, renderers, reference),
                html.escape(batch),
                html.escape(category),
                html.escape(step),
                contour_decision_commands(source),
            )
            for source, fontspector, batch, category, _command, step in contours
        ],
    )
    visual_table = table(
        ["Key", "Area", "Item", "Evidence", "Machine precheck", "Review cue", "Status", "Record pass"],
        [
            (
                f"<code>{html.escape(key)}</code>",
                html.escape(area),
                html.escape(item),
                html.escape(evidence),
                html.escape(machine_precheck),
                html.escape(cue),
                html.escape(status),
                visual_review_command(key),
            )
            for key, area, item, evidence, machine_precheck, cue, status in visual_rows
        ],
    )
    structure_prompt_table = table(
        ["Codepoint", "Glyphs", "Category", "Fonts", "Risk summary", "Review prompt", "Source edit targets"],
        grouped_structure_prompt_table_rows(),
    )
    mark_prompt_summary_table = table(
        ["Review row", "Font", "Samples", "Sample texts"],
        mark_prompt_summary_table_rows(),
    )
    mark_prompt_detail_table = table(
        ["Review row", "Font", "Sample", "Glyph sequence", "Source edit targets"],
        mark_prompt_detail_table_rows(),
    )
    if contours:
        contour_step = (
            "Use the contour table below to decide whether each Fontspector contour-count row "
            "is a real source edit, an accepted style divergence, or a native-reader deferral."
        )
    else:
        contour_step = (
            "Confirm the contour table is empty, then keep contour cleanup closed by rerunning "
            "the proof after any source edits."
        )
    proof_list = "".join(
        f"<li><a href='{html.escape(href)}'>{html.escape(label)}</a></li>" for label, href in links
    )
    sample_html = "\n".join(
        sample_block(label, text)
        for label, text in SAMPLES
        if label in {"Letter structures", "Joining texture", "Persian/Urdu letters"}
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Virtua Grotesk Arabic Next Review Batch</title>
<style>
{css()}
</style>
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const id = decodeURIComponent(window.location.hash.slice(1));
  if (!id) {{
    return;
  }}
  for (const section of document.querySelectorAll("section.sample")) {{
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
<h1>Virtua Grotesk Arabic Next Review Batch</h1>
<p>This focused page is generated from the current manual-review logs. It isolates the next unresolved batch: structure, wrong-glyph, and contour decisions. It is a review aid, not an automatic approval.</p>
<div class="summary">
<div class="pill">Batch: Structure And Wrong-Glyph Sweep</div>
<div class="pill">Visual rows: {len(visual_rows)}</div>
<div class="pill">Contour rows: {len(contours)}</div>
<div class="pill">Glyph proof links: {len(links)}</div>
</div>
<h2>Review Order</h2>
<ol>
<li>Open the glyph proof links and scan Regular, Medium, SemiBold, and Bold for missing, blank, clipped, duplicated, malformed, or wrong-codepoint Arabic glyphs.</li>
<li>{html.escape(contour_step)}</li>
<li>Only edit outlines after the proof and source agree that a drawing is wrong. Preserve Regular/Bold structure compatibility.</li>
<li>Regenerate with <code>make reports-only</code> and <code>make preflight-only</code> after any edits or decisions.</li>
</ol>
<h2>Target Samples</h2>
{sample_html}
<h2>Grouped Structure Prompts</h2>
<p>These are the current structure-triage prompts collapsed by codepoint. Use them as the short checklist before deciding whether the five structure-review rows pass, need fixes, or need deferral.</p>
{structure_prompt_table}
<h2>Mark Prompt Summary</h2>
<p>The current mark triage has no mechanical blockers. These zero-offset rows are visual proof checks for shadda stacking, not automatic failures.</p>
{mark_prompt_summary_table}
{mark_prompt_detail_table}
<h2>Visual Review Rows</h2>
{visual_table}
<h2>Contour Decision Rows</h2>
<p class="reference-note">Rubik previews are structural references only. Do not copy reference outlines into Virtua Grotesk.</p>
{contour_table}
<h2>Glyph Proof Links</h2>
<ul class="proofs">{proof_list}</ul>
</main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    output_path = Path(argv[1]) if len(argv) > 1 else OUTPUT
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    contours = contour_rows()
    risks = risk_rows()
    links = proof_links(output_path)
    renderers = preview_renderers()
    reference = reference_renderer()
    contour_table = table(
        ["Source glyph", "Fontspector glyph", "Preview", "Batch", "Category", "Review step", "Record decision"],
        [
            (
                f"<code>{html.escape(source)}</code>",
                f"<code>{html.escape(fontspector)}</code>",
                contour_preview(source, fontspector, renderers, reference),
                html.escape(batch),
                html.escape(category),
                html.escape(step),
                contour_decision_commands(source),
            )
            for source, fontspector, batch, category, _command, step in contours
        ],
    )
    risk_table = table(
        ["Font", "Codepoint", "Name", "Risks"],
        [
            (
                f"<code>{html.escape(font)}</code>",
                html.escape(codepoint),
                html.escape(name),
                html.escape(risks),
            )
            for font, codepoint, name, risks in risks
        ],
    )
    proof_list = "".join(
        f"<li><a href='{html.escape(href)}'>{html.escape(label)}</a></li>" for label, href in links
    )
    sample_html = "\n".join(sample_block(label, text) for label, text in SAMPLES)
    html_text = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Virtua Grotesk Arabic Manual Review Dashboard</title>
<style>
{css()}
</style>
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const id = decodeURIComponent(window.location.hash.slice(1));
  if (!id) {{
    return;
  }}
  for (const section of document.querySelectorAll("section.sample")) {{
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
<h1>Virtua Grotesk Arabic Manual Review Dashboard</h1>
<p>This generated dashboard embeds the current built fonts and gathers the fastest manual checks for the remaining Arabic drawing review. It is review evidence, not an automatic pass/fail result.</p>
<div class="summary">
<div class="pill">Visual review pending: {pending_count(VISUAL_LOG)}</div>
<div class="pill">Contour decisions pending: {pending_count(CONTOUR_LOG)}</div>
<div class="pill">Visual risk rows: {len(risks)}</div>
<div class="pill">GF proof files linked: {len(links)}</div>
</div>
<h2>Embedded Arabic Samples</h2>
{sample_html}
<h2>Visual Risk Rows</h2>
{risk_table}
<h2>Contour Decision Queue</h2>
<p class="reference-note">Rubik previews are structural references only. Do not copy reference outlines into Virtua Grotesk; use them to understand expected Arabic structure before judging the current Virtua drawing.</p>
{contour_table}
<h2>Google Fonts Proof Links</h2>
<ul class="proofs">{proof_list}</ul>
</main>
</body>
</html>
"""
    output_path.write_text(html_text, encoding="utf-8")
    next_batch_output = NEXT_BATCH_OUTPUT if output_path == OUTPUT else output_path.with_name("arabic-next-review-batch.html")
    next_batch_output.write_text(next_batch_html(next_batch_output), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(ROOT)}")
    print(f"Wrote {next_batch_output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
