import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import check_design
import evaluate_drafting as evaluation

SQUARE = [(0, 0), (100, 0), (100, 100), (0, 100)]


def glyph(contours, advance=200):
    points = [p for c in contours for p in c]
    return dict(advance=advance, contours=contours, points=points,
                structure=[['line'] * len(c) for c in contours])


class DraftingEvaluation(unittest.TestCase):
    def test_identical_outlines_score_as_identical(self):
        row = evaluation.compare(glyph([SQUARE]), glyph([SQUARE]))
        self.assertEqual((row['iou'], row['distance'], row['moved']), (1.0, 0.0, '0 of 4'))

    def test_a_shifted_outline_loses_overlap_and_reports_moved_points(self):
        shifted = [(x + 50, y) for x, y in SQUARE]
        row = evaluation.compare(glyph([SQUARE]), glyph([shifted], advance=240))
        self.assertAlmostEqual(row['iou'], 1 / 3, delta=0.05)
        self.assertEqual((row['moved'], row['advance']), ('4 of 4', 40))

    def test_an_empty_candidate_scores_zero(self):
        row = evaluation.compare(glyph([SQUARE]), glyph([]))
        self.assertEqual((row['iou'], row['moved']), (0.0, 'no outline'))

    def test_every_case_is_green_where_it_is_scored(self):
        green = evaluation.green_masters()
        for task in evaluation.TASKS:
            for case in evaluation.cases(task):
                with self.subTest(task=task, glyph=case['glyph']):
                    self.assertTrue(case['scored'])
                    if task == 'bold':
                        self.assertIn('Regular', green[case['glyph']])
                    targets = {c['glyph'] for c in evaluation.cases(task)}
                    for donor in case['donors']:
                        self.assertNotIn(donor, targets)
                        self.assertTrue(set(green.get(donor, [])) >= set(case['scored']), donor)

    def test_prepare_sets_each_task(self):
        sources = evaluation.ROOT / 'sources'
        with tempfile.TemporaryDirectory() as temp:
            for task in evaluation.TASKS:
                run = Path(temp) / task
                with contextlib.redirect_stdout(io.StringIO()):
                    evaluation.prepare(task, run)
                case = evaluation.cases(task)[0]
                for master in evaluation.MASTERS:
                    with self.subTest(task=task, master=master):
                        before = evaluation.read(evaluation.glif_path(sources, master, case['glyph']))
                        after = evaluation.read(evaluation.glif_path(run / 'sources', master, case['glyph']))
                        if master not in case['changed']:
                            self.assertEqual(after, before)
                        elif task == 'repair':
                            self.assertEqual(after['structure'], before['structure'])
                            self.assertNotEqual(after['points'], before['points'])
                        else:
                            self.assertEqual((after['contours'], after['advance']), ([], 0))
                        for donor in case['donors']:
                            self.assertEqual(
                                evaluation.read(evaluation.glif_path(run / 'sources', master, donor)),
                                evaluation.read(evaluation.glif_path(sources, master, donor)))


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
