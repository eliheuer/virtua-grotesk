#!/usr/bin/env python3
"""Patch generated TTF metadata that is not preserved by instance generation."""

from pathlib import Path
import sys

from fontTools import subset
from fontTools.ttLib import TTFont, newTable


ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = (ROOT / "OFL.txt").read_text().splitlines()[0]
SCRIPT_TAGS = "Arab, Latn"
SOURCE_ONLY_ARABIC_HELPERS = {
    "dotabovear",
    "dotbelowar",
    "dotcenterar",
    "doublestrokear",
    "gafsarkashabovear",
    "gafsarkashcenterar",
    "miniKehehar",
    "threedotsdownabovear",
    "threedotsdownbelowar",
    "threedotsdowncenterar",
    "threedotsupabovear",
    "threedotsupbelowar",
    "twodotshorizontalabovear",
    "twodotshorizontalbelowar",
    "twodotsverticalabovear",
    "twodotsverticalbelowar",
    "waslaar",
}


def set_name(font, name_id, value):
    # Windows, Unicode BMP, en-US. This is the platform GF QA tools check.
    font["name"].setName(value, name_id, 3, 1, 0x409)
    # Macintosh Roman, English. Keep legacy apps from showing blanks.
    font["name"].setName(value, name_id, 1, 0, 0)


def add_identity_avar(font):
    if "fvar" not in font or "avar" in font:
        return
    avar = newTable("avar")
    avar.majorVersion = 1
    avar.minorVersion = 0
    avar.segments = {
        axis.axisTag: {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}
        for axis in font["fvar"].axes
    }
    font["avar"] = avar


def remove_unreachable_arabic_helpers(font):
    glyph_order = font.getGlyphOrder()
    helpers = SOURCE_ONLY_ARABIC_HELPERS.intersection(glyph_order)
    if not helpers or "glyf" not in font:
        return

    glyf = font["glyf"]
    for glyph_name in glyph_order:
        if glyph_name in helpers:
            continue
        glyph = glyf[glyph_name]
        if glyph.isComposite() and any(component.glyphName in helpers for component in glyph.components):
            glyph.expand(glyf)

    options = subset.Options()
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.name_languages = ["*"]
    options.layout_features = ["*"]
    options.notdef_glyph = True
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.passthrough_tables = True
    options.glyph_names = True
    options.legacy_cmap = True

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(glyphs=[glyph_name for glyph_name in glyph_order if glyph_name not in helpers])
    subsetter.subset(font)


def patch_font(path):
    font = TTFont(path)
    font["OS/2"].fsType = 0
    set_name(font, 0, COPYRIGHT)
    add_identity_avar(font)
    meta = font["meta"] if "meta" in font else newTable("meta")
    meta.data = dict(getattr(meta, "data", {}))
    meta.data["dlng"] = SCRIPT_TAGS
    meta.data["slng"] = SCRIPT_TAGS
    font["meta"] = meta
    remove_unreachable_arabic_helpers(font)
    font.save(path)


def main(paths):
    if not paths:
        raise SystemExit("usage: fix_gf_metadata.py FONT.ttf [FONT.ttf ...]")
    for raw_path in paths:
        path = Path(raw_path)
        if path.suffix.lower() == ".ttf":
            patch_font(path)


if __name__ == "__main__":
    main(sys.argv[1:])
