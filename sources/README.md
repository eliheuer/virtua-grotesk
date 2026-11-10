# Sources

Active source files:

- `VirtuaGrotesk.designspace`
- `VirtuaGrotesk-Regular.ufo`
- `VirtuaGrotesk-Bold.ufo`

These files are the canonical designspace/UFO source set for Virtua Grotesk.
Build systems should consume the designspace and UFO masters directly, then
write generated fonts and intermediate files outside the source tree.

`design.toml` holds the grid values, stroke targets and mark colors that the
scripts read.

`config.yaml` is a local build recipe for tools that support that format. It is
not a replacement for the designspace/UFO sources.

Older Virtua Grotesk and Kinderhugel Grotesk sources are in the Git history,
in the folder `sources/archive/`, which was removed on 2026-11-10.
