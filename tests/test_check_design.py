"""Tests of the stroke and component measurements in scripts/check_design.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import check_design


class CheckDesign(unittest.TestCase):
    def test_strokes_split_by_direction_and_ignore_long_spans(self):
        analysis = {'spans': [
            {'axis': 'horizontal', 'ink': True, 'length': 96},
            {'axis': 'vertical', 'ink': True, 'length': 84},
            {'axis': 'vertical', 'ink': True, 'length': 576},
            {'axis': 'horizontal', 'ink': False, 'length': 90}]}
        self.assertEqual(check_design.strokes(analysis, 180),
                         {'vertical_stem': [96], 'horizontal_stroke': [84]})

    def test_leaves_resolve_nested_components(self):
        glyphs = {'A': {'components': [], 'contours': 1},
                  'acute': {'components': [], 'contours': 1},
                  'acutecomb': {'components': [{'base': 'acute'}], 'contours': 0},
                  'Aacute': {'components': [{'base': 'A'}, {'base': 'acutecomb'}], 'contours': 0},
                  'broken': {'components': [{'base': 'missing'}], 'contours': 0}}
        self.assertEqual(check_design.leaves('Aacute', glyphs), ['A', 'acute'])
        self.assertIsNone(check_design.leaves('broken', glyphs))


if __name__ == '__main__':
    unittest.main()
