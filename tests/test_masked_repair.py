import copy,json,sys,unittest,tempfile
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import masked_repair as mr

class MaskedRepairTests(unittest.TestCase):
 def record(self):
  # Tiny independent paired-boundary fixture with a locked terminal.
  return {'glyph':'fixture','master':'Regular','group':'g','source_sha256':'fixture','advance':512,
   'contours':[[{'x':'64','y':'0','type':'line'},{'x':'128','y':'0','type':'curve'},{'x':'192','y':'128','type':'line'}]]}
 def recipe(self):return {'outer':[(0,0)],'inner':[(0,1)],'axis':0,'description':'fixture'}
 def coords(self,r):return [[float(p[a]) for a in ('x','y')] for _,_,p in mr.flatten(r)]
 def test_exact_recovery_and_protected_points(self):
  for mode in ('noop','pinch','bulge'):
   r=self.record();e=mr.example(r,self.recipe(),mode);restored=mr.reconstruct(e,e['target_deltas'])
   self.assertEqual(self.coords(restored),self.coords(r));self.assertEqual(restored['advance'],r['advance'])
   self.assertEqual(e['input']['contours'][0][2],r['contours'][0][2])
   self.assertEqual([p.get('type') for _,_,p in mr.flatten(restored)],[p.get('type') for _,_,p in mr.flatten(r)])
 def test_noop_has_zero_residual(self):
  e=mr.example(self.record(),self.recipe(),'noop');self.assertEqual(e['target_deltas'],[[0,0]]*3)
 def test_predicted_locked_change_is_refused(self):
  e=mr.example(self.record(),self.recipe(),'pinch');d=copy.deepcopy(e['target_deltas']);d[2][0]=8
  with self.assertRaisesRegex(ValueError,'Locked'):mr.reconstruct(e,d)
 def test_bounds_nonfinite_and_grid(self):
  e=mr.example(self.record(),self.recipe(),'pinch')
  for v in (65,1,float('nan'),float('inf')):
   ds=copy.deepcopy(e['target_deltas']);ds[0][0]=v
   with self.assertRaises(ValueError):mr.reconstruct(e,ds)
  r=self.record();r['advance']=2050
  with self.assertRaises(ValueError):mr.example(r,self.recipe(),'noop')
 def test_no_bold_or_bad_correspondence(self):
  r=self.record();r['master']='Bold'
  with self.assertRaises(ValueError):mr.example(r,self.recipe(),'noop')
  recipe=self.recipe();recipe['inner']=[(0,7)]
  with self.assertRaises(ValueError):mr.example(self.record(),recipe,'noop')
 def test_padding_has_no_loss_and_features_do_not_read_targets(self):
  a=mr.example(self.record(),self.recipe(),'pinch');r=self.record();r['contours'][0].append({'x':'256','y':'128','type':'line'});b=mr.example(r,self.recipe(),'bulge')
  batch=mr.collate([a,b]);self.assertEqual(batch['attention_mask'][0],[1,1,1,0]);self.assertEqual(batch['loss_mask'][0],[1,1,0,0]);self.assertEqual(batch['loss_mask'][1],[1,1,0,0])
  c=copy.deepcopy(a);c['target']['contours'][0][0]['x']='1000';c['target_deltas'][0]=[32,32]
  self.assertEqual(mr.collate([a])['features'],mr.collate([c])['features'])

 def test_missing_train_recipe_refused_before_output(self):
  with tempfile.TemporaryDirectory() as d, patch.object(mr,'load_split',return_value=[]):
   out=Path(d)/'sample'
   with self.assertRaisesRegex(ValueError,'TRAIN Regular'):mr.prepare('snapshot','hash',out)
   self.assertFalse(out.exists())

if __name__=='__main__':unittest.main()
