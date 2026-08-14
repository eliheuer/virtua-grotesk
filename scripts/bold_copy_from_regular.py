#!/usr/bin/env python3
"""Unbreak the variable build by copying Regular drawings into Bold.

While a glyph is being redrawn in Regular, its Bold master goes structurally
incompatible and fontmake refuses to interpolate. This copies the Regular
outline, advance and anchors over the Bold ones for exactly those glyphs, so
the build runs again. The glyph then carries no bold weight until it is
redrawn or re-emboldened — Bold's mark colour is preserved so the state stays
visible rather than being silently marked done.

Usage:
    ./.venv/bin/python scripts/bold_copy_from_regular.py [--dry-run]
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

REG = pathlib.Path("sources/VirtuaGrotesk-Regular.ufo")
BOLD = pathlib.Path("sources/VirtuaGrotesk-Bold.ufo")

BLOCK = {
    "advance": re.compile(r"\t<advance [^\n]*/>\n"),
    "outline": re.compile(r"\t<outline>.*?\t</outline>\n", re.S),
    "anchors": re.compile(r"(?:\t<anchor [^\n]*/>\n)+"),
    "lib": re.compile(r"\t<lib>.*?\t</lib>\n", re.S),
}


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def structure(path):
    """Interpolation-relevant shape: per-contour point types, component bases."""
    root = ET.parse(path).getroot()
    contours = []
    for c in root.iter("contour"):
        contours.append(tuple(p.get("type") or "offcurve" for p in c.iter("point")))
    comps = [c.get("base") for c in root.iter("component")]
    return contours, comps


def graft(src_text, dst_text):
    """Regular's advance/outline/anchors into Bold, keeping Bold's lib."""
    out = src_text
    lib = BLOCK["lib"].search(dst_text)
    src_lib = BLOCK["lib"].search(out)
    if lib and src_lib:
        out = out[:src_lib.start()] + lib.group(0) + out[src_lib.end():]
    elif lib and not src_lib:
        out = out.replace("</glyph>", lib.group(0) + "</glyph>", 1)
    elif src_lib and not lib:
        out = out[:src_lib.start()] + out[src_lib.end():]
    # a copied drawing has no components, so any component-keyed lib is stale
    if "<component " not in out:
        out = re.sub(
            r"\t\t\t<key>public\.objectLibs</key>\n\t\t\t<dict>.*?\n\t\t\t</dict>\n",
            "", out, flags=re.S)
    return out


def main():
    dry = "--dry-run" in sys.argv
    rc, bc = contents(REG), contents(BOLD)
    broken, copied, missing = [], [], []

    for name in sorted(set(rc) & set(bc)):
        rp, bp = REG / "glyphs" / rc[name], BOLD / "glyphs" / bc[name]
        try:
            rs, bs = structure(rp), structure(bp)
        except ET.ParseError as e:
            missing.append(f"{name}: unparseable ({e})")
            continue
        if rs == bs:
            continue
        broken.append(name)
        if dry:
            continue
        bp.write_text(graft(rp.read_text(), bp.read_text()))
        copied.append(name)

    verb = "would copy" if dry else "copied"
    print(f"{verb} Regular -> Bold for {len(broken)} structurally "
          f"incompatible glyphs:")
    for n in broken:
        print("   " + n)
    if missing:
        print("\nunreadable:")
        for m in missing:
            print("   " + m)
    print("\nThese glyphs now carry no bold weight. Re-run "
          "`make arabic-sync` once their Regular drawings settle.")


if __name__ == "__main__":
    sys.exit(main())
