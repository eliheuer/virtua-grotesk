#!/usr/bin/env python3
"""Stop storing an anchor twice: let composites inherit from their components.

Every Arabic composite here carried its own copy of the `top`/`bottom` anchors
that already exist on the component it is built from. Two copies of one number
drift apart — `beh-ar` and `behDotless-ar` had, and `beeh-ar` was still holding
a `top` at (832, 288) long after its component moved to (472, 420). The copies
also clutter the composite view, which is the first thing you notice coming
from Glyphs, where composites show no anchors at all.

Glyphs does not store them either: glyphsLib copies anchors up from components
at export (`glyphsLib/builder/anchor_propagation.py`). ufo2ft ships the same
filter, `propagateAnchors`, but it is opt-in. Turn it on and the copies can go.

Ligatures keep their anchors. Propagation has no single component to inherit
from when both halves are bases, so stripping lam-alef drops its harakat
attachment entirely — verified against the compiled GPOS, not assumed.

Usage:
    ./.venv/bin/python scripts/propagate_anchors.py [--dry-run]
"""

import pathlib
import plistlib
import re
import sys
import xml.etree.ElementTree as ET

MASTERS = {m: pathlib.Path(f"sources/VirtuaGrotesk-{m}.ufo")
           for m in ("Regular", "Bold")}
FILTER_KEY = "com.github.googlei18n.ufo2ft.filters"
ANCHOR_RE = re.compile(r"^\t<anchor [^\n]*/>\n", re.M)


def keeps_own_anchors(name):
    """Ligatures: two bases, so there is nothing to inherit from."""
    return "_" in name.split(".")[0]


def main():
    dry = "--dry-run" in sys.argv
    enabled, stripped, kept = [], [], []

    for mname, ufo in MASTERS.items():
        lp = ufo / "lib.plist"
        text = lp.read_text()
        if FILTER_KEY not in text:
            block = (f"\t<key>{FILTER_KEY}</key>\n\t<array>\n\t\t<dict>\n"
                     "\t\t\t<key>name</key>\n"
                     "\t\t\t<string>propagateAnchors</string>\n"
                     "\t\t\t<key>pre</key>\n\t\t\t<true/>\n"
                     "\t\t</dict>\n\t</array>\n")
            if not dry:
                lp.write_text(text.replace("</dict>\n</plist>",
                                           block + "</dict>\n</plist>", 1))
            enabled.append(mname)

        cmap = plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())
        for name in sorted(cmap):
            path = ufo / "glyphs" / cmap[name]
            root = ET.parse(path).getroot()
            # only pure composites: a glyph with its own outline is its own base
            if not list(root.iter("component")) or list(root.iter("contour")):
                continue
            # marks stay put; their `_anchor` is what everything else attaches to
            if any(a.get("name", "").startswith("_")
                   for a in root.iter("anchor")):
                continue
            if not list(root.iter("anchor")):
                continue
            if keeps_own_anchors(name):
                kept.append(f"{mname}/{name}")
                continue
            if not dry:
                path.write_text(ANCHOR_RE.sub("", path.read_text()))
            stripped.append(f"{mname}/{name}")

    verb = "would strip" if dry else "stripped"
    print(f"propagateAnchors filter: "
          f"{'enabled in ' + ', '.join(enabled) if enabled else 'already on'}")
    print(f"{verb} duplicate anchors from {len(stripped)} composites")
    print(f"kept {len(kept)} ligatures, which cannot inherit: "
          f"{', '.join(sorted({k.split('/')[1] for k in kept}))}")


if __name__ == "__main__":
    sys.exit(main())
