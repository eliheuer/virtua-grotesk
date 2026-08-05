#!/usr/bin/env python3
"""Make the Latin diacritic system anchor-driven and consistent.

Unlike the Arabic (where both masters hold identical outlines), the Latin
IS properly bolded — so every anchor and every composite offset is computed
PER MASTER from that master's own ink. Nothing here writes one master's
geometry into the other.

What it does, in order:

1. `_top` / `_bottom` anchors on the 14 spacing accents, at (ink centre,
   576 / 0). Several had none at all; several sat at 576 regardless of
   where the ink was.
2. The 14 combining marks (`Xcomb`), which were ALL EMPTY — every
   combining accent in the font rendered blank. Each becomes a zero-width
   component of its spacing accent carrying the same attachment anchor,
   plus a `top`/`bottom` anchor so marks can stack (mkmk).
3. `top` / `bottom` anchors on every base letter that lacked them
   (20 of them: B F H J M P Q V X b d f h i j m p q v x).
4. Every accented composite re-placed from the anchors, so the whole
   family is consistent. 140 of them carried hand-tuned offsets that
   disagreed with each other — Acircumflex sat 105 units higher than
   Aacute, which is why it was the tallest glyph in the font.

Usage:
    ./.venv/bin/python scripts/latin_marks.py [--dry-run]
"""

import pathlib
import plistlib
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = {"Regular": REPO / "sources" / "VirtuaGrotesk-Regular.ufo",
           "Bold": REPO / "sources" / "VirtuaGrotesk-Bold.ufo"}
BLUE = "0,0.67,0.91,1"

XHEIGHT, CAP = 576.0, 768.0

TOP_ACCENTS = ["grave", "acute", "circumflex", "tilde", "macron", "breve",
               "dotaccent", "dieresis", "ring", "hungarumlaut", "caron"]
BOTTOM_ACCENTS = ["cedilla", "ogonek", "commaaccent"]


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def path_of(ufo, cmap, name):
    return ufo / "glyphs" / cmap[name]


def bbox(ufo, cmap, name, _seen=None):
    """Ink bbox with components resolved."""
    _seen = _seen or set()
    if name in _seen or name not in cmap:
        return None
    _seen = _seen | {name}
    root = ET.parse(path_of(ufo, cmap, name)).getroot()
    xs = [float(p.get("x")) for p in root.iter("point")]
    ys = [float(p.get("y")) for p in root.iter("point")]
    for comp in root.iter("component"):
        sub = bbox(ufo, cmap, comp.get("base"), _seen)
        if not sub:
            continue
        dx = float(comp.get("xOffset") or 0)
        dy = float(comp.get("yOffset") or 0)
        xs += [sub[0] + dx, sub[2] + dx]
        ys += [sub[1] + dy, sub[3] + dy]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def anchors_of(ufo, cmap, name):
    root = ET.parse(path_of(ufo, cmap, name)).getroot()
    return {a.get("name"): (float(a.get("x")), float(a.get("y")))
            for a in root.iter("anchor")}


def fmt(v):
    return str(int(round(v)))


def set_anchors(ufo, cmap, name, new):
    """Add/replace named anchors in a glif, leaving everything else alone."""
    p = path_of(ufo, cmap, name)
    text = p.read_text()
    for aname, (x, y) in new.items():
        line = f'\t<anchor name="{aname}" x="{fmt(x)}" y="{fmt(y)}"/>'
        pat = re.compile(rf'\t<anchor name="{re.escape(aname)}"[^/]*/>\n')
        if pat.search(text):
            text = pat.sub(line + "\n", text, count=1)
        else:
            text = text.replace("\t</outline>\n", "\t</outline>\n" + line + "\n", 1)
    p.write_text(text)


def set_component_offset(ufo, cmap, name, base, dx, dy):
    """Rewrite one component's offsets inside a composite glif."""
    p = path_of(ufo, cmap, name)
    text = p.read_text()
    pat = re.compile(rf'(\t\t<component base="{re.escape(base)}")[^/]*(/>)')
    attrs = ""
    if round(dx):
        attrs += f' xOffset="{fmt(dx)}"'
    if round(dy):
        attrs += f' yOffset="{fmt(dy)}"'
    new, n = pat.subn(lambda m: m.group(1) + attrs + m.group(2), text, count=1)
    if n:
        p.write_text(new)
    return bool(n)


def is_accented(cmap, ufo, name):
    root = ET.parse(path_of(ufo, cmap, name)).getroot()
    for u in root.iter("unicode"):
        try:
            ch = chr(int(u.get("hex"), 16))
        except ValueError:
            return False
        d = unicodedata.decomposition(ch).split()
        return "LATIN" in unicodedata.name(ch, "") and len(d) > 1
    return False


