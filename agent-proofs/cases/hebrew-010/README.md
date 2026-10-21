# HEB-010 — Hebrew marks and spacing

Eli accepted the heading-wrap repair as readable and asked to continue toward
whole-font grading, then a possible overnight Arabic run (2026-10-20).

## Scope and source permissions

The 16 Bold marks below are blue repair targets. The standing Hebrew drawing
authorization covers bounded repairs preserving their existing construction.
Regular counterparts are purple and were **not changed**. Meteg (U+05BD) and
Rafe (U+05BF) are uncolored in Bold and excluded. No grading changed.

| Bold mark | Active GLIF |
| --- | --- |
| sheva-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheva-hb.glif` |
| hatafsegol-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hatafsegol-hb.glif` |
| hatafpatah-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hatafpatah-hb.glif` |
| hatafqamats-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hatafqamats-hb.glif` |
| hiriq-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hiriq-hb.glif` |
| tsere-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/tsere-hb.glif` |
| segol-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/segol-hb.glif` |
| patah-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/patah-hb.glif` |
| qamats-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/qamats-hb.glif` |
| holam-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/holam-hb.glif` |
| holamhaser-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/holamhaser-hb.glif` |
| qubuts-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/qubuts-hb.glif` |
| dagesh-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/dagesh-hb.glif` |
| shindot-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/shindot-hb.glif` |
| sindot-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/sindot-hb.glif` |
| qamatsqatan-hb | `sources/VirtuaGrotesk-Bold.ufo/glyphs/qamatsqatan-hb.glif` |

## Findings and trial

The initial source/build audit found no intersections in 3,837 shaped sequences:
all 729 adjacent-letter pairs, single marks, selected stacks and final-letter
combinations at 400, 550 and 700. This is a collision screen, not optical spacing
approval. The closest adjacent-letter bounding-box gap was 32 units. No spacing
or base-letter changes were justified by this screen; running-text rhythm still
needs human judgment.

The marks had identical Regular/Bold outlines. At a normalized 1024 UPM,
Virtua’s Hiriq stayed 74×74 while Rubik grew from about 78×76 to 101×94; Patah
stayed 160×52 while Rubik’s bar grew from about 258×64 to 258×88. Reference
measurements are comparative evidence, not donor geometry or target dimensions.
The browser proof showed the unchanged marks looking light beside Bold.

V1 strengthened all dots to 96 units with symmetric 32-unit axis-tangent handles,
and bars to 64 units. It caused 13 collision cases: Dagesh against Gimel, Zayin,
and Tsadi, and compound vowels inside Final Kaf. This trial is retained in
`candidate-sources/`, `bold-candidate.json` and `after-audit.json` as rejected
clearance evidence, not an approved design.

V2 retains 96-unit standalone dots and 64-unit bars, but uses 80-unit dots with
24-unit handles for Dagesh and the compound vowels. Dagesh’s contour center moves
slightly within the unchanged attachment anchor; the compound-vowel package is
kept compact enough for Final Kaf. Qamats retains its T construction, and Qamats
Qatan retains its splayed stem. There are no new contour/point types. This is a
bounded weight trial; the numerical dimensions are not a new universal style rule.

All edited Bold outline coordinates are on 8. Existing anchors are preserved
exactly, including coordinates not on that lattice. Regular outlines, widths,
anchors, Unicode, review colors, and every other source byte are unchanged.
The 29 marked-letter components follow the edited Bold marks automatically;
no presentation-form GLIF or manual base drawing was rewritten.

## Evidence and verification

- `before-sources/`, `candidate-sources/` and `candidate-v2/` preserve exact pairs.
- `bold-candidate*.json` bind the trials to before/source/candidate hashes.
- `validation.json`: only 16 Bold source files changed; no compiled Regular
  outline changes, no advance changes; all intermediate changes confined to
  the marks and their component dependents at seven weights.
- `after-audit-v2.json`: 3,837 sequences, **zero outline intersections**.
- `contexts.json`: 423 marked presentation-form contexts still match canonical
  decompositions. Reused HEB-009’s `check_contexts.py` with HEB-010 output.
- `hebrew-check.json`: zero coverage/attachment smoke failures.
- `curve-lint.txt`: clean crest/tension and tangent-join audit for all 16 marks.
- Final `make preflight` passed; compatibility has zero blocking mismatches.
- Full offline Fontspector remains **1 FAIL / 28 WARN / 39 INFO / 525 PASS /
  299 SKIP**. The failure is development-directory naming; warnings and skipped
  network checks remain. This is not a Google Fonts readiness claim.

The final preflight rebuild differs from the frozen QA/proof font only in the
`head` modification timestamp and resulting checksum; all other tables match
exactly (`rebuild-equivalence.json`). QA reports retain their actual input hashes.

The live proof is `working-v2/` on port 60272. It retains Before/Working/Rubik/
Noto, the accepted wrapped headings, a complete-codepoint label for combining
sequences, and case-specific Text → Marks and spacing probes. Existing Hebrew
and mixed-text passages remain available. `baseline/` retains the prior current
font. Font hashes and OFL licenses are frozen with both views.

The browser was visually inspected at Bold for the main vowels, running-text
probes, and enlarged Final Kaf with Hataf Segol. The refined compound mark clears
the stem; selected screenshots are saved as `marks-bold-v2.jpg` and
`final-kaf-compound-v2.jpg`. Synthetic stress combinations are diagnostics, not
claims about ordinary Hebrew usage. A native-reader/script review remains open.

## Human grading and Arabic handoff

Eli’s next step is the whole-font grading pass, beginning with this working
Hebrew trial. Use Runebender’s established semantic colors. No agent may infer
or assign approval from the numerical checks above. Keep green/purple drawings
frozen; distinguish red replacements from orange/yellow repairs and blue/pink
composite work. Uncolored drawings require classification rather than silent
permission. Preserve both masters and record any fresh manual correction pairs.

After Eli saves grades, refresh the source hashes and permitted Arabic scope.
Then define a bounded unattended drafting/checkpoint/proof run against that
scope. Arabic has not been modified here; no overnight automation has been
created or started. Completion, native-reader approval and onboarding readiness
remain separate outcomes. Meteg/Rafe and cantillation beyond the selected
modern-Hebrew stress tests are also not silently approved by this pass.
