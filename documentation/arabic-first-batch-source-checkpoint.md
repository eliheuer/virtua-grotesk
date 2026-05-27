# Arabic First Batch Source Checkpoint

This generated report records source-side structure for the glyphs
called out by the current structure and wrong-glyph review batch.
Use it before and after hand edits to catch accidental Regular/Bold
structure drift. It is not visual approval and does not mark any
review row as passed.

## Summary

- Glyphs checked: 7
- Masters checked: 2
- Missing source files: 0
- Regular/Bold structure mismatches: 0
- Ready for paired-master hand review: yes

## Glyph Structure

| Glyph | Regular | Bold | Structure match | Components |
| --- | --- | --- | --- | --- |
| `hamzaabove-ar` | width 0; unicode 0654; contours 1; components 0; points 31; bbox `0,832,224,1024` | width 0; unicode 0654; contours 1; components 0; points 31; bbox `0,832,224,1024` | yes | - |
| `hamzabelow-ar` | width 0; unicode 0655; contours 1; components 0; points 31; bbox `0,-256,224,-64` | width 0; unicode 0655; contours 1; components 0; points 31; bbox `0,-256,224,-64` | yes | - |
| `madda-ar` | width 0; unicode 0653; contours 1; components 0; points 10; bbox `-144,4,144,152` | width 0; unicode 0653; contours 1; components 0; points 10; bbox `-144,4,144,152` | yes | - |
| `seen-ar` | width 864; unicode 0633; contours 1; components 0; points 61; bbox `-368,-296,768,432` | width 864; unicode 0633; contours 1; components 0; points 61; bbox `-368,-296,768,432` | yes | - |
| `sheen-ar` | width 864; unicode 0634; contours 0; components 2; points 0; bbox `none` | width 864; unicode 0634; contours 0; components 2; points 0; bbox `none` | yes | `seen-ar`<br>`threedotsupabove-ar` (xOffset=432, yOffset=-144) |
| `theh-ar` | width 600; unicode 062B; contours 0; components 2; points 0; bbox `none` | width 600; unicode 062B; contours 0; components 2; points 0; bbox `none` | yes | `behDotless-ar`<br>`threedotsupabove-ar` |
| `waw-ar` | width 570; unicode 0648; contours 2; components 0; points 44; bbox `-128,-256,538,408` | width 570; unicode 0648; contours 2; components 0; points 44; bbox `-128,-256,538,408` | yes | - |

## Source Files

| Glyph | Regular GLIF | Bold GLIF |
| --- | --- | --- |
| `hamzaabove-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzaabove-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzaabove-ar.glif` |
| `hamzabelow-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/hamzabelow-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/hamzabelow-ar.glif` |
| `madda-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/madda-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/madda-ar.glif` |
| `seen-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/seen-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/seen-ar.glif` |
| `sheen-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/sheen-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/sheen-ar.glif` |
| `theh-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/theh-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/theh-ar.glif` |
| `waw-ar` | `sources/VirtuaGrotesk-Regular.ufo/glyphs/waw-ar.glif` | `sources/VirtuaGrotesk-Bold.ufo/glyphs/waw-ar.glif` |

## Use

- If a visual row becomes `fix-needed`, edit the Regular and Bold
  source files together and preserve the structure match unless a
  deliberate mirrored structural change is required.
- Rerun `make arabic-first-batch-source-checkpoint` after source edits
  and before `make arabic-after-drawing-check`.
- Keep visual decisions in `documentation/arabic-visual-review-log.md`;
  this file is only a source-structure checkpoint.
