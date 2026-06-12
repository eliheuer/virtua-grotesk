---
name: font-qa
description: Run quality assurance checks on the font sources: metrics consistency, master compatibility, and kerning sanity. Use before handoff or when verifying source health.
---

# /font-qa

Run quality assurance checks on the font sources.

## Usage
`/font-qa [--check metrics|masters|kerning|all]`

Default: `all`

## Checks

### `metrics`
Verify font metrics consistency between masters:
1. Read `fontinfo.plist` from both Regular and Bold masters
2. Compare: `unitsPerEm`, `ascender`, `descender`, `capHeight`, `xHeight`
3. Report any mismatches — these values should be identical between masters

### `masters`
Verify glyph compatibility between Regular and Bold:
1. Read `glyphs/contents.plist` from both masters
2. Compare glyph inventories — report any glyphs present in one but not the other
3. For each glyph present in both masters:
   - Read both `.glif` files
   - Count contours and points per contour
   - Compare point types (line, curve, off-curve)
   - Report any mismatches with specific details

This is the most important check — incompatible masters will cause the variable font build to fail.

**Performance note:** For a full check of all glyphs, use Python with fontTools:
```bash
./venv/bin/python -c "
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib import UFOReader
import sys

ds = DesignSpaceDocument.fromfile('sources/VirtuaGrotesk.designspace')
regular = UFOReader('sources/VirtuaGrotesk-Regular.ufo')
bold = UFOReader('sources/VirtuaGrotesk-Bold.ufo')

reg_glyphs = set(regular.getGlyphSet().keys())
bold_glyphs = set(bold.getGlyphSet().keys())

only_regular = reg_glyphs - bold_glyphs
only_bold = bold_glyphs - reg_glyphs

if only_regular:
    print(f'Only in Regular ({len(only_regular)}): {sorted(only_regular)}')
if only_bold:
    print(f'Only in Bold ({len(only_bold)}): {sorted(only_bold)}')
if not only_regular and not only_bold:
    print(f'Glyph inventories match: {len(reg_glyphs)} glyphs')

# Check contour/point compatibility
reg_gs = regular.getGlyphSet()
bold_gs = bold.getGlyphSet()
issues = []

from fontTools.pens.pointPen import AbstractPointPen

class CountPen(AbstractPointPen):
    def __init__(self):
        self.contours = []
        self._current = []
    def beginPath(self, **kwargs):
        self._current = []
    def endPath(self):
        self.contours.append(len(self._current))
    def addPoint(self, pt, segmentType=None, **kwargs):
        self._current.append(segmentType)
    def addComponent(self, glyphName, transformation, **kwargs):
        pass

common = reg_glyphs & bold_glyphs
for gname in sorted(common):
    rp = CountPen()
    bp = CountPen()
    reg_gs[gname].drawPoints(rp)
    bold_gs[gname].drawPoints(bp)
    if len(rp.contours) != len(bp.contours):
        issues.append(f'{gname}: contour count {len(rp.contours)} vs {len(bp.contours)}')
    elif rp.contours != bp.contours:
        issues.append(f'{gname}: point counts differ {rp.contours} vs {bp.contours}')

if issues:
    print(f'\nCompatibility issues ({len(issues)}):')
    for i in issues:
        print(f'  - {i}')
else:
    print(f'All {len(common)} common glyphs are compatible')
"
```

### `kerning`
Validate kerning structure:
1. Check if both masters have kerning files
2. If both exist, verify groups are identical between masters
3. Verify all group references in kerning.plist exist in groups.plist
4. Check for orphaned groups (defined but never used in kerning)
5. Report pair counts per master

### `all`
Run all checks in sequence: metrics → masters → kerning. Summarize with a pass/fail status for each.
