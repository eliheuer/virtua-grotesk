# Variable Font Metadata

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`

This report records variable-font axis metadata that matters for Google Fonts packaging and metadata review. It is generated from the built variable TTF, not from source assumptions.

## Summary

- Has `fvar`: yes
- Has `STAT`: yes
- Has `avar`: no
- Axis tags: `wght`

## fvar Axes

| Tag | Name | Min | Default | Max | Flags |
| --- | --- | ---: | ---: | ---: | ---: |
| `wght` | Weight | 400 | 400 | 700 | 0 |

## fvar Instances

| Subfamily | Coordinates | PostScript name | Flags |
| --- | --- | --- | ---: |
| Regular | `wght=400` | `VirtuaGrotesk-Regular` | 0 |
| Medium | `wght=500` | `VirtuaGrotesk-Medium` | 0 |
| SemiBold | `wght=600` | `VirtuaGrotesk-SemiBold` | 0 |
| Bold | `wght=700` | `VirtuaGrotesk-Bold` | 0 |

## STAT Axes

| Tag | Name | Ordering |
| --- | --- | ---: |
| `wght` | Weight | 0 |

## STAT Axis Values

| Format | Name | Axis index | Value | Linked value | Flags |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3 | Regular | 0 | 400 | 700 | 2 |
| 1 | Medium | 0 | 500 |  | 0 |
| 1 | SemiBold | 0 | 600 |  | 0 |
| 1 | Bold | 0 | 700 |  | 0 |

## Review Notes

- The current `wght` axis is 400-700 with default 400.
- The 600 instance is named `SemiBold`, matching Google Fonts style naming.
- The Regular STAT axis value is linked to Bold.
- No `avar` table is emitted; keep or change this according to the `avar` decision log entry.
