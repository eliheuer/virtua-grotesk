# RUNBOOK — AI glyph completion (crawl phase)

Operating contract for a coding agent (Codex, Claude, or other) adding or
regenerating **one glyph at a time** in this repo. The full system plan is
`plans/ai-font-completion-harness.md`; the design contract every glyph must
obey is the root **`DESIGN.md`**. Read both before your first glyph.

Crawl-phase scope: single glyphs, Regular master quality first, a human
reviews every result. Do not batch, do not loop, do not touch glyphs you were
not asked about.

## Context you must load

1. `DESIGN.md` — the power-of-two grid, 16-unit chamfers, metrics, curve and
   spacing rules. Every adjustment you make is justified by this file.
2. `AGENTS.md` — repo conventions, especially the source-editing footguns.
3. `plans/ai-font-completion-harness.md` §3 — the mark-color protocol.

Hard rules (repeated from those files because agents skip links):

- **Never modify a green glyph** (`public.markColor` = `0.09,0.72,0.44,1`).
- **Never save the real UFOs through a font library** (defcon/ufoLib/norad
  `font.save()`). It reformats thousands of lines. Write `.glif` XML directly
  in repo style: tabs for indentation, double-quoted attributes, no space
  before `/>`, attribute order `x`, `y`, `type`, `smooth`.
- Both masters must keep **identical contour/point structure** per glyph.
- Use `./.venv/bin/python` for all Python.
- Plain commit messages; no AI credit trailers.
- Work goes in `.glyph-ai-runs/<glyph>/` (git-ignored). Never in `build/`.

## Environment setup (once per session)

```sh
export IMG2BEZ_LOG="$HOME/.img2bez/virtua-grotesk-traces.jsonl"
```

`img2bez` is on PATH (`~/.cargo/bin/img2bez`). Check `img2bez masters --help`
— it is authoritative over any flag list written here.

## The procedure: one glyph from a reference image

Inputs: a glyph name (e.g. `at`), and one or more reference images supplied
by the human (black ink on white, one glyph, generous margins; bigger is
better, ~1024px+). If you were asked to *generate* the image instead, use the
OpenAI image API with rendered green glyphs as style references and a prompt
built from `DESIGN.md`'s "Identity" and "What the AI pipeline takes" sections
— then continue identically.

### 1. Inspect the target

- Read `sources/VirtuaGrotesk-{Regular,Bold}.ufo/glyphs/<name>.glif` if it
  exists: note `public.markColor`, advance width, unicode, and the outline's
  y-range (you need it for the fit band). Red = replace the outline, keep the
  metrics. Missing = you must also register it (step 5b).
- If the existing glyph is green: stop and report — wrong target.

### 2. Trace on a scratch copy (never the real sources)

`img2bez masters` in UFO mode writes through norad, which reformats files —
so it must never point at `sources/`. Copy first:

```sh
RUN=.glyph-ai-runs/<name>
mkdir -p "$RUN/trace"
cp -R sources/VirtuaGrotesk.designspace \
      sources/VirtuaGrotesk-Regular.ufo \
      sources/VirtuaGrotesk-Bold.ufo "$RUN/trace/"

img2bez masters "$RUN/trace/VirtuaGrotesk.designspace" \
  --glyph <name> --unicode <HEX> \
  --image Regular=<regular-image> \
  --image Bold=<bold-image> \
  --fit <zone-or-number:zone-or-number> \
  --preserve-existing-metrics \
  --fail-on-low-confidence \
  --report "$RUN/report.json"
```

- Fit band: match the existing glyph's y-range, or the DESIGN.md zone the
  form belongs to (zones: `descender`, `baseline`, `xheight`, `cap`,
  `ascender`, or raw numbers). Remember round forms overshoot 16 units.
- **Only one image supplied?** Pass the same image for both masters. The
  joint trace then yields identical, compatible outlines; the Bold stays a
  placeholder (see step 6 for its color).
- Read `report.json` before proceeding. Require `compatible: true` and no
  `lowConfidence`; check per-master `points`, `bounds`, `outOfTarget`,
  warnings. Bad trace → adjust image or flags (`--profile`, `--mode`,
  `--corner-threshold`) and re-run; do not hand-fix a bad trace.

### 3. Adjust per DESIGN.md

Read the traced glif from `$RUN/trace/…ufo/glyphs/<name>.glif` and correct it
against `DESIGN.md`, keeping both masters structurally identical:

- Snap near-metric on-curve points exactly to baseline/x-height/cap
  (± overshoot 16 for curves), near-H/V lines exactly axial, near-45° chamfer
  segments exactly 45°.
- All coordinates even (grid 2); pull key measurements onto the
  power-of-two ladder (2, 4, 8, 16, 32, 64, 96, 128, 160 …) where the shape
  allows; small optical deviations are fine.
- Chamfers: every sharp straight-straight corner gets the 16-unit bevel
  (scaled up in Bold). Curves: on-curve extrema with on-axis handles.
- Check stroke weight against the master's stem ladder (~96 Regular,
  ~160+ Bold).

### 4. Render and look

Write a short drawbot-skia script (`./.venv/bin/python`) that renders the
adjusted outline next to 3–4 green reference glyphs into
`$RUN/review-<master>.png`, and look at it. Iterate step 3 until it sits
right. This is the loop the human cares about — don't skip it.

### 5. Port into the real sources (repo style)

a. Write the final outline into
   `sources/VirtuaGrotesk-{Regular,Bold}.ufo/glyphs/<name>.glif` as repo-style
   XML (tabs; attr order `x`, `y`, `type`, `smooth`; no space before `/>`),
   preserving the existing `advance`, `unicode`, and lib structure of the file
   you are replacing. Write atomically (temp file + rename) — the Runebender
   server may be watching.
b. **Only if the glyph is new**: register it in three places per master —
   `glyphs/contents.plist`, `public.glyphOrder` in `lib.plist`, and the glif
   file itself. Edit the plists surgically, matching the existing tab
   formatting.

### 6. Mark colors (the human's control channel)

- Regular (and Bold if it was traced from a real bold image):
  `public.markColor` → **blue** `0.27,0.44,1,1` = "AI output, awaiting
  grading".
- Bold placeholder (same-image or copied structure): keep/set **red**
  `1,0.29,0.24,1` = still needs real bold ink.
- Never set green — only the human promotes to green.

### 7. Verify

```sh
make build      # must succeed
make reports    # then check documentation/source/master-compatibility.md
```

Then verify the **built** font, not just the source: with fontTools confirm
the cmap entry and advance width; render the glyph from
`fonts/variable/*.ttf` in a word context to `$RUN/` and look at it.
`make test` should show no new FAILs (pre-existing exclude list is in
`scripts/check_gf_fonts.sh`).

### 8. Report and stop

One glyph per run. Summarize: what was traced, what you adjusted and which
DESIGN.md rule justified each adjustment, the report.json gates, and the
review image paths. Commit only if asked; plain message. The human grades the
blue glyph in Runebender (`make runebender`) — their color change is the
verdict, and the next run re-reads it.
