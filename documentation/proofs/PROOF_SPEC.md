# Virtua Grotesk — Print Proof Spec

Working spec for the designbot-built print proof(s). Derived from research into
Klim/RoboFont specimen conventions, the Adobe `drawBotProofing` + DJR
`Drawbot-Type-Proofs` codebases, VF interpolation-proof repos, and Google Fonts'
diffenator2 / fontspector coverage. **The old `general_proof.rs` /
`print_spacing_specimen.rs` are not being replicated** — this is a clean design.

## Two documents, not one

Research surfaced a hard split. We build them as two separate artifacts:

| | **QA Print Proof** (`make proof`) | **Marketing Specimen** (`make specimen`) |
|---|---|---|
| Job | Catch bugs (spacing, kerning, marks, interpolation) | Sell the typeface, show its range |
| Look | Systematic, dense, ugly-on-purpose | Curated, designed, on-brand |
| Priority | **Build first** | Later |
| Output | `documentation/proofs/proof.pdf` | `documentation/proofs/specimen.pdf` |

This doc specs the **QA Print Proof** in full; the specimen is sketched at the end.

## Font facts (drive everything off these)

- Variable, single axis **`wght` 400–700**, default 400. 4 named instances:
  Regular 400 / Medium 500 / SemiBold 600 / Bold 700.
- UPM **1024**. Metrics: ascender/cap 768, x-height 576, baseline 0,
  descender −256, overshoot 16.
- **Latin and Arabic.** Arabic is in scope and proofed: finishing it is the
  work left before submission, so the proof has to be able to carry it.
  Hebrew is compiled into the TTF but not proofed.
- 751 glyphs / 550 codepoints. Features present: `kern`, `mark`, `mkmk`, `tnum`,
  `ccmp`, `locl`, and the Arabic shaping features `init`/`medi`/`fina`/`rlig`.
- Drive off `fonts/variable/VirtuaGrotesk[wght].ttf` via
  `font_variation("wght", …)` — **never** re-parse SFNT (that was the old mess).

## Design system to reuse

- OG palette: bg `#92928e`, ink `#232323`, 6 OKLCH hues (red/orange/yellow/
  green/blue/purple). Proof pages are mostly ink-on-paper; palette is for the
  cover, labels, and pass/fail accents.
- 8-unit / 2-unit "grid systems as datasets" north-star. An optional grid /
  dimension-sheet overlay is the on-brand hero motif (belongs to the specimen,
  offered as a toggle on the proof).

## Coverage principle

The print proof must be a **superset by eye** of the diffenator2 `proof` view
(Glyphs / Text / Waterfall / Proofer) and let a human confirm every visual
category fontspector checks (marks, soft-dotted, tnum, vertical metrics,
coverage, interpolation). Fine outline QA (jaggies, colinear vectors) stays
fontspector's job — noted, not duplicated.

## Locked decisions

- **Page format:** US Letter landscape (792 × 612 pt).
- **Kerning:** control strings + running words toggled kern on/off. No
  synthesized pair table.
- **Build order:** engine + core pages (cover, glyph grid, waterfall, spacing)
  → review the look → then the remaining pages.

## Page-by-page (QA proof, in order)

Order = coverage → metrics → spacing → marks → kerning → sizes → weight →
interpolation → running text → features. Bugs caught lowest-level first. Every
page carries a running head: family · axis instance · point size · page N ·
date, so printed pages are self-identifying.

| # | Page | Shows | Covers | Weight(s) |
|---|---|---|---|---|
| 0 | **Cover / metadata** | Family, axis range + 4 instances w/ coords, UPM, glyph count, version, date, subsets. On-brand OG palette. | name/STAT/fvar (eyeball) | — |
| 1 | **Glyph grid** | Every glyph, one per cell, sized by UPM scale, auto-paginated. | completeness, .notdef, missing/modified | 400 + 700 |
| 2 | **Vertical metrics** | Metric lines (768/576/0/−256, overshoot 16) with tallest/lowest glyphs; overshoot alignment `o O n H`. | vertical metrics, clipping | 400 |
| 3 | **Spacing (kern OFF)** | DJR control-string method: per char, category control (`H`/`O`, `n`/`o`, `0`/`1`), pattern `HHXHOHOXOO`; lc×lc, UC×UC, figures, punct. | sidebearings/spacing | 400 + 700 |
| 4 | **Figures / numerals** | `0123456789`, **tabular column stack (verify equal `tnum` widths)**, currency `$ € £ ¥ ¢`, `$14.95`, fractions if present. Kern off. | numerals, tnum | 400 + 700 |
| 5 | **Accents / diacritics** | Explicit rows per mark (acute grave circ tilde diaeresis caron breve ring ogonek dotaccent macron cedilla), **UC + lc**, real words; bases æ ð ø ß; mark-over-base stacks. | marks, mkmk, soft-dotted (i/j), dotted-circle | 400 + 700 |
| 6 | **Kerning** | Classic problem strings `AV AW AY LT LV LY TA VA WA To Ta Te r. r, f) P. F.`, quotes+caps, num+punct — kern ON; plus running words kern on-vs-off. | kerning | 400 + 700 |
| 7 | **Size waterfall** | `Hamburgefonstiv` / `QUICK WAFTING ZEPHYRS VEX BOLD JIM.` / `minimum` / figure ladder, descending 72→8pt. Finds min legible size. | size range | 400 |
| 8 | **Weight waterfall** | One control string at 400/500/600/700 (+ 2 interp midpoints), stacked same size, to read weight progression. | weight/contrast (VF) | all |
| 9 | **Interpolation grid** | n-botthof method: per glyph (`o n H a e g` + troublemakers), show it across every weight stop consecutively — kinks/reversals/overshoot drift jump out. | interpolation sanity (VF) | all |
| 10 | **Text / paragraphs** | Running paragraphs 12/10/8pt, systematic charset-consumption for full coverage, one block per supported Latin-Ext language (locl forms). | running text, language coverage, locl | 400 + 700 |
| 11 | **OpenType features** | Any `liga tnum onum case locl frac zero ss/cv` present: default vs feature-on, side by side. | OT features fire & look right | 400 |

