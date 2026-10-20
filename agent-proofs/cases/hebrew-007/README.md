# HEB-007 — Gimel, Lamed and Qof

2026-10-20. Working v2 is installed in both active masters under Eli's standing
authorization to draw directly into the files. No extra application approval is
required. Human grading and final script acceptance remain separate.

## Scope and construction

Six GLIFs: `gimel-hb` U+05D2, `lamed-hb` U+05DC, `qof-hb` U+05E7 in Regular and
Bold. Their previous Bold outlines duplicated Regular. The before sources are
preserved in `before-sources/`; the browser's Before binary was built immediately
before this batch, including both manual Zayin corrections.

- Retain Gimel's angled main stroke and left foot, Lamed's ascender and curved
  return, and Qof's separate descending stem. External reference outlines were
  not copied. Rubik and Noto remain visual/script references.
- Green Virtua n supplies the 96/192 upright stem-weight contract; accepted
  Kaf and Nun supply 96/168 bar weights. Green H/E and accepted Hebrew use
  16-unit exposed cuts. This batch adapts dimensions and construction principles,
  not an exact transplant of their curves.
- Lamed and Qof share a deliberately constructed upper shoulder: 160 horizontal
  by 176 vertical units, with horizontal and vertical arrival. Inner turns are
  compact: Regular 80 × 96, Bold 56 × 56 with 40-unit handles. The latter applies
  the measured local relationship from Bold Zayin to a comparable junction;
  its success here still needs human review, not automatic approval.
- Lamed's flat ascender aligns to 768 (previously 784); Qof descends to −192.
  Gimel advances are 392/488; Lamed and Qof are 496/592. Anchors retain their
  names and move to the drawing's 8-unit grid, with above anchors following
  ascender changes. Complete mark-position review remains open.
- Both manual Zayin GLIFs remain byte-identical to the saved correction pair.
  All existing target source colors are retained. No glyph was graded green.

## Inspection and refinement

First pass v1 is retained. Rendering exposed two problems in Bold: Qof's thick
stem overlapped the returning stroke; Gimel's left-foot outer curve doubled
back vertically. V2 moves Qof's return terminal 96 units right, leaving a
40-unit minimum horizontal separation from the descending stem, and restores
a consistently descending outer branch on Gimel. These are agent-detected
technical/visual corrections, not additions to the human correction corpus.

The broader lesson is to check stroke clearance after weight expansion and
inspect complete curves in addition to endpoints and tangents. Do not mark a
curve successful merely because its points are on-grid.

## Evidence and reproduction

- `application-v1.json`, `application-v2.json`: exact active-source identities.
- `before-sources/`, `working-v1-sources/`, `working-v2-sources/`: six GLIFs per state.
- `draw.py`: final deterministic drawing generator; dry-run by default. It
  refuses to replace an existing before snapshot. `draw-v1.py` retains the first
  pass. Final dry-run output matches all six active GLIFs exactly.
- `working-v2/snapshot.json`: portable, hashed fonts; `evidence.json` is the same
  input relative to this case. Run `agent-proofs/app/prepare.py --evidence
  agent-proofs/cases/hebrew-007/evidence.json --output-dir <new-directory>`.
  Copy the accompanying OFL license files when preparing another delivery.
- `working-v2/`: browser UI, Before/Working/Rubik/Noto fonts, licenses and
  screenshots at 400/550/700, large Qof and running Hebrew.
- `grid-v2.json`, `curve-regular.txt`, `curve-bold.txt`, `compatibility.md`,
  `hebrew-qa.json`, `preflight.log`: checks for this exact working revision.

Root `make preflight` passed (variable/static builds, PDF proof, metadata and
master reports, required artifacts). Six glyph-masters passed the 8-grid gate;
curve lint reports all clean; global master compatibility has zero blockers;
compiled Hebrew checks report zero failures. Browser rendering was inspected
at 400, 550 and 700, including a large Qof and running text. Checks ran on the
current working tree, which also contains unrelated saved editor changes;
they are not a clean-checkout release certification.

Review focus: Gimel's foot/main-stroke balance, Lamed's return weight, Qof's
clearance and counter, then marks and spacing in words. Protected standalone
marked forms are unchanged and do not necessarily inherit these new bases.
Next drawing group: Tet and Ayin; then Alef, Tsadi, Final Tsadi and Shin.
