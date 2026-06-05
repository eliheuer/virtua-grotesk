# Arabic Review Packet

This generated packet collects the Arabic evidence needed for the Google
Fonts handoff. It does not replace drawing, native-reader review, or
final Fontspector cleanup; it keeps the minimum Arabic target and proofing
tasks visible in one place.

## Summary

- Minimum target: `GF_Arabic_Core`
- Required codepoints: 224
- Missing codepoints: 0
- GF Arabic Core coverage row: `224 / 224 present; 0 missing; 100.00% coverage`
- Missing Arabic letters: 0
- Missing Arabic marks: 0
- Missing Arabic numbers: 0
- Missing Arabic punctuation/symbols: 0
- Missing shared punctuation/symbols: 0
- Suggested source glyph names: 0
- Suggested Arabic source glyph names: 0
- Suggested shared punctuation/symbol glyph names: 0
- Suggested Arabic positional-form glyph names: 0
- Suggested glyph names missing in both masters: 0
- Required mark glyphs present: 16 / 16
- U+25CC dotted circle present: yes
- Source anchors present: yes
- Built mark/mkmk GPOS features present: yes
- Arabic GSUB smoke pass: 5 / 5 fonts
- Arabic GPOS smoke pass: 5 / 5 fonts
- Smoke strings shape without .notdef: yes
- Lam-alef smoke rows passing: 10
- Metadata script record present: yes
- Metadata primary script: `Arab`
- Downstream preview subsets match target: yes
- Downstream preview primary_script matches target: yes
- Compared Arabic package examples present: 9 / 9
- Compared examples with `arabic` subset: 9 / 9
- Compared examples with `primary_script: "Arab"`: 9 / 9
- Compared non-Noto Arabic examples omit `languages`: yes
- Compared non-Noto Arabic examples omit `sample_text`: yes
- Fontspector dotted_circle warning present: no
- Fontspector soft_dotted warning present: no
- Unreachable Arabic helper/form glyphs: 0
- Unreachable Arabic mark helper glyphs: 0

## Drawing And Source Work Buckets

1. Draw 0 shared punctuation and symbol glyphs also needed by Latin Core.
2. Draw Extended Arabic-Indic digits U+06F0-U+06F9.
3. Draw Urdu/Persian joining letters and 0 required positional-form glyph names.
4. Add missing Arabic marks and U+25CC dotted circle.
5. Add source anchors and compile mark/mkmk GPOS features.
6. Resolve or intentionally remove unreachable Arabic helper and mark helper glyphs.
7. Rebuild, regenerate reports, and visually proof shaped Arabic samples.

## Recent Arabic Google Fonts Reference

`documentation/google-fonts/google-fonts-language-metadata.md` compares the current
Virtua metadata target against several Arabic `METADATA.pb` files in
the synced local `google/fonts` checkout. Estedad remains the closest
recent new-family package in that set; the broader table is package
metadata evidence, not a drawing model for Virtua Grotesk.

- Package path: `ofl/estedad`
- Source repo: `https://github.com/aminabedi68/Estedad`
- Source commit: `69e879f78a4a1c7c4594baf7da13ba1c9f65ffd3`
- Source branch: `master`
- Primary script: `Arab`
- Subsets: `arabic, latin, latin-ext, menu, vietnamese`
- Variable source file under `fonts/variable/`: yes
- `source.config_yaml`: `sources/config.yaml`
- Downstream `upstream_info.md`: yes

Implications for Virtua Grotesk:

- Keeping `primary_script: "Arab"` is aligned with a recent Arabic-script
  new-family package while Arabic remains in first-submission scope.
- `source.config_yaml` has recent Arabic-script precedent, but only when the
  final Packager source strategy deliberately supports a reproducible source
  build.
- Estedad exposes its served variable font from `fonts/variable/`; Virtua's
  generated-font policy still needs the separate Packager source-strategy
  decision recorded in `documentation/google-fonts/google-fonts-decisions.md`.

## Evidence Reports

- `documentation/google-fonts/missing-gf-arabic-core.md`
- `documentation/glyph-review/arabic-source-work-checklist.md`
- `documentation/glyph-review/arabic-mark-readiness.md`
- `documentation/glyph-review/arabic-shaping-smoke-test.md`
- `documentation/google-fonts/google-fonts-language-metadata.md`
- `documentation/google-fonts/gf-glyphset-readiness.md`
- `documentation/google-fonts/recent-google-fonts-packages.md`
- `documentation/google-fonts/glyph-reachability.md`
- `documentation/google-fonts/fontspector-warnings.md`

## References

- https://googlefonts.github.io/gf-guide/requirements.html
- https://googlefonts.github.io/gf-guide/lang.html
- https://github.com/googlefonts/glyphsets

The source glyph worklist is intentionally kept in
`documentation/glyph-review/arabic-source-work-checklist.md` so drawing work can
use the per-codepoint UFO/master status table directly.
