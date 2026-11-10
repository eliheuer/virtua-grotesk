import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import benchmark
import check_design

SQUARE = [(0, 0), (100, 0), (100, 100), (0, 100)]


def glyph(contours, advance=200):
    points = [p for c in contours for p in c]
    return dict(advance=advance, contours=contours, points=points,
                structure=[['line'] * len(c) for c in contours])


class Benchmark(unittest.TestCase):
    def test_identical_outlines_score_as_identical(self):
        row = benchmark.compare(glyph([SQUARE]), glyph([SQUARE]))
        self.assertEqual((row['iou'], row['distance'], row['moved']), (1.0, 0.0, '0 of 4'))

    def test_a_shifted_outline_loses_overlap_and_reports_moved_points(self):
        shifted = [(x + 50, y) for x, y in SQUARE]
        row = benchmark.compare(glyph([SQUARE]), glyph([shifted], advance=240))
        self.assertAlmostEqual(row['iou'], 1 / 3, delta=0.05)
        self.assertEqual((row['moved'], row['advance']), ('4 of 4', 40))

    def test_an_empty_candidate_scores_zero(self):
        row = benchmark.compare(glyph([SQUARE]), glyph([]))
        self.assertEqual((row['iou'], row['moved']), (0.0, 'no outline'))

    def test_cases_are_green_in_the_sources(self):
        import json
        import source_inventory
        contract = json.loads(check_design.CONTRACT.read_text())
        data = {m: source_inventory.load_master(check_design.ROOT, m, contract)
                for m in check_design.MASTERS}
        for case in benchmark.cases():
            record = data[case['master']][case['glyph']]
            self.assertEqual(record['color']['name'], 'green', case)


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
