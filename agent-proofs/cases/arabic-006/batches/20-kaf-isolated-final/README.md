# Batch 20 — Bold Kaf isolated and final

Applied under Eli's standing autonomous authorization; pending human review.
Only `Bold kaf-ar` and `Bold kaf-ar.fina` are changed. All Regular sources,
including green final Kaf, are byte-identical. No component descendants exist
for these two Bold drawings. The recursive 18-file Beh reservation and manual
hamza are unchanged. Exact source baseline, candidates and hashes are retained
in `applied.json`, `before-sources/` and `candidate-sources/`.

## Diagnosis and construction

The former Bold bowl handles reversed direction, cap/terminal cuts were swollen,
and the small Kaf sign had pinched turns and inconsistent mass. The repaired
bowls use 160-unit upright strokes, a 176-unit base/join, 16-unit exposed cuts,
axis-tangent turns and a continuous final joining baseline. Advances are 864
isolated and 896 final. The extra final baseline segments remain collinear for
compatibility with protected Regular; they do not add bumps or coincident nodes.

A large raster caught an over-dominant inner sign after the first geometry pass.
The final sign occupies x296–536, y304–592, with 64-unit horizontal bars,
72-unit side strokes, 48-unit apertures and 16-unit terminal cuts. This is a
local proportion choice, not a new global weight rule. The existing rounded
sign skeleton is retained; no reference outlines were copied.

## Verification and visual observations

- Matching contour/type structure: isolated 24+36, final 32+36 points.
- Zero draft-grid findings, including anchors and widths; signed profiles have
  no sampled reversals, tangent kinks or undefined joins. Line/curve G1 curvature
  jumps remain in `curves.txt`; do not claim all joins are G2. Collinear final
  baseline runs are intentional compatibility structure.
- No sampled self/inter-contour crossings at 400, 475, 550, 625, 700.
- 679 compiled shaping comparisons across seven weights; only these two glyphs
  change in the compiled font. Weight 400 remains unchanged.
- Inspected all-four-reference rasters at 400/550/700, large source renders,
  final joins `بك ك`, marked isolated forms, and `كتاب كوكب` word contexts.
  The 550 Plex reference is explicitly the nearest supplied weight, 500.
- Preflight completed; this establishes artifacts and source/build checks,
  not reader approval or Google Fonts readiness.

The changed bowls and final join render without the former spikes, and the
smaller inner signs have visible separation from the bowl. The 550 proof still
inherits Regular's final underside bulge; Regular was intentionally preserved.
Marked isolated forms are shown without changing anchors or diacritics.

## Unresolved / next

The four-reference comparison exposes a structural issue in initial and medial
Kaf: Virtua's initial is a horizontal S-like construction, while the references
have an angled head; Virtua medial retains the isolated-style upright and inner
sign. Passing curve checks cannot establish correct contextual letter design.
Regular initial Kaf is green; a structural change requiring its topology must
not silently modify it. Regular medial is orange. Prepare that scope separately
and keep this mismatch visible, rather than claiming this family complete.

Continue with independent Keheh/Gaf bases and their local wrappers next. Preserve
Beh, green donors/descendants and the protected Regular initial/final Kaf.
