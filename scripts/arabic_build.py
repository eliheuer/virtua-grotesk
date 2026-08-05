#!/usr/bin/env python3
"""Construction toolkit for the Arabic completion pass.

Writes .glif XML directly in repo style (tabs, double quotes, attribute
order x, y, type, smooth) — never via font.save(). Glyphs are written
identically into BOTH masters (the green Arabic convention: Bold == Regular
until the Arabic bold pass). All output is marked BLUE (AI, awaiting
grading).

This module is a library + CLI: lane runners import the helpers; running
it directly builds the glyphs named on the command line.
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = [REPO / "sources" / "VirtuaGrotesk-Regular.ufo",
           REPO / "sources" / "VirtuaGrotesk-Bold.ufo"]
BLUE = "0,0.67,0.91,1"

_contents = {m: plistlib.loads((m / "glyphs" / "contents.plist").read_bytes())
             for m in MASTERS}


def glif_path(master, name):
    return master / "glyphs" / _contents[master][name]


def _glif_filename(name):
    """UFO filename convention used in this repo: an underscore after each
    uppercase letter, '.' kept."""
    out = []
    for ch in name:
        out.append(ch)
        if ch.isupper():
            out.append("_")
    return "".join(out) + ".glif"


def register_glyph(name):
    """Register a NEW glyph in all three places per master: contents.plist,
    public.glyphOrder in lib.plist, and (by the caller) the glif itself.
    Both plists are edited surgically to preserve the repo's tab style."""
    fn = _glif_filename(name)
    for m in MASTERS:
        if name in _contents[m]:
            continue
        # --- contents.plist: insert before the closing </dict>
        cp = m / "glyphs" / "contents.plist"
        text = cp.read_text()
        entry = f"\t<key>{name}</key>\n\t<string>{fn}</string>\n"
        i = text.rindex("</dict>")
        cp.write_text(text[:i] + entry + text[i:])
        _contents[m][name] = fn
        # --- lib.plist: append to public.glyphOrder
        lp = m / "lib.plist"
        text = lp.read_text()
        key = "<key>public.glyphOrder</key>"
        j = text.index(key)
        end = text.index("\t</array>", j)
        # keep .notdef last, as the existing order does
        notdef = text.find("\t\t<string>.notdef</string>\n", j, end)
        k = notdef if notdef != -1 else end
        lp.write_text(text[:k] + f"\t\t<string>{name}</string>\n" + text[k:])
    return fn


def read_points(name, master=MASTERS[0]):
    """Contours of a green donor as lists of (x, y, type, smooth)."""
    root = ET.parse(glif_path(master, name)).getroot()
    out = []
    for c in root.iter("contour"):
        out.append([(float(p.get("x")), float(p.get("y")),
                     p.get("type"), p.get("smooth") == "yes")
                    for p in c.iter("point")])
    return out


def translate(contour, dx, dy):
    return [(x + dx, y + dy, t, s) for x, y, t, s in contour]


def mirror_x(contour, axis):
    """Mirror around vertical line x=axis, reversing to keep winding."""
    pts = [(2 * axis - x, y, t, s) for x, y, t, s in contour]
    return reverse_contour(pts)


def reverse_contour(pts):
    """Reverse a closed contour. In glif order a point's type marks the
    segment ENDING at it, so we rebuild via segments: rotate to start at an
    on-curve point, split into segments, walk them backwards."""
    start = next(i for i, p in enumerate(pts) if p[2])
    pts = pts[start:] + pts[:start]
    segs = []          # (offcurves, end_point)
    cur = []
    for p in pts[1:] + [pts[0]]:
        if p[2]:
            segs.append((cur, p))
            cur = []
        else:
            cur.append(p)
    out = []
    anchor = pts[0]
    prev_start = anchor
    # walking segments in reverse: each reversed segment ends at the
    # original segment's START point and reuses the original's type
    rev = []
    for i in range(len(segs) - 1, -1, -1):
        offs, end = segs[i]
        seg_start = segs[i - 1][1] if i > 0 else anchor
        rev.append((list(reversed(offs)), seg_start, end[2]))
    out = [(anchor[0], anchor[1], "curve" if segs and segs[-1][1][2] == "curve"
            else "line", anchor[3])]
    # first element of out is the new start = old start (anchor); its type is
    # the type of the segment that now ends there = old first segment's type
    out = [(anchor[0], anchor[1], segs[0][1][2] if segs else "line", anchor[3])]
    for offs, endpt, typ in rev:
        for ox, oy, _, os_ in offs:
            out.append((ox, oy, None, os_))
        out.append((endpt[0], endpt[1], typ, endpt[3]))
    # the final appended point duplicates the anchor; drop it
    return out[:-1]


