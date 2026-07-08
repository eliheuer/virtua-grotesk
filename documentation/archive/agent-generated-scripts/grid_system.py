"""Shared modular grid system for all DrawBot-skia specimen output.

One source of truth for page geometry, in the Müller-Brockmann tradition
and the house drawbot idiom (W, H, M constants; unit = M/2; layout
coordinates as whole multiples of the unit; a toggleable overlay that
draws the REAL grid the layout is built on, in the same coordinate space).

Usage:
    from grid_system import Grid, grid_view

    g = Grid(2048, 2048)            # margin = min/16, unit = margin/2
    db.text("Aa", (g.x(0), g.y(4))) # place on unit lines
    if grid_view():                  # GRID_VIEW=1 in the environment
        g.draw(db)

See .agents/skills/specimen-grid-layout/SKILL.md for the full discipline.
"""

from __future__ import annotations

import os

from fontTools.ttLib import TTFont

OVERLAY_MINOR = (1, 0, 0, 0.28)
OVERLAY_MAJOR = (1, 0, 0, 0.55)
OVERLAY_FRAME = (1, 0, 0, 0.85)


def grid_view() -> bool:
    """Overlay toggle: GRID_VIEW=1 make social-images / make proof."""
    return os.environ.get("GRID_VIEW", "").lower() in ("1", "true", "yes", "on")


class Grid:
    """A modular unit grid inside margins.

    margin defaults to min(width, height) / 16, the house proportion.
    unit defaults to margin / 2 — every coordinate in the layout should
    be a whole multiple of the unit, measured from the margin lines.
    """

    def __init__(
        self,
        width: float,
        height: float,
        margin: float | None = None,
        unit: float | None = None,
    ):
        self.width = width
        self.height = height
        self.margin = margin if margin is not None else round(min(width, height) / 16)
        self.unit = unit if unit is not None else self.margin / 2
        self.inner_width = width - 2 * self.margin
        self.inner_height = height - 2 * self.margin

    # --- coordinates -----------------------------------------------------
    def x(self, units: float) -> float:
        """X position `units` to the right of the left margin line."""
        return self.margin + units * self.unit

    def y(self, units: float) -> float:
        """Y position `units` above the bottom margin line."""
        return self.margin + units * self.unit

    def y_top(self, units: float) -> float:
        """Y position `units` below the top margin line."""
        return self.height - self.margin - units * self.unit

    def snap(self, value: float) -> float:
        """Snap a length or position to the nearest unit line."""
        return round(value / self.unit) * self.unit

    def columns(self, count: int, gutter_units: float = 1.0) -> list[tuple[float, float]]:
        """(x, width) for `count` columns separated by gutters, spanning
        the inner width."""
        gutter = gutter_units * self.unit
        col_w = (self.inner_width - (count - 1) * gutter) / count
        return [(self.margin + i * (col_w + gutter), col_w) for i in range(count)]

    # --- optical alignment ----------------------------------------------
    def ink_left(self, font_path, text: str, size: float) -> float:
        """Left side-bearing of the first glyph, in points at `size`.

        A display-size headline whose BOX is on a grid line still reads
        as misaligned: its INK is inset by the side-bearing. Subtract
        this from the x position so the ink lands on the line:

            db.text(txt, (g.x(0) - g.ink_left(path, txt, size), baseline))
        """
        if not text:
            return 0.0
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        glyph_name = cmap.get(ord(text[0]))
        if glyph_name is None:
            font.close()
            return 0.0
        lsb = font["hmtx"][glyph_name][1]
        upm = font["head"].unitsPerEm
        font.close()
        return lsb * size / upm

    # --- overlay ---------------------------------------------------------
    def draw(self, db, major_every: int = 4) -> None:
        """Draw the live grid: unit lines, heavier major lines, the margin
        frame, and full-bleed center crosshairs. Same coordinate space as
        the layout, so what you see is what placement uses."""
        db.save()
        db.fill(None)
        db.strokeWidth(1)

        units_x = int(self.inner_width / self.unit + 0.5)
        units_y = int(self.inner_height / self.unit + 0.5)

        db.stroke(*OVERLAY_MINOR)
        for i in range(units_x + 1):
            x = self.x(i)
            db.line((x, self.margin), (x, self.height - self.margin))
        for i in range(units_y + 1):
            y = self.y(i)
            db.line((self.margin, y), (self.width - self.margin, y))

        db.stroke(*OVERLAY_MAJOR)
        for i in range(0, units_x + 1, major_every):
            x = self.x(i)
            db.line((x, self.margin), (x, self.height - self.margin))
        for i in range(0, units_y + 1, major_every):
            y = self.y(i)
            db.line((self.margin, y), (self.width - self.margin, y))

        db.strokeWidth(2)
        db.stroke(*OVERLAY_FRAME)
        db.rect(self.margin, self.margin, self.inner_width, self.inner_height)
        db.line((self.width / 2, 0), (self.width / 2, self.height))
        db.line((0, self.height / 2), (self.width, self.height / 2))

        db.restore()
