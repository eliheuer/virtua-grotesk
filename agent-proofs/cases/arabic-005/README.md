# ARB-005 — Beh base forms

Eli requested the next small Arabic base loop, both weights and four reference
families, with joined-plus-isolated text such as `ببب ب` to expose all four forms.
The trailing backslash in the message is not part of the Arabic sample.

Scope: Bold `behDotless-ar`, `.init`, `.medi`, `.fina`. Their Regular drawings
are green and remain byte-identical. Before: `211c3b8d`. This is one shared base
family: 41 Bold dependent glyphs inherit the four outlines; none is green.
The component closure is retained in `candidate.json`. No dots, diacritics,
attachment anchors, composite wrappers or features are edited.

## Construction trial

Keep Regular's skeleton and compatible point order. Bold has 168-unit uprights,
176-unit connecting bars, 16-unit terminal chamfers and an intentional 8-unit
underside shelf. Straight-to-curve joins are axis tangent. The old Bold's
reversing inner handles, kinks and 34×36 terminal cuts are replaced with bounded
turns and straight terminal runs. Isolated outer x extents return to Regular's
64–880; weight grows into the counter. Other forms follow their own join geometry,
not a uniform scale. Terminal tops are 336 for the bowl/medial/final and 432 for
initial. Root advances match existing Beh wrappers: 944/288/416/1024; wrappers'
advances remain untouched. This also fixes medial's old extension beyond its
wrapper advance (x516 vs 416). These are trial proportions, not universal rules.

The four red Bold roots become purple under the existing AI-unreviewed convention;
no dependent source color is changed and no human grade is assigned.

## Curve and lattice evidence

Before/after signed combs are retained per form. Old curves show ten sampled
sign reversals across the four forms; the candidate shows none. Tangent kinks
are removed. Deliberate chamfers, joining seams and underside shelf remain
corners rather than being harmonized away. This reuses ARB-003's diagnostic
lesson, not the hamza's dimensions or handle ratios.

New Bold outline points, handles, widths and ink sidebearings are on 8.
The full grid report also reports existing off-grid attachment anchors and
protected Regular geometry. These are preserved deliberately: this is a base
outline pass, not a mark-placement or green-source normalization pass. Do not
report the whole glyph-master grid check as passing.

`prepare.py` is a one-shot evidence preparation script; `apply.py` checks every
baseline source hash before installation. Exact snapshots preserve all four
Regular donors and the four Bold before/candidate pairs. The proof uses actual
Arabic shaping of `ببب ب`, never manually substituted presentation characters.

## Verification and review state

- `make preflight` passed: variable and static builds, proof, compatibility
  reports and artifact-presence checks. This is not release certification.
- `verify.py` passed 112 shaped before/after comparisons over seven weights.
  The four Beh forms are distinct in `ببب ب`; substitutions, offsets and advances
  in the tested contexts are unchanged. All 45 changed compiled glyphs belong
  to the recorded four-base dependency closure. Only the four base advances
  change; encoded Beh wrappers retain their advances.
- Every Regular source byte is unchanged. Because cu2qu selects compatible
  subdivisions across masters, the Regular compiled quadratics are not byte-
  identical. Sampled symmetric outline deviations for the four bases are
  0.459/0.441/0.436/0.667 units; these are approximation differences, not source
  drawing changes. Preserve this distinction in later comparisons.
- The nine Bold grid findings are unchanged attachment coordinates. All new
  outline geometry, widths and sidebearings pass the 8-grid checks. Regular's
  protected optical coordinates remain unchanged; full report has 27 findings.
- Browser review covered 400, 550 and 700 with the four-form sample and 700
  with Teh/Theh context. Exact endpoint screenshots: `regular-four-forms.png`,
  `bold-four-forms.png`; inherited context: `bold-related.png`. Existing dot
  crowding/proportions in related letters remain visible in Before and Working;
  they are deferred rather than silently included in this base drawing loop.
- Four before/after signed curvature combs are retained as `*-comb.svg` with
  their JSON reports. The final-form comb was visually inspected at common scale.

Status: installed in active Bold sources for interactive review, uncommitted.
The current proof opens the all-four-forms sample. No human grading or approval
of these new drawings is inferred from technical checks.

## Dot feedback and later correction

Eli judged this base trial better and requested near-circular Arabic dots.
The [round-dots revision](round-dots/README.md) preserves this base trial and
adds only the two Bold single-dot donor corrections. Its proof is current;
this folder's earlier snapshots remain unchanged.