def union(contours):
    """FLAT RULE: merge overlapping contours into one flat outline.
    Cubic-aware union via booleanOperations on a scratch defcon glyph
    (per the repo's union recipe), rounded back to the 2-grid."""
    import defcon
    from booleanOperations import BooleanOperationManager
    from fontTools.pens.pointPen import AbstractPointPen

    scratch = defcon.Glyph()
    pen = scratch.getPointPen()
    for c in contours:
        pen.beginPath()
        for x, y, t, s in c:
            pen.addPoint((x, y), t, s)
        pen.endPath()

    class _Collect(AbstractPointPen):
        def __init__(self):
            self.contours = []
        def beginPath(self, **kw):
            self._cur = []
        def addPoint(self, pt, segmentType=None, smooth=False, **kw):
            self._cur.append((round(pt[0] / 2) * 2, round(pt[1] / 2) * 2,
                              segmentType, smooth))
        def endPath(self):
            self.contours.append(self._cur)
        def addComponent(self, *a, **kw):
            pass

    out = _Collect()
    BooleanOperationManager.union(list(scratch), out)
    return out.contours


def fmt_num(v):
    v = round(v)
    return str(int(v))


def contour_xml(contour, indent="\t\t"):
    lines = [f"{indent}<contour>"]
    for x, y, t, s in contour:
        attrs = f'x="{fmt_num(x)}" y="{fmt_num(y)}"'
        if t:
            attrs += f' type="{t}"'
        if s:
            attrs += ' smooth="yes"'
        lines.append(f"{indent}\t<point {attrs}/>")
    lines.append(f"{indent}</contour>")
    return "\n".join(lines)


def component_xml(base, dx=0, dy=0, indent="\t\t"):
    attrs = f'base="{base}"'
    if dx:
        attrs += f' xOffset="{fmt_num(dx)}"'
    if dy:
        attrs += f' yOffset="{fmt_num(dy)}"'
    return f"{indent}<component {attrs}/>"


def write_glyph(name, advance, contours=(), components=(), anchors=(),
                unicode_hex=None, color=BLUE):
    """Write the glyph into both masters, repo-style XML. contours are
    point lists; components are (base, dx, dy); anchors are (name, x, y)."""
    body = []
    body.append('<?xml version="1.0" encoding="UTF-8"?>')
    body.append(f'<glyph name="{name}" format="2">')
    # Runebender writes <unicode> BEFORE <advance>; match it so a
    # regenerated glyph does not churn against a Runebender save.
    if unicode_hex:
        body.append(f'\t<unicode hex="{unicode_hex}"/>')
    body.append(f'\t<advance width="{fmt_num(advance)}"/>')
    body.append("\t<outline>")
    for base, dx, dy in components:
        body.append(component_xml(base, dx, dy))
    for c in contours:
        body.append(contour_xml(c))
    body.append("\t</outline>")
    for aname, ax, ay in anchors:
        body.append(f'\t<anchor name="{aname}" x="{fmt_num(ax)}" y="{fmt_num(ay)}"/>')
    body.append("\t<lib>")
    body.append("\t\t<dict>")
    body.append("\t\t\t<key>public.markColor</key>")
    body.append(f"\t\t\t<string>{color}</string>")
    body.append("\t\t</dict>")
    body.append("\t</lib>")
    body.append("</glyph>")
    body.append("")
    text = "\n".join(body)
    register_glyph(name)
    for m in MASTERS:
        # keep existing unicode assignment if the file already has one
        p = glif_path(m, name)
        old = p.read_text() if p.exists() else ""
        if unicode_hex is None:
            hexes = re.findall(r'<unicode hex="([0-9A-Fa-f]+)"/>', old)
            if hexes:
                t = text.replace(f'\t<advance width="{fmt_num(advance)}"/>',
                                 "".join(f'\t<unicode hex="{h}"/>\n'
                                         for h in hexes)
                                 + f'\t<advance width="{fmt_num(advance)}"/>',
                                 1)
            else:
                t = text
        else:
            t = text
        p.write_text(t)
    print(f"wrote {name} (adv {fmt_num(advance)}) -> both masters")


# ---------------------------------------------------------------------------
# geometry idiom helpers (all values from the green donors / grammar doc)

BAR = 104          # baseline joining-bar height
STEM = 96          # vertical stroke
CH = 16            # chamfer
TOOTH_LIP = 432    # beh/noon tooth height


def stub_left():
    """Joining stub run at the LEFT edge (x=-16), as in behDotless.init:
    ... (0,104) is provided by caller; this returns the two stub points."""
    return [(-16, 88, "line", False), (-16, 16, "line", False)]
