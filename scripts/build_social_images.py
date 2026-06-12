#!/usr/bin/env python3
"""Build DrawBot-skia PNG specimen images for social media posts.

Brutalist / neomodernist style: repetition as the layout device, type fit
to the frame width, tight leading, left-aligned ragged-right settings,
near-black ground with gray-white ink, captions in the four corners set in
the font itself (Font.Garden poster idiom), no decorative rules.

Every image is rendered in three formats at 2x resolution:
  square    2048x2048  (1:1   - Instagram feed, X/Twitter)
  portrait  1638x2048  (4:5   - Instagram feed, most screen area)
  landscape 2048x1152  (16:9  - X/Twitter in-stream)

Weights are discovered from fonts/ttf/*.ttf at runtime (style name from the
name table, ordering from OS/2 usWeightClass), so adding or removing
instances changes the output set without script edits.
"""

from __future__ import annotations

from pathlib import Path

from fontTools.misc.fixedTools import floatToFixedToStr
from fontTools.ttLib import TTFont
from PIL import Image

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run `make setup` to install it in .venv."
    ) from error

from grid_system import Grid, grid_view


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "fonts/ttf"
OUTPUT_DIR = ROOT / "documentation/assets/social"

FORMATS = {
    "square": (2048, 2048),
    "portrait": (1638, 2048),
    "landscape": (2048, 1152),
}

PAPER = (0.055, 0.055, 0.055)
INK = (0.83, 0.83, 0.80)
WHITE = (0.96, 0.96, 0.94)
MUTED = (0.56, 0.56, 0.53)
RULE = (0.30, 0.30, 0.28)
RED = (1.0, 0.29, 0.24)  # the source markColor, used as the single accent

LOGO = ""  # 3x3 grid mark from the font's PUA icon block
CAP_RATIO = 0.75  # cap height / UPM in this family

# Per-format geometry, set by set_format()
WIDTH = HEIGHT = MARGIN = CAPTION_SIZE = 0
BAND_TOP = BAND_BOTTOM = 0.0
FORMAT_NAME = "square"
GRID: Grid


def set_format(name: str) -> None:
    global WIDTH, HEIGHT, MARGIN, CAPTION_SIZE, BAND_TOP, BAND_BOTTOM
    global FORMAT_NAME, GRID
    FORMAT_NAME = name
    WIDTH, HEIGHT = FORMATS[name]
    GRID = Grid(WIDTH, HEIGHT)
    MARGIN = GRID.margin
    CAPTION_SIZE = max(36, round(min(WIDTH, HEIGHT) * 0.0225))
    # The big-type band runs between unit lines two units inside the
    # margins, clear of the corner captions.
    BAND_TOP = GRID.y_top(2)
    BAND_BOTTOM = GRID.y(2)


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


def page() -> Drawing:
    db = Drawing()
    db.newPage(WIDTH, HEIGHT)
    db.fill(*PAPER)
    db.rect(0, 0, WIDTH, HEIGHT)
    return db


def captions(db: Drawing, bottom_left: str | None = None, footer: bool = True) -> None:
    """Font.Garden poster idiom: small captions in the four corners."""
    if bottom_left is None:
        bottom_left = f"{LIGHTEST.family} {LIGHTEST.name} {LIGHTEST.version}"
    db.save()
    db.stroke(None)
    db.font(str(LIGHTEST.path))
    db.fontSize(CAPTION_SIZE)
    db.fill(*MUTED)
    top_baseline = HEIGHT - MARGIN - CAPTION_SIZE * CAP_RATIO
    db.text(f"{LOGO} Font.Garden/virtua", (MARGIN, top_baseline))
    db.text(
        "Open Font License OFL v1.1",
        (WIDTH - MARGIN, top_baseline),
        align="right",
    )
    if footer:
        db.text(bottom_left, (MARGIN, MARGIN))
        db.text(
            "github.com/eliheuer/virtua-grotesk",
            (WIDTH - MARGIN, MARGIN),
            align="right",
        )
    db.restore()


def fit_size(db: Drawing, txt: str, style: Style, target_w: float) -> float:
    db.font(str(style.path))
    db.fontSize(100)
    return 100 * target_w / db.textSize(txt)[0]


