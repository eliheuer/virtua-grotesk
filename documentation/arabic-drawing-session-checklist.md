# Arabic Drawing Session Checklist

This generated checklist is the short working surface for today's
Arabic hand-review and cleanup session. It points to the current
batch, the exact source files to touch if a row becomes
`fix-needed`, and the commands that keep the Google Fonts handoff
evidence fresh.

## Current State

- Pending or fix-needed visual rows: 32
- Passed visual rows: 0
- Deferred visual rows: 0
- Edit rule: review first, then edit only the specific glyphs named in a `fix-needed` row.
- Compatibility rule: edit Regular and Bold together and preserve contour order, point count, and point types.
- Style rule: keep Virtua's monoline geometric drawing, even coordinates, and 16-unit chamfer logic.

## Start Here

1. Run `make arabic-before-drawing-check` before opening the sources.
2. Open `documentation/arabic-print-proof.pdf` and `documentation/arabic-print-proof-index.md`.
3. Open `documentation/arabic-current-review-worksheet.md` for the current five-row sheet.
4. Open `documentation/arabic-next-review-board.html` for snapshots, AI notes, proof links, and edit targets.
5. Record each row as `pass`, `fix-needed`, or `deferred` using the row commands below; do not leave reviewed rows implicit.
6. Optional: use `make arabic-visual-review-batch-tsv` only if you want a small batch-entry form instead of one command per row.

Editor checks for this session:

- `make arabic-before-drawing-check` runs the UFO editor and Runebender/Norad source-load checks.
- `make arabic-source-edit-diff-check` shows whether changed Arabic-like GLIF files are edited in both Regular and Bold.
- `make arabic-first-batch-source-checkpoint` records current Regular/Bold structure for the first-batch watch glyphs.
- `make arabic-pending-source-checkpoint` records Regular/Bold structure for all unresolved review source targets.
- `make ufo-editor-check` validates both UFO packages and every GLIF in strict mode.
- `make runebender-ufo-check` validates both active UFOs with the same Norad loader family Runebender uses.
- The canonical review record is `documentation/arabic-visual-review-log.md`; the TSV is only an optional temporary input form.
- If you use the TSV form, `make arabic-visual-review-batch-apply-check` applies it, regenerates reports, and reruns preflight.
- If either check fails, fix the source package before drawing.

## Current Batch

- Name: 2. Structure And Wrong-Glyph Sweep
- Why: Catch missing, blank, clipped, duplicated, malformed, or wrong-codepoint glyphs before judging spacing.
- Visual rows to decide: 5
- Source targets if fixes are needed: 14 existing, 0 missing

### Review Rows

- `proof-regular-glyphs` (GF proof: Regular glyphs)
  - Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
  - Open: `documentation/gftools-qa/Proof/Regular-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-review-snapshots/proof-regular-glyphs.png`
  - Pass: `make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`
  - Fix: `make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`
  - Defer: `make arabic-visual-review-update REVIEW_KEY=proof-regular-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"`
- `proof-medium-glyphs` (GF proof: Medium glyphs)
  - Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
  - Open: `documentation/gftools-qa/Proof/Medium-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-review-snapshots/proof-medium-glyphs.png`
  - Pass: `make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`
  - Fix: `make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`
  - Defer: `make arabic-visual-review-update REVIEW_KEY=proof-medium-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"`
- `proof-semibold-glyphs` (GF proof: SemiBold glyphs)
  - Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
  - Open: `documentation/gftools-qa/Proof/SemiBold-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-review-snapshots/proof-semibold-glyphs.png`
  - Pass: `make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`
  - Fix: `make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`
  - Defer: `make arabic-visual-review-update REVIEW_KEY=proof-semibold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"`
- `proof-bold-glyphs` (GF proof: Bold glyphs)
  - Cue: Glyphs proof: missing, clipped, blank, malformed, duplicated, or wrong-codepoint Arabic glyphs
  - Open: `documentation/gftools-qa/Proof/Bold-diffbrowsers_glyphs.html`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-review-snapshots/proof-bold-glyphs.png`
  - Pass: `make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`
  - Fix: `make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`
  - Defer: `make arabic-visual-review-update REVIEW_KEY=proof-bold-glyphs REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"`
