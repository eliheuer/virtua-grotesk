#!/usr/bin/env python3
"""Build square DrawBot-skia PNG specimen images for social media posts.

Layout references: Klim's Die Grotesk poster lockups (type fills the frame,
one accent color), Geist's Instagram specimen set (header captions, hairline
rules, size waterfall, coded punctuation strings, giant cropped lowercase),
and Inter's character-grid density.
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

FONTS = {
    "Regular": FONT_DIR / "VirtuaGrotesk-Regular.ttf",
    "Medium": FONT_DIR / "VirtuaGrotesk-Medium.ttf",
    "SemiBold": FONT_DIR / "VirtuaGrotesk-SemiBold.ttf",
    "Bold": FONT_DIR / "VirtuaGrotesk-Bold.ttf",
}

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

UPM = 1024
TAB_WIDTHS = {"Regular": 664, "Medium": 680, "SemiBold": 696, "Bold": 712}


def require_fonts() -> None:
    missing = [str(p.relative_to(ROOT)) for p in FONTS.values() if not p.exists()]
    if missing:
        raise SystemExit(
            "Built fonts are missing. Run `make build` first. Missing: "
            + ", ".join(missing)
        )


def font_version() -> str:
    font = TTFont(FONTS["Regular"])
    version = floatToFixedToStr(font["head"].fontRevision, 16)
    font.close()
    return f"v{version}"


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


def frame(db: Drawing, footer: bool = True) -> None:
    """Geist-style header and footer captions, set in Virtua Grotesk."""
    db.save()
    db.stroke(None)
    db.font(str(FONTS["Regular"]))
    db.fontSize(34)
    db.fill(*MUTED)
    db.text("Virtua Grotesk", (MARGIN, HEIGHT - MARGIN - 24))
    db.text("Licensed under OFL", (WIDTH - MARGIN, HEIGHT - MARGIN - 24), align="right")
    if footer:
        db.text("Open source", (MARGIN, MARGIN))
        db.text(
            f"{font_version()} · {git_hash()} · github.com/eliheuer/virtua-grotesk",
            (WIDTH - MARGIN, MARGIN),
            align="right",
        )
    db.restore()
    hairline(db, HEIGHT - MARGIN - 56)
    if footer:
        hairline(db, MARGIN + 76)


def fit_size(db: Drawing, txt: str, style: str, target_w: float) -> float:
    db.font(str(FONTS[style]))
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
    s1 = fit_size(db, "Virtua", "Bold", inner)
    s2 = fit_size(db, "Grotesk", "Bold", inner)
    cap1 = 0.75 * s1
    cap2 = 0.75 * s2
    gap = 110
    top = HEIGHT - MARGIN - 56
    bottom = MARGIN + 76
    block = cap1 + gap + cap2
    baseline1 = (top + bottom) / 2 + block / 2 - cap1
    baseline2 = baseline1 - gap - cap2

    db.fill(*INK)
    db.font(str(FONTS["Bold"]))
    db.fontSize(s1)
    db.text("Virtua", (WIDTH / 2, baseline1), align="center")
    db.fontSize(s2)
    db.text("Grotesk", (WIDTH / 2, baseline2), align="center")

    frame(db)
    save(db, "social-01-hero.png")


def draw_weights() -> None:
    db = page()
    y = 1490
    for index, style in enumerate(["Regular", "Medium", "SemiBold", "Bold"]):
        db.font(str(FONTS["Regular"]))
        db.fontSize(40)
        db.fill(*MUTED)
        db.text(f"wght {400 + 100 * index}", (MARGIN, y + 290))
        db.font(str(FONTS[style]))
        db.fontSize(320)
        db.fill(*INK)
        db.text("Hamburg", (MARGIN, y))
        y -= 390

    frame(db)
    save(db, "social-02-weights.png")


def draw_alphabet() -> None:
    db = page()
    lines = [
        ("Bold", "ABCDEFGHIJ"),
        ("Bold", "KLMNOPQRST"),
        ("Bold", "UVWXYZ&?!"),
        ("Medium", "abcdefghijklm"),
        ("Medium", "nopqrstuvwxyz"),
        ("SemiBold", "0123456789"),
    ]
    y = 1620
    for style, txt in lines:
        db.font(str(FONTS[style]))
        db.fontSize(230)
        db.fill(*INK)
        db.text(txt, (WIDTH / 2, y), align="center")
        y -= 276

    frame(db)
    save(db, "social-03-alphabet.png")


def draw_tabular() -> None:
    db = page()
    db.font(str(FONTS["Bold"]))
    db.fontSize(170)
    db.fill(*INK)
    db.text("Tabular Figures", (WIDTH / 2, 1660), align="center")

    style = "SemiBold"
    size = 270
    rows = ["650118", "204937", "881265"]
    tab = TAB_WIDTHS[style] / UPM * size
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

    db.font(str(FONTS[style]))
    db.fontSize(size)
    db.fill(*INK)
    db.openTypeFeatures(tnum=True)
    for row in rows:
        db.text(row, (x0, y))
        y -= 330
    db.openTypeFeatures(resetFeatures=True)

    db.font(str(FONTS["Regular"]))
    db.fontSize(56)
    db.fill(*MUTED)
    db.text("tnum · uniform widths on every weight", (WIDTH / 2, 330), align="center")

    frame(db)
    save(db, "social-04-tabular.png")


def draw_chamfer() -> None:
    db = page()
    db.font(str(FONTS["Regular"]))
    db.fontSize(56)
    db.fill(*MUTED)
    db.text("16-unit chamfered corners", (WIDTH / 2, HEIGHT - MARGIN - 160), align="center")

    db.font(str(FONTS["Bold"]))
    db.fontSize(1340)
    db.fill(*INK)
    db.text("Aa", (WIDTH / 2, 540), align="center")

    frame(db)
    save(db, "social-05-chamfer.png")


def draw_waterfall() -> None:
    """Geist-style split: point sizes on the left, the name on the right."""
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
        db.font(str(FONTS["SemiBold"]))
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
    for row in rows:
        db.font(str(FONTS["Regular"]))
        db.fontSize(220)
        db.text(row, (WIDTH / 2, y), align="center")
        y -= 290

    frame(db)
    save(db, "social-07-symbols.png")


def draw_lowercase() -> None:
    """Geist-style giant lowercase, weights receding in tint steps."""
    db = page()
    layers = [
        ("Regular", 0.32, 1940),
        ("SemiBold", 0.52, 1040),
        ("Bold", 0.86, 140),
    ]
    for style, tint, x in reversed(layers):
        db.font(str(FONTS[style]))
        db.fontSize(2300)
        db.fill(tint, tint, tint * 0.96)
        db.text("a", (x, -130))

    db.font(str(FONTS["Regular"]))
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
    require_fonts()
    draw_hero()
    draw_weights()
    draw_alphabet()
    draw_tabular()
    draw_chamfer()
    draw_waterfall()
    draw_symbols()
    draw_lowercase()


if __name__ == "__main__":
    main()
