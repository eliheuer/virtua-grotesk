# Local model test — 2026-10-29

Requested: test existing local models on rejected Seen, scratch only; no training
or source application. Outcome: no usable repair in this bounded experiment.

## Evidence and limitations

Installed sketch checkpoint `virtua-12m-sketch` (clean1) and bolden checkpoint
`virtua-12m-bolden` (v09-f2); exact weights/config/vocab hashes in receipt.json.
Rejected revisions4/6 in Regular/Bold supplied directly as vector sequences,
bypassing tracing. Sketch ran greedy identity and faithful modes, eight outputs
per condition. Bolden ran two Regular inputs as weight-transfer tasks, not
same-weight cleanup. One additional Regular H identity control: 21 outputs total.
No sample sweep, learned critic, held-out accuracy or release claim.

Native Seen test is confounded: tokenizer clamps coordinates to [-512,1280].
Regular has 9 changed coordinates (up to128 units), Bold5 (up to96); advances
1504/1440 clamp to1280. Native outputs must not establish model quality.
Scaled repeat uniformly scales input0.75, quantizes to2-unit vocabulary, then
restores output scale. This avoids range clipping but changes conditioning
size/stroke weight and is not equivalent to a correctly supported native input.
`seen-ar` name token absent; U0633 token present. Identity uses UNK+U0633;
faithful uses UNK+no Unicode. Existing Python inference implementation reused.
MLX initialization needed access outside sandbox even with CPU selected.

Viewed every output as shared-em SVG outlines in actual browser, not compiled
text. Native sketch produces S-like replacements/spikes; scaled sketch produces
collapsed, disconnected, overlapping blocks and loses Seen identity. Scaled
input/output ink IoU0.127–0.224 is a fidelity diagnostic, not a beauty score.
Bolden retains more structure but does not repair the rejected transition;
scaled v6 also has visibly uneven bowl thickness. H control remains recognizable
but introduces a diagonal inner crossbar transition (IoU0.797). The pipeline can
produce a recognizable simple letter, but this is not a validated golden control.
No generated master pair is approved or claimed interpolation-compatible.

Local comparison: http://127.0.0.1:60272/seen-model-test.html
Generated GLIFs/UFOs, logs and screenshot: ignored `out/seen-model-test/`.
Recipes and compact receipts retained here; no model weights/font copies added
to the design library. Script outputs use the older helper's color initially;
final standalone scratch sketch GLIFs relabeled purple, hashes updated.
All3135 source files match the pre-test hash snapshot. No retraining/application.

## Proposed training plan — not started or scheduled

1. Fix input contract first: no silent clipping; test coordinate range, advance,
   contour order, identity aliases and codec round trips on all selected data.
   Reproduce a known successful checkpoint example before diagnosing model capacity.
2. Freeze green-only targets per master and recursive component dependencies;
   reject color conflicts. Separate related construction families and shared
   donors before any interpolation, corruptions or augmentation. Save hashes and
   split manifests. Existing general Regular sampling is not green-only, and
   pair exclusion alone does not stop interpolation leakage.
3. First experiment: bounded local repair using an editable-region mask and
   coordinate deltas. Lock teeth, chamfers, metrics and unaffected segments;
   expose both bowl boundaries and counter shape together. Unchanged green
   examples must teach identity/no-op. Include whole glyph context, not just a
   cropped bowl. Keep optical exceptions from real source geometry.
4. Use Eli-approved correction pairs as real supervision. Synthetic pinches,
   bulges and weight errors can supplement, but cannot define taste. Rejected
   Seen is a test input, not a positive target; we do not yet have an approved
   isolated Seen repair target. Collect that rather than appointing another
   agent output as ground truth. Inventory independent examples before deciding
   model size or claiming an overnight run has enough data.
5. Initially retain deterministic structural checks and reference retrieval.
   Train a separate preference/ranking model only if enough independent human
   comparisons exist. A generator likelihood or current heuristic score is not
   a design critic. Critic and generator need independent evaluation; neither
   can assign green or apply output.
6. Start with a small pilot against unchanged-input and donor-based baselines.
   Evaluate held-out Arabic families at reading/detail sizes, preservation,
   shaping/compatibility, and human correction effort. Stop on construction
   damage. Only expand overnight after a reviewable pilot improves on baseline.

Tonight's decision is pilot scope/data readiness first, not a promise that a
new model or ensemble will solve this after one run. No timed run is enabled.
