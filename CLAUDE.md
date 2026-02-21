# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Virtua Grotesk is an open-source variable font (OFL v1.1 licensed) with a Weight axis (wght 400–700). The sources are UFO files and the font is built using Google's Rust-based font compilers.

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
