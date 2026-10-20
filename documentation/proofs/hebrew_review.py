#!/usr/bin/env python3
"""Run the canonical DesignBot Rust review set; Python records/verifies evidence only."""
import argparse
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).with_suffix('.rs')
WEIGHTS = [400, 550, 700]
GROUPS = {'dalet-resh': 'ד ר דרך חדר סדר דרדר רדרד',
          'he-het-tav': 'ה ח ת היה חיה תחיה הח חה חת תח הָ חַ תֵ הּ חִ תַ הּ תּ',
          'he-het-tav-candidate': 'ה ח ת היה חיה תחיה הח חה חת תח הָ חַ תֵ הּ חִ תַ הּ תּ'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['before', 'after', 'rubik', 'noto']:
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--themes', nargs='+', choices=['light', 'dark'], default=['light', 'dark'])
    p.add_argument('--state', choices=['applied', 'candidate'], default='applied')
    p.add_argument('--headline-tracking-em', type=float, default=-0.02)
    p.add_argument('--grid', action='store_true')
    p.add_argument('--baseline-grid', action='store_true', help='Add baseline guides to the structural grid')
    p.add_argument('--details', action='store_true', help='Add three enlarged glyph sheets')
    p.add_argument('--group', choices=list(GROUPS), default='dalet-resh')
    a = p.parse_args()
    if a.details and a.group == 'dalet-resh':
        p.error('--details currently supports the he/het/tav groups only')
    if not -0.05 <= a.headline_tracking_em <= 0:
        p.error('Headline tracking must be between -0.05 and 0 em')
    if len(set(a.themes)) != len(a.themes):
        p.error('Themes must be unique')
    executable = shutil.which('designbot')
    if not executable:
        p.error('Install DesignBot before rendering')
    fonts = {name: getattr(a, name).resolve() for name in ['before', 'after', 'rubik', 'noto']}
    identities = {}
    for role, path in fonts.items():
        with TTFont(path) as font:
            family = font['name'].getDebugName(16) or font['name'].getDebugName(1)
            expected = {'before': 'Virtua Grotesk', 'after': 'Virtua Grotesk',
                        'rubik': 'Rubik', 'noto': 'Noto Sans Hebrew'}[role]
            if family != expected:
                p.error(f'{role}: expected family {expected!r}, got {family!r}')
            axes = {x.axisTag: [x.minValue, x.defaultValue, x.maxValue] for x in font['fvar'].axes}
            if not all(axes['wght'][0] <= w <= axes['wght'][2] for w in WEIGHTS):
                p.error(f'{role}: weight axis must include 400 through 700')
            chars = GROUPS[a.group] + ('n o H O' if role == 'after' else '')
            if role == 'after':
                chars += ''.join(chr(i) for i in range(32, 127))
            missing = sorted(set(ord(c) for c in chars) - set(font.getBestCmap()))
            if missing:
                p.error(f'{role}: missing codepoints {missing}')
            identities[role] = {'path': str(path), 'sha256': sha(path), 'family': family, 'axes': axes}
    out = a.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, HEADLINE_TRACKING_EM=str(a.headline_tracking_em),
                       GRID_VIEW='baseline' if a.baseline_grid else '1' if a.grid else '0', REVIEW_GROUP=a.group)
    records = []
    sheets = ['form', 'text', 'weight'] + (['detail-he', 'detail-het', 'detail-tav', 'marks'] if a.details else [])
    for theme in a.themes:
        for index, sheet in enumerate(sheets, 1):
            image_path = out / f'{index:02}-{sheet}-{theme}.png'
            command = [executable, '--raw', str(SCRIPT), '--output', str(image_path), '--',
                       theme, sheet, *map(str, fonts.values()), a.state]
            with image_path.with_suffix('.log').open('w') as log:
                # DesignBot's script cache shares an export target. Concurrent
                # invocations can succeed while writing another job's output.
                with (Path(tempfile.gettempdir()) / 'virtua-designbot-render.lock').open('a') as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    result = subprocess.run(command, cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f'DesignBot failed; see {image_path.with_suffix(".log")}')
            with Image.open(image_path) as image:
                if image.size != (1600, 1120):
                    raise ValueError(f'Unexpected page size: {image.size}')
                colors = image.convert('RGBA').getcolors(image.width * image.height)
                if not all(r == g == b and 68 <= r <= 222 and alpha == 255
                           for _, (r, g, b, alpha) in colors):
                    raise ValueError(f'Non-neutral, out-of-range or transparent pixels: {image_path}')
            records.append({'path': str(image_path), 'sha256': sha(image_path), 'theme': theme,
                            'sheet': sheet, 'command': command, 'pixel_checks': 'opaque neutral grays, 68..222'})
            print(image_path, flush=True)
    for role, path in fonts.items():
        if sha(path) != identities[role]['sha256']:
            raise RuntimeError(f'{role} font changed during render; outputs are not a coherent snapshot')
    evidence = {'fonts': identities, 'script': {'path': str(SCRIPT), 'sha256': sha(SCRIPT)},
                'runner_sha256': sha(Path(__file__)), 'designbot': {'path': executable, 'sha256': sha(Path(executable))},
                'outputs': records, 'weights': WEIGHTS,
                'group': a.group, 'state': 'current' if a.group == 'he-het-tav' else a.state,
                'palette': ['#dedede', '#444444'], 'page_size': [1600, 1120], 'margin': 80, 'baseline_unit': 8,
                'layout': {'label_rail': 128, 'rail_gutter': 32, 'comparison_origin': 240, 'comparison_width': 1280, 'four_column_gutter': 32, 'three_column_gutter': 64},
                'headline': {'size': 56, 'tracking_em': a.headline_tracking_em,
                             'tracking_px': a.headline_tracking_em * 56},
                'sample_tracking': 0, 'label_weight': 400, 'grid_overlay': a.grid or a.baseline_grid,
                'grid_mode': 'baseline' if a.baseline_grid else 'structure' if a.grid else 'off',
                'sizes': {'form': 136 if a.group == 'he-het-tav-candidate' else 160 if a.group == 'he-het-tav' else 192, 'text': [44, 32, 24],
                          'weight': 160 if a.group.startswith('he-het-tav') else 176, 'detail': 384 if a.details else None},
                'rendering': 'DesignBot / Parley / Swash outlines / Vello CPU; hinting enabled; raw PNG',
                'validation': 'Cmap, axis and family preflight; Rust advance/ink bounds; pixel checks. Not native-reader approval.',
                'verification_tools': {k: importlib.metadata.version(k) for k in ['fonttools', 'Pillow']}}
    (out / 'review.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
