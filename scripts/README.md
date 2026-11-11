# Scripts

Run the Python scripts from the repository root with `.venv/bin/python`.
`make help` lists the commands that use them.

## Build

| Script | Use |
| --- | --- |
| `build.sh` | The release build (`make build`). |
| `build_source_snapshot.py` | Copies the sources to a temporary folder for the build, so the glyph order of the editor stays unchanged. |
| `fix_gf_metadata.py` | Corrects the metadata of the compiled fonts. `build.sh` calls it. |
| `install_fontspector.py` | Installs Fontspector into `.venv` (`make setup`). |

## QA and reports

| Script | Use |
| --- | --- |
| `check_gf_fonts.sh` | Fontspector checks: development, full and package (`make qa`, `make qa-full`, `make qa-package`). |
| `check_hebrew.py` | Hebrew coverage and mark attachment in the compiled font (`make qa-hebrew`). |
| `run_reports.py` | Runs the three `report_*.py` scripts and writes to `out/reports/` (`make reports`). |
| `report_master_compatibility.py` | Compatibility of the two masters. `--check` fails on a blocking difference. |
| `report_source_metadata.py`, `report_generated_font_metadata.py` | Metadata of the UFOs and of the compiled fonts. |

## Design checks

The loop that uses these scripts is in
[documentation/design/system/learning.md](../documentation/design/system/learning.md).

| Script | Use |
| --- | --- |
| `check_design.py` | Checks glyphs against the grid and stroke targets in `sources/design.toml`, checks composites against their parts and anchor recipes, and ranks the glyphs that most composites wait on (`make check-design`, `make queue`). It needs the Runebender binary. |
| `check_changes.py` | Compares the sources with a base revision: no green glyph changed, and glyphs with changed contours are purple. It can draw before and after proofs (`make check-changes`). |
| `benchmark.py` | Scores a drafting method on the held-out green glyphs in `tests/benchmark.toml` (`make benchmark RUN=...`). |
| `status.py` | Writes `STATUS.md` from the mark colors (`make status`). |
| `source_inventory.py` | Reads glyph records and mark colors. Other scripts import it. |
| `glif_lint.py` | Finds structural faults in GLIF files, for example a missing component base. `check_changes.py` runs it on the changed glyphs. |
| `curve_lint.py` | Crest centering, tension breaks, inflections and join continuity (`make lint-curves`). |

## Proofs

Specimen and publicity images are DesignBot scripts in `documentation/`, next to
their output. `make proof` uses DesignBot for the PDF proof.

| Script | Use |
| --- | --- |
| `proof-web/` | The live comparison with `reference-fonts/` (`make proof-web`). See [proof-web/README.md](proof-web/README.md). |

Do not add scripts that write whole glyph sets into the UFOs. The old
generators are in the Git history before 2026-11-10. Draw named glyphs through
Runebender proposals.
