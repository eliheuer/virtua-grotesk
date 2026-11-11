# arabic-repair-hour-v1

Status: experimental. It does not pass its held-out test. Do not use it to
change real glyphs.

| Item | Value |
| --- | --- |
| Task | Move the masked points of one Regular Arabic glyph toward the font's construction. The topology stays the same. Output is on the 2-unit grid. |
| Size | 36,578 parameters, 151,285 bytes (`checkpoint.pt`, SHA-256 in `manifest.json`) |
| Runtime | CPU, PyTorch 2.6 or later (tested with 2.13.0). `propose_arabic_repair.py` |
| Training data | 36 green Regular Arabic drawings in 10 construction families, with synthetic point displacements and clean copies. |
| Training | 1,285,746 steps in one hour, 2026-10-30. `train_variable_pilot.py` |
| Held out | The Hah family (validation; inspected repeatedly during development). |

## Results

| Test | Cases | Result |
| --- | ---: | --- |
| Clean training drawings left unchanged | 36 | 36 |
| Clean held-out Hah drawings left unchanged | 3 | 0 (all three changed) |
| Displaced held-out Hah drawings | 21 | 9 improved, 12 worse |
| New displacements of training drawings | 18 | 18 improved |

The model reproduces the families it has seen and does not generalize to an
unseen family. A useful model must first leave clean held-out drawings
unchanged.

## Files

- `checkpoint.pt`: the weights. The runner checks the hash before loading.
- `manifest.json`: hashes and the full evaluation numbers.
- `sample.json`: one clean held-out initial Hah with a point mask.
- `expected-sample.json`: the model output for `sample.json`, to check that a
  new machine gives the same result. The output contains unwanted changes; do
  not use it as a training target.

Usage is in [documentation/native-model-workflow.md](../../documentation/native-model-workflow.md).
The training records of this run are in the Git history, in the folder
`models/training/seen-pilot/`, removed on 2026-11-10.
