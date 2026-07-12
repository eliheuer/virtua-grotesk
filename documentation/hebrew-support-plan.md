# Hebrew Support Plan

This document tracks the Hebrew expansion of Virtua Grotesk. The goal is full
Google Fonts Hebrew support, using Rubik (a shipped Google Fonts
Latin/Arabic/Hebrew family, cloned at `/Users/eli/GH/repos/rubik`) as the
reference for glyph inventory and source organization, and the glyph AI
harness (img2bez + designbot + OpenAI raster drafting) as the drawing tool.

## Current State (2026-07-12)

- **The full Hebrew skeleton is in both masters.** All 77 glyphs of Rubik's
  exporting Hebrew inventory are registered in `contents.plist` and encoded:
  27 letters incl. finals (U+05D0–U+05EA), niqqud and dot marks
  (U+05B0–U+05BC, U+05C1, U+05C2, U+05C7), punctuation (U+05BE maqaf,
  U+05F2–U+05F4), the dagesh/shin-dot presentation forms
  (U+FB2A–U+FB4B, Rubik's subset), and U+20AA sheqel.
- **Five glyphs are drawn** (mark color orange, promoted via the harness):
  `dalet-hb`, `vav-hb`, `yod-hb`, `finalnun-hb`, `resh-hb`.
- **72 glyphs are empty placeholders**, mark color red (= broken/regenerate,
  the harness to-do signal). Letters carry a placeholder advance of 600;
  combining marks have no advance (width 0). Empty glyphs are trivially
  master-compatible.
- Naming follows the readable `*-hb` convention (Rubik's `uni05B8` is named
  `qamats-hb` here). Unicode assignments live in each `.glif`.

## Drawing Workflow

Use the glyph AI harness per `harness/RUNBOOK-codex.md`: green references +
raster generation, then `img2bez masters` — which traces one image per master
and reconciles them into interpolation-compatible outlines in a single
command (the old single-master-trace constraint is gone). Check the report's
`compatible: true` before promotion, then re-mark blue for human grading.

Rubik metrics are proportions only — trace targets are Virtua's coordinate
system (UPM 1024, ascender 832, descender -256, x-height 576, grid 2), e.g.
`--fit descender:ascender` style zone bands rather than copied coordinates.

## Suggested Batch Order

1. Remaining simple-silhouette letters: `he-hb`, `het-hb`, `tav-hb`,
   `kaf-hb`, `finalkaf-hb`, `bet-hb` — rectilinear constructions close to
   the drawn five.
2. The rest of the letters and finals.
3. Punctuation, `sheqel`, `yodyod-hb`.
4. Niqqud marks + anchors, `languagesystem hebr dflt;`, mark/mkmk
   positioning, GDEF classes.
5. Dagesh presentation forms (mostly composites of letter + dagesh once
   anchors exist).

## QA Notes

- Empty placeholders will show as blank glyphs and will fail glyph-content
  QA until drawn — that is the intended burn-down signal (do not add
  excludes to hide them).
- Proof strings should mix Latin, Arabic, and Hebrew; rerun `make reports`,
  `make build`, and `make preflight` after each promoted batch.
