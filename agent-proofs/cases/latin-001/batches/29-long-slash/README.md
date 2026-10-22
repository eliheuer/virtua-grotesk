# LAT-001 batch29 · Long solidus overlay

Adds U+0338 and an unencoded narrow variant in Regular/Bold, plus Latin body
attachment and separate attachment to existing equal/less/greater/plus/minus.
The [Unicode chart](https://www.unicode.org/charts/PDF/U0300.pdf) distinguishes
long and short solidus overlays. Existing mathematical bases are unchanged.
The new mark lets HarfBuzz render canonical decompositions of ≠/≮/≯ without
adding those cmap entries. Encoded/NFD output agrees at five VF weights and
all four statics. This is not complete mathematical or non-Latin support.

## Construction and image findings

Both forms have eight-point clipped line contours, width0 and incoming anchor0,0.
Default slope3/2, height672, horizontal stroke80/112 (normal66.6/93.2).
Narrow slope2, height448, horizontal stroke64/80 (normal57.2/71.6).
Terminal construction uses16-unit cap setbacks and on8 side cutbacks.
New points/anchors on8; four glyph-masters have zero grid findings and convex
contours at400/475/550/625/700. No cubic score applies. Weight choices follow
existing Virtua accent/stem context; no Rubik outlines were copied.

The first narrow trial was too steep and merged into the stem; its exact
candidates and images remain in iterations/steep-narrow. A wider second trial
failed following-l/n clearance (up to8 units of bounding overlap at700), so it
was reduced before application; evidence in iterations/wide-narrow. Final
sampled following-n clearance is at least16. No base advance/kerning changed.
The final narrow slash remains subtle on heavy Bold i/l/f stems; this is an
explicit optical-review limitation, not visual approval. Generic a combinations
retain small counter fragments. Large <+slash can create an enclosed triangle;
its position/weight remains for human review. Bold density and stock mixed-text
spacing remain unresolved. Do not equate o+U0338 with encoded oslash.

Whole48px forms/words400/550/700 and224px endpoint details were inspected.
Actual Diffenator supplement plus stock first viewport were compared with Rubik
at all three weights; screenshot and font hashes are in diffenator/review.json.
Reference generic placement often follows letters/symbols rather than crossing
them; it was inspected, not treated as a desired attachment implementation.
Arabic live proof60272 remains unchanged. New drawings are purple pending review.

## Verification and source protection

Ten source files: four new GLIFs, four registration plists, two feature files.
All1799 other sources and every old GLIF unchanged, including326 Arabic recursive
reservations/master and131 Regular/74 Bold green sources. Exact before/candidate
snapshots, source hashes and application receipt retained. Existing mark positions
remain unchanged; separate math lookup does not extend older overlay attachment.
775 scoped comparisons,4435 exact old VF glyph/weight ink/advance comparisons,
3547 exact old static glyph ink/advance comparisons.22 Latin methods and2 build
snapshot tests pass;216 existing Hebrew failure subcases persist, zero new.
Active/scratch table identity except head and preflight recorded separately.

Full online unexcluded Fontspector1.9.0 package:12 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP. Before was10 FAIL/9 WARN. Two additional samples became testable:
Central Mazahua poster sm lacks U0338 in serving subsets; Ticuna masthead partial
lacks U1EBC/U1EBD. Central Mazahua poster md U0331 only changes explanatory text.
These are new exposed serving-set blockers, not a loss of prior font coverage or
shaping. No false subset declarations, metadata changes or exclusions were made.
Package metadata/artwork remain provisional. No whole-suite or release pass.
See package-failure-delta.json and current canonical release checklist.

Pinned Rubik gap346 encodings:182 Cyrillic,62 Common,102 Arabic presentation forms.
Latin and combining cmap gaps are zero; this is not language or visual approval.
Next independent common symbols: inspect missing mathematical constructions and
existing donors before drawing (not-equal/less-equal/greater-equal/plus-minus/not).
Serving-subset policy, protected attachment/spacing and reader review remain open.
No push/publication.

Preview: http://127.0.0.1:60273/batch29/comparison/long-slash.html
