"""Keep the repository small: every tracked file must have an allowed place.

This test fails when a commit adds a file that the layout does not allow, for
example a worklog, a report, a receipt, a plan or a dated document. To add a
new kind of file, change LAYOUT in the same commit and say why in the commit
message. AGENTS.md describes the layout for people and agents.

Every LAYOUT pattern must match at least one tracked file. When you remove the
last file of a kind, remove its pattern in the same commit.
"""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Allowed paths, as shell patterns. `*` does not match `/`; `**` matches any depth.
LAYOUT = [
    # Root: the Google Fonts template files, plus the agent guide and status.
    '.gitignore', 'AGENTS.md', 'AUTHORS.txt', 'CONTRIBUTORS.txt', 'Makefile',
    'OFL.txt', 'README.md', 'STATUS.md', 'requirements.in', 'requirements.txt',
    '.github/workflows/*.yaml',
    # Agent files: skills, task contracts, and the OMP rules link to AGENTS.md.
    '.agents/README.md', '.agents/skills/*/SKILL.md',
    '.agents/tasks/*.md', '.omp/RULES.md',
    # Sources.
    'sources/README.md', 'sources/VirtuaGrotesk.designspace', 'sources/config.yaml',
    'sources/design.toml', 'sources/held-out-glyphs.toml',
    'sources/VirtuaGrotesk-Regular.ufo/**', 'sources/VirtuaGrotesk-Bold.ufo/**',
    # Tools and their tests.
    'scripts/README.md', 'scripts/*.py', 'scripts/*.sh', 'scripts/proof-web/**',
    'tests/test_*.py',
    # Documentation: the design rules, the Google Fonts article, and the
    # DesignBot script for the README image.
    'documentation/*.md', 'documentation/design/**/*.md', 'documentation/article/**',
    'documentation/readme-images/*.rs',
]

# Document names that mark a record of work rather than a maintained document.
RECORD_NAME = re.compile(
    r'(worklog|handoff|receipt|audit|journal|todo|notes|checklist|plan|report|'
    r'summary|status|history|log)[-_.]|\d{4}-\d{2}-\d{2}', re.I)
RECORD_ALLOWED = {'STATUS.md'}

# Maintained documents stay short enough to read in one sitting.
MAX_DOCUMENT_LINES = 200


def tracked():
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout
    return [line for line in out.splitlines() if (ROOT / line).exists()]


def matches(path, pattern):
    regex = (re.escape(pattern).replace(r'\*\*/', '(?:.*/)?')
             .replace(r'\*\*', '.*').replace(r'\*', '[^/]*'))
    return re.fullmatch(regex, path) is not None


def problems(path):
    found = []
    if not any(matches(path, pattern) for pattern in LAYOUT):
        found.append('no allowed place in LAYOUT')
    name = Path(path).name
    document = Path(path).suffix in {'.md', '.txt', '.html', '.pdf'}
    if document and name not in RECORD_ALLOWED and RECORD_NAME.search(name):
        found.append('name of a work record')
    if path.endswith('.md') and path != 'STATUS.md' and (ROOT / path).exists():
        lines = (ROOT / path).read_text(errors='ignore').count('\n')
        if lines > MAX_DOCUMENT_LINES:
            found.append(f'{lines} lines, more than {MAX_DOCUMENT_LINES}')
    if path.endswith('.json') and not path.startswith('scripts/proof-web/'):
        found.append('JSON in a file that people edit; use TOML')
    return found


class RepositoryLayout(unittest.TestCase):
    def test_every_file_has_an_allowed_place(self):
        failures = []
        for path in tracked():
            for problem in problems(path):
                failures.append(f'{path}: {problem}')
        self.assertFalse(failures, '\n' + '\n'.join(failures) +
                         '\nSee tests/test_repository_layout.py and AGENTS.md.')

    def test_every_pattern_matches_a_file(self):
        files = tracked()
        unused = [p for p in LAYOUT if not any(matches(f, p) for f in files)]
        self.assertFalse(unused, f'Remove these patterns from LAYOUT: {unused}')


if __name__ == '__main__':
    unittest.main()
