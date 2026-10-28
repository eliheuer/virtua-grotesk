#!/usr/bin/env python3
"""Prepare live review assets from a verified DesignBot font snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import unicodedata
from fontTools.ttLib import TTFont
from reference_fonts import collect, reference_directory

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--frozen-references', action='store_true', help='Reproduce the references recorded in the evidence instead of project-local choices')
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text())
    target = args.output_dir.resolve()
    (target / 'fonts').mkdir(parents=True, exist_ok=True)
    records = {}
    for role, record in evidence['fonts'].items():
        if role not in ('before', 'after') and not args.frozen_references:
            continue
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
    if not args.frozen_references:
        references = collect(reference_directory(args.evidence), target)
        if references['errors']:
            raise ValueError('Reference fonts: ' + '; '.join(references['errors']))
        records.update(references['fonts'])
    overview = json.loads((Path(__file__).parent / 'overview-samples.json').read_text())
    # Inventory the actual Working font, not a guessed alphabet or system fallback.
    known_arabic = {ord(char) for paragraph in overview['arabic-alphabet']['paragraphs'] for run in paragraph['runs'] for char in run['text']}
    extended = [cp for cp in records['after']['codepoints'] if 0x600 <= cp <= 0x8ff
                and unicodedata.category(chr(cp)).startswith('L') and cp not in known_arabic and cp != 0x640]
    for offset in range(0, len(extended), 12):
        chunk = extended[offset:offset + 12]
        overview['arabic-alphabet']['paragraphs'].append(dict(label='Extended Arabic letters · ' + str(offset // 12 + 1),
            lang='ar', dir='rtl', runs=[dict(text=' '.join(map(chr, chunk)))]))
    groups = {}
    for cp in records['after']['codepoints']:
        char = chr(cp)
        if unicodedata.category(char).startswith('C') or char.isspace():
            continue
        if 0x590 <= cp <= 0x5ff or 0xfb1d <= cp <= 0xfb4f:
            group, lang, direction = 'Hebrew', 'he', 'rtl'
        elif 0x600 <= cp <= 0x8ff or 0xfb50 <= cp <= 0xfdff or 0xfe70 <= cp <= 0xfeff:
            group, lang, direction = 'Arabic', 'ar', 'rtl'
        elif cp < 0x250 or 0x1e00 <= cp <= 0x1eff:
            group, lang, direction = 'Latin', 'en', 'ltr'
        else:
            group, lang, direction = 'Symbols and other encoded glyphs', 'en', 'ltr'
        groups.setdefault((group, lang, direction), []).append(cp)
    repertoire = []
    for (group, lang, direction), points in groups.items():
        for start in range(0, len(points), 24):
            chunk = points[start:start + 24]
            # Dotted circles make combining marks visible without carrier collisions.
            text = ' '.join(('\u25cc' if unicodedata.category(chr(cp)).startswith('M') else '') + chr(cp) for cp in chunk)
            repertoire.append(dict(label=f'{group} · U+{chunk[0]:04X}–U+{chunk[-1]:04X}', lang=lang, dir=direction,
                                   codepoints=chunk, runs=[dict(text=text)]))
    overview['encoded-repertoire'] = dict(label='Encoded repertoire', overview=True, paragraphs=repertoire)
    default_reading = json.loads((Path(__file__).parent / 'reading-samples.json').read_text()) if evidence.get('study', {}).get('language', 'he') == 'he' else {}
    (target / 'review-data.js').write_text('window.REVIEW_DATA = '+json.dumps({'study': evidence.get('study'), 'fonts': records, 'reading': {**default_reading, **evidence.get('reading', {}), **overview}}, ensure_ascii=False)+';\n')
    for name in ['index.html', 'review.css', 'review.js', 'reference-selection.js']:
        shutil.copy2(Path(__file__).parent / name, target / name)
    # Native browser reloads can otherwise mix cached scripts with fresh HTML.
    css_path = target / 'review.css'
    css_path.write_text(css_path.read_text().replace('fonts/labels.ttf',
                        'fonts/labels.ttf?v=' + records['after']['sha256'][:12]))
    index_path = target / 'index.html'
    html = index_path.read_text()
    html = html.replace('between Before and Applied', 'between Before and ' + records['after']['label'])
    for name in ['review.css', 'review.js', 'review-data.js', 'reference-selection.js']:
        version = hashlib.sha256((target / name).read_bytes()).hexdigest()[:12]
        html = html.replace('"' + name + '"', '"' + name + '?v=' + version + '"')
    index_path.write_text(html)
    (target / 'live-fonts.json').write_text(json.dumps(records, indent=2, ensure_ascii=False)+'\n')
    print(target)

if __name__ == '__main__':
    main()
