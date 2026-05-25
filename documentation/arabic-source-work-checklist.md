# Arabic Source Work Checklist

This generated checklist translates the current `GF_Arabic_Core` cmap gaps into source-glyph work across both active UFO masters. It is a production aid for drawing and compatibility work; the authoritative coverage target remains the installed `glyphsets` definition, and visual Arabic review is still required.

## Summary

- Font checked: `fonts/variable/VirtuaGrotesk[wght].ttf`
- Minimum Arabic target: `GF_Arabic_Core`
- Missing required codepoints: 57
- Arabic-range missing codepoints: 29
- Shared punctuation/symbol missing codepoints: 28
- U+25CC dotted circle missing: yes
- Suggested source glyph names: 88
- Suggested Arabic source glyph names: 60
- Suggested shared punctuation/symbol glyph names: 28
- Suggested Arabic default glyph names: 29
- Suggested Arabic positional-form glyph names: 31
- Suggested glyph names present in both masters: 0
- Suggested glyph names missing in both masters: 88
- Suggested glyph names partial across masters: 0
- Arabic reuse prerequisites checked: 13 codepoints
- Missing reuse prerequisites across masters: 0
- Active source masters checked: `sources/VirtuaGrotesk-Regular.ufo`, `sources/VirtuaGrotesk-Bold.ufo`

## Suggested Source Inventory

| Bucket | Count |
| --- | ---: |
| Total suggested source glyph names | 88 |
| Arabic suggested source glyph names | 60 |
| Shared punctuation/symbol suggested glyph names | 28 |
| Arabic default glyph names | 29 |
| Arabic positional-form glyph names | 31 |
| Suggested glyph names already present in both masters | 0 |
| Suggested glyph names missing in both masters | 88 |
| Suggested glyph names partial across masters | 0 |

## Source Rules

- Add every required encoded glyph to both active UFO masters.
- For joining Arabic letters, keep the same default/final/initial/medial glyph structure in both masters.
- Preserve master compatibility: same contour/component structure, point counts, and point types in Regular and Bold.
- Add dotted circle and mark anchors before final Arabic mark proofing.
- Rerun `make preflight` after each source batch.

## Missing Codepoint Worklist

