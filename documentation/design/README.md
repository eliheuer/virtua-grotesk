# Virtua design rules

The rules themselves are numbered in
[context.md](../../context.md). These documents
explain them and give the procedures.

These documents describe how Virtua Grotesk is drawn. They are reference
material for people and agents. They do not grant permission to edit a glyph;
see [AGENTS.md](../../AGENTS.md) for the source rules.

| Topic | Documents |
| --- | --- |
| Character and construction | [Identity](system/identity.md) |
| Metrics, 8/2 grid, popcount | [Grid](system/grid.md), [context.md](../../context.md) |
| Weight and spacing | [Weight](system/weight.md), [Spacing](system/spacing.md) |
| Interpolation and source topology | [Interpolation](system/interpolation.md) |
| Verification of a change | [Verification](system/verification.md) |
| Chamfers, turns, curves, bowls, dots | [Constructions](constructions/README.md) |
| Arabic, Hebrew, Latin, symbols | [Writing systems](writing-systems/README.md) |
| Named glyph intent | [Glyph records](glyphs/README.md) |
| Reference roles and reference fonts | [References](references/README.md) |
| Checks, drafting evaluation and how corrections are recorded | [Learning loop](system/learning.md) |
| Editing UFO, designspace and kerning files | [Source editing](system/source-editing.md) |

The `toml` blocks of `context.md` hold the values that `fgtools` reads: grid, chamfers,
stroke targets, mark colors and the reference fonts. `make status` and `make check-design` read them.

The review records, correction library and context retrieval tool that these
documents once linked to are in the Git history before commit 1db2dfc7.
