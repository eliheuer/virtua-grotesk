# ARB-001 — Bold Alef construction loop

Starting point: Eli's grading commit `4318e7a1` (2026-10-21), clean tree.
Eli requested short Arabic feedback loops, roughly one codepoint at a time,
before later authorizing an unattended release-improvement run. No autonomous
all-day run or schedule starts in this case.

## Scope

U+0627 Alef: **Bold `alef-ar` and `alef-ar.fina` only**. Both are red in the
grading commit. Their Regular counterparts are green and remain byte-identical.
Standing Arabic drawing authorization allows installing the bounded trial after
preserving before files. New AI work is purple awaiting human review, following
Eli's requested AI/unreviewed label; that color does not signify approval.

## Diagnosis and proposed construction

- Green Regular Alef: 88-unit stem, y=0..768, 16-unit terminal cuts,
  64-unit isolated sidebearings. Final form has a 96×96 inner turn with equal
  64-unit handles, and a 184×184 outer turn with equal 128-unit handles.
- Red Bold: isolated stem is 168 units but its cuts stretch to 42×8 and
  sidebearings are 28/100. Final cuts are 34×8; its inner handles reverse
  vertically, producing a hook rather than a clean turn.
- Trial: retain the existing 168-unit Bold stem and 176-unit joining bar as
  provisional weight. Restore 16×16 cuts and the Regular's straight/cubic
  construction. Isolated x=64..232 retains advance 296 with equal 64-unit
  sidebearings. Final x=72..240, inner 96×96 turn with 64/64 handles;
  outer 264×264 turn with 176/176 handles. Final advance becomes 336 to
  accommodate that turn, keeping the baseline and joining edge continuous.
- Place top anchors on the 8-grid near the new stem centers (isolated 152,
  final 160); inspect marked text. Preserve mark glyphs and feature rules.

This reuses construction relationships from the current approved Regular,
not an automatic stroke offset or external font outlines. The old Arabic
contract/grammar files are historical; their 96-unit Regular stem and green
counts do not describe today's graded drawings. Rubik is a structural reference.
The 168/176 weight and new final width are trial choices, not confirmed global
Arabic rules. Dependent Bold composites will inherit the base geometry and
must be included in compiled scope/mark checks.

## Arabic proof accommodations and references

Eli requested script-specific proofing on 2026-10-21: retain Rubik, replace Noto
Sans Hebrew with Noto Sans Arabic, and prefer portable OFL references.
The live proof now sets `lang=ar`, includes isolated/final Alef, joining contexts,
combining marks, Arabic running text, and mixed Latin/Arabic/numeral text.
Its local reference fonts and OFL licenses are in `assets/`; `evidence.json`
records hashes and axis ranges. Noto uses default width 100. No outlines were
copied from either reference. Shared em size and native shaping are retained.

Optional reference shortlist (not added as extra columns):
- [Tajawal](https://github.com/googlefonts/tajawal): OFL low-contrast Arabic;
  its geometric direction is a useful comparison for the intended construction.
- [Readex Pro](https://github.com/ThomasJockin/readexpro): OFL Arabic/Latin family;
  another useful sans comparison. Neither defines Virtua's drawing rules.

## Verification and remaining review

- `make preflight`: completed, including build, PDF proof and source reports.
- `diff3proof` produced `out/review/diff3proof.html` from that built variable font.
- `curve-lint.txt`: smooth turns have zero tangent-angle error; right-edge
  joining corners are intentional. `grid.json`: zero findings in the two targets.
- `verify.py` / `verification.json`: only the two named Bold source files differ;
  204 shaping runs across Before/Working/Rubik/Noto, 17 probes, weights
  400/550/700, no missing glyphs, unchanged Before/Working glyph sequences.
- Compiled geometry changes are confined to Alef and its dependent composites.
  Regular source bytes, compiled bounds and advances are unchanged, but joint
  cubic-to-quadratic conversion changes the Regular final-Alef approximation and
  dependent outlines. Do not describe the compiled Regular as byte-identical.
- Browser inspection: isolated/final Alef, combining marks, and running Arabic
  render at Bold beside both Arabic references. Saved `marks-bold.jpg` and
  `text-bold.jpg`; the latter records the viewed Text layout. Human drawing
  approval is pending; this is not Arabic release QA.
- Next issue: derived Alef forms still have legacy component positions/advances
  (e.g. isolated hamza/madda composites use advance 224 against Alef's 296).
  Inherited changes are visible; reconcile these in the next small loop.
  Weight and width choices here remain proposals, not reusable confirmed rules.

## Four-reference selection — 2026-10-21

Eli selected **IBM Plex Sans Arabic and Readex Pro** as additions to Rubik and
Noto Sans Arabic. The proof now renders six panels including Before and Working.
Snapshots and OFL licenses are bundled in `assets/`, with exact hashes in
`evidence.json` and the generated `working/live-fonts.json`.

Plex uses its genuine static 400, 500, 600 and 700 faces with native CSS weight
matching at intermediate slider positions; it is not interpolated. Readex uses
its variable weight axis with HEXP at default 0. Font synthesis is disabled.
The generic proof loader verifies every face, and coverage uses the intersection
of all faces in a static family so unsupported text cannot silently fall back.

With more than four panels, widths below 1440px use two columns, keeping the
Before/Working pair together. Text uses one column below 600px. Wide comparisons
use all six columns. Existing four-font Hebrew layouts retain their behavior.
Browser inspection covered Regular/Bold and the wide/narrow layouts. The saved
`four-references-bold.jpg` shows all six panels in the restored narrow layout.
`reference-verification.json` records 63 successful shaping/coverage probes for
the new faces. No glyph source files changed in this reference-selection step.
