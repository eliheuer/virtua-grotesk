# Build and QA

Run commands from the repository root. The canonical build is `make build`;
`make build-fontc` is an alternate compiler path, not the release baseline.

## Source snapshot and static layout

`make build` uses `scripts/build_source_snapshot.py` to copy active sources into
a temporary directory and normalize master glyph order there. This permits
per-master explicit layout coordinates without reordering the editor's UFOs.
`sources/config.yaml` names the four static instances; gftools derives them from
the compiled VF, including GPOS interpolation and standard overlap removal.
Do not revert to compiling Regular feature text independently for every static
weight. Static contour records need not match the former UFO-instance build;
compare against serialized VF instances and inspect mixed-script images.
[LAT-001 batch27](../agent-proofs/cases/latin-001/batches/27-short-stroke/README.md)
retains the initial failure, regression tests and before/after evidence.

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
compatible; preserve green drawings and their inherited geometry unless explicitly
authorized. Purple identifies new AI drawings awaiting human review; preserve
existing human grades for engineering-only repairs. No automated grade establishes
visual approval or reference status.
After edits, inspect the compiled fonts and actual rendered proofs. For curves:

```sh
.venv/bin/python scripts/curve_lint.py Regular <glyphs>
.venv/bin/python scripts/curve_lint.py Bold <glyphs>
```

`make grid-qa` and `make metrics` provide additional design checks.

For a new machine-drawn candidate, use the explicit 8-unit gate before building:

```sh
.venv/bin/python scripts/draft_grid_check.py \
  --ufo out/qa/CANDIDATE/sources/VirtuaGrotesk-Regular.ufo \
  --ufo out/qa/CANDIDATE/sources/VirtuaGrotesk-Bold.ufo \
  --glyphs he-hb het-hb tav-hb --json out/qa/CANDIDATE/draft-grid.json
```

This reads only the selected scratch glyphs and component donors. It checks
on/off-curve points, anchors, advances, component offsets and true ink
sidebearings. Popcounts are descriptive, never an automatic review color.
Run curve lint, compatibility, build/shaping checks and visual proofs separately.
Existing green optical geometry must not be snapped automatically. The older
`grid_lint.py` collapses unfamiliar colors into orange; use its numerical
inventory cautiously, never its inferred color as editing permission.
`make review-rubik` makes a comparison proof; override `RUBIK_FONT` as needed.
Rubik is a reference, not an acceptance standard for Virtua's design.
Eli reaffirmed on2026-10-21 that the actual Diffenator browser preview must be
part of visual review, with a matching Rubik proof. Generate context proofs and
a same-text comparison, then inspect400/550/700 in the browser:

```sh
.venv/bin/diff3proof 'fonts/variable/VirtuaGrotesk[wght].ttf' --output out/review
.venv/bin/diff3proof /path/to/Rubik.ttf --output out/review-rubik
.venv/bin/diff3proof 'fonts/variable/VirtuaGrotesk[wght].ttf' /path/to/Rubik.ttf --sample-mode cover --output out/review-comparison
```

In the stock comparison, Old/New identify first/second inputs, not design
approval. Record actual slider weights; the instance dropdown can remain stale
after a manual slider change. Keep full-language review and native-reader review
separate from a sampled browser inspection.


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
   Eli's drawing approval. Keep drafts unapproved; never assign green; new AI drawings use purple under Eli’s convention.
5. Run compatibility, curve and compiled-shaping checks appropriate to the edit.
   Apply only the authorized files after checking the active source hashes still
   match the baseline. Preserve backups. Rebuild active sources, compare with the
   candidate, and run the relevant tests, proof and full package QA. Record results
   against those exact sources/binaries, including failures.

### Pixel-difference diagnostic (legacy Python renderer)

