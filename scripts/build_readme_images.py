#!/usr/bin/env python3
"""Build DrawBot-skia PNG images for the project README."""

from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run through `make readme-images` after "
        "setting DRAWBOT_SKIA_REPO=/path/to/drawbot-skia, or install "
        "drawbot_skia in .venv."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "fonts/ttf"
OUTPUT_DIR = ROOT / "documentation/assets/readme"

FONTS = {
    "Regular": FONT_DIR / "VirtuaGrotesk-Regular.ttf",
    "Medium": FONT_DIR / "VirtuaGrotesk-Medium.ttf",
    "SemiBold": FONT_DIR / "VirtuaGrotesk-SemiBold.ttf",
    "Bold": FONT_DIR / "VirtuaGrotesk-Bold.ttf",
}

WIDTH = 2048
HEIGHT = 1024
MARGIN = 96

INK = (0.86, 0.86, 0.82)
PAPER = (0.13, 0.13, 0.13)
MUTED = (0.58, 0.58, 0.54)
RULE = (0.34, 0.34, 0.32)
GRID_MINOR = (0.22, 0.22, 0.21)
GRID_MAJOR = (0.42, 0.42, 0.39)
ACCENT = (0.72, 0.72, 0.68)
BLUE = (0.78, 0.78, 0.74)


def require_fonts() -> None:
    missing = [str(path.relative_to(ROOT)) for path in FONTS.values() if not path.exists()]
    if missing:
        raise SystemExit(
            "Built fonts are missing. Run `make build` first. Missing: "
            + ", ".join(missing)
        )


def font_metrics(font_path: Path) -> dict[str, int | str]:
    font = TTFont(font_path)
    metrics = {
        "upm": font["head"].unitsPerEm,
        "ascender": font["hhea"].ascent,
        "descender": font["hhea"].descent,
        "cap_height": font["OS/2"].sCapHeight,
        "x_height": font["OS/2"].sxHeight,
        "family": font["name"].getDebugName(1) or "Virtua Grotesk",
    }
    font.close()
    return metrics


def page() -> Drawing:
    db = Drawing()
    db.newPage(WIDTH, HEIGHT)
    db.fill(*PAPER)
    db.rect(0, 0, WIDTH, HEIGHT)
    return db


