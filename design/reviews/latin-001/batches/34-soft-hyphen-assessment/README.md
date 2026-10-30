# LAT-001 batch34 · Soft-hyphen behavior assessment

Assessment of frozen source revision `9359e981`; no active font or source edits.
U+00AD remains absent from the cmap. In the tested Codex in-app browser,
English manual hyphenation already displays a hyphen at the selected break,
while unbroken text hides U+00AD and keeps the plain word's width. This is
observed behavior in one browser, not cross-platform certification or cmap
completion.

## Evidence and interpretation

- `assessment.json` freezes all1821 active source-file hashes, the326 Arabic
  recursive dependencies/master and green131 Regular/74 Bold sources. Hyphen's
  eight-member reverse closure/master has no Arabic intersection. Both hyphen
  donors remain unchanged: Regular yellow, Bold orange; neither is promoted to
  an approved construction reference. Existing U+2010 uses the hyphen component.
- The active VF hash matches batch33's final receipt. Virtua has U+002D and
  U+2010, but no U+00AD or U+2011. Pinned Rubik has U+00AD and U+002D; it lacks
  U+2010/U+2011. These are encoding facts, not equivalent implementation choices.
-75 shaping cases cover three words, five VF weights400/475/550/625/700 and
  five fonts (Virtua, Rubik and three diagnostic cmap variants). Default
  HarfBuzz output has the same visible glyphs, positions and advances as plain
  text. With `PRESERVE_DEFAULT_IGNORABLES`, current Virtua exposes `.notdef` at
  U+00AD with600 advance; Rubik exposes its encoded glyph. This flag is a
  diagnostic/legacy path, not normal line-break processing.
- Browser fixtures at400/550/700 use English,32px text,160px narrow columns,
  `hyphens: manual`, `hyphens: none`, explicit hyphen/hard-break controls and
  unbroken soft-hyphen/plain controls. Both fonts show two lines with a hyphen
  in manual mode and one overflowing unhyphenated line in none mode. No-wrap
  widths are exactly equal within each font/weight. Full screenshots and AX
  measurements are retained in `browser/`.
- Three **diagnostic-only** binaries change cmap entries, never outlines:
  U+00AD→hyphen, U+00AD→H, and U+2010→H. At all three browser weights the first
  two still break as `extra-`; the third breaks as `extraH`. This isolates
  selection of U+2010 for this Virtua browser break. It does not identify the
  mechanism used for Rubik or other applications. Probe binaries must never
  be promoted to sources, release packages, or normal proof inputs.
- Stock Diffenator3 coverage HTML is preserved. A separately labeled same-text
  supplement was inspected in both fonts at400/550/700 (six screenshots).
  U+00AD remains hidden in the sampled unbroken words, including `office`.
  The controlled line-break fixture is separate because ordinary Diffenator
  text alone does not establish discretionary-hyphen behavior. Virtua Bold
  remains denser, with less even word rhythm than Rubik; not human approval.

[Unicode UAX14 §5.4](https://www.unicode.org/reports/tr14/#SoftHyphen) assigns
soft hyphen an optional intraword break role; the layout implementation chooses
its visible realization. [CSS Text3 §5.3](https://www.w3.org/TR/css-text-3/#hyphenation)
defines `manual` and `none` handling. Both were checked2026-10-22. The
[Google Fonts QA guide](https://googlefonts.github.io/gf-guide/qa.html) separates
binary checks and actual browser/application review. No font data was uploaded.

## Disposition and next work

The next bounded engineering candidate is an encoded U+00AD compatibility
wrapper reusing the exact existing hyphen, with440 advance in both masters.
This would address direct-cmap/legacy access, **not repair the already working
browser behavior**. Preserve the original donor geometry and grades; use a
new purple wrapper, current hash guards, both-master registration, and verify
normal default-ignorable behavior, preserved-ignorable output, subsets and the
same actual line-break fixtures before application. Do not use a blank visible
placeholder or copy Rubik. There is no need to redesign the hyphen to add this
encoding. U+2011 remains a separate nonbreaking-behavior task.

No rebuild, raw DesignBot, preflight or full Fontspector rerun was needed for
this read-only assessment. All five active TTF hashes remain exact. Latest
full online package results remain batch33:12 FAIL/9 WARN/160 PASS/10 INFO/
40 SKIP; the216 Hebrew engineering failures remain open. The Rubik cmap gap
is still340 (182 Cyrillic,56 Common,102 Arabic presentation forms).
Arabic60272/current case/layout and Runebender were untouched. Local evidence
checkpoint only; no push or publication.

## Reproduction

Run `assess.py` with repository `.venv/bin/python` only against its frozen
source hashes; it refuses changed sources. It writes local diagnostic binaries
and fixtures to `out/review-latin-d2513094/batch34/`. Run `diffenator.py` for
stock and supplemented Diffenator HTML. Inspect browser output again; scripts
alone do not reproduce visual approval. Frozen asset copies are in `assets/`.

- [Controlled400 comparison](http://127.0.0.1:60273/batch34/comparison-400.html)
- [Diffenator supplement](http://127.0.0.1:60273/batch34/comparison/soft-hyphen.html)
