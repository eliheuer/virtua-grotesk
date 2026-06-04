# Fontspector Zero-Warning Worklist

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`

This generated report turns the remaining Fontspector warning floor into
explicit drawing, coverage, metadata, and reviewer-decision work. It is
not a recommendation to hide intended Arabic support.

## Current Warning Floor

- Honest zero-warning state possible with current scope: no
- Package-context warning checks: `contour_count`: 1, `googlefonts/glyphsets/shape_languages`: 1, `googlefonts/metadata/subsets_correct`: 1, `googlefonts/metadata/unreachable_subsetting`: 1, `outline_alignment_miss`: 1, `outline_direction`: 1
- Intended package subsets in preview: `arabic`, `latin`, `menu`
- Contour decision state: unique review items: 4; pending: 4; fix-now: 0; fixed: 0; accepted: 0; deferred: 0
- GF Latin Core missing codepoints: 0
- GF Arabic Core missing codepoints: 0

## Zero-Warning Verdict

True zero is not possible with the current intended scope without changing coverage, metadata scope, or reviewer policy.

Blockers: meet or revise the broad Google Fonts subset threshold for the intended subsets; resolve or get reviewer acceptance for required support codepoints that are not covered by serving subsets; clean up package-context contour-count warnings.

Do not spend the Arabic hand-review pass trying to force these warnings
to zero by deleting U+200F, U+25CC, dotless forms, rupee support, or
the intended `arabic` subset. Those experiments are tracked in the
metadata probe and either preserve the warning floor, create worse
Fontspector results, or misrepresent the first-submission scope.

## Current Honest Minimum

The package-context probe currently bottoms out at 6 warnings
without hiding intended script scope or removing shaping support:

- 1 contour-count warning(s): require source drawing cleanup or
  explicit reviewed acceptance.
- 1 subset-threshold warning(s): require broader `arabic`
  coverage, narrower final subset declarations, or reviewer
  acceptance for the first-submission scope.
- 1 reachability warning for U+0237, U+200F, U+20B9, and U+25CC:
  do not strip these codepoints just to reduce warnings; the
  metadata probe shows that removal or broad rescue subsets can
  keep the warning floor unchanged or create worse warnings.

## Subset Threshold Math

Google Fonts `subsets_correct` warnings use broad serving subsets, not just
`GF_Arabic_Core`. Passing the threshold by coverage alone would require:

| Subset | Threshold | Subset codepoints | Present | Present needed | Coverage | Additional needed | Threshold met |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `arabic` | 50% | 1432 | 126 | 717 | 8.80% | 591 | no |
| `latin-ext` | 20% | 1144 | 109 | 229 | 9.53% | 120 | no |

## Practical Zero-Warning Paths

### Release-Scope Path

This is the practical first-submission path when the intended scope remains
`menu`, `latin`, and Arabic Core:

1. Keep the loose-font `make test` WARN count in context: until a final
   downstream `METADATA.pb` is packaged with the fonts, loose Fontspector
   runs can repeat the same subset warning once per built font.
2. Keep contour-count cleanup closed by rerunning the contour proof after
   any source drawing changes.
3. Finish the 0 missing `GF_Latin_Core` codepoints so the current
   `googlefonts/glyph_coverage` FAIL bucket can close.
4. Finish Arabic visual review for the current Arabic Core drawings and
   carry the package-context 2-WARN floor as review evidence.
5. Ask Google Fonts review whether the intentional Arabic Core first
   submission may keep `subsets: "arabic"` before the family reaches
   broad `arabic` subset threshold coverage.

### True Zero-Warning Path

This is a larger coverage project, not a final-cleanup tweak:

1. Add at least the missing 0 `GF_Latin_Core` codepoints.
2. Add enough broad `arabic` subset codepoints to pass the 50% threshold
   shown above, or get a reviewer-approved narrower metadata path.
3. Do not add `latin-ext` until the broad subset reaches the 20% threshold
   shown above; otherwise it adds another `subsets_correct` warning.
4. Resolve U+0237, U+200F, U+20B9, and U+25CC reachability in a way that
   does not create replacement warnings. The current probe shows that
   deleting or broad-rescuing them is worse than carrying the warning.

## Fastest Honest Next Step

For this project, the fastest honest path is to close the actual drawing
and coverage blockers first: complete `GF_Latin_Core`, finish Arabic Core
visual review, and keep the metadata probe current. Do not suppress the
remaining package warnings by dropping `arabic` or removing required
support codepoints unless a Google Fonts reviewer explicitly approves
that narrower first-submission scope.

## Missing Threshold Samples

### `arabic` Threshold Worklist Sample

- `U+0604 ARABIC SIGN SAMVAT`
- `U+0605 ARABIC NUMBER MARK ABOVE`
- `U+0606 ARABIC-INDIC CUBE ROOT`
- `U+0607 ARABIC-INDIC FOURTH ROOT`
- `U+0608 ARABIC RAY`
- `U+060A ARABIC-INDIC PER TEN THOUSAND SIGN`
- `U+060B AFGHANI SIGN`
- `U+060E ARABIC POETIC VERSE SIGN`
- `U+060F ARABIC SIGN MISRA`
- `U+0610 ARABIC SIGN SALLALLAHOU ALAYHE WASSALLAM`
- `U+0611 ARABIC SIGN ALAYHE ASSALLAM`
- `U+0612 ARABIC SIGN RAHMATULLAH ALAYHE`
- `U+0613 ARABIC SIGN RADI ALLAHOU ANHU`
- `U+0614 ARABIC SIGN TAKHALLUS`
- `U+0616 ARABIC SMALL HIGH LIGATURE ALEF WITH LAM WITH YEH`
- `U+0618 ARABIC SMALL FATHA`
- `U+0619 ARABIC SMALL DAMMA`
- `U+061A ARABIC SMALL KASRA`
- `U+061C ARABIC LETTER MARK`
- `U+061D ARABIC END OF TEXT MARK`
- `U+061E ARABIC TRIPLE DOT PUNCTUATION MARK`
- `U+0620 ARABIC LETTER KASHMIRI YEH`
- `U+063B ARABIC LETTER KEHEH WITH TWO DOTS ABOVE`
- `U+063C ARABIC LETTER KEHEH WITH THREE DOTS BELOW`
- `U+063D ARABIC LETTER FARSI YEH WITH INVERTED V`
- `U+063E ARABIC LETTER FARSI YEH WITH TWO DOTS ABOVE`
- `U+063F ARABIC LETTER FARSI YEH WITH THREE DOTS ABOVE`
- `U+0659 ARABIC ZWARAKAY`
- `U+065A ARABIC VOWEL SIGN SMALL V ABOVE`
- `U+065B ARABIC VOWEL SIGN INVERTED SMALL V ABOVE`
- `U+065C ARABIC VOWEL SIGN DOT BELOW`
- `U+065D ARABIC REVERSED DAMMA`
- `U+065E ARABIC FATHA WITH TWO DOTS`
- `U+065F ARABIC WAVY HAMZA BELOW`
- `U+0672 ARABIC LETTER ALEF WITH WAVY HAMZA ABOVE`
- `U+0673 ARABIC LETTER ALEF WITH WAVY HAMZA BELOW`
- `U+0674 ARABIC LETTER HIGH HAMZA`
- `U+0675 ARABIC LETTER HIGH HAMZA ALEF`
- `U+0676 ARABIC LETTER HIGH HAMZA WAW`
- `U+0677 ARABIC LETTER U WITH HAMZA ABOVE`
- ... sample truncated; regenerate this report after choosing this expansion path.

### `latin-ext` Threshold Worklist Sample

- `U+0108 LATIN CAPITAL LETTER C WITH CIRCUMFLEX`
- `U+0109 LATIN SMALL LETTER C WITH CIRCUMFLEX`
- `U+0114 LATIN CAPITAL LETTER E WITH BREVE`
- `U+0115 LATIN SMALL LETTER E WITH BREVE`
- `U+011C LATIN CAPITAL LETTER G WITH CIRCUMFLEX`
- `U+011D LATIN SMALL LETTER G WITH CIRCUMFLEX`
- `U+0124 LATIN CAPITAL LETTER H WITH CIRCUMFLEX`
- `U+0125 LATIN SMALL LETTER H WITH CIRCUMFLEX`
- `U+0128 LATIN CAPITAL LETTER I WITH TILDE`
- `U+0129 LATIN SMALL LETTER I WITH TILDE`
- `U+012C LATIN CAPITAL LETTER I WITH BREVE`
- `U+012D LATIN SMALL LETTER I WITH BREVE`
- `U+0132 LATIN CAPITAL LIGATURE IJ`
- `U+0133 LATIN SMALL LIGATURE IJ`
- `U+0134 LATIN CAPITAL LETTER J WITH CIRCUMFLEX`
- `U+0135 LATIN SMALL LETTER J WITH CIRCUMFLEX`
- `U+0138 LATIN SMALL LETTER KRA`
- `U+013F LATIN CAPITAL LETTER L WITH MIDDLE DOT`
- `U+0140 LATIN SMALL LETTER L WITH MIDDLE DOT`
- `U+0149 LATIN SMALL LETTER N PRECEDED BY APOSTROPHE`
- `U+014A LATIN CAPITAL LETTER ENG`
- `U+014B LATIN SMALL LETTER ENG`
- `U+014C LATIN CAPITAL LETTER O WITH MACRON`
- `U+014D LATIN SMALL LETTER O WITH MACRON`
- `U+014E LATIN CAPITAL LETTER O WITH BREVE`
- `U+014F LATIN SMALL LETTER O WITH BREVE`
- `U+0156 LATIN CAPITAL LETTER R WITH CEDILLA`
- `U+0157 LATIN SMALL LETTER R WITH CEDILLA`
- `U+015C LATIN CAPITAL LETTER S WITH CIRCUMFLEX`
- `U+015D LATIN SMALL LETTER S WITH CIRCUMFLEX`
- `U+0162 LATIN CAPITAL LETTER T WITH CEDILLA`
- `U+0163 LATIN SMALL LETTER T WITH CEDILLA`
- `U+0166 LATIN CAPITAL LETTER T WITH STROKE`
- `U+0167 LATIN SMALL LETTER T WITH STROKE`
- `U+0168 LATIN CAPITAL LETTER U WITH TILDE`
- `U+0169 LATIN SMALL LETTER U WITH TILDE`
- `U+016C LATIN CAPITAL LETTER U WITH BREVE`
- `U+016D LATIN SMALL LETTER U WITH BREVE`
- `U+017F LATIN SMALL LETTER LONG S`
- `U+0180 LATIN SMALL LETTER B WITH STROKE`
- ... sample truncated; regenerate this report after choosing this expansion path.
