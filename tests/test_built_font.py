"""Tests of the compiled fonts. Run `make build` first.

Each test checks one property over the whole character set, in the variable
font at three weights and in each static font. The tests do not fix design
values such as kerning, spacing or mark positions; those are Eli's decisions.
"""
import io
import itertools
from pathlib import Path
import unicodedata
import unittest

from fontTools import subset
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).resolve().parents[1]
VARIABLE = ROOT / 'fonts/variable/VirtuaGrotesk[wght].ttf'
STATIC = [ROOT / f'fonts/ttf/VirtuaGrotesk-{style}.ttf'
          for style in ('Regular', 'Medium', 'SemiBold', 'Bold')]
VARIABLE_WEIGHTS = (400, 550, 700)
INVISIBLE = {0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x2060, 0xFEFF}
LATIN_ABOVE = [0x0300, 0x0301, 0x0302, 0x0303, 0x0304, 0x0306,
               0x0307, 0x0308, 0x030A, 0x030B, 0x030C]
TATWEEL = '\u0640'
# Precomposed characters whose composite places the mark differently from the
# mark anchors. Reported to Eli on 2026-11-11. Remove a character when its
# composite and its anchors agree; the test fails until it is removed.
KNOWN_COMPOSITE_DIFFERENCES = {
    0x00E0, 0x00E1, 0x00E2, 0x00E3, 0x00E4, 0x00E5, 0x0101, 0x0103, 0x01CE,  # a with marks
    0x013A, 0x01E9,  # lacute, kcaron
    0x0622, 0x0623, 0x0624, 0x0625, 0x0626, 0x06C2,  # Arabic hamza and madda letters
    0xFB1F,  # Hebrew yod yod patah
}
DOTTED_CIRCLE = '\u25CC'


