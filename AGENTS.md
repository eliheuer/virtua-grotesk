# AGENTS.md

This file is the canonical guidance for AI coding agents (Claude Code, Codex,
etc.) working in this repository. `CLAUDE.md` imports this file and adds
Claude Code-specific notes — shared guidance belongs here, not there.

Agent skills live in `.agents/skills/` (one directory per skill with a
`SKILL.md`). `.claude/skills` is a symlink to that directory so Claude Code
picks them up — edit skills only in `.agents/skills/`.

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
make reports    # Regenerate source/build metadata reports
make preflight  # Run the full local handoff gate
make test       # Build, then run Fontspector's googlefonts profile
```

Built fonts go to `fonts/variable/` and `fonts/ttf/` (gitignored). `build/` and `sources/instance_ufos/` are generated build outputs.

## Core QA Expectations

- `documentation/core-qa-process.md` is the canonical human/agent QA process.
- `documentation/manual-cleanup-handoff.md` is the pause/resume checkpoint when
  hand drawing, source cleanup, or final maintainer inputs are still pending.
- Reusable Google Fonts onboarding knowledge lives in `.agents/` so it can be
  copied into future font repos:
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
this repo's virtualenv Python at `./.venv/bin/python`. If `DRAWBOT_SKIA_REPO`
is set in the environment or ignored `local.mk`, it prepends that checkout's
`src` directory to `PYTHONPATH`; otherwise `drawbot_skia` must be importable
from `.venv`.
`make specimen` renders the landscape print review PDF at
`documentation/proofs/print-spacing-specimen.pdf` across Regular, Medium, SemiBold,
and Bold, with `documentation/proofs/print-spacing-specimen-index.md` as the page map.

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

## Design Philosophy

Virtua Grotesk is a geometric grotesk defined by its **16-unit chamfered corners** — every sharp junction gets a 45-degree bevel. Strokes are monolinear (no thick/thin contrast). Round forms use smooth cubic Bezier curves with generous counters. Weight gain across the axis works by **counter reduction** — outer contours often stay identical between Regular and Bold while the inner counter shrinks inward. See `documentation/source-guides/design-philosophy.md` for full outline drawing conventions.

## Master Compatibility Warning

Both masters (Regular and Bold) **must** have identical glyph structure: same contours, same point counts, same point types. Only coordinates and advance widths may differ. Structural changes to one master must be mirrored in the other. Incompatible masters will cause the variable font build to fail. Run `make reports` and review `documentation/source/master-compatibility.md` to verify.
