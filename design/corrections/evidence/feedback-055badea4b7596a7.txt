# ARB-003 — Bold Hamza Above

Eli requested on 2026-10-21: fix the Bold hamza, keep it clean and machined
with Virtua chamfers, and show all four references. This authorizes the Bold
`hamzaabove-ar` (U+0654) drawing; Regular and other source files stay unchanged.
Use the standing direct-application workflow, retaining a before snapshot.
No unattended work, green grading or release approval is implied.

## Construction trial

The old red Bold outline has crossed, reversed inner handles and distorted
34/36-unit terminal cuts. Reconstruct the existing 31-point contour, keeping
Regular's segment order and all Regular bytes. Bounds become −32..256 ×
816..1056. The base bar is 88 units thick, the right aperture 40 units high.
Outer upper quadrants are 96 × 96 with equal 64-unit handles; the small inner
upper quadrants are 32 × 32 with equal 24-unit handles. The lower inner turn
is 48 × 48 with paired 32-unit handles. These are trial dimensions, not a new
universal radius rule. Preserve the deliberate short lower-left joining shelf.

Exposed base corners and the upper terminal use 16-unit cuts; the tight inner
terminal keeps an 8-unit cut. Green Bold H (`H_.glif`) supplies the measured
16/8 cut convention; H is read-only. This reuses the bounded-turn principle
from the manual Zayin/Final Tsadi corrections in DESIGN.md, not their literal
radii. Zero advance and `_top` (112,768) stay fixed; envelope anchors track
816/1056, with `top` at 1104 (48 above ink). All new values are on 8.

The donor and 19 transitive component dependents are unprotected in Bold.
Their source files remain unchanged, but their compiled ink inherits the new
mark. Preserve all four reference families: Rubik, Noto Sans Arabic, IBM Plex
Sans Arabic and Readex Pro. Record exact source/font hashes and inspect
interpolation, direct/combined marks, Alef, Waw, Yeh, Heh Goal and Lam-Alef.

## Original AI trial — verification

- Applied only Bold `hamzaabove-ar.glif`; exact source hashes, dependencies,
  before/candidate files and the frozen ARB-002 binary are retained here.
  Purple identifies this AI drawing as unreviewed. No other source label changed.
- `make preflight` passed: all five TTFs, PDF, source/compatibility reports and
  artifact-presence checks. No blocking master structure mismatches.
- `verify.py`: 294 before/working contexts across seven weights, no missing
  glyphs or changed substitutions/clusters/advances. Compiled outline changes
  are confined to the mark and its 19 dependencies. Regular sources and shaped
  positions remain unchanged; joint cubic-to-quadratic conversion changes the
  Regular compiled contour segmentation for those dependencies. Do not claim
  the old and new Regular binaries have identical outlines.
- Bold grid: zero findings. Preserved Regular: six existing off-8 findings.
- `geometry.py`: no sampled contour crossings at 13 weights (400–700 by 25),
  no marked-smooth tangent kinks. `curve_lint.py Bold hamzaabove-ar --joins`
  reports four crest-centering flags because its closed-bowl heuristic groups
  this open contour's inner and outer extrema together. Each intended upper
  turn has equal paired extents/handles; there are no tension-break warnings.
  The 45-degree non-smooth joins are deliberate terminal/shelf transitions.
- Initial lower outer handle was extended from 16 to 32 to match incoming
  curvature and remove a tension break; `trials/initial.glif` retains that
  pre-application draft. Final coordinates and geometry report record the result.
- Browser inspected: enlarged Bold Alef/hamza, carrier group at 550/700, and
  stacked marks, with all four references. Screenshots retained here.

The aperture is visibly open with clean base/terminal chamfers. Existing stacked
mark issues remain: Fathatan intersects the hamza and a Dammatan element is
misplaced over the Alef stem in both Before and Working. Their source drawings
and offsets were not edited. Address stacked-mark composition/positioning in a
separate loop after feedback; these checks are not Arabic release readiness.

## Manual correction 01 — Bold Hamza Above

On 2026-10-21 Eli identified major drawing mistakes, edited the root Bold
`hamzaabove-ar`, and reported saving it. The exact AI/human pair is in
`manual-correction-01/ai.glif` and `human.glif`; `measurements.json` contains
SHA-256 identities and all 29 moved-point deltas. This is direct source evidence,
not a reconstruction from the screenshot. Every other source file, including
Regular, matches the pre-correction snapshot. No agent source edits followed.