def fit_stack_size(db: Drawing, rows: list[tuple[str, Style]]) -> float:
    """Largest size where the widest row fits the inner width and the
    block fits the caption band at tight leading."""
    inner = WIDTH - MARGIN * 2
    width_fit = min(fit_size(db, txt, style, inner) for txt, style in rows)
    band = BAND_TOP - BAND_BOTTOM
    cap_max = band / (1.12 * (len(rows) - 1) + 1)
    return min(width_fit, cap_max / CAP_RATIO)


def stack(
    db: Drawing,
    rows: list[tuple[str, Style]],
    size: float,
    color: tuple[float, float, float] = INK,
) -> float:
    """Left-aligned repetition block, vertically centered between the
    captions, leading clamped between tight and loose. Returns the top
    baseline y."""
    cap = CAP_RATIO * size
    count = len(rows)
    band = BAND_TOP - BAND_BOTTOM
    leading = (band - cap) / max(count - 1, 1)
    leading = max(min(leading, cap * 1.55), cap * 1.12)
    block = (count - 1) * leading + cap
    baseline = BAND_BOTTOM + (band - block) / 2 + block - cap
    top_baseline = baseline
    db.fill(*color)
    for txt, style in rows:
        db.font(str(style.path))
        db.fontSize(size)
        x = MARGIN - GRID.ink_left(style.path, txt, size)
        db.text(txt, (x, baseline))
        baseline -= leading
    return top_baseline


def save(db: Drawing, name: str) -> None:
    if grid_view():
        GRID.draw(db)
    path = OUTPUT_DIR / FORMAT_NAME / name
    path.parent.mkdir(parents=True, exist_ok=True)
    db.saveImage(str(path))
    # Quantize to a 256-color palette: these near-monochrome images lose
    # nothing visible and shrink ~60-70%, keeping the git repo lean.
    image = Image.open(path).convert("RGB")
    image.quantize(colors=256, dither=Image.Dither.NONE).save(path, optimize=True)
    print(path.relative_to(ROOT))


def repetition_rows(db: Drawing, txt: str, style: Style) -> list[tuple[str, Style]]:
    """As many repeated rows as fit the caption band at tight leading."""
    size = fit_size(db, txt, style, WIDTH - MARGIN * 2)
    cap = CAP_RATIO * size
    band = BAND_TOP - BAND_BOTTOM
    count = max(2, int((band - cap) / (1.15 * cap)) + 1)
    return [(txt, style)] * count


def draw_hero() -> None:
    """Repetition poster: the family name over and over, fit to the frame."""
    db = page()
    rows = repetition_rows(db, "Virtua Grotesk", style_near(500))
    stack(db, rows, fit_stack_size(db, rows), color=WHITE)
    captions(db)
    save(db, "social-01-hero.png")


def draw_weights() -> None:
    """One row per discovered weight, lightest to heaviest."""
    db = page()
    rows = [("Hamburg", s) for s in STYLES]
    stack(db, rows, fit_stack_size(db, rows))
    captions(
        db,
        bottom_left=(
            f"{LIGHTEST.family} wght {LIGHTEST.weight_class}"
            f"–{HEAVIEST.weight_class} {LIGHTEST.version}"
        ),
    )
    save(db, "social-02-weights.png")


def draw_alphabet(style: Style) -> None:
    db = page()
    lines = [
        "ABCDEFGHIJ",
        "KLMNOPQR",
        "STUVWXYZ",
        "0123456789",
        "abcdefghij",
        "klmnopqr",
        "stuvwxyz",
    ]
    rows = [(txt, style) for txt in lines]
    stack(db, rows, fit_stack_size(db, rows))
    captions(db, bottom_left=f"{style.family} {style.name} {style.version}")
    save(db, f"social-03-alphabet-{style.slug}.png")


