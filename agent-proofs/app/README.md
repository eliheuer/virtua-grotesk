# Live web proof

Design context and current work live in [design/](../../design/README.md).
This app renders verified Before/Working font snapshots and local references.
Its accepted layout remains in place. Historical UI proposals and feedback are
preserved in [the prior guide](history-2026-10-29.md); dated queues there are not
current drawing instructions.

## Start here

```sh
make proof-web
.venv/bin/python agent-proofs/serve.py --check
```

Open the printed localhost URL (default http://127.0.0.1:60272/). The server verifies
font hashes and reuses a matching implementation. It does not rebuild fonts or
watch UFO saves. Do not replace a missing baseline with today's build.

The default portable snapshot comes from `design/reviews/current.json`. An explicit
`--snapshot <prepared-directory>` selection is remembered in ignored
`out/live-proof-selection.json`, using a repository-relative path when possible.
The current state's label/verdict/note overlays only its exact proof_snapshot;
other explicit snapshots retain their own labels. An applied draft may still be
rejected. `--directory <archive>` serves frozen historical UI explicitly.

Live UI/cache output is under `out/live-proof/`. After changing the server code,
verify and stop only that proof process before restarting; use a separate --port
for an intentional separate review. Never stop an unrelated localhost server.

## Prepare a snapshot

Read prepare.py --help and the current case's evidence manifest. Supply actual
frozen fonts and SHA-256 values, source/candidate revision and chosen labels.
Preparation defaults to Candidate, never Applied. The manifest accepts `study`
metadata: glyphs, presets, id, status, note, language and readingDefault. Font
records may specify label. A current-only study may omit before and label after
Current; Toggle is then unavailable. Configure the study, not the shared layout.

Preserve the resulting source/font files, live-fonts.json, review-data.js and
selected screenshots in the case under design/reviews. Update current.json only
when that is the next intended review. See [review records](../../design/reviews/README.md).

## Shared reference fonts

The proof and Runebender use project-local reference-fonts/. It is ignored by Git;
keep font licenses with supplied local TTF/OTF files. Subdirectories and uppercase
extensions work. reference_fonts.py groups verified faces, reports coverage/errors,
and supplies nearest-weight static faces or variable ranges. It recognizes Git
worktrees. Polling refreshes references without replacing frozen Before/Working.
Missing coverage is visible; never interpret system fallback as a reference glyph.
External fonts inform script comparison, not approval of Virtua construction.

## Mode names

Compare shows matched columns; Toggle switches Before/Working in place; Waterfall
uses a continuous bounded size range; Text shows paragraphs/whole-font samples.
All comparisons keep one em size and weight. Fit preserves relative reference
proportions; do not scale each font separately. Text retains reading-size controls.
Names/Unicode identities wrap and reflow on narrow screens. Dark is the default;
light mode remains available. Preserve the neutral palette and shared grid.

## Arabic base-form samples

For dual-joining letters use normal shaped repetitions, e.g. `ببب ب`, to show
initial/medial/final/isolated forms. Right-joining letters have only their actual
forms; do not manufacture four using presentation characters. Keep language ar,
RTL and word/mark presets, and verify built-font glyph sequences at 400/700.
The Sample picker also provides Arabic alphabet/joining forms, All scripts and
Encoded repertoire. The latter uses printable cmap entries and dotted-circle
mark carriers; it is not a list of unencoded components/contextual alternates.

## Whole-font views and image inspection

Inspect the actual browser rendering, font loading, coverage, marks, bidi and
controls. Use bounded screenshots rather than one unreadable full-font image.
For fixed details use the verified live manifest:

```sh
.venv/bin/python agent-proofs/app/render-detail.py \
  --proof-dir out/live-proof --output out/detail-700.png \
  --text 'س سمسم سلام ش' --title 'Seen' --weight 700
```

The runner verifies hashes/coverage, invokes DesignBot --raw and records a receipt.
It isolates font contexts, measures actual ink bounds and keeps a shared size.
Inspect 400 and 700 for Arabic drawing, with Before/Working and Rubik, Noto Sans
Arabic, IBM Plex Sans Arabic and Readex Pro. Retain images, hashes and visible
findings in the case. Large and reading-size proofs complement curve diagnostics;
render success is not human approval. See [verification](../../design/system/verification.md).

## Spacing contract (P022)


Use the page’s side margin as **U**, defined once by `--space`. The current
responsive values are 32 px above 800 px, 24 px at 600–800 px, and 20 px below
600 px. Changing U changes its entire family of tokens together; do not add
independent component paddings to tune a screenshot.

| Relationship | Spacing |
| --- | --- |
| Page margins, headline padding, main section intervals | U |
| Column gutters, control row gaps, rule-to-caption spacing, footer inset | U/2 |
| Font-name to role gap, inline label gaps | U/4 |
| Fit field’s small horizontal safety inset | U/8 |
| Slider track to the value rule above and comparison rule below | U each |
| Sample ink field above the highest ink and below the lowest ink | U each |
| Wrapped comparison row separation | U, in addition to each sample field’s padding |

Control value boxes have height U + U/2 so native select text remains readable
at small widths. Font sizes, line metrics, border widths and slider-thumb shapes
are typography/control dimensions rather than arbitrary layout gaps. Headlines
and captions use native cap/baseline text-box trimming where supported.

For samples, browser TextMetrics measures ink ascent/descent. The first baseline
is shared across fonts, with U above the row’s maximum ascent and U below its
maximum descent (including wrapped lines). Only the native text’s vertical
position changes; equal em scale, advances, reference proportions and shaping
remain intact. Shorter glyphs naturally leave extra space above their own ink.
Canvas is used for measurement only; the visible sample remains live DOM text.
Do not replace this with per-font optical centering or a fixed em-height crop.

Grid shows shared columns and U/4 horizontal spacing guides. Before promoting
a layout change, inspect clean and guided output, check both slider intervals,
verify that marks/descenders and multiline text remain visible, and retain the
measured spacing with the case record. These checks support visual review;
Eli’s response determines whether the design works.

## Rendering contract

Visible samples are live DOM text from verified local fonts with independent
family aliases; canvas measures only. Preserve shared baselines, actual reference
proportions and glyph clipping clearance. Screenshots record a browser state.
Make review is separate Diffenator3 QA; make proof is the DesignBot print PDF.
None establishes human grading or Google Fonts release readiness.

P043 supersedes older divider/control proposals: structural rules and slider tracks
use 2px rounded strokes; controls start U/2 below the menu, field height is U,
label/row gap U/4, slider hit area U/2 and bottom padding U/4. Toggle retains its
U-high two-button control. Preserve existing checkboxes, typography and alignment.

## Code and evidence

| File | Owns |
| --- | --- |
| index.html, review.css, review.js | Shared interface and live rendering |
| prepare.py | Freeze verified source manifests into review assets |
| reference_fonts.py, reference-selection.js | Local font discovery and face choice |
| ../serve.py | Current-state selection, validation and server reuse |
| render-detail.py, render-detail.rs | Bounded fixed raster evidence |
| reading-samples.json, overview-samples.json | Shared reading and repertoire text |

Run Python app tests with `.venv/bin/python -m unittest discover -s agent-proofs/app -p 'test_*.py'`
and JS tests with `node --test agent-proofs/app/test-reference-selection.cjs`.
Frozen old copies in review folders reproduce earlier comparisons; edit the app
sources here for current UI. Do not overwrite archived evidence with a rerender.

## Construction study companion

For a rejected curve/style repair, use [the construction review gate](../../design/constructions/review-gates.md). `scripts/construction_review.py` generates a separate read-only shared-scale SVG study with optional point indices. Keep the live font proof for reference-font and reading-size comparison. The study does not replace this app or change its layout, sources or grading.