| Measurement | AI candidate | Saved human correction |
| --- | --- | --- |
| Bounds | −32..256 × 816..1056 | −16..240 × 816..1048 |
| Base width / thickness | 288 / 88 | 256 / 80 |
| Right aperture | 40 | 40 |
| Exposed cuts / inner cut | 16 / 8 | 16 / 8 |
| Inner upper extent | 32×32 | 32×32 |
| Inner upper handles, horizontal / vertical | 24 / 24 | 16 / 24 |
| Lower inner extent | 48×48 | 48×48 |
| Lower inner handles, horizontal / vertical | 32 / 32 | 32 / 24 |
| Outer left upper extent | 96×96 | 96×88 |
| Outer left upper handles, horizontal / vertical | 64 / 64 | 64 / 56 |
| Outer lower left extent | 24×48 | 24×56 |
| Outer lower left initial vertical handle | 32 | 24 |

The baseline stays 816. The base's sides move inward 16 each and its top moves
down 8. Most of the arch/opening moves down 8, while the left outer shoulder
stays at y=960; that is a local contour adjustment, not uniform scaling. All
31 point types and smooth flags, anchors, zero advance and purple label remain.
The small 8-unit vertical shelf and 40-unit opening remain. The `topDots` and
`top` anchors are still 1056/1104 despite the new ink top 1048; preserve those
saved anchors rather than silently aligning them to the changed bounds.

### Lessons and limits

Observed: the hand correction reduces the base mass/projection and adjusts
several turns to unequal handles while preserving axis tangencies, chamfers
and the existing skeleton. It stays entirely on the 8-unit lattice. My earlier
choice of square turns/equal handles was not sufficient to make a well-drawn
mark. These are evidence against promoting the Zayin example into a universal
square/equal-handle recipe.

Eli confirmed on 2026-10-21 that the AI draft was too inflated and base-heavy,
and added that there were basic curve issues. He asked us to study RuneBender's
Curvature Comb/Continuity tools, Glyphs SuperTool and related tools, and use
that knowledge in our drawing tools/skills. This confirms the rationale; the
individual measured ratios are still not defaults for unrelated marks.
Canonical routes: DESIGN.md and edit-glyph/draw-outline.
No further drawing batch or automated human grade follows this example.

Current proof is `manual-correction-01/working/`: **AI draft** versus **Your edit**,
with Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro. Original
ARB-003 Before/Working evidence remains frozen in `working/` and `assets/`.

Human-correction verification: `make preflight` passed; 294 before/after shaping
contexts preserved substitutions, clusters and advances. Source topology is
compatible; 13 sampled weights have no contour crossings and the saved Bold
has no marked-smooth tangent kinks. Its draft-grid report has zero findings.
Generic crest/tension lint output is retained for diagnosis, without modifying
human geometry. Regular source bytes are unchanged; joint quadratic compilation
retessellates the dependent Regular outlines as in the earlier loop. Skill
frontmatter validation and `git diff --check` passed. The browser was inspected
at 700 and retained as `manual-correction-01/carriers-bold.jpg`.

### Curve-tool research and diagnostics — 2026-10-21

Read-only comparison of the exact snapshots is saved in
`manual-correction-01/curve-profile.json` and `curve-comb.svg`.
Reproduce with `scripts/curve_profile.py` on `ai.glif` and `human.glif`.

- AI lower-left turn has a curvature sign reversal (one sampled sign change,
  also opposite signs at its endpoints); the human turn has no sampled reversal.
  This was not exposed by checking only the tangent at its smooth start.
- Inner join AI (88,952): signed curvatures −0.0104167 / −0.00925926,
  about 11.1% mismatch. Human (88,944): −0.0185185 / −0.0185185, G2.
- Human outer shoulder (16,960): 0.00680272 / 0.00925926, about 26.5%
  mismatch. This remains in the preferred drawing. Do not optimize it away
  merely to make the diagnostic all-G2.

The old coarse tension ratio did not flag that inner mismatch, and the join
CLI hid curvature behind tangent angles. It now prints classification, signed
curvatures and relative jump. The new profile includes full sampled signed
curvature and an SVG comb with a shared outline scale and gain. Sampling is
not a no-defects proof; deliberate corners and source grading remain human
choices. We do not infer which editor operations Eli used.

Research and the reusable workflow live in
[draw-outline's curve-quality reference](../../../.agents/skills/draw-outline/references/curve-quality.md).
This records verified native RuneBender behavior and links SuperTool, the
Cozens derivation, Glyphs harmonization/Speed Punk/Harmony and Curvatura.
No source geometry, anchors, colors or RuneBender code changed in this pass.

Validation: seven geometry regression tests passed; both updated skills passed
frontmatter validation; local links and `git diff --check` passed. The shared-scale
comb was rendered to `manual-correction-01/curve-comb.png` and visually inspected.
The active Bold hamza still matches the human snapshot SHA-256.
