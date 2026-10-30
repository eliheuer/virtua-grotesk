# LAT-001 batch50 · Fraction coverage and construction assessment

Read-only at `bef4a002`. All 1847 source files and five active fonts remain byte
identical. Arabic 326/master and green 131 Regular/74 Bold are preserved. No
active drawing, feature, metrics, kerning, color or package change; no fresh
build/preflight/full-QA claim. Exact donor copies and current hashes are retained.

## Coverage, normalization and feature behavior

Virtua lacks U2044 FRACTION SLASH and U00BC/U00BD/U00BE, with no fraction,
numerator or denominator source donors. It also lacks `frac`, `numr` and `dnom`.
Its ordinary ASCII slash remains available. Pinned Rubik has all four encodings
and the three fraction features. NFD preserves encoded fractions. NFKD expands
them to digits plus U2044; this is compatibility decomposition, not a repair for
Virtua's missing slash or features. U2044, U002F and U2215 are distinct characters;
none has a Unicode decomposition here. Do not install ordinary-slash aliases or
normalize user text to hide the gaps.

70 full-font cases × 8 modes and 120 real text-subset cases × 8 modes at
400/475/550/625/700 are retained. Matching `.notdef` results are not coverage.
Additional 10 U2044 probes distinguish feature controls:

- Virtua returns missing glyphs for encoded fractions and fraction slash; its
  ordinary figures remain unchanged under unsupported fraction features.
- Rubik's U2044 sequences select numerators/denominators even with `frac=0`.
  Disabling `frac`, `numr` and `dnom` together restores ordinary-sized figures
  around the fraction slash in these HarfBuzz samples.
- ASCII `1/4` stays ordinary by default; enabling `frac` produces the diagonal
  fraction. `tnum+frac` produces the same proportional fraction forms in the
  sampled contexts, not tabular fractions. Rubik's fraction lookups 22–24 precede
  tnum lookup 30. Global `numr+dnom` yields numerator forms in the sampled ASCII
  run because the earlier substitution removes the later lookup's input.
- Applying `frac` to the entire date or `1/2/3` run also changes those sequences.
  A future feature needs explicit run/context policy and regression cases; do not
  infer fraction intent from every slash or add default ASCII substitutions.
- Installed fontTools default subset policy **retains frac/numr/dnom**, unlike the
  optional sups/tnum cases in batch47. All 20 cases/font/policy preserve default,
  frac, numr and dnom behavior. Default subsets drop Virtua's tnum effect and
  Rubik's sups effect for 15 of those 20 cases. Explicit feature retention restores
  them. Full mode results and actual policy list are in `fraction-details.json`.

Official reference: [OpenType frac specification](https://learn.microsoft.com/en-us/typography/opentype/spec/features_fj#tag-frac)
permits application-driven U2044 handling and distinguishes it from discretionary
ASCII fraction formatting. The [Unicode punctuation chart](https://www.unicode.org/charts/PDF/U2000.pdf)
and local Unicode 15.1 decomposition data were inspected. No reference outlines
were imported.

## Construction and protected sources

The recomputed ordinary/tabular/superior/slash reverse closure contains 39 glyphs
per master and no Arabic-reserved intersection. Ordinary one/two/three/four are
green, including unlabeled RGBA green records. Existing superiors are purple,
unapproved drafts. Slash/backslash are yellow Regular/orange Bold, not approved
construction references; their bytes/grades remain untouched. Supplemental
X/x/seven guards find green x/seven in both masters, green Regular X and orange
Bold X. Only the green forms can establish diagonal construction/weight. This
three-member reverse closure also has no Arabic intersection.

Actual Rubik fractions use a broad diagonal slash with substantial side overhang
and a small advance, allowing numerator and denominator to nest beside it. At a
1024-normalized em, its slash has y0–716.8 and about180/183 advance, with bounds
about −199…394 Regular and −211…412 Bold. These measurements describe the
comparison, not target coordinates. Existing Virtua ASCII slash instead has
416 advance and x32…384/y0…768 in both masters; it is a steeper, differently
spaced construction and should not become an automatic U2044 alias.

Rubik's encoded superior digits and corresponding numerator glyphs have exactly
matching decomposed outlines and advances in all 50 digit/weight comparisons.
That is evidence about Rubik only. Virtua's superior baseline is384, nominal
height384 with overshoots; a potential fraction system must separately verify
position, weight, slash clearance and denominator alignment. No existing elevated
superior has been installed as a fraction numerator or denominator here. Retain
Virtua's curved one flag, rounded two/three construction and four counter, using
green ordinary figures as construction authority. New geometry/offsets/spacing
must be on8, preserve optical exceptions, and remain purple pending human review.

## Actual visual evidence and next bounded work

Five whole raster images were inspected: 48px400/550/700 forms, feature contexts,
and224px endpoint details. Nine actual browser screenshots were inspected:
three controlled two-column fixtures and six Diffenator target views. Controlled
Virtua fractions show small serif fallback ink and U2044 sequences retain large
ordinary figures; fallback fonts were not identified. Diffenator shows boxes for
missing Virtua characters. Rubik's fraction sequences nest legibly, while global
feature application visibly changes multi-slash runs. Regular Virtua superior
2/3 remain lighter than Rubik; Bold family mass/spacing still await human review.
Rubik acute/cedilla on encoded fractions use generic placement, not evidence of
special fraction anchors. Stock Diffenator was generated; unchanged batch49
stock review is referenced, not claimed repeated. Font/image hashes and sampled
scope are recorded. No human or native-reader approval.

Next: prepare a bounded purple `fraction` U2044 draft in both masters on scratch
sources using green Virtua diagonal weight/construction. Test its wider slope,
overhang and advance with clearly labeled scratch fraction-layout trials before
application; do not modify ASCII slash or claim that slash coverage alone gives
fraction shaping. Then assess dedicated numerator1/3 and denominator2/4 forms for
encoded quarter/half/threequarters, including a reviewed full figure-family and
feature scope if numr/dnom/frac are later added. Do not apply a partial feature or
blindly reuse the elevated superior family. Batch47's digit-only sups proposal
remains separate and unapplied.

Latest full online package QA remains **batch49:12FAIL/10WARN/159PASS/10INFO/40SKIP**.
The 216 Hebrew baseline failures, serving reachability, soft-hyphen retain/omit
policy and optical blockers remain. Pinned Rubik gap327 remains182 Cyrillic/
43 Common/102 Arabic presentation forms. No exclusions or subset changes.
Local only/no push; Arabic60272 and its current case/layout unchanged.

Previews: http://127.0.0.1:60273/batch50/comparison-400.html and
http://127.0.0.1:60273/batch50/comparison/fractions.html.
