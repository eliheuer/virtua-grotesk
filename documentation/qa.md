# Build and QA

Run commands from the repository root. The canonical build is `make build`;
`make build-fontc` is an alternate compiler path, not the release baseline.

## Tools

`make setup` installs `requirements.txt` into `.venv`. Python requirements are
pinned; use `.venv/bin/python` for scripts. `requirements.in` lists the direct
dependencies. Keep both files in sync when deliberately updating the toolchain.

`make setup` also installs [Fontspector 1.9.0](https://github.com/fonttools/fontspector/releases/tag/fontspector-v1.9.0)
into `.venv/bin`, verifying the official archive SHA-256. The wrapper prefers
that binary over older global installations. macOS ARM64 and Linux x86-64
are supported by the installer; on other platforms install the same version
manually and set `FONTSPECTOR=/path/to/fontspector`. CI uses the same installer.

Latest stable versions rechecked on **2026-10-18**:

| Tool | Version |
| --- | --- |
| Fontspector | 1.9.0 |
| gftools | 0.10.4 |
| Diffenator3 / diff3proof | 1.1.4 |
| fontTools | 4.67.0 |
| fontmake / ufo2ft | 3.12.2 / 3.9.1 |
| glyphsets / gflanguages | 1.1.3 / 0.7.11 |
| gfsubsets / axisregistry | 2025.11.4 / 0.4.20 |
| uharfbuzz / OpenType Sanitizer | 0.56.3 / 9.2.0 |

Recheck official releases/PyPI before submission. Evidence of this version
lookup is in `out/qa/2026-10-17/latest-tools/pypi-versions.json` and
`fontspector-release.json`. FontBakery's latest release is still 1.1.0; it is
not the active QA gate. Diffenator2 0.5.0 and FontBakery's legacy Google Fonts
extra require old protobuf and cannot share the latest gftools dependencies.
Use the current Fontspector/Diffenator3 stack in this environment.

`make proof` requires [designbot](https://github.com/eliheuer/designbot), installed
separately from its CLI crate. Browser proofs use the Python environment.

## Commands

| Command | Purpose |
| --- | --- |
| `make build` | Compile one variable and four static TTFs. |
| `make test` | Development QA, offline, with three documented exclusions. |
| `make qa-full` | Build and run the full Google Fonts profile, with network checks and no exclusions. |
| `make qa-full QA_NETWORK=offline` | Full profile without network checks; incomplete release evidence. |
| `make qa-package PACKAGE=/path/to/ofl/virtuagrotesk` | Full profile on the assembled downstream package; no rebuild. |
| `make review` | Build a Diffenator3 HTML proof in `out/review/`. |
| `make proof` | Build and render `documentation/proofs/proof.pdf`. |
| `make reports` | Regenerate the three metadata and compatibility reports. |
| `make preflight` | Build, proof, reports, and required-file checks. |

Package QA includes referenced article image/video files in its input set and
hashes. QA writes JSON, Markdown, and tool-version evidence under `out/qa/`. Use
`QA_REPORT_DIR` for a separate run. FAIL or worse returns a failing exit code;
WARN requires review and remains visible. No warnings are automatically waived.
The [official QA guide](https://googlefonts.github.io/gf-guide/qa.html) explains
these severities and the Google Fonts profile.

Preflight checks presence, not freshness or drawing quality. `make skeleton`
tolerates QA failures so it can finish reports; it is not a release gate.
`make specimen` is unimplemented. Do not use its output as release evidence.

## Drawing and spacing

Check source colors and unresolved decisions before editing. Keep both masters
compatible; preserve green and purple reference drawings unless explicitly
authorized. Leave new outline drafts orange and composite drafts blue; neither
color is approval or a claim of drawing quality.
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
.venv/bin/diffenator3 OLD.ttf NEW.ttf --html --instance '*' --output out/diff
```

Review accent centering, collisions, mark attachment, joining, mixed-direction
text, and interpolation across weights. Numeric coverage and table presence do
not establish script quality. Source-writing helpers are edits, not QA checks;
inspect their scope before running them.

For release review, keep source revision, binary hashes, tool versions, reports,
and proof review together. Finish the [onboarding checklist](google-fonts/README.md)
before publication. The CI workflow builds and reports failures; it does not
publish releases automatically.

## Chat proof workflow

This is the reusable workflow used for the October 2026 Arabic repairs and
Hebrew drafts. Start a new session by reading AGENTS.md, this section, and the
current evidence and remaining issues in [the onboarding record](google-fonts/README.md).
An older proof or passing check is not evidence for subsequently edited sources.

1. Record the named glyph/master scope and the user's authorization. Reuse an
   existing authorization, including a broader batch authorization; do not ask
   for the same permission at every step. Record any approval still pending.
2. Snapshot the active sources and compiled baseline before editing. Record
   source hashes and the Git revision, including dirty-file differences. Make
   candidate edits on scratch copies and build with the canonical build pipeline.
3. Render isolated details plus shaped text at 400, 550, and 700, and at useful
   reading sizes. Use identical scale, origin, and baseline for each before/after
   pair. Independently auto-fitting each glyph can conceal width/proportion
   changes. Include relevant vowel/mark stacks, joining, and inherited composites.
4. Inspect actual PNGs, show selected comparisons inline in chat, and describe
   visible changes and unresolved limitations. Use an absolute Markdown image
   path in Codex. Separate technical validation, agent visual inspection, and
   Eli's drawing approval. Keep drafts unapproved; never grade green/purple.
5. Run compatibility, curve and compiled-shaping checks appropriate to the edit.
   Apply only the authorized files after checking the active source hashes still
   match the baseline. Preserve backups. Rebuild active sources, compare with the
   candidate, and run the relevant tests, proof and full package QA. Record results
   against those exact sources/binaries, including failures.

### Reusable comparison renderer

`scripts/proof_compare.py` is read-only with respect to fonts and sources.
HarfBuzz shapes each sample; FreeType rasterizes the resulting glyph IDs and
positions without hinting; Pillow assembles the labeled PNG. All panels use a
fixed pixels-per-em scale and the union of both runs' bounds, including advances.
The third panel shows unchanged ink dark, removed ink magenta, and added ink
cyan. Pixel differences can include rasterization changes; they are not scores
of correctness or drawing quality. Baseline ticks sit outside the ink.

```sh
.venv/bin/python scripts/proof_compare.py \
  --before /absolute/path/to/before.ttf \
  --after 'fonts/variable/VirtuaGrotesk[wght].ttf' \
  --samples documentation/proofs/hebrew-review-samples.json \
  --weights 400 550 700 --size 96 \
  --output out/qa/my-candidate/comparison.png
```

The JSON sidecar records input SHA-256 hashes, renderer versions, exact text,
weights, positions, changed-pixel counts, and missing-glyph flags. The sample
file is a small Hebrew smoke set; extend or replace it for the named glyphs.
For large outline inspection use a short sample at `--size 384`; for reading
texture render at 24 or 32. For mixed-script paragraphs and browser-engine
behavior also use `make review`: this helper shapes each line as a single run,
not a full bidirectional paragraph layout. It does not build fonts or apply edits.

The standard designbot PDF remains `make proof`. Earlier batch-specific
isolated-glyph sheets used fontTools paths and Skia; some auto-fit each glyph
and must not be used to judge relative widths. The new helper standardizes
shaped comparisons, not the drawing/generation process.

### What survives another session

The renderer, smoke samples, instructions, regression tests, and current release
status are tracked in Git. A fresh clone can build and generate new comparisons.
Raw snapshots, candidate construction/apply scripts, historic PNGs, and QA logs
under `out/qa/` remain local ignored artifacts: links there work only while those
files exist. A new session must not assume they arrived with a clone or silently
regenerate a purported historical before state from today's sources. Preserve a
needed baseline explicitly, or build two known revisions in isolated checkouts.

For each handoff update the existing onboarding record with scope, source and
binary identities, proof paths, tests/results, remaining visual concerns, and
application/approval state. Keep future reusable helpers in `scripts/` and
sample recipes under `documentation/proofs/`; keep temporary experiments in
`out/`. This is a documented agent workflow, not an automatic background task.
