# Private-Use Glyph Scope

Primary font: `fonts/variable/VirtuaGrotesk[wght].ttf`
Variable font PUA codepoints: 23

This report inventories encoded Unicode Private Use Area glyphs from U+E000 through U+F8FF. PUA scope is a maintainer decision for Google Fonts review because these glyphs are not covered by public Unicode semantics.

## Google Fonts Review Impact

- PUA glyphs can affect Fontspector `unreachable_glyphs` warnings.
- PUA glyphs can affect `googlefonts/metadata/unreachable_subsetting` warnings.
- If these glyphs stay in the first submission, document why they should remain encoded and reachable.
- If these glyphs are removed or deferred, regenerate this report and the downstream package preview.
- Local Google Fonts package precedent shows PUA can ship, but usually with a small, family-specific rationale.

## Local Google Fonts PUA Precedent

This is a limited local checkout sample, not a policy exemption. Use it
only to frame the maintainer decision and any issue/PR rationale.

| Google Fonts package font | PUA codepoints | Min | Max |
| --- | ---: | --- | --- |
| `ofl/scheherazadenew/ScheherazadeNew-Regular.ttf` | 2 | U+F130 | U+F131 |
| `ofl/kedebideri/Kedebideri-Regular.ttf` | 2 | U+F130 | U+F131 |
| `ofl/inika/Inika-Regular.ttf` | 15 | U+E000 | U+E00E |
| `ofl/signikanegative/SignikaNegative[wght].ttf` | 251 | U+E000 | U+E12F |

## Source Coverage Summary

| Source | PUA codepoints | Matches variable cmap |
| --- | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | 23 | yes |
| `sources/VirtuaGrotesk-Bold.ufo` | 23 | yes |

## Built Font Summary

| Font | PUA codepoints | Matches variable cmap |
| --- | ---: | --- |
| `fonts/variable/VirtuaGrotesk[wght].ttf` | 23 | yes |
| `fonts/ttf/VirtuaGrotesk-Regular.ttf` | 23 | yes |
| `fonts/ttf/VirtuaGrotesk-Medium.ttf` | 23 | yes |
| `fonts/ttf/VirtuaGrotesk-SemiBold.ttf` | 23 | yes |
| `fonts/ttf/VirtuaGrotesk-Bold.ttf` | 23 | yes |

## PUA Codepoint Inventory

| Codepoint | Variable glyph | Regular source glyph | Bold source glyph | Present in all built fonts |
| --- | --- | --- | --- | --- |
| U+E000 | `uniE000` | `E000` | `E000` | yes |
| U+E004 | `uniE004` | `E004` | `E004` | yes |
| U+E005 | `uniE005` | `E005` | `E005` | yes |
| U+E006 | `uniE006` | `E006` | `E006` | yes |
| U+E007 | `uniE007` | `E007` | `E007` | yes |
| U+E008 | `uniE008` | `E008` | `E008` | yes |
| U+E009 | `uniE009` | `E009` | `E009` | yes |
| U+E010 | `uniE010` | `E010` | `E010` | yes |
| U+E011 | `uniE011` | `E011` | `E011` | yes |
| U+E012 | `uniE012` | `E012` | `E012` | yes |
| U+E013 | `uniE013` | `E013` | `E013` | yes |
| U+E014 | `uniE014` | `E014` | `E014` | yes |
| U+E015 | `uniE015` | `E015` | `E015` | yes |
| U+E016 | `uniE016` | `E016` | `E016` | yes |
| U+E017 | `uniE017` | `E017` | `E017` | yes |
| U+E018 | `uniE018` | `E018` | `E018` | yes |
| U+E019 | `uniE019` | `E019` | `E019` | yes |
| U+E020 | `uniE020` | `E020` | `E020` | yes |
| U+E021 | `uniE021` | `E021` | `E021` | yes |
| U+F000 | `uniF000` | `uniF000` | `uniF000` | yes |
| U+F001 | `uniF001` | `F001` | `F001` | yes |
| U+F002 | `uniF002` | `F002` | `F002` | yes |
| U+F003 | `uniF003` | `F003` | `F003` | yes |
