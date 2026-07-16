"""Snap graded (axis-aligned) handle lengths to short power-of-two sums.

Mirrors scripts/grid_qa.py's handle-grading logic exactly: an off-curve
point is graded against its adjacent on-curve neighbor (i-1 first, then
i+1); if axis-aligned, its length along that axis is the graded value.

For each graded length L:
  pop(L) >= 3  -> nearest even value with popcount <= 2 within
                  cap2 = max(4, 5% of L)
  pop(L) >= 4 and no pop<=2 candidate in cap ->
                  nearest even popcount-3 value within cap3 = 4
Only the handle's along-axis coordinate moves; the cross-axis coordinate
(which makes it axis-aligned) is untouched. On-curve points never move.

Usage: nice_handles.py [--apply] [glyph names...]
"""
import os
import plistlib
import re
import sys

LATIN = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine"]
DEFAULT_SET = LATIN + DIGITS

POINT_RE = re.compile(
    r'<point x="(-?[\d.]+)" y="(-?[\d.]+)"'
    r'((?: type="(\w+)")?( smooth="yes")?)/>')


def pop(v):
    return bin(int(abs(v))).count("1") if v else 0


P2 = [v for v in range(8, 1025, 2) if pop(v) <= 2]
P3 = [v for v in range(8, 1025, 2) if pop(v) == 3]


LOOSE = "--loose" in sys.argv


def snap(L):
    """Return new length or None."""
    Li = int(round(L))
    if pop(Li) <= 2:
        return None
    cap2 = max(6, round(0.07 * Li)) if LOOSE else max(4, round(0.05 * Li))
    c2 = min(P2, key=lambda v: (abs(v - Li), v))
    if abs(c2 - Li) <= cap2:
        return c2
    if pop(Li) >= 4:
        cap3 = max(6, round(0.04 * Li)) if LOOSE else 4
        c3 = min(P3, key=lambda v: (abs(v - Li), v))
        if abs(c3 - Li) <= cap3:
            return c3
    return None


def process(path, apply_):
    src = open(path).read()
    # parse contours with global point index in document order
    pts = []   # (x, y, on)
    for m in re.finditer(r"<contour>(.*?)</contour>", src, re.S):
        cpts = []
        for pm in POINT_RE.finditer(m.group(1)):
            cpts.append(dict(x=float(pm.group(1)), y=float(pm.group(2)),
                             on=bool(pm.group(4))))
        pts.append(cpts)
    edits = {}  # global point index -> (newx, newy)
    changes = []
    gidx = 0
    for cont in pts:
        n = len(cont)
        for i, p in enumerate(cont):
            if not p["on"]:
                for j in (i - 1, i + 1):
                    q = cont[j % n]
                    if q["on"]:
                        dx, dy = p["x"] - q["x"], p["y"] - q["y"]
                        if abs(dx) > 0.01 and abs(dy) > 0.01:
                            pass  # diagonal: not graded
                        else:
                            axis = "x" if abs(dx) > 0.01 else "y"
                            L = abs(dx) if axis == "x" else abs(dy)
                            if L > 0.01:
                                new = snap(L)
                                if new is not None:
                                    sign = 1 if (dx if axis == "x" else dy) > 0 else -1
                                    nx, ny = p["x"], p["y"]
                                    if axis == "x":
                                        nx = q["x"] + sign * new
                                    else:
                                        ny = q["y"] + sign * new
                                    edits[gidx + i] = (nx, ny)
                                    changes.append((int(L), new))
                        break
        gidx += n
    if not changes:
        return []
    if apply_:
        out, k = [], 0
        for line in src.splitlines(keepends=True):
            m = POINT_RE.search(line)
            if m:
                if k in edits:
                    nx, ny = edits[k]
                    line = line.replace(f'x="{m.group(1)}"', f'x="{nx:g}"', 1)
                    line = line.replace(f'y="{m.group(2)}"', f'y="{ny:g}"', 1)
                k += 1
            out.append(line)
        open(path, "w").write("".join(out))
    return changes


def main():
    apply_ = "--apply" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or DEFAULT_SET
    total = 0
    for master in ["Regular", "Bold"]:
        gdir = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
        contents = plistlib.load(open(f"{gdir}/contents.plist", "rb"))
        for name in names:
            fn = contents.get(name)
            if fn is None:
                continue
            ch = process(os.path.join(gdir, fn), apply_)
            if ch:
                total += len(ch)
                desc = ", ".join(f"{a}->{b}" for a, b in ch)
                print(f"{master:<8} {name:<10} {desc}")
    print(f"\n{total} handle lengths {'changed' if apply_ else 'to change'}")


if __name__ == "__main__":
    main()
