# AI Font-Completion Harness — Plan & Research

2026-07-06. The plan for getting Virtua Grotesk 100% Google Fonts-ready with an
agentic completion loop, and for making that loop a **portable template** that
can be dropped into any future font repo.

**The bigger picture: this is one unified project, not five repos.** img2bez
(tracer), img2ufo (bootstrap/assembler), designbot (renderer), the Codex
goal-mode + OpenAI image API (perception), and this repo's harness
(orchestration) are components of a single system whose demo deliverable is
**Virtua Grotesk shipped to Google Fonts** — proof that the pipeline produces
a high-quality font to the GF standard. Work on any component counts as work
on the project; contracts between components (the worklist schema, the
mark-color protocol, the design-doc format, the img2bez JSON report) matter
more than any single repo's internals, because they are what let the pieces
evolve in parallel.

**The design contract lives at the repo root: [`DESIGN.md`](../DESIGN.md).**
It states the power-of-two grid system (UPM 1024, grid 2, measurements on the
2/4/8/16/32/64 ladder, 16-unit chamfers, optical corrections allowed),
inspired by Replica's grid discipline. Every pipeline stage consumes it:
image prompts quote it, place/snap enforces it, review gates check it, humans
grade against it. A per-font `DESIGN.md` is part of the template — porting the
harness to a new font means writing that font's `DESIGN.md` first.

## 0. Rollout: crawl → walk → auto

We do **not** start with an autonomous loop. The system earns autonomy:

1. **Crawl (now): one glyph at a time, Regular-first.** Run the pipeline
   manually end-to-end on single glyphs; tune prompts, thresholds, snapping,
   and the DESIGN.md language after every run. Quality bar is the **Regular
   master** — once a few Regular generations come out good, Eli does a
   Runebender grading pass (update colors, improve Bold) before widening.
   For Bold during this phase: joint-trace both masters when the Bold image
   is usable; otherwise trace Regular and write a structure-identical copy
   into Bold marked **red** (keeps the variable build compatible, flags the
   Bold as to-do).
2. **Walk: small batches.** 3–5 glyphs per session via `loop --limit N`,
   Codex GUI driving generation, human grading between sessions.
3. **Auto: Codex goal mode.** Point Codex's /goal at `RUNBOOK-codex.md` and
   let it grind the queue unattended, with the STOP file and mark colors as
   the human controls. Only after the walk phase shows a high accept rate.

Division of labor, per the project owner's direction:

- **Claude (Anthropic)** — plans, builds, and documents the harness (this doc,
  the Python driver, the prompts, the runbook, tool fixes).
- **Codex + OpenAI image API** — executes the loop: generates glyph reference
  images, runs the deterministic pipeline steps, grinds until done.
- **Human (Eli)** — steers with mark colors in Runebender: can stop the loop at
  any time, re-grade glyphs (green/yellow/orange/red), and resume.

---

## 1. Framing: how a top-lab engineer would build this

Strip away the font specifics and this is a classic **agent + environment +
verifier** system. The design principles that follow from that:

1. **The environment is deterministic; the model is only perception.**
   Everything that can be code, is code: tracing (img2bez), placement, metrics,
   plist registration, builds, QA. The generative model touches exactly two
   surfaces — producing raster reference images, and (optionally, bounded)
   visual judgment. This is img2bez's stated principle ("generative models
   assist perception, deterministic code decides geometry") and it is what
   makes the loop debuggable.

2. **The proposer never grades its own work.** Acceptance is decided by
   machine-checkable gates (compatibility report, raster IoU, Fontspector,
   structural sanity vs. green-glyph statistics) plus the asynchronous human
   gate (mark colors). The agent's output enters the sources in a *quarantine
   color* (blue), never as green.

3. **State is derived, not cached.** Every loop iteration re-derives the work
   queue from the source of truth: the UFOs' mark colors + the glyphset diff.
   There is no state file that can go stale when the human re-grades glyphs in
   Runebender mid-run. Stop the loop, repaint colors, restart — the queue is
   simply recomputed. (A small ledger records *attempt history* per glyph so
   the loop doesn't thrash on a hopeless target, but it never overrides the
   colors.)

