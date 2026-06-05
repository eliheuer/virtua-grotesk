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
Run `./build.sh` from the project root. This prefers `gftools builder sources/config.yaml`, then falls back to the local fontc/fontmake path.

**`variable`:**
Run:
```bash
mkdir -p fonts
fontc sources/VirtuaGrotesk.designspace
mv build/font.ttf 'fonts/variable/VirtuaGrotesk[wght].ttf'
```

**`static`:**
Run:
```bash
mkdir -p fonts
fontmake -m sources/VirtuaGrotesk.designspace -i -o ttf --output-dir fonts/ttf
```

### After building:
1. List the built fonts with file sizes: `ls -lh fonts/variable/*.ttf fonts/ttf/*.ttf`
2. Report which fonts were built and their sizes
3. If the build failed, read the error output and suggest fixes (common issues: master incompatibility, missing glyphs, invalid XML in .glif files)
