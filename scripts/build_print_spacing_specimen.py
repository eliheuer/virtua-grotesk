#!/usr/bin/env python3
"""Build a landscape PDF specimen for print weight and spacing review."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from fontTools.ttLib import TTFont

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run through `make print-spacing-specimen` "
        "or set PYTHONPATH to /Users/eli/GH/repos/drawbot-skia/src."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONTS = [
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
DEFAULT_OUTPUT = ROOT / "documentation/proofs/print-spacing-specimen.pdf"
DEFAULT_INDEX_OUTPUT = ROOT / "documentation/proofs/print-spacing-specimen-index.md"

PAGE_WIDTH = 792
PAGE_HEIGHT = 612
MARGIN = 36
TEXT_LEFT = 110
TEXT_WIDTH = PAGE_WIDTH - TEXT_LEFT - MARGIN

LATIN_LOWER = "abcdefghijklmnopqrstuvwxyz"
LATIN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_DIGITS = "0123456789"
LATIN_PUNCT = ".,:;!?\"'()[]{}-/–—"

WATERFALL_LINES = [
    "Hamburgefontsiv 0123456789",
    "Typography on the UNIX System",
    "Pack my box with five dozen liquor jugs.",
]

TEXTURE_TEXT = (
    "The quick brown fox jumps over the lazy dog. Pack my box with five dozen "
    "liquor jugs. How vexingly quick daft zebras jump. Sphinx of black quartz, "
    "judge my vow. Two driven jocks help fax my big quiz."
)

ARABIC_SAMPLES = [
    ("shaping", "بسم الله الرحمن الرحيم"),
    ("letters", "سلام العربية كتاب قلم مدينة"),
    ("persian/urdu", "پ چ ژ گ ک ی ہ ھ ے"),
    ("marks", "بَ بُ بِ بّ بْ بً بٌ بٍ"),
    ("digits", "٠١٢٣٤٥٦٧٨٩  ۰۱۲۳۴۵۶۷۸۹"),
    ("punctuation", "، ؛ ؟ ٪ ٫ ٬ ؍ ۔"),
]


def font_info(font_path: Path) -> dict[str, str | int]:
    font = TTFont(font_path)
    info: dict[str, str | int] = {
        "family": "",
        "style": font_path.stem.removeprefix("VirtuaGrotesk-"),
        "glyphs": len(font.getGlyphOrder()),
        "version": "",
    }
    for record in font["name"].names:
        if record.nameID == 1 and not info["family"]:
            info["family"] = record.toUnicode()
        elif record.nameID == 2 and not info["style"]:
            info["style"] = record.toUnicode()
        elif record.nameID == 5 and not info["version"]:
            info["version"] = record.toUnicode()
    font.close()
    return info


def draw_header(
    db: Drawing,
    title: str,
    page_index: list[dict[str, str | int]],
    section: str,
) -> None:
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    page_index.append({"page": len(page_index) + 1, "title": title, "section": section})
    db.save()
    db.font("Helvetica", 8)
    db.fill(0.45)
    db.text("Virtua Grotesk print spacing specimen", (MARGIN, PAGE_HEIGHT - 22))
    title_width = db.textSize(title)[0]
    db.text(title, (PAGE_WIDTH - MARGIN - title_width, PAGE_HEIGHT - 22))
    db.text(datetime.now().strftime("%Y-%m-%d"), (MARGIN, 16))
    db.restore()


def rule(db: Drawing, y: float) -> None:
    db.save()
    db.stroke(0.78)
    db.strokeWidth(0.5)
    db.line((MARGIN, y), (PAGE_WIDTH - MARGIN, y))
    db.restore()


def label(db: Drawing, text: str, x: float, y: float, size: int = 8) -> None:
    db.save()
    db.font("Helvetica", size)
    db.fill(0.48)
    db.text(text, (x, y))
    db.restore()


def font_label(font_path: Path) -> str:
    info = font_info(font_path)
    return str(info["style"])


def draw_left_label(db: Drawing, text: str, y: float) -> None:
    db.save()
    db.font("Helvetica", 7)
    db.fill(0.48)
    db.text(text, (MARGIN, y))
    db.restore()


def draw_rtl(db: Drawing, font_path: Path, text: str, size: int, y: float) -> None:
    db.font(str(font_path), size)
    db.fill(0)
    width = db.textSize(text)[0]
    db.text(text, (PAGE_WIDTH - MARGIN - width, y))


def cover_page(db: Drawing, font_paths: list[Path], page_index: list[dict[str, str | int]]) -> None:
    info = font_info(font_paths[0])
    draw_header(db, "Weight axis overview", page_index, "Landscape waterfall across all static weights.")
    y = PAGE_HEIGHT - 90
    db.font(str(font_paths[-1]), 54)
    db.fill(0)
    db.text(str(info["family"] or "Virtua Grotesk"), (MARGIN, y))
    y -= 42
    label(db, f"{info['version']}  /  {len(font_paths)} static review weights  /  landscape letter PDF", MARGIN, y)
    y -= 38
    rule(db, y)
    y -= 42

    for font_path in font_paths:
        style = font_label(font_path)
        draw_left_label(db, style, y + 8)
        db.font(str(font_path), 34)
        db.fill(0)
        db.text("Hamburgefontsiv 0123456789", (TEXT_LEFT, y))
        y -= 62

    y -= 8
    rule(db, y)
    y -= 24
    label(
        db,
        "Use this PDF on paper for weight balance, sidebearing rhythm, numerals, punctuation, and Arabic texture review.",
        MARGIN,
        y,
    )


def waterfall_page(db: Drawing, font_paths: list[Path], page_index: list[dict[str, str | int]]) -> None:
    draw_header(db, "Latin waterfalls", page_index, "Latin weight and size comparisons.")
    y = PAGE_HEIGHT - 62
    sizes = [42, 30, 22, 16, 12, 9]
    for font_path in font_paths:
        draw_left_label(db, font_label(font_path), y - 2)
        for size, sample in zip(sizes, WATERFALL_LINES * 2, strict=False):
            db.font(str(font_path), size)
            db.fill(0)
            db.text(sample, (TEXT_LEFT, y))
            y -= size * 1.22
        y -= 16
        if y < 110 and font_path != font_paths[-1]:
            draw_header(db, "Latin waterfalls continued", page_index, "Latin weight and size comparisons.")
            y = PAGE_HEIGHT - 62


def generated_spacing_strings(chars: str, anchors: str) -> list[str]:
    lines = []
    for anchor in anchors:
        line = anchor + anchor.join(chars) + anchor
        lines.append(line)
    return lines


def spacing_page(
    db: Drawing,
    font_path: Path,
    page_index: list[dict[str, str | int]],
    title: str,
    chars: str,
    anchors: str,
) -> None:
    draw_header(db, f"{font_label(font_path)} {title}", page_index, f"Generated {title.lower()} strings.")
    y = PAGE_HEIGHT - 56
    db.font(str(font_path), 10)
    db.fill(0)
    for line in generated_spacing_strings(chars, anchors):
        if db.textSize(line)[0] > TEXT_WIDTH:
            while db.textSize(line)[0] > TEXT_WIDTH and len(line) > 18:
                line = line[:-2]
        db.text(line, (TEXT_LEFT, y))
        draw_left_label(db, line[:1], y)
        y -= 14
        if y < 42:
            draw_header(db, f"{font_label(font_path)} {title} continued", page_index, f"Generated {title.lower()} strings.")
            y = PAGE_HEIGHT - 56


def texture_page(db: Drawing, font_paths: list[Path], page_index: list[dict[str, str | int]]) -> None:
    draw_header(db, "Paragraph texture", page_index, "Short columns for print color, rhythm, and weight comparison.")
    col_gap = 20
    col_w = (PAGE_WIDTH - 2 * MARGIN - col_gap) / 2
    row_h = 208
    positions = [
        (MARGIN, PAGE_HEIGHT - 78 - row_h),
        (MARGIN + col_w + col_gap, PAGE_HEIGHT - 78 - row_h),
        (MARGIN, PAGE_HEIGHT - 318 - row_h),
        (MARGIN + col_w + col_gap, PAGE_HEIGHT - 318 - row_h),
    ]
    for font_path, (x, y) in zip(font_paths, positions, strict=True):
        label(db, font_label(font_path), x, y + row_h + 12)
        db.font(str(font_path), 11)
        db.fill(0)
        db.textBox(TEXTURE_TEXT, (x, y, col_w, row_h))
        db.save()
        db.stroke(0.88)
        db.strokeWidth(0.4)
        db.fill(None)
        db.rect(x, y, col_w, row_h)
        db.restore()


def numeral_punctuation_page(db: Drawing, font_paths: list[Path], page_index: list[dict[str, str | int]]) -> None:
    draw_header(db, "Numerals and punctuation", page_index, "Figures and punctuation across weights.")
    samples = [
        ("digits", LATIN_DIGITS),
        ("tabular contexts", "00 11 22 33 44 55 66 77 88 99"),
        ("punctuation", LATIN_PUNCT),
        ("mixed", "H1 H2 H3 10:45 12/24 100% $123.45"),
    ]
    y = PAGE_HEIGHT - 74
    for font_path in font_paths:
        draw_left_label(db, font_label(font_path), y + 4)
        for sample_label, text in samples:
            label(db, sample_label, TEXT_LEFT, y + 18, 6)
            db.font(str(font_path), 25)
            db.fill(0)
            db.text(text, (TEXT_LEFT + 70, y))
            y -= 42
        y -= 18


def arabic_weight_page(db: Drawing, font_paths: list[Path], page_index: list[dict[str, str | int]]) -> None:
    draw_header(db, "Arabic weight and spacing", page_index, "Arabic shaping, marks, numerals, and punctuation across weights.")
    y = PAGE_HEIGHT - 62
    for font_path in font_paths:
        draw_left_label(db, font_label(font_path), y + 4)
        for sample_label, text in ARABIC_SAMPLES:
            label(db, sample_label, TEXT_LEFT, y + 11, 6)
            draw_rtl(db, font_path, text, 24, y)
            y -= 35
        y -= 10
        if y < 120 and font_path != font_paths[-1]:
            draw_header(db, "Arabic weight and spacing continued", page_index, "Arabic shaping, marks, numerals, and punctuation.")
            y = PAGE_HEIGHT - 62


def glyph_grid_page(db: Drawing, font_path: Path, page_index: list[dict[str, str | int]]) -> None:
    font = TTFont(font_path)
    cmap = sorted(cp for cp in (font.getBestCmap() or {}) if cp >= 0x20 and cp != 0x00A0)
    font.close()
    draw_header(db, f"{font_label(font_path)} encoded glyph grid", page_index, "Compact encoded cmap grid for print scanning.")
    cols = 18
    cell_w = (PAGE_WIDTH - 2 * MARGIN) / cols
    cell_h = 34
    x = MARGIN
    y = PAGE_HEIGHT - 58
    for cp in cmap:
        if y - cell_h < 36:
            draw_header(db, f"{font_label(font_path)} encoded glyph grid continued", page_index, "Compact encoded cmap grid continuation.")
            x = MARGIN
            y = PAGE_HEIGHT - 58
        db.save()
        db.stroke(0.88)
        db.strokeWidth(0.35)
        db.fill(None)
        db.rect(x, y - cell_h, cell_w, cell_h)
        db.restore()
        char = chr(cp)
        db.font(str(font_path), 14)
        db.fill(0)
        text_w = db.textSize(char)[0]
        db.text(char, (x + (cell_w - text_w) / 2, y - cell_h + 12))
        label(db, f"{cp:04X}", x + 2, y - cell_h + 3, 4)
        x += cell_w
        if x + cell_w > PAGE_WIDTH - MARGIN + 0.01:
            x = MARGIN
            y -= cell_h


def index_markdown(output_path: Path, page_index: list[dict[str, str | int]]) -> str:
    lines = [
        "# Print Spacing Specimen Index",
        "",
        "This generated index maps the landscape print/PDF specimen used for",
        "weight, spacing, texture, numeral, punctuation, and Arabic review.",
        "",
        f"- PDF: `{output_path.relative_to(ROOT)}`",
        f"- Pages: {len(page_index)}",
        "- Build command: `make print-spacing-specimen`",
        "",
        "## Page Map",
        "",
        "| Page | Title | Review focus |",
        "| ---: | --- | --- |",
    ]
    for entry in page_index:
        lines.append(f"| {entry['page']} | {entry['title']} | {entry['section']} |")
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- Print in landscape mode at 100% scale; avoid fit-to-page scaling when",
            "  judging spacing and weight.",
            "- Use this PDF for paper review, then verify any suspected issue in the",
            "  source UFOs and Google Fonts HTML proof before recording final status.",
            "- Regenerate after drawing, spacing, kerning, metrics, or build changes.",
            "",
        ]
    )
    return "\n".join(lines)


def build(font_paths: list[Path], output_path: Path, index_output: Path | None) -> None:
    missing = [path for path in font_paths if not path.exists()]
    if missing:
        raise SystemExit("Missing font files: " + ", ".join(str(path) for path in missing))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    db = Drawing()
    db.newDrawing()
    page_index: list[dict[str, str | int]] = []

    cover_page(db, font_paths, page_index)
    waterfall_page(db, font_paths, page_index)
    texture_page(db, font_paths, page_index)
    numeral_punctuation_page(db, font_paths, page_index)
    arabic_weight_page(db, font_paths, page_index)
    for font_path in font_paths:
        spacing_page(db, font_path, page_index, "lowercase spacing", LATIN_LOWER, "noheisav")
        spacing_page(db, font_path, page_index, "uppercase spacing", LATIN_UPPER, "HODENS")
    glyph_grid_page(db, font_paths[0], page_index)

    db.saveImage(str(output_path))
    page_count = db.pageCount()
    db.endDrawing()
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise SystemExit(f"Print spacing specimen was not written: {output_path}")
    if index_output is not None:
        index_output.parent.mkdir(parents=True, exist_ok=True)
        index_output.write_text(index_markdown(output_path, page_index), encoding="utf-8")

    print(f"Wrote {output_path}")
    print(f"Pages: {page_count}")
    if index_output is not None:
        print(f"Wrote {index_output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--index-output", type=Path, default=DEFAULT_INDEX_OUTPUT)
    parser.add_argument("fonts", nargs="*", type=Path, default=DEFAULT_FONTS)
    args = parser.parse_args()

    build(
        [path.resolve() for path in args.fonts],
        args.output.resolve(),
        args.index_output.resolve() if args.index_output else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
