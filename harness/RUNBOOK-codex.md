# RUNBOOK — AI glyph completion (crawl phase)

Operating contract for a coding agent (Codex, Claude, or other) adding or
regenerating **one glyph at a time** in this repo. The full system plan is
`plans/ai-font-completion-harness.md`; the design contract every glyph must
obey is the root **`DESIGN.md`**. Read both before your first glyph.

Crawl-phase scope: single glyphs, Regular master quality first, a human
reviews every result. Do not batch, do not loop, do not touch glyphs you were
not asked about.

**Division of labor (do not invert it):** the image model supplies *drawing*
only — shape and style. Everything measurable — scale, vertical placement,
stroke weight, spacing — is deterministically derived, corrected, or gated by
you and the tools. A human-supplied image is **shape intent**, never weight or
placement ground truth; the weight/style ground truth is the font's **green
glyphs**. Never ask the human for a "better" image to fix weight or placement
— the pipeline fixes those.

## Context you must load

1. `DESIGN.md` — the power-of-two grid, 16-unit chamfers, metrics, curve and
   spacing rules. Every adjustment you make is justified by this file.
2. `AGENTS.md` — repo conventions, especially the source-editing footguns.
3. `plans/ai-font-completion-harness.md` §3 (mark-color protocol) and the
   canvas template spec (§4b).

Hard rules (repeated from those files because agents skip links):

- **Never modify a green glyph** (`public.markColor` = `0.09,0.72,0.44,1`).
- **Never save the real UFOs through a font library** (defcon/ufoLib/norad
  `font.save()`). Write `.glif` XML directly in repo style: tabs for
  indentation, double-quoted attributes, no space before `/>`, attribute
  order `x`, `y`, `type`, `smooth`.
- Both masters must keep **identical contour/point structure** per glyph.
- Rendering is **designbot (Rust)** — `designbot --render <script.rs>
  --output <png>`; scripts may use the re-exported `norad`/`kurbo` and
  `draw_path(BezPath)`. No Python for rendering.
- Plain commit messages; no AI credit trailers.
- Work goes in `.glyph-ai-runs/<glyph>/` (git-ignored). Never in `build/`.

## Environment setup (once per session)

```sh
export IMG2BEZ_LOG="$HOME/.img2bez/virtua-grotesk-traces.jsonl"
```

`img2bez` is on PATH (`~/.cargo/bin/img2bez`). Check `img2bez masters --help`
— it is authoritative over any flag list written here. `designbot` must be
the **local** build (`cargo install --path designbot-cli` in
`~/GH/repos/designbot`) — the GitHub build lacks the canvas APIs the
toolchain script needs.

## The canvas template (the shared coordinate frame)

Every machine-facing image in the loop — style sheets, generation targets,
returned generations — lives on one fixed canvas, so pixel↔font-unit mapping
is **known, never guessed**:

- **1536 × 1536 px, 1 font unit = 1 px.** Drawing band 1024 px tall
  (ascender→descender), 256 px margin top and bottom.
- Metric lines at fixed pixel rows: ascender & cap height **y=256** (they
  share the 768 ceiling), x-height **y=448**, baseline **y=1024**,
  descender **y=1280**.
- Small solid fiducial squares in the four margin corners (drift check).
- **Machine-facing images are light mode**: white background, black glyph
  ink; template graphics (metric lines, fiducials, labels) in **pure green
  `#00ff00`** — chroma-key style. The lines cross the drawing band and get
  repainted by the model, so the key color must survive approximate
  repainting: ink extraction keeps only dark, *desaturated* pixels and drops
  anything saturated. Dark mode is only for images a human reviews (step 7).

The mapping this buys: a pixel at row *y* is at font-unit
`768 − (y − 256)`; the ink's pixel bbox gives exact `--target-height` /
placement inputs for tracing. No `--fit` guessing.

## The procedure: one glyph

Inputs: a glyph name (e.g. `at`), and optionally a human sketch image
(shape intent).

### 1. Inspect the target

- Read `sources/VirtuaGrotesk-{Regular,Bold}.ufo/glyphs/<name>.glif` if it
  exists: note `public.markColor`, advance width, unicode. Red = replace the
  outline, keep metrics as a starting point. Missing = register it later
  (step 8b). Green = stop and report; wrong target.

### 2. Prepare canvas assets (checked-in toolchain — never hand-roll)

