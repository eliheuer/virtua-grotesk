"""Grid lint: enforce the two-lattice division of labor.

The Font Garden design system works on a hierarchical grid:

- 8-unit lattice — the STRUCTURE grid. Measurements (advance widths,
  stem widths, chamfer sizes) and machine-fitted geometry live here.
  Tools must emit 8-disciplined drafts; a human should never spend
  grading time snapping things to 8.
- 2-unit lattice — the CORRECTION grid. Deviations from 8 down to 2 are
  deliberate optical corrections made by eyes in Runebender. In a green
  glyph they are design data, never noise.
- off the 2-grid — always an error.

This lint reports:
  ERRORS   coordinates off the 2-grid anywhere
  ERRORS   advance widths off the 8-lattice on machine drafts (orange)
  REVIEW   advance widths off the 8-lattice elsewhere
  INFO     per-status optical density (share of coordinates off-8) —
           high density on ORANGE drafts means a tool is emitting noise

    make lint-grid   /   python scripts/grid_lint.py [--quiet]
"""

import plistlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTERS = ['Regular', 'Bold']
GREEN = '0.09,0.72,0.44,1'
RED = '1,0.29,0.24,1'


def status_of(root):
    lib = root.find('lib')
    if lib is not None:
        d = lib.find('dict')
        keys = list(d) if d is not None else []
        for i, el in enumerate(keys):
            if el.tag == 'key' and el.text == 'public.markColor':
                mark = keys[i + 1].text
                return {GREEN: 'green', RED: 'red'}.get(mark, 'orange')
    return 'unmarked'


def main():
    quiet = '--quiet' in sys.argv
    errors, review = [], []
    density = {}  # status -> [off8, total]
    for master in MASTERS:
        gdir = ROOT / f'sources/VirtuaGrotesk-{master}.ufo/glyphs'
        contents = plistlib.load(open(gdir / 'contents.plist', 'rb'))
        for name, fn in contents.items():
            root = ET.parse(gdir / fn).getroot()
            status = status_of(root)
            adv = root.find('advance')
            width = float(adv.get('width', 0)) if adv is not None else 0.0
            if width % 8:
                target = errors if status == 'orange' else review
                target.append(f'{master}/{name}: advance {width:g} off the '
                              f'8-lattice ({status})')
            outline = root.find('outline')
            for c in (outline.findall('contour') if outline is not None else []):
                for p in c.findall('point'):
                    x, y = float(p.get('x')), float(p.get('y'))
                    if x % 2 or y % 2:
                        errors.append(
                            f'{master}/{name}: point {x:g},{y:g} off the '
                            f'2-grid ({status})')
                    d = density.setdefault(status, [0, 0])
                    d[0] += (x % 8 != 0) + (y % 8 != 0)
                    d[1] += 2

    for e in errors:
        print('ERROR ', e)
    if not quiet:
        for r in review:
            print('review', r)
    print('grid lint:', f'{len(errors)} errors, {len(review)} for review')
    for status in ['green', 'unmarked', 'orange', 'red']:
        if status in density:
            off8, total = density[status]
            print(f'  optical density ({status}): {off8}/{total} '
                  f'coordinates off-8 ({100 * off8 / max(total, 1):.1f}%)')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
