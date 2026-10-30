# Masked-repair adapter smoke sample

Eli approved the Regular-only pilot and requested adapter plus visual sample
before an overnight run. This original adapter stage performed **zero optimizer steps**.
The subsequently authorized short TRAIN run is now complete; see [results and
limits](PLAN.md#short-run-result-and-next-decision). The page below remains the
original data-only smoke sample. No font
sources are changed. Review: http://127.0.0.1:60272/masked-smoke/index.html

Adapter: `scripts/masked_repair.py`; renderer: `scripts/render_masked_smoke.py`.
Frozen manifest remains arabic-split-v3.json. Only the TRAIN split is loaded.
Three explicit Regular recipes: dotless Beh left bowl, Meem right bowl, final Reh
lower turn. Each names outer and inner point indices bound to the frozen source
hash through the dataset. No validation/test targets or rejected Seen drawings
are used to manufacture positive examples.

Nine examples: unchanged, paired +/-16-unit handle/point perturbation, inverse
perturbation. Whole-glyph input features contain x/y, advance, point type,
contour start and editable mask. Targets contain coordinate residuals only;
no target geometry is fed into input features. Collation provides attention and
loss masks; padding and protected points contribute no repair loss. Reconstruction
rejects nonzero predictions outside the editable mask, invalid dimensions,
nonfinite values, odd coordinates, excessive residuals and coordinate overflow.
It returns an in-memory record, never writes a UFO. Topology/advance are retained.

Representation: v1 numeric features (not the old categorical vocabulary),
2-unit coordinates in [-1024,2048], residuals in [-64,64]. No legacy checkpoint
is compatible by assumption. A future model must produce residuals that pass the
checked reconstruction; any quantization policy for continuous predictions must
be explicit, not hidden in the decoder.

Browser uses a diagnostic CFF/OTF generated from the example contours, with PUA
codepoints, at224px and48px. These are isolated forms, not shaped Arabic text.
Editable mask diagrams are source SVGs. Targets are the exact frozen green
drawings, **not model outputs**. Mode selector was exercised. Baselines were
corrected after a wrapped heading initially displaced the target column. Pinch
and bulge rows were inspected; no-op CFF outline identity checked for all3 pairs.

11 tests pass (7 adapter +4 dataset/tokenizer). Exact residual reconstruction
verified for all9 actual examples. All3135 guarded font-source files unchanged.
See masked-smoke-receipt.json. Generated examples, batch arrays and scratch font
stay in ignored out/. No fonts/model weights copied into durable context.

## Limits to review before the pilot

Masks are manually chosen, not inferred from a bowl detector. Only one magnitude
and axis of perturbation are included. Some handle shifts deliberately break
local tangent behavior; those corruptions teach reversal to the authentic source,
not a universal curve ideal. The optical target is preserved unchanged.
Three independent glyphs do not become nine independent designs. This checks the
adapter's mechanics and sample presentation, not generalization or taste.

The small residual predictor and TRAIN overfit have now been run after sample
review. Further varied corruptions and held-out evaluation remain pending; see
the current PLAN.md rather than repeating this adapter sample. Prepare separate fixed masks
for validation without incorporating its targets into training. Do not begin an
overnight job or apply generated glyphs automatically.
