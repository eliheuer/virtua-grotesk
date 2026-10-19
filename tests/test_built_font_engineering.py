"""Regression checks for compiled layout/metadata. Run after make build."""
from pathlib import Path
import io
import unicodedata
import unittest

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
from scripts.check_hebrew import audit as audit_hebrew

ROOT = Path(__file__).resolve().parents[1]
VF = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"


@unittest.skipUnless(VF.exists(), "Run make build for compiled-font checks")
class BuiltFontEngineeringTests(unittest.TestCase):
    def fonts(self):
        paths = [VF] + [ROOT / f"fonts/ttf/VirtuaGrotesk-{style}.ttf"
                        for style in ("Regular", "Medium", "SemiBold", "Bold")]
        for path in paths:
            with TTFont(path) as font:
                yield path, font

    def test_zero_width_space_and_combining_mark_classes(self):
        for path, font in self.fonts():
            with self.subTest(font=path.name):
                cmap = font.getBestCmap()
                self.assertEqual(font["hmtx"][cmap[0x200B]][0], 0)
                classes = font["GDEF"].table.GlyphClassDef.classDefs
                for cp, name in cmap.items():
                    if unicodedata.category(chr(cp)).startswith("M"):
                        self.assertEqual(classes.get(name), 3, f"U+{cp:04X}")
                        self.assertEqual(font["hmtx"][name][0], 0, f"U+{cp:04X}")

    def test_hebrew_attachment_in_all_outputs(self):
        for path, _font in self.fonts():
            with self.subTest(font=path.name):
                self.assertEqual(audit_hebrew(path)["failures"], [])

    def test_dotless_qaf_final_reaches_the_joining_edge(self):
        for path, font in self.fonts():
            weights = (400, 500, 600, 700) if "fvar" in font else (None,)
            for weight in weights:
                with self.subTest(font=path.name, weight=weight):
                    shaped = hb.Font(hb.Face(path.read_bytes()))
                    if weight is not None:
                        shaped.set_variations({"wght": weight})
                    buf = hb.Buffer()
                    buf.add_str("بٯ")
                    buf.guess_segment_properties()
                    hb.shape(shaped, buf)
                    name = font.getGlyphName(buf.glyph_infos[0].codepoint)
                    self.assertEqual(name, "uni066F.fina")
                    glyphs = font.getGlyphSet(location={"wght": weight}
                                              if weight is not None else None)
                    bounds = BoundsPen(glyphs)
                    glyphs[name].draw(bounds)
                    self.assertAlmostEqual(buf.glyph_positions[0].x_advance,
                                           bounds.bounds[2], delta=1)

    def test_hebrew_marks_attach_to_dotted_circle(self):
        for path, font in self.fonts():
            cmap = font.getBestCmap()
            attached = set()
            for lookup in font["GPOS"].table.LookupList.Lookup:
                for subtable in lookup.SubTable:
                    st = getattr(subtable, "ExtSubTable", subtable)
                    if hasattr(st, "BaseCoverage") and cmap[0x25CC] in st.BaseCoverage.glyphs:
                        attached.update(st.MarkCoverage.glyphs)
            for cp in [*range(0x05B0, 0x05BD), 0x05C1, 0x05C2, 0x05C7]:
                with self.subTest(font=path.name, codepoint=hex(cp)):
                    self.assertIn(cmap[cp], attached)

    def test_latin_composite_mark_attachment(self):
        for path, font in self.fonts():
            face = hb.Face(path.read_bytes())
            shaped_font = hb.Font(face)
            for sample in ("Ą́", "ę̃", "į́", "Ų̃"):
                with self.subTest(font=path.name, sample=sample):
                    positions = []
                    for enabled in (False, True):
                        buf = hb.Buffer()
                        buf.add_str(sample)
                        buf.guess_segment_properties()
                        hb.shape(shaped_font, buf, {"mark": enabled})
                        positions.append([(p.x_offset, p.y_offset)
                                          for p in buf.glyph_positions])
                    self.assertNotEqual(positions[0], positions[1])

    def test_noon_ghunna_mark_attaches(self):
        for path, font in self.fonts():
            weights = (400, 550, 700) if "fvar" in font else (None,)
            shaped = hb.Font(hb.Face(path.read_bytes()))
            for weight in weights:
                if weight is not None:
                    shaped.set_variations({"wght": weight})
                for sample in ("◌٘", "ب٘"):
                    with self.subTest(font=path.name, weight=weight, sample=sample):
                        positions = []
                        for enabled in (False, True):
                            buf = hb.Buffer()
                            buf.add_str(sample)
                            buf.guess_segment_properties()
                            hb.shape(shaped, buf, {"mark": enabled})
                            self.assertTrue(all(g.codepoint for g in buf.glyph_infos))
                            positions.append([(p.x_offset, p.y_offset)
                                              for p in buf.glyph_positions])
                        self.assertNotEqual(positions[0], positions[1])

    def test_repaired_composites_have_visible_outlines(self):
        for path, font in self.fonts():
            cmap = font.getBestCmap()
            glyphs = font.getGlyphSet()
            for cp in (0x0132, 0x0133, 0x014A, 0x014B, 0x02BB, 0xFB1D, 0xFB1F,
                       0x05BD, 0x05BF, 0x05C0, 0x05C3, 0x05C6, 0xFB20,
                       0xFB29, 0xFB4C, 0xFB4D, 0xFB4E, 0xFB4F):
                with self.subTest(font=path.name, codepoint=hex(cp)):
                    self.assertIn(cp, cmap)
                    pen = BoundsPen(glyphs)
                    glyphs[cmap[cp]].draw(pen)
                    self.assertIsNotNone(pen.bounds)

    def test_all_encoded_hebrew_has_ink_across_weights(self):
        for path, font in self.fonts():
            cmap = font.getBestCmap()
            for weight in ((400, 550, 700) if "fvar" in font else (None,)):
                glyphs = font.getGlyphSet(location={"wght": weight}
                                          if weight is not None else None)
                for cp, name in cmap.items():
                    if not (0x0590 <= cp <= 0x05FF or 0xFB1D <= cp <= 0xFB4F):
                        continue
                    with self.subTest(font=path.name, weight=weight, cp=hex(cp)):
                        pen = BoundsPen(glyphs)
                        glyphs[name].draw(pen)
                        self.assertIsNotNone(pen.bounds)

    def test_cantillation_clears_points_on_correct_side(self):
        marks = (*range(0x0591, 0x05B0), 0x05C4, 0x05C5, 0xFB1E)
        for path, font in self.fonts():
            cmap = font.getBestCmap()
            for weight in ((400, 550, 700) if "fvar" in font else (None,)):
                shaped = hb.Font(hb.Face(path.read_bytes()))
                if weight is not None:
                    shaped.set_variations({"wght": weight})
                glyphs = font.getGlyphSet(location={"wght": weight}
                                          if weight is not None else None)
                for cp in marks:
                    below = unicodedata.combining(chr(cp)) in (220, 222)
                    point = 0x05B2 if below else 0x05B9
                    with self.subTest(font=path.name, weight=weight, cp=hex(cp)):
                        buf = hb.Buffer()
                        buf.add_str("ב" + chr(point) + chr(cp))
                        buf.guess_segment_properties()
                        hb.shape(shaped, buf)
                        boxes = {}
                        x = 0
                        for glyph, pos in zip(buf.glyph_infos, buf.glyph_positions):
                            self.assertNotEqual(glyph.codepoint, 0)
                            name = font.getGlyphName(glyph.codepoint)
                            pen = BoundsPen(glyphs)
                            glyphs[name].draw(pen)
                            self.assertIsNotNone(pen.bounds)
                            boxes[name] = (pen.bounds[0] + x + pos.x_offset,
                                           pen.bounds[2] + x + pos.x_offset)
                            if name in (cmap[cp], cmap[point]):
                                self.assertEqual(pos.x_advance, 0)
                            x += pos.x_advance
                        accent, vowel = boxes[cmap[cp]], boxes[cmap[point]]
                        on_right = (cp in (0x059A, 0x05AD) if below else
                                    cp not in (0x0592, 0x0599, 0x05A9, 0x05AE))
                        gap = accent[0] - vowel[1] if on_right else vowel[0] - accent[1]
                        self.assertGreaterEqual(gap, 30)

    def test_hebrew_meteg_clearance_and_nun_dot(self):
        for path, font in self.fonts():
            cmap = font.getBestCmap()
            shaped = hb.Font(hb.Face(path.read_bytes()))
            for weight in ((400, 550, 700) if "fvar" in font else (None,)):
                if weight is not None:
                    shaped.set_variations({"wght": weight})
                glyphs = font.getGlyphSet(location={"wght": weight}
                                          if weight is not None else None)

                def ink(text):
                    buf = hb.Buffer()
                    buf.add_str(text)
                    buf.guess_segment_properties()
                    hb.shape(shaped, buf)
                    boxes = {}
                    x = 0
                    for glyph, pos in zip(buf.glyph_infos, buf.glyph_positions):
                        self.assertNotEqual(glyph.codepoint, 0)
                        name = font.getGlyphName(glyph.codepoint)
                        pen = BoundsPen(glyphs)
                        glyphs[name].draw(pen)
                        self.assertIsNotNone(pen.bounds)
                        a, b, c, d = pen.bounds
                        boxes[name] = (a + x + pos.x_offset, b + pos.y_offset,
                                       c + x + pos.x_offset, d + pos.y_offset)
                        if name in (cmap[0x05BD], cmap[0x05BF], cmap[0x0307]):
                            self.assertEqual(pos.x_advance, 0)
                        x += pos.x_advance
                    return boxes, x

                for base in "אבכפעת":
                    for vowel in (*range(0x05B0, 0x05B9), 0x05BB, 0x05C7):
                        with self.subTest(font=path.name, weight=weight,
                                          base=base, vowel=hex(vowel)):
                            boxes, _ = ink(base + chr(vowel) + "\u05BD")
                            self.assertGreaterEqual(
                                boxes[cmap[vowel]][0] - boxes[cmap[0x05BD]][2], 24)
                with self.subTest(font=path.name, weight=weight, sample="nun dot"):
                    boxes, _ = ink("\u05C6\u0307")
                    self.assertAlmostEqual(
                        boxes[cmap[0x0307]][1] - boxes[cmap[0x05C6]][3], 96, delta=2)
                for composed, decomposed in (("בֿ", "בֿ"), ("כֿ", "כֿ"), ("פֿ", "פֿ")):
                    with self.subTest(font=path.name, weight=weight, sample=composed):
                        results = []
                        for text in (composed, decomposed):
                            boxes, advance = ink(text)
                            bb = list(boxes.values())
                            results.append((advance, min(b[0] for b in bb),
                                            min(b[1] for b in bb), max(b[2] for b in bb),
                                            max(b[3] for b in bb)))
                        for a, b in zip(*results):
                            self.assertAlmostEqual(a, b, delta=1)

    def test_tilde_decomposition_preserves_placement(self):
        # A web subset may omit the precomposed letters but retain E/e and
        # U+0303. Exercise HarfBuzz's real fallback, not only GPOS presence.
        for path, font in self.fonts():
            fallback = TTFont(path)
            options = subset.Options()
            options.layout_features = ["*"]
            options.drop_tables += ["meta"]
            worker = subset.Subsetter(options=options)
            worker.populate(unicodes=set(fallback.getBestCmap()) - {0x1EBC, 0x1EBD})
            worker.subset(fallback)
            stream = io.BytesIO()
            fallback.save(stream)
            weights = (400, 499, 500, 550, 700) if "fvar" in font else (None,)
            for weight in weights:
                for text, features in (("Ẽ", {"ccmp": False}), ("ẽ", {"ccmp": False}),
                                       ("Tẽ Vẽ ẽt ẽz rẽ ẽT tẽ ẽ’", {})):
                    results = []
                    for data, ttfont in ((path.read_bytes(), font),
                                         (stream.getvalue(), fallback)):
                        shaped = hb.Font(hb.Face(data))
                        if weight is not None:
                            shaped.set_variations({"wght": weight})
                        buf = hb.Buffer()
                        buf.add_str(text)
                        buf.guess_segment_properties()
                        hb.shape(shaped, buf, features)
                        glyphs = ttfont.getGlyphSet(location={"wght": weight}
                                                   if weight is not None else None)
                        pen = BoundsPen(glyphs)
                        advance = 0
                        for glyph, pos in zip(buf.glyph_infos, buf.glyph_positions):
                            self.assertNotEqual(glyph.codepoint, 0)
                            name = ttfont.getGlyphName(glyph.codepoint)
                            glyphs[name].draw(TransformPen(
                                pen, (1, 0, 0, 1, advance + pos.x_offset, pos.y_offset)))
                            advance += pos.x_advance
                        results.append((advance, pen.bounds))
                    with self.subTest(font=path.name, weight=weight, text=text):
                        self.assertEqual(results[0][0], results[1][0])
                        for full, decomposed in zip(results[0][1], results[1][1]):
                            self.assertAlmostEqual(full, decomposed, delta=1)

    def test_tilde_clears_ascenders_and_dotted_circle(self):
        for path, font in self.fonts():
            weights = (400, 550, 700) if "fvar" in font else (None,)
            for weight in weights:
                shaped = hb.Font(hb.Face(path.read_bytes()))
                if weight is not None:
                    shaped.set_variations({"wght": weight})
                glyphs = font.getGlyphSet(location={"wght": weight}
                                          if weight is not None else None)
                for base in "bdfhklt◌":
                    with self.subTest(font=path.name, weight=weight, base=base):
                        buf = hb.Buffer()
                        buf.add_str(base + "\u0303")
                        buf.guess_segment_properties()
                        hb.shape(shaped, buf)
                        self.assertEqual(len(buf.glyph_infos), 2)
                        bounds = []
                        for glyph, pos in zip(buf.glyph_infos, buf.glyph_positions):
                            self.assertNotEqual(glyph.codepoint, 0)
                            pen = BoundsPen(glyphs)
                            glyphs[font.getGlyphName(glyph.codepoint)].draw(pen)
                            bounds.append((pen.bounds[1] + pos.y_offset,
                                           pen.bounds[3] + pos.y_offset))
                        self.assertGreaterEqual(bounds[1][0] - bounds[0][1], 48)

    def test_static_stat_and_unused_alternate(self):
        for path, font in self.fonts():
            if "fvar" in font:
                self.assertIn("a.bold", font.getGlyphOrder())
                continue
            with self.subTest(font=path.name):
                stat = font["STAT"].table
                tags = [a.AxisTag for a in stat.DesignAxisRecord.Axis]
                weights = [v.Value for v in stat.AxisValueArray.AxisValue
                           if tags[v.AxisIndex] == "wght"]
                self.assertEqual(weights, [font["OS/2"].usWeightClass])
                if font["OS/2"].usWeightClass == 400:
                    self.assertNotIn("a.bold", font.getGlyphOrder())

    def test_macron_below_attaches_across_weight_alternate(self):
        for path, font in self.fonts():
            weights = (400, 499, 500, 550, 700) if "fvar" in font else (None,)
            shaped = hb.Font(hb.Face(path.read_bytes()))
            for weight in weights:
                if weight is not None:
                    shaped.set_variations({"wght": weight})
                for sample in ("a̱", "e̱", "i̱", "o̱", "u̱", "◌̱"):
                    with self.subTest(font=path.name, weight=weight, sample=sample):
                        positions = []
                        for enabled in (False, True):
                            buf = hb.Buffer()
                            buf.add_str(sample)
                            buf.guess_segment_properties()
                            hb.shape(shaped, buf, {"mark": enabled})
                            self.assertEqual(len(buf.glyph_infos), 2)
                            self.assertTrue(all(g.codepoint for g in buf.glyph_infos))
                            self.assertEqual(buf.glyph_positions[-1].x_advance, 0)
                            positions.append([(p.x_offset, p.y_offset)
                                              for p in buf.glyph_positions])
                        self.assertNotEqual(positions[0], positions[1])

    def test_weight_alternate_still_shapes(self):
        font = hb.Font(hb.Face(VF.read_bytes()))
        names = TTFont(VF).getGlyphOrder()
        for weight, expected in [(400, "a"), (499, "a"), (500, "a.bold"), (700, "a.bold")]:
            font.set_variations({"wght": weight})
            buf = hb.Buffer()
            buf.add_str("a")
            buf.guess_segment_properties()
            hb.shape(font, buf)
            self.assertEqual(names[buf.glyph_infos[0].codepoint], expected)

    def test_recovered_regular_kerning_and_existing_override(self):
        font = hb.Font(hb.Face(VF.read_bytes()))
        for sample, expected in {"nv": -32, "Fs": -64, "Ps": -64,
                                 ".c": -32, ".o": -32, ".p": -32,
                                 "rc": -32, "rp": -32, "r.": -128,
                                 "ta": -32, "ro": -64}.items():
            widths = []
            for enabled in (False, True):
                buf = hb.Buffer()
                buf.add_str(sample)
                buf.guess_segment_properties()
                hb.shape(font, buf, {"kern": enabled})
                widths.append(sum(p.x_advance for p in buf.glyph_positions))
            self.assertEqual(widths[1] - widths[0], expected, sample)


if __name__ == "__main__":
    unittest.main()
