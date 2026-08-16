#!/usr/bin/env python3
"""Make Arabic dot placement anchor-driven instead of hand-offset.

Three passes, all of them touching only anchors, component offsets and lib
keys — never an outline, never a mark colour.

  1. MARKS   Each dot mark keeps exactly two anchors: its `_topDots` /
             `_bottomDots` attachment anchor FIRST, then one `top` / `bottom`
             anchor so harakat can still stack on it. The redundant
             `topDots` / `bottomDots` / opposite-side anchors are dropped —
             nothing consumes them, and while they sit in front of the
             underscore anchor Runebender's aligner never reaches it
             (core/src/editor.rs: it returns from the function on the first
             anchor rather than scanning them all).

  2. ANCHORS Each base glyph gets one dots-anchor per side, positioned so the
             dot lands under the VERTICAL for joining forms (.init/.medi) and
             stays exactly where it is for everything else. Vertical position
             is always preserved.

  3. SNAP    Every dot component offset is rewritten as
             base.anchor - mark._anchor, and the
             `com.glyphsapp.component.alignment = -1` flags that were pinning
             them to hand positions are removed.

Usage:
    ./.venv/bin/python scripts/arabic_dot_anchors.py [--dry-run]
"""

import pathlib
import plistlib
import re
import statistics
import sys
import xml.etree.ElementTree as ET

MASTERS = {m: pathlib.Path(f"sources/VirtuaGrotesk-{m}.ufo")
           for m in ("Regular", "Bold")}

# Ink above this y is the tooth / stem rather than the joining bar.
TOOTH_FLOOR = 200.0
# A tooth wider than this fraction of the advance is a bowl, not a stem;
# those forms keep their existing horizontal placement.
TOOTH_MAX_FRAC = 0.45
GRID = 2


def fmt(v):
    v = round(v / GRID) * GRID
    return str(int(v)) if v == int(v) else str(v)


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def path_of(ufo, cmap, name):
    return ufo / "glyphs" / cmap[name]


def root_of(ufo, cmap, name):
    return ET.parse(path_of(ufo, cmap, name)).getroot()


def anchors_of(ufo, cmap, name):
    return {a.get("name"): (float(a.get("x")), float(a.get("y")))
            for a in root_of(ufo, cmap, name).iter("anchor")}


def is_dot_mark(name, cmap):
    return (name in cmap and name.endswith("-ar") and "." not in name
            and "Dotless" not in name and ("dot" in name or "Dot" in name))


def dot_marks(ufo, cmap):
    """Mark glyphs actually used as dot components, keyed to their slot."""
    used = set()
    for n in cmap:
        for c in root_of(ufo, cmap, n).iter("component"):
            b = c.get("base")
            if is_dot_mark(b, cmap):
                used.add(b)
    out = {}
    for b in sorted(used):
        a = anchors_of(ufo, cmap, b)
        slot = next((k for k in a if k.startswith("_")), None)
        if slot:
            out[b] = slot
    return out


def ink(ufo, cmap, name, ymin=None):
    xs = [float(p.get("x")) for p in root_of(ufo, cmap, name).iter("point")
          if ymin is None or float(p.get("y")) > ymin]
    return (min(xs), max(xs)) if xs else None


def advance(ufo, cmap, name):
    a = root_of(ufo, cmap, name).find("advance")
    return float(a.get("width")) if a is not None else 0.0


# --------------------------------------------------------------------------
# surgical glif rewriting (repo style: tabs, double quotes, no space before />)
# --------------------------------------------------------------------------

ANCHOR_RE = re.compile(r"^\t<anchor [^\n]*/>\n", re.M)


def write_anchors(text, anchors):
    """Replace the glif's anchor block with `anchors` (list of (name,x,y))."""
    lines = "".join(f'\t<anchor name="{n}" x="{fmt(x)}" y="{fmt(y)}"/>\n'
                    for n, x, y in anchors)
    if ANCHOR_RE.search(text):
        first = ANCHOR_RE.search(text).start()
        text = ANCHOR_RE.sub("", text)
        return text[:first] + lines + text[first:]
    # no anchors yet: insert after </outline>
    return text.replace("\t</outline>\n", "\t</outline>\n" + lines, 1)


def upsert_anchor(text, name, x, y):
    """Set one anchor in place, preserving the file's existing anchor order.

    Base glyphs are mostly green; rewriting their whole anchor block just to
    move one anchor produces noise diffs for no benefit.
    """
    line = f'\t<anchor name="{name}" x="{fmt(x)}" y="{fmt(y)}"/>\n'
    pat = re.compile(r'^\t<anchor name="' + re.escape(name) + r'"[^\n]*/>\n', re.M)
    if pat.search(text):
        return pat.sub(lambda _: line, text, count=1)
    m = list(ANCHOR_RE.finditer(text))
    if m:
        return text[:m[-1].end()] + line + text[m[-1].end():]
    return text.replace("\t</outline>\n", "\t</outline>\n" + line, 1)


