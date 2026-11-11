import contextlib,importlib.util,io,json,math,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'models/arabic-repair-hour-v1'))
import prepare_green_dataset as prep
import frozen_green_dataset as frozen
import hashlib

class DatasetTests(unittest.TestCase):
 def test_frozen_green_split_and_no_source_writes(self):
  with tempfile.TemporaryDirectory() as t,contextlib.redirect_stdout(io.StringIO()):
   a=prep.build(ROOT,Path(t)/'a');b=prep.build(ROOT,Path(t)/'b')
   self.assertEqual(a,b)
   groups={}
   for r in a['rows']:
    self.assertTrue(r['color']['reference_eligible']);self.assertEqual(r['off_2_points'],0)
    self.assertEqual(prep.dc.digest(Path(t)/'a'/r['path']),r['sha256'])
    self.assertEqual(groups.setdefault(r['group'],r['split']),r['split'])
   for path,digest in a['source_guards'].items():self.assertEqual(prep.dc.digest(ROOT/path),digest)
   self.assertFalse(a['training_authorized'])
   arabic=[r for r in a['rows'] if '-ar' in r['glyph']]
   self.assertEqual({r['split'] for r in arabic},{'train','validation','test'})
   self.assertTrue(all(r['glyph'] not in a['policy']['shared_marks'] for r in a['rows']))
   self.assertTrue(all(r['split']=='test' for r in arabic if r['glyph'].startswith('seen-ar')))
   self.assertTrue(all(r['split']=='validation' for r in arabic if r['glyph'].startswith('hah-ar')))
   sha=hashlib.sha256((Path(t)/'a/manifest.json').read_bytes()).hexdigest()
   self.assertEqual(len(frozen.load_split(Path(t)/'a',sha,'train')),sum(r['split']=='train' for r in a['rows']))
   first=Path(t)/'a'/a['rows'][0]['path'];first.write_text(first.read_text()+' ')
   with self.assertRaisesRegex(ValueError,'identity mismatch'):frozen.load_split(Path(t)/'a',sha,'train')
   with self.assertRaises(ValueError):prep.build(ROOT,Path(t)/'a')

if __name__=='__main__':unittest.main()
