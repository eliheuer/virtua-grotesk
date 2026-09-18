#!/usr/bin/env python3
"""Audit Hebrew coverage and attachment in a compiled font; optionally render proofs.

Exit 1 for missing/blank modern Hebrew or absent GDEF/GPOS attachment.
The wider Hebrew blocks are inventoried separately, including protected blanks.
Requires fontTools, uharfbuzz, and hb-view for --proof-dir.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

MODERN = set(range(0x05D0, 0x05EB)) | set(range(0x05B0, 0x05BD)) | {
    0x05BE, 0x05C1, 0x05C2, 0x05C7, 0x05F3, 0x05F4, 0x20AA,
}
SAMPLES = {
    'letters': 'אבגדהוזחטיכלמנסעפצקרשת ךםןףץ',
    'vowels': 'בַ בָ בֶ בֵ בִ בֹ בֻ בְ שָׁ שִׂ בּ',
    'words': 'שָׁלוֹם עִבְרִית בְּרֵאשִׁית',
    'finals': 'ךָ ךְ םִ ןִ ףִ ץִ',
    'stacked': 'בְּ בִּ שָּׁ שִּׂ וּ וֹ',
}


def audit(path):
    data = path.read_bytes()
    font = TTFont(path)
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    classes = (font['GDEF'].table.GlyphClassDef.classDefs
               if 'GDEF' in font and font['GDEF'].table.GlyphClassDef else {})
    records = []
    failures = []
    for cp in sorted(MODERN | {cp for cp in cmap if 0x590 <= cp <= 0x5FF or 0xFB1D <= cp <= 0xFB4F}):
        name = cmap.get(cp)
        bounds = None
        if name:
            pen = BoundsPen(glyphs)
            glyphs[name].draw(pen)
            bounds = pen.bounds
        mark = unicodedata.category(chr(cp)) in {'Mn', 'Mc', 'Me'}
        record = dict(codepoint=f'U+{cp:04X}', name=name, ink=bounds is not None,
                      advance=font['hmtx'][name][0] if name else None,
                      mark=mark, gdef_class=classes.get(name))
        records.append(record)
        if cp in MODERN:
            if bounds is None:
                failures.append(f'U+{cp:04X}: missing or blank')
            if mark and (classes.get(name) != 3 or record['advance'] != 0):
                failures.append(f'U+{cp:04X}: needs GDEF mark class and zero advance')
    scripts = []
    features = []
    if 'GPOS' in font:
        table = font['GPOS'].table
        scripts = [r.ScriptTag for r in table.ScriptList.ScriptRecord]
        for record in table.ScriptList.ScriptRecord:
            if record.ScriptTag == 'hebr' and record.Script.DefaultLangSys:
                features = [table.FeatureList.FeatureRecord[i].FeatureTag
                            for i in record.Script.DefaultLangSys.FeatureIndex]
    if 'mark' not in features:
        failures.append('Hebrew default language has no GPOS mark feature')
    # A mark feature may exist but contain only another script's lookups.
    attached = set()
    if 'GPOS' in font:
        for record in font['GPOS'].table.ScriptList.ScriptRecord:
            if record.ScriptTag != 'hebr' or not record.Script.DefaultLangSys:
                continue
            for index in record.Script.DefaultLangSys.FeatureIndex:
                feature = font['GPOS'].table.FeatureList.FeatureRecord[index]
                if feature.FeatureTag != 'mark':
                    continue
                for lookup_index in feature.Feature.LookupListIndex:
                    lookup = font['GPOS'].table.LookupList.Lookup[lookup_index]
                    for subtable in lookup.SubTable:
                        subtable = getattr(subtable, 'ExtSubTable', subtable)
                        if hasattr(subtable, 'MarkCoverage') and hasattr(subtable, 'BaseCoverage'):
                            if cmap.get(0x05D1) in subtable.BaseCoverage.glyphs:
                                attached.update(subtable.MarkCoverage.glyphs)
    for cp in range(0x05B0, 0x05BD):
        if cmap.get(cp) not in attached:
            failures.append(f'U+{cp:04X}: no explicit mark-to-bet attachment')
    shaping = {}
    weights = [400, 550, 700] if 'fvar' in font else [None]
    for weight in weights:
        face = hb.Face(data)
        hfont = hb.Font(face)
        if weight is not None:
            hfont.set_variations({'wght': weight})
        runs = {}
        for label, sample in SAMPLES.items():
            buf = hb.Buffer()
            buf.add_str(sample)
            buf.guess_segment_properties()
            hb.shape(hfont, buf)
            runs[label] = [dict(glyph=font.getGlyphName(i.codepoint), cluster=i.cluster,
                                advance=p.x_advance, x=p.x_offset, y=p.y_offset)
                           for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
            if any(i.codepoint == 0 for i in buf.glyph_infos):
                failures.append(f'{weight}/{label}: .notdef in shaped output')
        shaping[str(weight)] = runs
    return dict(font=str(path.resolve()), sha256=hashlib.sha256(data).hexdigest(),
                gpos_scripts=scripts, hebrew_features=features,
                glyphs=records, shaping=shaping, failures=failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('font', type=Path)
    parser.add_argument('--json', type=Path, required=True)
    parser.add_argument('--proof-dir', type=Path)
    args = parser.parse_args()
    result = audit(args.font)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if args.proof_dir:
        args.proof_dir.mkdir(parents=True, exist_ok=True)
        for weight in (400, 550, 700):
            subprocess.run(['hb-view', str(args.font), '\n'.join(SAMPLES.values()),
                            '--direction=rtl', '--script=hebr', '--language=he',
                            f'--variations=wght={weight}', '--font-size=100',
                            '--margin=32', '--line-space=40',
                            f'--output-file={args.proof_dir / f"hebrew-{weight}.png"}'], check=True)
    print(f'{len(result["failures"])} Hebrew checks failed; report: {args.json}')
    for failure in result['failures']:
        print(f'  {failure}')
    raise SystemExit(bool(result['failures']))


if __name__ == '__main__':
    main()
