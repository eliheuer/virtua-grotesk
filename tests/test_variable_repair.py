import copy
import sys
import unittest
from pathlib import Path
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import variable_repair as vr

class VariableRepairTests(unittest.TestCase):
 def example(self,n):
  r={'glyph':'fixture','master':'Regular','group':'fixture','source_sha256':'fixture','advance':704,
     'contours':[[{'x':str((i%100)*8),'y':str((i%3)*16),'type':'line'} for i in range(n)]]}
  return vr.make_example(r,set(range(n)),{},'noop','test')
 def test_full_lengths_and_padding_invariance(self):
  torch.manual_seed(4);model=vr.VariableRepair().eval()
  torch.nn.init.normal_(model.head[-1].weight,std=.01)
  short=self.example(33);long=self.example(68)
  a=vr.collate([short]);b=vr.collate([short,long])
  with torch.no_grad():one=model(*a[:5])[0];mixed=model(*b[:5])
  self.assertEqual(tuple(mixed.shape),(2,68,2))
  self.assertTrue(torch.allclose(one,mixed[0,:33],atol=1e-5))
  self.assertTrue(mixed[0,33:].eq(0).all())
  for n in (44,50):self.assertEqual(len(vr.features(self.example(n))[0]),n)
 def test_no_target_leak_and_locked_mask(self):
  e=self.example(50);other=copy.deepcopy(e);other['target']['advance']=1000;other['target_deltas']=[[32,32]]*50
  self.assertEqual(vr.features(e),vr.features(other))
  e['editable_mask']=[0]*50;args=vr.collate([e]);model=vr.VariableRepair()
  torch.nn.init.normal_(model.head[-1].weight)
  self.assertTrue(model(*args[:5]).eq(0).all())
 def test_no_point_truncation(self):
  with self.assertRaisesRegex(ValueError,'no truncation'):vr.features(self.example(513))
 def test_corruptions_roundtrip_and_keep_optical_targets(self):
  import random
  import masked_repair as mr
  r=self.example(12)['target']
  for i,p in enumerate(r['contours'][0]):
   if i%3:p.pop('type')
  before=copy.deepcopy(r)
  for mode in ('noop','single','cluster','paired-x','paired-y','jitter'):
   e=vr.synthetic(r,random.Random(11),mode)
   self.assertEqual(e['target'],before);self.assertEqual(r,before)
   restored=mr.reconstruct(e,e['target_deltas'])
   coords=lambda a:[[float(p[k]) for k in ('x','y')] for _,_,p in mr.flatten(a)]
   self.assertEqual(coords(restored),coords(before))
if __name__=='__main__':unittest.main()
