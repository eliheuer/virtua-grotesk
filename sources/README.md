# Sources

Active source files:

- `VirtuaGrotesk.designspace`
- `VirtuaGrotesk-Regular.ufo`
- `VirtuaGrotesk-Bold.ufo`

These files are the canonical designspace/UFO source set for Virtua Grotesk.
Build systems should consume the designspace and UFO masters directly, then
write generated fonts and intermediate files outside the source tree.

The grid values, stroke targets, mark colors and the list of reference fonts
are in the `toml` blocks of `context.md` at the root. `fgtools` reads them.

`config.yaml` is the gftools builder recipe that `make build` uses.

Older Virtua Grotesk and Kinderhugel Grotesk sources were removed on
2026-11-10. They are in the Git history, in the folder sources/archive/.
