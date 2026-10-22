# LAT-001 batch11 · Alternate carons and uppercase Ť

Applied pending human review:12 GLIFs and2 Latin feature files, with all1765
other source files unchanged. All base letter drawings, Arabic recursive donors,
green sources, saved human corrections and wrapper grades remain unchanged.
The two newly drawn caroncomb.alt donors are purple. No kerning was changed.

## Visible defects and repair

The shared alternate caron was a tall, identical-weight six-point mark. In ď and
ľ it fell inside the stem; in ť it crossed the top bar. Ľ was unnecessarily tall.
Uppercase Ť incorrectly used this apostrophe form instead of an ordinary caron.
The Before/Working/Rubik whole-letter proofs show these construction problems.

- Both alternate donors now use eight-point convex outlines,64/96-unit nominal
  horizontal weights,160-unit height (y608..768), parallel diagonal sides and
  16-unit cuts. This follows the small clipped-mark construction used for the
  comma accent; neither Rubik nor another font supplies source outlines.
- Local components in Ľ ď ľ ť move beside the upper stems. Minimum measured
  upper-stem clearance is32 at all five sampled weights. Ľ has44/48; the other
  forms have32 except Regular ť40. The mark's y608 bottom clears t's y576 bar by32.
- Uppercase Ť now inherits existing caron at yOffset192. Its horizontal offsets
  are128/112; its widths match the unmodified T bases680/648. Ordinary caron
  donors and Dcaron comparison sources remain untouched.
- The top anchor of ť is explicitly y768 in each master, clearing the taller
  side mark when another accent follows. Other propagated anchors remain intact.
- Five canonical ccmp compositions per master preserve these constructions when
  a web subset omits ĽďľŤť cmap entries. Basic fallback and full-font NFC/NFD agree.

The whole silhouettes, reading words, adjacent-letter pairs, repeated forms and
above-mark stacks were inspected at400/550/700, plus224px/em endpoint details.
These are constructed proofs, not evidence of native Czech/Slovak reader approval.
Regular marks are smaller/lighter than Rubik; Bold letter-to-mark balance and
conservative spacing await Eli's optical review. The ordinary caron's inherited
Regular pointed apex/shape is unchanged and not newly approved.

## Spacing and grid

New wrapper advances are on8: Ľ608/640, ď728/840, ľ328/440, Ť680/648, ť376/488.
ď/ľ/ť reserve32 units after their rightmost mark. This prevents collisions in
repeated/tall-letter contexts; tighter optical pairs may need a later kerning
pass, especially before lowercase bowls. `spacing-measurements.json` records
endpoint advances/bearings and descriptive popcounts for Before/Working/Rubik.
Do not infer language quality from matching reference widths.

Every new point, component offset, width and explicit anchor is on8. The expanded
closure grid check retains100 findings in inherited base/caron geometry, anchor
values, donor advance260 and resulting bearings; no green sources were snapped.
The two alternate donors have no cubics. Five interpolation samples remain convex
with positive winding; curve lint has no crest/tension/kink flags. No claim of
curve improvement applies to the unchanged base letters.

## Verification and evidence

Fresh pre-application dependency closure is6 glyphs/master with no green/Arabic
intersection;326 Arabic recursive reservations/master. Tcaron leaves the alternate
donor's consumer closure after the component correction, but remains in this
batch's expected compiled-ink changes.

135 scoped shaping/ink comparisons pass at400/475/550/625/700, including exact
non-target glyph ink preservation, full master compatibility, Arabic/Hebrew
contexts, basic missing-cmap fallback and additional above-mark clearance.
Seven Latin test methods pass across VF/four statics. Frozen engineering baseline
reproduces the same216 existing Hebrew failures, zero new failures. Existing
ogonek-plus-acute subset normalization failures from batch10 remain unresolved.
Build/preflight completed; all five active fonts match scratch tables except
head timestamps/checksum adjustment. No Fontspector rerun or release approval.

Raw DesignBot renders ran sequentially. Its NFD attachment row is not authoritative
for canonical recomposition; independent FreeType/RAQM `compiled-attachment-*`
shows both text encodings with the correct forms. Whole compiled stacking rows
are retained separately. The224px proof uses the existing280-unit panel baseline
so the tall Dcaron/Ť accent is not cropped; the first264-unit-baseline render was
rejected by the panel-overflow assertion, before any visual acceptance.

Exact before/candidate sources, all-source hashes, candidate/baseline fonts,
guarded application, scoped checks, preserved failure records and inspected-image
hashes are retained here. No push, publication, Runebender change or Arabic live
proof change. Next: independent precomposed/base spacing discrepancies, then
remaining coverage and technical release blockers.