4. **Human labels are the reward signal, and they're cheap to give.** The
   green→red gradient in Runebender is an RLHF-style label stream. The harness
   must (a) never overwrite green, (b) surface its own output for grading
   (blue), and (c) log every trace (`IMG2BEZ_LOG`) so accepted/rejected runs
   accumulate into training data for img2bez's input-adaptive selector — the
   grind itself improves the tools.

5. **Everything observable, everything resumable.** Per-glyph run packets on
   disk, one JSONL event log, a `status` command that prints the whole burn-down
   (color counts, coverage %, Fontspector excludes remaining). Crash or Ctrl-C
   anywhere and the next `loop` invocation picks up cleanly.

6. **Verifiable definition of done.** Not vibes: **zero excludes in
   `scripts/check_gf_fonts.sh` + `make test` clean + `METADATA.pb` + the
   google/fonts PR**. The exclude list is the burn-down chart
   (`documentation/google-fonts-readiness.md` already establishes this).

---

## 2. Research digest (compiled 2026-07-06)

### 2.1 This repo — what already exists

`scripts/glyph_ai_harness.py` (639 lines) + `.agents/skills/glyph-ai-harness/SKILL.md`
already implement the *front half* of the loop:

| Stage | Status |
|---|---|
| `inventory` — classify every glyph by `public.markColor` in both masters | **working** |
| `render` — glyph → PNG via drawbot-skia (1536px canvas, 224 padding) | **working** |
| `prepare` — run packet: green reference renders + prompt briefs + `trace-commands.sh` | **working** |
| `trace` — copies master UFO to scratch, shells out to `img2bez` (single-master), runs compat report | **working but outdated** (should use `img2bez masters`) |
| `generate` (OpenAI call), `place`, `specimen`, `review`, `promote`, `plan --script` | **missing — documentation only** |

The workflow contract lives in `documentation/glyph-ai-harness-workflow.md`
(8 phases); `documentation/glyph-ai-harness-dalet-test.md` records the first
successful end-to-end run (Hebrew dalet, U+05D3, promoted to both masters,
`make test` clean) and its 7 bug findings — most importantly: placement/scaling
is mandatory (raw traces land wrong), raster cleanup to exact H/V/45° is
mandatory, and run packets must live in `.glyph-ai-runs/` (git-ignored, not
wiped by builds).

Current classification bug: the script lumps **yellow** (`1,0.86,0.2,1`) in
with orange, losing a rung of the human's quality gradient. Fix in Phase 1.

**GF readiness state** (`documentation/google-fonts-readiness.md` +
`scripts/check_gf_fonts.sh`): GF Latin Core is complete (319/319), masters
interpolate, kerning and Arabic shaping are done. The exclude list is down to
**four** (three Arabic outline checks were just cleared — the readiness doc is
stale and says four Arabic excludes remain; only `outline_alignment_miss`
does):

1. `googlefonts/repo/dirname_matches_nameid_1` — local naming, clears at packaging
2. `outline_alignment_miss` — ~16 Arabic glyphs with points 1–2.5 units off baseline (bulk-snap job)
3. `googlefonts/glyphsets/shape_languages` — Latin anchor/composite coverage pass
4. `googlefonts/metadata/unreachable_subsetting` — clears with real `METADATA.pb`

Plus a known FAIL: `whitespace_widths` (`space`=200 vs `nbspace`=256 — must be
equal), and 4 Arabic `contour_count` glyphs (uni062C.fina, uni062D.fina,
uni0635.init, uni0636.init). **Honest scope check: most of the remaining
distance to GF is *fixing marked-red/orange existing glyphs* and deterministic
cleanup, not filling missing glyphs** — the harness must handle "redraw red
glyph" as a first-class target type, not just "missing glyph."

**Mark-color ground truth** (Regular master, today): 53 green, 17 orange,
85 red (two red values — see 2.4), 0 yellow. `glyphsets 1.1.0`, `gflanguages`,
and `shaperglot` are already in `.venv`, so glyphset-diff enumeration of
missing glyphs is a solved dependency. Codex CLI is installed
(`/opt/homebrew/bin/codex`) and reads `AGENTS.md` / `~/.codex/AGENTS.md`.

### 2.2 img2bez (`~/GH/repos/img2bez`) — the tracer, in good shape

