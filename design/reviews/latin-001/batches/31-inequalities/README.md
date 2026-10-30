# LAT-001 batch31 · Less-equal and greater-equal

Adds lessequal/greaterequal (U2264/U2265) in Regular/Bold. Two compatible line
contours each: a16-point chevron and8-point lower bar. Advance600, bounds72–528,
72-unit bearings; lower bars72/112 thick, y64–136/176. Chevron y232–680 leaves
96/56 vertical clearance. Greater-equal mirrors the chevron about x300, reversing
point order to retain winding.16-unit exposed cuts,16-unit inner apex flat;
all new geometry, spacing and feature anchors on8, zero grid findings.

Green H/E supply the chamfer and weight context; their bars96/168 are heavier
than the new symbol bars. Existing less/greater/equal were inspected as diagnostic
context, not approved outline donors. No reference outlines copied. Rubik's
compressed chevron over a separate horizontal line supplies structural comparison.
Unicode normalization was checked: ≤/≥ have no canonical decomposition. No
less+equal or greater+equal sequence substitution was added.

## Whole-image corrections and remaining review

The first proof exposed dangling long-slash negation after the new symbols.
Extend only the existing MATH_LONG_SOLIDUS_BASES lookup with anchors304,368 on
the two new bases. This renders canonical ≰/≱ through ≤/≥ plus U0338; no new
negation cmap entries. The first Bold drawing was too filled-in; its inner apex
moves352→304, inside terminals open16, and lower bar128→112. Rejected source
candidates and images remain in iterations/. No existing mathematical base changes.

Final complete forms/equations400/550/700 and224px endpoint details were inspected,
along with actual Diffenator same-text supplement and stock first viewport against
Rubik at all three weights. The new chevrons are broader/flatter than Rubik;
separate bars remain clear. Small enclosed wedges in slash-negated signs, overall
proportions and pair spacing still need human optical review. Generic math accents
retain right-side fallback placement; this is not comprehensive math attachment.
Dense Bold and uneven text rhythm remain unresolved. Purple is pending review,
not final quality approval. Arabic live proof60272 remains unchanged.

## Verification

Ten source files: four new GLIFs, four registration plists, two feature files.
All1805 other source files and every old GLIF unchanged, including326 Arabic
recursive reservations/master and131 Regular/74 Bold green sources. Current hashes
checked before surgical application; before/candidate snapshots retained. New
masters have matching16+8-point line structure. Source winding is counterclockwise;
compiled winding is clockwise, no sampled proper polygon crossings at five weights.
There are no cubics requiring curvature scoring.

160 scoped comparisons,4450 exact old VF glyph/weight ink/advance checks,3559
old static glyph ink/advance checks.24 Latin methods plus2 build-helper methods
pass, including canonical negation and preserved <=/>= sequences.216 Hebrew
baseline failures reproduce without new failures. Active/scratch tables match
except head; preflight complete. No whole-suite pass is claimed.

Fresh online unexcluded Fontspector1.9.0 package:12 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP. Failure meaning is unchanged from batch30; only Ticuna U1EBC/U1EBD bullet
ordering differs. Raw before/after records are retained in package-failure-delta.
No subset declarations, exclusions, metrics or package metadata changed. The
[official QA guidance](https://googlefonts.github.io/gf-guide/qa.html) was refreshed;
automated passes do not establish drawing or release approval. Metadata/artwork
remain provisional and existing serving-set/Hebrew/protected-source blockers remain.

Pinned Rubik gap343 encodings:182 Cyrillic,59 Common,102 Arabic presentation forms.
Latin/combining cmap parity is not complete language coverage. Next independent
plus-minus and not-sign, then other Common symbols and release blockers. Local
checkpoint only; no push or publication.

Preview: http://127.0.0.1:60273/batch31/comparison/inequalities.html
