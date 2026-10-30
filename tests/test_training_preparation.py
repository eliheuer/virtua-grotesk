import contextlib,importlib.util,io,json,math,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
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

class TokenizerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  path=Path(os.environ.get('VIRTUA_TOKENIZER','/Users/eli/GH/repos/font-garden-lab/glyphlab/tokenizer.py'))
  if not path.exists():raise unittest.SkipTest('Set VIRTUA_TOKENIZER to the lab tokenizer')
  spec=importlib.util.spec_from_file_location('tested_tokenizer',path);cls.tk=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.tk)
 def test_coordinate_no_clipping(self):
  for x in (-513,1281,1408,1504,float('nan'),float('inf')):
   with self.assertRaises(ValueError):self.tk.snap(x)
 def test_valid_ids_unchanged(self):
  v=self.tk.Vocab(['H'],[72])
  for x in range(-512,1281,2):
   self.assertEqual(v.coord(x),v.coord_base+(x+512)//2);self.assertEqual(v.coord_value(v.coord(x)),x)
 def test_delta_no_clipping_or_unicode_decode(self):
  v=self.tk.Vocab(['H'],[72])
  for x in (-385,385,float('nan')):
   with self.assertRaises(ValueError):v.delta(x)
  for x in range(-384,385,2):self.assertEqual(v.delta_value(v.delta(x)),x)
  self.assertIsNone(v.delta_value(v.uni(72)))
if __name__=='__main__':unittest.main()
