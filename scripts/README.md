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

## Drawing and source-writing utilities

`anchor_sheet.py` and `symbol_gen.py` measure reference sheets and write
candidate GLIFs under `out/`.

The `arabic_*`, `latin_*`, `build_anchors.py`, `propagate_anchors.py`,
`realign_components.py`, `fix_accent_offsets.py`, `embolden.py`,
`bold_copy_from_regular.py`, `normalize_winding.py`, `dot_variants.py`, and
`lam_alef_variants.py` tools include source construction, measurement, and
repair experiments. Read the individual script before running it. Their
presence is not permission to apply an entire batch to live UFOs. Use a scratch
copy for exploratory changes and preserve protected colors.

`find_should_be_components.py` and `rubik_weight_deltas.py` are analysis aids.
`refresh-ui-font.sh` is a local editor-development utility, not a font release
step.

The retired report/packaging script collection is available in Git history.
Do not restore it wholesale; extend the maintained commands only when needed.

## Source compatibility

`report_master_compatibility.py --check` makes blocking source differences fail;
without --check its historical report-only interface is preserved.
