#!/usr/bin/env python3
"""Build square DrawBot-skia PNG specimen images for social media posts.

Layout references: Klim's Die Grotesk poster lockups (type fills the frame,
one accent color), Geist's Instagram specimen set (header captions, hairline
rules, size waterfall, coded punctuation strings, giant cropped lowercase),
and Inter's character-grid density.

Weights are discovered from fonts/ttf/*.ttf at runtime (style name from the
name table, ordering from OS/2 usWeightClass), so adding or removing
instances changes the output set without script edits.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from fontTools.misc.fixedTools import floatToFixedToStr
from fontTools.ttLib import TTFont

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run `make setup` to install it in .venv."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "fonts/ttf"
OUTPUT_DIR = ROOT / "documentation/assets/social"

WIDTH = 2048
HEIGHT = 2048
MARGIN = 128

INK = (0.86, 0.86, 0.82)
PAPER = (0.13, 0.13, 0.13)
MUTED = (0.58, 0.58, 0.54)
RULE = (0.34, 0.34, 0.32)
HAIRLINE = (0.24, 0.24, 0.23)
RED = (1.0, 0.29, 0.24)  # the source markColor, used as the single accent

GRID_VIEW = False  # Toggle for a red layout grid overlay


class Style:
    def __init__(self, path: Path):
        font = TTFont(path)
        self.path = path
        self.name = (
            font["name"].getDebugName(17)
            or font["name"].getDebugName(2)
            or path.stem
        )
        self.weight_class = font["OS/2"].usWeightClass
        self.upm = font["head"].unitsPerEm
        self.version = f"v{floatToFixedToStr(font['head'].fontRevision, 16)}"
        self.family = font["name"].getDebugName(16) or font["name"].getDebugName(1)
        glyph_order = font.getGlyphOrder()
        self.tab_width = (
            font["hmtx"]["zero.tf"][0] if "zero.tf" in glyph_order else None
        )
        font.close()

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")


def discover_styles() -> list[Style]:
    paths = sorted(FONT_DIR.glob("*.ttf"))
    if not paths:
        raise SystemExit("No fonts in fonts/ttf/. Run `make build` first.")
    return sorted((Style(p) for p in paths), key=lambda s: s.weight_class)


STYLES = discover_styles()
LIGHTEST = STYLES[0]
HEAVIEST = STYLES[-1]


def style_near(weight_class: int) -> Style:
    return min(STYLES, key=lambda s: abs(s.weight_class - weight_class))


def git_hash() -> str:
    return subprocess.check_output(
        "git rev-parse --short HEAD", shell=True, cwd=ROOT
    ).decode().strip()


def grid(db: Drawing) -> None:
    db.save()
    db.stroke(1, 0, 0, 0.75)
    db.strokeWidth(2)
    db.fill(None)
    db.rect(MARGIN, MARGIN, WIDTH - MARGIN * 2, HEIGHT - MARGIN * 2)
    step = MARGIN / 2
    x = MARGIN
    while x <= WIDTH - MARGIN:
        db.line((x, MARGIN), (x, HEIGHT - MARGIN))
        x += step
    y = MARGIN
    while y <= HEIGHT - MARGIN:
        db.line((MARGIN, y), (WIDTH - MARGIN, y))
        y += step
    db.line((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    db.line((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))
    db.restore()


def page() -> Drawing:
    db = Drawing()
    db.newPage(WIDTH, HEIGHT)
    db.fill(*PAPER)
    db.rect(0, 0, WIDTH, HEIGHT)
    if GRID_VIEW:
        grid(db)
    return db


def hairline(db: Drawing, y: float) -> None:
    db.save()
    db.stroke(*HAIRLINE)
    db.strokeWidth(2)
    db.line((0, y), (WIDTH, y))
    db.restore()


def frame(db: Drawing, footer: bool = True, note: str | None = None) -> None:
    """Geist-style header and footer captions, set in the font itself."""
    db.save()
    db.stroke(None)
    db.font(str(LIGHTEST.path))
    db.fontSize(34)
    db.fill(*MUTED)
    db.text(LIGHTEST.family, (MARGIN, HEIGHT - MARGIN - 24))
    right = note if note else "Licensed under OFL"
    db.text(right, (WIDTH - MARGIN, HEIGHT - MARGIN - 24), align="right")
    if footer:
        db.text("Open source", (MARGIN, MARGIN))
        db.text(
            f"{LIGHTEST.version} · {git_hash()} · github.com/eliheuer/virtua-grotesk",
            (WIDTH - MARGIN, MARGIN),
            align="right",
        )
    db.restore()
    hairline(db, HEIGHT - MARGIN - 56)
    if footer:
        hairline(db, MARGIN + 76)


def fit_size(db: Drawing, txt: str, style: Style, target_w: float) -> float:
    db.font(str(style.path))
    db.fontSize(100)
    return 100 * target_w / db.textSize(txt)[0]


def save(db: Drawing, name: str) -> None:
    path = OUTPUT_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    db.saveImage(str(path))
    print(path.relative_to(ROOT))


def draw_hero() -> None:
    """Klim-style lockup: each line fit to the full inner width."""
    db = page()
    inner = WIDTH - MARGIN * 2
    s1 = fit_size(db, "Virtua", HEAVIEST, inner)
    s2 = fit_size(db, "Grotesk", HEAVIEST, inner)
    cap1 = 0.75 * s1
    cap2 = 0.75 * s2
    gap = 110
    top = HEIGHT - MARGIN - 56
    bottom = MARGIN + 76
    block = cap1 + gap + cap2
    baseline1 = (top + bottom) / 2 + block / 2 - cap1
    baseline2 = baseline1 - gap - cap2

    db.fill(*INK)
    db.font(str(HEAVIEST.path))
    db.fontSize(s1)
    db.text("Virtua", (WIDTH / 2, baseline1), align="center")
    db.fontSize(s2)
    db.text("Grotesk", (WIDTH / 2, baseline2), align="center")

    frame(db)
    save(db, "social-01-hero.png")


def draw_weights() -> None:
    db = page()
    rows = len(STYLES)
    top = 1490
    step = min(390, (top - 300) / max(rows - 1, 1))
    y = top
    for style in STYLES:
        db.font(str(LIGHTEST.path))
        db.fontSize(40)
        db.fill(*MUTED)
        db.text(f"wght {style.weight_class}", (MARGIN, y + 290))
        db.font(str(style.path))
        db.fontSize(320)
        db.fill(*INK)
        db.text("Hamburg", (MARGIN, y))
        y -= step

    frame(db)
    save(db, "social-02-weights.png")


def draw_alphabet(style: Style) -> None:
    db = page()
    lines = [
        "ABCDEFGHIJ",
        "KLMNOPQRST",
        "UVWXYZ&?!",
        "abcdefghijklm",
        "nopqrstuvwxyz",
        "0123456789",
    ]
    y = 1620
    db.font(str(style.path))
    for txt in lines:
        db.fontSize(230)
        db.fill(*INK)
        db.text(txt, (WIDTH / 2, y), align="center")
        y -= 276

    frame(db, note=f"{style.name} · wght {style.weight_class}")
    save(db, f"social-03-alphabet-{style.slug}.png")


def draw_tabular() -> None:
    style = style_near(600)
    if style.tab_width is None:
        print("skipping tabular image: no zero.tf glyph in", style.path.name)
        return

    db = page()
    db.font(str(HEAVIEST.path))
    db.fontSize(170)
    db.fill(*INK)
    db.text("Tabular Figures", (WIDTH / 2, 1660), align="center")

    size = 270
    rows = ["650118", "204937", "881265"]
    tab = style.tab_width / style.upm * size
    block_w = tab * len(rows[0])
    x0 = (WIDTH - block_w) / 2
    y = 1280

    db.save()
    db.stroke(*RULE)
    db.strokeWidth(2)
    top = y + size * 0.82
    bottom = y - 2 * 330 - size * 0.12
    for i in range(len(rows[0]) + 1):
        x = x0 + i * tab
        db.line((x, bottom), (x, top))
    db.restore()

    db.font(str(style.path))
    db.fontSize(size)
    db.fill(*INK)
    db.openTypeFeatures(tnum=True)
    for row in rows:
        db.text(row, (x0, y))
        y -= 330
    db.openTypeFeatures(resetFeatures=True)

    db.font(str(LIGHTEST.path))
    db.fontSize(56)
    db.fill(*MUTED)
    db.text("tnum · uniform widths on every weight", (WIDTH / 2, 330), align="center")

    frame(db)
    save(db, "social-04-tabular.png")


def draw_chamfer() -> None:
    db = page()
    db.font(str(LIGHTEST.path))
    db.fontSize(56)
    db.fill(*MUTED)
    db.text("16-unit chamfered corners", (WIDTH / 2, HEIGHT - MARGIN - 160), align="center")

    db.font(str(HEAVIEST.path))
    db.fontSize(1340)
    db.fill(*INK)
    db.text("Aa", (WIDTH / 2, 540), align="center")

    frame(db)
    save(db, "social-05-chamfer.png")


def draw_waterfall() -> None:
    """Geist-style split: point sizes on the left, the name on the right."""
    style = style_near(600)
    db = page()
    split = WIDTH * 0.36
    db.save()
    db.stroke(*HAIRLINE)
    db.strokeWidth(2)
    db.line((split, MARGIN + 76), (split, HEIGHT - MARGIN - 56))
    db.restore()

    sizes = [236, 196, 162, 132, 106, 82, 62, 46]
    y = 1560
    for index, size in enumerate(sizes):
        tint = max(0.30, 0.86 - index * 0.075)
        db.font(str(style.path))
        db.fontSize(size)
        db.fill(tint, tint, tint * 0.96)
        db.text(str(size), (split - 56, y), align="right")
        db.fill(*INK)
        name = "Virtua©" if index < 5 else "Grotesk©"
        db.text(name, (split + 56, y))
        y -= size * 1.16 + 14

    frame(db)
    save(db, "social-06-waterfall.png")


def draw_symbols() -> None:
    """Geist-style coded strings, in the source markColor red."""
    db = page()
    rows = [
        "*{Virtua}*",
        "<GROTESK>",
        "(+Chamfer)",
        "@16/1024_u",
        "#OFL—2026",
    ]
    y = 1500
    db.fill(*RED)
    db.font(str(LIGHTEST.path))
    for row in rows:
        db.fontSize(220)
        db.text(row, (WIDTH / 2, y), align="center")
        y -= 290

    frame(db)
    save(db, "social-07-symbols.png")


def draw_lowercase() -> None:
    """Geist-style giant lowercase, weights receding in tint steps."""
    db = page()
    layers = [
        (LIGHTEST, 0.32, 1940),
        (style_near(600), 0.52, 1040),
        (HEAVIEST, 0.86, 140),
    ]
    for style, tint, x in reversed(layers):
        db.font(str(style.path))
        db.fontSize(2300)
        db.fill(tint, tint, tint * 0.96)
        db.text("a", (x, -130))

    db.font(str(LIGHTEST.path))
    db.fontSize(46)
    db.fill(*MUTED)
    db.textBox(
        "Virtua Grotesk is a geometric grotesk with 16-unit chamfered "
        "corners — monolinear strokes and a retro-futurist technical "
        "character, drawn with modern precision on a 1024-unit grid.",
        (MARGIN, HEIGHT - MARGIN - 420, 1280, 300),
    )

    frame(db, footer=False)
    save(db, "social-08-lowercase.png")


def main() -> None:
    draw_hero()
    draw_weights()
    for style in STYLES:
        draw_alphabet(style)
    draw_tabular()
    draw_chamfer()
    draw_waterfall()
    draw_symbols()
    draw_lowercase()


if __name__ == "__main__":
    main()
