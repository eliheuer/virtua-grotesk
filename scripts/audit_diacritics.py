#!/usr/bin/env python3
"""Audit every accent composite for PLACEMENT problems (deterministic):
 - base or mark missing the anchor it needs
 - composite offset that doesn't match the anchor-derived value (stale/unrebuilt)
 - multi-component composites (stacked/Vietnamese) that need special handling
 - marks with no known attach type
Placement only -- mark DRAWING quality (flat tilde etc.) is a separate design pass.
Usage: python scripts/audit_diacritics.py [Regular|Bold]
"""
import re, glob, os, sys

MASTER = sys.argv[1] if len(sys.argv) > 1 else "Regular"
G = f"sources/VirtuaGrotesk-{MASTER}.ufo/glyphs"
TOP = {"acute","grave","circumflex","dieresis","tilde","macron","caron","breve",
       "ring","hungarumlaut","dotaccent","caroncomb.alt"}
BELOW = {"cedilla","commaaccent"}
CORNER = {"ogonek"}   # attach at a base corner, not center -- own sub-scheme

# glyph name -> file text map (Glyphs escapes uppercase as X_.glif, and the
# macOS case-insensitive FS makes name+".glif" resolve to the wrong case, so
# never look up by guessed filename -- map by the actual <glyph name=>).
_NAME2TEXT = {}
for _p in glob.glob(f"{G}/*.glif"):
    _t = open(_p).read()
    _m = re.search(r'<glyph name="([^"]+)"', _t)
    if _m:
        _NAME2TEXT[_m.group(1)] = _t
def read(n):
    return _NAME2TEXT.get(n)
def anchor(t, name):
    if not t: return None
    m = re.search(rf'<anchor name="{re.escape(name)}" x="(-?\d+)"', t)
    return int(m.group(1)) if m else None

problems = {"unanchored_base": [], "unanchored_mark": [], "stale_offset": [],
            "multi_component": [], "unknown_mark": [], "ogonek": []}

for p in sorted(glob.glob(f"{G}/*.glif")):
    t = open(p).read()
    gname = re.search(r'<glyph name="([^"]+)"', t).group(1)
    comps = re.findall(r'<component base="([^"]+)"([^/]*)/>', t)
    if not comps:
        continue
    if len(comps) != 2:
        if any(m in TOP | BELOW | CORNER for _, m in [(c[0], c[0]) for c in comps]) or len(comps) > 2:
            problems["multi_component"].append(f"{gname} ({[c[0] for c in comps]})")
        continue
    (base, _), (mark, ma) = comps
    if mark in CORNER:
        problems["ogonek"].append(gname); continue
    if mark not in TOP | BELOW:
        continue  # not a diacritic composite (ligature etc.)
    bt, mt = read(base), read(mark)
    aname, mname = ("top", "_top") if mark in TOP else ("bottom", "_bottom")
    bx, mx = anchor(bt, aname), anchor(mt, mname)
    if bx is None:
        problems["unanchored_base"].append(f"{gname} (base {base})"); continue
    if mx is None:
        problems["unanchored_mark"].append(f"{gname} (mark {mark})"); continue
    actual = int(re.search(r'xOffset="(-?\d+)"', ma).group(1)) if 'xOffset' in ma else 0
    if actual != bx - mx:
        problems["stale_offset"].append(f"{gname}: {actual} != anchor {bx-mx}")

print(f"=== {MASTER} diacritic placement audit ===")
total = 0
for k, v in problems.items():
    if v:
        total += len(v)
        print(f"\n{k} ({len(v)}):")
        for x in v[:30]:
            print(f"   {x}")
print(f"\nTOTAL placement problems: {total}")
