# LAT-001 batch12 · Lowercase vowel advances

Baseline `8e48e04e`. This bounded spacing repair changes only the advance field
of31 accented a/e/o/u wrappers per master (62 GLIFs). Exact names, grades,
before/after hashes and values are in `changes.json` and `dependencies.json`.
Eight other wrappers in each family already matched and are untouched.

All outlines, component positions, anchors, human grades and kerning stay exact.
No purple reassignment is appropriate for a metrics-only edit. All1717 other
source files remain byte-identical, including green bases, shared mark donors
and326 recursively reserved Arabic sources per master. Reverse-consumer closure
has no additional descendants and no green/Arabic intersections.

## Change and whole-image judgment

The copied wrappers retained widths from older base drawings. The correction
matches their existing unshifted base component's advance:

| Family | Regular before → after | Bold before → after |
| --- | --- | --- |
| a accents (9) |592 →608|592 →632|
| e accents (8) |620 →624|668 →656|
| o accents (6) |648 →640|648 →704|
| u accents (8) |600 →592|672 →720|

The repeated words now have the same basic rhythm with and without accents;
Bold ó and ú no longer squeeze the following letter. Complete silhouettes and
31-form rows were inspected at400/550/700 against Before and actual Rubik,
alongside48px/em reading words and224px/em enlarged endpoint letters. Raw
DesignBot ran sequentially; independent FreeType/RAQM rows include all targets.
All reference characters in these rows are supported, without fallback.

This establishes a useful spacing correction, not optical approval of the whole
family. Bold e remains heavy with a small counter; inherited base proportions,
Regular acute taper/angle and mark balance remain review items. No base drawing
was changed or newly approved. Other uppercase/consonant/i-family stale widths
remain on the next queue; alternate-caron side spacing from batch11 is intentional
and must not be normalized back to base widths.

## Grid and preservation

All new advances are on8 and copied from the current bases, not rounded from
an unrelated design. `spacing-measurements.json` records actual compiled bounds,
before/after bearings and descriptive advance popcounts. The expanded grid gate
retains649 Regular +536 Bold inherited findings (1185 total) in unchanged
components, anchors, donor metrics and bounds/bearings. There are no new advance
grid failures. Human optical geometry is preserved rather than snapped.
No curve edit occurred; all compiled glyph drawing commands are identical at
five sampled weights. A new signed-curve audit is therefore not applicable.

## Verification

- 500 scoped comparisons at400/475/550/625/700: advance equality, full-font NFC/NFD,
 Arabic/Hebrew and prior-family preservation. Full source master topology passes.
- Every compiled outline and GPOS/GSUB/GDEF/cmap table is identical to Before.
 Only the62 source advances and corresponding compiled metrics change. At475,
 old/new e advances cross exactly, so those eight metrics are equal at that sample.
- Basic missing-cmap advance differences fall from133 to0 across155 samples.
 This test concerns advances only: generic mark placement and the earlier
 ogonek-plus-acute normalization problem are not claimed fixed.
- Eight Latin test methods pass on VF and all four static fonts. Frozen baseline
 reproduces the same216 existing Hebrew failures, with zero new/resolved failures.
- Active build and preflight complete; all five active font tables match scratch
 except head timestamp/checksum adjustment. No online Fontspector rerun.

`final-identity.json` binds active sources/fonts and the eight actually inspected
PNGs. Before/candidate sources, source hashes, baseline fonts, source guards,
reproduction scripts and exact failure evidence are retained. The Arabic live
proof remains unchanged. Local checkpoint only; no push or publication.
