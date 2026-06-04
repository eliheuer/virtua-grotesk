# DrawBot Runtime Readiness

This generated report records the proof-generation runtime. Virtua Grotesk proofs intentionally use Eli Heuer's local `drawbot-skia` fork instead of a generic DrawBot runtime.

## Summary

- Local drawbot-skia checkout exists: yes
- Expected fork origin owner/repo: `eliheuer/drawbot-skia`
- Actual origin: `git@github.com:eliheuer/drawbot-skia.git`
- Origin is Eli Heuer fork: yes
- Accepted origin URL forms: `git@github.com:eliheuer/drawbot-skia.git`, `https://github.com/eliheuer/drawbot-skia`, `https://github.com/eliheuer/drawbot-skia.git`
- Expected upstream: `https://github.com/justvanrossum/drawbot-skia.git`
- Actual upstream: `https://github.com/justvanrossum/drawbot-skia.git`
- Upstream is canonical drawbot-skia: yes
- Local drawbot-skia branch: `master`
- Local drawbot-skia HEAD: `ac56b2a`
- Local drawbot-skia worktree clean: yes
- Project venv Python exists: yes
- Project venv Python: `/Users/eli/GH/repos/virtua-grotesk/venv/bin/python`
- drawbot-skia src exists: yes
- Drawing API importable: yes
- Import status: `import ok with fork src on PYTHONPATH`

## Repository Wiring

- Makefile sets `DRAWBOT_SKIA_REPO`: yes
- Makefile uses project venv Python for DrawBot proofs: yes
- Makefile prepends fork `src` to `PYTHONPATH`: yes
- `proof.py` supports `drawbot_skia.drawing.Drawing`: yes
- `proof.py` requires eliheuer/drawbot-skia instead of generic DrawBot: yes
- README documents the fork runtime: yes
- Python tooling notes document the fork runtime: yes

## Apply Before Proof Review

- Keep `/Users/eli/GH/repos/drawbot-skia` synced with the intended
  `eliheuer/drawbot-skia` fork state before regenerating final proofs.
- Regenerate this report with `make preflight` after changing the
  DrawBot runtime, proof script, or local drawbot-skia checkout.
- Use `make proof-only` after a successful font build to regenerate
  `proof.pdf` for final visual review.

References:

- https://github.com/eliheuer/drawbot-skia
- https://github.com/justvanrossum/drawbot-skia
