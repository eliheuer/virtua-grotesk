# avar Readiness

This generated report tracks the `avar` decision surface for Google
Fonts onboarding. The Google Fonts variable-font guide explains that a
linear interpolation can make `avar` unnecessary, while non-linear
weight progression should be encoded with an `avar` table.

## Summary

- Font: `fonts/variable/VirtuaGrotesk[wght].ttf`
- Axis: `wght` 400-700, default 400
- Has `avar`: no
- Fontspector `mandatory_avar_table` warnings: 1
- Current decision: decided

## Current Linear Mapping

| Instance | User coordinate | Normalized coordinate |
| --- | ---: | ---: |
| Regular | 400 | 0.0000 |
| Medium | 500 | 0.3333 |
| SemiBold | 600 | 0.6667 |
| Bold | 700 | 1.0000 |

## Review Options

- Keep the axis linear and record that `avar` is intentionally omitted.
- Add a non-linear `avar` mapping if Medium, SemiBold, or another
  interpolated style should sit at a different design-space pace than
  the current linear coordinates.

## Apply After Maintainer Decision

- If keeping the axis linear, record the decision in
  `documentation/google-fonts-decisions.md` and the downstream issue or
  PR notes if Fontspector still warns.
- If adding `avar`, update the source designspace/build config, rebuild,
  and regenerate `documentation/variable-font-metadata.md`,
  `documentation/google-fonts-axis-registry-audit.md`, this report, and
  Fontspector reports.

References:

- https://googlefonts.github.io/gf-guide/variable.html
- https://googlefonts.github.io/gf-guide/metadata.html
- https://github.com/fonttools/fontspector
