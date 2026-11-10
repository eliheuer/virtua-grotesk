# Virtua design rules

These documents describe how Virtua Grotesk is drawn. They are reference
material for people and agents. They do not grant permission to edit a glyph;
see [AGENTS.md](../AGENTS.md) for the source rules.

| Topic | Documents |
| --- | --- |
| Character and construction | [Identity](system/identity.md) |
| Metrics, 8/2 grid, popcount | [Grid](system/grid.md), [contract.json](system/contract.json) |
| Weight and spacing | [Weight](system/weight.md), [Spacing](system/spacing.md) |
| Interpolation and source topology | [Interpolation](system/interpolation.md) |
| Source protection | [Source safety](system/source-safety.md) |
| Verification of a change | [Verification](system/verification.md) |
| Chamfers, turns, curves, bowls, dots | [Constructions](constructions/README.md) |
| Arabic, Hebrew, Latin, symbols | [Writing systems](writing-systems/README.md) |
| Named glyph intent | [Glyph records](glyphs/README.md) |
| Reference roles and Latin dimensions | [References](references/README.md), [Latin dimensions](references/latin-dimensions.md) |
| Training data boundaries | [Learning](system/learning.md) |
| Earlier design philosophy | [History](system/design-philosophy-history.md) |

`design/system/contract.json` is the machine-readable contract for metrics, grid
and mark colors. `make status` reads its color definitions.

The review records, correction library and context retrieval tool that these
documents once linked to are on branch `archive/agent-records-2026-11-09`.
