"""Geometry regressions for the read-only comb diagnostics (standard unittest)."""
import math
from pathlib import Path
import tempfile
import unittest

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

    def test_saved_correction_exposes_actual_failure(self):
        case=Path(__file__).resolve().parents[1]/'agent-proofs/cases/arabic-003/manual-correction-01'
        ai=profile(case/'ai.glif'); human=profile(case/'human.glif')
        self.assertEqual(sum(c['sampled_sign_changes'] for c in ai['curves']),1)
        self.assertEqual(sum(c['sampled_sign_changes'] for c in human['curves']),0)
        a=next(j for j in ai['joins'] if j['point']==(88,952))
        h=next(j for j in human['joins'] if j['point']==(88,944))
        self.assertEqual(a['classification'],'G1')
        self.assertEqual(h['classification'],'G2')
        # Do not turn the preferred human drawing into an artificial all-G2 target.
        outer=next(j for j in human['joins'] if j['point']==(16,960))
        self.assertEqual(outer['classification'],'G1')
        self.assertIn('Same outline scale',svg([ai,human]))


if __name__=='__main__':
    unittest.main()
