# LAT-001 batch28 · Short slash overlay

Adds U+0337 COMBINING SHORT SOLIDUS OVERLAY and an unencoded narrow variant
in Regular/Bold. The [Unicode chart](https://www.unicode.org/charts/PDF/U0300.pdf)
distinguishes this from U0338 long solidus overlay, which remains next work.
Both new forms use compatible eight-point clipped polygons, zero advance and
incoming overlay anchors at0,0. Main diagonal45 degrees; perpendicular stroke
weight approximately67.9/90.5 units (horizontal sections96/128). Default bounds
±264/272; narrow bounds±136/144. Corner construction uses16-unit diagonal
projections. All points/anchors on8; four glyph-masters have zero grid findings.

The existing Latin body attachment class is extended without moving its anchors.
The existing narrow-base context selects the short variant on narrow letters
and encoded ligature endings. Latin capitals/lowercase, dotless forms, a.bold,
and fi/fl numbered components use the batch27 placement logic. Existing accents
keep their positions; no ordinary-letter substitution, base drawing, metric,
kerning or protected anchor change. This does not implement generic non-Latin
or mathematical-symbol overlay attachment. Do not equate o+U0337 with encoded ø.

## Drawing decisions and image review

The first trial was rejected: its Bold diagonal was heavier and its shorter
narrow form looked like small stem bumps. Exact trial candidates/images are
retained in iterations/short-heavy. The applied version lengthens both forms
and reduces Bold normal weight from113.1 to90.5. Existing Virtua i and short
stroke provided stem/mark weight context. Existing slash was inspected but is
not green and has identical weights; it was not copied as an approved donor.
Rubik was viewed as a shape/attachment comparison, never as an outline source.

Whole48px forms/words at400/550/700 and224px endpoint details were inspected.
Actual Diffenator supplement and stock first viewport were compared in Virtua
and Rubik at400/550/700. The narrow diagonal now reads more clearly and passes
neighbor-clearance contexts. The generic overlay still leaves small counter
fragments in some Bold a combinations and varies in terminal projection as base
proportions change; these remain optical-review findings. Bold density and long
text spacing remain unresolved. A body overlay is not a bespoke redesign of
every stroked base. New drawings are purple pending human review.

## Verification and preservation

Ten source files: four new GLIFs, four registration plists and two feature files.
All1795 other existing sources and every old GLIF remain byte-identical,
including326 Arabic recursive reservations/master and131/74 green sources.
Dependency hashes, exact before/candidate snapshots and surgical application
receipt are retained. Source contours match and are convex at five weights;
there are no cubic segments to score.

770 scoped checks and4425 exact old VF glyph/weight ink/advance comparisons;
3539 old static glyph ink/advance comparisons also exact.21 Latin methods pass
at five VF weights and all four statics, including narrow-letter/following-n
clearance and above/below accent preservation.216 known Hebrew engineering
subcase failures reproduce with zero new failures. No whole-suite pass claimed.
Active/scratch table identity and preflight recorded separately.

Full online unexcluded Fontspector1.9.0 package:10 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP, unchanged. Serving-set failures and protected warnings remain; no
metadata, exclusions or subset declarations changed. The checked package uses
the candidate VF; active/scratch identity binds it to application. Metadata and
artwork remain provisional. No publication/push.

Pinned Rubik gap347 encodings:182 Cyrillic,1 combining (U0338),62 Common and102
Arabic presentation forms. Latin cmap parity is not full language coverage.
Next U0338 with actual mathematical negation/normalization and attachment checks,
then independent symbols and release blockers. Preserve Arabic60272.

Preview: http://127.0.0.1:60273/batch28/comparison/short-slash.html
