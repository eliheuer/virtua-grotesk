#!/usr/bin/env python3
"""Fix the metadata of the built fonts that the sources cannot set.

The sources set everything else: fsType, the meta table, the WWS bit of the
variable font and the glyphs that are not exported. These three fixes have
no source or gftools builder setting:

- The variable font gets an identity avar table. varLib does not write an
  avar table for an identity axis map. Fontspector: mandatory_avar_table.
- The static fonts get fsSelection bit 8 (WWS). The family varies only by
  weight and has WWS names. gftools clears the bit when it makes the static
  fonts. Fontspector: opentype/fsselection_wws.
- The Regular static font loses a.bold. The variable font switches a to
  a.bold from weight 500, so no character reaches a.bold at 400.
  Fontspector: unreachable_glyphs.

    fix_gf_metadata.py FONT.ttf ...
"""
import sys

from fontTools import subset
from fontTools.ttLib import TTFont, newTable

WWS = 1 << 8


def add_identity_avar(font):
    avar = newTable('avar')
    avar.majorVersion, avar.minorVersion = 1, 0
    avar.segments = {axis.axisTag: {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0} for axis in font['fvar'].axes}
    font['avar'] = avar


def remove_glyph(font, name):
    options = subset.Options()
    for option in ('name_legacy', 'notdef_glyph', 'notdef_outline', 'recommended_glyphs',
                   'passthrough_tables', 'glyph_names', 'legacy_cmap'):
        setattr(options, option, True)
    options.name_IDs = options.name_languages = options.layout_features = ['*']
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(glyphs=[g for g in font.getGlyphOrder() if g != name])
    subsetter.subset(font)


def fix(path):
    font = TTFont(path)
    if 'fvar' in font:
        if 'avar' not in font:
            add_identity_avar(font)
    else:
        font['OS/2'].fsSelection |= WWS
        if font['OS/2'].usWeightClass == 400 and 'a.bold' in font.getGlyphOrder():
            remove_glyph(font, 'a.bold')
    font.save(path)


def main(paths):
    if not paths:
        sys.exit('usage: fix_gf_metadata.py FONT.ttf ...')
    for path in paths:
        fix(path)


if __name__ == '__main__':
    main(sys.argv[1:])