- **`img2bez masters <designspace> --glyph X --image Regular=a.png --image
  Bold=b.png --fit descender:cap --report r.json`** is the headless contract we
  need: it traces the master set **jointly** (one structural plan fitted to
  each master → interpolation-compatible by construction), falls back to
  `compat::make_compatible` reconciliation when topology diverges, and reports
  `compatible` / `lowConfidence` / `insertedPoints` / per-master `outOfTarget`,
  `profile`, `sharpness`, `bilevelness`, `points`, `advance`, `bounds`.
  `--fail-on-low-confidence` gives a clean regenerate-or-accept exit code.
  `--format json` returns the reconciled outlines *without writing UFOs*.
- **Critical constraint: img2bez writes UFOs through norad `font.save()`**,
  which (a) rewrites the whole UFO in norad's serialization style — exactly the
  formatting-noise footgun this repo's CLAUDE.md forbids — and (b) never
  touches `public.glyphOrder`. **Decision: the harness consumes
  `masters --format json` and writes `.glif` XML itself in repo-native style**
  (tabs, attr order `x,y,type,smooth`), registering in `contents.plist` +
  `lib.plist` surgically. img2bez stays a pure tracer; no img2bez change needed.
- `img2bez stats` gives no-reference image QC (sharpness, bilevelness, noise,
  extent) — use it to reject bad generated images *before* tracing.
- `IMG2BEZ_LOG` (JSONL: image features + settings + output per trace) is the
  training-data hopper for the input-adaptive selector; the selector itself is
  minimal today (photo-vs-wild pre-blur trigger only), so the harness passes
  `--profile` explicitly and logs everything. `eval-harness/tracelog.py` gauges
  readiness (wants ≥80 unique images, ≥20 photo-class).
- Known tracer limitations that matter here: corners sit ~+0.4 units inside
  ink; gentle bowing can flatten to lines; long shallow diagonals
  over-segment. All survivable with the review gate; none blocks the loop.
- img2bez is already coupled to this font: `eval-harness/reference.ufo`
  symlinks to `sources/VirtuaGrotesk-Regular.ufo` and recent site-head training
  used Virtua Grotesk chamfers.

### 2.3 img2ufo + designbot — roles and needed work

**img2ufo** (`~/GH/repos/img2ufo`) is the *bootstrap* tool — specimen scan →
whole UFO + GF repo scaffold ("one image in, one UFO out"), wrapping img2bez as
a library and adding segmentation (img2glyph), auto-composition (~140 Latin
composites from anchors), GF Latin Core accounting, fontc compile, and a
Fontspector gate. **For Virtua Grotesk it is not on the critical path** (this
repo already has its build); it *is* the template story for future fonts.
Its `docs/glyph-completion-harness.md` (2026-07-05) already specifies the
completion contract — worklist JSON with `missing_marks` sorted by unlock
count, `missing_atomic`, a mark-color rebuild-safety protocol, and "Codex
desktop + OpenAI image API" named as the intended agent. **This repo's harness
should implement the same worklist schema and color protocol** so the two
converge into one system.

img2ufo work items (owner: Claude, as we go): (1) **stale img2bez pin** —
`Cargo.toml` pins rev `2eed2fa`, 36 commits behind HEAD, with a "switch back
when HEAD builds" note; (2) README flag-table drift vs `main.rs`; (3)
`spacing.rs` is placeholder-honest, kerning deferred (acknowledged, not a bug);
(4) its harness doc's color semantics differ from ours (see 2.4) — unify.

**designbot** (`~/GH/repos/designbot`) is a Rust DrawBot-style renderer
(vello_cpu/Parley/Swash), *not* an image-generation tool. It has variable-font
axis control, custom font loading, and image compositing — the natural renderer
for reference-vs-render comparison sheets eventually. **But this repo's
standard is drawbot-skia** (CLAUDE.md), and the existing render code works.
Decision: **drawbot-skia stays the renderer for this harness**; designbot is a
future swap once it renders side-by-side sheets better (tracked, not blocking).

### 2.4 Runebender-web — mark colors and live-edit safety

The web picker offers exactly seven colors (`src/themeTokens.ts`), stored
verbatim as `public.markColor` in the glif lib:

