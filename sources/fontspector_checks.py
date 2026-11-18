"""Fontspector checks that only Virtua Grotesk needs.

`fgtools qa` (`make test`) runs them with the Font.Garden profile, in the
section "This font". A check that every Font.Garden font needs belongs in
fgtools, not here.
"""
from pathlib import Path
from unicodedata import normalize

from fontspectorapi import FAIL, PASS, CheckContext, CheckStatuses, Message, check
from fontTools.ttLib import TTFont
import uharfbuzz as hb

# Modern Hebrew: the letters, the vowel points, maqaf, the shin and sin dots,
# qamats qatan, geresh, gershayim and the new sheqel sign.
MODERN_HEBREW = {*range(0x05D0, 0x05EB), *range(0x05B0, 0x05BD),
                 0x05BE, 0x05C1, 0x05C2, 0x05C7, 0x05F3, 0x05F4, 0x20AA}


@check(id='virtua/modern_hebrew', title='Modern Hebrew is covered',
       rationale='The first release has Latin, Arabic and Hebrew. Every font has the '
                 'characters of modern Hebrew.')
def modern_hebrew(font_path: Path, context: CheckContext) -> CheckStatuses:
    missing = sorted(MODERN_HEBREW - set(TTFont(font_path).getBestCmap()))
    if missing:
        yield FAIL, Message('missing', 'Missing: ' + ' '.join(f'U+{code:04X}' for code in missing))
    else:
        yield PASS, Message('ok', 'Modern Hebrew is covered.')


@check(id='virtua/a_continuous', title='The a uses one glyph at every weight',
       rationale='The lowercase a and its accented forms interpolate without a glyph switch.')
def a_continuous(font_path: Path, context: CheckContext) -> CheckStatuses:
    with TTFont(font_path) as ttfont:
        glyphs = ttfont.getGlyphOrder()
        variable = 'fvar' in ttfont
    if 'a.bold' in glyphs:
        yield FAIL, Message('retired-alternate', 'The retired a.bold glyph is still exported.')
        return
    font = hb.Font(hb.Face(font_path.read_bytes()))

    def shape(text):
        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.guess_segment_properties()
        hb.shape(font, buffer)
        return [(glyphs[info.codepoint], pos.x_advance, pos.x_offset, pos.y_offset)
                for info, pos in zip(buffer.glyph_infos, buffer.glyph_positions)]

    wrong = []
    for weight in (400, 499, 500, 550, 700) if variable else (None,):
        if weight is not None:
            font.set_variations({'wght': weight})
        location = f'at weight {weight}' if weight is not None else 'in the static font'
        if [row[0] for row in shape('a')] != ['a']:
            wrong.append(f'The a uses another glyph {location}.')
        for letter in 'àáâãäåāăąǎ':
            if shape(letter) != shape(normalize('NFD', letter)):
                wrong.append(f'{letter} shapes differently when decomposed {location}.')
    if wrong:
        yield FAIL, Message('wrong-form', ' '.join(wrong))
    else:
        yield PASS, Message('ok', 'The a uses one glyph and its accents shape consistently.')
