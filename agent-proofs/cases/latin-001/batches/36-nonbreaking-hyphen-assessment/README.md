# LAT-001 batch36 · Nonbreaking-hyphen behavior assessment

Read-only assessment of revision `cd4e4fd7`. All 1,823 active source files and
five built font hashes remain exact. No source, grade, drawing, feature, metric,
kerning or release-package change. Arabic live proof60272 remains untouched.

## Results

Both Virtua and pinned Rubik lack U+2011. Unicode gives it a compatibility
`<noBreak> 2010` decomposition: NFD retains U+2011; NFKD replaces it with U+2010.
Line breaking belongs to the layout engine, independently of the displayed
hyphen outline; see [Unicode UAX14](https://www.unicode.org/reports/tr14/#GL).
Do not normalize compatibility text merely to make a glyph appear.

- 80 direct HarfBuzz samples cover four frozen/probe fonts at five weights,
  U+2011/U+2010/ASCII contexts, with default and preserved-ignorable modes.
  Flag modes agree. Full Virtua renders U+2011 through `uni2010`; full pinned
  Rubik returns `.notdef` in direct HarfBuzz. This is measured fallback behavior,
  not a new cmap entry or a canonical decomposition claim.
- 30 real subset samples expose the limit: a text-only Virtua subset requesting
  U+2011 drops U+2010 and gives `.notdef` at all five weights. Explicitly retaining
  U+2010 restores Virtua fallback at all five weights, with or without U+002D.
  Rubik still gives `.notdef` for all three subset requests. Total 20 missing-glyph
  samples out of30 across the two fonts. These are diagnostic subsets, not a
  change to serving metadata or evidence of a Google Fonts production failure.
- Actual browser English text at400/550/700 keeps U+2011 words on one overflowing
  line in a160px column, while U+2010/ASCII hyphens break into two lines. Both
  fonts visibly show hyphens; browser Rubik fallback differs from direct HarfBuzz,
  and its actual fallback font has not been identified. No claim it is Rubik ink.
- Two cmap-only Virtua diagnostic probes map either U+2011 or U+2010 to H.
  Both display H for the nonbreaking character while preserving its no-break
  behavior. The U+2010 probe also changes the ordinary hyphen control. This
  isolates Virtua's displayed U+2011 fallback to U+2010 in this browser.
  Probe fonts change only cmap/head and are never candidates or release inputs.
- Six controlled comparison/probe screenshots and six actual Diffenator
  Virtua/Rubik supplement screenshots were inspected at400/550/700. The original
  32px fixture crowded adjacent columns; final28px fixtures were regenerated and
  all six re-inspected. Font hashes and final measurements are retained.
  Dense Bold and inherited light hyphen remain optical findings. One browser,
  sampled English only; no exhaustive language, platform or native-reader approval.

Hyphen reverse closure now includes nine glyphs/master (including batch35
softhyphen), with no Arabic intersection. Arabic326/master and green131 Regular/
74 Bold are hashed. Hyphen donors remain yellow/orange and unchanged; no green
reference promotion. Source hashes, exact donor copies, font hashes and probe
mapping are in `assessment.json`; final preservation receipt is
`final-identity.json`. `subset-assessment.json` retains the30 results.

## Disposition and next work

No U+2011 alias is added: both reference cmaps lack it, normal sampled browser
behavior already works, and whether to guarantee direct-cmap/text-subset support
is a separate optional coverage decision. Keep the demonstrated subset fallback
limit explicit. This assessment is complete; do not repeat it as a drawing task.
Next inspect generic currency U+00A4 references and protected donors, then other
remaining Common symbols. Preserve the separate batch35 soft-hyphen retain/omit
release choice.

No build/preflight or new full-QA run is needed for this unchanged-source
assessment. Current package evidence remains batch35:12 FAIL/10 WARN/159 PASS/
10 INFO/40 SKIP, including the soft_hyphen policy warning. The216 Hebrew baseline
failures and Rubik gap339 (182 Cyrillic/55 Common/102 Arabic presentation forms)
are unchanged. Local only; no push or publication.

- [Controlled comparison](http://127.0.0.1:60273/batch36/comparison-400.html)
- [Actual Diffenator supplement](http://127.0.0.1:60273/batch36/comparison/nonbreaking-hyphen.html)
