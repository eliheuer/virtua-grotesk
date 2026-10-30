"""Server reuse must identify this project, directory and implementation."""
import importlib.util
import io
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch
from urllib.error import URLError

spec = importlib.util.spec_from_file_location('proof_serve', Path(__file__).parents[1]/'serve.py')
serve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(serve)


class ServerIdentityTest(unittest.TestCase):
    def test_explicit_and_remembered_snapshot_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            selection = Path(temp)/'selection.json'
            with patch.object(serve, 'SELECTION', selection):
                state = json.loads(serve.STATE.read_text())
                self.assertEqual(serve.selected_snapshot(), (serve.ROOT / state['proof_snapshot']).resolve())
                # State changes must be read anew, not captured in a module constant.
                state_file = Path(temp)/'current.json'
                state_file.write_text(json.dumps({'proof_snapshot': 'another/proof'}))
                with patch.object(serve, 'STATE', state_file):
                    self.assertEqual(serve.selected_snapshot(), (serve.ROOT/'another/proof').resolve())
                selection.write_text(json.dumps({'snapshot': temp}))
                self.assertEqual(serve.selected_snapshot(), Path(temp).resolve())
                self.assertEqual(serve.selected_snapshot(Path('/tmp/explicit')), Path('/tmp/explicit').resolve())

    def test_reuses_only_matching_server_and_fonts(self):
        identity = serve.server_identity(Path('/tmp/live'), True)
        fonts = {'before': {'sha256': 'frozen'}}
        def responses(other_identity, other_fonts):
            return [io.BytesIO(json.dumps(item).encode()) for item in (other_identity, other_fonts)]
        with patch.object(serve, 'urlopen', side_effect=responses(identity, fonts)):
            self.assertTrue(serve.matching_server('http://localhost/', fonts, identity))
        for key, value in [('project', '/other'), ('directory', '/archive'), ('live', False), ('implementation', 'older')]:
            with self.subTest(key=key), patch.object(serve, 'urlopen', side_effect=responses({**identity, key: value}, fonts)):
                self.assertFalse(serve.matching_server('http://localhost/', fonts, identity))
        with patch.object(serve, 'urlopen', side_effect=responses(identity, {})):
            self.assertFalse(serve.matching_server('http://localhost/', fonts, identity))

    def test_old_or_unavailable_server_is_not_reused(self):
        for response in [URLError('unavailable'), io.BytesIO(b'<html>old server</html>')]:
            with self.subTest(response=response):
                kwargs = {'side_effect': response} if isinstance(response, Exception) else {'return_value': response}
                with patch.object(serve, 'urlopen', **kwargs):
                    self.assertFalse(serve.matching_server('http://localhost/', {}, {}))


if __name__ == '__main__':
    unittest.main()
