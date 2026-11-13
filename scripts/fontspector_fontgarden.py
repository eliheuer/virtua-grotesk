#!/usr/bin/env python3
"""Fontspector plugin with the Font.Garden profile.

The profile `fontgarden` includes the Google Fonts profile and adds the
Font.Garden requirements:

    fontgarden/unitsperem  the em is 1024 units
    fontgarden/grid        every master of a variable font has its on-curve
                           points and advance widths on the 2-unit grid
    fontgarden/vendor_id   the OS/2 vendor ID is FTGD
    fontgarden/license     the name table gives the OFL 1.1 and its URL

    fontspector --plugin scripts/fontspector_fontgarden.py -p fontgarden FONT...

Add a requirement as a check here, with the reason in its rationale.
"""
from __future__ import annotations

import io
from pathlib import Path

from fontspectorapi import FAIL, PASS, SKIP, CheckContext, CheckStatuses, Message, Plugin
from fontspectorapi import ProfileDefinition, check, plugin_main
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

UNITS_PER_EM = 1024
GRID = 2
VENDOR_ID = 'FTGD'
LICENSE = 'SIL Open Font License, Version 1.1'
LICENSE_URL = 'https://openfontlicense.org'
ARTICLE = 'https://elih.net/blog/virtua-grotesk/'


@check(id='fontgarden/unitsperem', title='The em is 1024 units',
       rationale='The Font.Garden grid divides the em by powers of two. 1024 is 2 to the '
                 'power 10, so the grids of 2, 8 and 64 units and the vertical metrics '
                 'are whole numbers.',
       proposal=ARTICLE)
def units_per_em(font_path: Path, context: CheckContext) -> CheckStatuses:
    upm = TTFont(font_path)['head'].unitsPerEm
    if upm == UNITS_PER_EM:
        yield PASS, Message('ok', f'unitsPerEm is {upm}.')
    else:
        yield FAIL, Message('wrong-upm', f'unitsPerEm is {upm}, not {UNITS_PER_EM}.')


@check(id='fontgarden/vendor_id', title='The OS/2 vendor ID is FTGD',
       rationale='FTGD is the registered vendor ID of Font.Garden.')
def vendor_id(font_path: Path, context: CheckContext) -> CheckStatuses:
    found = TTFont(font_path)['OS/2'].achVendID
    if found == VENDOR_ID:
        yield PASS, Message('ok', f'The vendor ID is {found}.')
    else:
        yield FAIL, Message('wrong-vendor-id', f'The vendor ID is "{found}", not {VENDOR_ID}.')


@check(id='fontgarden/license', title='The name table gives the OFL 1.1',
       rationale='Font.Garden fonts are licensed under the SIL Open Font License 1.1. '
                 'Name ID 13 gives the license and name ID 14 its URL.',
       proposal=LICENSE_URL)
def license_names(font_path: Path, context: CheckContext) -> CheckStatuses:
    name = TTFont(font_path)['name']
    description, url = name.getDebugName(13) or '', name.getDebugName(14) or ''
    failed = False
    if LICENSE not in description:
        failed = True
        yield FAIL, Message('license-description', f'Name ID 13 does not contain "{LICENSE}".')
    if url != LICENSE_URL:
        failed = True
        yield FAIL, Message('license-url', f'Name ID 14 is "{url}", not {LICENSE_URL}.')
    if not failed:
        yield PASS, Message('ok', 'The name table gives the OFL 1.1 and its URL.')


def master_locations(font):
    """User-space locations of the masters of a variable font: the default
    location and the peak of each gvar tuple."""
    axes = {a.axisTag: a for a in font['fvar'].axes}
    avar = font['avar'].segments if 'avar' in font else {}
    peaks = {tuple(sorted((tag, value[1]) for tag, value in v.axes.items()))
             for variations in font['gvar'].variations.values() for v in variations}
    locations = [{tag: a.defaultValue for tag, a in axes.items()}]
    for peak in sorted(peaks):
        location = {tag: a.defaultValue for tag, a in axes.items()}
        for tag, value in peak:
            value = invert(avar.get(tag), value)
            a = axes[tag]
            span = a.maxValue - a.defaultValue if value > 0 else a.defaultValue - a.minValue
            location[tag] = a.defaultValue + value * span
        locations.append(location)
    return locations


