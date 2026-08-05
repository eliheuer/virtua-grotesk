#!/usr/bin/env python3
"""Regenerate the LATIN half of the mark feature in features.fea from the
UFO anchors. The Arabic half is left byte-for-byte alone.

Before this, the Latin mark attachment covered three bases
(`@LATIN_TOP_BASES = [J jdotless dottedCircle]`) against a single hardcoded
anchor, and exactly one mark class (acutecomb — which was an empty glyph).
So every combining accent in the font either rendered blank or sat in the
wrong place.

Both masters get the same file, matching the repo's current convention;
the anchor values come from the Regular. That means Latin mark attachment
does not vary across the weight axis — a real limitation, but the Arabic
feature already works this way, and fixing it properly means letting
ufo2ft generate mark/mkmk from anchors, which would first need the Arabic
marks to carry `_top`/`_bottom` anchors. Noted, not attempted here.

Usage:
    ./.venv/bin/python scripts/latin_mark_feature.py [--dry-run]
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from latin_marks import (MASTERS, contents, anchors_of,  # noqa: E402
                         TOP_ACCENTS, BOTTOM_ACCENTS)

REG = MASTERS["Regular"]


def main():
    dry = "--dry-run" in sys.argv
    cmap = contents(REG)

    # --- bases: every Latin letter (and dottedCircle) carrying anchors ---
    top_bases, bottom_bases = {}, {}
    for g in sorted(cmap):
        if not (g == "dottedCircle" or (len(g) == 1 and g.isalpha()
                                        and g.isascii())
                or g in ("idotless", "jdotless")):
            continue
        a = anchors_of(REG, cmap, g)
        if "top" in a:
            top_bases[g] = a["top"]
        if "bottom" in a:
            bottom_bases[g] = a["bottom"]

    # --- marks ------------------------------------------------------------
    top_marks, bottom_marks = {}, {}
    for acc in TOP_ACCENTS:
        c = f"{acc}comb"
        if c in cmap and "_top" in anchors_of(REG, cmap, c):
            top_marks[c] = anchors_of(REG, cmap, c)["_top"]
    for acc in BOTTOM_ACCENTS:
        c = f"{acc}comb"
        if c in cmap and "_bottom" in anchors_of(REG, cmap, c):
            bottom_marks[c] = anchors_of(REG, cmap, c)["_bottom"]

    def n(v):
        return str(int(round(v)))

    # --- build the replacement blocks -------------------------------------
    classes = [f"@LATIN_TOP_BASES = [{' '.join(sorted(top_bases))}];",
               f"@LATIN_BOTTOM_BASES = [{' '.join(sorted(bottom_bases))}];",
               ""]
    for m, (x, y) in sorted(top_marks.items()):
        classes.append(f"markClass {m} <anchor {n(x)} {n(y)}> @MC_latin_top;")
    for m, (x, y) in sorted(bottom_marks.items()):
        classes.append(
            f"markClass {m} <anchor {n(x)} {n(y)}> @MC_latin_bottom;")
    classes_block = "\n".join(classes)

    lookup = ["lookup mark_latin_0 {"]
    for g, (x, y) in sorted(top_bases.items()):
        lookup.append(f"\tpos base {g} <anchor {n(x)} {n(y)}> "
                      f"mark @MC_latin_top;")
    lookup.append("} mark_latin_0;")
    lookup.append("")
    lookup.append("lookup mark_latin_1 {")
    for g, (x, y) in sorted(bottom_bases.items()):
        lookup.append(f"\tpos base {g} <anchor {n(x)} {n(y)}> "
                      f"mark @MC_latin_bottom;")
    lookup.append("} mark_latin_1;")
    lookup_block = "\n".join(lookup)

    for mname, ufo in MASTERS.items():
        p = ufo / "features.fea"
        text = p.read_text()

        # replace the class + markClass region (Latin only)
        text2, k1 = re.subn(
            r"@LATIN_TOP_BASES = \[[^\]]*\];\n\nmarkClass acutecomb [^\n]*\n",
            classes_block + "\n", text, count=1)
        # replace the Latin lookup, keeping the Arabic one untouched
        text2, k2 = re.subn(
            r"lookup mark_latin_0 \{.*?\} mark_latin_0;\n",
            lookup_block + "\n", text2, count=1, flags=re.S)
        # register the new lookup in the script blocks
        text2 = text2.replace("lookup mark_latin_0;\n",
                              "lookup mark_latin_0;\nlookup mark_latin_1;\n")
        if not (k1 and k2):
            print(f"  {mname}: PATTERN NOT FOUND (k1={k1} k2={k2}) — "
                  f"features.fea left alone")
            continue
        if not dry:
            p.write_text(text2)

    print(f"Latin mark feature: {len(top_bases)} top bases, "
          f"{len(bottom_bases)} bottom bases, "
          f"{len(top_marks)} top marks, {len(bottom_marks)} bottom marks")
    if dry:
        print("\n--- classes ---\n" + classes_block)
        print("\n--- lookups ---\n" + lookup_block[:600] + " ...")


if __name__ == "__main__":
    sys.exit(main())