| name | UFO rgba | hex |
|--------|------------------|---------|
| red | `1,0.29,0.24,1` | #ff4a3d |
| orange | `1,0.6,0.06,1` | #ff980f |
| yellow | `1,0.86,0.2,1` | #ffdc32 |
| green | `0.09,0.72,0.44,1` | #18b86f |
| blue | `0.27,0.44,1,1` | #456fff |
| purple | `0.55,0.42,1,1` | #8c6cff |
| pink | `0.91,0.42,0.72,1` | #e86ab8 |

The `1,0.3,0.3,1` red on 60 glyphs is a **legacy value** from the old
xilem/native palette (`runebender-core/src/mark_color.rs` `PRESET_UFO_RGBA`) —
the harness must treat both reds as red (the current inventory code already
does).

**Concurrent editing is safe by design.** `runebender-serve` (the workspace
server) content-hashes its own writes, watches the tree with a 200ms debounce,
broadcasts external changes over SSE for live reload, and guards saves with
ETags — a stale editor gets a 409 instead of clobbering a harness write, and
vice versa. The one requirement on the harness: **write files atomically**
(write-temp-then-rename or single write-then-close; never leave a `.glif` half
written). This is what makes "stop the loop, repaint colors, resume" work with
the editor open the whole time.

### 2.5 OpenAI image generation (the Codex side)

From the workflow doc's research + the img2ufo contract: use the image API's
**reference-image mode** (`images.edit` / Responses API image generation with
input images) — feed 6–10 rendered green glyphs *of the same master* as style
references plus a text brief (glyph name, codepoint, weight, metric
proportions). Black ink on white, one glyph, generous margins, no transparency
(the API composites on black otherwise), render large (~1024–1536px) since
placement is metric-driven, not pixel-driven. Per-master generation: one image
for Regular, one for Bold, same prompt scaffold with weight language swapped.
The gpt-image models handle style transfer from references well; the dalet test
confirmed a usable skeleton on the first real attempt.

---

## 3. The mark-color protocol (canonical for this repo + the template)

