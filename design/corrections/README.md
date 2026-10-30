# Correction library

`records/*.json` are the canonical correction records. They are discovered by
`scripts/design_context.py` without a second handwritten index. Raw drawing/proof evidence lives
with its original review under `design/reviews/`; keeping it there preserves exact
pairs, receipts and relative paths. A correction is indexed here once, then linked
from construction rules and glyph contracts.

```sh
.venv/bin/python scripts/design_context.py --list
.venv/bin/python scripts/design_context.py --glyph zayin-hb --operation weight-transfer
```

## Record a correction

Capture Eli's feedback before the next revision. Preserve his exact words where
available; mark a paraphrase as a paraphrase. Separate observation, interpretation,
proposed generalization, application and visual verdict. Identify glyphs, masters,
source revision and hashes. Save before/after GLIFs, comparison measurements and
viewed proof images in the case. Never overwrite a rejected draft to make it look
accepted. Keep licensing/provenance beside supplied reference assets.

Copy an existing scoped record such as [Zayin Bold](records/zayin-bold-02.json).
Use a stable unique id and these fields:

| Field | Meaning |
| --- | --- |
| schema_version, id, kind, title | Version 1; kind correction; stable identity |
| glyphs, masters, scripts, operations, tags | Exact applicability; patterns only for genuinely shared lessons |
| status, summary, limits | Evidence state, reusable lesson, boundaries |
| human_feedback, interpretation | Human statement versus agent inference |
| application, visual_verdict | Where the drawing is applied versus whether it was accepted |
| training_eligibility | not-approved, negative-example, requires-curation, approved-pair |
| evidence | Repository-relative path, role and SHA-256 for each retained artifact |
| pairs | before/after evidence paths and master for each exact delta |
| related | Record ids of necessary examples and counterexamples |
| approval_evidence | Required for an approved training pair; must name an evidence path with a hash and actual explicit approval |

`make design-check` checks paths, hashes, related ids, pair evidence and verdict
consistency. A positive pair still needs human curation; this is not a training
exporter. Color or a successful build does not establish approval. Unknown history
remains not-approved. Exclude metadata/serialization-only changes when deriving
geometry deltas. Split related glyph families before interpolation or augmentation.

Historical anchor-sheet lessons were indexed individually under `history/` with
scopes and evidence hashes. Their dated operational instructions are superseded by
current system rules. The old all-in-one log is retained for provenance, not loaded
wholesale. Consult [learning boundaries](../system/learning.md).

Feedback cited from a mutable case README is frozen byte for byte as a .txt
snapshot under evidence/; source_path retains its original location. Later case
updates must not rewrite that snapshot or silently update its evidence hash.
Historical links inside frozen text are relative to source_path, not the snapshot
folder. New feedback gets a new record/snapshot or an explicitly versioned revision.