| Codepoint | Unicode name | Type | Suggested source glyphs | Built cmap glyph | Regular source | Bold source | Reuse note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U+002B + | PLUS SIGN | Shared punctuation/symbol | `plus` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+003C < | LESS-THAN SIGN | Shared punctuation/symbol | `less` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+003D = | EQUALS SIGN | Shared punctuation/symbol | `equal` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+003E > | GREATER-THAN SIGN | Shared punctuation/symbol | `greater` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0040 @ | COMMERCIAL AT | Shared punctuation/symbol | `at` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+005B [ | LEFT SQUARE BRACKET | Shared punctuation/symbol | `bracketleft` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+005D ] | RIGHT SQUARE BRACKET | Shared punctuation/symbol | `bracketright` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+005E ^ | CIRCUMFLEX ACCENT | Shared punctuation/symbol | `asciicircum` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0060 ` | GRAVE ACCENT | Shared punctuation/symbol | `grave` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+007B { | LEFT CURLY BRACKET | Shared punctuation/symbol | `braceleft` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+007C \| | VERTICAL LINE | Shared punctuation/symbol | `bar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+007D } | RIGHT CURLY BRACKET | Shared punctuation/symbol | `braceright` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+007E ~ | TILDE | Shared punctuation/symbol | `asciitilde` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00A2 ¢ | CENT SIGN | Shared punctuation/symbol | `cent` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00A3 £ | POUND SIGN | Shared punctuation/symbol | `sterling` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00A5 ¥ | YEN SIGN | Shared punctuation/symbol | `yen` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00A9 © | COPYRIGHT SIGN | Shared punctuation/symbol | `copyright` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00AB « | LEFT-POINTING DOUBLE ANGLE QUOTATION MARK | Shared punctuation/symbol | `guillemotleft` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00AE ® | REGISTERED SIGN | Shared punctuation/symbol | `registered` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00B0 ° | DEGREE SIGN | Shared punctuation/symbol | `degree` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00BB » | RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK | Shared punctuation/symbol | `guillemotright` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00D7 × | MULTIPLICATION SIGN | Shared punctuation/symbol | `multiply` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+00F7 ÷ | DIVISION SIGN | Shared punctuation/symbol | `divide` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0609 ؉ | ARABIC-INDIC PER MILLE SIGN | Arabic punctuation | `perMille-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+060D ؍ | ARABIC DATE SEPARATOR | Arabic punctuation | `dateSeparator-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0615 | ARABIC SMALL HIGH TAH | Arabic mark | `smallHighTah-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0658 | ARABIC MARK NOON GHUNNA | Arabic mark | `noonGhunna-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0679 ٹ | ARABIC LETTER TTEH | Arabic letter | `tteh-ar`, `tteh-ar.fina`, `tteh-ar.init`, `tteh-ar.medi` | `.notdef` | missing | missing | `teh-ar` plus `twodotsverticalabove-ar` pattern |
| U+067E پ | ARABIC LETTER PEH | Arabic letter | `peh-ar`, `peh-ar.fina`, `peh-ar.init`, `peh-ar.medi` | `.notdef` | missing | missing | `behDotless-ar` plus `threedotsdownbelow-ar` |
| U+0686 چ | ARABIC LETTER TCHEH | Arabic letter | `tcheh-ar`, `tcheh-ar.fina`, `tcheh-ar.init`, `tcheh-ar.medi` | `.notdef` | missing | missing | `hah-ar` plus `threedotsdownbelow-ar` |
| U+0688 ڈ | ARABIC LETTER DDAL | Arabic letter | `ddal-ar`, `ddal-ar.fina` | `.notdef` | missing | missing | `dal-ar` plus dot/mark pattern |
| U+0691 ڑ | ARABIC LETTER RREH | Arabic letter | `rreh-ar`, `rreh-ar.fina` | `.notdef` | missing | missing | `reh-ar` plus dot/mark pattern |
| U+0698 ژ | ARABIC LETTER JEH | Arabic letter | `jeh-ar`, `jeh-ar.fina` | `.notdef` | missing | missing | `reh-ar` plus `threedotsupabove-ar` |
| U+06A9 ک | ARABIC LETTER KEHEH | Arabic letter | `keheh-ar`, `keheh-ar.fina`, `keheh-ar.init`, `keheh-ar.medi` | `.notdef` | missing | missing | `kaf-ar` skeleton, Persian/Urdu proportions need review |
| U+06AF گ | ARABIC LETTER GAF | Arabic letter | `gaf-ar`, `gaf-ar.fina`, `gaf-ar.init`, `gaf-ar.medi` | `.notdef` | missing | missing | `kaf-ar` plus `gafsarkashabove-ar` pattern |
| U+06BE ھ | ARABIC LETTER HEH DOACHASHMEE | Arabic letter | `hehDoachashmee-ar`, `hehDoachashmee-ar.fina`, `hehDoachashmee-ar.init`, `hehDoachashmee-ar.medi` | `.notdef` | missing | missing | `heh-ar` skeleton, Urdu joining behavior needs review |
| U+06C1 ہ | ARABIC LETTER HEH GOAL | Arabic letter | `hehGoal-ar`, `hehGoal-ar.fina`, `hehGoal-ar.init`, `hehGoal-ar.medi` | `.notdef` | missing | missing | `heh-ar` skeleton, Urdu joining behavior needs review |
| U+06CC ی | ARABIC LETTER FARSI YEH | Arabic letter | `farsiYeh-ar`, `farsiYeh-ar.fina`, `farsiYeh-ar.init`, `farsiYeh-ar.medi` | `.notdef` | missing | missing | `yeh-ar` skeleton, Persian/Urdu dot behavior needs review |
| U+06D2 ے | ARABIC LETTER YEH BARREE | Arabic letter | `yehBarree-ar`, `yehBarree-ar.fina` | `.notdef` | missing | missing | `alefMaksura-ar` / `yeh-ar` skeleton, Urdu behavior needs review |
| U+06D4 ۔ | ARABIC FULL STOP | Arabic punctuation | `fullStop-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06DB | ARABIC SMALL HIGH THREE DOTS | Arabic mark | `smallHighThreeDots-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F0 ۰ | EXTENDED ARABIC-INDIC DIGIT ZERO | Arabic number | `zeroFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F1 ۱ | EXTENDED ARABIC-INDIC DIGIT ONE | Arabic number | `oneFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F2 ۲ | EXTENDED ARABIC-INDIC DIGIT TWO | Arabic number | `twoFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F3 ۳ | EXTENDED ARABIC-INDIC DIGIT THREE | Arabic number | `threeFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F4 ۴ | EXTENDED ARABIC-INDIC DIGIT FOUR | Arabic number | `fourFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F5 ۵ | EXTENDED ARABIC-INDIC DIGIT FIVE | Arabic number | `fiveFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F6 ۶ | EXTENDED ARABIC-INDIC DIGIT SIX | Arabic number | `sixFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F7 ۷ | EXTENDED ARABIC-INDIC DIGIT SEVEN | Arabic number | `sevenFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F8 ۸ | EXTENDED ARABIC-INDIC DIGIT EIGHT | Arabic number | `eightFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+06F9 ۹ | EXTENDED ARABIC-INDIC DIGIT NINE | Arabic number | `nineFarsi-ar` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+0763 ݣ | ARABIC LETTER KEHEH WITH THREE DOTS ABOVE | Arabic letter | `kehehThreedotsabove-ar`, `kehehThreedotsabove-ar.fina`, `kehehThreedotsabove-ar.init`, `kehehThreedotsabove-ar.medi` | `.notdef` | missing | missing | `keheh-ar` plus three-dot-above pattern after `keheh-ar` exists |
| U+2039 ‹ | SINGLE LEFT-POINTING ANGLE QUOTATION MARK | Shared punctuation/symbol | `guilsinglleft` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+203A › | SINGLE RIGHT-POINTING ANGLE QUOTATION MARK | Shared punctuation/symbol | `guilsinglright` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+20AC € | EURO SIGN | Shared punctuation/symbol | `Euro` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+2122 ™ | TRADE MARK SIGN | Shared punctuation/symbol | `trademark` | `.notdef` | missing | missing | draw/review as standalone shared glyph |
| U+25CC ◌ | DOTTED CIRCLE | Shared punctuation/symbol | `dottedCircle` | `.notdef` | missing | missing | needed for mark specimens and mark attachment proofing |

## Reuse Prerequisite Audit

These rows check whether suggested Arabic source reuse bases already exist in both active masters. They do not replace drawing review; they only verify that the referenced skeleton or dot helper names are available before new glyphs are built.

| Codepoint | Target glyphs | Reuse prerequisites | Regular prerequisites | Bold prerequisites |
| --- | --- | --- | --- | --- |
| U+0679 ٹ | `tteh-ar`, `tteh-ar.fina`, `tteh-ar.init`, `tteh-ar.medi` | `teh-ar`, `teh-ar.fina`, `teh-ar.init`, `teh-ar.medi`, `twodotsverticalabove-ar` | ready | ready |
| U+067E پ | `peh-ar`, `peh-ar.fina`, `peh-ar.init`, `peh-ar.medi` | `behDotless-ar`, `behDotless-ar.fina`, `behDotless-ar.init`, `behDotless-ar.medi`, `threedotsdownbelow-ar` | ready | ready |
| U+0686 چ | `tcheh-ar`, `tcheh-ar.fina`, `tcheh-ar.init`, `tcheh-ar.medi` | `hah-ar`, `hah-ar.fina`, `hah-ar.init`, `hah-ar.medi`, `threedotsdownbelow-ar` | ready | ready |
| U+0688 ڈ | `ddal-ar`, `ddal-ar.fina` | `dal-ar`, `dal-ar.fina` | ready | ready |
| U+0691 ڑ | `rreh-ar`, `rreh-ar.fina` | `reh-ar`, `reh-ar.fina` | ready | ready |
| U+0698 ژ | `jeh-ar`, `jeh-ar.fina` | `reh-ar`, `reh-ar.fina`, `threedotsupabove-ar` | ready | ready |
| U+06A9 ک | `keheh-ar`, `keheh-ar.fina`, `keheh-ar.init`, `keheh-ar.medi` | `kaf-ar`, `kaf-ar.fina`, `kaf-ar.init`, `kaf-ar.medi` | ready | ready |
| U+06AF گ | `gaf-ar`, `gaf-ar.fina`, `gaf-ar.init`, `gaf-ar.medi` | `kaf-ar`, `kaf-ar.fina`, `kaf-ar.init`, `kaf-ar.medi`, `gafsarkashabove-ar` | ready | ready |
| U+06BE ھ | `hehDoachashmee-ar`, `hehDoachashmee-ar.fina`, `hehDoachashmee-ar.init`, `hehDoachashmee-ar.medi` | `heh-ar`, `heh-ar.fina`, `heh-ar.init`, `heh-ar.medi` | ready | ready |
| U+06C1 ہ | `hehGoal-ar`, `hehGoal-ar.fina`, `hehGoal-ar.init`, `hehGoal-ar.medi` | `heh-ar`, `heh-ar.fina`, `heh-ar.init`, `heh-ar.medi` | ready | ready |
| U+06CC ی | `farsiYeh-ar`, `farsiYeh-ar.fina`, `farsiYeh-ar.init`, `farsiYeh-ar.medi` | `yeh-ar`, `yeh-ar.fina`, `yeh-ar.init`, `yeh-ar.medi` | ready | ready |
| U+06D2 ے | `yehBarree-ar`, `yehBarree-ar.fina` | `alefMaksura-ar`, `alefMaksura-ar.fina`, `yeh-ar`, `yeh-ar.fina` | ready | ready |
| U+0763 ݣ | `kehehThreedotsabove-ar`, `kehehThreedotsabove-ar.fina`, `kehehThreedotsabove-ar.init`, `kehehThreedotsabove-ar.medi` | `kaf-ar`, `kaf-ar.fina`, `kaf-ar.init`, `kaf-ar.medi`, `threedotsupabove-ar` | ready | ready |

## Batch Work Plan

These batches group the same `GF_Arabic_Core` gaps by production
dependency so drawing work can move in source-compatible passes.
The per-codepoint table above remains the source of truth for
which encoded characters are still missing.

| Order | Batch | Codepoints | Source glyph names | Notes |
| ---: | --- | ---: | ---: | --- |
| 1 | Shared punctuation and symbols | 28 | 28 | Also reduces Latin Core shared punctuation gaps. |
| 2 | Extended Arabic-Indic digits | 10 | 10 | Draw encoded digit defaults before numeral proofing. |
| 3 | Urdu/Persian joining letters | 13 | 44 | Includes default, final, initial, and medial forms where required. |
| 4 | Arabic punctuation and symbols | 3 | 3 | Review directionality and Arabic text rhythm in proof strings. |
| 5 | Arabic marks | 3 | 3 | Pair with dotted circle, anchors, and mark/mkmk proofing. |

## Batch Glyph Lists

### Shared punctuation and symbols

- Codepoints: U+002B +, U+003C <, U+003D =, U+003E >, U+0040 @, U+005B [, U+005D ], U+005E ^, U+0060 `, U+007B {, U+007C \|, U+007D }, U+007E ~, U+00A2 ¢, U+00A3 £, U+00A5 ¥, U+00A9 ©, U+00AB «, U+00AE ®, U+00B0 °, U+00BB », U+00D7 ×, U+00F7 ÷, U+2039 ‹, U+203A ›, U+20AC €, U+2122 ™, U+25CC ◌
- Source glyphs: `Euro`, `asciicircum`, `asciitilde`, `at`, `bar`, `braceleft`, `braceright`, `bracketleft`, `bracketright`, `cent`, `copyright`, `degree`, `divide`, `dottedCircle`, `equal`, `grave`, `greater`, `guillemotleft`, `guillemotright`, `guilsinglleft`, `guilsinglright`, `less`, `multiply`, `plus`, `registered`, `sterling`, `trademark`, `yen`

