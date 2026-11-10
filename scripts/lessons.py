#!/usr/bin/env python3
"""Count the corrections in the Git history by topic.

A correction commit has one line for each correction:

    Correction: <topic>: <what was wrong, in one sentence>

The topics and their rule documents are in the [lessons] table of
sources/design.toml. This script reads the Git log and writes nothing.

    lessons.py              corrections by topic, the repeated topics first
    lessons.py curves       the corrections of one topic

A correction is "recorded" when its short commit hash appears in the rule
document of its topic. A topic with two or more unrecorded corrections needs
a rule entry, or an extra glyph on an existing entry.
"""
from __future__ import annotations

import argparse
import plistlib
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r'^Correction:\s*([a-z-]+)\s*:\s*(.+?)\s*$', re.M)
GLIF = re.compile(r'^sources/VirtuaGrotesk-(Regular|Bold)\.ufo/glyphs/(.+)\.glif$')


def topics():
    return tomllib.loads((ROOT / 'sources/design.toml').read_text())['lessons']


def glyph_names():
    """GLIF file name to glyph name, from the current contents.plist files."""
    names = {}
    for master in ('Regular', 'Bold'):
        path = ROOT / f'sources/VirtuaGrotesk-{master}.ufo/glyphs/contents.plist'
        for name, filename in plistlib.loads(path.read_bytes()).items():
            names[(master, filename[:-len('.glif')])] = name
    return names


def parse(log, names=None):
    """Corrections from `git log` output in the format that `corrections` requests."""
    names = names or {}
    found = []
    for record in log.split('\x1e'):
        if not record.strip():
            continue
        header, _, files = record.partition('\x1d')
        commit, date, body = header.strip('\n').split('\x1f', 2)
        glyphs = sorted({f'{names.get((m[1], m[2]), m[2])} {m[1]}'
                         for m in map(GLIF.match, files.split()) if m})
        for topic, text in LINE.findall(body):
            found.append(dict(commit=commit[:8], date=date, topic=topic, text=text, glyphs=glyphs))
    return found


def corrections():
    log = subprocess.run(
        ['git', 'log', '--no-merges', '--name-only',
         '--format=%x1e%H%x1f%ad%x1f%B%x1d', '--date=short'],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return parse(log, glyph_names())


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('topic', nargs='?')
    args = parser.parse_args()
    table = topics()
    if args.topic and args.topic not in table:
        sys.exit(f"Unknown topic {args.topic!r}. Topics: {', '.join(table)}")

    by_topic = {}
    for item in corrections():
        by_topic.setdefault(item['topic'], []).append(item)
    for topic in by_topic.keys() - table.keys():
        print(f'warning: unknown topic {topic!r} in commit '
              f"{', '.join(i['commit'] for i in by_topic[topic])}")
    if not by_topic:
        print('No correction lines in the Git history yet.')
        return 0

    shown = [args.topic] if args.topic else sorted(
        (t for t in by_topic if t in table), key=lambda t: -len(by_topic[t]))
    for topic in shown:
        items = by_topic.get(topic, [])
        document = (ROOT / table[topic]).read_text()
        open_items = [i for i in items if i['commit'] not in document]
        flag = '  <- needs a rule entry' if len(open_items) >= 2 else ''
        print(f'{topic}: {len(items)} corrections, {len(open_items)} not recorded '
              f'in {table[topic]}{flag}')
        for item in items:
            state = ' ' if item['commit'] in document else '*'
            glyphs = ', '.join(item['glyphs']) or 'no glyph files'
            print(f"  {state} {item['date']} {item['commit']}  {item['text']}  [{glyphs}]")
    print('\n* = not recorded in the rule document of its topic')
    return 0


if __name__ == '__main__':
    sys.exit(main())
