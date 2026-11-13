#!/usr/bin/env python3
"""List Eli's reviews of purple drafts from the Git history.

A review is a commit that changes a purple glyph and removes the purple mark.
The version before the commit is the draft. The new mark is Eli's grade:

    red     broken; replace it
    orange  better, not good enough
    yellow  close, and can stay yellow for a long time
    green   locked in as close to final

The draft is then compared with the first green version of the glyph. Until
the glyph is green, it is compared with the latest version that is not
purple; the column "against" gives the mark of that version:

    accepted   the same contours and advance as the draft
    corrected  other contours or another advance

    list_corrections.py          the open corrections, then a summary by month
    list_corrections.py --all    every review, then the summary

A correction is open until a tracked file or a later commit message cites the
first 7 or more characters of its review commit: a rule entry ("Seen in"), a
case in sources/held-out-glyphs.toml, a glyph record, or the message of the
commit that changes a check. The summary shows whether the drafts improve:
the grades rise, more drafts are accepted, and the overlap with Eli's version
increases. Edits of a glyph that stays purple are not visible, so Eli
changes the mark in the commit that grades or corrects the draft.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import evaluate_drafting as evaluation

ROOT = Path(__file__).resolve().parents[1]
GLYPHS = 'sources/VirtuaGrotesk-*.ufo/glyphs/*.glif'
COLORS = tomllib.loads((ROOT / 'sources/design.toml').read_text())['colors']
MARK = re.compile(r'<key>public.markColor</key>\s*<string>([^<]*)</string>')
HASH = re.compile(r'\b[0-9a-f]{7,40}\b')


def git(*args, root=ROOT, check=True):
    return subprocess.run(['git', *args], cwd=root, capture_output=True, text=True,
                          check=check).stdout


def color(text):
    found = MARK.search(text)
    if not found:
        return 'none'
    rgba = [float(v) for v in found[1].split(',')]
    for name, record in COLORS.items():
        if any(all(abs(a - b) < 0.015 for a, b in zip(rgba, known)) for known in record['rgba']):
            return name
    return 'unknown'


GRADES = {'red': 0, 'orange': 1, 'yellow': 2, 'green': 3}


def grade(draft, after):
    """The mark that a review gives, or None when the change is not a review."""
    if color(draft) != 'purple' or color(after) == 'purple':
        return None
    return color(after)


def outcome(draft, final):
    """Compare a draft with Eli's version of the glyph."""
    before, after = evaluation.parse(draft), evaluation.parse(final)
    same = (before['points'], before['advance']) == (after['points'], after['advance'])
    row = evaluation.compare(after, before) if after['contours'] else {}
    return dict(result='accepted' if same else 'corrected',
                iou=row.get('iou'), distance=row.get('distance'))


class Blobs:
    """Read blobs through one `git cat-file --batch` process."""
    def __init__(self, root=ROOT):
        self.process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=root,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def __call__(self, blob):
        self.process.stdin.write(blob.encode() + b'\n')
        self.process.stdin.flush()
        size = int(self.process.stdout.readline().split()[2])
        text = self.process.stdout.read(size).decode()
        self.process.stdout.read(1)
        return text

    def close(self):
        self.process.stdin.close()
        self.process.wait()
        self.process.stdout.close()


def reviews(root=ROOT):
    """Every review in the history, oldest first."""
    blob, commit, date = Blobs(root), None, None
    rows, waiting, latest = [], {}, {}
    try:
        for line in git('log', '--reverse', '--raw', '--no-abbrev', '--no-renames',
                        '--diff-filter=M', '--format=@%H %as', '--', GLYPHS, root=root).splitlines():
            if line.startswith('@'):
                commit, date = line[1:].split()
                continue
            if not line.startswith(':'):
                continue
            meta, path = line.split('\t')
            old, new = meta.split()[2:4]
            draft, after = blob(old), blob(new)
            mark = grade(draft, after)
            if mark:
                row = dict(commit=commit, date=date, glyph=re.search(r'<glyph name="([^"]+)"', draft)[1],
                           master=path.split('VirtuaGrotesk-')[1].split('.ufo')[0], grade=mark,
                           against=None, result=None, iou=None, distance=None, draft=draft)
                rows.append(row)
                waiting.setdefault(path, []).append(row)
            if color(after) != 'purple':
                latest[path] = after
            if color(after) == 'green':
                for row in waiting.pop(path, []):
                    row.update(outcome(row.pop('draft'), after), against='green')
    finally:
        blob.close()
    for path, group in waiting.items():
        for row in group:
            row.update(outcome(row.pop('draft'), latest[path]), against=color(latest[path]))
    return rows


def citations(root=ROOT):
    """7-character prefixes of the hashes in commit messages and tracked files."""
    text = git('log', '--format=%B', root=root) + git(
        'grep', '-h', '-I', '-E', r'\b[0-9a-f]{7,40}\b', '--', '.', ':!sources/*.ufo', root=root, check=False)
    return {token[:7] for token in HASH.findall(text)}


def number(value, digits):
    return '' if value is None else f'{value:.{digits}f}'


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--all', action='store_true', help='list every review')
    args = parser.parse_args()
    cited, months = citations(), {}
    print(f"{'date':10}  {'commit':8}  {'master':7}  {'glyph':24}  {'grade':6}  {'against':7}  {'result':9}  "
          f"{'iou':>5}  {'dist':>5}  cited")
    for row in reviews():
        row['cited'] = row['commit'][:7] in cited
        months.setdefault(row['date'][:7], []).append(row)
        if args.all or (row['result'] == 'corrected' and not row['cited']):
            print(f"{row['date']}  {row['commit'][:8]}  {row['master']:7}  {row['glyph']:24}  "
                  f"{row['grade']:6}  {row['against']:7}  {row['result']:9}  {number(row['iou'], 3):>5}  "
                  f"{number(row['distance'], 1):>5}  {'yes' if row['cited'] else ''}")
    print(f"\n{'month':7}  {'reviewed':>8}  {'red':>4}  {'orange':>6}  {'yellow':>6}  {'green':>5}  "
          f"{'grade':>5}  {'accepted':>8}  {'corrected':>9}  {'iou':>5}  {'open':>4}")
    for month, rows in sorted(months.items()):
        count = lambda key, value: sum(1 for r in rows if r[key] == value)
        grades = [GRADES[r['grade']] for r in rows if r['grade'] in GRADES]
        scores = [r['iou'] for r in rows if r['iou'] is not None]
        open_ = sum(1 for r in rows if r['result'] == 'corrected' and not r['cited'])
        print(f"{month:7}  {len(rows):8}  {count('grade', 'red'):4}  {count('grade', 'orange'):6}  "
              f"{count('grade', 'yellow'):6}  {count('grade', 'green'):5}  "
              f"{number(sum(grades) / len(grades) if grades else None, 2):>5}  "
              f"{count('result', 'accepted'):8}  {count('result', 'corrected'):9}  "
              f"{number(sum(scores) / len(scores) if scores else None, 3):>5}  {open_:4}")
    print('\ngrade: mean of red 0, orange 1, yellow 2, green 3. iou: overlap of the draft '
          'with the green version, or the latest version that is not purple.')


if __name__ == '__main__':
    sys.exit(main())
