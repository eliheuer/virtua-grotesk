# Google Fonts Production Requirements Audit

This generated report maps current built fonts and source evidence to
Google Fonts production and font-file requirements that can be checked
locally. It separates satisfied engineering requirements from drawing,
source-feature, and maintainer-decision blockers.

## Summary

- Built TTF outputs present: yes
- All handoff font binaries are `.ttf`: yes
- One-command build path present: yes
- Open-source build toolchain documented: yes
- Source UFO/designspace inputs present: yes
- Installable embedding fsType across built fonts: yes
- Version strings match first-submission version `1.000`: yes
- Vertical metrics match GF source metrics: yes
- Variable font has `fvar`: yes
- Variable font has `STAT`: yes
- Variable `wght` axis includes 400: yes
- Variable `fvar` instance names are GF-allowed: yes
- Tabular Numbers (`tnum`) feature present in any built font: yes
- Default ASCII digits are proportional in every built font: yes
- `tnum` substitutes all ten ASCII digits in every built font: yes
- `tnum` substitutes to equal-width digits in every built font: yes
- Numeric feature requirement ready: yes
- GF Latin Core missing codepoints: 0
- GF Arabic Core missing codepoints: 0
- Fontspector googlefonts profile: 10 FAIL, 20 WARN, 517 PASS
- Open maintainer decisions: 2
- Decided maintainer decisions: 13
- Open decision names: Private-use icon block, Kerning

## Built Font Requirements

| Font | Exists | TTF | fsType | Version | Typo metrics | hhea metrics | tnum |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | yes | yes | 0 | `Version 1.000` | `1024/-296/0` | `1024/-296/0` | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | yes | yes | 0 | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | `1024/-296/0` | `1024/-296/0` | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | yes | yes | 0 | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | `1024/-296/0` | `1024/-296/0` | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | yes | yes | 0 | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | `1024/-296/0` | `1024/-296/0` | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | yes | yes | 0 | `Version 1.000; ttfautohint (v1.8.4.16-eb64)` | `1024/-296/0` | `1024/-296/0` | yes |

## Variable Font Requirements

- Filename: `VirtuaGrotesk[wght].ttf`
- Filename uses GF axis-bracket convention: yes
- Axis tags: `wght`
- `wght` min/default/max: 400/400/700
- `fvar` instances: Regular 400, Medium 500, SemiBold 600, Bold 700
- `avar` present: yes

## Outstanding Requirement Buckets

- Drawing/source coverage: complete GF Latin Core and GF Arabic Core coverage.
- Numeric feature status: default ASCII digits are proportional and the
  current `tnum` feature substitutes all ten digits to equal-width
  tabular alternates, so numeric feature readiness is no longer a
  production blocker.
- Fontspector: resolve current FAILs, or record explicit Google Fonts
  reviewer acceptance for any remaining FAIL before submission.
- Maintainer decisions: only the open decisions listed above remain
  unresolved here; decided items stay covered by their dedicated
  readiness reports and preflight checks.

## Evidence Reports

- `documentation/upstream-structure-readiness.md`
- `documentation/source-ufo-metadata.md`
- `documentation/generated-font-metadata.md`
- `documentation/variable-font-metadata.md`
- `documentation/numeric-feature-readiness.md`
- `documentation/google-fonts-axis-registry-audit.md`
- `documentation/missing-gf-latin-core.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/fontspector-googlefonts-report.md`

References:

- https://googlefonts.github.io/gf-guide/production.html
- https://googlefonts.github.io/gf-guide/requirements.html
- https://googlefonts.github.io/gf-guide/variable.html
- https://googlefonts.github.io/gf-guide/statics.html
- https://googlefonts.github.io/gf-guide/build.html
