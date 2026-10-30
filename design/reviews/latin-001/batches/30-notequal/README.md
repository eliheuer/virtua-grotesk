# LAT-001 batch30 · Encoded not-equal

Adds U+2260 notequal in Regular/Bold as unchanged equal and slashlongcomb
components. The slash offset304,352 reproduces the exact prior batch29
mathematical attachment. Advance600 is unchanged from equal; new registration
classifies the composite as a base. No new outlines, anchors, feature rules,
kerning or donor changes. New composites are purple pending human review.
This closes one Common-script cmap gap without changing its existing canonical
rendering through equal + U0338. No claim of complete mathematical support.

## Whole-image review

Inspected complete forms and equations at400/550/700,224px endpoint details,
and actual Diffenator same-text supplement and stock first viewport in Virtua
and Rubik at all three weights. Receipts bind screenshots and fonts in
`diffenator/review.json`. Encoded and decomposed signs have the same silhouette;
Virtua has a longer, less steep slash than Rubik and clipped terminals. Bold
bars remain heavy, inherited from equal. Dense Bold and uneven mixed-text
spacing remain human-review issues, not accepted design quality.

Generic acute/cedilla after mathematical symbols still sit to the right rather
than attaching centrally. Fifteen before/after samples preserve exactly those
existing mark positions (`mark-followup.json`); this encoding does not implement
new math accent attachment. Empty Before cmap rows are labeled unavailable;
separate decomposed rows show the old actual rendering. Arabic60272 is unchanged.

## Source and compiled checks

Six source files: two new composite GLIFs and four registration plists. All1805
other source files and every previous GLIF are byte-identical, including326
Arabic recursive reservations/master and131 Regular/74 Bold green sources.
Exact before/candidate snapshots, full source guards and application receipt
retained. Both masters have identical component structure. All new offsets and
advances on8; Regular has zero grid findings, Bold has16 inherited equal-point
y findings. The existing donor geometry is deliberately preserved.

90 scoped checks,4445 exact old VF glyph/weight ink/advance comparisons and3555
old static glyph comparisons pass. The new glyph is exactly the prior positioned
equal-plus-slash geometry at five VF weights.23 Latin methods and2 build-helper
methods pass. Tests cover encoded/NFD equality, missing-cmap fallback and real
fontTools serving subsets at five VF weights and all four statics. Glyph counts
change when HarfBuzz composes the newly encoded sign; do not claim unchanged
shaped glyph arrays.216 baseline Hebrew failures reproduce unchanged with zero
new failures. Active/scratch tables match except head; preflight completed.

Fresh full online unexcluded Fontspector1.9.0:12 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP. Existing serving-set blockers remain; no metadata, declarations or
exclusions changed. Metadata/artwork remain provisional; no release approval.
Rubik gap now345 encodings:182 Cyrillic,61 Common,102 Arabic presentation forms.
Latin/combining cmap parity is not language coverage or native-reader approval.

Next: less-equal/greater-equal, plus-minus and not-sign constructions, inspecting
actual references and protected donor closure first. All other protected
attachment, spacing and script findings remain in the central case. Local only;
no push or publication.

Preview: http://127.0.0.1:60273/batch30/comparison/notequal.html
