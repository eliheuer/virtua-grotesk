"""Safety checks for fixed-checkpoint evaluation; no training occurs in tests."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import evaluate_masked_pilot as ev
import masked_repair as mr


class EvaluationTests(unittest.TestCase):
    def record(self, count=5):
        return {'glyph':'fixture','master':'Regular','group':'holdout','source_sha256':'fixture',
                'advance':512,'contours':[[{'x':str(64+i*8),'y':'128','type':'line'} for i in range(count)]]}

    def recipe(self):
        return {'outer':[(0,1)],'inner':[(0,3)]}

    def test_corruptions_preserve_targets_and_locked_points(self):
        for mode in ev.VARIANTS:
            original=self.record();before=copy.deepcopy(original)
            ex=ev.make_example(original,self.recipe(),mode,'validation')
            self.assertEqual(original,before)
            self.assertEqual(ex['target'],before)
            recovered=mr.reconstruct(ex,ex['target_deltas'])
            self.assertEqual([[float(p[a]) for a in ('x','y')] for _,_,p in mr.flatten(recovered)],
                             [[float(p[a]) for a in ('x','y')] for _,_,p in mr.flatten(original)])
            for i in (0,2,4):
                self.assertEqual(ex['coordinates'][i],[64+i*8,128])
            self.assertEqual(ex['cohort'],'heldout-hah')

    def test_no_target_features_and_exact_padding(self):
        ex=ev.make_example(self.record(),self.recipe(),'paired-y-plus16','validation')
        features=ev.input_tensor(ex,36)
        altered=copy.deepcopy(ex)
        altered['target']['contours'][0][0]['x']='1000'
        altered['target_deltas']=[[64,64]]*5
        self.assertTrue(features.eq(ev.input_tensor(altered,36)).all())
        self.assertEqual(tuple(features.shape),(1,288))
        self.assertTrue(features[0,40:].eq(0).all())

    def test_long_glyphs_refused_without_truncation(self):
        for count in (44,50):
            ex=ev.make_example(self.record(count),self.recipe(),'noop','validation')
            with self.assertRaisesRegex(ValueError,'no truncation'):
                ev.input_tensor(ex,36)
            self.assertEqual(len(ex['coordinates']),count)


if __name__=='__main__':unittest.main()