For interactive review use the [live browser workflow](#live-browser-review) below. The Python helper remains available for explicit pixel-difference diagnostics; its old palette/layout is not the standard specimen design.

`scripts/proof_compare.py` is read-only with respect to fonts and sources.
HarfBuzz shapes each sample; FreeType rasterizes the resulting glyph IDs and
positions without hinting; Pillow assembles the labeled PNG. All panels use a
fixed pixels-per-em scale and the union of both runs' bounds, including advances.
The third panel shows unchanged ink dark, removed ink magenta, and added ink
cyan. Pixel differences can include rasterization changes; they are not scores
of correctness or drawing quality. Baseline ticks sit outside the ink.
Use the lower-contrast preview palette requested by Eli: light gray background
(`#dedede`) and dark gray glyphs and labels (`#444444`). Keep the magenta/cyan
difference colors. The JSON sidecar records the palette for reproducibility.

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
For large outline inspection use a single glyph at `--size 384`; for reading
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

### Ad hoc reference comparison (legacy Python renderer)

Use the live browser workflow below for interactive review; DesignBot can reproduce the historical three-sheet sets.
For ad hoc or historical reproduction, `scripts/proof_reference.py` can put Virtua beside one or more reference
fonts. It reuses the same shaping, rasterization, and gray palette as the
before/after renderer. Each panel uses the same pixels-per-em and baseline;
reference width axes stay at their defaults. Matching weight coordinates do
not guarantee matched apparent weight. Explicit size differences belong in a
separately labeled experiment, never hidden auto-fitting.

```sh
.venv/bin/python scripts/proof_reference.py \
  --font 'Virtua Grotesk=fonts/variable/VirtuaGrotesk[wght].ttf' \
  --font 'Rubik=/absolute/path/to/Rubik[wght].ttf' \
  --font 'Noto Sans Hebrew=/absolute/path/to/NotoSansHebrew[wdth,wght].ttf' \
  --samples documentation/proofs/hebrew-reference-samples.json \
  --weights 400 700 --output out/qa/reference/overview.png
```

Each sample has `label`, `text`, and optional `size` in pixels per em. For a
focused first review use `hebrew-dalet-resh-samples.json` with weights 400, 550,
and 700. To include a real candidate, add another `--font 'Virtua candidate=...'`;
do not duplicate current Virtua under a candidate heading. Use the difference
overlay tool for Virtua's own revisions, not to score likeness to another family.
A missing glyph produces a failing command with evidence left for diagnosis.

Before interpreting the proof, inspect every column and verify font provenance,
current source/build identity, script coverage, and the JSON sidecar. Keep named
references and exact hashes in the review. These are single-script samples;
paragraph bidi behavior still needs a browser proof.

Capture the feedback and selected proof images in
[Design review and feedback](../agent-proofs/FEEDBACK.md). That is the persistent
review record; this section owns the rendering mechanics.


### Live browser review

Start with the [web-proof guide](../agent-proofs/app/README.md) and `make proof-web`.
It is the default interactive review path. The
[Virtua Design Review entry point](../agent-proofs/README.md) owns the current
handoff; the web-proof guide owns launch and implementation instructions.

Eli selected live font rendering on 2026-10-19 (P018), after the image viewer
shrunk a 1600 px sheet into a roughly 455 px panel. For interactive reviews,
render the actual fonts as text; do not fit a raster specimen page into the panel.
Keep two grays, title case, Virtua labels and grid-based organization. Use the
[margin-based spacing contract](../agent-proofs/app/README.md#spacing-contract-p022)
for layout gaps and balanced sample ink fields. Screenshots
are evidence of a reviewed browser state, not the rendering mechanism.

The initial HEB-002 implementation is in `agent-proofs/app/`.
It supports comparison, in-place before/applied switching, size studies, running
text in Reading, weight
400–700 through numerical fields and sliders, custom text, reference fonts, dark mode and
layout guides. Font sizes
are CSS pixels per em, with zero extra tracking and no synthetic bold or hidden
rescaling. Fit defaults to one shared size that fits the available columns;
the size field displays the actual em size. Turn Fit off for fixed-size linked
scrolling. Samples share a baseline within each visual comparison row. Sizes
preserves its stated em sizes and reflows the columns as needed. Native browser font metrics and shaping
apply; this is not a pixel-equivalent replacement for the DesignBot renderer.
Do not interpret cross-renderer antialiasing differences as source edits.

Prepare from the exact reviewed font snapshot:

```sh
.venv/bin/python agent-proofs/app/prepare.py \
  --evidence agent-proofs/cases/hebrew-002/layout-v3/snapshot.json \
  --output-dir agent-proofs/cases/hebrew-002/layout-v3
.venv/bin/python -m http.server 60271 --bind 127.0.0.1 \
  --directory agent-proofs/cases/hebrew-002/layout-v3
```

Do not start a duplicate server if that local review is already open. The HTML
sample/title definitions currently describe HEB-002; adapt and record them when
preparing a different glyph group. Preparation checks snapshot hashes and copies
local fonts without editing them. Browser loading verifies those hashes again,
uses separate font-family aliases, and hides proofs on load/hash failure. Custom
text is checked against each font's cmap; unsupported strings show a missing-codepoint
notice instead of silent fallback. This gate does not establish language correctness.

Inspect the actual browser view at the user's panel width, test each relevant
control, and capture the state used for feedback. Record the rendering engine,
font hashes, settings and approval state. Font grading remains Eli's decision.
The fixed DesignBot workflow below is retained for historical reproduction or
explicitly requested exports; it is no longer the interactive-review default.

### Standard DesignBot comparison workflow

The DesignBot workflow was approved earlier on 2026-10-19; P018 subsequently selected live browser rendering for interactive review. The current v3 layout
is a revision awaiting visual approval after Eli rejected the earlier label
spacing and use of negative space. The canonical recipe is
[`documentation/proofs/hebrew_review.rs`](proofs/hebrew_review.rs), one Rust script
with three sheet modes. All labels and font samples are shaped and rendered by
DesignBot. `hebrew_review.py` is now a thin command runner and evidence verifier;
it no longer draws the sheets. Python/Pillow comparison images are retained as
historical evidence or explicit diagnostics, not the default presentation path.

The standard set is:

1. **Letterform comparison:** before / applied or candidate / Rubik / Noto;
   400, 550, 700 at 192 pixels per em.
2. **Reading texture:** the same columns and weights at 44, 32 and 24 pixels per em.
3. **Latin / Hebrew weight:** green Latin lowercase and capitals alongside the
   revised Hebrew, at 176 pixels per em. Weight remains provisional.

Every set exports both light and dark PNGs, swapping #dedede and #444444. Normal
antialiasing yields intermediate neutral grays. There are no red accents or colored
difference overlays in standard specimens. Labels use Virtua Grotesk at 400, with
title case for headings and short captions; explanatory footnotes use sentence
case. Literal case-sensitive glyph-test strings retain their intended case.
The current layout proposal is 1600 × 1120 with 80-pixel margins and an 8-pixel
baseline unit. A 128-pixel label rail plus a 32-pixel gutter gives the comparison
field its own left edge at x=240. Four columns are 296 pixels wide with 32-pixel
gutters; three-column sheets use 384-pixel columns and 64-pixel gutters.
Use alignment and whitespace instead of repeated slash separators: font name
above review role, weight name above its numeric coordinate in the adjacent
label rail, and one size note
per page. Keep the folio quiet and footnotes brief; omit redundant column numbers.
Labels must visually belong to their samples. Separate rows with deliberate
whitespace and light rules; do not interpret a square-grid overlay as proof of
good grouping. This records Eli's later correction (P016), superseding the prior
layout approval. V3's precise dimensions remain a proposal until reviewed.

Large headlines are 56 px with **−0.02 em tracking (−1.12 px)** as the initial
setting for Eli's request for tighter headlines. It is explicit and adjustable
with `--headline-tracking-em`; other labels and every specimen run use zero added
tracking. Keep font size, sample text, origin and baseline shared across the fonts in each
comparison row. Any group-wide sample/scale change must be explicit in evidence;
never auto-fit or adjust one font to resemble another. Width and ink-bound checks fail instead of auto-fitting.

```sh
.venv/bin/python documentation/proofs/hebrew_review.py \
  --before /absolute/path/to/frozen-before.ttf \
  --after 'fonts/variable/VirtuaGrotesk[wght].ttf' \
  --rubik '/absolute/path/to/Rubik[wght].ttf' \
  --noto '/absolute/path/to/NotoSansHebrew[wdth,wght].ttf' \
  --state applied \
  --output-dir out/qa/my-review/specimens
```

Use `--state candidate` for a scratch proposal. The runner exports six PNGs plus
`review.json`, containing input and output hashes, exact commands, axis ranges,
size/tracking choices and validation. It checks the required cmap coverage and
family/weight identities, then verifies that final PNGs are opaque and use only
neutral grays between the two palette endpoints. `--grid` makes a separate structural-guide export showing the actual rail,
columns, gutters and row modules. `--baseline-grid` adds the 8-pixel baseline
guides. Neither flag produces the clean export; omit both for clean output.
The layout and overlay share `ReviewGrid` in the Rust recipe. Inspect guides
and final sheets. `--themes light` or `--themes dark` is
useful while developing, but retain both for a completed review.

The Rust script can also run directly:

```sh
designbot --raw documentation/proofs/hebrew_review.rs --output out/form.png -- \
  light form BEFORE.ttf AFTER.ttf RUBIK.ttf NOTO.ttf applied
```

Its other sheet modes are `text` and `weight`. Direct execution accepts
`HEADLINE_TRACKING_EM`, `GRID_VIEW=1` (structure), and
`GRID_VIEW=baseline` (structure plus baselines). `GRID_VIEW=0` is clean. Always use `--raw` to avoid DesignBot's
social-image processing. The present DesignBot text path enables hinting; record
any later change rather than silently mixing rendering policies.

Each column renders in a separate font context. Before and after must never
compete under the same family name in one collection. Native-size monochrome
layers preserve origins and coverage; the script converts the backend's
premultiplied frame RGB to the straight-alpha representation expected by the image
API. Keep that conversion or dark-mode edge halos return. These are DesignBot
renders throughout, without Pillow sample rasterization.

After a layout change: render both polarities, inspect all three sheets and a grid
overlay, verify title tracking does not leak into samples, and retain selected
PNGs plus the evidence JSON in the review record. Preserve the frozen before font
and reference hashes; never reconstruct historical “before” from current sources.
No font build or full release QA rerun is needed for presentation-only edits.
Shaping/layout smoke checks do not replace native-reader review or full script QA.

The [HEB-001 review](../agent-proofs/cases/hebrew-001/README.md) records the approved
workflow and selected outputs. Extend the Rust recipe for the next named glyph
scope; do not revive the superseded Python presentation stack by default.

### DesignBot rendering diagnostic

The focused [Rust diagnostic](proofs/designbot_diagnostic.rs) tested the
DesignBot rendering path before the approved port of the full specimen set. It uses Virtua
Regular captions, title case, and two reversible grays. The only Pillow input is
a labeled frozen control panel, generated by `designbot_diagnostic_control.py`.
See [HEB-001](../agent-proofs/cases/hebrew-001/README.md#designbot-diagnostic-and-virtua-captions--2026-10-19)
for commands, font identities, inspected light/dark outputs and the hinting/
alpha-compositing findings. The full port now uses the standard workflow above; retain this diagnostic and
the original Python images as historical evidence.


For the next current-state group, pass `--group he-het-tav` and supply the current
Virtua VF for both `--before` and `--after`. This mode displays only Current,
Rubik and Noto columns; no duplicate before column or implied candidate. Form
and Latin-context sheets use one shared 160 px/em size to fit three Hebrew
letters; the default dalet/resh group retains its sample sizes within the revised layout.
See [HEB-002](../agent-proofs/cases/hebrew-002/README.md) for the proposal and exact evidence.
For its scratch comparison use `--group he-het-tav-candidate --state candidate
--details` with frozen baseline and candidate fonts. This adds Before/Candidate
columns, uses one shared 136 px/em for the four-column form sheet, and adds
384 px/em single-glyph details plus mark-attachment examples. Both light and dark
versions remain required. The precomposed he/tav-with-dagesh forms are shown as
unchanged dependencies, not silently updated with the three plain letters.
The form string now uses the contiguous letters `החת` at 136 px/em in the
four-column group, rather than the former spaced string at 120 px/em. Samples
remain identically shaped at the stated scale in every font. Historical v2
proofs are retained with their original size and text.

The planned long mixed-script text review follows the alphabet pass; its scope
is recorded in [Next phases](../agent-proofs/FEEDBACK.md#next-phases).
