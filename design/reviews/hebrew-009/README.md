# HEB-009 — marked-form reconciliation

Reconciliation following the read-only audit after retaining HEB-008 v7 in commit `df38c4a`. All 27 base/final
letters now have distinct master drawings, and all 76 frozen Rubik Hebrew
codepoints are present. This establishes coverage/development, not grading.

29 stored presentation forms retain identical Regular/Bold outlines. The five
Shin examples in `marked-shin-audit.png` compare the stored glyph (left) with
the actual compiled current base plus marks (right), at 400 and 700.
`audit.json` records the exact compiled font hash and HarfBuzz placements.
These are direct-outline diagnostics: normal text shaping may decompose the
precomposed codepoint and conceal the stale stored glyph.

Authorized repair: rebuild each form below from its current base and existing
marks in both masters, preserve Unicode and grading, and verify compatibility,
compiled shaping and before/after renders. Prefer reusable source components
where the build supports them; inspect flattening/nested-composite behavior.
Do not alter standalone mark drawings or unrelated letters in this repair.
Regular forms are purple-protected. Eli explicitly approved rebuilding these
29 forms in both masters on 2026-10-20. Standalone marks and grades remain
unchanged. Preparation and application evidence follows below.

| Codepoint | Glyph | Requested scope |
| --- | --- | --- |
| U+FB2A | shinshindot-hb | Regular and Bold |
| U+FB2B | shinsindot-hb | Regular and Bold |
| U+FB2C | shindageshshindot-hb | Regular and Bold |
| U+FB2D | shindageshsindot-hb | Regular and Bold |
| U+FB2E | alefpatah-hb | Regular and Bold |
| U+FB2F | alefqamats-hb | Regular and Bold |
| U+FB30 | alefdagesh-hb | Regular and Bold |
| U+FB31 | betdagesh-hb | Regular and Bold |
| U+FB32 | gimeldagesh-hb | Regular and Bold |
| U+FB33 | daletdagesh-hb | Regular and Bold |
| U+FB34 | hedagesh-hb | Regular and Bold |
| U+FB35 | vavdagesh-hb | Regular and Bold |
| U+FB36 | zayindagesh-hb | Regular and Bold |
| U+FB38 | tetdagesh-hb | Regular and Bold |
| U+FB39 | yoddagesh-hb | Regular and Bold |
| U+FB3A | finalkafdagesh-hb | Regular and Bold |
| U+FB3B | kafdagesh-hb | Regular and Bold |
| U+FB3C | lameddagesh-hb | Regular and Bold |
| U+FB3E | memdagesh-hb | Regular and Bold |
| U+FB40 | nundagesh-hb | Regular and Bold |
| U+FB41 | samekhdagesh-hb | Regular and Bold |
| U+FB43 | finalpedagesh-hb | Regular and Bold |
| U+FB44 | pedagesh-hb | Regular and Bold |
| U+FB46 | tsadidagesh-hb | Regular and Bold |
| U+FB47 | qofdagesh-hb | Regular and Bold |
| U+FB48 | reshdagesh-hb | Regular and Bold |
| U+FB49 | shindagesh-hb | Regular and Bold |
| U+FB4A | tavdagesh-hb | Regular and Bold |
| U+FB4B | vavholam-hb | Regular and Bold |

After these forms: review niqqud weight/placement, punctuation and running-text
spacing. Keep native-reader review separate from numerical checks. Eli wants
a whole-font human grading pass after basic Hebrew, then to consider an
unattended Arabic drafting run using the resulting permissions and references.
No overnight automation or Arabic job has been started.

## Applied reconciliation — 2026-10-20

Eli answered **“Yes, rebuild those 29 forms in both masters.”** The 58 active
GLIFs now contain the current base plus unchanged marks as direct components.
No donor is itself a composite, and no other source component references these
29 targets. Component order matches across masters. Advances follow the current
base; attachment anchors follow the base and translated mark anchors. Unicode,
review colors and all non-target source bytes are unchanged, including the manual
Zayin, Gimel and Regular Final Tsadi drawings.

`rebuild.json` freezes source hashes, before/candidate hashes, component offsets
and the exact authorization. `before-sources/` and `candidate-sources/` retain
all 58 files. `rebuild.py apply` guards against source drift and is not a generic
permission to reapply over later manual edits. The earlier audit is preserved.

Verification against the compiled variable font:

- `make preflight` passed; source compatibility reports zero blocking mismatches.
- 203 raw stored-form comparisons at seven weights (400–700) match the shaped
  current base and marks within 1/3 font unit of HarfBuzz rounding. Changes to
  compiled outlines/advances are confined to the 29 named forms.
- 423 precomposed-plus-mark contexts match their canonical decompositions;
  the existing decomposed text shaping is unchanged. Hebrew smoke checks pass.
- All rebuilt forms are single-level composites, avoiding the earlier nested
  TrueType component regression.
- Full offline Fontspector: **1 FAIL, 28 WARN, 39 INFO, 525 PASS, 299 SKIP**.
  The failure is `dirname_matches_nameid_1` for the development `fonts/ttf`
  directory. Counts match the prior full run; warnings and offline skips remain
  release work, not exemptions. See `qa-full/` for exact inputs and findings.

`stored-forms-400.png`, `stored-forms-550.png`, and `stored-forms-700.png` render
all 29 raw glyphs from the compiled fonts, Before left / Working right. Regular
and Bold sheets were visually inspected: the stale constructions are replaced
by the current base drawings, with open counters and visible marks. These are
Cairo diagnostics, not browser screenshots or human grading. Standalone mark
weight remains unchanged and should be judged alongside the heavier letters.

The live proof is `working-v1/`, with frozen Before / Working / Rubik / Noto
fonts and licenses. Its selected examples are marked Shin, Bet and Pe; the
sample menu also groups the other repaired forms. Text mode supports running
text and custom passages. Browser display has not been visually reverified in
this run; the launcher verified the four font hashes and serves port 60272.

Next: niqqud texture, combined marks, punctuation and running-text spacing,
then Eli’s whole-font grading pass. No new standalone-mark drawing permission
is implied by this exception. An unattended Arabic run can follow a defined
scope and reference set from that grading pass; it has not been scheduled.

## Heading overflow correction — 2026-10-20

Eli reported colliding long glyph names in the live specimen (22:02 screenshot).
The old `white-space: nowrap` heading rule lets names paint across adjacent
columns. Repair the responsive identity grid and name wrapping, retaining
full names, Unicode, the shared headline/UI sizes and established page margins.
This is a proof-layout correction only, not a font drawing change.

Applied in the canonical `app/review.css` and regenerated the current proof.
Identity cells now use a responsive minimum-width grid; long names wrap inside
their cell and Unicode labels align at each row’s bottom. The shared type scale
and page margins remain. Browser DOM checks found no cell/page overflow at
333, 711 and 1333 CSS pixels (viewport requests 360, 768 and 1440 under the
browser’s current scaling). The normal-width browser screenshot was visually
inspected and retained in `heading-layout-fixed.jpg`; measurements are in
`heading-layout-checks.json`. The temporary viewport override was reset.
