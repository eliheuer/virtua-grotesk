#!/usr/bin/env python3
"""Fix the metadata of the built fonts that the sources cannot set.

The sources set everything else: fsType, the meta table, the WWS bit of the
variable font and the glyphs that are not exported. These two fixes have
no source or gftools builder setting:

- The variable font gets an identity avar table. varLib does not write an
  avar table for an identity axis map. Fontspector: mandatory_avar_table.
- The static fonts get fsSelection bit 8 (WWS). The family varies only by
  weight and has WWS names. gftools clears the bit when it makes the static
  fonts. Fontspector: opentype/fsselection_wws.

    fix_gf_metadata.py FONT.ttf ...
"""
import sys

from fontTools.ttLib import TTFont, newTable

WWS = 1 << 8


def add_identity_avar(font):
    avar = newTable('avar')
    avar.majorVersion, avar.minorVersion = 1, 0
    avar.segments = {axis.axisTag: {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0} for axis in font['fvar'].axes}
    font['avar'] = avar


def fix(path):
    font = TTFont(path)
    if 'fvar' in font:
        if 'avar' not in font:
            add_identity_avar(font)
    else:
        font['OS/2'].fsSelection |= WWS
    font.save(path)


def main(paths):
    if not paths:
        sys.exit('usage: fix_gf_metadata.py FONT.ttf ...')
    for path in paths:
        fix(path)


if __name__ == '__main__':
    main(sys.argv[1:])