Human semantics (Eli's grading system) take precedence; harness colors extend
it without collision:

| color | who sets it | meaning | harness behavior |
|---------|---------|-----------------------------------------|------------------------------------|
| green | human | done; design authority | **frozen** — never modified; used as style reference |
| yellow | human | almost done — minor polish | polish tier: bounded deterministic edits only (snap, sidebearings); never regenerated |
| orange | human | almost done — needs more work than yellow | same as yellow (lower confidence) |
| red | human | broken — restart from scratch | **regeneration target**: full generate→trace→place, replaces outline |
| *(none)* | — | ignore | untouched (unless it's in the glyphset diff as *missing* — then it doesn't exist yet) |
| blue | **harness** | AI-generated, awaiting human grading | quarantine: the only color the harness writes; human promotes to green or demotes |
| purple | human (opt) | do-not-touch override (e.g. PUA icons) | excluded from every queue |
| pink | — | reserved | — |

Targets, in priority order: (1) **missing** glyphs required by the target
glyphsets, sorted by unlock count (composites they enable) and script priority;
(2) **red** glyphs (regenerate); (3) **yellow/orange** (deterministic polish
proposals only — these stay human-led). Blue glyphs are *output*, re-queued
only if the human repaints them red.

Divergence to reconcile in img2ufo's doc: it uses green=preserved /
red=traced / yellow=auto-composite / orange=derived, and an old green value
(`0.3,0.7,0.3,1`). Unify both repos on **this table + the web palette values**
(owner: Claude, Phase 8).

---

## 4. The per-glyph pipeline (one loop iteration)

```
┌─ plan ──── derive queue: glyphset diff (glyphsets pkg) ∪ red glyphs,
│            minus purple/green/blue, sorted by unlock count → queue.json (ephemeral)
├─ prepare ─ run packet in .glyph-ai-runs/<glyph>/:
│            reference sheet PNGs per master (green glyphs, drawbot-skia),
│            prompt.md per master, manifest.json (name, unicode, fit band,
│            per-master widths, references used)
├─ generate  [CODEX + OpenAI image API] one grayscale PNG per master →
│            generated/<master>.png  (the ONLY generative step)
├─ inspect ─ img2bez stats on each PNG: reject on low sharpness/extent/
│            bilevelness → retry generate (≤N attempts, logged)
├─ trace ── img2bez masters <designspace> --glyph X --image ... --fit <band>
│            --format json --report → reconciled outlines, never writes UFOs
│            gates: compatible==true, lowConfidence==false (else retry)
├─ place ── deterministic: scale to fit band, snap to grid 2, snap
│            near-baseline/H/V/45° (the dalet-test lesson), sidebearings from
│            reference stats or --preserve-existing-metrics for red targets
├─ write ── repo-style .glif writer (tabs, x,y,type,smooth attr order) into
│            BOTH masters + surgical contents.plist/lib.plist registration +
│            public.markColor = blue; atomic writes (Runebender live-reloads)
├─ verify ── make build → fontTools/uharfbuzz checks on built font,
│            raster IoU: built-glyph render vs generated PNG ≥ threshold,
│            point-count sanity vs green-glyph distribution,
│            compat report, no new Fontspector FAILs
├─ review ── mixed specimen (new glyph inline with green neighbors);
│            [CODEX vision, bounded] optional JSON verdict: accept | adjust
│            {scale, translate, lsb, rsb} | reject — never free-form edits
└─ commit ── git commit on the harness branch, one commit per accepted glyph;
             rejected → log attempt, re-queue or park after N failures
```

Stop/resume: the loop re-derives the queue every iteration and honors a
`.glyph-ai-runs/STOP` file + Ctrl-C. Human repaints colors in Runebender at any
time (server handles concurrency); next iteration sees the new labels.

Deterministic-only track (no image gen needed, runs before/alongside the loop):
baseline snapping for `outline_alignment_miss`, the `whitespace_widths` fix,
`shape_languages` anchor/composite work, the 4 `contour_count` glyphs. These
are ordinary Claude/Codex code-and-glif tasks gated by `make test`.

---

## 5. Harness layout (portable template)

Everything the loop needs lives in two places — repo-agnostic code under
`harness/`, repo-specific facts in one config file:

```
harness/
  config.yaml          # THE portability seam — see below
  font_harness.py      # CLI: plan | status | prepare | inspect | trace |
                       #      place | write | verify | review | promote | loop
  glif_writer.py       # repo-style .glif XML + plist registration (atomic)
  prompts/             # image-gen prompt templates (per script, per master)
  RUNBOOK-codex.md     # the Codex operating contract (§6)
.glyph-ai-runs/        # git-ignored run packets + events.jsonl + STOP file
```

`config.yaml` carries: designspace path, master names/styles, metric zones
(UPM 1024, asc 832, cap 768, xh 576, desc −256, grid 2), the path to the
font's `DESIGN.md` (prompt templates interpolate it), mark-palette values +
semantics table, target glyphsets (`GF_Latin_Core` done; Arabic set per
readiness doc), fit-band defaults per script, IoU/stats thresholds, retry
budget, `IMG2BEZ_LOG` path, and the QA command (`make test`). **Porting to a
new font = copy `harness/`, write the font's `DESIGN.md`, edit
`config.yaml`.** For brand-new fonts, img2ufo
bootstraps the repo first (it already names virtua-grotesk as its output
template), then this harness takes over for completion — same worklist schema,
same color protocol.

Migration note: `scripts/glyph_ai_harness.py`'s working pieces (inventory,
mark parsing, drawbot render, packet prep) move into `harness/font_harness.py`;
the old script and Make targets get thin deprecation shims or are re-pointed.

## 6. The Codex execution contract (RUNBOOK-codex.md, sketch)

The runbook is written so you can point the Codex GUI at the repo with one
standing instruction, roughly:

> Read `harness/RUNBOOK-codex.md`. Run `./.venv/bin/python
> harness/font_harness.py loop` and follow its instructions. When the loop
> pauses at a `generate` step, produce the requested images with the OpenAI
> image API using the reference sheet and prompt in the run packet, save them
> to the named paths, and resume. Never edit green glyphs. Stop when the queue
> is empty or `.glyph-ai-runs/STOP` exists.

Contract points the runbook spells out: the harness drives, Codex fills the
two perception holes (image gen, bounded vision review); all writes go through
`font_harness.py write` (never hand-edit plists); every accepted glyph is blue;
commit messages are plain (no AI credits — repo rule); `make test` is the gate
before any batch ends; the queue is re-derived, so human color edits between
sessions are automatically respected. A section of `AGENTS.md` will point to
the runbook so Codex discovers it natively.

## 7. Acceptance gates (numeric, initial values — tune during dry runs)

