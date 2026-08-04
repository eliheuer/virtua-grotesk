#!/usr/bin/env python3
"""Lane-1 recomposition: build every dotted / marked Arabic glyph as
components over a skeleton, using the green set's placement convention.

Placement rule (measured from the green composites, e.g. teh-ar.medi,
theh-ar.medi, qaf-ar.medi, noon-ar.init, beh-ar.init):

  xOffset = base.<kind>Dots.x - mark_ink_center_x
  above:  yOffset = (base.topDots.y    + 112) - mark_ink_bottom_y
  below:  yOffset = (base.bottomDots.y - 112) - mark_ink_top_y

When the base has no dot anchor, fall back to the base's ink center x and
the mark's own natural band (offset 0).

Usage:
    ./.venv/bin/python scripts/arabic_recompose.py            # build all
    ./.venv/bin/python scripts/arabic_recompose.py teh-ar     # named only
"""

import sys
import pathlib
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import write_glyph, glif_path, MASTERS  # noqa: E402

UFO = MASTERS[0]
GAP = 112          # ink gap between skeleton dot-anchor and mark band

# The font declares openTypeOS2WinAscent 1094 / WinDescent 438, so no glyph
# may put ink outside that. Marks are clamped into this envelope; anything
# that would need more is a design problem, not a metrics problem.
MAX_TOP = 1024     # matches TypoAscender and the green threedotsupabove
MIN_BOTTOM = -432


# --- geometry of an existing glyph (components resolved) --------------------

def _glyph_root(name):
    return ET.parse(glif_path(UFO, name)).getroot()


def glyph_advance(name):
    a = _glyph_root(name).find("advance")
    return float(a.get("width")) if a is not None else 0.0


def glyph_anchors(name):
    return {a.get("name"): (float(a.get("x")), float(a.get("y")))
            for a in _glyph_root(name).iter("anchor")}


def glyph_bbox(name, _seen=None):
    """Ink bbox with components resolved. Control points included — good
    enough for centering decisions."""
    _seen = _seen or set()
    if name in _seen:
        return None
    _seen = _seen | {name}
    root = _glyph_root(name)
    xs, ys = [], []
    for p in root.iter("point"):
        xs.append(float(p.get("x")))
        ys.append(float(p.get("y")))
    for comp in root.iter("component"):
        sub = glyph_bbox(comp.get("base"), _seen)
        if sub is None:
            continue
        dx = float(comp.get("xOffset") or 0)
        dy = float(comp.get("yOffset") or 0)
        xs += [sub[0] + dx, sub[2] + dx]
        ys += [sub[1] + dy, sub[3] + dy]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def place(base, mark, kind, nudge=(0, 0)):
    """Return (mark, dx, dy) placing mark on base per the green convention."""
    bb_m = glyph_bbox(mark)
    anchors = glyph_anchors(base)
    anchor = anchors.get(f"{kind}Dots") or anchors.get(kind)
    mcx = (bb_m[0] + bb_m[2]) / 2
    mh = bb_m[3] - bb_m[1]
    if anchor:
        dx = anchor[0] - mcx
        if kind == "top":
            dy = (anchor[1] + GAP) - bb_m[1]
        else:
            dy = (anchor[1] - GAP) - bb_m[3]
    else:
        bb_b = glyph_bbox(base)
        dx = (bb_b[0] + bb_b[2]) / 2 - mcx
        dy = 0
    dx += nudge[0]
    dy += nudge[1]
    # clamp into the font's vertical envelope
    if bb_m[3] + dy > MAX_TOP:
        dy = MAX_TOP - bb_m[3]
    if bb_m[1] + dy < MIN_BOTTOM:
        dy = MIN_BOTTOM - bb_m[1]
    return (mark, round(dx / 2) * 2, round(dy / 2) * 2)


# --- recipes ---------------------------------------------------------------
# (glyph, base, [(mark, kind) | (mark, kind, (nudge_x, nudge_y))])

