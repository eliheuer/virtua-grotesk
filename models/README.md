# Models

Small models trained on this font for narrow tasks. Cloud models do general
work; a model here does one task that the font's own drawings can teach.

Each model has one directory with these files only:

- `README.md`: the model card: status, task, size, runtime, training data,
  held-out test and results.
- the checkpoint, at most 5 MB. A larger checkpoint goes to a GitHub release
  or Hugging Face, with its SHA-256 and link in the model card.
- small JSON files that the runner needs, for example a manifest or a sample.
- the Python files that run and train the model.

Training logs, receipts and data snapshots
go to `out/`, which Git ignores. Train only on green glyphs, and keep a held
out family that the model never sees in training.

| Model | Task | Status |
| --- | --- | --- |
| [arabic-repair-hour-v1](arabic-repair-hour-v1/README.md) | Repair masked points of a Regular Arabic glyph | Experimental; fails its held-out test |
