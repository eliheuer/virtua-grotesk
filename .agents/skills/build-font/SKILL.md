# /build-font

Build Virtua Grotesk fonts from UFO sources.

## Usage
`/build-font [variable|static|all]`

Default: `all`

## Instructions

### Activate the Python venv first
Run: `source ~/Py/venvs/basic-fonts/bin/activate`

### Based on the argument:

**`all` (default):**
Run `./build.sh` from the project root. This builds both the variable font (via fontc) and static instances (via fontmake).

**`variable`:**
Run:
```bash
mkdir -p fonts
fontc sources/VirtuaGrotesk.designspace
mv build/font.ttf fonts/VirtuaGrotesk-VF.ttf
```

**`static`:**
Run:
```bash
mkdir -p fonts
fontmake -m sources/VirtuaGrotesk.designspace -i -o ttf --output-dir fonts/
```

### After building:
1. List the built fonts with file sizes: `ls -lh fonts/*.ttf`
2. Report which fonts were built and their sizes
3. If the build failed, read the error output and suggest fixes (common issues: master incompatibility, missing glyphs, invalid XML in .glif files)
