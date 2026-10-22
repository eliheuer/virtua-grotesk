"""Build snapshots normalize ordering without saving editor-owned sources."""
import tempfile
from pathlib import Path
import plistlib
import unittest
from scripts.build_source_snapshot import build_snapshot

class BuildSourceSnapshotTests(unittest.TestCase):
    def test_order_normalization_is_temporary_and_other_bytes_are_exact(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);src=root/'sources';src.mkdir()
            (src/'config.yaml').write_text('sources: [Test.designspace]\noutputDir: ../fonts\n')
            (src/'Test.designspace').write_text('<designspace><sources><source filename="Regular.ufo"/><source filename="Bold.ufo"/></sources></designspace>')
            for name,order in [('Regular',['b','a']),('Bold',['a','b'])]:
                d=src/(name+'.ufo');(d/'glyphs').mkdir(parents=True)
                (d/'lib.plist').write_bytes(plistlib.dumps({'public.glyphOrder':order,'private':'preserve'}))
                (d/'glyphs/contents.plist').write_bytes(plistlib.dumps({'a':'a.glif','b':'b.glif'}))
                (d/'glyphs/a.glif').write_text('exact human bytes')
            original={str(p.relative_to(src)):p.read_bytes() for p in src.rglob('*') if p.is_file()}
            with build_snapshot(src/'config.yaml') as copied:
                snapshot=copied.parent
                for name in ['Regular','Bold']:
                    lib=plistlib.loads((snapshot/(name+'.ufo')/'lib.plist').read_bytes())
                    self.assertEqual(lib['public.glyphOrder'],['b','a'])
                    self.assertEqual(lib['private'],'preserve')
                    self.assertEqual((snapshot/(name+'.ufo')/'glyphs/a.glif').read_text(),'exact human bytes')
                self.assertTrue(snapshot.exists())
            self.assertFalse(snapshot.exists())
            self.assertEqual(original,{str(p.relative_to(src)):p.read_bytes() for p in src.rglob('*') if p.is_file()})

    def test_rejects_sources_outside_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            src=Path(td);(src/'config.yaml').write_text('sources: [Test.designspace]\n')
            (src/'Test.designspace').write_text('<designspace><sources><source filename="../outside.ufo"/></sources></designspace>')
            with self.assertRaises(ValueError):
                with build_snapshot(src/'config.yaml'):pass
