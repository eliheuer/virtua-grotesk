# Virtua Grotesk design

The canonical design library is [design/README.md](design/README.md).
Retrieve the relevant context before drawing:

```sh
make design-context GLYPH=seen-ar OPERATION=curve-repair
```

| Topic | Owner |
| --- | --- |
| Character and construction | [Identity](design/system/identity.md) |
| Metrics, 8/2 grid, popcount | [Grid](design/system/grid.md), [machine contract](design/system/contract.json) |
| Weight and spacing | [Weight](design/system/weight.md), [spacing](design/system/spacing.md) |
| Interpolation and source topology | [Interpolation](design/system/interpolation.md) |
| Chamfers, turns, curves, bowls, dots | [Construction index](design/constructions/README.md) |
| Arabic, Hebrew, Latin, symbols | [Writing systems](design/writing-systems/README.md) |
| Named intent and exceptions | [Glyph contracts](design/glyphs/README.md) |
| Human corrections and rejected examples | [Correction library](design/corrections/README.md) |
| Current state and evidence | [Reviews](design/reviews/README.md) |
| Training provenance | [Learning boundaries](design/system/learning.md) |

The earlier monolithic guide is preserved in
[the migration archive](design/migration/original-documents/DESIGN.md).
It is historical evidence; use the maintained topics above for current work.
