"""Tests of the review classification in scripts/list_corrections.py."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import list_corrections as corrections

PURPLE, GREEN, ORANGE = '0.54,0.44,0.88,1', '0,1,0,1', '1,0.5,0,1'


def glif(mark, right=100, advance=200):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<glyph name="square" format="2">
	<advance width="{advance}"/>
	<outline>
		<contour>
			<point x="0" y="0" type="line"/>
			<point x="{right}" y="0" type="line"/>
			<point x="{right}" y="100" type="line"/>
			<point x="0" y="100" type="line"/>
		</contour>
	</outline>
	<lib>
		<dict>
			<key>public.markColor</key>
			<string>{mark}</string>
		</dict>
	</lib>
</glyph>
'''


class Review(unittest.TestCase):
    def test_green_with_the_same_outline_is_accepted(self):
        result = corrections.review(glif(PURPLE), glif(GREEN))
        self.assertEqual((result['result'], result['iou']), ('accepted', 1.0))

    def test_green_with_another_outline_is_corrected(self):
        result = corrections.review(glif(PURPLE), glif(GREEN, right=150))
        self.assertEqual(result['result'], 'corrected')
        self.assertLess(result['iou'], 1.0)

    def test_green_with_another_advance_is_corrected(self):
        result = corrections.review(glif(PURPLE), glif(GREEN, advance=220))
        self.assertEqual(result['result'], 'corrected')

    def test_another_mark_is_a_grade(self):
        self.assertEqual(corrections.review(glif(PURPLE), glif(ORANGE))['result'], 'orange')

    def test_a_change_that_keeps_or_never_had_purple_is_not_a_review(self):
        self.assertIsNone(corrections.review(glif(PURPLE), glif(PURPLE, right=150)))
        self.assertIsNone(corrections.review(glif(ORANGE), glif(GREEN)))


class History(unittest.TestCase):
    def test_a_correction_is_open_until_a_commit_cites_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / 'sources/VirtuaGrotesk-Regular.ufo/glyphs/square.glif'
            path.parent.mkdir(parents=True)

            def commit(message, text=None):
                if text:
                    path.write_text(text)
                subprocess.run(['git', 'add', '-A'], cwd=root, check=True)
                subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                                'commit', '-q', '--allow-empty', '-m', message], cwd=root, check=True)
                return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, check=True,
                                      capture_output=True, text=True).stdout.strip()

            subprocess.run(['git', 'init', '-q'], cwd=root, check=True)
            commit('Draft', glif(PURPLE))
            correction = commit('Correct', glif(GREEN, right=150))
            [row] = corrections.reviews(root)
            self.assertEqual((row['commit'], row['glyph'], row['result']),
                             (correction, 'square', 'corrected'))
            self.assertNotIn(correction[:7], corrections.citations(root))
            commit(f'Add a rule entry from {correction[:8]}')
            self.assertIn(correction[:7], corrections.citations(root))


if __name__ == '__main__':
    unittest.main()
