"""Compensated-pair handle tuning: fix popcount>=3 handle lengths by
redistributing length between the two handles of one cubic segment
(lengthen one, shorten the other by ~the same amount), per Eli's rules:
form is roughly preserved, and segment handles should stay/get more even.

Constraints per segment (handles L1, L2 -> L1', L2'):
  pop(L1') <= 2 and pop(L2') <= 2, both even, both >= 8
  |net change| = |(L1'+L2') - (L1+L2)| <= 4
  per-handle move <= 20
  evenness: |L1'-L2'| <= |L1-L2| + 8   (prefer improving)
Only fires when the segment has a popcount>=3 handle. --audit lists
uneven pairs (ratio > 2.2) without editing.
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


P2set = set(v for v in range(8, 1025, 2) if pop(v) <= 2)


def axis_len(p, q):
    """(axis, length, sign) of handle p anchored at on-curve q, or None."""
    dx, dy = p["x"] - q["x"], p["y"] - q["y"]
    if abs(dx) > 0.01 and abs(dy) > 0.01:
        return None
    if abs(dx) > 0.01:
        return ("x", abs(dx), 1 if dx > 0 else -1)
    if abs(dy) > 0.01:
        return ("y", abs(dy), 1 if dy > 0 else -1)
    return None


def best_pair(L1, L2):
    tot, uneven = L1 + L2, abs(L1 - L2)
    cands = []
    for a in range(max(8, int(L1) - 20), int(L1) + 21, 2):
        if a not in P2set:
            continue
        for net in (0, -2, 2, -4, 4):
            b = int(tot) + net - a
            if b < 8 or b not in P2set or abs(b - L2) > 20:
                continue
            if abs(a - b) > uneven + 8:
                continue
            cands.append((max(abs(a - L1), abs(b - L2)), abs(a - b), a, b))
    if not cands:
        return None
    cands.sort()
    return cands[0][2], cands[0][3]


def process(path, apply_, audit):
    src = open(path).read()
    conts = []
    for m in re.finditer(r"<contour>(.*?)</contour>", src, re.S):
        cpts = [dict(x=float(pm.group(1)), y=float(pm.group(2)),
                     on=bool(pm.group(4)))
                for pm in POINT_RE.finditer(m.group(1))]
        conts.append(cpts)
    edits = {}
    notes = []
    gidx = 0
    for cont in conts:
        n = len(cont)
        for i in range(n):
            p0, p1, p2, p3 = (cont[i], cont[(i + 1) % n],
                              cont[(i + 2) % n], cont[(i + 3) % n])
            if not (p0["on"] and not p1["on"] and not p2["on"] and p3["on"]):
                continue
            a1, a2 = axis_len(p1, p0), axis_len(p2, p3)
            if a1 is None or a2 is None:
                continue
            L1, L2 = a1[1], a2[1]
            if audit and min(L1, L2) > 0 and max(L1, L2) / min(L1, L2) > 2.2:
                notes.append(f"uneven pair {int(L1)}/{int(L2)}")
                continue
            if pop(int(round(L1))) <= 2 and pop(int(round(L2))) <= 2:
                continue
            got = best_pair(int(round(L1)), int(round(L2)))
            if got is None:
                continue
            n1, n2 = got
            if (n1, n2) == (int(L1), int(L2)):
                continue
            e1 = dict(p1)
            e2 = dict(p2)
            if a1[0] == "x":
                e1["x"] = p0["x"] + a1[2] * n1
            else:
                e1["y"] = p0["y"] + a1[2] * n1
            if a2[0] == "x":
                e2["x"] = p3["x"] + a2[2] * n2
            else:
                e2["y"] = p3["y"] + a2[2] * n2
            edits[gidx + (i + 1) % n] = (e1["x"], e1["y"])
            edits[gidx + (i + 2) % n] = (e2["x"], e2["y"])
            notes.append(f"{int(L1)}/{int(L2)} -> {n1}/{n2}")
        gidx += n
    if apply_ and edits:
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
    return notes


def main():
    apply_ = "--apply" in sys.argv
    audit = "--audit" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or DEFAULT_SET
    for master in ["Regular", "Bold"]:
        gdir = f"sources/VirtuaGrotesk-{master}.ufo/glyphs"
        contents = plistlib.load(open(f"{gdir}/contents.plist", "rb"))
        for name in names:
            fn = contents.get(name)
            if fn is None:
                continue
            notes = process(os.path.join(gdir, fn), apply_, audit)
            if notes:
                print(f"{master:<8} {name:<10} {'; '.join(notes)}")


if __name__ == "__main__":
    main()
