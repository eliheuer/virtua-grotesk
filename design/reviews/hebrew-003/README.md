# HEB-003 — Bet, Kaf and Final Kaf

2026-10-19. **Candidate v2 approved, applied and verified.**
Eli asked to resume Hebrew after the mode-indicator correction. This opens the
next proposed related group: ב U+05D1, כ U+05DB, ך U+05DA in both masters.

Open `make proof-web`, currently localhost:60272. The previous HEB-002 server
remains on 60271. The current proof shows Before / Candidate / Rubik / Noto, including Toggle.
The initial Current / Rubik / Noto inspection is retained in `baseline/`.
The manifest owns this study's identities, samples and status; it does not
relabel the previous case or invent a candidate.

## Verified baseline

Current is the exact HEB-002 Applied binary, hash
`70dc500c2240b606da09de615e85e0631966c004f1cdd6f14ced60d337a04edf`,
which equals the current variable font on disk. Reference hashes are unchanged.
[source-inspection.json](source-inspection.json) records all six source hashes
and point listings. [compiled-check.json](compiled-check.json) confirms equal
compiled outlines and advances at 400 and 700 for all three letters.

| Glyph | Advance | Point bounds | Points | Straight measurements |
| --- | ---: | --- | ---: | --- |
| Bet | 532 | (14, 0)–(518, 576) | 16 | Stem 88; roof 78; base 80; right foot projects 62 |
| Kaf | 460 | (14, 0)–(428, 576) | 18 | Top terminal 78; bottom terminal 80 |
| Final Kaf | 490 | (14, −182)–(434, 576) | 12 | Stem 88; roof 78 |

These are source point bounds, not a curve-extrema calculation. Each glyph has
one contour. Regular is orange; Bold has the blue mark color but contains a
standalone outline. Preserve existing drawings and colors; do not interpret
blue as AI output or silently approve either master.

## Review and proposed direction

The native-font browser proof was inspected at 400 and 700. Virtua remains thin
at Bold; Rubik and Noto visibly gain weight. Exposed straight terminals lack
the chamfer construction already established in Virtua's reviewed Hebrew.
Reference weights are not claimed to be optical matches.

Proposed next scratch trial, pending design feedback:

- Develop real weight progression in both masters, using the previous Hebrew
  trial as a starting point and live green Latin as the construction authority.
  The cross-script weight relationship remains provisional.
- Preserve Bet's projecting foot and clear distinction from Kaf. Give their
  related right curves coherent construction without making them identical.
- Preserve Final Kaf's descending identity; inspect its shoulder-to-stem tangent
  and descender balance in words before choosing any length change.
- Use 16-unit straight chamfers on exposed corners and deliberate smooth cubic
  curves, on the machine draft lattice. Recheck spacing and anchor placement.
- Include בּ / כּ / ךּ and vowel contexts in the eventual family review; base
  edits alone do not establish marked-form correctness or Google Fonts readiness.

No donor curves have been selected or reused yet. Read live donors before the
scratch trial, retain the existing outline information, and follow the drawing,
grid, compatibility, compiled shaping and proof gates. The current inspection
is not drawing approval or submission QA.

Evidence: [Regular](baseline/regular.png), [Bold](baseline/bold.png).

## Candidate authorization — 2026-10-19, 19:47

Eli: “ok go for it and do that work,” referring to the proposed weight,
chamfer and curve work. Prepare the three-glyph candidate in both scratch
masters, then present it for review. No active-source application is implied.
First fix specimen rule thickness and control spacing as requested in the same
message (P043). Preserve the live drawings, existing unrelated work and colors.

### Scratch v1 construction plan

One contour per glyph, matching point structure between masters. Flat tops stay
at 576. Bet advances 544/640 with 16-unit sidebearings, 96/192 stems, 96/168 roof
and base bars and a 64-unit projecting foot. Kaf advances 480/576, bearings
16/48, with 96/192 side weight and 96/168 terminal bars. Final Kaf advances
496/592 with bearings 16/56 and a −184 descender (the existing −182 adapted to
8). Bold adds 96 width to retain open counters. These are trial dimensions.

Bet and Final Kaf use the live green n outer right quadrant translated to the
Hebrew top, and the reviewed resh inner shoulder. Kaf adapts green o's symmetric
right-half construction to a 0–576 open bowl: Regular outer quadrant handles
128 horizontal / 184 vertical, Bold 168 / 168; inner handles 88 / 128 and
64 / 80. This is a deliberate 8-grid adaptation, not exact optical reuse of o.
H/E supply the exposed 16-unit and concave 8-unit corner patterns. Donors remain
unchanged. Target colors and original Unicode values are retained. Central
anchors move +48 x in Bold, right anchors +96; anchors are snapped to 8 and
recorded individually for mark review. Original GLIFs are preserved in scratch.


