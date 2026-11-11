# Virtua design rules

These documents describe how Virtua Grotesk is drawn. They are reference
material for people and agents. They do not grant permission to edit a glyph;
see [AGENTS.md](../../AGENTS.md) for the source rules.

| Topic | Documents |
| --- | --- |
| Character and construction | [Identity](system/identity.md) |
| Metrics, 8/2 grid, popcount | [Grid](system/grid.md), [design.toml](../../sources/design.toml) |
| Weight and spacing | [Weight](system/weight.md), [Spacing](system/spacing.md) |
| Interpolation and source topology | [Interpolation](system/interpolation.md) |
| Verification of a change | [Verification](system/verification.md) |
| Chamfers, turns, curves, bowls, dots | [Constructions](constructions/README.md) |
| Arabic, Hebrew, Latin, symbols | [Writing systems](writing-systems/README.md) |
| Named glyph intent | [Glyph records](glyphs/README.md) |
| Reference roles and reference fonts | [References](references/README.md) |
| Checks, benchmark and how corrections are recorded | [Learning loop](system/learning.md) |
| Editing UFO, designspace and kerning files | [Source editing](system/source-editing.md) |

`sources/design.toml` holds the values that scripts read: grid, chamfers,
stroke targets and mark colors. `make status` and `make check-design` read it.

The review records, correction library and context retrieval tool that these
documents once linked to are in the Git history before commit 1db2dfc7.
