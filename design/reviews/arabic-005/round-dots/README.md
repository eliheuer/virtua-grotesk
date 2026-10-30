# ARB-005 correction — Round Arabic letter dots

2026-10-21: Eli said the Beh bases looked better, but the dots should be close
to perfect circles, following https://elih.net/blog/virtua-grotesk/.
Confirmed preference is promoted to DESIGN.md. This applies to Arabic letter
dots, not an instruction to circularize vowel marks or undo Hebrew decisions.

## Exact scope

Two red Bold donors: `dotbelow-ar` and `dotabove-ar`. Green Regular dots already
have symmetric 160-unit diameter circles (44-unit handles on the human 2-grid)
and remain byte-identical. Bold's skewed 232×216 outlines become symmetric
224×224 four-cubic circles: radius 112, equal tangent handles 64. Centers remain
(120,-192) below and (152,768) above; anchors and advances are unchanged.
All new outline coordinates lie on 8. The two new drawings are purple under
the AI-unreviewed convention; no dependent source colors change.

The dependency closure contains 47 glyphs including these donors, none green
in Bold. Multi-dot drawings that do not reference these donors are outside
this correction. Their existing distortion/placement remains future work.
No bases, feature code, dot component placements or diacritics are changed.

`before-sources/` retains both masters; `candidate-sources/` retains the two
Bold trials. `candidate.json` and `applied.json` freeze all source hashes at the
already-applied Beh base trial. `assets/before.ttf` is that exact trial's built
font, so this comparison isolates the dot change. The original base trial and
its proof remain in the parent folder; do not rerun its older verification
script against these later sources and call the expected scope mismatch a
base regression.

## Validation

- Build and `make preflight` passed; source master structures remain compatible.
- `verify.py`: 147 shaped comparisons over seven weights, all substitutions,
  offsets and advances unchanged. Compiled changes stay within the dot dependency
  closure. Exact hashes confirm only two Bold GLIFs changed from this baseline;
  the prior Beh bases and all Regular source bytes are unchanged.
- `radial-check.json`: 1,001 samples per quarter at 13 weights; maximum sampled
  Bold radial deviation 1.1371 units (about 1.02% of radius). This is a near-circle
  on the 8-grid, not a mathematically exact rational circle or proof of visual
  approval. Corresponding source curves interpolate as symmetric quarters.
- `curves.json` and `comb.svg`: the old Bold has four tangent kinks; new Bold
  quarters meet with G2 continuity and no sampled sign reversals. The common-
  scale comb was visually inspected.
- Full grid report retains 21 findings: human Regular handles and existing
  metrics/anchors. Bold's four findings are retained below-dot `_bottomDots.x`
  124, `bottom.x` 124 and `bottom.y` -306, plus above-dot `top.y` 812. See the exact
  JSON rather than assuming all glyph metadata passes. New outline points and
  handles pass the 8-unit lattice; no attachment normalization was performed.
- Browser proof retains `ببب ب` and all four reference families, with separate
  above-dot contexts. Existing Noon-context dot crowding is visible in Before
  and Working; this correction changes shape, not component placement.

Status: applied working correction for visual review, not committed or graded.