The coordinate frame is implemented **once**, in
`harness/designbot/glyph_canvas.rs`. Use it for every canvas image; do not
write your own renderer or do any px↔unit math (this is where run 2 failed).
All commands run from the repo root; `RUN=.glyph-ai-runs/<name>`.

- **Style sheet** per master — 6–10 green glyphs at true scale showing
  style, weight, and how ink relates to the lines (pick load-bearing greens:
  o n H O e s, plus any structurally close to the target; it warns on
  non-green picks):

  ```sh
  designbot --render harness/designbot/glyph_canvas.rs \
    --output "$RUN/style-Regular.png" -- \
    sheet sources/VirtuaGrotesk-Regular.ufo o,n,H,O,e,s
  ```

- **Target canvas + mask** per master — registers the shape-intent image
  into a vertical band as a light-gray ghost and writes the drawing-band
  mask (transparent = editable):

  ```sh
  designbot --render harness/designbot/glyph_canvas.rs \
    --output "$RUN/target-Regular.png" -- \
    ghost <shape-intent.png> baseline:cap "$RUN/mask.png"
  ```

  Band by glyph class (zones or raw numbers): caps/figures `baseline:cap`,
  lowercase `baseline:xheight`, descenders e.g. `-256:xheight`. If there is
  no sketch, bootstrap: one unmasked generation on a bare `template` render
  to get a shape draft, then feed that draft back as the ghost.
- **Current-state render** of any source glyph (sanity view):
  `... -- glyphbox sources/VirtuaGrotesk-Regular.ufo <name>`.

### 3. Generate (OpenAI image API) — with the correction loop

Call the image edit endpoint with: the target canvas as the base image, the
mask, and the style sheet as a reference image. gpt-image-2 keeps input
fidelity high automatically; on older models pass `input_fidelity: "high"`.
Prompt essentials: "ink the light-gray ghost glyph in exactly the style and
stroke weight of the reference sheet — monolinear geometric grotesk, 45°
chamfered corners on straight junctions, open apertures; solid black ink,
one glyph; change nothing outside the ghost; preserve all red guide lines
and markers." Repeat the preserve-list on every iteration.

Then **gate and self-correct — never ask the human**. One command runs the
gates (interim Python; being ported to img2bez):

```sh
./.venv/bin/python harness/canvas.py extract \
  --image "$RUN/generated-Regular.png" --master Regular \
  --out "$RUN/ink-Regular.png"
```

It prints JSON: fiducial check, ink bbox in **font units**, the exact
`--fit` band for tracing, measured stroke width vs the master's stem ladder
(±15% gate), and — on a weight failure — a ready-made `correction_prompt`
("same glyph, same skeleton, strokes ~N% thicker"). Exit code 2 = a gate
failed → re-prompt with the correction (reuse the previous output as the new
base image) and run extract again. Also sanity-check the ink's vertical
band: a glyph in the wrong zones (e.g. a question mark plunging below
baseline) → regenerate with the ghost/band fixed. Run `img2bez stats` on the
extracted ink if sharpness is in doubt.

Budget: ~3 correction rounds. Still failing → stop and report with the
attempts attached; do not trace a failing image.

### 4. Trace

- The extract step already wrote clean black-on-white ink
  (`ink-<master>.png`) and printed the exact fit band — use them verbatim.
- **Trace on a scratch copy — never point img2bez at `sources/`** (it
  writes through norad, which reformats files):

```sh
RUN=.glyph-ai-runs/<name>
mkdir -p "$RUN/trace"
cp -R sources/VirtuaGrotesk.designspace \
      sources/VirtuaGrotesk-Regular.ufo \
      sources/VirtuaGrotesk-Bold.ufo "$RUN/trace/"

img2bez masters "$RUN/trace/VirtuaGrotesk.designspace" \
  --glyph <name> --unicode <HEX> \
  --image Regular="$RUN/ink-Regular.png" \
  --image Bold="$RUN/ink-Bold.png" \
  --fit <fit_band from the extract JSON — raw numbers, never zone guesses> \
  --preserve-existing-metrics \
  --fail-on-low-confidence \
  --report "$RUN/report.json"
```

  Use each master's own `fit_band` from its extract output; remember round
  forms overshoot 16.
- Read `report.json`. Require `compatible: true`, no `lowConfidence`; check
  per-master `points`, `bounds`, warnings. Bad trace → adjust flags
  (`--profile`, `--mode`, `--corner-threshold`) or regenerate; do not
  hand-fix a bad trace.

