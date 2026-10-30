"""Regression tests for the failed Seen repairs, without claiming optical grading."""
import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import construction_review as cr

class ConstructionReviewTests(unittest.TestCase):
    def setUp(self):
        self.before=ROOT/'design/reviews/arabic-006/seen-2026-10-29/revision3/Bold.glif'
        self.rules=[{'kind':'straight_run','contour':0,'start':41,'end':42,'axis':'x','min_length':128,
                     'reason':'Test fixture only: preserve an upright first-tooth run, not an approved universal threshold'}]
    def test_unchanged_passes_structure_only(self):
        self.assertEqual(cr.check_pair(self.before,self.before,self.rules),[])
    def test_v6_bent_tooth_is_caught(self):
        candidate=ROOT/'design/reviews/arabic-006/seen-2026-10-29/revision6/Bold.glif'
        self.assertTrue(any('shorter' in s for s in cr.check_pair(self.before,candidate,self.rules)))
    def test_v4_topology_requires_remapping(self):
        candidate=ROOT/'design/reviews/arabic-006/seen-2026-10-29/revision4/Bold.glif'
        self.assertIn('correspondence',cr.check_pair(self.before,candidate,self.rules)[0])
    def test_empty_constraints_do_not_pass(self):
        self.assertTrue(cr.check_pair(self.before,self.before,[]))
    def test_source_hash_guard(self):
        plan={'items':[{'path':str(self.before.relative_to(ROOT)),'sha256':'bad','label':'x','role':'x'}]}
        with self.assertRaisesRegex(ValueError,'Stale'):cr.render(ROOT,plan)
    def test_html_escapes_annotations(self):
        plan={'diagnosis':'<script>bad</script>','items':[]}
        self.assertNotIn('<script>',cr.render(ROOT,plan))
    def test_indexed_svg(self):
        s=cr.svg(self.before)
        self.assertIn('41',s);self.assertIn('viewBox="-64 -900 1728 1300"',s)

if __name__=='__main__':unittest.main()
