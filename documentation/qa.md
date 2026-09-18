# Build and QA

Run commands from the repository root. The canonical build is `make build`;
`make build-fontc` is an alternate compiler path, not the release baseline.

## Tools

`make setup` installs `requirements.txt` into `.venv`. Python requirements are
pinned; use `.venv/bin/python` for scripts. `requirements.in` lists the direct
dependencies. Keep both files in sync when deliberately updating the toolchain.

Install [Fontspector 1.7.4](https://github.com/fonttools/fontspector/releases/tag/fontspector-v1.7.4)
for the current audit baseline. Set `FONTSPECTOR=/path/to/fontspector` to use a
specific binary without changing the system installation. Recheck the official
release before submission and rerun QA after any tool update.

`make proof` requires [designbot](https://github.com/eliheuer/designbot), installed
separately from its CLI crate. Browser proofs use the Python environment.

## Commands

| Command | Purpose |
| --- | --- |
| `make build` | Compile one variable and four static TTFs. |
| `make test` | Development QA, offline, with four documented exclusions. |
| `make qa-full` | Build and run the full Google Fonts profile, with network checks and no exclusions. |
| `make qa-full QA_NETWORK=offline` | Full profile without network checks; incomplete release evidence. |
| `make qa-package PACKAGE=/path/to/ofl/virtuagrotesk` | Full profile on the assembled downstream package; no rebuild. |
| `make review` | Build a diffenator2 proof in `out/review/`. |
| `make proof` | Build and render `documentation/proofs/proof.pdf`. |
| `make reports` | Regenerate the three metadata and compatibility reports. |
| `make preflight` | Build, proof, reports, and required-file checks. |

QA writes JSON, Markdown, and tool-version evidence under `out/qa/`. Use
`QA_REPORT_DIR` for a separate run. FAIL or worse returns a failing exit code;
WARN requires review and remains visible. No warnings are automatically waived.
The [official QA guide](https://googlefonts.github.io/gf-guide/qa.html) explains
these severities and the Google Fonts profile.

Preflight checks presence, not freshness or drawing quality. `make skeleton`
tolerates QA failures so it can finish reports; it is not a release gate.
`make specimen` is unimplemented. Do not use its output as release evidence.

## Drawing and spacing

Check source colors and unresolved decisions before editing. Keep both masters
compatible; preserve green and purple glyphs and leave AI candidates blue.
After edits, inspect the compiled fonts and actual rendered proofs. For curves:

```sh
.venv/bin/python scripts/curve_lint.py Regular <glyphs>
.venv/bin/python scripts/curve_lint.py Bold <glyphs>
```

`make grid-qa` and `make metrics` provide additional design checks.
`make review-rubik` makes a comparison proof; override `RUBIK_FONT` as needed.
Rubik is a reference, not an acceptance standard for Virtua's design.

For regression comparisons:

```sh
PATH="$PWD/.venv/bin:$PATH" .venv/bin/diffenator2 diff OLD.ttf NEW.ttf -o out/diff
```

Review accent centering, collisions, mark attachment, joining, mixed-direction
text, and interpolation across weights. Numeric coverage and table presence do
not establish script quality. Source-writing helpers are edits, not QA checks;
inspect their scope before running them.

For release review, keep source revision, binary hashes, tool versions, reports,
and proof review together. Finish the [onboarding checklist](google-fonts/README.md)
before publication. The CI workflow builds and reports failures; it does not
publish releases automatically.
