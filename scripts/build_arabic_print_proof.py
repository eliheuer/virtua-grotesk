#!/usr/bin/env python3
"""Build a focused Arabic PDF proof with the local drawbot-skia runtime."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from fontTools.ttLib import TTFont

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run through `make arabic-print-proof` "
        "after setting DRAWBOT_SKIA_REPO=/path/to/drawbot-skia, or install drawbot_skia in .venv."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONTS = [
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
DEFAULT_OUTPUT = ROOT / "documentation/glyph-review/arabic-print-proof.pdf"
DEFAULT_INDEX_OUTPUT = ROOT / "documentation/glyph-review/arabic-print-proof-index.md"

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN = 36

SHAPING_SAMPLES = [
    ("salaam", "سلام"),
    ("arabic", "العربية"),
    ("bismillah", "بسم الله"),
    ("lam-alef", "لا"),
    ("Persian/Urdu letters", "پ چ ژ گ ک ی ہ ھ ے"),
    ("dot stacks", "ث ش ڤ ڨ ٹ پ چ گ"),
]

MARK_SAMPLES = [
    ("base + fatha", "بَ تَ كَ"),
    ("base + damma", "بُ تُ كُ"),
    ("base + kasra", "بِ تِ كِ"),
    ("shadda + marks", "بَّ بُّ بِّ"),
    ("tanween", "بً بٌ بٍ"),
    ("hamza marks", "أ إ"),
    ("dotted circle", "◌َ ◌ُ ◌ِ ◌ّ ◌ْ ◌ٓ ◌ٔ ◌ٕ"),
    ("small marks", "بؕ ب٘ بۛ"),
]

NUMERAL_SAMPLES = [
    ("Arabic-Indic", "٠١٢٣٤٥٦٧٨٩"),
    ("Extended Arabic-Indic", "۰۱۲۳۴۵۶۷۸۹"),
    ("Punctuation", "، ؛ ؟ ٪ ٫ ٬ ؍ ۔"),
]


def font_info(font_path: Path) -> dict[str, str | int]:
    font = TTFont(font_path)
    names = font["name"].names
    style_from_filename = font_path.stem.removeprefix("VirtuaGrotesk-")
    info: dict[str, str | int] = {
        "family": "",
        "style": style_from_filename,
        "glyphs": len(font.getGlyphOrder()),
    }
    for record in names:
        if record.nameID == 1 and not info["family"]:
            info["family"] = record.toUnicode()
        if record.nameID == 2 and not info["style"]:
            info["style"] = record.toUnicode()
    font.close()
    return info


def cmap_codepoints(font_path: Path) -> list[int]:
    font = TTFont(font_path)
    cmap = font.getBestCmap() or {}
    font.close()
    arabic = [
        cp
        for cp in sorted(cmap)
        if cp == 0x25CC
        or 0x0600 <= cp <= 0x06FF
        or 0x0750 <= cp <= 0x077F
        or 0x08A0 <= cp <= 0x08FF
    ]
    return arabic


def draw_header(db: Drawing, info: dict[str, str | int], title: str) -> None:
    db.save()
    db.font("Helvetica", 8)
    db.fill(0.45)
    db.text(f"{info['family']} {info['style']}", (MARGIN, PAGE_HEIGHT - 24))
    title_width = db.textSize(title)[0]
    db.text(title, (PAGE_WIDTH - MARGIN - title_width, PAGE_HEIGHT - 24))
    db.text(datetime.now().strftime("%Y-%m-%d"), (MARGIN, 18))
    db.restore()


def draw_rule(db: Drawing, y: float) -> None:
    db.save()
    db.stroke(0.82)
    db.strokeWidth(0.5)
    db.line((MARGIN, y), (PAGE_WIDTH - MARGIN, y))
    db.restore()


def draw_rtl(db: Drawing, font_path: Path, text: str, size: int, y: float) -> None:
    db.font(str(font_path), size)
    db.fill(0)
    width = db.textSize(text)[0]
    db.text(text, (PAGE_WIDTH - MARGIN - width, y))


def start_page(
    db: Drawing,
    info: dict[str, str | int],
    title: str,
    page_index: list[dict[str, str | int]],
    section: str,
) -> None:
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    page_index.append(
        {
            "page": len(page_index) + 1,
            "style": str(info["style"]),
            "title": title,
            "section": section,
        }
    )
    draw_header(db, info, title)


def sample_page(
    db: Drawing,
    font_path: Path,
    info: dict[str, str | int],
    page_index: list[dict[str, str | int]],
) -> None:
    start_page(
        db,
        info,
        "Arabic samples",
        page_index,
        "Shaping strings, Persian/Urdu letters, dot stacks, and mark attachment samples.",
    )

    y = PAGE_HEIGHT - 68
    db.font("Helvetica", 10)
    db.fill(0.45)
    db.text("SHAPING", (MARGIN, y))
    draw_rule(db, y - 8)
    y -= 40

    for label, sample in SHAPING_SAMPLES:
        db.font("Helvetica", 8)
        db.fill(0.45)
        db.text(label, (MARGIN, y + 10))
        draw_rtl(db, font_path, sample, 34, y)
        y -= 54

    y -= 8
    db.font("Helvetica", 10)
    db.fill(0.45)
    db.text("MARK ATTACHMENT", (MARGIN, y))
    draw_rule(db, y - 8)
    y -= 36

    for label, sample in MARK_SAMPLES:
        db.font("Helvetica", 8)
        db.fill(0.45)
        db.text(label, (MARGIN, y + 8))
        draw_rtl(db, font_path, sample, 28, y)
        y -= 38
        if y < 86:
            break


def numerals_page(
    db: Drawing,
    font_path: Path,
    info: dict[str, str | int],
    page_index: list[dict[str, str | int]],
) -> None:
    start_page(
        db,
        info,
        "Arabic numerals and punctuation",
        page_index,
        "Arabic-Indic digits, extended Arabic-Indic digits, and Arabic punctuation at multiple sizes.",
    )

    y = PAGE_HEIGHT - 84
    for label, sample in NUMERAL_SAMPLES:
        db.font("Helvetica", 9)
        db.fill(0.45)
        db.text(label, (MARGIN, y + 18))
        for size in (54, 36, 24, 18):
            draw_rtl(db, font_path, sample, size, y)
            y -= size * 1.25
        y -= 28


def glyph_grid_pages(
    db: Drawing,
    font_path: Path,
    info: dict[str, str | int],
    codepoints: list[int],
    page_index: list[dict[str, str | int]],
) -> None:
    cols = 10
    cell = (PAGE_WIDTH - 2 * MARGIN) / cols
    glyph_size = 24
    x_start = MARGIN
    y_start = PAGE_HEIGHT - 72

    start_page(
        db,
        info,
        "Arabic cmap grid",
        page_index,
        "Encoded Arabic and dotted-circle cmap grid.",
    )
    x = x_start
    y = y_start

    for cp in codepoints:
        if y - cell < MARGIN + 14:
            start_page(
                db,
                info,
                "Arabic cmap grid continued",
                page_index,
                "Encoded Arabic and dotted-circle cmap grid continuation.",
            )
            x = x_start
            y = y_start

        db.save()
        db.stroke(0.86)
        db.strokeWidth(0.5)
        db.fill(None)
        db.rect(x, y - cell, cell, cell)
        db.restore()

        char = chr(cp)
        db.font(str(font_path), glyph_size)
        db.fill(0)
        width = db.textSize(char)[0]
        db.text(char, (x + (cell - width) / 2, y - cell + 20))

        db.font("Helvetica", 5)
        db.fill(0.55)
        db.text(f"U+{cp:04X}", (x + 3, y - cell + 4))

        x += cell
        if x + cell > PAGE_WIDTH - MARGIN + 0.01:
            x = x_start
            y -= cell


def index_markdown(output_path: Path, page_index: list[dict[str, str | int]]) -> str:
    lines = [
        "# Arabic Print Proof Index",
        "",
        "This generated index maps `documentation/glyph-review/arabic-print-proof.pdf` pages to",
        "the Arabic visual-review pass. The PDF is a fast print/PDF aid; keep the",
        "Google Fonts HTML proof and source GLIF files authoritative for final",
        "review decisions.",
        "",
        f"- PDF: `{output_path.relative_to(ROOT)}`",
        f"- Pages: {len(page_index)}",
        "- Review log: `documentation/glyph-review/arabic-visual-review-log.md`",
        "- Current worksheet: `documentation/glyph-review/arabic-current-review-worksheet.md`",
        "- Next packet: `documentation/glyph-review/arabic-next-review-packet.md`",
        "",
        "## Page Map",
        "",
        "| Page | Style | Section | Use during review |",
        "| ---: | --- | --- | --- |",
    ]
    for entry in page_index:
        lines.append(
            f"| {entry['page']} | {entry['style']} | {entry['title']} | {entry['section']} |"
        )

    lines.extend(
        [
            "",
            "## Review Shortcut",
            "",
            "1. For the current structure/wrong-glyph sweep, scan the `Arabic cmap grid`",
            "   pages for each style first, then open the matching Google Fonts glyphs",
            "   proof if anything looks missing, clipped, blank, duplicated, malformed,",
            "   or wrong-codepoint.",
            "2. For marks and dotted-circle rows, scan each `Arabic samples` page, then",
            "   open `documentation/glyph-review/arabic-mark-review-proof.html` and the source glyphs",
            "   for anything that needs drawing or anchor edits.",
            "3. For numeral and punctuation rows, scan each `Arabic numerals and",
            "   punctuation` page before checking the proofer/text HTML.",
            "4. Record review outcomes only through",
            "   `make arabic-visual-review-update ...` after checking the linked proof",
            "   or source evidence.",
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

    for font_path in font_paths:
        info = font_info(font_path)
        codepoints = cmap_codepoints(font_path)
        sample_page(db, font_path, info, page_index)
        numerals_page(db, font_path, info, page_index)
        glyph_grid_pages(db, font_path, info, codepoints, page_index)

    db.saveImage(str(output_path))
    page_count = db.pageCount()
    db.endDrawing()
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise SystemExit(f"Arabic print proof was not written: {output_path}")
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
