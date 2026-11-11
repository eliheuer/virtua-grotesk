"""Tests of the curvature and join measurements in scripts/curve_lint.py."""
import math
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from curve_lint import all_segments, inflections, join_audit, lint_glyph, parse, signed_curvature

KAPPA = 276  # Handle length of a quarter circle with radius 500.


def circle(right_handle=KAPPA, pull=0):
    """GLIF text of a circle of four arcs, with two optional faults.

    right_handle shortens the first handle, so that the join at (500, 0)
    stays tangent but the curvature changes. pull moves the last handle
    inside the circle, so that the last arc inflects.
    """
    c = KAPPA
    points = [
        (500, 0, 'curve'), (500 + right_handle, 0, None), (1000, 500 - c, None),
        (1000, 500, 'curve'), (1000, 500 + c, None), (500 + c, 1000, None),
        (500, 1000, 'curve'), (500 - c, 1000, None), (0, 500 + c, None),
        (0, 500, 'curve'), (0, 500 - c, None), (500 - c + pull, pull, None),
    ]
    rows = ''.join(f'<point x="{x}" y="{y}"' + (f' type="{t}" smooth="yes"' if t else '') + '/>'
                   for x, y, t in points)
    return f'<glyph><outline><contour>{rows}</contour></outline></glyph>'


class Curvature(unittest.TestCase):
    def test_a_straight_segment_has_zero_curvature(self):
        for t in (0, .25, .5, .75, 1):
            self.assertEqual(signed_curvature((0, 0), (1, 0), (2, 0), (3, 0), t), 0)

    def test_a_quarter_circle_has_equal_curvature_at_both_ends(self):
        h = 4 / 3 * math.tan(math.pi / 8)
        arc = ((1, 0), (1, h), (h, 1), (0, 1))
        self.assertAlmostEqual(signed_curvature(*arc, 0), 2 * (1 - h) / (3 * h * h))
        self.assertAlmostEqual(signed_curvature(*arc, 0), signed_curvature(*arc, 1))

    def test_a_zero_length_handle_has_no_curvature(self):
        self.assertIsNone(signed_curvature((0, 0), (0, 0), (1, 1), (2, 1), 0))

    def test_an_s_curve_has_one_inflection(self):
        self.assertEqual(inflections((0, 0), (1, 1), (2, -1), (3, 0)), 1)
        self.assertEqual(inflections((1, 0), (1, .55), (.55, 1), (0, 1)), 0)


class Glyphs(unittest.TestCase):
    def joins(self, text):
        return {row['point']: row['classification'] for row in join_audit(parse(text))}

    def test_a_circle_has_curvature_continuous_joins(self):
        self.assertEqual(set(self.joins(circle()).values()), {'G2'})

    def test_unequal_handles_make_a_tangent_only_join(self):
        self.assertEqual(self.joins(circle(right_handle=200))[(500, 0)], 'G1')

    def test_lint_reports_an_inflection_only_in_the_dented_circle(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.glif'
            path.write_text(circle())
            self.assertEqual(lint_glyph(path, 'circle'), [])
            path.write_text(circle(pull=300))
            self.assertTrue(any('inflection' in issue for issue in lint_glyph(path, 'circle')))


if __name__ == '__main__':
    unittest.main()