def main():
    dry = "--dry-run" in sys.argv
    report = {"accent_anchors": 0, "combs": 0, "base_anchors": 0,
              "composites": 0, "skipped": []}

    for mname, ufo in MASTERS.items():
        cmap = contents(ufo)

        # -- 1. attachment anchors on the spacing accents ------------------
        for a in TOP_ACCENTS + BOTTOM_ACCENTS:
            if a not in cmap:
                continue
            bb = bbox(ufo, cmap, a)
            if not bb:
                continue
            cx = (bb[0] + bb[2]) / 2
            key = "_top" if a in TOP_ACCENTS else "_bottom"
            y = XHEIGHT if key == "_top" else 0.0
            if not dry:
                set_anchors(ufo, cmap, a, {key: (cx, y)})
            report["accent_anchors"] += 1

        # -- 2. the combining marks ----------------------------------------
        for a in TOP_ACCENTS + BOTTOM_ACCENTS:
            comb = f"{a}comb"
            if comb not in cmap or a not in cmap:
                continue
            bb = bbox(ufo, cmap, a)
            if not bb:
                continue
            cx = (bb[0] + bb[2]) / 2
            top = a in TOP_ACCENTS
            key = "_top" if top else "_bottom"
            stack = "top" if top else "bottom"
            # stacking anchor: just clear of this mark's own ink
            stack_y = bb[3] + 32 if top else bb[1] - 32
            if not dry:
                p = path_of(ufo, cmap, comb)
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>\n'
                    f'<glyph name="{comb}" format="2">\n')
                old = p.read_text()
                for h in re.findall(r'<unicode hex="([0-9A-Fa-f]+)"/>', old):
                    body += f'\t<unicode hex="{h}"/>\n'
                body += ('\t<advance width="0"/>\n'
                         '\t<outline>\n'
                         f'\t\t<component base="{a}"/>\n'
                         '\t</outline>\n'
                         f'\t<anchor name="{key}" x="{fmt(cx)}" y="{fmt(XHEIGHT if top else 0)}"/>\n'
                         f'\t<anchor name="{stack}" x="{fmt(cx)}" y="{fmt(stack_y)}"/>\n'
                         '\t<lib>\n\t\t<dict>\n'
                         '\t\t\t<key>public.markColor</key>\n'
                         f'\t\t\t<string>{BLUE}</string>\n'
                         '\t\t</dict>\n\t</lib>\n'
                         '</glyph>\n')
                p.write_text(body)
            report["combs"] += 1

        # -- 3. anchors on the base letters --------------------------------
        for g in sorted(cmap):
            if len(g) != 1 or not g.isalpha():
                continue
            have = anchors_of(ufo, cmap, g)
            if "top" in have and "bottom" in have:
                continue
            bb = bbox(ufo, cmap, g)
            if not bb:
                continue
            cx = round((bb[0] + bb[2]) / 4) * 2
            y = CAP if g.isupper() else XHEIGHT
            if not dry:
                set_anchors(ufo, cmap, g,
                            {"top": (cx, y), "bottom": (cx, 0.0)})
            report["base_anchors"] += 1

        # -- 4. re-place every accented composite from the anchors ---------
        for g in sorted(cmap):
            if not is_accented(cmap, ufo, g):
                continue
            root = ET.parse(path_of(ufo, cmap, g)).getroot()
            comps = [c.get("base") for c in root.iter("component")]
            if len(comps) < 2:
                continue
            base, marks = comps[0], comps[1:]
            base_anc = anchors_of(ufo, cmap, base)
            for m in marks:
                if m not in cmap:
                    continue
                m_anc = anchors_of(ufo, cmap, m)
                for key, bkey in (("_top", "top"), ("_bottom", "bottom")):
                    if key in m_anc and bkey in base_anc:
                        dx = base_anc[bkey][0] - m_anc[key][0]
                        dy = base_anc[bkey][1] - m_anc[key][1]
                        if not dry:
                            set_component_offset(ufo, cmap, g, m, dx, dy)
                        report["composites"] += 1
                        break
                else:
                    report["skipped"].append(f"{mname} {g}: {m} has no "
                                             f"attachment anchor")

    verb = "would set" if dry else "set"
    print(f"{verb} (both masters):")
    print(f"  accent attachment anchors : {report['accent_anchors']}")
    print(f"  combining marks built     : {report['combs']}")
    print(f"  base letters given anchors: {report['base_anchors']}")
    print(f"  composites re-placed      : {report['composites']}")
    if report["skipped"]:
        uniq = sorted(set(report["skipped"]))
        print(f"  SKIPPED {len(uniq)}:")
        for s in uniq[:12]:
            print("    " + s)


if __name__ == "__main__":
    sys.exit(main())
