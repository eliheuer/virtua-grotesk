#!/usr/bin/env python3
"""Rebuild the lam-alef variants on top of the drawn lam-alef.

lam_alef-ar is drawn: the two strokes cross. The five hamza/madda/wasla
variants were not built from it — each one stacked lam-ar.init and
alef-ar.fina side by side and added the mark, so ل + أ came out as a U with
a hamza on it and nothing in the word looked like the ligature the plain
form shows.

This makes each variant what it should have been: the ligature it is a
variant of, placed as one component, plus the mark. The isolated forms sit
on lam_alef-ar, the final forms on lam_alef-ar.fina, so a variant can never
again drift away from the shape it is a variant of.

Mark placement follows SF Arabic and Geeza Pro: on the crossed form the
hamza and madda go over the right-hand arm and the hamza below sits under
the left corner; on the final form they go on the alef, at the same offsets
the standalone alefHamzaabove-ar.fina and friends already use.

The mark component is written unlocked (alignment = -1) because it is not on
the ligature's own top/bottom anchor and a realign would drag it there.

Usage:
    ./.venv/bin/python scripts/lam_alef_variants.py [--dry-run]
"""

import pathlib
import plistlib
import sys

MASTERS = ("Regular", "Bold")

# advance of each base, per master
BASE_ADVANCE = {
    "lam_alef-ar": {"Regular": 496, "Bold": 584},
    "lam_alef-ar.fina": {"Regular": 672, "Bold": 672},
}

# What to draw for each base. lam_alef-ar is drawn, so one component does it.
# lam_alef-ar.fina is itself a composite, and a component pointing at a
# composite is a nested component — which Google Fonts' QA fails outright
# (`nested_components`). So the final forms repeat its two components instead
# of pointing at it. If lam_alef-ar.fina is ever redrawn, this list has to
# follow it.
BASE_COMPONENTS = {
    "lam_alef-ar": [("lam_alef-ar", 0, 0)],
    "lam_alef-ar.fina": [("lam-ar.medi", 256, 0), ("alef-ar.fina", 0, 0)],
}

# glyph -> base, mark, {master: (xOffset, yOffset, top anchor, bottom anchor)}
PLAN = {
    "lam_alefHamzaabove-ar": ("lam_alef-ar", "hamzaabove-ar", {
        "Regular": (276, 0, (388, 1072), (252, 0)),
        "Bold": (288, 0, (400, 1100), (272, 0)),
    }),
    "lam_alefHamzabelow-ar": ("lam_alef-ar", "hamzabelow-ar", {
        "Regular": (-4, 0, (264, 768), (108, -304)),
        "Bold": (0, 0, (272, 768), (112, -318)),
    }),
    "lam_alefMadda-ar": ("lam_alef-ar", "madda-ar", {
        "Regular": (244, 168, (388, 992), (252, 0)),
        "Bold": (256, 196, (400, 1048), (272, 0)),
    }),
    "lam_alefWasla-ar": ("lam_alef-ar", "wasla-ar", {
        "Regular": (276, 208, (388, 1104), (252, 0)),
        "Bold": (288, 218, (400, 1142), (272, 0)),
    }),
    "lam_alefHamzaabove-ar.fina": ("lam_alef-ar.fina", "hamzaabove-ar", {
        "Regular": (0, 0, (112, 1072), (208, 0)),
        "Bold": (0, 0, (112, 1100), (226, -24)),
    }),
    "lam_alefHamzabelow-ar.fina": ("lam_alef-ar.fina", "hamzabelow-ar", {
        "Regular": (48, 0, (208, 768), (160, -304)),
        "Bold": (48, 0, (226, 768), (160, -318)),
    }),
    "lam_alefMadda-ar.fina": ("lam_alef-ar.fina", "madda-ar", {
        "Regular": (-32, 168, (112, 992), (208, 0)),
        "Bold": (-32, 196, (112, 1048), (226, -24)),
    }),
    "lam_alefWasla-ar.fina": ("lam_alef-ar.fina", "wasla-ar", {
        "Regular": (0, 208, (112, 1104), (208, 0)),
        "Bold": (0, 218, (112, 1142), (226, -24)),
    }),
}

BLUE = "0,0.67,0.91,1"


def offsets(x, y):
    out = ""
    if x:
        out += f' xOffset="{x}"'
    if y:
        out += f' yOffset="{y}"'
    return out


def build(name, master):
    base, mark, per_master = PLAN[name]
    x, y, top, bottom = per_master[master]
    advance = BASE_ADVANCE[base][master]
    ident = f"la{abs(hash((master, name))) % 10**10:010d}"
    drawn = "".join(
        f'\t\t<component base="{part}"{offsets(px, py)}/>\n'
        for part, px, py in BASE_COMPONENTS[base]
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<glyph name="{name}" format="2">\n'
        f'\t<advance width="{advance}"/>\n'
        "\t<outline>\n"
        f"{drawn}"
        f'\t\t<component base="{mark}"{offsets(x, y)} identifier="{ident}"/>\n'
        "\t</outline>\n"
        f'\t<anchor name="top" x="{top[0]}" y="{top[1]}"/>\n'
        f'\t<anchor name="bottom" x="{bottom[0]}" y="{bottom[1]}"/>\n'
        "\t<lib>\n"
        "\t\t<dict>\n"
        "\t\t\t<key>public.markColor</key>\n"
        f"\t\t\t<string>{BLUE}</string>\n"
        "\t\t\t<key>public.objectLibs</key>\n"
        "\t\t\t<dict>\n"
        f"\t\t\t\t<key>{ident}</key>\n"
        "\t\t\t\t<dict>\n"
        "\t\t\t\t\t<key>com.glyphsapp.component.alignment</key>\n"
        "\t\t\t\t\t<integer>-1</integer>\n"
        "\t\t\t\t</dict>\n"
        "\t\t\t</dict>\n"
        "\t\t</dict>\n"
        "\t</lib>\n"
        "</glyph>\n"
    )


def main():
    dry = "--dry-run" in sys.argv
    for master in MASTERS:
        ufo = pathlib.Path(f"sources/VirtuaGrotesk-{master}.ufo")
        cmap = plistlib.loads((ufo / "glyphs" / "contents.plist").read_bytes())
        for name in PLAN:
            path = ufo / "glyphs" / cmap[name]
            text = build(name, master)
            print(f"{'would write' if dry else 'wrote'} {master}/{path.name}")
            if not dry:
                path.write_text(text)


if __name__ == "__main__":
    sys.exit(main())
