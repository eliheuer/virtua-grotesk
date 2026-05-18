# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Virtua Grotesk is an open-source variable font (OFL v1.1 licensed) with a Weight axis (wght 400–700). The sources are UFO files and the font is built using Google's Rust-based font compilers.

## Quick Start

```bash
/build-font              # Build all fonts (variable + static)
/render-specimen 001     # Render character set specimen
/proof                   # Generate PDF proof document
/font-qa                 # Run all quality checks
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

**Prerequisites:** `cargo install fontc`, `fontmake` (via Python venv at `~/Py/venvs/basic-fonts/`)

```bash
# Build all fonts (variable + static instances)
./build.sh

# Build variable font only with fontc
fontc sources/VirtuaGrotesk.designspace

# Build static instances only with fontmake
fontmake -m sources/VirtuaGrotesk.designspace -i -o ttf --output-dir fonts/
```

Built fonts go to `fonts/` (gitignored). The `build/` directory is fontc's intermediate output.

## Rendering Specimens

**Prerequisite:** `cargo install designbot`

```bash
designbot --render designbot/001.rs --output designbot/001.png
```

Specimen scripts are Rust files in `designbot/` that use the DesignBot API. They load built fonts from `../fonts/` relative to the designbot directory.

## Proof Generation

```bash
python proof.py [font_path] [output_path]
```

Uses DrawBot (Python) to generate multi-page PDF proofs. Defaults to `fonts/VirtuaGrotesk-Regular.ttf` → `proof.pdf`.

## Source Architecture

- `sources/VirtuaGrotesk.designspace` — master designspace defining the Weight axis with two masters (Regular=400, Bold=700) and four instances (Regular, Medium, Semi-Bold, Bold)
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

The core workflow for type design with Claude Code:

1. **Render** — `/render-specimen` or `/proof` to see the current state
2. **Compare** — `/compare-reference <image>` to compare against a target
3. **Edit** — `/edit-glyph <name>` to make changes based on the comparison
4. **Build** — `/build-font` to compile the edited sources
5. **Verify** — `/font-qa` to check nothing broke, then back to step 1

## Design Philosophy

Virtua Grotesk is a geometric grotesk defined by its **16-unit chamfered corners** — every sharp junction gets a 45-degree bevel. Strokes are monolinear (no thick/thin contrast). Round forms use smooth cubic Bezier curves with generous counters. Weight gain across the axis works by **counter reduction** — outer contours often stay identical between Regular and Bold while the inner counter shrinks inward. See `.claude/rules/design-philosophy.md` for full outline drawing conventions.

## Master Compatibility Warning

Both masters (Regular and Bold) **must** have identical glyph structure: same contours, same point counts, same point types. Only coordinates and advance widths may differ. Structural changes to one master must be mirrored in the other. Incompatible masters will cause the variable font build to fail. Run `/font-qa --check masters` to verify.
