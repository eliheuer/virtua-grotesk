#!/usr/bin/env python3
"""Audit the Latin diacritic system: which accented glyphs exist, how they
are built, whether the anchors that drive them are present and consistent,
and where the marks actually land.

Read-only. Prints the work-list; changes nothing.

Usage:
    ./.venv/bin/python scripts/latin_diacritics_audit.py
"""

import pathlib
import plistlib
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
R = REPO / "sources" / "VirtuaGrotesk-Regular.ufo"
B = REPO / "sources" / "VirtuaGrotesk-Bold.ufo"

# The combining marks a Latin font needs, by the anchor they attach to.
TOP_MARKS = ["grave", "acute", "circumflex", "tilde", "macron", "breve",
             "dotaccent", "dieresis", "ring", "hungarumlaut", "caron"]
BOTTOM_MARKS = ["cedilla", "ogonek", "commaaccent", "dotbelow", "macronbelow"]


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def root_of(ufo, cmap, name):
    return ET.parse(ufo / "glyphs" / cmap[name]).getroot()


def info(ufo, cmap, name):
    root = root_of(ufo, cmap, name)
    comps = [(c.get("base"), float(c.get("xOffset") or 0),
              float(c.get("yOffset") or 0)) for c in root.iter("component")]
    anchors = {a.get("name"): (float(a.get("x")), float(a.get("y")))
               for a in root.iter("anchor")}
    npts = len(list(root.iter("point")))
    uni = [u.get("hex") for u in root.iter("unicode")]
    adv = root.find("advance")
    return {"components": comps, "anchors": anchors, "points": npts,
            "unicodes": uni,
            "advance": float(adv.get("width")) if adv is not None else 0.0}


def main():
    cr = contents(R)
    cb = contents(B)
    data = {n: info(R, cr, n) for n in cr}

    # --- 1. which accented glyphs exist, and are they composites? --------
    accented, drawn_accented, empty = [], [], []
    for n, d in data.items():
        if not d["unicodes"]:
            continue
        try:
            ch = chr(int(d["unicodes"][0], 16))
        except ValueError:
            continue
        if not ("LATIN" in unicodedata.name(ch, "")
                and len(unicodedata.decomposition(ch).split()) > 1):
            continue
        accented.append(n)
        if not d["components"] and d["points"]:
            drawn_accented.append(n)
        if not d["components"] and not d["points"]:
            empty.append(n)

    print(f"accented Latin glyphs: {len(accented)}")
    print(f"  built as composites : {len(accented) - len(drawn_accented) - len(empty)}")
    print(f"  DRAWN (not composed): {len(drawn_accented)}")
    if drawn_accented:
        print("    " + " ".join(sorted(drawn_accented)))
    print(f"  EMPTY               : {len(empty)}")
    if empty:
        print("    " + " ".join(sorted(empty)))

    # --- 2. mark glyphs and their anchors --------------------------------
    print("\n--- combining marks ---")
    print(f"{'mark':22s} {'exists':>7s} {'_marks anchor':>14s} {'ink bbox':>26s}")
    for m in TOP_MARKS + BOTTOM_MARKS:
        for cand in (f"{m}comb", m):
            if cand in data:
                d = data[cand]
                # resolve components: the comb glyphs are components of the
                # spacing accents and have no points of their own
                sys.path.insert(0, str(pathlib.Path(__file__).parent))
                from latin_marks import bbox as _bbox
                bb_t = _bbox(R, cr, cand)
                bb = (f"{bb_t[0]:.0f},{bb_t[1]:.0f}..{bb_t[2]:.0f},{bb_t[3]:.0f}"
                      if bb_t else "EMPTY")
                anc = ",".join(k for k in d["anchors"] if k.startswith("_"))
                print(f"{cand:22s} {'yes':>7s} {anc or 'MISSING':>14s} {bb:>26s}")
                break
        else:
            print(f"{m:22s} {'NO':>7s}")

    # --- 3. anchors on the bases -----------------------------------------
    print("\n--- base letters missing anchors ---")
    bases = [n for n in data if len(n) == 1 and n.isalpha()]
    no_top = sorted(n for n in bases if "top" not in data[n]["anchors"])
    no_bot = sorted(n for n in bases if "bottom" not in data[n]["anchors"])
    print(f"no 'top' anchor    ({len(no_top)}): {' '.join(no_top) or 'none'}")
    print(f"no 'bottom' anchor ({len(no_bot)}): {' '.join(no_bot) or 'none'}")

    # --- 4. do the two masters agree on anchors? -------------------------
    print("\n--- anchor mismatches between masters ---")
    bad = []
    for n in sorted(set(cr) & set(cb)):
        a = info(R, cr, n)["anchors"]
        b = info(B, cb, n)["anchors"]
        if set(a) != set(b):
            bad.append(f"{n}: R{sorted(a)} vs B{sorted(b)}")
    print(f"{len(bad)} glyph(s) differ")
    for x in bad[:12]:
        print("  " + x)

    # --- 5. composites that place a mark with a raw offset ---------------
    print("\n--- accented composites carrying a nonzero mark offset ---")
    off = []
    for n in sorted(accented):
        for base, dx, dy in data[n]["components"]:
            if base.endswith("comb") or base in TOP_MARKS + BOTTOM_MARKS:
                if dx or dy:
                    off.append(f"{n}: {base} @ {dx:+.0f},{dy:+.0f}")
    print(f"{len(off)} (these are hand-placed, not anchor-driven)")
    for x in off[:12]:
        print("  " + x)


if __name__ == "__main__":
    sys.exit(main())
