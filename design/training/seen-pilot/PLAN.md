# Regular Arabic repair pilot — review before further training

Updated 2026-10-30. **The variable-length short pilot is complete and fails clean
preservation. Do not start an overnight run of this setup. Active sources and
built fonts remain unchanged.**

[Current visual proof](http://127.0.0.1:60272/variable-pilot/index.html) ·
[Variable pilot receipt](variable-pilot-receipt.json).
Earlier evidence: [adapter smoke](masked-smoke-receipt.json),
[TRAIN memorization](regular-pilot-receipt.json),
[fixed-size evaluation](evaluation-receipt.json).

## Latest result

The new shared-point model handles variable contour lengths without truncation,
including the44/50-point Hah forms the old model could not process. It uses local
cyclic neighbors, spatial neighbors and whole-glyph context with fixed coordinate
normalization. It has36,578 parameters and predicts bounded masked residuals.
No target geometry or glyph labels enter inference features. Original green
optical coordinates remain targets; they are not geometrically regularized.

One CPU run:1800 steps, batch24, AdamW lr0.001; training loop4.82 seconds excluding
preparation/rendering. Final checkpoint only; no validation-based selection.
2013 TRAIN examples from33 green Regular drawings in9 families include single
handle, cluster, paired-x/y, jitter and matching-mask clean controls. Roughly half
are clean; clean loss has weight2. Straight-only drawings receive identity
controls, not invented curve corruption. Spatial pairing is synthetic and is not
semantic identification of corresponding stroke boundaries.

| Evaluation cohort | Cases | Exact | Improved | Worse | Tied |
|---|---:|---:|---:|---:|---:|
| Familiar fixed probes (includes clean) |21|0|6|13|2|
| Newly sampled corruptions |18|0|9|8|1|
| Hah probes (includes clean) |21|0|0|20|1|
| Wide clean controls, TRAIN |33|0|0|33|0|
| Wide clean controls, Hah |3|0|0|3|0|

**None of36 wide clean controls remained exact.** Maximum unwanted displacement
per TRAIN drawing is2–8 units; Hah final/initial/medial maxima are16/24/16 units.
Some differences are visually subtle, but they fail the requested preservation
check. No evaluation output matches its green target exactly after2-unit rounding
or in compiled scratch CFF outlines/advance. This is not evidence that training
longer is sufficient, nor proof that this architecture cannot learn.

Six browser panels were inspected at224px and48px: all three clean Hah forms,
clean Meem, and Meem new draws1(worse) and4(improved, still inexact). Full final
Hah descenders are visible. Other cases have numerical/compiled checks but no
individual visual-review claim. These are isolated diagnostic forms, not shaping
or font-release QA. The proof displays actual predictions, with no hidden
confidence threshold, fallback or substitution of targets.

All3140 source/font files and their path set remain exact. Four variable-model
safety tests and seven existing adapter tests pass. Padding independence, target
exclusion, locked outputs, overflow refusal and optical-target round trips are
covered. Hard masking is an enforced constraint, not learned behavior; points
inside clean-control masks are intentionally editable. Large datasets, models,
diagnostic fonts and screenshots stay in ignored out/. See the receipt for hashes.

## Next decision — not started

Review this failure before another run. A useful next experiment must test an
explicit edit/no-edit or abstention mechanism against unchanged-input controls,
without hiding regressions behind a post-hoc threshold. Define the criterion on
TRAIN/development data before evaluating a fresh family. A donor/retrieval baseline
remains outstanding. Preserve optical variation and both stroke boundaries; clean
reconstruction alone is not a learned aesthetic critic.

Eli's manual cleanup would help: prioritize3–5 independent Regular construction
families with different bowls, joins or tails, rather than more dotted variants of
one body. Preserve exact before and human-corrected after files and brief intent.
Human corrections provide evidence synthetic perturbations cannot. More green
codepoints alone will not solve unwanted edits. Freeze a new reviewed snapshot
before using additions; keep Hah/Seen family exclusions. A separate fresh family
is still required for blind acceptance. No additional training is authorized by
this plan, and no overnight scheduler is enabled.

## Frozen dataset and split

Current snapshot: `out/training-prep/green-arabic-v3/manifest.json`.
Exact manifest hash, policy and Arabic selections: [arabic-split-v3.json](arabic-split-v3.json).
The earlier selection.json is historical v1, not tonight's input.

| Supervision | Train | Validation | Test |
|---|---:|---:|---:|
| Arabic Regular bodies | 33 | 3 | 2 |
| All eligible Regular | 106 | 7 | 6 |
| All eligible Bold | 65 | 4 | 4 |
| Two-green-master compatible pairs | 62 | 4 | 4 |

192 direct outlines total; 70 compatible pairs. **No green Bold Arabic body
examples qualify.** First Arabic repair pilot is Regular-only. The other Bold
examples are retained for future weight-transfer work, not mislabeled as Arabic
repair supervision. Five precision-sensitive green examples stay excluded and
unchanged. No rejected, purple or uncertain-grade drawings become positive targets.

Arabic validation is Hah/Jeem/Khah (three green Hah forms). Arabic test is
Seen/Sheen (two green joining Seen forms). All contextual variants and associated
body donors stay in their family group across masters, including rejected or
non-green variants. Remaining Arabic families train. Marks/dots are explicitly
**reference-only**, excluded from body targets. Shared mark edges no longer join
unrelated letter bodies into one giant split group. Body dependency edges,
canonical variants, exact outline duplicates and declared construction-family
links remain grouped. This is an explicit body-repair evaluation protocol, not a
claim that a model never sees a generic dot used by a held-out letter.

We have already inspected rejected Seen, so this is a transparent development
holdout, not an untouched final benchmark. Do not tune repeatedly against it and
claim unseen accuracy. A fresh human-chosen family is needed for a final blind
acceptance test after the pilot. No approved isolated Seen target exists yet.

## Data consumption safeguards

`scripts/prepare_green_dataset.py` makes a new, immutable-by-convention snapshot
and refuses overwrites. `scripts/frozen_green_dataset.py` reads only frozen bytes,
requires the reviewed manifest hash, checks every glyph hash, unique examples,
group separation and green/direct-outline eligibility, and never falls back to
live UFOs. Changed snapshots fail. Generated data stays in ignored out/; the repo
keeps small selection receipts and recipes rather than duplicate fonts/models.

Example inspection (prints data; does not train):

```
.venv/bin/python scripts/frozen_green_dataset.py out/training-prep/green-arabic-v3 \
  --manifest-sha256 a4135c690ecb830987fa6dd873a4e645508da71e20abe74eeb8f2397d9c76e19 \
  --split train
```

The existing live-source lab Corpus must not be used. Synthetic variants inherit
their original family split and do not count as independent drawings.

## Runtime and tokenizer status

Python and Rust encoders refuse unsupported coordinates/advances/deltas rather
than clipping them; legacy valid IDs are unchanged. Rust inference/training callers
propagate errors. The checked Rust binary is
`/Users/eli/GH/repos/font-ml/target/release/font-ml`; its hash and CLI evidence are
in [rust-runtime.json](rust-runtime.json). The installed `~/.cargo/bin/font-ml`
was not replaced and retains the old behavior. External editor clients have not
been rebuilt against the Result-returning API. Prior77 Rust unit/3 integration
passes are historical evidence, not rerun by this pilot.

Pilot scripts: `scripts/variable_repair.py`, `scripts/train_variable_pilot.py`,
`scripts/render_masked_pilot.py`. Torch runtime:
`/Users/eli/GH/repos/font-garden-lab/.venv/bin/python`.
Run artifacts: `out/training-prep/variable-pilot-v1`.
The previous fixed-size model and its failed held-out evaluation remain available;
the new pilot does not overwrite their checkpoints. No commit or push performed.
