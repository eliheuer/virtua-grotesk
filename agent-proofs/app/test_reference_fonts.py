"""Run with .venv/bin/python -m unittest discover -s agent-proofs/app -p 'test_*.py'."""
from pathlib import Path
import json
import hashlib
import tempfile
import unittest
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from reference_fonts import ReferenceCache, reference_directory, prune_reference_cache, CACHE_GRACE_SECONDS


def font(path, weight=400, family='Test', italic=False, characters=(65,)):
    builder = FontBuilder(1000, isTTF=True)
    order = ['.notdef', *[f'u{cp:04X}' for cp in characters]]
    builder.setupGlyphOrder(order)
    builder.setupCharacterMap(dict(zip(characters, order[1:])))
    builder.setupGlyf({name: TTGlyphPen(None).glyph() for name in order})
    builder.setupHorizontalMetrics({name: (500, 0) for name in order})
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupOS2(usWeightClass=weight, usWidthClass=5, fsSelection=1 if italic else 0)
    builder.setupNameTable({'familyName': family, 'styleName': 'Italic' if italic else 'Regular', 'fullName':family, 'psName':family})
    builder.setupPost()
    builder.font['head'].macStyle = 2 if italic else 0
    builder.save(path)


class ReferencesTest(unittest.TestCase):
    def test_group_coverage_refresh_and_removal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder, target = root/'reference-fonts', root/'out'
            folder.mkdir()
            cache = ReferenceCache(folder, target)
            self.assertFalse(cache.get()['fonts'])
            font(folder/'regular.TTF')
            font(folder/'bold.ttf',700,characters=(65,66))
            font(folder/'italic.ttf',italic=True)
            (folder/'broken.otf').write_text('invalid')
            (folder/'ignored.txt').write_text('not a font')
            result = cache.get()
            self.assertEqual(len(result['fonts']),2)
            family = result['fonts']['reference-0']
            self.assertEqual(len(family['faces']),2)
            self.assertEqual(family['faces'][0]['codepoints'],[65,66])
            self.assertEqual(len(result['errors']),1)
            old = result['revision']
            (folder/'bold.ttf').unlink()
            self.assertNotEqual(cache.get()['revision'],old)
            self.assertEqual(len(cache.get()['fonts']['reference-0']['faces']),1)
            font(folder/'regular.TTF',500,characters=(66,))
            self.assertEqual(cache.get()['fonts']['reference-0']['faces'][0]['minWeight'],500)

    def test_root_and_no_git(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            document = root/'sources/font.ufo'
            document.mkdir(parents=True)
            self.assertEqual(reference_directory(document),root/'sources/reference-fonts')
            (root/'.git').write_text('gitdir: worktree')
            self.assertEqual(reference_directory(document),root/'reference-fonts')

    def test_duplicate_bytes_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); folder = root/'references'; folder.mkdir()
            font(folder/'a.ttf')
            (folder/'b.ttf').write_bytes((folder/'a.ttf').read_bytes())
            (folder/'cycle').symlink_to(folder,target_is_directory=True)
            cache=ReferenceCache(folder,root/'out')
            self.assertEqual(len(cache.get()['fonts']['reference-0']['faces']),1)

    def test_refresh_preserves_newly_prepared_revisions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); folder = root/'references'; folder.mkdir()
            target = root/'out'; target.mkdir()
            font(folder/'a.ttf')
            cache = ReferenceCache(folder, target, {'before': {'sha256': 'old'}})
            cache.get()
            manifest = target/'live-fonts.json'
            manifest.write_text(json.dumps({'before': {'sha256': 'new'}}))
            font(folder/'b.ttf', 700)
            cache.get()
            self.assertEqual(json.loads(manifest.read_text())['before']['sha256'], 'new')

    def test_cleanup_preserves_manifests_and_unmanaged_files(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp); folder = target/'fonts'; folder.mkdir()
            def copy(raw):
                path = folder/f'reference-{hashlib.sha256(raw).hexdigest()}.ttf'
                path.write_bytes(raw)
                return path
            old, startup, current, before = [copy(raw) for raw in (b'old', b'startup', b'current', b'before')]
            record = lambda p: {'url': f'fonts/{p.name}'}
            (target/'live-fonts.json').write_text(json.dumps({'before': record(before), 'reference': {'faces': [record(current)]}}))
            (target/'review-data.js').write_text('window.REVIEW_DATA = ' + json.dumps({'fonts': {'reference': {'faces': [record(startup)]}}}) + ';')
            unmanaged = folder/'labels.ttf'; unmanaged.write_bytes(b'labels')
            altered = copy(b'changed'); altered.write_bytes(b'human replacement')
            external = target/'outside.ttf'; external.write_bytes(b'outside')
            link = folder/f'reference-{hashlib.sha256(b"outside").hexdigest()}.ttf'; link.symlink_to(external)
            stale = {}
            self.assertEqual(prune_reference_cache(target, stale, 0), [])
            self.assertEqual(prune_reference_cache(target, stale, CACHE_GRACE_SECONDS-1), [])
            self.assertEqual(prune_reference_cache(target, stale, CACHE_GRACE_SECONDS), [old.name])
            for p in (startup, current, before, unmanaged, altered, link, external):
                self.assertTrue(p.exists(), p)
            # Returning to the current set cancels an obsolete file's grace clock.
            (target/'live-fonts.json').write_text('{}')
            prune_reference_cache(target, stale, 400)
            (target/'live-fonts.json').write_text(json.dumps({'reference': record(current)}))
            prune_reference_cache(target, stale, 500)
            self.assertNotIn(current.name, stale)
            (target/'live-fonts.json').write_text('{}')
            prune_reference_cache(target, stale, 600)
            prune_reference_cache(target, stale, 800)
            self.assertTrue(current.exists())

    def test_cleanup_fails_closed_on_incomplete_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp); (target/'fonts').mkdir()
            path = target/'fonts'/f'reference-{hashlib.sha256(b"old").hexdigest()}.ttf'
            path.write_bytes(b'old')
            (target/'live-fonts.json').write_text('{}')
            (target/'review-data.js').write_text('incomplete')
            self.assertEqual(prune_reference_cache(target, {path.name: 0}, 999), [])
            self.assertTrue(path.exists())

    def test_cleanup_runs_on_unchanged_polls_only_when_enabled(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'references').mkdir()
            cache = ReferenceCache(root/'references', root/'out')
            with patch('reference_fonts.prune_reference_cache') as prune:
                cache.get()
                prune.assert_not_called()
                cache.prune = True
                cache.get(); cache.get()
                self.assertEqual(prune.call_count, 2)

if __name__ == '__main__': unittest.main()
