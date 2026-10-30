# LAT-001 batch38 · Superior-digit assessment

Read-only assessment at `4a940d06`. All1,825 active source files and all five
compiled font hashes remain exact. No drawing, alias, feature, grade, metric,
kerning or build-input edit. Arabic326/master and green131 Regular/74 Bold stay
unchanged; Arabic live proof60272 and Runebender are untouched.

## Coverage, normalization and feature behavior

There are no named superior/numerator donors in either UFO and no U+00B9,
U+00B2 or U+00B3 cmap entries. Virtua also has no `sups` or `numr` GSUB feature.
The existing `one`, `two`, `three` drawings are green in both masters, including
the RGBA-only grades. Their full reverse component closure has three members
per master and no Arabic intersection. The `tnum` feature selects separate
`.tf` glyphs; this is a shaping dependency, not a component relationship.

`assessment.json` retains complete donor points, grades, exact source snapshots,
all source/font hashes, glyph bounds, feature inventory and60 shaping cases,
each in four feature modes, at400/475/550/625/700. Encoded¹²³ return `.notdef`
in direct Virtua shaping; `sups=1` on123 leaves ordinary figures unchanged.
Rubik has encoded superior forms; its `sups` output for123 uses those same
glyphs. `numr` selects separate numerator glyphs in Rubik.

These three Unicode decompositions are compatibility `<super>` mappings:
NFD preserves¹²³, while NFKD yields123. Replacing text with the latter would
discard the superior distinction; it is not a coverage repair. See the
[Unicode Latin-1 chart](https://www.unicode.org/charts/PDF/U0080.pdf).
OpenType `sups` is an optional substitution feature, separate from encoded
character support; the [OpenType specification](https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt#tag-sups)
describes designed superior forms rather than ordinary-size aliases.

Forty real in-memory subset cases, each with default and `sups` shaping, cover
the same five weights. Virtua's missing characters stay missing. Rubik encoded
superiors survive requested-text subsetting. For plain123, fontTools' default
layout-feature set drops Rubik `sups`; retaining all features preserves it.
Thus encoded coverage, optional feature support and serving-subset retention
must be verified separately. No subset font is a source/release candidate.

## Actual visual review

Five full FreeType/RAQM images were inspected:48px contexts at400/550/700 and
224px endpoint details. Missing Virtua rows are explicitly unavailable; no
fallback is passed off as a Virtua drawing. Initial enlarged fixture rows
overlapped labels; vertical spacing was corrected and both final details
were re-rendered and inspected.

Fifteen actual browser screenshots were inspected: three controlled side-by-side
fixtures, plus six Diffenator supplement and six stock first-viewport images.
The controlled browser supplies visibly different fallback superior ink for
Virtua (the actual fallback font was not identified). The Diffenator supplement
instead displays missing-glyph boxes for Virtua. Rubik's encoded and feature
superiors are visible at all three weights. This difference is renderer/CSS
context, not evidence of Virtua coverage. `browser-review.json` records hashes.

Rubik's superior flat height is350 of1000UPM, with baseline350 and cap700;
its2 reaches705 and3 descends345. These are comparison measurements only,
not outline sources or a mandated Virtua metric. Virtua's normal one has a
curved flag and three has two rounded bowls, unlike Rubik's angular3 top.
Keep those Virtua identities in future drafts. The inherited Bold figure mass,
stock text density and uneven spacing remain human-review issues.

## Next bounded drawing scope

Prepare new purple `onesuperior`, `twosuperior`, `threesuperior` in both masters,
using the frozen green Virtua figure construction while leaving donors exact.
Test a half-cap-height starting envelope (nominal384 high, baseline384) and
optical stem/counter corrections in scratch; these are trial values, not
approved dimensions. Preserve the16-unit exposed cuts instead of blindly
scaling them to8. New points, placement and advances must be on8; retain
Regular three's636 advance in its protected donor, not as a new-width target.
Review the complete small figures and exponent/footnote contexts before applying.

Do not add ordinary-size cmap aliases or normalize text to erase superiors.
Start with the three encoded glyphs; any `sups` implementation needs a separate
coherent figure-family scope and explicit subset checks. No partial feature or
automatic ordinary-digit substitution is introduced by this assessment.

This batch does not rerun a build, preflight or full Fontspector. Latest package
QA remains batch37 **12 FAIL/10 WARN/159 PASS/10 INFO/40 SKIP**, with216 existing
Hebrew engineering failure subcases. Soft-hyphen retain/omit and serving mappings
remain unresolved. Pinned Rubik gap338 encodings remains unchanged:182 Cyrillic,
54 Common,102 Arabic presentation forms. No human/native-reader or release approval.
Local evidence only; no push or publication.

[Controlled comparison](http://127.0.0.1:60273/batch38/comparison-400.html) ·
[Diffenator supplement](http://127.0.0.1:60273/batch38/comparison/superiors.html)
