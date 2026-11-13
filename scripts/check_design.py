#!/usr/bin/env python3
"""Check glyphs against the measurable design specification.

The specification is the `targets` section of
sources/design.toml. Runebender measures the glyphs
(`runebender agent call analyze_glyph`); this script holds the Virtua policy.
It reads the sources and never writes them.

    check_design.py n a seen-ar        report on named glyphs, both masters
    check_design.py --not-green        report on every glyph that is not green
    check_design.py --green            run the checks on green glyphs (measures
                                       how often the checks flag approved work)
    check_design.py --observe          print stroke ranges of the green glyphs
    check_design.py --ready            list composites that pass and are not green
    check_design.py --queue            rank the glyphs that most composites wait on

A contour glyph passes when its strokes are inside the target range, all
points are on the 2-unit grid, the analyzer reports no kink, and the two
masters have the same structure. A composite passes when every part is green,
the two masters use the same parts, and Runebender's anchor recipe gives the same
placement. A composite without a recipe needs review by eye. A pass is a filter before review, not approval.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tomllib
import unicodedata
from pathlib import Path

import source_inventory as inventory

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'sources/design.toml'
CACHE = ROOT / 'out/check-design-cache'
MASTERS = ['Regular', 'Bold']


def find_runebender():
    """The path of the Runebender binary, or None."""
    for candidate in (os.environ.get('RUNEBENDER'),
                      Path.home() / 'GH/repos/runebender/target/release/runebender',
                      shutil.which('runebender')):
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def runebender():
    return find_runebender() or sys.exit('Runebender binary not found. Set RUNEBENDER to its path.')


def script_of(name, record=None):
    """The target class of a glyph. Symbols and icons have no stroke target."""
    if '-ar' in name:
        return 'Arabic'
    if '-hb' in name:
        return 'Hebrew'
    codes = record['unicodes'] if record else []
    if any(unicodedata.category(chr(c))[0] in 'LN' and c < 0xE000 for c in codes):
        return 'Latin'
    return 'Symbol'


def analyze(master, record, root=ROOT):
    """Runebender's measurement of one glyph, cached by the GLIF digest."""
    cached = CACHE / f"{record['sha256']}.json"
    if cached.exists():
        return json.loads(cached.read_text())
    run = subprocess.run(
        [runebender(), 'agent', 'call', 'analyze_glyph', '--font',
         str(root / f'sources/VirtuaGrotesk-{master}.ufo'),
         '--args', json.dumps({'glyph': record['glyph']})],
        capture_output=True, text=True)
    result = json.loads(run.stdout)['result']
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps(result))
    return result


def recipes(master):
    """Runebender's anchor recipes: glyph name to whether the source matches."""
    run = subprocess.run(
        [runebender(), 'compose', str(ROOT / f'sources/VirtuaGrotesk-{master}.ufo'), '--json'],
        capture_output=True, text=True)
    try:
        return {row['glyph']: row['up_to_date'] for row in json.loads(run.stdout)['derived']}
    except (ValueError, KeyError):
        return {}


def strokes(analysis, limit):
    """Ink spans short enough to be a stroke, by the direction of the stroke."""
    found = {'vertical_stem': [], 'horizontal_stroke': []}
    for span in analysis['spans']:
        if span['ink'] and span['length'] <= limit:
            # A span measured along the horizontal axis crosses a vertical stem.
            key = 'vertical_stem' if span['axis'] == 'horizontal' else 'horizontal_stroke'
            found[key].append(span['length'])
    return found


def leaves(name, glyphs, seen=()):
    """The contour glyphs that a composite resolves to, or None for a broken reference."""
    record = glyphs.get(name)
    if record is None or name in seen:
        return None
    if not record['components']:
        return [name]
    out = [name] if record['contours'] else []
    for component in record['components']:
        below = leaves(component['base'], glyphs, seen + (name,))
        if below is None:
            return None
        out += below
    return out


def check_contour(name, data, targets, root=ROOT, masters=MASTERS):
    findings = []
    for master in masters:
        record = data[master][name]
        analysis = analyze(master, record, root)
        if record['off_2_points']:
            findings.append(f"{master}: {record['off_2_points']} points off the 2-unit grid")
        for issue in analysis['nodes']['issues']:
            if issue['level'] == 'kink':
                findings.append(f"{master}: kink at {issue['x']:g}, {issue['y']:g}")
        script = script_of(name, record)
        target = targets.get(master, {}).get(script)
        if not target:
            if script != 'Symbol':
                findings.append(f'{master}: no stroke target for {script} yet')
            continue
        for key, lengths in strokes(analysis, target['stroke_limit']).items():
            low, high = target[key]
            outside = sorted({length for length in lengths if not low <= length <= high})
            if outside:
                findings.append(f'{master}: {key} {outside} outside {low} to {high}')
    regular, bold = (data[m][name] for m in MASTERS)
    if regular['point_types'] != bold['point_types']:
        findings.append('masters: contour or point structure differs')
    return findings


