# DrawBot Runtime Readiness

This generated report records the proof-generation runtime. Virtua Grotesk proofs use `drawbot-skia`. A local fork checkout can be supplied with `DRAWBOT_SKIA_REPO`, but shared repo files must not hardcode machine-specific paths.

## Summary

- DRAWBOT_SKIA_REPO configured: no
- Local drawbot-skia checkout exists: no
- Expected fork origin owner/repo: `eliheuer/drawbot-skia`
- Actual origin: `missing`
- Origin is Eli Heuer fork: no
- Accepted origin URL forms: `git@github.com:eliheuer/drawbot-skia.git`, `https://github.com/eliheuer/drawbot-skia`, `https://github.com/eliheuer/drawbot-skia.git`
- Expected upstream: `https://github.com/justvanrossum/drawbot-skia.git`
- Actual upstream: `missing`
- Upstream is canonical drawbot-skia: no
- Local drawbot-skia branch: `missing`
- Local drawbot-skia HEAD: `missing`
- Local drawbot-skia worktree clean: yes
- Project .venv Python exists: yes
- Project .venv Python: `.venv/bin/python`
- drawbot-skia src exists: no
- Drawing API importable: no
- Import status: `Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from drawbot_skia.drawing import Drawing; db = Drawing(); assert hasattr(db, 'saveImage')
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'drawbot_skia'`

## Repository Wiring

- Makefile keeps `DRAWBOT_SKIA_REPO` portable: yes
- Makefile uses project .venv Python for DrawBot proofs: yes
- Makefile supports optional fork `src` on `PYTHONPATH`: yes
- `scripts/build_general_proof.py` supports `drawbot_skia.drawing.Drawing`: yes
- `scripts/build_general_proof.py` requires eliheuer/drawbot-skia instead of generic DrawBot: yes
- README documents the fork runtime: yes
- Python tooling notes document the fork runtime: no

## Apply Before Proof Review

- Set `DRAWBOT_SKIA_REPO=/path/to/drawbot-skia` when you want to run
  proofs from a local fork checkout.
- Regenerate this report with `make preflight` after changing the
  DrawBot runtime, proof script, or local drawbot-skia checkout.
- Use `make proof` after a successful font build to regenerate
  `documentation/proofs/proof.pdf` for final visual review.

References:

- https://github.com/eliheuer/drawbot-skia
- https://github.com/justvanrossum/drawbot-skia
