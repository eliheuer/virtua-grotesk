# Batch 10 — Bold Hah family

Applied working drawings under Eli’s unattended Arabic authorization. Pending
human review; not a release approval. Baseline: `9887c4f2`.

## Scope and construction

- Redrawn Bold `hah-ar`, `.init`, `.medi`, `.fina`, preserving the compatible
  Regular topology. All Regular GLIF bytes are unchanged, including green forms.
- Shared wave head: 160-unit left terminal/nose, approximately 144-unit crown;
  16-unit exposed cuts and an 8-unit aperture landing. Descending bowls use
  160-unit sides and 176-unit bases; joining bars are 176. These remain the local
  provisional Arabic weight model, not a replacement for the Latin ladder.
- Advances now follow the actual base: 784 isolated/initial, 832 medial/final.
  Jeem/Khah wrappers and three inherited Tcheh wrappers follow those advances,
  closing the former gaps caused by 668/800/960 advances around mismatched bases.
- Bold Jeem dots were moved into the isolated/final bowls and centered beneath
  joined forms. Bold Khah dot offsets are consistent across forms. The actual
  dot donors are unchanged, including the shared Beh dependencies.
- Fifteen Bold GLIFs changed. All are purple working drawings. The recomputed
  Beh dependency reservation contains 18 files across the two masters; exact
  hashes, all source hashes, before GLIFs and candidate bytes are retained.
- No anchor or feature edits. Twenty grid findings are preserved anchor
  coordinates; all new outline points, handles, bounds and advances are on 8.

## Curve and raster review

The first draft made the inner crest too abrupt: its small left turn met a much
longer shoulder at a 6.6:1 curvature ratio. `refine.py` widens that local turn
and adjusts neighboring handles without inflating the whole head. The initial
candidate and `hah-v1-700.png` are retained as rejected evidence.

Signed profiles retain intentional reversals in the wave head and the joining
sweeps. Bowls are convex. The 8-unit aperture landing and branch cuts are corners,
not accidental smooth nodes; the erroneous Bold smooth flag on the branch cut
was removed. No sampled within-contour crossings or smooth tangent kinks remain.
G1 curvature jumps remain reported in the comb/JSON; this is not an all-G2 claim.

Inspected `hah`, `jeem`, and `khah` rasters at **400, 550 and 700**, with Before,
Working and all four references. The new Bold head has a consistent terminal and
crown, joins stay connected, and Jeem’s dots clear the bowls. Regular’s existing
final Jeem dot collides with its bowl, and Regular Khah dot heights vary; those
unchanged wrapper placements remain follow-up work. The large source Hah and
live browser Bold capture agree with the compiled silhouette. The 550 Plex panel
explicitly labels the nearest supplied static face (500).

The inherited Tcheh diagnostic exposes an existing separate problem: its three
component forms put their dot group above the letter, while the independently
drawn initial has a different head and lacks dots. This batch changes only the
three inherited base widths, not those dot groups or the independent initial.
**Tcheh remains unfinished.** `tcheh-700.png` uses three available references and
an explicit unavailable panel: this Readex Pro file has no U+0686. No fallback
font was substituted. The local recipe retains that exception visibly.

## Verification and evidence

- `verify.py`: 336 compiled shaping comparisons at 400/450/500/550/600/650/700;
  no missing glyphs or changed substitutions/clusters, only declared advance and
  interpolated component-offset deltas. Compiled changes stay in the family.
- Regular sources/advances are unchanged. Joint cubic-to-quadratic conversion
  changes subdivision/rounding in 11 compiled Regular forms: the bidirectional
  sampled outline distance is at most **0.673 source units**. See
  `regular-approximation.json`; do not claim binary-identical Regular outlines.
- `quality-check.py` and `interpolation-check.py`: sampled crossings checked
  at five source-interpolated weights; explicit curve exceptions above.
- Full master report: zero blocking mismatches, 508 width-only differences.
- `make preflight` passed build/proof/report/artifact checks. This is not a
  release-readiness or human visual-grade claim.
- `candidate.json` is the first-draft receipt. `applied.json` records the final
  refined bytes and the original before hashes. Apply scripts are historical
  reproducibility records, not instructions to rerun over human edits.

Next: inspect and repair the independent Tcheh initial base and its three-dot
placement as a bounded follow-up, preserving the reserved Beh donors; then
Ain/Ghain. Keep the protected Regular Meem and Lam–Alef follow-ups open.
