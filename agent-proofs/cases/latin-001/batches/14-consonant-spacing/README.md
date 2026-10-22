# LAT-001 batch14 · Lowercase consonant and iogonek advances

Baseline `0b1d4f14`. Advance-only correction of20 Regular and25 Bold wrappers
(45 GLIFs,25 distinct characters): ğģġįńňņñŕřśšşșẃŵẅẁýŷÿỳźžż.
They now match their current unshifted g/i/n/r/s/w/y/z bases. Only mismatches
change; `changes.json` retains exact names, widths and before/after hashes.
All45 new advances are on8. All contours, components, offsets, anchors,
kerning and human grades are unchanged; no new geometry or color assignment.
All1734 other source files remain exact, including326 recursively reserved
Arabic sources/master. No target or reverse consumer is green or Arabic.

## Whole-image review

Complete25-character and base comparison rows at400/550/700 were inspected
with FreeType/RAQM, plus48px/em reading words and224px/em endpoint details
(n/ñ/g/ģ/i/į). Sequential DesignBot renders compare Before/Working/Rubik.
All final proof rows use characters actually supported by Rubik. Accented
forms now maintain the base's rhythm; no new overlap was observed in these
contexts. The Bold g counter, heavier base proportions, mark weight and ogonek
neck remain human-review items; this spacing correction does not approve them.

The first spacing-only trial included Regular hcaron. Whole-image inspection
revealed the inherited caron/ascender collision in both weights, so that target
was withdrawn before application. Both active hcaron sources remain exact.
The rejected rows and receipt are in `rejected-hcaron-spacing-only/` and the
next repair is recorded in `hcaron-followup.json`. Rubik lacks U+021F and was
explicitly unavailable in that trial row, never substituted.

`deferred-spacing.json` records I/l overhangs and off8 K/c/k/t base widths.
Do not blindly narrow I accents or Bold l accents: some would have negative
right bearings, and Bold l already extends beyond its base advance. Preserve
batch11 intentional side-caron spacing and human optical exceptions.

## Verification and limits

- 415 scoped comparisons at400/475/550/625/700; full master topology compatible.
- Every compiled outline and GPOS/GSUB/GDEF/cmap table is unchanged. Only expected
 advance metrics change. No curve edits; exact outline equality establishes
 preservation, not a new curve-quality approval.
- Basic missing-cmap advance mismatches fall105→0 across125 samples. This does
 not establish generic mark placement or compound-accent subset correctness;
 batch10 ogonek-plus-acute and protected g+U0326 findings remain unresolved.
- Eight Latin test methods pass. Frozen engineering baseline reproduces exactly
216 Hebrew failures, with zero new or resolved failures.
- Active preflight completed; all five active fonts match scratch tables except
 head timestamps/checksum adjustment. No fresh online Fontspector run.
- 1037 inherited closure-grid findings remain (531 Regular,506 Bold), in
 preserved geometry/anchors/offsets/metrics. New advances and actual target
 wrapper sidebearings are on8. Popcounts/bearings are retained in measurements.

Exact before/candidate sources, full hashes, guarded application, baseline
fonts and eight inspected-image hashes are retained. Arabic live proof remains
unchanged. Local checkpoint only; no push or publication. Next: hcaron attachment,
then remaining narrow/off8 spacing exceptions, Latin coverage and release blockers.
