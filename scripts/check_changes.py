#!/usr/bin/env python3
"""Check source changes against a base revision before Eli reviews them.

Use this after an agent has edited glyphs, in particular after an unattended
run. It compares the UFO sources in the working tree with a base revision
and reads nothing else.

    check_changes.py                        compare with main
    check_changes.py --base HEAD~3          compare with another revision
    check_changes.py --glyphs "a e seen-ar" allow changes to these glyphs only
    check_changes.py --proof out/review     also draw SVG proof sheets of the
                                            changed glyphs, before and after

It fails (exit status 1) when:

- a glyph that is green at the base revision changed;
- the contours of a glyph changed and it is not purple (a change of anchors,
  advance or components only does not need purple);
- a changed composite is green but `check_design.py --ready` does not list it;
- a glyph outside --glyphs changed;
- a source file other than a glyph file changed, unless --allow-other;
- a changed glyph has points off the 2-unit grid, or a different structure in
  the two masters.

It also prints the other design check findings (stroke ranges, kinks) for each
changed glyph. Those are for review and do not fail the check.
"""
from __future__ import annotations

import argparse
import plistlib
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import check_design
import source_inventory as inventory

ROOT = Path(__file__).resolve().parents[1]
MASTERS = check_design.MASTERS
HARD = ('off the 2-unit grid', 'structure differs', 'component lists differ', 'does not resolve')


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_files(base):
    tracked = git('diff', '--name-only', base, '--', 'sources').splitlines()
    new = git('ls-files', '--others', '--exclude-standard', '--', 'sources').splitlines()
    return sorted(set(tracked + new))


def base_contents(base, master):
    path = f'sources/VirtuaGrotesk-{master}.ufo/glyphs/contents.plist'
    return plistlib.loads(git('show', f'{base}:{path}').encode())


def base_colors(base, contract):
    """Mark color of every glyph at the base revision, by master."""
    out = {}
    for master in MASTERS:
        out[master] = {}
        for name, filename in base_contents(base, master).items():
            path = f'sources/VirtuaGrotesk-{master}.ufo/glyphs/{filename}'
            text = git('show', f'{base}:{path}')
            lib = {}
            if '<key>public.markColor</key>' in text:
                value = text.split('<key>public.markColor</key>', 1)[1]
                lib['public.markColor'] = value.split('<string>', 1)[1].split('</string>', 1)[0]
            out[master][name] = inventory.color_state(lib, contract)['name']
    return out


def contours_at(base, path):
    """The contour elements of a GLIF file at a base revision, as text."""
    try:
        text = git('show', f'{base}:{path}')
    except subprocess.CalledProcessError:
        return None
    return re.findall(r'<contour>.*?</contour>', text, re.S)


def draw_proofs(base, glyphs, directory):
    """SVG proof sheets of the changed glyphs, at the base and in the working tree."""
    directory.mkdir(parents=True, exist_ok=True)
    binary = check_design.runebender()
    with tempfile.TemporaryDirectory() as scratch:
        git('worktree', 'add', '--detach', scratch, base)
        try:
            for master in MASTERS:
                names = ','.join(sorted(glyphs[master]))
                if not names:
                    continue
                for label, root in (('before', Path(scratch)), ('after', ROOT)):
                    out = directory / f'{master}-{label}.svg'
                    subprocess.run([binary, 'proof', str(root / f'sources/VirtuaGrotesk-{master}.ufo'),
                                    '--glyphs', names, '--out', str(out)],
                                   capture_output=True, check=True)
                    print(f'proof: {out}')
        finally:
            git('worktree', 'remove', '--force', scratch)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--base', default='main')
    parser.add_argument('--glyphs', default='', help='space-separated glyph names')
    parser.add_argument('--allow-other', action='store_true')
    parser.add_argument('--proof', type=Path)
    args = parser.parse_args()

    contract = tomllib.loads(check_design.CONTRACT.read_text())
    current = {m: inventory.load_master(ROOT, m, contract) for m in MASTERS}
    before = base_colors(args.base, contract)
    scope = set(args.glyphs.split())
    errors, notes = [], []

    by_file = {}
    for master in MASTERS:
        for name, record in current[master].items():
            by_file[record['path']] = (master, name)
    changed = {m: set() for m in MASTERS}
    for path in changed_files(args.base):
        if path in by_file:
            master, name = by_file[path]
            changed[master].add(name)
        elif not args.allow_other:
            errors.append(f'{path}: source file other than a glyph changed (use --allow-other)')
        else:
            notes.append(f'{path}: changed')

    ready = None
    for master in MASTERS:
        for name in sorted(changed[master]):
            record = current[master][name]
            color = record['color']['name']
            was = before[master].get(name, 'new')
            label = f'{master} {name}'
            if was == 'green':
                errors.append(f'{label}: was green at {args.base} and changed')
            if scope and name not in scope:
                errors.append(f'{label}: outside --glyphs')
            drawn = re.findall(r'<contour>.*?</contour>', (ROOT / record['path']).read_text(), re.S)
            if drawn and drawn != contours_at(args.base, record['path']) and color != 'purple':
                errors.append(f'{label}: contours changed and the glyph is {color}, not purple')
            if not record['contours'] and color == 'green' and was != 'green':
                if ready is None:
                    ready = set(subprocess.run(
                        [sys.executable, str(ROOT / 'scripts/check_design.py'), '--ready'],
                        capture_output=True, text=True).stdout.split())
                if name not in ready:
                    errors.append(f'{label}: marked green but check_design.py --ready does not list it')

    names = sorted(changed['Regular'] | changed['Bold'])
    both = [n for n in names if n in current['Regular'] and n in current['Bold']]
    recipe = {m: check_design.recipes(m) for m in MASTERS} if both else {}
    for name in both:
        composite = not current['Regular'][name]['contours'] and not current['Bold'][name]['contours']
        findings = (check_design.check_composite(name, current, recipe) if composite
                    else check_design.check_contour(name, current, contract.get('targets', {})))
        for finding in findings:
            (errors if any(h in finding for h in HARD) else notes).append(f'{name}: {finding}')

    print(f"Changed glyphs since {args.base}: Regular {len(changed['Regular'])}, "
          f"Bold {len(changed['Bold'])}")
    for line in notes:
        print(f'  note: {line}')
    for line in errors:
        print(f'  error: {line}')
    if args.proof and names:
        draw_proofs(args.base, changed, args.proof)
    print('FAIL' if errors else 'PASS')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
