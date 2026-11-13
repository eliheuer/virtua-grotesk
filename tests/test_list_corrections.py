"""Tests of the review classification in scripts/list_corrections.py."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import list_corrections as corrections

PURPLE, GREEN, YELLOW, ORANGE = '0.54,0.44,0.88,1', '0,1,0,1', '1,1,0,1', '1,0.5,0,1'


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
    def test_the_new_mark_of_a_purple_draft_is_the_grade(self):
        self.assertEqual(corrections.grade(glif(PURPLE), glif(ORANGE)), 'orange')
        self.assertEqual(corrections.grade(glif(PURPLE), glif(GREEN)), 'green')

    def test_a_change_that_keeps_or_never_had_purple_is_not_a_review(self):
        self.assertIsNone(corrections.grade(glif(PURPLE), glif(PURPLE, right=150)))
        self.assertIsNone(corrections.grade(glif(ORANGE), glif(GREEN)))

    def test_the_same_outline_is_accepted(self):
        row = corrections.outcome(glif(PURPLE), glif(GREEN))
        self.assertEqual((row['result'], row['iou']), ('accepted', 1.0))

    def test_another_outline_or_advance_is_corrected(self):
        row = corrections.outcome(glif(PURPLE), glif(GREEN, right=150))
        self.assertEqual(row['result'], 'corrected')
        self.assertLess(row['iou'], 1.0)
        self.assertEqual(corrections.outcome(glif(PURPLE), glif(GREEN, advance=220))['result'],
                         'corrected')


class History(unittest.TestCase):
    def test_a_yellow_draft_is_compared_with_its_later_green_version_and_cited(self):
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
            correction = commit('Grade yellow', glif(YELLOW, right=120))
            [row] = corrections.reviews(root)
            self.assertEqual((row['grade'], row['against'], row['result']),
                             ('yellow', 'yellow', 'corrected'))
            commit('Redraft', glif(PURPLE, right=100))
            commit('Approve', glif(GREEN, right=150))
            first, second = corrections.reviews(root)
            self.assertEqual((first['commit'], first['glyph'], first['against']),
                             (correction, 'square', 'green'))
            self.assertAlmostEqual(first['iou'], 2 / 3, delta=0.03)
            self.assertEqual((second['grade'], second['against']), ('green', 'green'))
            self.assertNotIn(correction[:7], corrections.citations(root))
            commit(f'Add a rule entry from {correction[:8]}')
            self.assertIn(correction[:7], corrections.citations(root))


if __name__ == '__main__':
    unittest.main()
