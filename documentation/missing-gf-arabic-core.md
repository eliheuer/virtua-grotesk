# Missing GF Arabic Core Codepoints

Font: `fonts/variable/VirtuaGrotesk[wght].ttf`
GF Arabic Core required codepoints: 224
Missing codepoints: 57

Google Fonts uses the `glyphsets` package for authoring glyphset definitions. For this family, Arabic support means the first submission must cover `GF_Arabic_Core` at minimum, in addition to the Latin coverage target already tracked separately. This report checks Unicode cmap coverage only; contextual forms, mark behavior, and OpenType layout are tracked in the Arabic shaping smoke test and still need visual proofing.

## Submission target

- Minimum Arabic authoring glyphset: `GF_Arabic_Core`
- Installed `glyphsets` required codepoints: 224
- Current built-font gap: 57
- Coverage source: `glyphsets.unicodes_per_glyphset("GF_Arabic_Core")`

## Arabic letters

Missing: 13

| Codepoint | Character | Unicode name |
| --- | --- | --- |
| U+0679 | ٹ | ARABIC LETTER TTEH |
| U+067E | پ | ARABIC LETTER PEH |
| U+0686 | چ | ARABIC LETTER TCHEH |
| U+0688 | ڈ | ARABIC LETTER DDAL |
| U+0691 | ڑ | ARABIC LETTER RREH |
| U+0698 | ژ | ARABIC LETTER JEH |
| U+06A9 | ک | ARABIC LETTER KEHEH |
| U+06AF | گ | ARABIC LETTER GAF |
| U+06BE | ھ | ARABIC LETTER HEH DOACHASHMEE |
| U+06C1 | ہ | ARABIC LETTER HEH GOAL |
| U+06CC | ی | ARABIC LETTER FARSI YEH |
| U+06D2 | ے | ARABIC LETTER YEH BARREE |
| U+0763 | ݣ | ARABIC LETTER KEHEH WITH THREE DOTS ABOVE |

## Arabic marks

Missing: 3

| Codepoint | Character | Unicode name |
| --- | --- | --- |
| U+0615 |  | ARABIC SMALL HIGH TAH |
| U+0658 |  | ARABIC MARK NOON GHUNNA |
| U+06DB |  | ARABIC SMALL HIGH THREE DOTS |

## Arabic numbers

Missing: 10

| Codepoint | Character | Unicode name |
| --- | --- | --- |
| U+06F0 | ۰ | EXTENDED ARABIC-INDIC DIGIT ZERO |
| U+06F1 | ۱ | EXTENDED ARABIC-INDIC DIGIT ONE |
| U+06F2 | ۲ | EXTENDED ARABIC-INDIC DIGIT TWO |
| U+06F3 | ۳ | EXTENDED ARABIC-INDIC DIGIT THREE |
| U+06F4 | ۴ | EXTENDED ARABIC-INDIC DIGIT FOUR |
| U+06F5 | ۵ | EXTENDED ARABIC-INDIC DIGIT FIVE |
| U+06F6 | ۶ | EXTENDED ARABIC-INDIC DIGIT SIX |
| U+06F7 | ۷ | EXTENDED ARABIC-INDIC DIGIT SEVEN |
| U+06F8 | ۸ | EXTENDED ARABIC-INDIC DIGIT EIGHT |
| U+06F9 | ۹ | EXTENDED ARABIC-INDIC DIGIT NINE |

## Arabic punctuation and symbols

Missing: 3

| Codepoint | Character | Unicode name |
| --- | --- | --- |
| U+0609 | ؉ | ARABIC-INDIC PER MILLE SIGN |
| U+060D | ؍ | ARABIC DATE SEPARATOR |
| U+06D4 | ۔ | ARABIC FULL STOP |

## Shared punctuation and symbols

Missing: 28

| Codepoint | Character | Unicode name |
| --- | --- | --- |
| U+002B | + | PLUS SIGN |
| U+003C | < | LESS-THAN SIGN |
| U+003D | = | EQUALS SIGN |
| U+003E | > | GREATER-THAN SIGN |
| U+0040 | @ | COMMERCIAL AT |
| U+005B | [ | LEFT SQUARE BRACKET |
| U+005D | ] | RIGHT SQUARE BRACKET |
| U+005E | ^ | CIRCUMFLEX ACCENT |
| U+0060 | ` | GRAVE ACCENT |
| U+007B | { | LEFT CURLY BRACKET |
| U+007C | \| | VERTICAL LINE |
| U+007D | } | RIGHT CURLY BRACKET |
| U+007E | ~ | TILDE |
| U+00A2 | ¢ | CENT SIGN |
| U+00A3 | £ | POUND SIGN |
| U+00A5 | ¥ | YEN SIGN |
| U+00A9 | © | COPYRIGHT SIGN |
| U+00AB | « | LEFT-POINTING DOUBLE ANGLE QUOTATION MARK |
| U+00AE | ® | REGISTERED SIGN |
| U+00B0 | ° | DEGREE SIGN |
| U+00BB | » | RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK |
| U+00D7 | × | MULTIPLICATION SIGN |
| U+00F7 | ÷ | DIVISION SIGN |
| U+2039 | ‹ | SINGLE LEFT-POINTING ANGLE QUOTATION MARK |
| U+203A | › | SINGLE RIGHT-POINTING ANGLE QUOTATION MARK |
| U+20AC | € | EURO SIGN |
| U+2122 | ™ | TRADE MARK SIGN |
| U+25CC | ◌ | DOTTED CIRCLE |

