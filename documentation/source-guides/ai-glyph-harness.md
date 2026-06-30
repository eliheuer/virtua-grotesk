# AI Glyph Harness

This repo has a staged harness for AI-assisted glyph expansion:

```bash
make glyph-ai-inventory
make glyph-ai-prepare TARGET=<glyph-name> REFERENCES="a,e,exclam"
```

The harness reads Runebender's `public.markColor` labels from the UFO sources.
Green (`0.09,0.72,0.44,1`) means a glyph is a good reference. The script renders
those reference glyphs from the active UFO outlines with drawbot-skia, then
creates a run packet under `build/glyph-ai-harness/<glyph-name>/`.

Each run packet contains:

- `references/` source-rendered PNGs for green reference glyphs
- `current/` source-rendered PNGs for the current target, if present
- `prompts/` OpenAI image-generation briefs for Regular and Bold
- `generated/` expected location for generated PNGs
- `trace-commands.sh` img2bez commands that trace into scratch UFOs
- `manifest.json` with paths, warnings, and trace command metadata

After generating images, save them as:

```text
build/glyph-ai-harness/<glyph-name>/generated/regular/<glyph-name>.png
build/glyph-ai-harness/<glyph-name>/generated/bold/<glyph-name>.png
```

Then trace into scratch UFOs:

```bash
./build/glyph-ai-harness/<glyph-name>/trace-commands.sh
```

or:

```bash
./.venv/bin/python scripts/glyph_ai_harness.py trace --run-dir build/glyph-ai-harness/<glyph-name>
```

Do not treat traced contours as final. Separate AI-generated Regular and Bold
images usually trace to different point structures, so review
`trace/master-compatibility.md`, clean the outlines in Runebender, and run the
normal build/proof checks before promoting anything into `sources/`.

The harness traces with `--chamfer 0` by default. Virtua Grotesk still uses
16-unit chamfers as a drawing convention, but automatic img2bez chamfering is
only for reviewed line-based shapes; it can flatten curved glyphs into
polygonal outlines.
