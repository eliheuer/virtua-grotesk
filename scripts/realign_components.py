#!/usr/bin/env python3
"""Re-place anchor-locked components against the anchors they are locked to.

A composite stores its components as fixed offsets, so alignment is baked into
the file, not re-derived when the font is built. Move a base glyph's anchor and
every composite that places it is silently wrong until something re-places it.
That is what happened to khah-ar: hah-ar was redrawn, its topDots anchor moved,
and the dot stayed where the old anchor used to be — correct anchor, wrong dot,
in the sources and so in the built font.

This is the same rule the editor applies live (`realign_component_offsets` in
runebender-web): walk the components in order, and when a component's base
carries `_x`, move it so that `_x` lands on the nearest preceding `x` offered
by a component before it. Anchors accumulate, so a second mark stacks on the
first rather than dropping back onto the letter.

Components unlocked from their anchor (`com.glyphsapp.component.alignment` of
-1, what the editor's "unlock from anchor" writes) are left exactly as they
are — that flag exists to say "I placed this by hand, do not touch it".

Anchors themselves are never edited here. Only component offsets move.

Two things it will not touch on its own, because doing so made the font worse
once already:

  * composites built out of marks (shaddaFatha-ar, hamzaaboveDammatan-ar,
    dammatan-ar and the rest). A mark's own `top` anchor is a mkmk anchor,
    sized for the next mark in a run — stacking a precomposed pair on it
    throws the two halves apart. Those pairs are placed by hand and stay
    that way.
  * moves beyond `--max-move` (64 units by default). Small disagreements are
    drift: an anchor was nudged and the composite did not follow. A large one
    means the anchor and the drawing disagree about the design, and a script
    guessing between them is how tcheh-ar's three dots ended up on top of the
    letter. Those are listed, not applied.

Name a glyph with `--glyph` to apply its move whatever the size — that is the
escape hatch for a base that really was redrawn.

Usage:
    ./.venv/bin/python scripts/realign_components.py            # report only
    ./.venv/bin/python scripts/realign_components.py --write
    ./.venv/bin/python scripts/realign_components.py --glyph khah-ar --write
    ./.venv/bin/python scripts/realign_components.py --all --write   # no limits
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

MASTERS = ("Regular", "Bold")


def fmt(value):
    """Repo style: integers stay integers."""
    return str(int(value)) if float(value).is_integer() else repr(float(value))


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def anchors_of(root):
    return [
        (a.get("name") or "", (float(a.get("x", 0)), float(a.get("y", 0))))
        for a in root.iter("anchor")
    ]


def unlocked_identifiers(root):
    """Component identifiers the file marks as unlocked from their anchor."""
    out = set()
    header = b'<?xml version="1.0" encoding="UTF-8"?><plist version="1.0">'
    for lib in root.findall("lib"):
        if not len(lib):
            continue
        data = plistlib.loads(header + ET.tostring(lib[0]) + b"</plist>")
        for identifier, entry in (data.get("public.objectLibs") or {}).items():
            alignment = entry.get("com.glyphsapp.component.alignment")
            if alignment is not None and int(alignment) < 0:
                out.add(identifier)
    return out


def realign(components, unlocked):
    """The editor's rule, in Python. `components` is a list of
    (base, (dx, dy), base anchors, identifier). Returns the corrected offsets."""
    available = []  # (name, point) in composite coordinates
    out = []
    for base, offset, base_anchors, identifier in components:
        dx, dy = offset
        if identifier not in unlocked:
            for name, (ax, ay) in base_anchors:
                if not name.startswith("_"):
                    continue
                target_name = name[1:]
                match = next(
                    (p for n, p in reversed(available) if n == target_name), None
                )
                if match is None:
                    continue
                dx += match[0] - (ax + dx)
                dy += match[1] - (ay + dy)
                break
        out.append((dx, dy))
        for name, (ax, ay) in base_anchors:
            if not name.startswith("_"):
                available.append((name, (ax + dx, ay + dy)))
    return out


def set_component_offset(text, index, dx, dy):
    """Rewrite the nth component's offsets, in the repo's own glif style."""
    matches = list(re.finditer(r"\t\t<component\b[^\n]*?/>", text))
    element = matches[index].group(0)
    rest = re.sub(r' [xy]Offset="[^"]*"', "", element)
    attrs = ""
    if round(dx):
        attrs += f' xOffset="{fmt(dx)}"'
    if round(dy):
        attrs += f' yOffset="{fmt(dy)}"'
    # offsets go after base, before identifier, the way the sources write them
    rest = rest.replace('"', '"', 1)
    parts = re.match(r'(\t\t<component base="[^"]*")(.*?)(/>)', rest)
    updated = parts.group(1) + attrs + parts.group(2) + parts.group(3)
    return text[: matches[index].start()] + updated + text[matches[index].end() :]


def is_mark(root):
    """A glyph that attaches to something else: it carries an `_x` anchor."""
    return any(name.startswith("_") for name, _ in anchors_of(root))


def main():
    write = "--write" in sys.argv
    unrestricted = "--all" in sys.argv
    only = None
    if "--glyph" in sys.argv:
        only = sys.argv[sys.argv.index("--glyph") + 1]
    max_move = 64.0
    if "--max-move" in sys.argv:
        max_move = float(sys.argv[sys.argv.index("--max-move") + 1])

    total = 0
    held = 0
    for master in MASTERS:
        ufo = pathlib.Path(f"sources/VirtuaGrotesk-{master}.ufo")
        cmap = contents(ufo)
        roots = {}
        for name, filename in cmap.items():
            roots[name] = ET.parse(ufo / "glyphs" / filename).getroot()

        for name in sorted(cmap):
            if only and name != only:
                continue
            root = roots[name]
            comps = list(root.iter("component"))
            if not comps:
                continue
            described = []
            for comp in comps:
                base = comp.get("base") or ""
                offset = (float(comp.get("xOffset", 0)), float(comp.get("yOffset", 0)))
                base_root = roots.get(base)
                described.append(
                    (
                        base,
                        offset,
                        anchors_of(base_root) if base_root is not None else [],
                        comp.get("identifier"),
                    )
                )
            wanted = realign(described, unlocked_identifiers(root))
            # A composite of marks: hand-placed, and the mkmk anchors are the
            # wrong ruler for it. See the module docstring.
            first_base = roots.get(described[0][0])
            stacked_marks = first_base is not None and is_mark(first_base)

            text = None
            for index, ((base, offset, _, _), new) in enumerate(zip(described, wanted)):
                if (round(new[0]), round(new[1])) == (
                    round(offset[0]),
                    round(offset[1]),
                ):
                    continue
                move = max(abs(new[0] - offset[0]), abs(new[1] - offset[1]))
                targeted = only == name or unrestricted
                apply = targeted or (not stacked_marks and move <= max_move)
                total += 1
                print(
                    f"{'    ' if apply else 'HELD'} {master}/{name}: {base} "
                    f"({fmt(offset[0])}, {fmt(offset[1])}) -> ({fmt(new[0])}, {fmt(new[1])})"
                    + ("" if apply else
                       f"  [{'mark stack' if stacked_marks else f'{fmt(move)}u'}]")
                )
                if not apply:
                    held += 1
                    continue
                if write:
                    if text is None:
                        text = (ufo / "glyphs" / cmap[name]).read_text()
                    text = set_component_offset(text, index, new[0], new[1])
            if write and text is not None:
                (ufo / "glyphs" / cmap[name]).write_text(text)

    action = "rewritten" if write else "to rewrite (run with --write)"
    print(f"\n{total} component{'' if total == 1 else 's'} off their anchor: "
          f"{total - held} {action}, {held} held back for a human "
          f"(mark stacks and moves over {fmt(max_move)}u)")


if __name__ == "__main__":
    sys.exit(main())
