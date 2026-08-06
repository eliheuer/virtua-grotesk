#!/usr/bin/env python3
"""Put the Arabic on a real anchor system, modelled on Rubik.

The problem: of 128 Arabic composites carrying a dot or mark, only 47 sat
where their anchors said. 8 of the 14 marks had no attachment anchor at
all, so their placement fell back to a homegrown "ink centre + 112" rule
and drifted.

Rubik's model, which this adopts — the important idea is that **dots and
harakat use different slots**:

    topDots / bottomDots   the letter's own dots, tucked close to it
    top / bottom           vowel marks, clear above/below everything

Marks carry the matching `_topDots` / `_bottomDots` / `_top` / `_bottom`,
plus a plain `top`/`bottom` for mark-on-mark stacking. A composite's stored
offset is then exactly `base.slot - mark._slot` — in Rubik every one I
checked matches to the unit, e.g. teh-ar.init stores (-90,-194) and
base topDots (110,326) minus mark _topDots (200,520) is (-90,-194).

The attachment constant comes from Virtua's own GREEN composites, not from
Rubik: a top mark's ink bottom lands 112 above the base's slot. Check:
behDotless-ar.init topDots is y=448, and green noon-ar.init places
dotabove-ar at yOffset -128, putting its ink bottom at 688-128 = 560 =
448+112. So `_topDots` on a mark = (ink centre, ink_bottom - 112).

GREEN IS THE SOURCE OF TRUTH. Existing anchor values are never moved —
only missing ones are added — and if recomputing a green composite would
shift it, the offset is left alone and reported instead.

Usage:
    ./.venv/bin/python scripts/arabic_anchors.py [--dry-run]
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = {"Regular": REPO / "sources" / "VirtuaGrotesk-Regular.ufo",
           "Bold": REPO / "sources" / "VirtuaGrotesk-Bold.ufo"}
GREEN = "0.09,0.72,0.44,1"
GAP = 112                     # ink clearance between a slot and its mark
MIN_Y, MAX_Y = -438.0, 1094.0 # the font's declared WinDescent / WinAscent

# marks that are the LETTER'S OWN DOTS -> the *Dots slots
DOT_MARKS = {
    "dotabove-ar", "dotbelow-ar", "dotcenter-ar",
    "twodotshorizontalabove-ar", "twodotshorizontalbelow-ar",
    "twodotsverticalabove-ar", "twodotsverticalbelow-ar",
    "threedotsupabove-ar", "threedotsupbelow-ar",
    "threedotsdownabove-ar", "threedotsdownbelow-ar",
    "threedotsdowncenter-ar", "ring-ar",
    "gafsarkashabove-ar", "gafsarkashcenter-ar", "smallHighTah-ar",
    "smallHighZain-ar", "smallHighThreeDots-ar", "miniKeheh-ar",
}
# vowel marks and hamza -> the plain top/bottom slots, clear of the dots
HARAKAT = {
    "fatha-ar", "kasra-ar", "damma-ar", "shadda-ar", "sukun-ar",
    "madda-ar", "wasla-ar", "hamzaabove-ar", "hamzabelow-ar",
    "alefabove-ar", "alefbelow-ar", "invertedDamma-ar",
    "fathatan-ar", "kasratan-ar", "dammatan-ar",
}
BELOW = {"dotbelow-ar", "twodotshorizontalbelow-ar", "twodotsverticalbelow-ar",
         "threedotsupbelow-ar", "threedotsdownbelow-ar", "kasra-ar",
         "kasratan-ar", "hamzabelow-ar", "alefbelow-ar"}


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def gpath(ufo, cmap, n):
    return ufo / "glyphs" / cmap[n]


def is_green(ufo, cmap, n):
    return GREEN in gpath(ufo, cmap, n).read_text()


def anchors(ufo, cmap, n):
    r = ET.parse(gpath(ufo, cmap, n)).getroot()
    return {a.get("name"): (float(a.get("x")), float(a.get("y")))
            for a in r.iter("anchor")}


def components(ufo, cmap, n):
    r = ET.parse(gpath(ufo, cmap, n)).getroot()
    return [(c.get("base"), float(c.get("xOffset") or 0),
             float(c.get("yOffset") or 0)) for c in r.iter("component")]


def bbox(ufo, cmap, n, _seen=None):
    _seen = _seen or set()
    if n in _seen or n not in cmap:
        return None
    _seen = _seen | {n}
    r = ET.parse(gpath(ufo, cmap, n)).getroot()
    xs = [float(p.get("x")) for p in r.iter("point")]
    ys = [float(p.get("y")) for p in r.iter("point")]
    for c in r.iter("component"):
        sub = bbox(ufo, cmap, c.get("base"), _seen)
        if not sub:
            continue
        dx = float(c.get("xOffset") or 0)
        dy = float(c.get("yOffset") or 0)
        xs += [sub[0] + dx, sub[2] + dx]
        ys += [sub[1] + dy, sub[3] + dy]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def f(v):
    return str(int(round(v)))


def set_anchors(ufo, cmap, n, new, overwrite=False):
    """Add anchors; never move an existing one unless overwrite is set."""
    p = gpath(ufo, cmap, n)
    text = p.read_text()
    have = set(anchors(ufo, cmap, n))
    changed = False
    for name, (x, y) in new.items():
        if name in have and not overwrite:
            continue
        line = f'\t<anchor name="{name}" x="{f(x)}" y="{f(y)}"/>'
        pat = re.compile(rf'\t<anchor name="{re.escape(name)}"[^/]*/>\n')
        if pat.search(text):
            text = pat.sub(line + "\n", text, count=1)
        else:
            text = text.replace("\t</outline>\n",
                                "\t</outline>\n" + line + "\n", 1)
        changed = True
    if changed:
        p.write_text(text)
    return changed


def drop_anchors(ufo, cmap, n, names):
    """Remove named anchors from a glif."""
    p = gpath(ufo, cmap, n)
    text = p.read_text()
    out = text
    for name in names:
        out = re.sub(rf'\t<anchor name="{re.escape(name)}"[^/]*/>\n', "", out)
    if out != text:
        p.write_text(out)
        return True
    return False


def set_offset(ufo, cmap, n, base, dx, dy):
    p = gpath(ufo, cmap, n)
    text = p.read_text()
    pat = re.compile(rf'(\t\t<component base="{re.escape(base)}")[^/]*(/>)')
    attrs = ""
    if round(dx):
        attrs += f' xOffset="{f(dx)}"'
    if round(dy):
        attrs += f' yOffset="{f(dy)}"'
    new, k = pat.subn(lambda m: m.group(1) + attrs + m.group(2), text, count=1)
    if k:
        p.write_text(new)
    return bool(k)


def slot_for(mark):
    """Which slot this mark attaches into, and on which side."""
    below = mark in BELOW
    if mark in DOT_MARKS:
        return ("_bottomDots", "bottomDots") if below else ("_topDots",
                                                            "topDots")
    return ("_bottom", "bottom") if below else ("_top", "top")


def main():
    dry = "--dry-run" in sys.argv
    stats = {"mark_anchors": 0, "base_slots": 0, "offsets": 0}
    kept_green, no_slot = [], []

    for mname, ufo in MASTERS.items():
        cmap = contents(ufo)
        arabic = [n for n in cmap if "-ar" in n]

        # -- 1. attachment + stacking anchors on every mark ---------------
        for m in sorted(set(DOT_MARKS | HARAKAT) & set(arabic)):
            bb = bbox(ufo, cmap, m)
            if not bb:
                continue
            cx = (bb[0] + bb[2]) / 2
            under, _ = slot_for(m)
            if m in BELOW:
                att = (cx, bb[3] + GAP)          # ink top sits GAP below slot
                stack = ("bottom", (cx, bb[1] - 48))
            else:
                att = (cx, bb[1] - GAP)          # ink bottom sits GAP above
                stack = ("top", (cx, bb[3] + 48))
            if not dry:
                if set_anchors(ufo, cmap, m, {under: att, stack[0]: stack[1]}):
                    stats["mark_anchors"] += 1

        # -- 2. slots on every base that lacks them ------------------------
        for n in sorted(arabic):
            if components(ufo, cmap, n):
                continue                          # composites handled below
            bb = bbox(ufo, cmap, n)
            if not bb:
                continue
            cx = round((bb[0] + bb[2]) / 4) * 2
            want = {"topDots": (cx, bb[3]), "bottomDots": (cx, bb[1]),
                    "top": (cx, bb[3]), "bottom": (cx, bb[1])}
            if not dry:
                if set_anchors(ufo, cmap, n, want):
                    stats["base_slots"] += 1

        # -- 3. every composite placed as base.slot - mark._slot -----------
        for n in sorted(arabic):
            comps = components(ufo, cmap, n)
            if len(comps) < 2:
                continue
            base = comps[0][0]
            if base not in cmap:
                continue
            ba = anchors(ufo, cmap, base)
            green = is_green(ufo, cmap, n)
            for mark, dx0, dy0 in comps[1:]:
                if mark not in cmap:
                    continue
                under, slot = slot_for(mark)
                ma = anchors(ufo, cmap, mark)
                if under not in ma or slot not in ba:
                    no_slot.append(f"{n}: {mark} -> {slot}")
                    continue
                mbb = bbox(ufo, cmap, mark)
                bbb = bbox(ufo, cmap, base)
                if base in DOT_MARKS | HARAKAT and mbb and bbb:
                    # MARK ON MARK (dammatan = damma over damma). The
                    # base/mark anchor pair is meant for a letter and a
                    # mark; used between two marks it throws the second one
                    # far out of the envelope. Stack tightly instead.
                    dx = ((bbb[0] + bbb[2]) - (mbb[0] + mbb[2])) / 2
                    dy = (bbb[3] + 32) - mbb[1] if mark not in BELOW \
                        else (bbb[1] - 32) - mbb[3]
                else:
                    dx = ba[slot][0] - ma[under][0]
                    dy = ba[slot][1] - ma[under][1]
                # WinAscent 1094 / WinDescent 438 are hard limits.
                if mbb:
                    if mbb[3] + dy > MAX_Y:
                        dy = MAX_Y - mbb[3]
                    if mbb[1] + dy < MIN_Y:
                        dy = MIN_Y - mbb[1]
                if green and (abs(dx - dx0) > 2 or abs(dy - dy0) > 2):
                    # Eli graded this placement: keep it, report the drift
                    kept_green.append(
                        f"{n}: {mark} kept at {dx0:+.0f},{dy0:+.0f} "
                        f"(anchors say {dx:+.0f},{dy:+.0f})")
                    continue
                if not dry and set_offset(ufo, cmap, n, mark, dx, dy):
                    stats["offsets"] += 1

            # composite inherits the base's slots, but `top`/`bottom` move
            # clear of the dots so harakat stack above them (Rubik does the
            # same: teh-ar.init raises top from 520 to 556)
            bb = bbox(ufo, cmap, n)
            if bb and not dry:
                # A composite keeps ONLY top/bottom. Those are load-bearing:
                # they are where a haraka attaches (several composites are
                # in @ARAB_MARK_BASES in features.fea), and they must clear
                # the dots the composite just added.
                #
                # It does NOT keep topDots/bottomDots. A letter that already
                # has its dots never receives more, and no Arabic composite
                # is a base for another glyph — so those slots would only be
                # dead weight in the source.
                inherit = {}
                if "top" in ba:
                    inherit["top"] = (ba["top"][0], max(ba["top"][1], bb[3]))
                if "bottom" in ba:
                    inherit["bottom"] = (ba["bottom"][0],
                                         min(ba["bottom"][1], bb[1]))
                set_anchors(ufo, cmap, n, inherit, overwrite=True)
                drop_anchors(ufo, cmap, n, ("topDots", "bottomDots"))

    verb = "would set" if dry else "set"
    print(f"{verb} (both masters):")
    print(f"  marks given attachment anchors : {stats['mark_anchors']}")
    print(f"  bases given slots              : {stats['base_slots']}")
    print(f"  composite offsets from anchors : {stats['offsets']}")
    if kept_green:
        u = sorted(set(kept_green))
        print(f"\n  GREEN placements kept as-is ({len(u)}) — these are your "
              f"graded positions; the anchors disagree:")
        for s in u[:15]:
            print("    " + s)
    if no_slot:
        u = sorted(set(no_slot))
        print(f"\n  no matching slot ({len(u)}):")
        for s in u[:10]:
            print("    " + s)


if __name__ == "__main__":
    sys.exit(main())
