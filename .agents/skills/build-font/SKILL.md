---
name: build-font
description: Build Virtua Grotesk variable and static fonts from the UFO sources. Use when asked to build, compile, or regenerate fonts, or after editing sources.
---

# /build-font

Build Virtua Grotesk fonts from UFO sources.

## Usage
`/build-font [variable|static|all]`

Default: `all`

## Instructions

### Activate the project Python venv first
Run: `source venv/bin/activate`

### Based on the argument:

**`all` (default):**
Run `./build.sh` from the project root. This is the canonical build entrypoint
and wraps `gftools builder sources/config.yaml`.

**`variable`:**
Run `./build.sh`, then inspect `fonts/variable/VirtuaGrotesk[wght].ttf`.

**`static`:**
Run `./build.sh`, then inspect `fonts/ttf/*.ttf`.

### After building:
1. List the built fonts with file sizes: `ls -lh fonts/variable/*.ttf fonts/ttf/*.ttf`
2. Report which fonts were built and their sizes
3. If the build failed, read the error output and suggest fixes (common issues: master incompatibility, missing glyphs, invalid XML in .glif files)