def fam(stem, base_stem, marks, forms=("", ".init", ".medi", ".fina")):
    """Expand one dot-variant family over positional forms."""
    return [(f"{stem}-ar{f}", f"{base_stem}-ar{f}", marks) for f in forms]


RECIPES = []

# beh-family teeth (behDotless isol/init/medi/fina all exist)
RECIPES += fam("beh", "behDotless", [("dotbelow-ar", "bottom")], ("", ".fina"))
RECIPES += fam("teh", "behDotless",
               [("twodotshorizontalabove-ar", "top")], ("", ".fina"))
RECIPES += fam("theh", "behDotless",
               [("threedotsupabove-ar", "top")], ("", ".fina"))
RECIPES += fam("tteh", "behDotless",
               [("twodotshorizontalabove-ar", "top")], ("", ".fina"))
RECIPES += fam("peh", "behDotless",
               [("threedotsdownbelow-ar", "bottom")], ("", ".fina"))
RECIPES += fam("beeh", "behDotless", [("twodotsverticalbelow-ar", "bottom")])
RECIPES += fam("tteheh", "behDotless",
               [("twodotsverticalabove-ar", "top")])
RECIPES += fam("tehThreedotsdown", "behDotless",
               [("threedotsdownabove-ar", "top")])
RECIPES += fam("tehRing", "behDotless", [("ring-ar", "top")])
RECIPES += fam("yehHamzaabove", "behDotless",
               [("hamzaabove-ar", "top")], (".init", ".medi"))
RECIPES += [("yehHamzaabove-ar", "alefMaksura-ar", [("hamzaabove-ar", "top")]),
            ("yehHamzaabove-ar.fina", "alefMaksura-ar.fina",
             [("hamzaabove-ar", "top")])]
RECIPES += [("yeh-ar", "alefMaksura-ar",
             [("twodotshorizontalbelow-ar", "bottom")])]

# feh / qaf bowls
RECIPES += fam("feh", "fehDotless", [("dotabove-ar", "top")], ("", ".fina"))
RECIPES += fam("fehDotmovedbelow", "fehDotless",
               [("dotbelow-ar", "bottom")], (".init", ".medi"))
RECIPES += [("fehDotmovedbelow-ar", "qafDotless-ar",
             [("dotbelow-ar", "bottom")]),
            ("fehDotmovedbelow-ar.fina", "qafDotless-ar.fina",
             [("dotbelow-ar", "bottom")])]
RECIPES += fam("fehThreedotsbelow", "fehDotless",
               [("threedotsdownbelow-ar", "bottom")], (".init", ".medi"))
RECIPES += [("fehThreedotsbelow-ar", "qafDotless-ar",
             [("threedotsdownbelow-ar", "bottom")]),
            ("fehThreedotsbelow-ar.fina", "qafDotless-ar.fina",
             [("threedotsdownbelow-ar", "bottom")])]
RECIPES += fam("qaf", "qafDotless",
               [("twodotshorizontalabove-ar", "top")], ("", ".fina"))
RECIPES += fam("qafDotabove", "fehDotless",
               [("dotabove-ar", "top")], (".init", ".medi"))
RECIPES += [("qafDotabove-ar", "qafDotless-ar", [("dotabove-ar", "top")]),
            ("qafDotabove-ar.fina", "qafDotless-ar.fina",
             [("dotabove-ar", "top")])]
RECIPES += fam("qafThreedotsabove", "fehDotless",
               [("threedotsupabove-ar", "top")], (".init", ".medi"))
RECIPES += [("qafThreedotsabove-ar", "qafDotless-ar",
             [("threedotsupabove-ar", "top")]),
            ("qafThreedotsabove-ar.fina", "qafDotless-ar.fina",
             [("threedotsupabove-ar", "top")])]
RECIPES += fam("veh", "fehDotless",
               [("threedotsupabove-ar", "top")], ("", ".fina"))