## Variable-font handling

- Most pages render at masters **400 & 700**; pages 8–9 sweep all four instances
  plus a couple of unnamed interpolation midpoints.
- Weight waterfall (8) replaces a size ladder with an **axis ladder** (same size,
  `wght` stepping).
- Interpolation grid (9) is the highest-value VF page — glyph-outer, weight-inner
  loop.

## Kerning philosophy (a real fork)

The established tools (Adobe, DJR) **deliberately do not synthesize kerning-pair
tables** — they use category control strings + real frequency-word text + a
kern on/off toggle. The old Virtua proof hand-coded a pair table. Recommendation:
**follow the established approach** (page 6 = curated problem strings + on/off
running words). Explicit exhaustive pair pages are available if wanted, but no
reference tool does it.

## Architecture — a built-in default proof

The default proof is a **first-class designbot feature, not a per-repo script**.
designbot ships a complete proof generator that introspects any font and emits
the full multi-page PDF with zero per-repo code:

```
designbot proof fonts/variable/VirtuaGrotesk[wght].ttf -o documentation/proofs/proof.pdf
```

This means:
- **Nothing to maintain in Virtua** (or any font repo) for the standard proof —
  it's `make proof` calling one designbot command. Fixes/improvements to the
  proof land once, in designbot, and every font benefits.
- The generator **reads the font itself** for everything it needs: fvar axes +
  named instances, cmap/glyph list, name/version, vertical metrics, feature list
  (`tnum`/`kern`/`mark`/`locl`/…), per-glyph advances. (New introspection in
  designbot, most likely via `skrifa`/`read-fonts`, already in the Vello/parley
  tree. No hand-rolled SFNT parsing.)
- Page selection **adapts to the font**: single-master fonts skip the weight/
  interpolation pages; a font without `tnum` skips the tabular check; only the
  languages the font actually covers get text blocks.

Per-repo **custom** proofs remain possible — a repo drops extra `.rs` scripts
under `documentation/proofs/` exactly like the social-image scripts — but that's
the exception, for showings the default proof doesn't cover. Virtua is the
reference/test font for getting the default proof looking great first.

## Makefile

- `make proof` → `designbot proof $(VARIABLE_FONT) -o documentation/proofs/proof.pdf`
  (the built-in default proof — no repo script).
- `make specimen` → `documentation/proofs/specimen.pdf` (marketing, later; may be
  a built-in `designbot specimen` too, or a per-repo on-brand script).
- `make review` / `review-rubik` (diffenator2) stay as the GF review gate — the
  print proof is the internal design-review artifact, not a replacement.

## Marketing specimen (sketch, build later)

Klim order: hero/headline → design narrative + credits + tech table → weights
index → language support → curated text settings (large→small) → OpenType
showcase → numeral styles → full glyph display → footer. On-brand: OG palette,
the grid-as-dataset dimension-sheet hero (Bézier points + power-of-two stem/
advance labels), "Grid Systems for Dataset Engineering".

## Arabic pages

Added to the designbot built-in (`designbot-render/src/proof.rs`), gated on the
font actually covering the script, so a latin-only font proofs exactly as before.
Eleven sheets, in build order:

| Page | What it catches |
|---|---|
| Arabic Character Set | a missing or misencoded glyph; combining marks shown on a dotted circle |
| Joining — Positional Forms | a wrong `init`/`medi`/`fina` substitution, a stub that misses its neighbour |
| Mark Attachment (2 sheets) | every harakat on every skeleton, against a baseline rule — anchors that sit off the shared line |
| Dot Clusters & Ligatures | dot clusters merging where two dotted letters meet; the four lam-alef ligatures |
| Running Text & Waterfall | the abjad, then vocalised text down the sizes |
| Quranic Text — Al-Fatiha | the densest ordinary mark stacking: shadda over fatha, tanwin, superscript alef, alef wasla |
| Quranic Text — Running Paragraphs | wrapping meeting mark stacking |
| Long Text — Surah Yusuf (2 sheets) | colour and spacing in aggregate at 13pt and 9.5pt |
| Weights | mark anchors drifting sideways or vertically across the axis |

Scripture is byte-exact from tanzil via api.alquran.cloud. Al-Fatiha is in the
Uthmani orthography (fully covered by the font); the rest are in the simple
orthography, and Surah Yusuf has its waqf marks dropped — those are recitation
annotations rather than part of the words, and no ordinary Arabic character set
encodes them.

Known gaps this surfaced, all Quranic annotation marks the font does not yet
have: U+06D6, U+06D7, U+06DA, U+06DE, U+06DF, U+06E2, U+06E5, U+06E6, U+06ED.