def invert(segments, value):
    """The normalized value that the avar segment map maps to `value`."""
    if not segments:
        return value
    pairs = sorted(segments.items(), key=lambda pair: pair[1])
    for (a, b), (c, d) in zip(pairs, pairs[1:]):
        if b <= value <= d:
            return a if d == b else a + (value - b) * (c - a) / (d - b)
    return value


def off_grid(font):
    """Glyphs with an on-curve point or an advance width off the grid."""
    glyf, hmtx, found = font['glyf'], font['hmtx'], {}
    for name in font.getGlyphOrder():
        problems = []
        if hmtx[name][0] % GRID:
            problems.append(f'advance {hmtx[name][0]}')
        glyph = glyf[name]
        if glyph.numberOfContours > 0:
            coordinates, _, flags = glyph.getCoordinates(glyf)
            # Optimized gvar deltas leave a master up to half a unit off its
            # source, so compare the rounded coordinates.
            points = [(round(x), round(y)) for (x, y), flag in zip(coordinates, flags)
                      if flag & 1 and (round(x) % GRID or round(y) % GRID)]
            if points:
                problems.append(f'{len(points)} points, for example {points[0]}')
        if problems:
            found[name] = ', '.join(problems)
    return found


@check(id='fontgarden/grid', title='The masters are on the 2-unit grid',
       rationale='Every point of a Font.Garden source is on the 2-unit grid, so that a '
                 'coordinate tells its grid level. The quadratic conversion moves the '
                 'off-curve points, so this check reads the on-curve points and the '
                 'advance widths of every master of the variable font. Static fonts are '
                 'instances, mostly between masters, so they are not checked.',
       proposal=ARTICLE)
def grid(font_path: Path, context: CheckContext) -> CheckStatuses:
    font = TTFont(font_path)
    if 'fvar' not in font:
        yield SKIP, Message('static', 'A static font is an instance; the masters are checked '
                                      'in the variable font.')
        return
    failed = False
    for location in master_locations(font):
        buffer = io.BytesIO()
        font.save(buffer)
        found = off_grid(instancer.instantiateVariableFont(TTFont(buffer), location))
        if found:
            failed = True
            lines = '\n'.join(f'- {name}: {problem}' for name, problem in sorted(found.items()))
            yield FAIL, Message('off-grid', f'At {location}, {len(found)} glyphs are off the '
                                            f'{GRID}-unit grid:\n{lines}')
    if not failed:
        yield PASS, Message('ok', f'All masters are on the {GRID}-unit grid.')


def register(plugin: Plugin) -> None:
    checks = [units_per_em, grid, vendor_id, license_names]
    for fn in checks:
        plugin.register_check(fn)
    # An included profile does not bring its exclusions and configuration, so
    # these are copied from the googlefonts profile of Fontspector 1.9.0.
    plugin.register_profile('fontgarden', ProfileDefinition(
        sections={'Font.Garden': [fn._fontspector_check['id'] for fn in checks]},
        include_profiles=['googlefonts'],
        exclude_checks=['cmap/format_12', 'empty_letters', 'inconsistencies_between_fvar_STAT',
                        'no_mac_entries', 'typographic_family_name', 'vtt_volt_data'],
        configuration_defaults={
            'file_size': {'WARN_SIZE': 1048576, 'FAIL_SIZE': 9437184, 'FATAL_SIZE': 10485760},
            'googlefonts/family/file_size': {'FATAL_SIZE': 26214400}}))


if __name__ == '__main__':
    raise SystemExit(plugin_main(register, plugin_name='fontgarden'))
