#!/usr/bin/env python3
"""#12 -- real anchors for diacritics, modeled on Rubik's scheme.

Writes anchors into the UFO (the durable source of truth, editable in
Runebender and usable by ufo2ft's mark feature -- the foundation for
Arabic/Hebrew), then rebuilds every accent composite's component offset from
those anchors (preserving the already-correct yOffset).

Rubik's rules (normalized): base top/bottom anchor at the glyph's optical
center; mark _top at its center EXCEPT the angled marks lean --
acute _top = center-56, grave = center+44 (per 1000upm; ~same in Virtua's
1024). Symmetric marks (dieresis/circumflex/tilde/macron/caron/breve/ring) and
below marks (cedilla) attach at center.

Idempotent: strips its own anchors before rewriting, so it can be rerun after
any base-glyph edit to re-center everything. Ogonek (corner attach) deferred.
"""
import re, glob, os

XH = 576
CAP = 768
OPTICAL = {"acute": -56, "grave": 44}          # mark _top x-offset from center
TOP_MARKS = {"acute", "grave", "circumflex", "dieresis", "tilde", "macron",
             "caron", "breve", "ring", "hungarumlaut", "dotaccent"}
BELOW_MARKS = {"cedilla", "commaaccent"}
MARKS = TOP_MARKS | BELOW_MARKS

def read(p): return open(p).read()
def ink_center(t):
    xs = [float(x) for x in re.findall(r'point x="(-?[\d.]+)"', t)]
    return (min(xs) + max(xs)) / 2 if xs else None
def ys(t):
    return [float(y) for y in re.findall(r'point y="(-?[\d.]+)"', t)]
def snap2(v): return int(round(v / 2) * 2)

def strip_anchors(t):
    return re.sub(r'[ \t]*<anchor[^>]*/>\n?', '', t)

def add_anchors(t, anchors):
    """Insert <anchor> elements right after </outline>."""
    block = "".join(f'\t<anchor name="{n}" x="{x}" y="{y}"/>\n' for n, x, y in anchors)
    return t.replace("</outline>\n", "</outline>\n" + block, 1)

def is_cap(name):
    # cap composites are files like A_acute.glif (glyph name Aacute); heuristic:
    return name[:1].isupper()

def process(master):
    G = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
    txt = {os.path.basename(p)[:-5]: read(p) for p in glob.glob(f"{G}/*.glif")}
    # glyph name from file: strip Glyphs '_' suffix escaping is already the name inside; use <glyph name=>
    name_of = {f: re.search(r'<glyph name="([^"]+)"', t).group(1) for f, t in txt.items()}
    center = {name_of[f]: ink_center(t) for f, t in txt.items()}

    # 1) anchors on marks
    for f, t in list(txt.items()):
        nm = name_of[f]
        if nm not in MARKS:
            continue
        c = center.get(nm)
        if c is None:
            continue
        t = strip_anchors(t)
        if nm in TOP_MARKS:
            off = OPTICAL.get(nm, 0)
            t = add_anchors(t, [("_top", snap2(c + off), XH)])
        else:  # below
            t = add_anchors(t, [("_bottom", snap2(c), 0)])
        txt[f] = t

    # 2) anchors on bases (any glyph used as the first component of a composite)
    base_names = set()
    for f, t in txt.items():
        comps = re.findall(r'<component base="([^"]+)"', t)
        if len(comps) == 2 and comps[1] in MARKS:
            base_names.add(comps[0])
    for f, t in list(txt.items()):
        nm = name_of[f]
        if nm not in base_names:
            continue
        c = center.get(nm)
        if c is None:
            continue
        top_y = CAP if is_cap(nm) else XH
        t = strip_anchors(t)
        t = add_anchors(t, [("top", snap2(c), top_y), ("bottom", snap2(c), 0)])
        txt[f] = t
        center[nm] = c  # unchanged

    # recompute anchor lookups after writing (parse from the written text)
    def anchor_x(nm, aname):
        m = re.search(rf'<anchor name="{aname}" x="(-?\d+)"', txt_by_name.get(nm, ""))
        return int(m.group(1)) if m else None
    txt_by_name = {name_of[f]: t for f, t in txt.items()}

    # 3) rebuild composite offsets from anchors (xOffset only; keep yOffset)
    fixed = 0
    for f, t in list(txt.items()):
        comps = re.findall(r'<component base="([^"]+)"([^/]*)/>', t)
        if len(comps) != 2:
            continue
        (base, ba), (mark, ma) = comps
        if mark not in MARKS:
            continue
        if mark in TOP_MARKS:
            bx = anchor_x(base, "top"); mx = anchor_x(mark, "_top")
        else:
            bx = anchor_x(base, "bottom"); mx = anchor_x(mark, "_bottom")
        if bx is None or mx is None:
            continue
        newx = bx - mx
        def repl(m):
            attrs = re.sub(r'\s*xOffset="[^"]*"', '', m.group(1))
            return f'<component base="{mark}"{attrs} xOffset="{newx}"/>'
        t2 = re.sub(rf'<component base="{re.escape(mark)}"([^/]*)/>', repl, t)
        if t2 != t:
            txt[f] = t2; fixed += 1

    for f, t in txt.items():
        open(f"{G}/{f}.glif", "w").write(t)
    print(f"{master}: {len(base_names)} bases + marks anchored, {fixed} composites rebuilt")

for m in ["Regular", "Bold"]:
    process(m)
