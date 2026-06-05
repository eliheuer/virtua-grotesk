# avar Readiness

This generated report tracks the `avar` decision surface for Google
Fonts onboarding. Virtua Grotesk keeps a linear `wght` axis and emits
an identity `avar` table so the explicit axis mapping is present
without changing interpolation.

## Summary

- Font: `fonts/variable/VirtuaGrotesk[wght].ttf`
- Axis: `wght` 400-700, default 400
- Has `avar`: yes
- Fontspector `mandatory_avar_table` warnings: 0
- Current decision: decided

## Current Axis Mapping

| Instance | User coordinate | Normalized coordinate |
| --- | ---: | ---: |
| Regular | 400 | 0.0000 |
| Medium | 500 | 0.3333 |
| SemiBold | 600 | 0.6667 |
| Bold | 700 | 1.0000 |

## Review Notes

- The current mapping is linear: 400 -> 400, 500 -> 500,
  600 -> 600, and 700 -> 700.
- The generated variable font should include an identity `avar`
  table and should not produce Fontspector's `mandatory_avar_table`
  warning.
- Add a non-linear `avar` mapping only if Medium, SemiBold, or
  another interpolated style should sit at a different design-space
  pace than the current linear coordinates.

## Apply After Mapping Changes

- Rebuild, then regenerate `documentation/google-fonts/variable-font-metadata.md`,
  `documentation/google-fonts/google-fonts-axis-registry-audit.md`, this report, and
  Fontspector reports.

References:

- https://googlefonts.github.io/gf-guide/variable.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://github.com/fonttools/fontspector
