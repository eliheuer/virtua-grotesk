#!/usr/bin/env python3
"""Structural lint for the UFO sources — the checks that catch scripted
construction errors before `make build` does, with a glyph name attached.

Checks, per master:
  * every component base exists, and no glyph components itself
  * no empty / 1-point / all-off-curve contours
  * every 'curve' segment has exactly 2 off-curve points (a curve with 0
    off-curves is what makes cu2qu raise a bare IndexError)
  * no zero-length curve segments (start == end with coincident handles)
  * masters agree on contour count, per-contour point count, and the
    component list

Exit code 1 if anything is found.

Usage:
    ./.venv/bin/python scripts/glif_lint.py [glyph ...]
"""

import pathlib
import plistlib
import sys
import xml.etree.ElementTree as ET

REPO = pathlib.Path(__file__).resolve().parent.parent
MASTERS = {"Regular": REPO / "sources" / "VirtuaGrotesk-Regular.ufo",
           "Bold": REPO / "sources" / "VirtuaGrotesk-Bold.ufo"}


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def contours_of(root):
    out = []
    for cont in root.iter("contour"):
        out.append([(float(p.get("x")), float(p.get("y")), p.get("type"))
                    for p in cont.iter("point")])
    return out


def segments(points):
    """Yield (start, offcurves, end) for a closed contour."""
    if not points or not any(p[2] for p in points):
        return
    s = next(i for i, p in enumerate(points) if p[2])
    pts = points[s:] + points[:s]
    prev, cur = pts[0], []
    for p in pts[1:] + [pts[0]]:
        if p[2]:
            yield prev, cur, p
            prev, cur = p, []
        else:
            cur.append(p)


def lint(only=None):
    findings = []
    shapes = {}
    for mname, ufo in MASTERS.items():
        cmap = contents(ufo)
        shapes[mname] = {}
        for name, fn in sorted(cmap.items()):
            if only and name not in only:
                continue
            path = ufo / "glyphs" / fn
            if not path.exists():
                findings.append(f"{mname} {name}: glif file missing ({fn})")
                continue
            root = ET.parse(path).getroot()
            comps = [e.get("base") for e in root.iter("component")]
            for b in comps:
                if b not in cmap:
                    findings.append(
                        f"{mname} {name}: component base '{b}' does not exist")
                if b == name:
                    findings.append(f"{mname} {name}: components itself")
            for b in comps:
                if b in cmap:
                    bp = ufo / "glyphs" / cmap[b]
                    if bp.exists() and any(
                            True for _ in ET.parse(bp).getroot()
                            .iter("component")):
                        findings.append(
                            f"{mname} {name}: nested component -> '{b}' is "
                            f"itself a composite (Google Fonts rejects "
                            f"nested components)")
            cs = contours_of(root)
            for ci, pts in enumerate(cs):
                if len(pts) == 0:
                    findings.append(f"{mname} {name} c{ci}: empty contour")
                    continue
                if len(pts) < 3:
                    findings.append(
                        f"{mname} {name} c{ci}: only {len(pts)} points")
                if not any(p[2] for p in pts):
                    findings.append(
                        f"{mname} {name} c{ci}: no on-curve points")
                    continue
                for start, offs, end in segments(pts):
                    if end[2] == "curve" and len(offs) != 2:
                        findings.append(
                            f"{mname} {name} c{ci}: curve into "
                            f"({end[0]:.0f},{end[1]:.0f}) has {len(offs)} "
                            f"off-curve points, need 2")
                    if end[2] == "curve" and len(offs) == 2:
                        if start[:2] == end[:2] and offs[0][:2] == offs[1][:2]:
                            findings.append(
                                f"{mname} {name} c{ci}: zero-length curve at "
                                f"({end[0]:.0f},{end[1]:.0f})")
            shapes[mname][name] = ([len(p) for p in cs], comps)

    common = set(shapes["Regular"]) & set(shapes["Bold"])
    for name in sorted(common):
        a, b = shapes["Regular"][name], shapes["Bold"][name]
        if a[0] != b[0]:
            findings.append(
                f"{name}: point counts differ Regular {a[0]} vs Bold {b[0]}")
        if a[1] != b[1]:
            findings.append(
                f"{name}: components differ Regular {a[1]} vs Bold {b[1]}")
    only_a = set(shapes["Regular"]) - set(shapes["Bold"])
    only_b = set(shapes["Bold"]) - set(shapes["Regular"])
    for n in sorted(only_a):
        findings.append(f"{n}: present in Regular only")
    for n in sorted(only_b):
        findings.append(f"{n}: present in Bold only")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print("  " + f)
        return 1
    print("glif_lint: clean")
    return 0


if __name__ == "__main__":
    sys.exit(lint(set(sys.argv[1:]) or None))
