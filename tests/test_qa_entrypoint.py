"""Check release/development separation without running network checks."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QaEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        # A standalone runner fixture needs only expected inputs and a Git HEAD.
        (self.work / 'scripts').mkdir()
        (self.work / 'scripts/check_gf_fonts.sh').write_bytes(
            (ROOT / 'scripts/check_gf_fonts.sh').read_bytes())
        subprocess.run(['git', 'init', '-q', str(self.work)], check=True)
        subprocess.run(['git', '-c', 'user.name=QA Test', '-c',
                        'user.email=qa@example.invalid', 'commit', '-q',
                        '--allow-empty', '-m', 'fixture'], cwd=self.work, check=True)
        paths = ['fonts/variable/VirtuaGrotesk[wght].ttf'] + [
            f'fonts/ttf/VirtuaGrotesk-{style}.ttf'
            for style in ['Regular', 'Medium', 'SemiBold', 'Bold']]
        for name in paths:
            p = self.work / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
        self.capture = self.work / 'arguments.txt'
        self.tool = self.work / 'fontspector'
        self.tool.write_text('''#!/bin/sh
if [ "$1" = --version ]; then echo fixture; exit 0; fi
printf '%s\\n' "$@" > "$CAPTURE_FILE"
exit "${FIXTURE_EXIT:-0}"
''')
        self.tool.chmod(0o755)

    def run_qa(self, *args, exit_code=0):
        env = dict(os.environ, FONTSPECTOR=str(self.tool),
                   QA_REPORT_DIR=str(self.work / 'report'),
                   CAPTURE_FILE=str(self.capture), FIXTURE_EXIT=str(exit_code),
                   QA_NETWORK='online')
        result = subprocess.run(['bash', 'scripts/check_gf_fonts.sh', *args],
                                cwd=self.work, env=env, capture_output=True)
        captured = self.capture.read_text().splitlines() if self.capture.exists() else []
        return result.returncode, captured

    def test_development_is_explicitly_offline_and_excluded(self):
        code, args = self.run_qa('development')
        self.assertEqual(code, 0)
        self.assertEqual(args.count('--exclude-checkid'), 4)
        self.assertIn('--skip-network', args)

    def test_full_qa_has_no_exclusions_and_preserves_failure(self):
        code, args = self.run_qa('full', exit_code=1)
        self.assertEqual(code, 1)
        self.assertNotIn('--exclude-checkid', args)
        self.assertNotIn('--skip-network', args)
        self.assertEqual(args[args.index('--error-code-on') + 1], 'fail')

    def test_package_qa_includes_non_font_inputs(self):
        package = self.work / 'ofl/virtuagrotesk'
        for name in ['METADATA.pb', 'OFL.txt', 'article/ARTICLE.en_us.html', 'Font.ttf']:
            p = package / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
        code, args = self.run_qa('package', str(package))
        self.assertEqual(code, 0)
        self.assertNotIn('--exclude-checkid', args)
        for name in ['METADATA.pb', 'OFL.txt', 'article/ARTICLE.en_us.html']:
            self.assertIn(str(package / name), args)

    def test_missing_package_fails_before_tool_runs(self):
        code, args = self.run_qa('package', str(self.work / 'missing'))
        self.assertEqual(code, 2)
        self.assertEqual(args, [])


if __name__ == '__main__':
    unittest.main()
