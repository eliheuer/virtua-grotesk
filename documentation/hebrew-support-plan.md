# Hebrew development

Hebrew is included in the first release (Eli, 2026-09-09). Current work is
Hebrew only. The findings below replace the July placeholder inventory.

## Source findings — 2026-09-09

- All 27 letters, including finals, have outlines in both masters.
- 22 of those letters have exactly identical Regular and Bold outlines.
  Only dalet, vav, yod, final nun, and resh currently change weight. This is
  a substantial drawing task; a successful variable build does not resolve it.
- 58 encoded Hebrew characters are blank in each master. They include
  cantillation, meteg, rafe, additional punctuation, Yiddish digraphs, and
  presentation forms. All 58 are purple in Regular; Bold is uncolored.
- Most Regular vowel marks are also purple. Active sources have no Hebrew
  attachment anchors. The built font has GDEF classifications for the existing
  vowel marks, but no Hebrew GPOS mark feature; HarfBuzz positions by fallback.
- Existing dotted presentation forms sometimes have different drawings or
  advances from their base letters. Normalized text and presentation forms
  need a consistency review after the base drawings are settled.

## Anchor candidate

`scripts/prepare_hebrew_anchors.py` prepares a new scratch source directory;
its interface never edits active sources. It adds anchors to 72 glyphs in each
master, Hebrew script registration, and missing explicit base categories.
All candidate edits are blue. Outlines, advances, and encodings are unchanged.

The latest local candidate is `out/hebrew/candidate-v3/`. Build and shaping
checks passed. Rendered samples at weights 400, 550, and 700 were inspected:
vowels, shin/sin dots, dagesh combinations, words, and finals. The dagesh on
vav/yod was moved clear of the stem; final kaf uses an interior vowel slot.
Other descending finals have below-outline vowel placement. These are
reviewable positioning choices, not native-reader approval.

This candidate is **not installed in active sources**. Approval to edit purple
Hebrew glyphs is pending. No outlines have been copied from Rubik.

## Reference

[Rubik](https://github.com/googlefonts/rubik) has both Glyphs and converted UFO
sources in the local sibling checkout. Its Hebrew anchor slots informed the
attachment structure; candidate coordinates come from Virtua's bounds and
existing dagesh drawings. Rubik was rendered at explicit weights 400/550/700.
Its Hebrew reference does not establish cantillation coverage for Virtua.

[Microsoft's Hebrew shaping guide](https://learn.microsoft.com/en-us/typography/script-development/hebrew)
is the technical reference for positioning and script behavior.

## Repeatable checks

```sh
make qa-hebrew
# Audit a supplied candidate without rebuilding the active font:
.venv/bin/python scripts/check_hebrew.py out/hebrew/candidate-v3/VirtuaGrotesk.ttf \
  --json out/hebrew/candidate-v3/qa.json \
  --proof-dir out/hebrew/candidate-v3/proofs
```

The check records the binary hash, encoded Hebrew ink/width/class inventory,
Hebrew GPOS lookup coverage, and shaped samples at three variable weights.
It fails for missing basic modern coverage or absent tested attachment.
The active binary currently fails 14 attachment checks; Rubik and candidate-v3
pass them. This is a focused smoke gate: it does not approve the 58 blanks,
all mark combinations, optical spacing, Biblical text, or script quality.
`hb-view` renders shaped runs, not full paragraph bidi layout; mixed-direction
text still needs a browser/application proof.

## Remaining work

1. Resolve permission for the protected Hebrew marks and blank slots, then
   install and recheck the anchor candidate if accepted.
2. Draw compatible Bold counterparts for the 22 unchanged letters; review
   spacing and the five already weighted letters alongside them.
3. Complete the protected blanks without silently deleting their encodings.
   Separate ordinary pointed Hebrew/Yiddish from cantillation review.
4. Reconcile presentation forms with the final bases and marks; test canonical
   equivalents, repeated marks, collisions, and mixed-direction text.
5. Get native-reader and human design grading, then run full release QA on the
   actual release binaries. Blue candidates are not an onboarding approval.
