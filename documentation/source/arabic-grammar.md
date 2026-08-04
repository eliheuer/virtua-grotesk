# Arabic grammar constants

Measured from the 70 green (Eli-approved) Arabic glyphs in
`VirtuaGrotesk-Regular.ufo` by `scripts/arabic_measure.py`
(raw data: `build/arabic-measure.json`). These numbers are the style
contract for every derived or newly drawn Arabic glyph. All values are
font units on the 2-grid.

**Bold status:** the green Arabic is byte-identical in both masters — the
Arabic bold weight has not been drawn yet. All new Arabic work follows the
same convention: draw Regular, mirror identically into Bold. The Arabic
emboldening pass is a separate workstream (OPEN, Eli's call on approach).

## Stroke weights (Regular)

| Stroke | Value | Source |
|---|---|---|
| Vertical stem / tooth | 96 | alef, lam.init, lam.fina, yeh.fina tail |
| Horizontal baseline stroke | 104–117 (typ. 112) | hah 104, dal 112, waw 112, reh 111, heh ~110, ain 106–117 |
| Round/bowl stroke | ~112 | waw bowl, reh tail |

Horizontals and rounds run slightly heavier than stems, the same optical
move as Latin (lc stems 96, rounds 98) but more pronounced.

## Vertical zones (Regular)

| Zone | Value | Source |
|---|---|---|
| Baseline | 0 | flat Arabic baseline, teeth sit on it |
| Tooth height (beh/noon/yeh) | 432 | behDotless.init/medi, peh, yeh.medi |
| Loop-glyph top (heh.medi) | 448 | heh.medi, hehGoal.medi |
| hah/jeem bowl top | 504 | hah.init, tcheh.init |
| feh.init bowl top | 592 | fehDotless.init |
| Ascender (alef, lam, kaf) | 768 (= cap height) | alef, lam.*, kaf.fina, gaf.fina |
| Descender | −256 (ink to −272 with below-dots) | reh.fina, jeh.fina, waw, heh.medi loop −296 |
| Dot-above band | 688..848 | dotabove |
| Dot-below band | −272..−112 | dotbelow |
| Hamza-above band | 832..1024 | hamzaabove |
| Three-dots peak | 1024 | threedotsupabove |

## Dots and small marks

- Single dot: **160 × 160** (chamfered square), advance-centered over/under
  the skeleton via component offset.
- Two dots horizontal: two 160-dots, **96 gap** (total width 416), same
  688..848 band.
- Three dots up: 448 wide × 368 tall (two below in the dot band, one above,
  peak 1024).
- Hamza (above/below): 224 × 192.

## Advance classes (Regular)

| Class | Advance | Members |
|---|---|---|
| Narrow init (tooth) | 288 | beh/peh/noon/theh .init, lam.init |
| Medial (tooth) | 416 | beh/teh/yeh/noon/theh .medi, lam.medi |
| yeh/farsiYeh init | 256 | yeh.init |
| alef | 224 isol / 256 fina | alef-ar |
| dal | 480 isol / 528 fina | dal, ddal |
| reh/zain family | 600 | reh.fina, jeh.fina |
| waw | 568 | waw-ar |
| feh init / medi | 480–482 / 592 | fehDotless |
| ain init / medi | 464–468 / 608 | ain, ghain |
| hah family | 668–672 | hah.init, khah.init, tcheh.init |
| heh medial | 480 | heh.medi family |
| Wide fina (kaf, seen, yeh) | 864–976 | kaf.fina 864, seen.init 864, yeh.fina 976 |

## Componentization conventions (from the green set)

The approved set builds dot-variants as **components over dotless
skeletons**: `beh-ar.init = behDotless-ar.init + dotbelow-ar`,
`ghain-ar.init = ain-ar.init + dotabove-ar`, `qaf-ar.medi =
fehDotless-ar.medi + twodotshorizontalabove-ar`. All derived work follows
this pattern. Positional entry stubs overhang: init/medi forms start at
x = −16 (joining overlap into the previous glyph).

## Vertical envelope (hard limit)

`fontinfo.plist` declares `openTypeOS2WinAscent` **1094** and
`openTypeOS2WinDescent` **438**. No glyph may put ink outside that band or
`family/win_ascent_and_descent` fails. Generated mark placement is clamped
to +1024 / −432 in `scripts/arabic_recompose.py`; stacked below-dot
clusters are tightened rather than offset by two full bands.

## Tooling

| Script | Job |
|---|---|
| `arabic_measure.py` | measure the green set → the numbers above |
| `arabic_lanes.py` | classify every non-green Arabic glyph into a lane |
| `arabic_build.py` | write repo-style glif, register new glyphs, union |
| `arabic_skeletons.py` | lane 3 — new skeletons and tail splices |
| `arabic_derive.py` | lane 2 — donor copies and bar removal |
| `arabic_recompose.py` | lane 1 — every dotted/marked composite |
| `arabic_symbols.py` | lane 4 — digits, punctuation, signs |
| `glif_lint.py` | structural gate — run before `make build` |
| `normalize_winding.py` | outer-CCW / holes-CW on blue glyphs only |

`harness/designbot/arabic_words.rs` renders shaped Arabic words from the
built variable font — the real verification for a contextual script.

## OPEN (Eli)

- Arabic Bold weight: counter-reduction like Latin, or stroke offset?
  Currently Bold == Regular by copy.
- Exact horizontal-stroke constant: green set varies 104–117; pick a
  canonical value (112?) for new drawings, or keep per-family optics.
- seen-ar.init dips to y = −16 (teeth baseline overshoot). Intentional?
  New teeth glyphs follow it.
- Green Arabic winding is inconsistent: `alef-ar` and `behDotless-ar.init`
  are CCW-outer, but `behDotless-ar.medi`, `seen-ar.init`, `hah-ar.init`
  and ~24 more are CW. Normalizing is mechanical (no shape change) but
  they are green, so it needs a decision.
- gaf / keheh three-dot placement: the dots currently clamp to the ceiling
  and may sit over the stem rather than beside the kaf arm.
- **`lam-ar.fina` (green) has no bowl** — it is a bare stem plus a joining
  bar (ink 80..528 × 0..768, nothing below the baseline), where a final lam
  normally sweeps into a deep bowl below the baseline (compare Rubik's
  lam-ar, which reaches −210 on a 750 cap). This is visible in shaped words
  ending in ل, e.g. جميل. `lam-ar` (isolated) was derived from it and so
  inherits the same gap. Fixing it means changing a green glyph and the
  whole lam family together, so it needs Eli's decision.
- `peh-ar.init` (green) carries no dots — pre-existing gap.
- hehGoal and hehDoachashmee are the same shape in every form, inherited
  from their green fina/medi which are also identical.
