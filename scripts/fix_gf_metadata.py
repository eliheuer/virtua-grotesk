#!/usr/bin/env python3
"""Patch generated TTF metadata that is not preserved by instance generation."""

from pathlib import Path
import sys

from fontTools.ttLib import TTFont, newTable


ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = (ROOT / "OFL.txt").read_text().splitlines()[0]
SCRIPT_TAGS = "Arab, Latn"


def set_name(font, name_id, value):
    # Windows, Unicode BMP, en-US. This is the platform GF QA tools check.
    font["name"].setName(value, name_id, 3, 1, 0x409)
    # Macintosh Roman, English. Keep legacy apps from showing blanks.
    font["name"].setName(value, name_id, 1, 0, 0)


def patch_font(path):
    font = TTFont(path)
    font["OS/2"].fsType = 0
    set_name(font, 0, COPYRIGHT)
    meta = font["meta"] if "meta" in font else newTable("meta")
    meta.data = dict(getattr(meta, "data", {}))
    meta.data["dlng"] = SCRIPT_TAGS
    meta.data["slng"] = SCRIPT_TAGS
    font["meta"] = meta
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
