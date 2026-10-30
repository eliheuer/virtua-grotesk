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

## Gimel foot-direction trial — v3, 2026-10-20

Eli requested trying a foot that sweeps the other way, as in Rubik and Noto,
before making manual edits. V3 replaces the separate downward left leg with a
continuous leftward sweep and a chamfered vertical terminal in both masters.
The first 15 points (head and main-stem approach), advances, anchors and colors
are unchanged; Lamed, Qof and both manual Zayins remain unchanged. Both Gimels
have matching 26-point topology. This is a requested trial, not final acceptance.

`gimel-sweep.py` reproduces the scoped change from frozen v2, refuses a changed
source baseline and is dry-run unless `--write` is passed. Exact new GLIFs and
hashes are in `working-v3-sources/` and `application-v3.json`. The current browser
proof is `working-v3/`, with v2 as Before, v3 as Working, plus Rubik and Noto.
Large Regular and Bold screenshots were inspected and saved there. The v2 proof
remains intact. `evidence-v3.json` and the proof's `snapshot.json` use portable
paths to the frozen binaries.

Root preflight, 8-grid check, curve lint in both masters and compiled Hebrew
checks pass. See `preflight-v3.log`, `grid-v3.json`, `hebrew-qa-v3.json`.
The prior `draw.py` describes v2; use the scoped v3 script for this foot trial.

## Manual correction 01 — Regular Gimel, 2026-10-20

Eli redrew Regular after the v3 foot-direction trial and requested a Bold
transfer test. `hand-edit-01-Regular-gimel.glif` preserves the latest saved
30-point outline exactly (including a further save that added the outer stem's
short vertical landing). The contour start moved; comparing raw point indices
without aligning contour order would misidentify the changes.

### Measured changes, not inferred intent

| Feature | Agent v3 Regular | Eli's saved Regular |
| --- | --- | --- |
| Stem → upper foot | (208,256) departs toward (176,192), unmarked corner | Departs toward (224,194), marked smooth |
| Tangent turn at that join | 40.601 degrees | 0.434 degrees (near-tangent optical correction) |
| Upper foot arrival | Curve arrives directly at chamfer start (32,96) | Curve ends at (64,96), with horizontal handle (160,96), then a 32-unit flat to (32,96) |
| Lower foot departure | Curve leaves chamfer end (32,0) directly | 32-unit flat to (64,0), horizontal handle (152,0) |
| Lower curve / inner leg | Curve ends at (240,128), then straight into leg | Handle (210,44) → (232,128), then 8-unit flat to (240,128) |
| Outer stem / baseline cut | Diagonal runs straight to (368,16) | Added (368,32), then 16-unit vertical run to (368,16) |

The 16-unit terminal chamfers, head, advance 392 and anchors remain intact.
The user retains optical 2-grid coordinates (210,44) and (224,194); do not snap
these to the machine grid. Exact hashes and all curve-join angles are recorded
in `hand-edit-01-comparison.json`. Short flats isolate curves from chamfers; the
upper join now continues the stem before turning left. Eli explicitly confirmed that the 8-unit inner shelf is deliberate and must
remain. Preserve it in this Gimel construction; this does not establish a
family-wide shelf rule or approve the rest of the Bold transfer.

### Bold transfer test — v4

Only active Bold was edited. Regular is byte-identical to the saved correction.
Bold follows Regular's 30-point order, segment types and smooth flags.
It retains the pre-test Bold head, advance 488, anchors and color, and carries:

- 32-unit horizontal landings at the terminal top and bottom, at x=32…64;
- foot-top y=168 (chosen to match existing Bold horizontal bars; v3 was 192);
- upper sweep (184,280) → handles (200,216), (152,168) → (64,168), with
  exact tangent continuation from the preceding 1:4 stem slope;
- lower sweep (64,0) → handles (160,0), (224,56) → (248,144), then an
  8-unit flat to (256,144);
- the new vertical landing at x=464, y=32…16 before the baseline chamfer.

These are provisional transfer choices, not a claim that the lesson has already
been learned successfully. Eli's verdict or next correction will test them.
`adapt-bold-v4.py` is dry-run-first and guards both live sources against changes;
`application-v4.json` and `working-v4-sources/` record the installed result.

### Why the previous check missed it; process change

The default `curve_lint.py` CLI checks crest centering and curve-to-curve tension.
It did not invoke its existing geometric continuity routines. Even those routines
treat unmarked points as intended corners. Therefore an "all clean" result did
not validate the line-to-curve construction I presented as checked.

New optional `--joins` output reports tangent angles at every line/curve and
curve/curve join, including unmarked corners, and flags marked-smooth kinks.
Unmarked corners are review evidence, never automatic failures or permission to
round them. A historical regression check confirms the old unmarked 40.6-degree
join is now visible in the audit; the saved near-tangent edit is under 0.5 degrees.
The intentional shelf corners remain visible instead of being smoothed away.

Checks: root preflight passed; global master compatibility has zero blockers;
compiled Hebrew checks report zero failures. All Bold draft points/anchors are
on 8; Regular's intentional 2-grid edits are preserved. New join audits are in
`join-audit-regular-v4.txt` and `join-audit-bold-v4.txt`. Browser screenshots at
400/550/700 are in `working-v4/`. Before is frozen v3; Working at 400 is Eli's
Regular and at 700 is the Bold test. This is pending human review, not approval.

## Continuation verdict — 2026-10-20

Eli said Gimel v4 was “good enough for now” and asked to move on and finish
Hebrew. Retain both masters as the working baseline, including the deliberate
8-unit flat. This accepts continuation, not green grading or release readiness.
The next case is [HEB-008](../hebrew-008/README.md).
