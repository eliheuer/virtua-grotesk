# LAT-001 batch13 · Uppercase accent advances

Baseline `0a7c7d43`. Width-only correction:21 Regular and45 Bold wrappers
(66 GLIFs,52 distinct characters) now match their current unshifted base.
The selected families are A/D/G/L/N/O/R/S/T/U/W/Y/Z. Only existing mismatches
change; `changes.json` lists exact names, widths and before/after hashes.
I and K are deferred for narrow-accent/optical-grid review. Intentional side
carons, ligatures, barred letters and all base drawings are untouched.

Examples: Regular O accents864→800, Y accents736→608; Bold R accents716→784,
U accents840→792, W accents1112→1176. Matching is to Virtua's own base advance,
not reference font widths. All66 new advances are on8. Base component offsets,
mark placements, anchors, contours, kerning and human grades are unchanged.
All1713 other source files remain byte-identical, including326 recursively
reserved Arabic sources per master. No new geometry or grade assignment.
The reverse closures contain only the21/45 targets; none are green or Arabic.

## Whole-image review

All52 affected characters and their base comparisons were inspected in complete
FreeType/RAQM rows at400/550/700, plus48px/em reading words and224px/em O/Ó/Y/Ý
endpoint details. The stale accented/unaccented rhythm is removed. All raw
DesignBot renders were sequential. Rubik lacks U+0162 (Ţ): the mixed T/U row
is explicitly unavailable; separate supported T/U rows at all three weights
retain the actual reference. No fallback font was substituted.

This is a useful advance correction, not approval of the underlying shapes or
full optical kerning. Bold Y's heavy fork/stem and the existing cross-family
weight balance remain human-review issues. Regular marks' taper/placement and
previously documented ring/ogonek proportions remain pending. The green bases
are unchanged. No new curve operation occurred; exact compiled-outline equality
at five weights establishes that curve shapes are preserved, not that they pass
a new quality review.

## Verification and limits

- 815 scoped comparisons at400/475/550/625/700: base advance equality, full-font
 NFC/NFD and protected-script/prior-form contexts. All master topology matches.
- Every compiled glyph outline and GPOS/GSUB/GDEF/cmap table is unchanged.
 Only expected width metrics change. Targets differ by master; interpolated
 checks account for metrics that cross the old value at an intermediate weight.
- Basic missing-cmap advance mismatches fall201→0 across260 samples. This checks
 advance widths only, not generic mark placement or compound-accent subset
 normalization. The batch10 ogonek-plus-acute finding remains unresolved.
- Eight Latin test methods pass, including expanded uppercase metric/fallback
 coverage on VF/four statics. The frozen engineering baseline reproduces the
 same216 Hebrew failures, zero new/resolved failures.
- Active build/preflight complete; active and scratch font tables match except
 head timestamps/checksum adjustment. No online Fontspector rerun.

The expanded grid gate retains484 Regular +596 Bold inherited findings (1080).
No new advance is off8. Bold Racute/Rcaron have60-unit right bearings because the
unchanged R base ends at x724 with advance784; retain that inherited optical
exception rather than shift green geometry. `spacing-measurements.json` records
actual bounds, bearings and advance popcounts. All other target wrapper bearings
are on8; component/donor findings remain explicitly visible.

Before/candidate sources, complete source hashes, guarded application, baseline
fonts, tests and14 inspected-image hashes are retained. Arabic's live proof
stays unchanged. Local checkpoint only; no push or publication. Next: remaining
lowercase consonant/i spacing, uppercase I/K exceptions and independent coverage
work. Do not undo batch11 intentional side-caron widths.
