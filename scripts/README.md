# Scripts

This folder holds only the tools that are specific to Virtua Grotesk. The
general source tools are in
[fontgarden-tools](https://github.com/fontgarden/fontgarden-tools), which
`make setup` installs: status, queue, design checks, change checks, GLIF and
curve checks, the build, the drafting evaluation and the corrections. Run them
with `make` or `.venv/bin/fontgarden <command>`. Change a general tool in
fontgarden-tools, not here.

Run the Python scripts from the repository root with `.venv/bin/python`.
`make help` lists the commands that use them.

## Build

| Script | Use |
| --- | --- |
| `build.sh` | The release build (`make build`): `fontgarden build`, then `fix_gf_metadata.py`. |
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

## QA profile

| Script | Use |
| --- | --- |
| `fontspector_fontgarden.py` | Fontspector plugin with the Font.Garden profile: the Google Fonts profile plus the em size, grid, vendor ID and license checks (`make qa`). It will be replaced by [fontspector-fontgarden](https://github.com/fontgarden/fontspector-fontgarden). |

## Proofs

Specimen and publicity images are DesignBot scripts in `documentation/`, next to
their output. `make proof` uses DesignBot for the PDF proof.

| Script | Use |
| --- | --- |
| `proof-web/` | The live comparison with `reference-fonts/` (`make proof-web`). See [proof-web/README.md](proof-web/README.md). |

Do not add scripts that write whole glyph sets into the UFOs. The old
generators are in the Git history before 2026-11-10. Draw named glyphs through
Runebender proposals.