def draw_tabular() -> None:
    style = style_near(600)
    if style.tab_width is None:
        print("skipping tabular image: no zero.tf glyph in", style.path.name)
        return

    db = page()
    rows = [("0123456789", style), ("1463082957", style), ("2048102464", style)]
    # Fit by tabular advance, not proportional widths: every row is
    # digits * tab_width wide once tnum is applied.
    digits = len(rows[0][0])
    inner = WIDTH - MARGIN * 2
    width_fit = inner * style.upm / (digits * style.tab_width)
    band = BAND_TOP - BAND_BOTTOM
    cap_max = band / (1.12 * (len(rows) - 1) + 1)
    size = min(width_fit, cap_max / CAP_RATIO)
    tab = style.tab_width / style.upm * size
    cap = CAP_RATIO * size

    db.openTypeFeatures(tnum=True)
    top_baseline = stack(db, rows, size)
    db.openTypeFeatures(resetFeatures=True)

    leading = max(
        min((BAND_TOP - BAND_BOTTOM - cap) / (len(rows) - 1), cap * 1.55),
        cap * 1.12,
    )
    bottom = top_baseline - (len(rows) - 1) * leading - size * 0.06
    db.save()
    db.stroke(*RULE)
    db.strokeWidth(2)
    for i in range(len(rows[0][0]) + 1):
        x = MARGIN + i * tab
        db.line((x, bottom), (x, top_baseline + cap))
    db.restore()

    captions(db, bottom_left=f"{style.family} Tabular Figures · tnum")
    save(db, "social-04-tabular.png")


def draw_chamfer() -> None:
    db = page()
    rows = [("Aa", HEAVIEST)]
    size = fit_stack_size(db, rows)
    cap = CAP_RATIO * size
    baseline = (BAND_TOP + BAND_BOTTOM) / 2 - cap / 2
    db.font(str(HEAVIEST.path))
    db.fontSize(size)
    db.fill(*INK)
    db.text("Aa", (MARGIN - GRID.ink_left(HEAVIEST.path, "Aa", size), baseline))
    captions(db, bottom_left=f"{HEAVIEST.family} · 16-unit chamfered corners")
    save(db, "social-05-chamfer.png")


def draw_waterfall() -> None:
    """Split panel: point sizes on the left, the name on the right."""
    style = style_near(600)
    db = page()
    split = GRID.snap(WIDTH * 0.36)
    db.save()
    db.stroke(*RULE)
    db.strokeWidth(2)
    db.line((split, BAND_BOTTOM - 36), (split, BAND_TOP + 36))
    db.restore()

    band = BAND_TOP - BAND_BOTTOM
    factor = band / 1480
    sizes = [round(s * factor) for s in [236, 196, 162, 132, 106, 82, 62, 46]]
    y = BAND_TOP - sizes[0] * 0.82
    for index, size in enumerate(sizes):
        tint = max(0.30, 0.83 - index * 0.07)
        db.font(str(style.path))
        db.fontSize(size)
        db.fill(tint, tint, tint * 0.96)
        db.text(str(size), (split - 56, y), align="right")
        db.fill(*INK)
        name = "Virtua©" if index < 5 else "Grotesk©"
        db.text(name, (split + 56, y))
        y -= size * 1.16 + 14 * factor

    captions(db)
    save(db, "social-06-waterfall.png")


def draw_symbols() -> None:
    """Coded strings in the source markColor red."""
    db = page()
    lines = [
        "*{Virtua}*",
        "<GROTESK>",
        "(+Chamfer)",
        "@16/1024_u",
        "#OFL—2026",
    ]
    rows = [(txt, LIGHTEST) for txt in lines]
    stack(db, rows, fit_stack_size(db, rows), color=RED)
    captions(db)
    save(db, "social-07-symbols.png")


def draw_lowercase() -> None:
    """Giant cropped lowercase, weights receding in tint steps."""
    db = page()
    size = HEIGHT * 1.12
    layers = [
        (LIGHTEST, 0.30, 0.947),
        (style_near(600), 0.50, 0.508),
        (HEAVIEST, 0.83, 0.068),
    ]
    for style, tint, x_frac in reversed(layers):
        db.font(str(style.path))
        db.fontSize(size)
        db.fill(tint, tint, tint * 0.96)
        db.text("a", (WIDTH * x_frac, -HEIGHT * 0.064))

    db.font(str(LIGHTEST.path))
    db.fontSize(CAPTION_SIZE)
    db.fill(*MUTED)
    box_w = WIDTH * 0.625
    db.textBox(
        "Virtua Grotesk is a geometric grotesk with 16-unit chamfered "
        "corners — monolinear strokes and a retro-futurist technical "
        "character, drawn with modern precision on a 1024-unit grid.",
        (MARGIN, HEIGHT - MARGIN - CAPTION_SIZE * 2 - 300, box_w, 300),
    )

    captions(db, footer=False)
    save(db, "social-08-lowercase.png")


def main() -> None:
    for format_name in FORMATS:
        set_format(format_name)
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
