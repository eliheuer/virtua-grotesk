"""Fontspector checks that only Virtua Grotesk needs.

`fgtools qa` (`make test`) runs them with the Font.Garden profile, in the
section "This font". A check that every Font.Garden font needs belongs in
fgtools, not here.
"""
from pathlib import Path

from fontspectorapi import FAIL, PASS, SKIP, CheckContext, CheckStatuses, Message, check
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


@check(id='virtua/a_bold', title='The a switches to its bold form at weight 500',
       rationale='The designspace has a rule that replaces a with a.bold from weight 500. '
                 'The variable font must make the same switch.')
def a_bold(font_path: Path, context: CheckContext) -> CheckStatuses:
    if 'fvar' not in TTFont(font_path):
        yield SKIP, Message('static', 'The switch is checked in the variable font.')
        return
    font = hb.Font(hb.Face(Path(font_path).read_bytes()))
    wrong = []
    for weight, expected in ((400, 'a'), (499, 'a'), (500, 'a.bold'), (700, 'a.bold')):
        font.set_variations({'wght': weight})
        buffer = hb.Buffer()
        buffer.add_str('a')
        buffer.guess_segment_properties()
        hb.shape(font, buffer)
        found = font.glyph_to_string(buffer.glyph_infos[0].codepoint)
        if found != expected:
            wrong.append(f'at {weight}: {found}, not {expected}')
    if wrong:
        yield FAIL, Message('wrong-form', '; '.join(wrong))
    else:
        yield PASS, Message('ok', 'The a switches at 500.')
