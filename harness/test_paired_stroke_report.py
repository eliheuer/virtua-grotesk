import unittest
import numpy as np
from paired_stroke_report import normal_hits

class NormalHits(unittest.TestCase):
    def test_known_parallel_width(self):
        c=np.array([[0.,0],[10,0],[20,0],[30,0]])
        h=normal_hits(c,c+[0,20],.5)
        self.assertEqual(h['status'],'unique');self.assertAlmostEqual(h['hits'][0]['width'],20)
    def test_wrong_branch_not_silently_matched(self):
        c=np.array([[0.,0],[10,0],[20,0],[30,0]])
        self.assertEqual(normal_hits(c,c+[100,20],.5)['status'],'missing')
    def test_multiple_hits_are_ambiguous(self):
        c=np.array([[0.,0],[10,0],[20,0],[30,0]])
        opposite=np.array([[5.,20],[45,25],[-15,30],[25,35]])
        self.assertEqual(normal_hits(c,opposite,.5)['status'],'ambiguous')
    def test_zero_speed(self):
        self.assertEqual(normal_hits(np.zeros((4,2)),np.ones((4,2)),.5)['status'],'undefined_tangent')

if __name__=='__main__':unittest.main()
