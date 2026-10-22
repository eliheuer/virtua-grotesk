# LAT-001 batch23 · Ogonek normalization in cmap-limited subsets

Repairs the batch10 serving-fallback failure without changing any drawing.
When ogonek cmap entries are absent, HarfBuzz can normalize Ą+acute into Aacute+
ogonek instead of Aogonek+acute. Generic positioning then centers the hook under
A rather than using the existing right-foot construction. Other above accents
and wrapper advances are affected by the same normalization path.

## Applied scope

Only the two master `features.fea` files change. A contextual lookup decomposes
71 existing above-accent vowel glyphs only when followed by ogonek. An ogonek-only
mark-filtered lookup restores the existing A/a/E/e/I/i/U/u ogonek composites,
skipping intervening above marks. This runs before soft-dotted handling, preserving
existing dotless-i behavior. A standalone decomposition lookup is invoked by
context, not unconditionally applied to accented text. All prior feature text is
retained; Arabic/Hebrew constructions are untouched.

Both feature candidates were prepared on scratch, compiled, tested and inspected
before hash-guarded application. All1793 other existing source files are exact,
including every GLIF,326 Arabic recursive sources/master,131 Regular and74 Bold
green sources, anchors, metrics, human grades and manual corrections. No new
geometry or spacing values. Full-font cmap and glyf/gvar/hmtx/OS2/hhea tables are
exact. Adding a mark-filter set reindexes GPOS MarkFilteringSet indices; after
mapping those indices back by their actual glyph sets, GPOS bytes are exact.
This is not a drawing-quality approval.

## Verification

- Original forty VF acute failure cases now pass.
- Expanded cmap-only removal:435 failing samples before, zero after, across
  600 samples/font (eight letters, fifteen suffixes and five weights).
- Real fontTools subsets retaining layout closure:870 failing cases before,
  zero after across1,200 cases/font, including encoded and NFD sequences. The
  stronger check compares glyph names and absolute positions as well as advance.
- Sixteen Latin test methods pass on VF plus four static builds; the new method
  exercises real subsetting and thirteen above/mixed suffixes. Existing216 Hebrew
  failing subcases reproduce exactly on the frozen baseline, zero new/resolved.
-3,995 preservation comparisons cover old encoded characters, original full-font
  ogonek stacks and unrelated Latin/Arabic/Hebrew text at five weights.
- Active build/preflight complete; active/scratch binary tables match except head
  timestamps. Final source and binary hashes are in `final-identity.json`.

One diagnostic initially reported40 remaining mixed cedilla/acute cases because
non-overlapping above/below mark output order differed. The positioned glyphs
and advance were identical. The final real-subset test compares sorted positioned
glyph records, so it does not mistake equivalent ordering for displaced ink.
Tests do not suppress missing glyphs or accept changed mark positions.

## Visual evidence and limits

Whole48px proofs at400/550/700 and160px endpoint details compare Before subset,
Working subset, Working full font and Rubik. Detached A hooks and generic other
hooks move to the intended foot/stem; Working subset/full rows agree. Existing
heavy Bold bases, hook proportions and accent balance still need human review.
FreeType/RAQM proofs are in `forms-*` and `large-*` with font hashes.

Actual Diffenator browser supplements were inspected at400/550/700 for Working
subset and full font versus Rubik, with the failing400 subset captured. NFD text
explicitly uses codepoints present in the subsets; this avoids browser fallback
from missing encoded letters. Stock reports are generated, not exhaustively
reviewed this batch. Browser screenshots, weights and font hashes are retained.
Arabic live proof60272 is unchanged. Local previews:
- http://127.0.0.1:60273/batch23/subset/ogonek.html (Old=Before subset/New=Working subset)
- http://127.0.0.1:60273/batch23/comparison/ogonek.html (Old=Working/New=Rubik)

This fixes the recorded ogonek normalization cases, not every Google Fonts serving
subset or the package's old10 Fontspector failures. Fresh full package QA remains
required. Other blockers:216 Hebrew failures; protected g+comma attachment;
missing combining/common/Cyrillic coverage; protected base/spacing review; platform
metrics testing. Next bounded work: four missing combining marks and current
serving-subset/package diagnostics. No glyph approval, push or publication.
