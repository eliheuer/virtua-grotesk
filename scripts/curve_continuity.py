#!/usr/bin/env python3
"""Continuity checker — Runebender web's G0-G3 overlay as a CLI gate.

Classifies every on-curve joint in a glyph:
  corner       not smooth-marked, tangents disagree (fine, by design)
  line<->curve smooth line-curve joint, tangents collinear (G1; curvature
               cannot match a straight line, so G1 is the ceiling here)
  G1           smooth curve joint, tangents collinear but curvatures differ
  G2           smooth curve joint, tangents collinear AND endpoint
               curvatures match within tolerance
  KINK         smooth-marked joint whose tangents disagree — always a bug

House targets (LESSONS.md): every smooth curve-curve joint should be G2;
line->curve transitions must be tangent; no KINKs ever.

    ./.venv/bin/python scripts/curve_continuity.py Regular asciitilde braceleft
    ./.venv/bin/python scripts/curve_continuity.py Bold --all-smooth-glyphs
"""
import math, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
KINK_DEG = 2.0          # tangent mismatch tolerance
G2_REL = 0.25           # relative curvature mismatch tolerance for G2


def parse(path):
    txt = pathlib.Path(path).read_text()
    contours = []
    for cm in re.finditer(r"<contour>(.*?)</contour>", txt, re.S):
        pts = []
        for pm in re.finditer(
                r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"(?: type="(\w+)")?( smooth="yes")?', cm.group(1)):
            pts.append((float(pm.group(1)), float(pm.group(2)), pm.group(3), bool(pm.group(4))))
        contours.append(pts)
    return contours


def seginfo(pts, i):
    """For on-curve index i return (in_tangent, out_tangent, kappa_in, kappa_out,
    in_is_curve, out_is_curve). Tangents point along travel direction."""
    n = len(pts)

    def prev_on(j):
        k = (j - 1) % n
        while pts[k][2] is None:
            k = (k - 1) % n
        return k

    def next_on(j):
        k = (j + 1) % n
        while pts[k][2] is None:
            k = (k + 1) % n
        return k

    P = pts[i][:2]
    # incoming segment: from prev oncurve to P
    j = prev_on(i)
    offs_in = []
    k = (j + 1) % n
    while k != i:
        offs_in.append(pts[k][:2]); k = (k + 1) % n
    if offs_in:
        c1, c2 = offs_in[-1], (offs_in[-2] if len(offs_in) > 1 else pts[j][:2])
        t_in = (P[0] - c1[0], P[1] - c1[1])
        l = math.hypot(*t_in)
        # curvature at end of cubic: (2/3) * dist(c2, tangent line) / l^2
        if l > 0:
            ux, uy = t_in[0] / l, t_in[1] / l
            d = abs((c2[0] - P[0]) * uy - (c2[1] - P[1]) * ux)
            k_in = (2.0 / 3.0) * d / (l * l)
        else:
            k_in = None
        in_curve = True
    else:
        t_in = (P[0] - pts[j][0], P[1] - pts[j][1])
        k_in, in_curve = 0.0, False
    # outgoing segment: from P to next oncurve
    j2 = next_on(i)
    offs_out = []
    k = (i + 1) % n
    while k != j2:
        offs_out.append(pts[k][:2]); k = (k + 1) % n
    if offs_out:
        c1, c2 = offs_out[0], (offs_out[1] if len(offs_out) > 1 else pts[j2][:2])
        t_out = (c1[0] - P[0], c1[1] - P[1])
        l = math.hypot(*t_out)
        if l > 0:
            ux, uy = t_out[0] / l, t_out[1] / l
            d = abs((c2[0] - P[0]) * uy - (c2[1] - P[1]) * ux)
            k_out = (2.0 / 3.0) * d / (l * l)
        else:
            k_out = None
        out_curve = True
    else:
        t_out = (pts[j2][0] - P[0], pts[j2][1] - P[1])
        k_out, out_curve = 0.0, False
    return t_in, t_out, k_in, k_out, in_curve, out_curve


def classify(path):
    findings = []
    for ci, pts in enumerate(parse(path)):
        onc = [i for i, p in enumerate(pts) if p[2] is not None]
        if len(onc) < 2:
            continue
        for i in onc:
            x, y, typ, smooth = pts[i]
            t_in, t_out, k_in, k_out, inc, outc = seginfo(pts, i)
            a_in = math.atan2(t_in[1], t_in[0])
            a_out = math.atan2(t_out[1], t_out[0])
            dev = abs(math.degrees((a_out - a_in + math.pi) % (2 * math.pi) - math.pi))
            tangent = dev <= KINK_DEG
            if not (inc or outc):
                continue  # line-line corners: not our department
            if smooth and not tangent:
                cls = "KINK"
            elif not smooth and not tangent:
                cls = "corner"
            elif inc != outc:
                cls = "line<->curve" if tangent else "KINK(line-curve)"
            else:
                if k_in is None or k_out is None:
                    cls = "G1"
                else:
                    hi, lo = max(k_in, k_out), min(k_in, k_out)
                    cls = "G2" if hi == 0 or (hi - lo) / hi <= G2_REL else "G1"
            findings.append((ci, (x, y), cls, round(dev, 1),
                             None if k_in is None else round(k_in, 5),
                             None if k_out is None else round(k_out, 5), smooth))
    return findings


def main():
    master, glyphs = sys.argv[1], sys.argv[2:]
    bad = 0
    for g in glyphs:
        import plistlib
        ufo = REPO / f"sources/VirtuaGrotesk-{master}.ufo"
        contents = plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())
        fn = contents.get(g, f"{g}_.glif" if g[0].isupper() else f"{g}.glif")
        path = ufo / "glyphs" / fn
        print(f"== {master} {g} ==")
        for ci, (x, y), cls, dev, ki, ko, smooth in classify(path):
            flag = ""
            if cls.startswith("KINK"):
                flag = "  <-- FIX"; bad += 1
            elif cls == "G1" and smooth:
                flag = "  <-- want G2"; bad += 1
            print(f"  c{ci} ({x:.0f},{y:.0f})  {cls:14s} dev {dev:5.1f}°  κin {ki}  κout {ko}{flag}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