def check_composite(name, data, recipe):
    findings = []
    for master in MASTERS:
        glyphs = data[master]
        record = glyphs[name]
        if not record['components']:
            kinds = {unicodedata.category(chr(c)) for c in record['unicodes']}
            if not kinds or not kinds <= {'Zs', 'Zl', 'Zp', 'Cf'}:
                findings.append(f'{master}: empty glyph')
            continue
        parts = leaves(name, glyphs)
        if parts is None:
            findings.append(f'{master}: a component reference does not resolve')
            continue
        not_green = sorted({p for p in parts if p != name and glyphs[p]['color']['name'] != 'green'})
        if not_green:
            findings.append(f"{master}: parts not green: {', '.join(not_green)}")
        if name not in recipe[master]:
            findings.append(f'{master}: no anchor recipe, so placement needs review by eye')
        elif not recipe[master][name]:
            findings.append(f'{master}: placement differs from the anchor recipe')
    bases = [[c['base'] for c in data[m][name]['components']] for m in MASTERS]
    if bases[0] != bases[1]:
        findings.append('masters: component lists differ')
    return findings


def queue(data):
    """Contour glyphs that are not green, ranked by the composites that wait on them."""
    for master in MASTERS:
        glyphs = data[master]
        blocked = {}
        for name, record in glyphs.items():
            if record['components'] and record['color']['name'] != 'green':
                for part in set(leaves(name, glyphs) or []) - {name}:
                    if glyphs[part]['color']['name'] != 'green':
                        blocked.setdefault(part, []).append(name)
        print(f'{master}: glyph (color), composites that wait on it')
        for part, waiting in sorted(blocked.items(), key=lambda item: -len(item[1]))[:25]:
            print(f"  {part} ({glyphs[part]['color']['name']}) {len(waiting)}")


def observe(data, limit):
    """Stroke ranges of the green glyphs: the evidence for the targets."""
    for master in MASTERS:
        for script in ['Latin', 'Arabic', 'Hebrew']:
            pool = {'vertical_stem': [], 'horizontal_stroke': []}
            count = 0
            for name, record in data[master].items():
                if (script_of(name, record) == script and record['contours']
                        and record['color']['name'] == 'green'):
                    count += 1
                    for key, lengths in strokes(analyze(master, record), limit[master]).items():
                        pool[key] += lengths
            for key, lengths in pool.items():
                if lengths:
                    lengths.sort()
                    pick = lambda q: lengths[min(len(lengths) - 1, int(q * len(lengths)))]
                    print(f'{master} {script} {key}: {count} glyphs, {len(lengths)} strokes, '
                          f'5% {pick(.05)}, median {pick(.5)}, 95% {pick(.95)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('glyphs', nargs='*')
    parser.add_argument('--not-green', action='store_true')
    parser.add_argument('--green', action='store_true')
    parser.add_argument('--observe', action='store_true')
    parser.add_argument('--ready', action='store_true')
    parser.add_argument('--queue', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    contract = tomllib.loads(CONTRACT.read_text())
    targets = contract.get('targets', {})
    data = {m: inventory.load_master(ROOT, m, contract) for m in MASTERS}
    if args.observe:
        observe(data, {'Regular': 180, 'Bold': 300})
        return 0
    if args.queue:
        queue(data)
        return 0

    names = [n for n in data['Regular'] if n in data['Bold']]
    is_green = lambda n: all(data[m][n]['color']['name'] == 'green' for m in MASTERS)
    is_composite = lambda n: not data['Regular'][n]['contours'] and not data['Bold'][n]['contours']
    if args.glyphs:
        missing = [n for n in args.glyphs if n not in names]
        if missing:
            sys.exit(f"Not in both masters: {', '.join(missing)}")
        names = args.glyphs
    elif args.green:
        names = [n for n in names if is_green(n)]
    elif args.not_green:
        names = [n for n in names if not is_green(n)]
    elif args.ready:
        names = [n for n in names if is_composite(n) and not is_green(n)]
    else:
        parser.error('name glyphs or pass --not-green, --green, --ready, --queue or --observe')

    recipe = {m: recipes(m) for m in MASTERS} if any(is_composite(n) for n in names) else {}
    report = {}
    for name in names:
        if is_composite(name):
            report[name] = check_composite(name, data, recipe)
        else:
            report[name] = check_contour(name, data, targets)

    passed = [n for n, findings in report.items() if not findings]
    if args.json:
        print(json.dumps(report, indent=1))
    elif args.ready:
        print(' '.join(passed))
    else:
        for name, findings in report.items():
            if findings:
                print(name)
                for finding in findings:
                    print(f'  {finding}')
    print(f'{len(passed)} of {len(report)} pass', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
