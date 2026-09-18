#!/usr/bin/env python3
"""Prepare Hebrew anchor candidates in a NEW scratch source directory.

Never writes active sources. Review rendered attachment, then explicitly port
selected GLIFs; purple source glyphs need owner approval before replacement.
No Rubik outlines or coordinates are copied. Placement uses Virtua bounds and
its existing dagesh composites. Blue candidates still require optical review.
"""
import argparse
import json
from pathlib import Path
import plistlib
import re
import shutil

from defcon import Font

ROOT = Path(__file__).resolve().parents[1]
BLUE = '0.27,0.44,1,1'


def even(value):
    return int(round(value / 2) * 2)


def anchors(font, glyph):
    cp = glyph.unicode
    if cp is None or glyph.bounds is None:
        return []
    x0, y0, x1, y1 = glyph.bounds
    cx = even((x0 + x1) / 2)
    if 0x05B0 <= cp <= 0x05B8 or cp in (0x05BB, 0x05C7):
        return [('_hbBottom', cx, 0)]
    if cp in (0x05B9, 0x05BA):
        return [('_hbHolam', cx, 576)]
    if cp == 0x05BC:
        return [('_hbCenter', cx, even((y0 + y1) / 2))]
    if cp in (0x05C1, 0x05C2):
        return [('_hbShin' if cp == 0x05C1 else '_hbSin', cx, 576)]
    if not (0x05D0 <= cp <= 0x05EA or 0xFB2A <= cp <= 0xFB4B):
        return []
    bottom_y = 240 if cp in (0x05DA, 0xFB3A) else 0
    # Descending strokes must clear vowels. Final kaf takes its vowel inside.
    if cp in (0x05DF, 0x05E3, 0x05E5, 0xFB43):
        bottom_y = even(min(0, y0))
    center_x, center_y = cx, 320
    composite_name = glyph.name.replace('-hb', 'dagesh-hb')
    if composite_name in font and len(font[composite_name]) > len(glyph):
        dot = font[composite_name][-1].bounds
        if dot:
            center_x, center_y = even((dot[0] + dot[2]) / 2), even((dot[1] + dot[3]) / 2)
    if cp in (0x05D5, 0x05D9):
        center_x, center_y = even(x0 - 72), 320
    top = max(576, even(y1))
    holam_x = cx if cp == 0x05D5 else even(x0)
    result = [('hbBottom', cx, bottom_y), ('hbCenter', center_x, center_y),
              ('hbHolam', holam_x, top)]
    if cp == 0x05E9 or 0xFB2A <= cp <= 0xFB2D or cp == 0xFB49:
        result += [('hbShin', even(x1 - 48), top), ('hbSin', even(x0 + 48), top)]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='New directory for scratch sources')
    args = parser.parse_args()
    target = args.destination.resolve()
    if target.exists():
        parser.error('Destination must not exist; preserve previous candidates for comparison')
    shutil.copytree(ROOT / 'sources', target, ignore=shutil.ignore_patterns('archive', 'instance_ufos'))
    changed = []
    for master in ('Regular', 'Bold'):
        ufo = target / f'VirtuaGrotesk-{master}.ufo'
        font = Font(ufo)
        contents = plistlib.loads((ufo / 'glyphs/contents.plist').read_bytes())
        for glyph in font:
            values = anchors(font, glyph)
            if not values:
                continue
            if glyph.anchors:
                raise ValueError(f'{master}/{glyph.name}: existing anchors need review')
            path = ufo / 'glyphs' / contents[glyph.name]
            text = path.read_text()
            block = ''.join(f'\t<anchor x="{x}" y="{y}" name="{name}"/>\n' for name, x, y in values)
            text = text.replace('\t<outline>', block + '\t<outline>', 1)
            text = re.sub(r'(<key>public.markColor</key>\s*<string>)[^<]+',
                          lambda m: m[1] + BLUE, text)
            text = re.sub(r'(<key>com.runebender.markLabel</key>\s*<string>)[^<]+',
                          lambda m: m[1] + 'blue', text)
            path.write_text(text)
            changed.append(dict(master=master, glyph=glyph.name, original_color=str(glyph.markColor), anchors=values))
        # Explicit categories disable inference for uncategorized bases in ufo2ft.
        libpath = ufo / 'lib.plist'
        libtext = libpath.read_text()
        categories = font.lib.get('public.openTypeCategories', {})
        missing = [g.name for g in font if anchors(font, g)
                   and not anchors(font, g)[0][0].startswith('_') and g.name not in categories]
        block = ''.join(f'\t\t<key>{name}</key>\n\t\t<string>base</string>\n'
                        for name in sorted(missing))
        libtext, count = re.subn(r'(<key>public.openTypeCategories</key>\s*<dict>\n)',
                                lambda match: match[1] + block, libtext, count=1)
        if count != 1:
            raise ValueError('Expected explicit public.openTypeCategories dictionary')
        libpath.write_text(libtext)
        feature = ufo / 'features.fea'
        text = feature.read_text()
        if 'languagesystem hebr dflt;' not in text:
            feature.write_text(text.replace('languagesystem DFLT dflt;',
                                             'languagesystem DFLT dflt;\nlanguagesystem hebr dflt;', 1))
    (target / 'hebrew-anchor-candidates.json').write_text(json.dumps(changed, indent=2) + '\n')
    print(f'Prepared {len(changed)} glyph/master anchor candidates in {target}')


if __name__ == '__main__':
    main()