def save(db: Drawing, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    db.saveImage(str(path))
    print(path.relative_to(ROOT))


def label(db: Drawing, text: str, x: float, y: float, size: int = 24) -> None:
    db.save()
    db.stroke(None)
    db.font("Helvetica")
    db.fontSize(size)
    db.fill(*MUTED)
    db.text(text, (x, y))
    db.restore()


def title(db: Drawing, heading: str, subheading: str) -> None:
    db.save()
    db.stroke(None)
    db.font(str(FONTS["Bold"]))
    db.fontSize(72)
    db.fill(*INK)
    db.text(heading, (MARGIN, HEIGHT - MARGIN - 24))
    db.font("Helvetica")
    db.fontSize(25)
    db.fill(*MUTED)
    db.text(subheading, (MARGIN, HEIGHT - MARGIN - 68))
    db.stroke(*RULE)
    db.strokeWidth(2)
    db.line((MARGIN, HEIGHT - MARGIN - 100), (WIDTH - MARGIN, HEIGHT - MARGIN - 100))
    db.restore()


def draw_glyphset_overview() -> None:
    db = page()
    title(
        db,
        "Virtua Grotesk",
        "Weight axis overview and core Latin glyph set",
    )

    y = HEIGHT - 290
    samples = [
        ("Regular", "ABCDEFGHIJKLM"),
        ("Regular", "NOPQRSTUVWXYZ"),
        ("Medium", "abcdefghijklm"),
        ("Medium", "nopqrstuvwxyz"),
        ("SemiBold", "0123456789"),
        ("Bold", ".,:;!?&@#$/()[]{}"),
    ]
    for style, text in samples:
        label(db, style, MARGIN, y + 20)
        db.font(str(FONTS[style]))
        db.fontSize(74)
        db.stroke(None)
        db.fill(*INK)
        db.text(text, (MARGIN + 170, y))
        y -= 86

    y -= 8
    db.stroke(*RULE)
    db.strokeWidth(2)
    db.line((MARGIN, y), (WIDTH - MARGIN, y))
    db.stroke(None)

    y -= 47
    for style, text in [
        ("Regular", "Hamburgefontsiv"),
        ("Medium", "Sphinx of black quartz"),
        ("SemiBold", "Pack my box with five dozen"),
        ("Bold", "The quick brown fox jumps"),
    ]:
        label(db, f"wght {style}", MARGIN, y + 9, 20)
        db.font(str(FONTS[style]))
        db.fontSize(36)
        db.stroke(None)
        db.fill(*INK)
        db.text(text, (MARGIN + 170, y))
        y -= 42

    save(db, OUTPUT_DIR / "glyphset-overview.png")


def draw_metric_line(
    db: Drawing,
    name: str,
    y: float,
    x0: float,
    x1: float,
    color: tuple[float, float, float],
) -> None:
    db.save()
    db.stroke(None)
    db.stroke(*color)
    db.strokeWidth(3)
    db.line((x0, y), (x1, y))
    db.font("Helvetica")
    db.fontSize(18)
    db.stroke(None)
    db.fill(*color)
    db.text(name, (x0 + 14, y + 8))
    db.restore()


def draw_aa_grid() -> None:
    metrics = font_metrics(FONTS["Regular"])
    upm = int(metrics["upm"])
    ascender = int(metrics["ascender"])
    descender = int(metrics["descender"])
    cap_height = int(metrics["cap_height"])
    x_height = int(metrics["x_height"])

    db = page()
    title(
        db,
        "Aa Construction",
        "1024 UPM, even coordinates, 16-unit chamfer logic",
    )

    grid_x = 170
    grid_y = 115
    grid_w = 1230
    grid_h = 720
    scale = grid_h / (ascender - descender)
    baseline_y = grid_y + (-descender * scale)

    db.save()
    db.stroke(*GRID_MINOR)
    db.strokeWidth(1)
    for unit in range(descender, ascender + 1, 64):
        y = baseline_y + unit * scale
        db.line((grid_x, y), (grid_x + grid_w, y))
    for unit in range(0, 1537, 64):
        x = grid_x + unit * scale
        if x <= grid_x + grid_w:
            db.line((x, grid_y), (x, grid_y + grid_h))
    db.stroke(*GRID_MAJOR)
    db.strokeWidth(2)
    for unit in range(0, 1537, 128):
        x = grid_x + unit * scale
        if x <= grid_x + grid_w:
            db.line((x, grid_y), (x, grid_y + grid_h))
    db.restore()

    draw_metric_line(db, "ascender 832", baseline_y + 832 * scale, grid_x, grid_x + grid_w, MUTED)
    draw_metric_line(db, "cap 768", baseline_y + cap_height * scale, grid_x, grid_x + grid_w, BLUE)
    draw_metric_line(db, "x-height 576", baseline_y + x_height * scale, grid_x, grid_x + grid_w, ACCENT)
    draw_metric_line(db, "baseline", baseline_y, grid_x, grid_x + grid_w, INK)
    draw_metric_line(db, "descender -256", baseline_y + (-256 * scale), grid_x, grid_x + grid_w, MUTED)

    db.font(str(FONTS["Regular"]))
    db.fontSize(upm * scale)
    db.stroke(None)
    db.fill(*INK)
    db.text("Aa", (grid_x + 78, baseline_y))

    x = grid_x + grid_w + 78
    y = grid_y + grid_h - 36
    notes = [
        ("2", "source grid"),
        ("16", "chamfer module"),
        ("64", "visible guide step"),
        ("128", "major guide step"),
    ]
    for value, note in notes:
        db.font(str(FONTS["Bold"]))
        db.fontSize(48)
        db.stroke(None)
        db.fill(*INK)
        db.text(value, (x, y))
        label(db, note, x + 112, y + 11, 23)
        y -= 78

    db.stroke(*ACCENT)
    db.strokeWidth(3)
    db.line((grid_x + 210, baseline_y + 715 * scale), (grid_x + 276, baseline_y + 768 * scale))
    db.line((grid_x + 286, baseline_y + 768 * scale), (grid_x + 350, baseline_y + 715 * scale))
    db.stroke(None)
    label(db, "45-degree bevel joins", x, y - 12, 24)

    save(db, OUTPUT_DIR / "aa-grid.png")


def draw_text_sizes() -> None:
    db = page()
    title(
        db,
        "Text Sizes",
        "Regular text proof from display down to interface sizes",
    )

    samples = [
        (92, "Virtua Grotesk"),
        (62, "Chamfered corners, monolinear strokes"),
        (42, "The quick brown fox jumps over the lazy dog."),
        (30, "Pack my box with five dozen liquor jugs."),
        (22, "Sphinx of black quartz, judge my vow. 0123456789"),
        (16, "Small text remains open, sturdy, and useful for interface systems."),
        (12, "Caption size: regular rhythm, clear counters, compact spacing, and sharp construction detail."),
    ]
    y = HEIGHT - 304
    for size, text in samples:
        label(db, f"{size} px", MARGIN, y + size * 0.26, 20)
        db.font(str(FONTS["Regular"]))
        db.fontSize(size)
        db.stroke(None)
        db.fill(*INK)
        db.text(text, (MARGIN + 122, y))
        y -= max(58, size * 1.12)

    y -= 6
    db.stroke(*RULE)
    db.strokeWidth(2)
    db.line((MARGIN, y), (WIDTH - MARGIN, y))
    db.stroke(None)
    y -= 52

    for style in ["Regular", "Medium", "SemiBold", "Bold"]:
        label(db, style, MARGIN, y + 8, 20)
        db.font(str(FONTS[style]))
        db.fontSize(38)
        db.stroke(None)
        db.fill(*INK)
        db.text("Designing software for careful reading.", (MARGIN + 122, y))
        y -= 45

    save(db, OUTPUT_DIR / "text-sizes.png")


def main() -> None:
    require_fonts()
    draw_glyphset_overview()
    draw_aa_grid()
    draw_text_sizes()


if __name__ == "__main__":
    main()
