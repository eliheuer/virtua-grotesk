#!/usr/bin/env python3
"""Render a reproducible DesignBot PNG from a prepared web proof."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from fontTools.ttLib import TTFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--proof-dir', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--text', required=True)
parser.add_argument('--title', default='Arabic detail')
parser.add_argument('--weight', type=int, required=True)
parser.add_argument('--size', type=int, default=144)
args = parser.parse_args()
if not 400 <= args.weight <= 700:
    parser.error('Weight must be between 400 and 700')
if not 8 <= args.size <= 512:
    parser.error('Size must be between 8 and 512 px/em')
root = args.proof_dir.resolve()
manifest = json.loads((root / 'live-fonts.json').read_text())
recipe = Path(__file__).with_suffix('.rs').resolve()
command = ['designbot', '--raw', str(recipe), '--output', str(args.output.resolve()),
           '--', str(args.weight), str(args.size), args.text, args.title, str(root / manifest['after']['url'])]
inputs = []
roles = [role for role in ('before', 'after') if role in manifest] + [role for role in manifest if role not in ('before', 'after')]
for role in roles:
    font = manifest[role]
    faces = font.get('faces', [])
    def actual(face):
        axis = face.get('axes', {}).get('wght')
        return max(axis[0], min(axis[2], args.weight)) if axis else int(face.get('weight', args.weight))
    face = min(faces, key=lambda f: (abs(actual(f) - args.weight), actual(f), -int('wght' in f.get('axes', {})), f.get('path', f['url']))) if faces else font
    path = root / face['url']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != face['sha256']:
        raise ValueError(f'Snapshot hash mismatch: {path}')
    with TTFont(path) as tt:
        # Joining controls are shaping instructions, not visible glyph coverage.
        required = {ord(c) for c in args.text if not c.isspace() and ord(c) not in (0x200C, 0x200D)}
        missing = sorted(required - set(tt.getBestCmap()))
        if missing:
            raise ValueError(f'{role} lacks {missing}; do not substitute fallback fonts')
    label = font['label'] if role in ('before', 'after') else font['family']
    actual_weight = actual(face)
    if actual_weight != args.weight:
        label += f' · {actual_weight} (nearest supplied weight)'
    command.extend([str(path), font.get('sourceFamily', font['family']), label, str(actual_weight)])
    inputs.append({'role': role, 'family': font['family'], 'file': face['url'], 'sha256': digest, 'rendered_weight': actual_weight})
args.output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(command, check=True)
receipt = dict(renderer='DesignBot --raw', weight=args.weight, size_px_em=args.size,
               text=args.text, title=args.title, dimensions=[1600, 208 + ((len(inputs) + 1) // 2) * 304], fonts=inputs,
               recipe_sha256=hashlib.sha256(recipe.read_bytes()).hexdigest(),
               image_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest())
args.output.with_suffix('.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(args.output.resolve())