# noon cup
RECIPES += [("noon-ar", "noonghunna-ar", [("dotabove-ar", "top")]),
            ("noon-ar.fina", "noonghunna-ar.fina", [("dotabove-ar", "top")])]

# hah family
RECIPES += fam("jeem", "hah", [("dotbelow-ar", "bottom")],
               ("", ".medi", ".fina"))
RECIPES += fam("khah", "hah", [("dotabove-ar", "top")],
               ("", ".medi", ".fina"))
RECIPES += fam("tcheh", "hah", [("threedotsdowncenter-ar", "bottom")],
               ("", ".medi", ".fina"))

# ain family
RECIPES += fam("ghain", "ain", [("dotabove-ar", "top")], ("", ".fina"))

# seen family
RECIPES += fam("sheen", "seen", [("threedotsupabove-ar", "top")],
               ("", ".medi", ".fina"))
RECIPES += fam("seenSixdots", "seen", [("threedotsdownabove-ar", "top")])

# sad / tah
RECIPES += fam("dad", "sad", [("dotabove-ar", "top")])
RECIPES += fam("zah", "tah", [("dotabove-ar", "top")])

# reh / dal
RECIPES += [("zain-ar", "reh-ar", [("dotabove-ar", "top")]),
            ("zain-ar.fina", "reh-ar.fina", [("dotabove-ar", "top")]),
            ("thal-ar", "dal-ar", [("dotabove-ar", "top")]),
            ("thal-ar.fina", "dal-ar.fina", [("dotabove-ar", "top")]),
            ("jeh-ar", "reh-ar", [("threedotsupabove-ar", "top")]),
            ("rreh-ar", "reh-ar", [("smallHighTah-ar", "top")])]

# kaf / gaf / keheh
RECIPES += fam("kehehThreedotsabove", "keheh",
               [("threedotsupabove-ar", "top")], ("", ".init", ".medi"))
RECIPES += fam("gaf", "keheh", [("gafsarkashabove-ar", "top")],
               ("", ".init", ".medi"))

# alef variants
RECIPES += [("alefMadda-ar", "alef-ar", [("madda-ar", "top")]),
            ("alefMadda-ar.fina", "alef-ar.fina", [("madda-ar", "top")]),
            ("alefWasla-ar", "alef-ar", [("wasla-ar", "top")]),
            ("alefWasla-ar.fina", "alef-ar.fina", [("wasla-ar", "top")]),
            ("alefHamzabelow-ar.fina", "alef-ar.fina",
             [("hamzabelow-ar", "bottom")])]

# lam_alef ligatures
RECIPES += [("lam_alefHamzaabove-ar", "lam_alef-ar",
             [("hamzaabove-ar", "top")]),
            ("lam_alefHamzaabove-ar.fina", "lam_alef-ar.fina",
             [("hamzaabove-ar", "top")]),
            ("lam_alefHamzabelow-ar", "lam_alef-ar",
             [("hamzabelow-ar", "bottom")]),
            ("lam_alefHamzabelow-ar.fina", "lam_alef-ar.fina",
             [("hamzabelow-ar", "bottom")]),
            ("lam_alefMadda-ar", "lam_alef-ar", [("madda-ar", "top")]),
            ("lam_alefMadda-ar.fina", "lam_alef-ar.fina",
             [("madda-ar", "top")]),
            ("lam_alefWasla-ar", "lam_alef-ar", [("wasla-ar", "top")]),
            ("lam_alefWasla-ar.fina", "lam_alef-ar.fina",
             [("wasla-ar", "top")])]

# waw / heh
RECIPES += [("wawHamzaabove-ar", "waw-ar", [("hamzaabove-ar", "top")]),
            ("wawHamzaabove-ar.fina", "waw-ar.fina",
             [("hamzaabove-ar", "top")]),
            ("tehMarbuta-ar", "heh-ar",
             [("twodotshorizontalabove-ar", "top")]),
            ("tehMarbuta-ar.fina", "heh-ar.fina",
             [("twodotshorizontalabove-ar", "top")]),
            ("tehMarbutaGoal-ar", "hehGoal-ar",
             [("twodotshorizontalabove-ar", "top")]),
            ("tehMarbutaGoal-ar.fina", "hehGoal-ar.fina",
             [("twodotshorizontalabove-ar", "top")])]