class Instance:
    """One font at one weight: its tables, outlines and a HarfBuzz font."""

    def __init__(self, path, font, data, weight):
        self.path, self.font, self.weight = path, font, weight
        self.name = f'{path.name} {weight}' if weight else path.name
        self.cmap = font.getBestCmap()
        self.glyphs = font.getGlyphSet(location={'wght': weight} if weight else None)
        self.shaper = hb.Font(hb.Face(data))
        if weight:
            self.shaper.set_variations({'wght': weight})

    def bounds(self, name):
        pen = BoundsPen(self.glyphs)
        self.glyphs[name].draw(pen)
        return pen.bounds

    def shape(self, text, features=None):
        """Shape text; return (glyph name, ink box in text coordinates, position)."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.shaper, buf, features or {})
        rows, x = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.font.getGlyphName(info.codepoint)
            pen = BoundsPen(self.glyphs)
            self.glyphs[name].draw(TransformPen(pen, (1, 0, 0, 1, x + pos.x_offset, pos.y_offset)))
            rows.append((name, pen.bounds, pos))
            x += pos.x_advance
        return rows


def instances(path):
    font = TTFont(path)
    data = path.read_bytes()
    weights = VARIABLE_WEIGHTS if 'fvar' in font else (None,)
    return [Instance(path, font, data, weight) for weight in weights]


def without_precomposed(path):
    """A subset of the font without its precomposed letters, as a web font
    subset can be. HarfBuzz then shapes their decomposed sequences."""
    font = TTFont(path)
    cmap = font.getBestCmap()
    options = subset.Options()
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.glyph_names = True
    options.notdef_outline = True
    options.drop_tables += ['meta']
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes={cp for cp in cmap if cp not in precomposed(cmap)})
    subsetter.subset(font)
    stream = io.BytesIO()
    font.save(stream)
    return stream.getvalue()


def precomposed(cmap):
    """Encoded characters whose canonical decomposition is also encoded."""
    found = []
    for cp in cmap:
        nfd = unicodedata.normalize('NFD', chr(cp))
        if nfd != chr(cp) and all(ord(c) in cmap for c in nfd):
            found.append(cp)
    return found


def union(boxes):
    boxes = [b for b in boxes if b]
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


@unittest.skipUnless(VARIABLE.exists(), 'Run make build first')
class BuiltFontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = [VARIABLE] + STATIC
        cls.instances = [i for path in cls.paths for i in instances(path)]

    def test_every_visible_character_has_ink(self):
        for i in self.instances:
            for cp, name in i.cmap.items():
                category = unicodedata.category(chr(cp))
                if category.startswith('Z') or category == 'Cc' or cp in INVISIBLE:
                    continue
                with self.subTest(font=i.name, character=f'U+{cp:04X}'):
                    self.assertIsNotNone(i.bounds(name))

    def test_spaces_and_invisible_characters_have_no_ink(self):
        for i in self.instances:
            for cp, name in i.cmap.items():
                if unicodedata.category(chr(cp)) == 'Zs' or cp in INVISIBLE:
                    with self.subTest(font=i.name, character=f'U+{cp:04X}'):
                        self.assertIsNone(i.bounds(name))

    def test_combining_marks_have_mark_class_and_zero_advance(self):
        for path in self.paths:
            font = TTFont(path)
            classes = font['GDEF'].table.GlyphClassDef.classDefs
            for cp, name in font.getBestCmap().items():
                if unicodedata.category(chr(cp)) == 'Mn':
                    with self.subTest(font=path.name, character=f'U+{cp:04X}'):
                        self.assertEqual(classes.get(name), 3)
                        self.assertEqual(font['hmtx'][name][0], 0)

    def test_combining_marks_attach_to_their_bases(self):
        # A mark attaches when the mark feature moves it. A base and mark that
        # HarfBuzz composes into one precomposed glyph need no attachment.
        def bases(cp):
            if cp in (0x05C1, 0x05C2):
                return DOTTED_CIRCLE, '\u05E9'
            if 0x0590 <= cp <= 0x05FF:
                return DOTTED_CIRCLE, '\u05D1'
            if 0x0600 <= cp <= 0x06FF:
                return DOTTED_CIRCLE, '\u0628'
            if 0x0300 <= cp <= 0x036F:
                return DOTTED_CIRCLE, 'a', 'x'
            return (DOTTED_CIRCLE,)
        for i in self.instances:
            for cp in i.cmap:
                if unicodedata.category(chr(cp)) != 'Mn':
                    continue
                for base in bases(cp):
                    with self.subTest(font=i.name, base=base, mark=f'U+{cp:04X}'):
                        on = i.shape(base + chr(cp))
                        if len(on) == 1:
                            continue
                        off = i.shape(base + chr(cp), {'mark': False})
                        self.assertNotEqual([(p.x_offset, p.y_offset) for _, _, p in on],
                                            [(p.x_offset, p.y_offset) for _, _, p in off])

    def test_precomposed_letters_match_their_decomposed_sequences(self):
        # Compares ink only. The advance of an accented letter can differ
        # from its base by design.
        differs = set()
        for path in self.paths:
            reduced = without_precomposed(path)
            reduced_font = TTFont(io.BytesIO(reduced))
            for full in instances(path):
                fallback = Instance(path, reduced_font, reduced, full.weight)
                for cp in precomposed(full.cmap):
                    expected = union(b for _, b, _ in full.shape(chr(cp)))
                    actual = union(b for _, b, _ in fallback.shape(chr(cp)))
                    if all(abs(a - b) <= 2 for a, b in zip(expected, actual)):
                        continue
                    differs.add(cp)
                    if cp not in KNOWN_COMPOSITE_DIFFERENCES:
                        self.fail(f'{full.name} U+{cp:04X}: composite {expected}, anchors {actual}')
        now_equal = sorted(f'U+{cp:04X}' for cp in KNOWN_COMPOSITE_DIFFERENCES - differs)
        self.assertFalse(now_equal, f'Remove from KNOWN_COMPOSITE_DIFFERENCES: {now_equal}')

    def test_stacked_marks_do_not_touch(self):
        for i in self.instances:
            for base, (first, second) in itertools.product('oOn', itertools.product(LATIN_ABOVE, repeat=2)):
                rows = i.shape(base + chr(first) + chr(second))
                if len(rows) < 3:
                    continue
                with self.subTest(font=i.name, text=base + chr(first) + chr(second)):
                    self.assertGreaterEqual(rows[2][1][1] - rows[1][1][3], 16)

    def test_arabic_letters_join_without_gaps(self):
        # The shaped glyphs are in visual order, left to right. A final or
        # medial form joins the glyph on its right; an initial or medial
        # form joins the glyph on its left.
        for i in self.instances:
            tatweel = i.cmap[ord(TATWEEL)]
            letters = [cp for cp in i.cmap if 0x0620 <= cp <= 0x06FF
                       and unicodedata.category(chr(cp)) == 'Lo']
            for cp in letters:
                for text in (TATWEEL + chr(cp) + TATWEEL, TATWEEL + chr(cp)):
                    rows = i.shape(text)
                    for (left, a, _), (right, b, _) in zip(rows, rows[1:]):
                        if tatweel not in (left, right) or a is None or b is None:
                            continue
                        letter = right if left == tatweel else left
                        joins = (letter.endswith(('.fina', '.medi')) if letter == left
                                 else letter.endswith(('.init', '.medi')))
                        if joins:
                            with self.subTest(font=i.name, text=text):
                                self.assertLessEqual(b[0] - a[2], 1)

    def test_hebrew_cantillation_clears_the_vowel_point(self):
        # Above: holam. Below: hataf patah. Each accent sits on one side of
        # the point and keeps 30 units from it.
        right_below = {0x059A, 0x05AD}
        left_above = {0x0592, 0x0599, 0x05A9, 0x05AE}
        for i in self.instances:
            for cp in (*range(0x0591, 0x05B0), 0x05C4, 0x05C5):
                below = unicodedata.combining(chr(cp)) in (220, 222)
                point = '\u05B2' if below else '\u05B9'
                with self.subTest(font=i.name, accent=f'U+{cp:04X}'):
                    boxes = {name: box for name, box, _ in i.shape('\u05D1' + point + chr(cp))}
                    accent, vowel = boxes[i.cmap[cp]], boxes[i.cmap[ord(point)]]
                    on_right = cp in right_below if below else cp not in left_above
                    gap = accent[0] - vowel[2] if on_right else vowel[0] - accent[2]
                    self.assertGreaterEqual(gap, 30)

    def test_hebrew_meteg_clears_the_vowel_point(self):
        vowels = (*range(0x05B0, 0x05B9), 0x05BB, 0x05C7)
        for i in self.instances:
            meteg = i.cmap[0x05BD]
            for base, vowel in itertools.product('\u05D0\u05D1\u05DB\u05E4\u05E2\u05EA', vowels):
                with self.subTest(font=i.name, base=base, vowel=f'U+{vowel:04X}'):
                    boxes = {name: box for name, box, _ in i.shape(base + chr(vowel) + '\u05BD')}
                    self.assertGreaterEqual(boxes[i.cmap[vowel]][0] - boxes[meteg][2], 24)

    def test_each_static_font_has_its_own_stat_weight(self):
        for path in STATIC:
            font = TTFont(path)
            with self.subTest(font=path.name):
                stat = font['STAT'].table
                tags = [axis.AxisTag for axis in stat.DesignAxisRecord.Axis]
                weights = [value.Value for value in stat.AxisValueArray.AxisValue
                           if tags[value.AxisIndex] == 'wght']
                self.assertEqual(weights, [font['OS/2'].usWeightClass])

    def test_a_switches_to_its_bold_form_at_500(self):
        i = instances(VARIABLE)[0]
        for weight, expected in ((400, 'a'), (499, 'a'), (500, 'a.bold'), (700, 'a.bold')):
            i.shaper.set_variations({'wght': weight})
            with self.subTest(weight=weight):
                self.assertEqual(i.shape('a')[0][0], expected)


if __name__ == '__main__':
    unittest.main()
