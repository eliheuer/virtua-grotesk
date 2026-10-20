"""The draft gate must inspect handles and true curve bounds, not just nodes."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from draft_grid_check import inspect_glif


def glyph(points, width=128, anchor=''):
    return f'<glyph name="test" format="2"><advance width="{width}"/>{anchor}<outline><contour>{points}</contour></outline></glyph>'


RECT = '<point x="16" y="0" type="line"/><point x="112" y="0" type="line"/><point x="112" y="64" type="line"/><point x="16" y="64" type="line"/>'


class DraftGridTests(unittest.TestCase):
    def test_clean_and_high_popcount_measurements_pass(self):
        result = inspect_glif(glyph(RECT, width=248))
        self.assertTrue(result['passed'])
        self.assertEqual(result['measurements'][0]['popcount'], 5)

    def test_off_grid_width_and_anchor_fail(self):
        result = inspect_glif(glyph(RECT, 130, '<anchor name="top" x="66" y="64"/>'))
        self.assertEqual({f['field'] for f in result['failures']},
                         {'advance.width', 'anchor[top].x', 'right_sidebearing'})

    def test_off_grid_handle_fails(self):
        points = '<point x="16" y="0" type="line"/><point x="16" y="62"/><point x="112" y="64"/><point x="112" y="0" type="curve"/>'
        self.assertIn('contour[0].point[1].y', [f['field'] for f in inspect_glif(glyph(points))['failures']])

    def test_actual_curve_extremum_not_control_box(self):
        points = '<point x="16" y="0" type="line"/><point x="24" y="0"/><point x="24" y="64"/><point x="16" y="64" type="curve"/>'
        result = inspect_glif(glyph(points))
        self.assertEqual(result['bounds'][2], 22)
        self.assertEqual(result['failures'], [{'field': 'right_sidebearing', 'value': 106.0}])

    def test_off_grid_oncurve_fails(self):
        self.assertFalse(inspect_glif(glyph(RECT.replace('x="16"', 'x="18"')))['passed'])


if __name__ == '__main__':
    unittest.main()