RECIPES += fam("hehGoalHamzaabove", "hehGoal", [("hamzaabove-ar", "top")])

# stacked harakat: mark over mark, both zero-advance
RECIPES += [
    ("fathatan-ar", "fatha-ar", [("fatha-ar", "top", (0, 152))]),
    ("kasratan-ar", "kasra-ar", [("kasra-ar", "top", (0, -152))]),
    ("dammatan-ar", "damma-ar", [("damma-ar", "top", (0, 176))]),
    ("hamzaaboveFatha-ar", "hamzaabove-ar", [("fatha-ar", "top", (0, 232))]),
    ("hamzaaboveFathatan-ar", "hamzaabove-ar",
     [("fathatan-ar", "top", (0, 232))]),
    ("hamzaaboveDamma-ar", "hamzaabove-ar", [("damma-ar", "top", (0, 232))]),
    ("hamzaaboveDammatan-ar", "hamzaabove-ar",
     [("dammatan-ar", "top", (0, 232))]),
    ("hamzaaboveSukun-ar", "hamzaabove-ar", [("sukun-ar", "top", (0, 232))]),
    ("hamzabelowKasra-ar", "hamzabelow-ar",
     [("kasra-ar", "bottom", (0, -168))]),
    ("hamzabelowKasratan-ar", "hamzabelow-ar",
     [("kasratan-ar", "bottom", (0, -168))]),
    ("shaddaFatha-ar", "shadda-ar", [("fatha-ar", "top", (0, 176))]),
    ("shaddaFathatan-ar", "shadda-ar", [("fathatan-ar", "top", (0, 176))]),
    ("shaddaDamma-ar", "shadda-ar", [("damma-ar", "top", (0, 176))]),
    ("shaddaDammatan-ar", "shadda-ar", [("dammatan-ar", "top", (0, 176))]),
    # shadda stays in the above band; the kasra keeps its own below band,
    # so no nudge — the two marks never meet.
    ("shaddaKasra-ar", "shadda-ar", [("kasra-ar", "bottom")]),
    ("shaddaKasratan-ar", "shadda-ar", [("kasratan-ar", "bottom")]),
    ("shaddaAlefabove-ar", "shadda-ar", [("alefabove-ar", "top", (0, 176))]),
]


def own_components(name):
    return [(e.get("base"), float(e.get("xOffset") or 0),
             float(e.get("yOffset") or 0))
            for e in _glyph_root(name).iter("component")]


def flatten(comps):
    """Google Fonts rejects nested components, so resolve any component
    whose base is itself a composite down to its primitives."""
    out = []
    for base, dx, dy in comps:
        sub = own_components(base)
        if sub:
            for sb, sdx, sdy in sub:
                out.append((sb, dx + sdx, dy + sdy))
        else:
            out.append((base, dx, dy))
    return out


def build(names=None):
    made, skipped = 0, []
    for entry in RECIPES:
        name, base, marks = entry
        if names and name not in names:
            continue
        try:
            comps = [(base, 0, 0)]
            for m in marks:
                mark, kind = m[0], m[1]
                nudge = m[2] if len(m) > 2 else (0, 0)
                comps.append(place(base, mark, kind, nudge))
            write_glyph(name, glyph_advance(base),
                        components=flatten(comps))
            made += 1
        except (KeyError, FileNotFoundError, TypeError) as e:
            skipped.append(f"{name}: missing {base if base else ''} ({e})")
    print(f"\nbuilt {made} composites")
    if skipped:
        print(f"SKIPPED {len(skipped)} (base not built yet):")
        for s in skipped:
            print("  " + s)


if __name__ == "__main__":
    build(set(sys.argv[1:]) or None)
