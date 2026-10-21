#!/usr/bin/env python3
"""Prepare live review assets from a verified DesignBot font snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from fontTools.ttLib import TTFont

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text())
    target = args.output_dir.resolve()
    (target / 'fonts').mkdir(parents=True, exist_ok=True)
    records = {}
    for role, record in evidence['fonts'].items():
        label = record.get('label', {'before': 'Before', 'after': 'Applied'}.get(role, 'Reference'))
        faces = []
        coverage = None
        for item in record.get('faces', [record]):
            source = Path(item['path'])
            if not source.is_absolute():
                source = args.evidence.resolve().parent / source
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if digest != item['sha256']:
                raise ValueError(f'{role}: font differs from recorded review snapshot')
            name = f'{role}-{digest[:12]}.ttf'
            destination = target / 'fonts' / name
            if source.resolve() != destination.resolve():
                shutil.copy2(source, destination)
            if role == 'after':
                shutil.copy2(source, target / 'fonts' / 'labels.ttf')
            with TTFont(source) as font:
                cmap = set(font.getBestCmap())
                coverage = cmap if coverage is None else coverage & cmap
                axes = {a.axisTag: [a.minValue, a.defaultValue, a.maxValue] for a in font['fvar'].axes} if 'fvar' in font else {}
                weight = item.get('weight', '400 700' if 'wght' in axes else font['OS/2'].usWeightClass)
                faces.append(dict(url=f'fonts/{name}', sha256=digest, axes=axes, weight=str(weight)))
        records[role] = dict(family=record['family'], label=label, codepoints=sorted(coverage))
        if 'faces' in record:
            records[role]['faces'] = faces
        else:
            records[role].update(faces[0])
    default_reading = json.loads((Path(__file__).parent / 'reading-samples.json').read_text()) if evidence.get('study', {}).get('language', 'he') == 'he' else {}
    (target / 'review-data.js').write_text('window.REVIEW_DATA = '+json.dumps({'study': evidence.get('study'), 'fonts': records, 'reading': {**default_reading, **evidence.get('reading', {})}}, ensure_ascii=False)+';\n')
    for name in ['index.html', 'review.css', 'review.js']:
        shutil.copy2(Path(__file__).parent / name, target / name)
    # Native browser reloads can otherwise mix cached scripts with fresh HTML.
    css_path = target / 'review.css'
    css_path.write_text(css_path.read_text().replace('fonts/labels.ttf',
                        'fonts/labels.ttf?v=' + records['after']['sha256'][:12]))
    index_path = target / 'index.html'
    html = index_path.read_text()
    html = html.replace('between Before and Applied', 'between Before and ' + records['after']['label'])
    for name in ['review.css', 'review.js', 'review-data.js']:
        version = hashlib.sha256((target / name).read_bytes()).hexdigest()[:12]
        html = html.replace('"' + name + '"', '"' + name + '?v=' + version + '"')
    index_path.write_text(html)
    (target / 'live-fonts.json').write_text(json.dumps(records, indent=2, ensure_ascii=False)+'\n')
    print(target)

if __name__ == '__main__':
    main()