def set_component_offset(text, base, dx, dy):
    """Rewrite xOffset/yOffset on the <component base="..."/> line."""
    pat = re.compile(r'(\t\t<component base="' + re.escape(base) + r'")([^\n]*?)(/>)')
    m = pat.search(text)
    if not m:
        return text, False
    rest = m.group(2)
    ident = re.search(r' identifier="[^"]*"', rest)
    attrs = ""
    if round(dx):
        attrs += f' xOffset="{fmt(dx)}"'
    if round(dy):
        attrs += f' yOffset="{fmt(dy)}"'
    if ident:
        attrs += ident.group(0)
    new = m.group(1) + attrs + m.group(3)
    return text[:m.start()] + new + text[m.end():], (new != m.group(0))


OBJLIB_RE = re.compile(
    r"\t\t\t<key>public\.objectLibs</key>\n\t\t\t<dict>\n(.*?)\n\t\t\t</dict>\n",
    re.S)
ENTRY_RE = re.compile(
    r"\t\t\t\t<key>([^<]+)</key>\n\t\t\t\t<dict>\n.*?\n\t\t\t\t</dict>\n?", re.S)


def is_unpinned(text, base):
    """Whether `base`'s component here has been unlocked from its anchor."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(text)
    ident = next((c.get("identifier") for c in root.iter("component")
                  if c.get("base") == base and c.get("identifier")), None)
    if not ident:
        return False
    m = OBJLIB_RE.search(text)
    if not m:
        return False
    for entry in ENTRY_RE.finditer(m.group(1) + "\n"):
        if entry.group(1) == ident and "alignment" in entry.group(0):
            return True
    return False


def unpin(text, identifiers):
    """Remove alignment pins for `identifiers` only.

    Other components' pins are deliberate (hamza placement, quoteright) and
    must survive; the block itself goes only once it is empty.
    """
    m = OBJLIB_RE.search(text)
    if not m or not identifiers:
        return text, False
    kept = [e.group(0) for e in ENTRY_RE.finditer(m.group(1) + "\n")
            if e.group(1) not in identifiers]
    if len(kept) == len(list(ENTRY_RE.finditer(m.group(1) + "\n"))):
        return text, False
    if kept:
        body = "".join(kept).rstrip("\n")
        new = (f"\t\t\t<key>public.objectLibs</key>\n\t\t\t<dict>\n"
               f"{body}\n\t\t\t</dict>\n")
    else:
        new = ""
    return text[:m.start()] + new + text[m.end():], True


# --------------------------------------------------------------------------


def main():
    dry = "--dry-run" in sys.argv
    report = {"marks": [], "moved": [], "kept": [], "snapped": 0,
              "unpinned": [], "skipped": [], "outliers": [], "left_unlocked": []}

    for mname, ufo in MASTERS.items():
        cmap = contents(ufo)
        marks = dot_marks(ufo, cmap)

        # ---- pass 1: trim each mark to [_slot, stacking anchor] -----------
        for mark, slot in marks.items():
            a = anchors_of(ufo, cmap, mark)
            side = "top" if slot.endswith("topDots") else "bottom"
            keep = [(slot, *a[slot])]
            if side in a:
                keep.append((side, *a[side]))
            text = path_of(ufo, cmap, mark).read_text()
            new = write_anchors(text, keep)
            if new != text:
                report["marks"].append(f"{mname}/{mark}")
                if not dry:
                    path_of(ufo, cmap, mark).write_text(new)

        # ---- gather consumers: base glyph + slot -> [(composite, mark)] ---
        consumers = {}
        for n in sorted(cmap):
            r = root_of(ufo, cmap, n)
            comps = list(r.iter("component"))
            dots = [c for c in comps if c.get("base") in marks]
            if not dots:
                continue
            body = next((c.get("base") for c in comps
                         if c.get("base") not in marks), None)
            if body is None:
                # The letter's own tooth is drawn in this glyph (teh-ar.init,
                # tteh-ar.init): the glyph is its own base, so the dots-anchor
                # belongs on it.
                if list(r.iter("contour")):
                    body = n
                else:
                    report["skipped"].append(f"{mname}/{n}: no body outline")
                    continue
            if body not in cmap:
                report["skipped"].append(f"{mname}/{n}: base {body} missing")
                continue
            for c in dots:
                mark = c.get("base")
                slot = marks[mark].lstrip("_")
                consumers.setdefault((body, slot), []).append(
                    (n, mark, float(c.get("xOffset") or 0),
                     float(c.get("yOffset") or 0)))

        # ---- pass 2: position each base's dots-anchor ---------------------
        targets = {}
        for (body, slot), uses in sorted(consumers.items()):
            # One anchor serves every consumer of this base, so a malformed
            # composite (wrong advance, stale offset) must not drag the
            # anchor off. Only consumers whose dots actually sit over the
            # base get a vote.
            badv = advance(ufo, cmap, body)
            implied, trusted = [], []
            for comp, mark, dx, dy in uses:
                mx, my = anchors_of(ufo, cmap, mark)[f"_{slot}"]
                implied.append((dx + mx, dy + my))
                span = ink(ufo, cmap, mark)
                centre = (span[0] + span[1]) / 2 + dx if span else None
                if centre is not None and 0 <= centre <= badv:
                    trusted.append((dx + mx, dy + my))
                else:
                    report["outliers"].append(
                        f"{mname}/{comp}: dots centre off the base, ignored "
                        f"when placing {body}:{slot}")
            vote = trusted or implied
            ty = statistics.median(p[1] for p in vote)
            cur_x = statistics.median(p[0] for p in vote)

            tooth = ink(ufo, cmap, body, TOOTH_FLOOR)
            adv = advance(ufo, cmap, body)
            joining = body.endswith((".init", ".medi"))
            if joining and tooth and adv and \
                    (tooth[1] - tooth[0]) <= TOOTH_MAX_FRAC * adv:
                tx = (tooth[0] + tooth[1]) / 2
                if abs(tx - cur_x) > GRID:
                    report["moved"].append(
                        (mname, body, slot, round(cur_x), round(tx)))
            else:
                tx = cur_x
                if joining:
                    report["kept"].append(f"{mname}/{body}:{slot} (bowl, not a stem)")
            targets[(body, slot)] = (tx, ty)

            text = path_of(ufo, cmap, body).read_text()
            new = upsert_anchor(text, slot, tx, ty)
            if new != text and not dry:
                path_of(ufo, cmap, body).write_text(new)

        # ---- pass 3: snap offsets, drop the alignment pins ----------------
        for (body, slot), uses in sorted(consumers.items()):
            bx, by = targets[(body, slot)]
            for comp, mark, _, _ in uses:
                mx, my = anchors_of(ufo, cmap, mark)[f"_{slot}"]
                p = path_of(ufo, cmap, comp)
                text = p.read_text()
                r = ET.fromstring(text)
                # A component unlocked on purpose stays where it was put.
                # This was written as a one-off migration, when every pin in
                # the font was stale; now the centred alternates are pinned
                # deliberately, and re-running it used to snap their dots back
                # onto the anchor — silently undoing the reason they exist.
                if is_unpinned(text, mark):
                    report["left_unlocked"].append(f"{mname}/{comp}")
                    continue
                pinned = {c.get("identifier") for c in r.iter("component")
                          if c.get("base") in marks and c.get("identifier")}
                text, changed = set_component_offset(text, mark, bx - mx, by - my)
                text, unpinned = unpin(text, pinned)
                if unpinned:
                    report["unpinned"].append(f"{mname}/{comp}")
                if changed:
                    report["snapped"] += 1
                if not dry:
                    p.write_text(text)

    verb = "would change" if dry else "changed"
    print(f"marks trimmed to two anchors: {len(report['marks'])} ({verb})")
    print(f"dot components re-snapped to anchors: {report['snapped']}")
    print(f"alignment pins removed: {len(set(report['unpinned']))}")
    print(f"\nanchors moved onto the vertical ({len(report['moved'])}):")
    for m, body, slot, a, b in report["moved"]:
        print(f"   {m:8s} {body:26s} {slot:11s} x {a:5d} -> {b:5d}")
    if report["kept"]:
        print(f"\njoining forms left alone ({len(report['kept'])}):")
        for k in report["kept"][:12]:
            print("   " + k)
    if report["left_unlocked"]:
        n = len(set(report["left_unlocked"]))
        print(f"\nleft alone, unlocked from their anchor ({n}):")
        for u in sorted(set(report["left_unlocked"]))[:10]:
            print("   " + u)
    if report["outliers"]:
        n_out = len(set(report["outliers"]))
        print(f"\ncomposites ignored when placing an anchor ({n_out}):")
        for o in sorted(set(report["outliers"]))[:10]:
            print("   " + o)
    if report["skipped"]:
        print(f"\nskipped ({len(report['skipped'])}):")
        for s in report["skipped"][:8]:
            print("   " + s)


if __name__ == "__main__":
    sys.exit(main())
