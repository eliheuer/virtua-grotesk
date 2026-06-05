# Arabic Mark Triage

This generated report supports visual-review batch 3:
`Marks, Dotted Circle, And Stacking`. It shapes the same samples used
by `documentation/glyph-review/arabic-mark-review-proof.html` and records mechanical
risks that AI can pre-triage before hand review.

It does not approve mark placement. Zero-position offsets can be valid
for this source if marks are drawn at their intended origin, so those
rows remain hand-review prompts, not automatic failures.

## Summary

- Fonts checked: 5
- Review sections checked: 8
- Shaped sample rows: 370
- Mechanical blocking risks: 0
- No-offset mark review prompts: 10

## Review Sections

| Review row | Section | Samples |
| --- | --- | ---: |
| `mark-base+fatha` | Base plus fatha | 8 |
| `mark-base+damma` | Base plus damma | 8 |
| `mark-base+kasra` | Base plus kasra | 8 |
| `mark-shadda+sukun` | Shadda and sukun stacking | 8 |
| `mark-tanween` | Tanween | 8 |
| `mark-hamza-above-below` | Hamza above and below | 8 |
| `mark-dotted-circle` | Dotted circle | 10 |
| `class-mark-combinations` | Required mark inventory | 16 |

## Risk Counts

| Risk | Rows |
| --- | ---: |
| `no-mark-position-offset-observed` | 10 |

## Mechanical Blocking Rows

| Review row | Font | Sample | Glyph sequence | Risks |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## No-Offset Review Prompt Summary

These rows need visual inspection in the proof. They are not automatic
failures because this source can place marks at their intended origin.

| Review row | Font | Samples | Sample texts |
| --- | --- | ---: | --- |
| `mark-shadda+sukun` | Bold | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Medium | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Regular | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | SemiBold | 2 | `بُّ`, `بَّ` |
| `mark-shadda+sukun` | Variable | 2 | `بُّ`, `بَّ` |

## No-Offset Review Prompt Rows

| Review row | Font | Sample | Glyph sequence | Source edit targets |
| --- | --- | --- | --- | --- |
| `mark-shadda+sukun` | Bold | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Bold | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Medium | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Medium | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Regular | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Regular | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | SemiBold | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | SemiBold | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Variable | `بَّ` | `uni0651064E adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaFatha-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaF_atha-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |
| `mark-shadda+sukun` | Variable | `بُّ` | `uni0651064F adv=0,0 off=0,0`<br>`uni0628 adv=600,0 off=0,0` | `VirtuaGrotesk-Regular.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `shaddaDamma-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/shaddaD_amma-ar.glif`<br>`VirtuaGrotesk-Regular.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/beh-ar.glif`<br>`VirtuaGrotesk-Bold.ufo` `beh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/beh-ar.glif` |

## Next Manual Action

Open these together for the mark review batch:

- `documentation/glyph-review/arabic-mark-review-proof.html`
- `documentation/glyph-review/arabic-mark-readiness.md`
- `documentation/glyph-review/arabic-manual-review-dashboard.html`

Record the eight batch-3 rows in
`documentation/glyph-review/arabic-visual-review-log.md` after hand inspection.
