# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

Virtua Grotesk is an open-source variable font (OFL v1.1 licensed) with a Weight axis (wght 400–700). The sources are UFO files and the Google Fonts-ready build path uses `gftools builder sources/config.yaml`.

## Quick Start

```bash
/build-font              # Build all fonts (variable + static)
/render-specimen 001     # Render character set specimen
/proof                   # Generate PDF proof document
make preflight           # Run current Google Fonts handoff gate
make test                # Build, then run Fontspector googlefonts profile
make kerning-proof-check # Generate gftools QA HTML proof for spacing/kerning review
/edit-glyph A            # Inspect/edit a glyph
/kerning list            # View current kerning pairs
/compare-reference img   # Compare font to a reference image
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

**Prerequisites:** Python venv with `pip install -r requirements.txt`; optional `cargo install fontc` for fallback variable-font builds.

```bash
# Build all fonts (variable + static instances)
./build.sh

# Run local Google Fonts readiness preflight from a fresh build
make preflight

# Run local preflight against the current generated fonts/reports
make preflight-only

# Build, then run Fontspector's Google Fonts profile
make test

# Run Fontspector's Google Fonts profile directly
./scripts/check_gf_fonts.sh

# Run the Google Fonts visual proof used for spacing/kerning review
make kerning-proof-check

# Generate the visual proof review checklist
make kerning-proof-review-check

# Dry-run final designer-profile install into local google/fonts fork
make designer-profile-prepare-check
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
- `make test` is the automated Fontspector `googlefonts` profile gate.
- `make kerning-proof-check` is part of the core visual QA process, not an
  optional extra. It runs `gftools qa --proof` and writes HTML proof output to
  `documentation/gftools-qa/` for human spacing and kerning review.
- `make kerning-proof-review-check` generates
  `documentation/kerning-proof-review.md`, which enumerates the expected proof
  HTML by weight and proof type for human and agent review.
- Agents should regenerate or re-review that proof after any spacing, kerning,
  build-output, or kerning-scope decision change, then rerun `make preflight`.
- Run `make kerning-check` before and after kerning edits to verify source
  kerning symmetry, built GPOS `kern` coverage, Fontspector warnings, and
  `gftools qa` proof readiness.
- Do not treat kerning as final until the source kerning decision is recorded,
  the generated fonts expose the expected kerning behavior, and the
  `gftools qa --proof` output has been reviewed.

## Rendering Specimens

**Prerequisite:** `cargo install designbot`

```bash
designbot --render designbot/001.rs --output designbot/001.png
```

Specimen scripts are Rust files in `designbot/` that use the DesignBot API. They load built fonts from `fonts/ttf/` relative to the repository root.

## Proof Generation

```bash
python proof.py [font_path] [output_path]
```

Uses DrawBot-style APIs to generate multi-page PDF proofs. The Makefile
defaults to the local `eliheuer/drawbot-skia` fork at
`/Users/eli/GH/repos/drawbot-skia` and renders
`fonts/ttf/VirtuaGrotesk-Regular.ttf` → `proof.pdf`.

## Source Architecture

- `sources/VirtuaGrotesk.designspace` — master designspace defining the Weight axis with two masters (Regular=400, Bold=700) and four instances (Regular, Medium, SemiBold, Bold)
- `sources/VirtuaGrotesk-Regular.ufo` / `VirtuaGrotesk-Bold.ufo` — the two master UFO sources
- `sources/archive/` — older versions of the sources (lowercase naming convention)

### UFO File Quick Reference

Each `.ufo` directory contains:
- `fontinfo.plist` — font-level metrics and naming
- `glyphs/contents.plist` — maps glyph names → `.glif` filenames
- `glyphs/*.glif` — individual glyph outlines (XML)
- `kerning.plist` — flat kerning pairs (Bold has ~90 pairs; Regular has none yet)
- `groups.plist` — kerning group definitions (Bold has 40+ groups)
- `lib.plist` — font-level metadata

### Character Set

Latin uppercase (A–Z), lowercase (a–z), numerals (0–9), punctuation, accented Latin characters, and a developing Arabic character set. Plus a private-use area block (E000–E020) for custom icons/symbols.

## The Render-Compare-Edit Loop

The core workflow for type design with Codex:

1. **Render** — `/render-specimen` or `/proof` to see the current state
2. **Compare** — `/compare-reference <image>` to compare against a target
3. **Edit** — `/edit-glyph <name>` to make changes based on the comparison
4. **Build** — `/build-font` to compile the edited sources
5. **Verify** — `make preflight` during drawing work, then `make test` before final submission

## Design Philosophy

Virtua Grotesk is a geometric grotesk defined by its **16-unit chamfered corners** — every sharp junction gets a 45-degree bevel. Strokes are monolinear (no thick/thin contrast). Round forms use smooth cubic Bezier curves with generous counters. Weight gain across the axis works by **counter reduction** — outer contours often stay identical between Regular and Bold while the inner counter shrinks inward. See `.claude/rules/design-philosophy.md` for full outline drawing conventions.

## Master Compatibility Warning

Both masters (Regular and Bold) **must** have identical glyph structure: same contours, same point counts, same point types. Only coordinates and advance widths may differ. Structural changes to one master must be mirrored in the other. Incompatible masters will cause the variable font build to fail. Run `make reports-only` and review `documentation/master-compatibility.md` to verify.
