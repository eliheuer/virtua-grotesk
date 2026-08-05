#!/usr/bin/env python3
"""Add the accented Latin composites Google Fonts wants but the font lacks.

These are the codepoints behind the `googlefonts/glyphsets/shape_languages`
exclude — auxiliary orthography for Czech, Welsh, Spanish, Hungarian,
Portuguese, Slovak, Turkish and Catalan.

Every one is a plain composite, placed from the anchors set by
scripts/latin_marks.py, and written PER MASTER (the Latin is properly
bolded, so the offsets differ between them).

Usage:
    ./.venv/bin/python scripts/latin_add_composites.py [--dry-run]
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from latin_marks import (MASTERS, contents, bbox, anchors_of,  # noqa: E402
                         path_of, fmt, BLUE)
from arabic_build import register_glyph  # noqa: E402

# name -> (unicode, base, mark)  — mark placed via anchors
COMPOSITES = [
    ("Ebreve",  "0114", "E", "brevecomb"),
    ("ebreve",  "0115", "e", "brevecomb"),
    ("Ibreve",  "012C", "I", "brevecomb"),
    ("ibreve",  "012D", "idotless", "brevecomb"),
    ("Obreve",  "014E", "O", "brevecomb"),
    ("obreve",  "014F", "o", "brevecomb"),
    ("Omacron", "014C", "O", "macroncomb"),
    ("omacron", "014D", "o", "macroncomb"),
    ("Ubreve",  "016C", "U", "brevecomb"),
    ("ubreve",  "016D", "u", "brevecomb"),

    # --- second pass: the rest of the auxiliary set that is pure
    # base+mark (Finnish / Sami / Esperanto / Latvian / pinyin).
    ("Itilde",       "0128", "I", "tildecomb"),
    ("itilde",       "0129", "idotless", "tildecomb"),
    ("Utilde",       "0168", "U", "tildecomb"),
    ("utilde",       "0169", "u", "tildecomb"),
    ("Etilde",       "1EBC", "E", "tildecomb"),
    ("etilde",       "1EBD", "e", "tildecomb"),
    ("Acaron",       "01CD", "A", "caroncomb"),
    ("acaron",       "01CE", "a", "caroncomb"),
    ("Ucaron",       "01D3", "U", "caroncomb"),
    ("ucaron",       "01D4", "u", "caroncomb"),
    ("Gcaron",       "01E6", "G", "caroncomb"),
    ("gcaron",       "01E7", "g", "caroncomb"),
    ("Kcaron",       "01E8", "K", "caroncomb"),
    ("kcaron",       "01E9", "k", "caroncomb"),
    ("Hcaron",       "021E", "H", "caroncomb"),
    ("hcaron",       "021F", "h", "caroncomb"),
    ("Scircumflex",  "015C", "S", "circumflexcomb"),
    ("scircumflex",  "015D", "s", "circumflexcomb"),
    ("Rcedilla",     "0156", "R", "cedillacomb"),
    ("rcedilla",     "0157", "r", "cedillacomb"),
    ("Tcedilla",     "0162", "T", "cedillacomb"),
    ("tcedilla",     "0163", "t", "cedillacomb"),
    ("Oslashacute",  "01FE", "Oslash", "acutecomb"),
    ("oslashacute",  "01FF", "oslash", "acutecomb"),
]

# L with middle dot: the dot sits to the RIGHT of the letter, not above,
# so it is placed from the letter's advance rather than an anchor.
MIDDLE_DOT = [("Ldot", "013F", "L"), ("ldot", "0140", "l")]


def advance_of(ufo, cmap, name):
    import xml.etree.ElementTree as ET
    a = ET.parse(path_of(ufo, cmap, name)).getroot().find("advance")
    return float(a.get("width")) if a is not None else 0.0


def write_composite(ufo, cmap, name, uni, comps, advance):
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            f'<glyph name="{name}" format="2">',
            f'\t<unicode hex="{uni}"/>',
            f'\t<advance width="{fmt(advance)}"/>',
            "\t<outline>"]
    for base, dx, dy in comps:
        attrs = f'base="{base}"'
        if round(dx):
            attrs += f' xOffset="{fmt(dx)}"'
        if round(dy):
            attrs += f' yOffset="{fmt(dy)}"'
        body.append(f"\t\t<component {attrs}/>")
    body += ["\t</outline>", "\t<lib>", "\t\t<dict>",
             "\t\t\t<key>public.markColor</key>",
             f"\t\t\t<string>{BLUE}</string>",
             "\t\t</dict>", "\t</lib>", "</glyph>", ""]
    path_of(ufo, cmap, name).write_text("\n".join(body))


def main():
    dry = "--dry-run" in sys.argv
    made, skipped = [], []

    for name, uni, base, mark in COMPOSITES:
        for mname, ufo in MASTERS.items():
            cmap = contents(ufo)
            if base not in cmap or mark not in cmap:
                skipped.append(f"{name}: missing {base} or {mark}")
                continue
            ba = anchors_of(ufo, cmap, base)
            ma = anchors_of(ufo, cmap, mark)
            # pick the side from the MARK: cedilla/ogonek attach below
            side = "_bottom" if "_bottom" in ma else "_top"
            bkey = "bottom" if side == "_bottom" else "top"
            if side not in ma:
                skipped.append(f"{name}: {mark} has no attachment anchor")
                continue
            if bkey in ba:
                bx, by = ba[bkey]
            else:
                # base carries no anchor of its own (Oslash, ligatures):
                # fall back to its ink centre on the relevant metric line
                bb = bbox(ufo, cmap, base)
                if not bb:
                    skipped.append(f"{name}: {base} has no ink")
                    continue
                bx = (bb[0] + bb[2]) / 2
                by = 0.0 if bkey == "bottom" else (
                    768.0 if base[0].isupper() else 576.0)
            dx = bx - ma[side][0]
            dy = by - ma[side][1]
            if dry:
                continue
            register_glyph(name)
            cmap = contents(ufo)
            write_composite(ufo, cmap, name, uni,
                            [(base, 0, 0), (mark, dx, dy)],
                            advance_of(ufo, cmap, base))
        made.append(name)

    # --- L/l with middle dot ------------------------------------------
    for name, uni, base in MIDDLE_DOT:
        for mname, ufo in MASTERS.items():
            cmap = contents(ufo)
            if base not in cmap or "periodcentered" not in cmap:
                skipped.append(f"{name}: missing {base}/periodcentered")
                continue
            adv_b = advance_of(ufo, cmap, base)
            bb_b = bbox(ufo, cmap, base)
            bb_d = bbox(ufo, cmap, "periodcentered")
            if not bb_b or not bb_d:
                skipped.append(f"{name}: no ink")
                continue
            # dot sits in the sidebearing to the right of the stem, its own
            # ink centred on the gap between the letter and the advance
            gap_centre = (bb_b[2] + adv_b + 48) / 2
            dx = gap_centre - (bb_d[0] + bb_d[2]) / 2
            if dry:
                continue
            register_glyph(name)
            cmap = contents(ufo)
            write_composite(ufo, cmap, name, uni,
                            [(base, 0, 0), ("periodcentered", dx, 0)],
                            adv_b + 96)
        made.append(name)

    verb = "would add" if dry else "added"
    print(f"{verb} {len(made)} composites: {' '.join(made)}")
    if skipped:
        print(f"SKIPPED {len(set(skipped))}:")
        for s in sorted(set(skipped))[:10]:
            print("  " + s)


if __name__ == "__main__":
    sys.exit(main())
