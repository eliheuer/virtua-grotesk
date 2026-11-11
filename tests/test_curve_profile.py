"""Geometry regressions for the read-only comb diagnostics (standard unittest)."""
import math
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from curve_lint import all_segments, classify_join, join_audit
from curve_profile import profile, read_contours, sample, svg


class CurveProfileTests(unittest.TestCase):
    def test_straight_has_zero_curvature(self):
        s=((0,0),(1,0),(2,0),(3,0),False,True)
        for t in (0,.25,.5,.75,1):
            self.assertEqual(sample(s,t)['curvature'],0)

    def test_quarter_circle_endpoint_curvature(self):
        h=4/3*math.tan(math.pi/8)
        s=((1,0),(1,h),(h,1),(0,1),False,True)
        self.assertAlmostEqual(sample(s,0)['curvature'],2*(1-h)/(3*h*h))
        self.assertAlmostEqual(sample(s,0)['curvature'],sample(s,1)['curvature'])

    def test_inflection_changes_sign(self):
        s=((0,0),(1,1),(2,-1),(3,0),False,True)
        self.assertLess(sample(s,.2)['curvature']*sample(s,.8)['curvature'],0)

    def test_zero_handle_is_undefined(self):
        s=((0,0),(0,0),(1,1),(2,1),False,True)
        self.assertIsNone(sample(s,0)['curvature'])

    def test_line_curve_can_have_zero_endpoint_curvature(self):
        line=((-3,0),(-2,0),(-1,0),(0,0),True,True)
        curve=((0,0),(1,0),(2,0),(3,1),False,True)
        self.assertEqual(sample(curve,0)['curvature'],0)
        # Legacy category is NOT a mathematical ceiling on continuity.
        self.assertEqual(classify_join(line,curve)[0],'G1line')

    def test_xml_attributes_and_unsupported_shapes(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'test.glif'
            p.write_text('<glyph><outline><contour identifier="c"><point type="line" y="0" x="0" identifier="a"/><point type="line" x="10" y="0"/><point type="line" x="0" y="10"/></contour></outline></glyph>')
            self.assertEqual(len(read_contours(p)[0]),3)
            p.write_text('<glyph><outline><component base="a"/></outline></glyph>')
            with self.assertRaisesRegex(ValueError,'components'):
                read_contours(p)
            p.write_text('<glyph><outline><contour><point type="move" x="0" y="0"/></contour></outline></glyph>')
            with self.assertRaisesRegex(ValueError,'unsupported'):
                read_contours(p)

    def test_profile_of_a_glif_file(self):
        # A circle of four arcs: no inflection, and curvature-continuous (G2)
        # joins. Shorter handles on the right side of the first arc keep the
        # joins tangent but change the curvature (G1). A control point pulled
        # inside the circle makes the first arc inflect.
        def glif(right_handle=276, pull=0):
            c = 276
            points = [
                (500, 0, 'curve'), (500 + right_handle, 0, None), (1000, 500 - c, None),
                (1000, 500, 'curve'), (1000, 500 + c, None), (500 + c, 1000, None),
                (500, 1000, 'curve'), (500 - c, 1000, None), (0, 500 + c, None),
                (0, 500, 'curve'), (0, 500 - c, None), (500 - c + pull, pull, None),
            ]
            rows = ''.join(f'<point x="{x}" y="{y}"' + (f' type="{k}" smooth="yes"' if k else '') + '/>' for x, y, k in points)
            return f'<glyph><outline><contour>{rows}</contour></outline></glyph>'
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'test.glif'
            p.write_text(glif())
            circle = profile(p)
            p.write_text(glif(right_handle=200))
            uneven = profile(p)
            p.write_text(glif(pull=300))
            dented = profile(p)
        self.assertEqual(sum(c['sampled_sign_changes'] for c in circle['curves']), 0)
        self.assertEqual({j['classification'] for j in circle['joins']}, {'G2'})
        self.assertEqual(next(j for j in uneven['joins'] if j['point'] == (500, 0))['classification'], 'G1')
        self.assertGreater(sum(c['sampled_sign_changes'] for c in dented['curves']), 0)
        self.assertIn('Same outline scale', svg([circle, dented]))

if __name__=='__main__':
    unittest.main()
