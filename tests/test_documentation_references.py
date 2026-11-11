"""Documents must not point at files or commands that do not exist.

A stale reference is how old systems stay alive in the documentation after the
code is gone. This test reads every tracked Markdown file and checks:

- relative Markdown links resolve to a tracked file or directory;
- repository paths in backticks (`scripts/...`, `documentation/...` and the
  other top-level directories) exist;
- `make <target>` in backticks names a target in the Makefile.

A path that is only in the Git history is written without backticks, or with
the words "in the Git history", which this test skips.
"""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ('scripts/', 'documentation/', 'sources/', 'tests/', '.agents/', '.github/')
LINK = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')
CODE = re.compile(r'`([^`\s]+)`')
MAKE = re.compile(r'`make ([a-z][a-z0-9-]*)')
HISTORY = re.compile(r'Git\s+history', re.I)


def tracked():
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


class DocumentationReferenceTests(unittest.TestCase):
    def test_references_exist(self):
        files = tracked()
        paths = set(files) | {str(Path(f).parent) + '/' for f in files}
        for f in files:
            for parent in Path(f).parents:
                paths.add(str(parent) + '/')
        targets = set(re.findall(r'^([a-z][a-z0-9-]*):', (ROOT / 'Makefile').read_text(), re.M))
        problems = []
        for doc in (f for f in files if f.endswith('.md') and not (ROOT / f).is_symlink()):
            for number, line in enumerate((ROOT / doc).read_text().splitlines(), 1):
                if HISTORY.search(line):
                    continue
                where = f'{doc}:{number}'
                for link in LINK.findall(line):
                    if '://' in link or link.startswith('mailto:'):
                        continue
                    target = (ROOT / doc).parent.joinpath(link).resolve()
                    rel = target.relative_to(ROOT) if target.is_relative_to(ROOT) else None
                    if rel is None or not (str(rel) in paths or str(rel) + '/' in paths):
                        problems.append(f'{where}: link {link}')
                for code in CODE.findall(line):
                    code = code.rstrip('.,:;')
                    if not code.startswith(TOP) or any(c in code for c in '*<>{}$'):
                        continue
                    if not (code in paths or code.rstrip('/') + '/' in paths):
                        problems.append(f'{where}: path {code}')
                for target in MAKE.findall(line):
                    if target not in targets:
                        problems.append(f'{where}: make {target}')
        self.assertFalse(problems, 'Stale references:\n' + '\n'.join(problems))


if __name__ == '__main__':
    unittest.main()
