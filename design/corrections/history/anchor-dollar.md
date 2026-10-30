# 2026-07-29 — dollar must use uppercase S (Eli correction)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


**Wrong:** the first flattened dollar used lowercase `s` exactly (Regular
advance 560, body bounds x 40..520 / y -16..592), so the body sat at x-height
and the -96..848 bar looked much too long. The `n$` sheet clearly specifies a
cap-height dollar body: about 4/3 the `n` height.

**Cause:** `symbol_gen._read_glyph("S")` guessed `S.glif`; on the
case-insensitive macOS filesystem that resolved to `s.glif`. UFO glyph names
must be resolved through `contents.plist` (`S` -> `S_.glif`), never by guessed
filenames. The same rule protects uppercase `C` and `R` donors.

**Rule / encoded:** dollar = the real green uppercase `S` verbatim + centered
64/104 bar, y -96..848, cubic-aware union. `symbol_gen._read_glyph` now uses
`contents.plist`; `gen_dollar` unions and removes the two Bold-only sliver
structures so both masters are 3 contours with 45/7/7 points and identical
point types. Regular advance/bounds are 704 / x 40..664; Bold 704 /
x 16..680.
