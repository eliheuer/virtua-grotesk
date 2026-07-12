# Master Compatibility Report

Regular master: `sources/VirtuaGrotesk-Regular.ufo`
Bold master: `sources/VirtuaGrotesk-Bold.ufo`

Blocking structure mismatches: 7
Width-only differences: 204

This report checks glyph-set presence, Unicode assignments, contour point types/counts, component bases, and anchors. Width differences are expected across the Weight axis and are reported separately.

## Summary

| Category | Count |
| --- | ---: |
| Missing in Regular | 0 |
| Missing in Bold | 0 |
| Unicode mismatches | 0 |
| Contour structure mismatches | 7 |
| Component mismatches | 0 |
| Anchor mismatches | 0 |
| Width-only differences | 204 |

## Blocking Mismatches

| Glyph | Issue | Detail | Action |
| --- | --- | --- | --- |
| `a.bold` | Contour structure mismatch | Regular points [39, 12] / Bold points [0] | Must match for variable interpolation. |
| `asciicircum` | Contour structure mismatch | Regular points [7] / Bold points [0] | Must match for variable interpolation. |
| `backslash` | Contour structure mismatch | Regular points [4] / Bold points [0] | Must match for variable interpolation. |
| `bracketleft` | Contour structure mismatch | Regular points [4, 4, 4] / Bold points [0] | Must match for variable interpolation. |
| `bracketright` | Contour structure mismatch | Regular points [4, 4, 4] / Bold points [0] | Must match for variable interpolation. |
| `grave` | Contour structure mismatch | Regular points [4] / Bold points [0] | Must match for variable interpolation. |
| `underscore` | Contour structure mismatch | Regular points [4] / Bold points [0] | Must match for variable interpolation. |
