"""Tests of scripts/build_source_snapshot.py.

The build copies the sources to a temporary folder and gives every master the
glyph order of the first master. The sources themselves must not change.
"""
from pathlib import Path
import plistlib
import tempfile
import unittest

from scripts.build_source_snapshot import build_snapshot


def write_sources(folder):
    """Two masters with different glyph orders."""
    (folder / 'config.yaml').write_text('sources: [Test.designspace]\noutputDir: ../fonts\n')
    (folder / 'Test.designspace').write_text(
        '<designspace><sources><source filename="Regular.ufo"/>'
        '<source filename="Bold.ufo"/></sources></designspace>')
    for name, order in (('Regular', ['b', 'a']), ('Bold', ['a', 'b'])):
        ufo = folder / f'{name}.ufo'
        (ufo / 'glyphs').mkdir(parents=True)
        (ufo / 'lib.plist').write_bytes(plistlib.dumps({'public.glyphOrder': order, 'other': 'kept'}))
        (ufo / 'glyphs/contents.plist').write_bytes(plistlib.dumps({'a': 'a.glif', 'b': 'b.glif'}))
        (ufo / 'glyphs/a.glif').write_text('glyph bytes')


def contents(folder):
    return {str(p.relative_to(folder)): p.read_bytes() for p in folder.rglob('*') if p.is_file()}


class BuildSourceSnapshotTests(unittest.TestCase):
    def test_the_snapshot_has_one_glyph_order_and_the_sources_do_not_change(self):
        with tempfile.TemporaryDirectory() as temp:
            sources = Path(temp) / 'sources'
            sources.mkdir()
            write_sources(sources)
            before = contents(sources)
            with build_snapshot(sources / 'config.yaml') as config:
                snapshot = config.parent
                for name in ('Regular', 'Bold'):
                    ufo = snapshot / f'{name}.ufo'
                    lib = plistlib.loads((ufo / 'lib.plist').read_bytes())
                    self.assertEqual(lib['public.glyphOrder'], ['b', 'a'])
                    self.assertEqual(lib['other'], 'kept')
                    self.assertEqual((ufo / 'glyphs/a.glif').read_text(), 'glyph bytes')
            self.assertFalse(snapshot.exists())
            self.assertEqual(contents(sources), before)

    def test_a_source_outside_the_folder_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            sources = Path(temp)
            (sources / 'config.yaml').write_text('sources: [Test.designspace]\n')
            (sources / 'Test.designspace').write_text(
                '<designspace><sources><source filename="../outside.ufo"/></sources></designspace>')
            with self.assertRaises(ValueError):
                with build_snapshot(sources / 'config.yaml'):
                    pass


if __name__ == '__main__':
    unittest.main()
