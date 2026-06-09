# Sources

Active source files:

- `VirtuaGrotesk.designspace`
- `VirtuaGrotesk-Regular.ufo`
- `VirtuaGrotesk-Bold.ufo`

These files are the canonical designspace/UFO source set for Virtua Grotesk.
Build systems should consume the designspace and UFO masters directly, then
write generated fonts and intermediate files outside the source tree.

`config.yaml` is a local build recipe for tools that support that format. It is
not a replacement for the designspace/UFO sources.

Older source material lives in `archive/` for reference only. It is not part of
the active source set and should not be used for normal builds unless a
maintainer explicitly promotes it back into the active source tree.