- `class-letter-structures` (Glyph class: letter-structures)
  - Cue: sad, dad, tah, zah, meem, heh, wawHamzaabove, lam-alef forms; review sidebearing-risk glyphs in the focused proof
  - Open: `documentation/contour-cleanup-decision-log.md`; `documentation/arabic-cleanup-drawing-briefs.md`; `documentation/arabic-manual-review-dashboard.html`; `documentation/arabic-visual-risk-proof.html`; `documentation/arabic-review-snapshots/class-letter-structures.png`
  - Pass: `make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=pass REVIEWER="Name YYYY-MM-DD" NOTES="reviewed current proof/source evidence"`
  - Fix: `make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=fix-needed REVIEWER="Name YYYY-MM-DD" NOTES="specific glyph or proof issue"`
  - Defer: `make arabic-visual-review-update REVIEW_KEY=class-letter-structures REVIEW_STATUS=deferred REVIEWER="Name YYYY-MM-DD" NOTES="needs Arabic native-reader review"`

### Source Files To Touch Only After `fix-needed`

- `VirtuaGrotesk-Regular.ufo` `theh-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `theh-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `seen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `sheen-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `waw-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `madda-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `madda-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `hamzaabove-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `hamzaabove-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif`
- `VirtuaGrotesk-Regular.ufo` `hamzabelow-ar` -> `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif`
- `VirtuaGrotesk-Bold.ufo` `hamzabelow-ar` -> `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif`

### Glyph-Level Drawing Punchlist

Use this as the first-pass inspection order before changing
outlines. If a glyph needs work, edit the Regular and Bold
source files as a pair, then run the edit-loop checks below.

| Glyph | Masters | Review prompt source |
| --- | --- | --- |
| `hamzaabove-ar` | Bold, Regular | `U+0654 ARABIC HAMZA ABOVE` structure prompt |
| `hamzabelow-ar` | Bold, Regular | `U+0655 ARABIC HAMZA BELOW` structure prompt |
| `madda-ar` | Bold, Regular | `U+0653 ARABIC MADDAH ABOVE` structure prompt |
| `seen-ar` | Bold, Regular | `U+0633 ARABIC LETTER SEEN` structure prompt |
| `sheen-ar` | Bold, Regular | `U+0634 ARABIC LETTER SHEEN` structure prompt |
| `theh-ar` | Bold, Regular | `U+062B ARABIC LETTER THEH` structure prompt |
| `waw-ar` | Bold, Regular | `U+0648 ARABIC LETTER WAW` structure prompt |

## Edit Loop

After any source edit:

```bash
make arabic-source-edit-diff-check
make arabic-first-batch-source-checkpoint
make arabic-pending-source-checkpoint
make arabic-after-drawing-check
```

The diff check is a fast git-status guard for one-sided
Arabic-like GLIF edits. The source checkpoint records the first
batch's Regular/Bold structure after edits, and the pending
checkpoint checks every unresolved row's source targets. The
after-drawing target remains the full source/load/build/report/preflight check.

That target runs `make ufo-editor-check`, `make runebender-ufo-check`,
`./build.sh`, `make reports-only`, and `make preflight-only` in order.

After shaping-sensitive edits, also run:

```bash
make preflight
make kerning-proof-check
make kerning-proof-review-check
```

Before closing the Arabic goal, verify `documentation/arabic-goal-completion-audit.md`
shows every requirement as proven, including human visual review.

## Optional Batch Recording Shortcut

The per-row commands above are the clearest path. If you prefer
to record several reviewed rows at once, use the generated TSV
as a temporary input form:

```bash
make arabic-visual-review-batch-tsv
$EDITOR documentation/arabic-visual-review-batch.tsv
make arabic-visual-review-batch-dry-run
make arabic-visual-review-batch-apply-check
```

Leave rows blank until they are actually reviewed. Valid statuses are
`pass`, `fix-needed`, and `deferred`. The TSV is not canonical;
the canonical record remains `documentation/arabic-visual-review-log.md`.
