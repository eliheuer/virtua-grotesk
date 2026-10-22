# LAT-001 batch10 · Ogonek hooks and local attachment

Applied as a pending human-review draft. Eighteen GLIFs and two Latin feature
files; no base letter, Arabic source/donor, green source, advance or kerning edit.
The two new donor drawings are purple. Fourteen local component placements keep
the wrappers' human grades; the combining wrappers retain their grades too.

## Drawing and whole-image decisions

The original ogonek was the same nine-point polygon at both weights, with a
pointed/slanted inner landing and weak Bold weight. Both donors now have a
20-point, four-cubic hook, diagonal neck landings, axis tangencies, 16-unit cuts
and 48/64-unit cardinal bowl weight. Incoming anchor120,0 and advance260 stay.
Bounds are64..224/-208..0 Regular and48..224/-224..0 Bold. Outgoing bottom anchors
in donor/combining wrapper move to-240/-256, 32 units below the hook.

The first donor-only whole-letter proof was rejected: **Ą was visibly detached
under the center of A**, and several end-stem hooks used generic centered
placement. `trial-donor-only/` retains that image/curve evidence. Local ogonek
components in Aogonek, Eogonek, aogonek, uogonek, Iogonek, iogonek and
 dotlessiogonek now attach at the right foot/stem. Both masters are covered;
new offsets are on8. The bowl-attached eogonek/Uogonek placements stay as saved.
Base geometry and human grades are byte-identical. No inherited green geometry
was altered to fix attachment.

Whole DesignBot word/attachment images at400/550/700, 224px/em endpoint letters,
and independent FreeType/RAQM attachment and stack images at all three weights
were inspected. All these characters exist in the pinned Rubik file. The hook
is deliberately lighter and more open than Rubik; its neck, projection and
weight remain for Eli's optical review. There is no native-reader approval.

## Shaping and renderer limits

Eight canonical ogonek compositions were added to the existing Latin ccmp lookup
in each master, retaining the same local placement when a web subset omits an
ogonek cmap entry. Full-font composed/decomposed shapes match, including an acute
or another ogonek; basic missing-cmap and repeated-ogonek fallback match too.
The six Latin test methods cover the VF and four statics.

DesignBot's decomposed second attachment row still uses generic mark placement,
despite the compiled ccmp rules. HarfBuzz inspection and the separately rendered
`compiled-attachment-400/550/700.png` show matching composed/decomposed rows. Keep
this renderer discrepancy visible; do not judge canonical output from that
DesignBot second row alone. `compiled-canonical-550.png` is an additional direct
comparison. The retained images were rendered sequentially.

**Separate unresolved subset case:** after removing the ogonek cmap entry and
adding an acute, normalization chooses an acute-precomposed base plus generic
ogonek before GSUB. `subset-accent-followup.json` records the same40 affected VF
samples before and after (8 letters ×5 weights). The expanded test first exposed
72 failures across VF/statics. Its basic-fallback assertions are scoped explicitly;
this broader above-accent/subset normalization issue is not reported as passing.
Keep it with the serving-subset release work, not a reason to alter green anchors.

## Verification and exact limits

- Fresh consumer closure:11 glyphs/master, no green/Arabic intersection;326
  Arabic recursive reservations/master. All1759 non-target source files unchanged.
- 100 scoped shaping/ink comparisons at400/475/550/625/700; all masters compatible,
  only the expected eleven compiled glyphs change ink. Arabic/Hebrew preservation
  samples retain exact glyph positions/ink. No width or kerning changes.
- Six Latin tests pass within their stated scope. Existing engineering baseline
  reproduces exactly216 Hebrew failures, zero new failures. The separate40-sample
  subset-acute finding above remains outside that historical engineering suite.
- Five-weight signed profiles and sampled intersections checked. The trial's
  62.5% inner join jump was reduced to G2 by changing inner lower-turn handles.
  Outer left joins retain18.4% Regular/33.3% Bold curvature jumps; four tangent
  line landings are G1line. No sampled reversal/intersection. These scores are
  not approval of proportions or curve quality.
- Every new point, outgoing anchor y and component offset is on8. The expanded
  closure grid report has219 inherited findings in base drawings, saved anchors,
  advances/sidebearings and unchanged Uogonek offsets; eight are repeated donor
  advance260/right-bearing36 findings. No green geometry was snapped.
- Deep b+two-ogonek reaches-480, inside unchanged Windows descent576. All fontinfo
  and other metadata are untouched. Active build/preflight completed; all five
  active fonts match scratch tables except head timestamps/checksum adjustment.

`baseline.json`, exact before/candidate sources, `changes.json`, hash-guarded
`apply.py`, final font/image hashes and validation receipts are retained. These
recipes deliberately refuse changed source baselines. No push, publication,
Fontspector rerun or change to the Arabic live proof occurred.

Next: alternate carons; then independent spacing/coverage and serving-subset work.