### Extended Arabic-Indic digits

- Codepoints: U+06F0 ۰, U+06F1 ۱, U+06F2 ۲, U+06F3 ۳, U+06F4 ۴, U+06F5 ۵, U+06F6 ۶, U+06F7 ۷, U+06F8 ۸, U+06F9 ۹
- Source glyphs: `eightFarsi-ar`, `fiveFarsi-ar`, `fourFarsi-ar`, `nineFarsi-ar`, `oneFarsi-ar`, `sevenFarsi-ar`, `sixFarsi-ar`, `threeFarsi-ar`, `twoFarsi-ar`, `zeroFarsi-ar`

### Urdu/Persian joining letters

- Codepoints: U+0679 ٹ, U+067E پ, U+0686 چ, U+0688 ڈ, U+0691 ڑ, U+0698 ژ, U+06A9 ک, U+06AF گ, U+06BE ھ, U+06C1 ہ, U+06CC ی, U+06D2 ے, U+0763 ݣ
- Source glyphs: `ddal-ar`, `ddal-ar.fina`, `farsiYeh-ar`, `farsiYeh-ar.fina`, `farsiYeh-ar.init`, `farsiYeh-ar.medi`, `gaf-ar`, `gaf-ar.fina`, `gaf-ar.init`, `gaf-ar.medi`, `hehDoachashmee-ar`, `hehDoachashmee-ar.fina`, `hehDoachashmee-ar.init`, `hehDoachashmee-ar.medi`, `hehGoal-ar`, `hehGoal-ar.fina`, `hehGoal-ar.init`, `hehGoal-ar.medi`, `jeh-ar`, `jeh-ar.fina`, `keheh-ar`, `keheh-ar.fina`, `keheh-ar.init`, `keheh-ar.medi`, `kehehThreedotsabove-ar`, `kehehThreedotsabove-ar.fina`, `kehehThreedotsabove-ar.init`, `kehehThreedotsabove-ar.medi`, `peh-ar`, `peh-ar.fina`, `peh-ar.init`, `peh-ar.medi`, `rreh-ar`, `rreh-ar.fina`, `tcheh-ar`, `tcheh-ar.fina`, `tcheh-ar.init`, `tcheh-ar.medi`, `tteh-ar`, `tteh-ar.fina`, `tteh-ar.init`, `tteh-ar.medi`, `yehBarree-ar`, `yehBarree-ar.fina`

### Arabic punctuation and symbols

- Codepoints: U+0609 ؉, U+060D ؍, U+06D4 ۔
- Source glyphs: `dateSeparator-ar`, `fullStop-ar`, `perMille-ar`

### Arabic marks

- Codepoints: U+0615, U+0658, U+06DB
- Source glyphs: `noonGhunna-ar`, `smallHighTah-ar`, `smallHighThreeDots-ar`

## Batch Order Suggestion

1. Shared punctuation and symbols that are also needed by Latin Core.
2. Extended Arabic-Indic digits U+06F0-U+06F9.
3. Urdu/Persian joining letters and their positional forms.
4. Missing Arabic marks plus U+25CC dotted circle.
5. Source anchors and built `mark`/`mkmk` features.
