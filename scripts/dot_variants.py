#!/usr/bin/env python3
"""Build centred-dot alternates for the initial forms, for contextual testing.

An initial beh's dot sits under the tooth, which is where it has to be when
the next letter also carries dots below — it is the position furthest from a
collision. But in a word like با the tooth is at the far right of what reads
as a single bowl, and the dot looks pushed aside.

So there are two right answers and the context decides. This makes the second
one: a `.ctr` alternate with the dot moved toward the middle of the form. The
rule that picks between them lives in features.fea and is expected to change —
the offsets here are a starting point to look at, not a conclusion.

Usage:
    ./.venv/bin/python scripts/dot_variants.py [--shift N] [--dry-run]
"""

import pathlib
import plistlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import register_glyph  # noqa: E402

MASTERS = {m: pathlib.Path(f"sources/VirtuaGrotesk-{m}.ufo")
           for m in ("Regular", "Bold")}

# Glyphs that get a centred alternate, and the mark component to move in each.
TARGETS = {
    "beh-ar.init": "dotbelow-ar",
}

# How far to move the dot toward the middle, in units. Tuned by eye against
# با; expect to change it.
DEFAULT_SHIFT = 84


def contents(ufo):
    return plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())


def variant_name(name):
    """beh-ar.init -> beh-ar.init.ctr, keeping the positional suffix intact."""
    return f"{name}.ctr"


def shift_component(text, base, shift):
    """Move one component left by `shift`, adding xOffset if it had none."""
    pattern = re.compile(r'(\t\t<component base="' + re.escape(base) + r'")([^\n]*?)(/>)')
    m = pattern.search(text)
    if not m:
        return None
    rest = m.group(2)
    current = re.search(r' xOffset="(-?[\d.]+)"', rest)
    x = float(current.group(1)) if current else 0.0
    x -= shift
    rest = re.sub(r' xOffset="-?[\d.]+"', "", rest)
    # a fresh identifier: this is a different component in a different glyph,
    # and reusing the original's would tie their lib entries together
    rest = re.sub(r' identifier="[^"]*"', "", rest)
    attrs = f' xOffset="{int(x)}"' if round(x) else ""
    return text[:m.start()] + m.group(1) + attrs + rest + m.group(3) + text[m.end():]


def main():
    dry = "--dry-run" in sys.argv
    shift = DEFAULT_SHIFT
    if "--shift" in sys.argv:
        shift = int(sys.argv[sys.argv.index("--shift") + 1])

    made, skipped = [], []
    for source, mark in TARGETS.items():
        target = variant_name(source)
        for mname, ufo in MASTERS.items():
            cmap = contents(ufo)
            if source not in cmap:
                skipped.append(f"{mname}/{source}: missing")
                continue
            text = (ufo / "glyphs" / cmap[source]).read_text()
            moved = shift_component(text, mark, shift)
            if moved is None:
                skipped.append(f"{mname}/{source}: no {mark} component")
                continue
            moved = moved.replace(f'<glyph name="{source}"', f'<glyph name="{target}"', 1)
            # an alternate is reached through a substitution, never a codepoint
            moved = re.sub(r"\t<unicode [^\n]*/>\n", "", moved)
            if dry:
                continue
            register_glyph(target)
            cmap = contents(ufo)
            (ufo / "glyphs" / cmap[target]).write_text(moved)
        made.append(f"{target} (dot moved {shift}u toward the middle)")

    verb = "would build" if dry else "built"
    print(f"{verb} {len(made)} centred alternates:")
    for m in made:
        print("   " + m)
    if skipped:
        print("skipped:")
        for s in skipped:
            print("   " + s)


if __name__ == "__main__":
    sys.exit(main())
