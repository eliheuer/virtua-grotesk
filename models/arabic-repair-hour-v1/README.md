# Experimental Regular Arabic repair model

151,285-byte PyTorch checkpoint; 36,578 parameters. Ordinary Git is sufficient.
This is a local proposal helper, not a general drawing model or an approved
cleanup tool. It predicts bounded coordinate residuals for explicitly masked
points, preserves topology, and quantizes output to2 units. It cannot add contours,
repair topology, generate arbitrary glyphs, or infer Bold drawings. The2-unit
quantization preserves the experiment's optical-resolution protocol; it does not
replace the font's8-unit machine-draft construction rules.

Training:36 green Regular Arabic drawings in10 families, synthetic perturbations
and clean controls;1,285,746 steps in one hour. Hah was excluded from training but
repeatedly inspected as a development holdout; it is not a fresh blind benchmark.
Seen test data was not used in this run. See manifest.json and the maintained
[training plan](../../design/training/seen-pilot/PLAN.md).

Final results:36/36 clean TRAIN drawings preserved;0/3 clean Hah drawings
preserved;9/21 corrupted Hah examples improved and12 worsened versus unchanged
input. All24 Hah cases scored better than the earlier100k model, which does not
make them good drawings. Human visual review is required. No automatic acceptance.

checkpoint.pt is the exact final checkpoint, hash-checked by the runner and loaded
with weights_only=True on CPU. sample.json is one clean held-out initial Hah with
an explicit mask; expected-sample.json records its actual output, including its
undesired changes. Do not turn that output into a positive training target.
These small sample records are retained for reproducibility; bulk training runs,
logs, snapshots and generated UFOs stay under ignored out/.

See [native interactive workflow](../../documentation/native-model-workflow.md).