| gate | threshold | source |
|---|---|---|
| trace compatibility | `compatible == true` | img2bez masters report |
| correspondence confidence | `lowConfidence == false` (1 retry allowed) | report |
| fit | `outOfTarget == false` per master | report |
| image QC | sharpness ≥ 80, bilevelness ≥ 0.9, extent sane | `img2bez stats` |
| raster fidelity | IoU(built render, generated PNG) ≥ 0.90 | harness verify |
| structure sanity | point count within ~2σ of green-glyph distribution for the script | inventory stats |
| build | `make build` succeeds; widths/cmap verified via fontTools | repo gate |
| QA | no new Fontspector FAILs vs. baseline run | `check_gf_fonts.sh` |
| retry budget | 3 generate attempts per glyph per session, then park | ledger |

---

## 8. Risks / open questions

- **Arabic generation quality** — only 53 green refs exist in Regular and few
  in Bold, mostly Latin. Arabic red-glyph regeneration may need script-specific
  reference sheets and prompts; the dry run must include one Arabic glyph
  early. Fallback: Arabic stays a deterministic-cleanup + human track while the
  loop grinds Latin/Hebrew.
- **Bold reference scarcity** (dalet-test finding #3) — resolved by the
  rollout plan: crawl phase is Regular-first; when a Bold image is weak, fall
  back to a structure-identical copy of the Regular outline written into Bold
  and marked red. Eli improves Bold + regrades colors once Regular runs look
  good, which also grows the Bold green-reference pool for later batches.
- **Chamfer fidelity** — the 16-unit chamfer is the brand; the review gate must
  check corners specifically (img2bez's known +0.4-unit corner bias, and
  `--chamfer` only applies to line-based forms).
- **Two stale docs** contradict reality today (readiness doc's exclude list;
  `documentation/source-guides/ai-glyph-harness.md` old paths) — fix in Phase 0
  so Codex never reads stale contracts.
- **Branch strategy** — default decision: crawl-phase single-glyph runs can
  land on `main` directly (each is human-reviewed immediately); walk/auto
  phases run on an `ai-harness` branch, one commit per accepted glyph, merged
  after grading sessions.
- **Yellow/orange polish tier** — kept deterministic-only in v1 (no
  regeneration) so the human gradient stays meaningful. Revisit if polish
  stalls.

---

## 9. The checklist

Owners: **[C]** Claude builds it now · **[X]** Codex executes in the loop ·
**[H]** human. Work top to bottom; each phase ends in a verifiable state.

### Phase 0 — Ground truth cleanup (make the repo honest before automating)
- [x] [C] Write `DESIGN.md` at the repo root — the power-of-two grid / chamfer design contract every pipeline stage consumes
- [ ] [H] Commit or stash the current WIP (Arabic outline cleanup, Hebrew glyphs, harness edits) so the harness branch starts clean
- [ ] [C] Update `documentation/google-fonts-readiness.md` to the real exclude list (4, not 7) and current worklist
- [ ] [C] Fix or delete the stale `documentation/source-guides/ai-glyph-harness.md` (old `build/` paths)
- [ ] [C] Add yellow (`1,0.86,0.2,1`) as its own class in inventory; classify all 7 palette colors + legacy red distinctly
- [ ] [H] Grading pass in Runebender: confirm every glyph's color reflects current truth (85 reds especially)

### Phase 1 — Harness core [C]
- [ ] Scaffold `harness/` + `config.yaml` (metrics, palette, glyphsets, thresholds) — the portability seam
- [ ] `plan`: queue = glyphset diff (via `glyphsets` pkg) ∪ red glyphs − green/blue/purple, unlock-count sorted, per-script priorities
- [ ] `status`: burn-down dashboard — color counts per master, coverage %, excludes remaining, parked glyphs
- [ ] Port inventory/render/prepare from `scripts/glyph_ai_harness.py`; per-master widths in manifest; unicode inference for new glyphs (dalet bugs #1, #2)
- [ ] Attempt ledger + `STOP` file + events.jsonl

### Phase 2 — Generation packet [C builds, X uses]
- [ ] Reference-sheet renderer: N green glyphs per master on one labeled sheet (style refs for the image API)
- [ ] Prompt templates per script × master (weight language for Bold; Arabic-specific variants)
- [ ] `inspect`: `img2bez stats` QC gate on generated PNGs with retry messaging
- [ ] Optional `generate --api`: direct OpenAI images call when a key is present (so the loop can also run keyed, not only via Codex GUI)

### Phase 3 — Trace, place, write [C]
- [ ] Switch tracing to `img2bez masters --format json --report` (joint-trace both masters; drop the single-master path)
- [ ] `place`: fit-band scaling, grid-2 snap, near-H/V/45° + baseline snapping (dalet bugs #5, #6)
- [ ] `glif_writer.py`: repo-native glif XML + surgical `contents.plist`/`lib.plist` registration, atomic writes, `markColor` = blue
- [ ] `verify`: build + fontTools/uharfbuzz checks + raster IoU + point-count sanity + no-new-FAILs vs baseline
- [ ] Wire `IMG2BEZ_LOG` into every trace (the training-data hopper)

### Phase 4 — Review loop [C builds, X runs]
- [ ] Mixed-specimen render (target inline with green neighbors, both masters)
- [ ] Bounded vision-review schema: `accept | adjust{scale,translate,lsb,rsb} | reject` JSON only
- [ ] `loop` orchestrator: plan → … → commit, one commit per accepted glyph on the `ai-harness` branch, pause-at-generate mode for Codex GUI

### Phase 5 — Codex handoff (crawl → walk → auto)
- [x] [C] Write `harness/RUNBOOK-codex.md` (crawl-phase version: one glyph from a reference image) + AGENTS.md pointer section — extend for walk/auto later
- [ ] [C] Make targets: `make harness-status`, `make harness-next` (one glyph), `make harness-loop`
- [ ] [C+H] **Crawl**: single-glyph Regular-first runs (start Latin, then one Arabic probe); tune prompts / thresholds / DESIGN.md language after each until results are consistently good
- [ ] [H] Grading checkpoint: update mark colors in Runebender, improve Bold drawings for the accepted glyphs
- [ ] [X+H] **Walk**: `loop --limit 3..5` batches, Codex GUI generating, human grading between sessions; track accept rate in `status`
- [ ] [X] **Auto**: Codex /goal grinds the queue unattended; [H] periodic Runebender grading sessions (blue → green/red); STOP file + colors are the controls

### Phase 6 — Deterministic GF cleanup (parallel track, no image gen)
- [ ] [C/X] `whitespace_widths` FAIL: make `space` and `nbspace` widths equal
- [ ] [C/X] Bulk baseline-snap the ~16 `outline_alignment_miss` Arabic glyphs → remove exclude
- [ ] [C/X] Fix 4 Arabic `contour_count` glyphs (uni062C.fina, uni062D.fina, uni0635.init, uni0636.init)
- [ ] [C/X] `shape_languages`: mark anchors over ogonek/dotaccent, breve/macron composites → remove exclude
- [ ] [H] Kerning sign-off per core-qa-process (source decision recorded, `gftools qa --proof` reviewed)

### Phase 7 — Package & submit
- [ ] [C] `/google-fonts-packaging`: `METADATA.pb` + `ofl/virtuagrotesk/` → removes `unreachable_subsetting` + `dirname_matches_nameid_1` excludes
- [ ] [C] **Zero excludes in `check_gf_fonts.sh`, `make test` clean** ← the definition of done
- [ ] [H] Human/legal gates: family name, copyright, upstream URL, designer metadata
- [ ] [C+H] google/fonts PR via `/google-fonts-onboarding`

### Phase 8 — Templateization & tool debt (as we go / after)
- [ ] [C] img2ufo: bump the stale img2bez pin (rev `2eed2fa` → HEAD), fix README↔CLI drift
- [ ] [C] Unify the mark-color protocol across this doc and `img2ufo/docs/glyph-completion-harness.md` (this table wins; web-palette values)
- [ ] [C] Align worklist JSON schema with img2ufo's `<Family>-<Style>-completion.json`
- [ ] [C] Document the port procedure: img2ufo bootstrap → copy `harness/` → edit `config.yaml` → point Codex at RUNBOOK
- [ ] [C] Evaluate designbot as the comparison-sheet renderer (side-by-side ref-vs-render); swap only if it beats drawbot-skia here
- [ ] [C] Feed the accumulated `IMG2BEZ_LOG` corpus to img2bez's input-adaptive selector work (needs ≥80 unique images; the grind supplies them)
