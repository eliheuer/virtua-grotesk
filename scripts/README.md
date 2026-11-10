# Script index

Run scripts from the repository root with `.venv/bin/python`, unless they are
shell entrypoints. `make help` lists the maintained command interface.

## Build and validation

- `build.sh`: the release build (`make build`). `build-fontc.sh`: the fontc build (`make build-fontc`).
- `proof-web/`: the live comparison proof (`make proof-web`). See [proof-web/README.md](proof-web/README.md).
- `fix_gf_metadata.py`: postprocesses compiled fonts; called by both build scripts.
- `check_gf_fonts.sh`: development, full-font, and downstream-package QA.
- `run_reports.py` and `report_*.py`: source, compatibility, and binary reports.
- `preflight.py`: checks required local artifact paths.
- `glif_lint.py`, `grid_lint.py`, `curve_lint.py`, `curve_continuity.py`:
  outline checks; inspect each CLI before choosing a scope.
- `grid_qa.py`, `scoreboard.py`, `normalize_metrics.py`: design measurements
  and review summaries. Generated scores do not approve glyphs.
- `audit_diacritics.py`, `latin_diacritics_audit.py`, `compare_diacritics.py`,
  `shape_sheet.py`, `qa_loop.py`: focused diacritic and shaping review.

## Design harness

- `check_design.py`: checks glyphs against the stroke targets in
  `documentation/design/system/contract.json`, checks composites against their
  parts and anchor recipes, and ranks the glyphs that most composites wait on
  (`make check-design`, `make queue`). It needs the Runebender binary.
- `benchmark.py`: scores a drafting pipeline on the held-out green glyphs in
  `tests/benchmark.json` (`make benchmark RUN=...`).
- `status.py`: writes `STATUS.md` from the mark colors (`make status`).

The loop that uses them is in
[documentation/design/system/learning.md](../documentation/design/system/learning.md).

`find_should_be_components.py` is an analysis aid. `refresh-ui-font.sh` is a
local editor-development utility, not a font release step.

The generator scripts that wrote whole glyph sets into the UFOs (`arabic_*`,
`latin_accents.py`, `embolden.py`, `build_anchors.py` and others) are in the
Git history before 2026-11-10. Do not restore them. Draw named glyphs through
Runebender proposals.

## Source compatibility

`report_master_compatibility.py --check` makes blocking source differences fail;
without --check its historical report-only interface is preserved.
