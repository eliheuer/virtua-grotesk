# LAT-001 batch16 · Bold c/k/t accent spacing

Baseline `40d5b7d7`. Six advance-only Bold corrections match existing bases:
cacute/ccaron/ccedilla/cdotaccent644→640, kcommaaccent644→664 and
tcommaaccent438→416. New advances and target ink bearings are on8. Both human
grades and all component placements/anchors/contours/kerning are exact. All1773
other source files, including every Regular source and326 Arabic reservations
per master, remain unchanged. No green target or inherited green drawing changes.
Intentional side-caron spacing is excluded.

The Regular c/k/t base advances610/596/372 are existing optical exceptions.
Their accent mismatches remain untouched: blindly snapping the green base or
assigning new off8 wrapper widths would resolve neither design policy nor
fallback consistently. I/l overhangs and Bold K804 remain measured in batch14's
`deferred-spacing.json`. Those findings stay open while independent coverage
work proceeds; this is not completion of the whole spacing pass.

## Whole-image review and verification

Complete forms, paired base/accent strings and reading words at400/550/700,
plus224px/em c/ć/k/ķ/t/ț endpoint details, were inspected against Rubik.
All raw DesignBot renders were sequential. Bold accent rhythm now follows
its bases without a new observed collision. The Regular plate is unchanged.
The supplementary h/ȟ row explicitly reports Rubik's missing U+021F; the six
changed characters and reading rows are all supported by actual Rubik.
Heavy Bold base proportions, Regular c-terminal behavior and mark proportions
remain human-review issues; a width repair does not approve their geometry.

- 130 scoped comparisons; all master topology compatible.
- All compiled ink and GPOS/GSUB/GDEF/cmap tables exact; only expected metrics change.
- Nine Latin test methods pass; frozen engineering baseline reproduces the same
216 Hebrew failures, zero new or resolved failures.
- Missing-cmap advance differences fall25→20 across30 VF samples. At700 the five
existing differences become zero; kcommaaccent already uses canonical ccmp.
Five differences at each lower sampled weight remain because Regular widths
were preserved. Some intermediate differences change magnitude/sign as the Bold
endpoint changes; this is not a full-axis fallback-spacing fix. Exact values
are retained in `fallback-advance.json`.
- 91 inherited Bold closure-grid findings remain in base/donor geometry, anchors,
offsets and donor metrics. New wrapper advances and actual bearings are on8.
- Active preflight completed; five active fonts match scratch tables except head
timestamps/checksum adjustment. No curves changed and no fresh curve-quality or
online Fontspector result is claimed.

Before/candidate sources, dependency/source guards, compiled snapshots and eight
inspected-image hashes are retained. Arabic live proof unchanged. Local only;
no push/publication or reader approval. Next: remaining Latin coverage, starting
Tbar/tbar constructions; preserve the measured I/l/K/c/k/t exceptions for review.
