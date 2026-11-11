"""Keep the repository small: every tracked file must have an allowed place.

This test fails when a commit adds a file that the layout does not allow, for
example a worklog, a report, a receipt, a plan or a dated document. To add a
new kind of file, change LAYOUT in the same commit and say why in the commit
message. AGENTS.md describes the layout for people and agents.

PENDING lists the files that existed before this test and do not fit. They are
under review. The list can only get shorter: when a file is removed or moved,
remove its entry.
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
    'sources/design.toml',
    'sources/VirtuaGrotesk-Regular.ufo/**', 'sources/VirtuaGrotesk-Bold.ufo/**',
    # Small models: a model card, the checkpoint and small runner files.
    'models/README.md', 'models/*/README.md', 'models/*/checkpoint.*', 'models/*/*.json', 'models/*/*.py',
    # Tools and their tests.
    'scripts/README.md', 'scripts/*.py', 'scripts/*.sh', 'scripts/proof-web/**',
    'tests/test_*.py', 'tests/benchmark.toml', 'tests/fixtures/**',
    # Documentation: the design rules, the Google Fonts article, and the
    # DesignBot scripts for the README image and social media.
    'documentation/*.md', 'documentation/design/**/*.md', 'documentation/article/**',
    'documentation/readme-images/*.rs',
    'documentation/social-assets/README.md', 'documentation/social-assets/*/*.rs',
]

# Document names that mark a record of work rather than a maintained document.
RECORD_NAME = re.compile(
    r'(worklog|handoff|receipt|audit|journal|todo|notes|checklist|plan|report|'
    r'summary|status|history|log)[-_.]|\d{4}-\d{2}-\d{2}', re.I)
RECORD_ALLOWED = {'STATUS.md'}

# Maintained documents stay short enough to read in one sitting.
MAX_DOCUMENT_LINES = 200

# Model checkpoints in Git stay small.
MAX_CHECKPOINT_BYTES = 5 * 1024 * 1024

PENDING = set()  # empty since 2026-11-11; keep it empty


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
    if path.endswith('.json') and not path.startswith(('scripts/proof-web/', 'models/')):
        found.append('JSON in a file that people edit; use TOML')
    if path.startswith('models/') and '/checkpoint.' in path and (ROOT / path).exists():
        size = (ROOT / path).stat().st_size
        if size > MAX_CHECKPOINT_BYTES:
            found.append(f'{size} bytes; a checkpoint over 5 MB goes to a release or Hugging Face')
    return found


class RepositoryLayout(unittest.TestCase):
    def test_every_file_has_an_allowed_place(self):
        failures = []
        for path in tracked():
            if any(matches(path, pattern) for pattern in PENDING):
                continue
            for problem in problems(path):
                failures.append(f'{path}: {problem}')
        self.assertFalse(failures, '\n' + '\n'.join(failures) +
                         '\nSee tests/test_repository_layout.py and AGENTS.md.')

    def test_pending_entries_still_exist(self):
        files = tracked()
        stale = [p for p in PENDING if not any(matches(f, p) for f in files)]
        self.assertFalse(stale, f'Remove these entries from PENDING: {stale}')


if __name__ == '__main__':
    unittest.main()
