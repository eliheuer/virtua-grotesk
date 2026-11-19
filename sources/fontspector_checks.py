"""Fontspector checks that only Virtua Grotesk needs.

`fgtools qa` (`make test`) runs them with the Font.Garden profile, in the
section "This font". A check that every Font.Garden font needs belongs in
fgtools, not here.
"""
from itertools import product
from pathlib import Path
from unicodedata import normalize

from fgtools import project
from fontspectorapi import FAIL, PASS, CheckContext, CheckStatuses, Message, check
from fontTools.pens.recordingPen import RecordingPen
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


def horizontal_edges(glyph):
    """Yield (start x, end x, y) for each horizontal line in outline order."""
    pen = RecordingPen()
    glyph.draw(pen)
    start = previous = None
    for operation, points in pen.value:
        if operation == 'moveTo':
            start = points[0]
        elif operation in ('lineTo', 'closePath'):
            end = points[0] if operation == 'lineTo' else start
            if previous is not None and end is not None:
                x0, y0 = previous
                x1, y1 = end
                if abs(y1 - y0) < 1e-6 and abs(x1 - x0) > 1e-6:
                    yield x0, x1, y0
        previous = points[-1] if points else None


@check(id='virtua/a_flats', title='The a keeps both waist shelves and the foot flat',
       rationale='The waist and baseline land on straight segments across the designspace.')
def a_flats(font_path: Path, context: CheckContext) -> CheckStatuses:
    design = project.load(Path(__file__).resolve().parents[1]).design()['a_geometry']
    upper = design['regular_upper_waist']
    lower = design['regular_lower_waist']
    foot = design['regular_foot']

    wrong = []
    with TTFont(font_path) as font:
        if 'fvar' in font:
            fvar = font['fvar']
            values = {}
            for axis in fvar.axes:
                tag = axis.axisTag
                knots = sorted({axis.minValue, axis.defaultValue, axis.maxValue}
                               | {instance.coordinates[tag] for instance in fvar.instances})
                values[tag] = sorted(set(knots) | {(a + b) / 2 for a, b in zip(knots, knots[1:])})
            locations = [(weight, size, {'wght': weight, 'opsz': size})
                         for weight, size in product(values['wght'], values['opsz'])]
        else:
            # The static fonts in the build are the text-size instances.
            locations = [(font['OS/2'].usWeightClass, 14, None)]

        glyph_name = font.getBestCmap().get(ord('a'))
        if glyph_name is None:
            yield FAIL, Message('missing-a', 'The lowercase a is absent.')
            return
        for weight, size, location in locations:
            glyph = font.getGlyphSet(location=location)[glyph_name]
            edges = list(horizontal_edges(glyph))
            if weight == 400 and size == 14:
                flats = [(min(x0, x1), max(x0, x1), y) for x0, x1, y in edges]
                has_upper = tuple(upper) in flats
                has_lower = tuple(lower) in flats
                has_foot = tuple(foot) in flats
            else:
                # The waist is in the right half of the glyph. Opposite
                # directions identify the outer and counter edges in TrueType.
                right_half = glyph.width / 2
                has_upper = any(x1 >= right_half and x1 - x0 >= 16 and y > lower[2]
                                for x0, x1, y in edges)
                has_lower = any(x0 >= right_half and x0 - x1 >= 16 and foot[2] < y < upper[2]
                                for x0, x1, y in edges)
                has_foot = any(x1 >= right_half and x0 - x1 >= 16 and abs(y - foot[2]) < 1e-6
                               for x0, x1, y in edges)
            missing = [label for label, found in (('upper waist shelf', has_upper),
                                                  ('lower waist shelf', has_lower),
                                                  ('foot flat', has_foot)) if not found]
            if missing:
                wrong.append(f'wght {weight:g}, opsz {size:g}: {", ".join(missing)}')

    if wrong:
        count = len(wrong)
        examples = '; '.join(wrong[:5])
        yield FAIL, Message('missing-flats', f'{count} location(s) with missing or changed flats. {examples}')
    else:
        yield PASS, Message('ok', 'The a keeps both waist shelves and the foot flat.')


def arabic_counter_size(font, name):
    """Measure the enclosed counter of a TrueType feh or feh–yeh."""
    glyf = font['glyf']
    coords, ends, _ = glyf[name].getCoordinates(glyf)
    start = 0
    counters = []
    for end in ends:
        points = list(coords[start:end + 1])
        start = end + 1
        area = sum(x * v - y * u for (x, y), (u, v)
                   in zip(points, points[1:] + points[:1]))
        if area > 0:
            xs, ys = zip(*points)
            counters.append((max(xs) - min(xs), max(ys) - min(ys)))
    return counters


@check(id='virtua/feh_yeh_counter', title='The stacked feh keeps the donor counter',
       rationale='A compressed counter makes the ligature look heavier than neighboring feh.')
def feh_yeh_counter(font_path: Path, context: CheckContext) -> CheckStatuses:
    with TTFont(font_path) as font:
        pair = ('uni0641.init', 'feh_yehar')
        if any(name not in font.getGlyphOrder() for name in pair):
            yield FAIL, Message('missing-form', 'Missing initial feh or its yeh ligature.')
            return
        donor, ligature = (arabic_counter_size(font, name) for name in pair)
        # Translating an interpolated contour can change integer rounding by one unit.
        if (len(donor) != 1 or len(ligature) != 1
                or any(abs(a - b) > 1 for a, b in zip(donor[0], ligature[0]))):
            yield FAIL, Message('counter-size', f'Initial feh {donor}, feh–yeh {ligature}.')
        else:
            yield PASS, Message('ok', f'Initial feh {donor}, feh–yeh {ligature}.')