### 5. Adjust per DESIGN.md

Read the traced glifs from `$RUN/trace/…ufo/glyphs/` and correct against
`DESIGN.md`, keeping both masters structurally identical:

- Snap near-metric on-curve points exactly to baseline/x-height/cap
  (± overshoot 16 for curves), near-H/V lines exactly axial, near-45°
  chamfer segments exactly 45°.
- All coordinates even (grid 2); key measurements onto the power-of-two
  ladder (2, 4, 8, 16, 32, 64, 96, 128, 160 …) where the shape allows.
- Chamfers: every sharp straight-straight corner gets the 16-unit bevel
  (scaled up in Bold). Curves: on-curve extrema with on-axis handles.
- **Normalize the weight — measured, not eyeballed.** Measure perpendicular
  distance between parallel edges of a representative stem. If off the
  master's ladder (~96 R / ~160+ B) by more than ~4 units, correct it:
  offset the contours by half the difference (this font is monolinear and
  gains weight inward — thicken toward the counters, keep the outer
  silhouette where DESIGN.md says it stays). Re-measure after.

Verify numerically after adjusting (and again after porting, per master):

```sh
./.venv/bin/python harness/canvas.py check --glyph <name> --master Regular
```

It reports yMin/yMax with the nearest metric zones, LSB/RSB, and the count
of odd coordinates — every number should be explainable before you move on.

### 6. Space it (sidebearings — do not skip)

`--preserve-existing-metrics` keeps the *advance width*, not the spacing.
Set spacing deliberately, by analogy:

- Pick 2–3 structurally similar **green** glyphs (round → `o`/`O`/`zero`,
  flat-sided → `n`/`H`) and read their LSB/RSB as the target range.
- Set LSB and RSB on the power-of-two ladder (multiples of 8 typical);
  round forms fit tighter. Advance = `LSB + outline width + RSB` — never
  leave the outline touching the advance box edges. Both masters (Bold
  slightly tighter).

### 7. Render and look (designbot, dark mode)

Render `$RUN/review-<master>.png` for the human: the adjusted glyph **with
its metrics drawn** (advance-box sides, baseline, x-height, cap) plus 3–4
green-marked reference glyphs at the same scale with their real advances.
Draw all guide lines in **bright green `#18b86f`** (the Runebender palette
green) — clearly distinct from the light-gray glyph ink, never the same
color as the letterforms. Human-facing
style: **dark mode — dark gray background (~#202020–#2a2a2a), light gray ink
(~#c8c8c8–#e6e6e6), never pure black on white**; Swiss / International
Typographic Style layout (modular grid, flush-left, generous margins, no
decoration). Iterate steps 5–6 until shape, weight, and spacing sit right.

### 8. Port into the real sources (repo style)

a. Write the final outlines into
   `sources/VirtuaGrotesk-{Regular,Bold}.ufo/glyphs/<name>.glif` as
   repo-style XML, preserving the file's `advance` (as updated in step 6),
   `unicode`, and lib structure. Write atomically (temp file + rename) — the
   Runebender server may be watching.
b. **Only if the glyph is new**: register it in three places per master —
   `glyphs/contents.plist`, `public.glyphOrder` in `lib.plist`, and the glif
   file itself. Edit the plists surgically, matching existing tab formatting.

### 9. Mark colors (the human's control channel)

- Both masters traced from real per-master generations → **blue**
  `0.27,0.44,1,1` ("AI output, awaiting grading").
- A Bold that is only a structure copy / placeholder → keep/set **red**
  `1,0.29,0.24,1`.
- Never set green — only the human promotes to green.

### 10. Verify

```sh
make build      # must succeed
make reports    # then check documentation/source/master-compatibility.md
```

Verify the **built** font: confirm cmap and advance width in the TTF; render
a word context (e.g. `A@B name@example.com`) from `fonts/variable/*.ttf` with
designbot at both weight extremes, dark-mode style, to `$RUN/` — weight and
spacing must match the neighbors. `make test` must show no new FAILs
(pre-existing excludes: `scripts/check_gf_fonts.sh`).

### 11. Report and stop

One glyph per run. Summarize: generation attempts and what each gate
measured, what you adjusted and which DESIGN.md rule justified it, the
report.json gates, and the review image paths. Commit only if asked; plain
message. The human grades the blue glyph in Runebender (`make runebender`) —
their color change is the verdict, and the next run re-reads it.
