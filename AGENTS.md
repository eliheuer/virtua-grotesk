# AGENTS.md

This file is the canonical guidance for AI coding agents (Claude Code, Codex,
etc.) working in this repository. `CLAUDE.md` imports this file and adds
Claude Code-specific notes — shared guidance belongs here, not there.

Agent skills live in `.agents/skills/` (one directory per skill with a
`SKILL.md`). `.claude/skills` is a symlink to that directory so Claude Code
picks them up — edit skills only in `.agents/skills/`.

## Mission & Map

**Goal: finish Virtua Grotesk and publish it to Google Fonts.** This repo is a
small AI-driven type studio — an agent (you) orchestrates the tools below to
draw, space, QA, and ship the font.

The phases and the tools for each:

- **Draw / fix glyphs** — `img2bez` traces from reference images (see "Adding
  Glyphs from Images"); Runebender (`make runebender`) is the visual review +
  live-edit surface. Skills: `/draw-outline`, `/edit-glyph`, `/compare-reference`,
  `/glyph-ai-harness`.
- **Space & kern** — per-glyph sidebearings in the UFOs; `/kerning`.
- **Build & QA** — `make build`, `make test` (the Fontspector `googlefonts`
  gate), `make proof` / `make specimen`, `make preflight`; skill `/font-qa`.
- **Package & submit** — `/google-fonts-packaging` (produces `METADATA.pb` + the
  `ofl/virtuagrotesk` layout), `/google-fonts-onboarding`, `/google-fonts-qa`.

**The finish line and current priorities live in
[`documentation/google-fonts-readiness.md`](documentation/google-fonts-readiness.md)
— read it first.** In short: the build, Latin, kerning, and the Arabic OpenType
shaping are done; what remains, in order, is (1) the **Arabic outline cleanup
pass** (top priority — the bulk of the work left), (2) Latin language-coverage
anchors, (3) `METADATA.pb` + packaging, (4) the `google/fonts` PR. Progress is
measured by the excludes in `scripts/check_gf_fonts.sh`: each one removed is a
step toward done, and **zero excludes = ready to submit.**

**Guardrails:** keep both masters structurally identical (master compatibility),
and never re-add a QA exclude to force a green `make test` — the excludes are the
to-do list, not a setting.

## Project Overview

Virtua Grotesk is an open-source variable font (OFL v1.1 licensed) with a Weight axis (wght 400–700). The sources are UFO files and the Google Fonts-ready build path uses `gftools builder sources/config.yaml`.

## Quick Start

```bash
/build-font             # Build all fonts (variable + static)
/proof                  # Generate PDF proof document
make specimen           # Generate landscape print spacing specimen
make reports            # Regenerate source/build metadata reports
make preflight          # Build, proof, specimen, reports, then check artifacts
make test               # Build, then run Fontspector googlefonts profile
/edit-glyph A           # Inspect/edit a glyph
make runebender         # Open the font in the Runebender web editor —
                        # edits to sources/ on disk live-reload in the
                        # browser; the user's Cmd+S saves back to disk
/kerning list           # View current kerning pairs
/compare-reference img  # Compare font to a reference image
```

## Font Metrics

| Metric | Value |
|--------|-------|
| Units per Em | 1024 |
| Ascender | 832 |
| Cap Height | 768 |
| x-Height | 576 |
| Descender | -256 |
| Grid Size | 2 (prefer even coordinates) |

## Build Commands

**Prerequisites:** Python virtual environment at `.venv/` with `pip install -r requirements.txt`.

```bash
make setup      # Create .venv and install requirements
make build      # Build variable and static TTFs into fonts/
make proof      # Build documentation/proofs/proof.pdf
make specimen   # Build documentation/proofs/print-spacing-specimen.pdf
make runebender # Open sources/VirtuaGrotesk.designspace in Runebender web
make reports    # Regenerate source/build metadata reports
make preflight  # Run the full local handoff gate
make test       # Build, then run Fontspector's googlefonts profile
```

Built fonts go to `fonts/variable/` and `fonts/ttf/` (gitignored). `build/` and `sources/instance_ufos/` are generated build outputs.

## Runebender Web Editing

Use `make runebender` to open `sources/VirtuaGrotesk.designspace` in the local
Runebender web editor. The target runs:

```bash
runebender-serve sources/VirtuaGrotesk.designspace --open
```

Keep the server running while editing. Source edits on disk live-reload in the
browser, and the user's Cmd+S in Runebender saves back to disk. Do not use the
old native `~/.cargo/bin/runebender` unless the user explicitly asks for the
native app.

## Core QA Expectations

- `documentation/core-qa-process.md` is the canonical human/agent QA process.
- `documentation/manual-cleanup-handoff.md` is the pause/resume checkpoint when
  hand drawing, source cleanup, or final maintainer inputs are still pending.
- Reusable Google Fonts onboarding knowledge lives in `.agents/` so it can be
  copied into future font repos:
  - `GOOGLE_FONTS_PORTING_CHECKLIST.md`
  - `.agents/google-fonts-onboarding-checklists.md`
  - `.agents/google-fonts-official-reference-map.md`
  - `.agents/skills/google-fonts-onboarding/SKILL.md`
  - `.agents/skills/google-fonts-qa/SKILL.md`
  - `.agents/skills/google-fonts-packaging/SKILL.md`
  - `.agents/skills/google-fonts-nonlatin-drawing/SKILL.md`
- `make test` is the automated Fontspector `googlefonts` profile gate.
- `make proof` renders the main DrawBot-skia PDF proof.
- `make specimen` renders the landscape print spacing specimen at
  `documentation/proofs/print-spacing-specimen.pdf`.
- `make reports` refreshes the active source/build metadata Markdown reports.
- `make preflight` is the normal local gate: build, proof, specimen, reports,
  then verify expected artifacts exist.
- Agents should regenerate or re-review proofs after spacing, kerning,
  build-output, or kerning-scope changes, then rerun `make preflight`.
- Do not treat kerning as final until the source kerning decision is recorded,
  the generated fonts expose the expected kerning behavior, and the
  `gftools qa --proof` output has been reviewed.
- Old agent-generated helper scripts are archived under
  `documentation/archive/agent-generated-scripts/`; do not wire them back into
  the active Makefile unless there is a clear current need.

## Proof Generation

```bash
python scripts/build_general_proof.py [font_path] [output_path]
make proof
make specimen
```

Uses DrawBot-style APIs to generate multi-page PDF proofs. The Makefile runs
this repo's virtualenv Python at `./.venv/bin/python`. drawbot-skia is
installed into `.venv` from `github.com/eliheuer/drawbot-skia` via
`requirements.txt`, so proofs work after a plain `make setup` on any machine.
Setting `DRAWBOT_SKIA_REPO` in the environment or ignored `local.mk` prepends
a live checkout's `src` directory to `PYTHONPATH` instead, for drawbot
development. drawbot-skia is also the standard tool for any ad-hoc image
generation (quick PNG renders of glyphs or feature tests).
`make specimen` renders the landscape print review PDF at
`documentation/proofs/print-spacing-specimen.pdf` across Regular, Medium, SemiBold,
and Bold.

## Source Architecture

- `sources/VirtuaGrotesk.designspace` — master designspace defining the Weight axis with two masters (Regular=400, Bold=700) and four instances (Regular, Medium, SemiBold, Bold)
- `sources/VirtuaGrotesk-Regular.ufo` / `VirtuaGrotesk-Bold.ufo` — the two master UFO sources
- `sources/archive/` — older versions of the sources (lowercase naming convention)

### UFO File Quick Reference

Each `.ufo` directory contains:
- `fontinfo.plist` — font-level metrics and naming
- `glyphs/contents.plist` — maps glyph names → `.glif` filenames
- `glyphs/*.glif` — individual glyph outlines (XML)
- `kerning.plist` — group-based kerning pairs (~78 pairs per master)
- `groups.plist` — kerning group definitions (89 groups per master)
- `lib.plist` — font-level metadata

### Character Set

Latin uppercase (A–Z), lowercase (a–z), numerals (0–9), punctuation, accented Latin characters, and a developing Arabic character set. Plus a private-use area block (E000–E020) for custom icons/symbols.

## The Render-Compare-Edit Loop

The core workflow for type design with an agent:

1. **Render** — `/proof`, `make proof`, or `make specimen` to see the current state
2. **Compare** — `/compare-reference <image>` to compare against a target
3. **Edit** — `/edit-glyph <name>` to make changes based on the comparison
4. **Build** — `/build-font` to compile the edited sources
5. **Verify** — `make preflight` during drawing work, then `make test` before final submission

## Adding Glyphs from Images (img2bez)

To add or replace a glyph from reference images (AI-generated or scanned
masters), use the `img2bez` CLI — do **not** hand-draw it in the editor.
img2bez owns deterministic tracing, ink placement, sidebearings, master
reconciliation, UFO writing, and the report; Runebender is only for visual
review afterward.

One image per master, traced and reconciled into interpolation-compatible
outlines in a single command:

```sh
img2bez masters sources/VirtuaGrotesk.designspace \
  --glyph germandbls --unicode 00DF \
  --image Regular=~/Desktop/00DF-regular.png \
  --image Bold=~/Desktop/00DF-bold.png \
  --fit descender:cap \
  --preserve-existing-metrics \
  --report build/germandbls-trace.json
```

- `--image NAME=path` names each image by its master stylename (`Regular`,
  `Bold`); or `--images <dir>` with files named `<stylename>.png`.
- `--fit zone:zone` sets the vertical band (e.g. `descender:cap`) in the font's
  own metric zones.
- `--format json` prints the report + outlines to stdout and writes no UFOs —
  use it to preview before writing.
- **Run `img2bez masters --help` for the full, current flag list — it is
  authoritative; do not rely on a copy of it here.**

**Read the report before opening the editor:**

- `compatible: true` — masters reconciled into one shared point structure
  (required for the variable build; see Master Compatibility Warning).
  `false` means a different contour count — regenerate the failing image.
- `lowConfidence: true` — a point was placed by a guessed correspondence;
  accept-but-review, or regenerate (`--fail-on-low-confidence` makes this exit
  non-zero for an unattended loop).
- Per master: `profile` (`wild`/`clean`/`photo` — how the image was classified),
  `sharpness`/`bilevelness` (input character), `points`, `advance`, `bounds`.

**Input tuning.** The default auto-detects the input class; clean crisp renders
trace as `wild`. Force `--profile photo` for soft, low-contrast scans of printed
type (it clears edge texture that otherwise over-segments). Other per-run
levers: `--pre-blur`, `--smoothing`, `--corner-threshold`, `--mode
{smooth,line}`. If a trace in the report looks wrong, re-run with the right flag
rather than hand-fixing in the editor.

**Trace logging (build the tuning dataset).** Export `IMG2BEZ_LOG` so every
trace appends a record (image features + settings + output) to one JSONL file —
this is how the input-adaptive selector gets its training data, and the settings
you re-run with (last trace per image) are the accepted label:

```sh
export IMG2BEZ_LOG="$HOME/.img2bez/virtua-grotesk-traces.jsonl"
```

Set it once at the start of a session; it covers `img2bez masters` and
single-glyph runs. Inspect the growing dataset with `img2bez`'s
`eval-harness/tracelog.py "$IMG2BEZ_LOG" --per-image`.

**Then review in Runebender** (`make runebender`) — it live-reloads the written
UFOs from disk. Use it only for the human visual check and final touch-ups.

## Design Philosophy

Virtua Grotesk is a geometric grotesk defined by its **16-unit chamfered corners** — every sharp junction gets a 45-degree bevel. Strokes are monolinear (no thick/thin contrast). Round forms use smooth cubic Bezier curves with generous counters. Weight gain across the axis works by **counter reduction** — outer contours often stay identical between Regular and Bold while the inner counter shrinks inward. See `documentation/source-guides/design-philosophy.md` for full outline drawing conventions.

## Master Compatibility Warning

Both masters (Regular and Bold) **must** have identical glyph structure: same contours, same point counts, same point types. Only coordinates and advance widths may differ. Structural changes to one master must be mirrored in the other. Incompatible masters will cause the variable font build to fail. Run `make reports` and review `documentation/source/master-compatibility.md` to verify.
