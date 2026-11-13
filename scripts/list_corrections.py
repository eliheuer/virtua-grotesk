#!/usr/bin/env python3
"""List Eli's reviews of purple drafts from the Git history.

A review is a commit that changes a purple glyph and removes the purple mark.
The version before the commit is the draft. The result is:

    accepted   green, with the contours and advance of the draft
    corrected  green, with other contours or another advance
    <color>    another mark, for example orange: Eli graded the draft

    list_corrections.py          the open corrections, then a summary by month
    list_corrections.py --all    every review, then the summary

A correction is open until a tracked file or a later commit message cites the
first 7 or more characters of its commit hash: a rule entry ("Seen in"), a
case in sources/held-out-glyphs.toml, a glyph record, or the message of the
commit that changes a check. The summary shows whether the drafts need less
correction over time. Edits of a glyph that stays purple are not visible, so
Eli changes the mark in the commit that corrects the draft.
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


def review(draft, after):
    """The result of a review, or None when the change is not a review."""
    if color(draft) != 'purple' or color(after) == 'purple':
        return None
    result = dict(result=color(after), iou=None, distance=None)
    if result['result'] == 'green':
        before, now = evaluation.parse(draft), evaluation.parse(after)
        same = (before['points'], before['advance']) == (now['points'], now['advance'])
        result['result'] = 'accepted' if same else 'corrected'
        if now['contours']:
            row = evaluation.compare(now, before)
            result.update(iou=row['iou'], distance=row['distance'])
    return result


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
            draft = blob(old)
            if color(draft) != 'purple':
                continue
            result = review(draft, blob(new))
            if result:
                master = path.split('VirtuaGrotesk-')[1].split('.ufo')[0]
                glyph = re.search(r'<glyph name="([^"]+)"', draft)[1]
                yield dict(commit=commit, date=date, master=master, glyph=glyph, **result)
    finally:
        blob.close()


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
    print(f"{'date':10}  {'commit':8}  {'master':7}  {'glyph':28}  {'result':9}  "
          f"{'iou':>5}  {'dist':>5}  cited")
    for row in reviews():
        row['cited'] = row['commit'][:7] in cited
        months.setdefault(row['date'][:7], []).append(row)
        if args.all or (row['result'] == 'corrected' and not row['cited']):
            print(f"{row['date']}  {row['commit'][:8]}  {row['master']:7}  {row['glyph']:28}  "
                  f"{row['result']:9}  {number(row['iou'], 3):>5}  "
                  f"{number(row['distance'], 1):>5}  {'yes' if row['cited'] else ''}")
    print(f"\n{'month':7}  {'reviewed':>8}  {'accepted':>8}  {'corrected':>9}  {'graded':>6}  "
          f"{'mean iou':>8}  {'open':>4}")
    for month, rows in sorted(months.items()):
        accepted = [r for r in rows if r['result'] == 'accepted']
        corrected = [r for r in rows if r['result'] == 'corrected']
        scores = [r['iou'] for r in accepted + corrected if r['iou'] is not None]
        mean = sum(scores) / len(scores) if scores else None
        open_ = sum(1 for r in corrected if not r['cited'])
        print(f"{month:7}  {len(rows):8}  {len(accepted):8}  {len(corrected):9}  "
              f"{len(rows) - len(accepted) - len(corrected):6}  {number(mean, 3):>8}  {open_:4}")


if __name__ == '__main__':
    sys.exit(main())