Scratch v1 mark checking found collisions between Final Kaf's descending stem
and below marks at intermediate/Bold weights. V2 retains the drawings but moves
its hbBottom/hbMeteg/hbCantBelow/hbCantBelowRight anchors to x=208 in both masters
instead of the generic +48 Bold shift. The widest tested below mark then has
16 units of clearance to the inner stem at x=344. Other anchor rules remain.
V1 stays in ignored scratch for diagnosis; it is not the review candidate.

## Candidate v2 ready for review

Eli reaffirmed “draw the new hebrew codepoints” while the scratch build was
underway. All six target drawings are now prepared and compiled. No active
source file was edited. The case retains the exact [before and candidate GLIFs](candidate-v2-sources/),
[scope and anchor changes](candidate-v2-scope.json), variable binaries and OFL
licenses in `candidate-v2/fonts/`, and a portable `candidate-v2/snapshot.json`.
The complete isolated build is in `out/qa/2026-10-19/hebrew-003-v2/`.

Validation:

- [Grid](candidate-v2-grid.json): six glyph-masters, zero off-grid findings.
- Both curve-lint runs clean; full master report has zero blocking mismatches.
- Canonical scratch `make preflight` passed: variable font, four static fonts,
  PDF and reports generated. Preflight is an artifact check, not release approval.
- [Compiled validation](candidate-v2-validation.json): 6,048 glyph/weight
  comparisons across seven weights. Only Bet, Kaf, Final Kaf and the two
  inherited rafe outlines differ; only the three base advances differ.
- 294 before/candidate mark pairs across seven weights have no ink intersections.
  [Hebrew QA](candidate-v2-hebrew-qa.json) reports zero failed checks.
- All active source hashes still match the captured baseline; source edits are
  limited to the six scratch GLIFs. Existing colors and Unicode values survive.

Agent visual review: Regular, midpoint and Bold group proofs, each large Bold glyph,
marked text and Bold running text inspected in the browser. The new shapes have
visible chamfers and real Bold progression; Bet retains its projecting foot,
Kaf remains open, and Final Kaf retains the descending stem. This remains a
trial requiring Eli's design judgment. The running text still shows uneven
weight from other unfinished Hebrew letters; this batch does not solve those.

Evidence: [Regular](candidate-v2/regular.png), [Bold](candidate-v2/bold.png), [midpoint](candidate-v2/midpoint.png),
[Bet](candidate-v2/bet-detail.png), [Kaf](candidate-v2/kaf-detail.png),
[Final Kaf](candidate-v2/finalkaf-detail.png), [marks](candidate-v2/marks-bold.png),
[running text](candidate-v2/text-bold.png).

### Protected dependencies

Regular `uniFB4C` and `uniFB4D` are purple composites. Their compiled outlines
inherit the changed bases, but their original advances and rafe offsets remain;
those metrics no longer track the wider Bold bases. The three standalone
`betdagesh-hb`, `kafdagesh-hb`, `finalkafdagesh-hb` Regular drawings are also
purple and unchanged. Normal base-plus-mark shaping was tested separately.
Do not claim the presentation forms are updated or ship-ready. Keep this
explicit follow-up when deciding whether/how to apply the six base drawings.

### Specimen correction (P043)

Eli accepted the compact control layout before reaffirming the drawing work.
Rules and slider tracks are now 2px, with rounded ends. The field-rule-to-slider
center and slider-center-to-caption-rule intervals both measure 16px at U=32;
controls begin U/2 below the menu. Original page margins and shared UI size
remain. [UI evidence](baseline/compact-controls.png).

## Applied — 2026-10-19

Eli: “ok this looks good, ship it, next?” Applied the exact six reviewed base
GLIFs, preserving colors and all unrelated source bytes. [Application receipt](application-v2.json)
records before/after hashes and checks. Active preflight, grid, curve lint,
compatibility and Hebrew checks pass. The rebuilt variable matches all reviewed
candidate tables except the head modification timestamp/checksum. The proof now
serves the actual applied binary; the original candidate manifest and binary are
retained. This is source application, not a public Google Fonts release.

Protected marked-form follow-ups above remain open. Next proposed group:
[HEB-004 — Pe and Final Pe](../hebrew-004/README.md), building on Kaf's bowl and
Final Kaf's descender. No new drawings for that group yet.
