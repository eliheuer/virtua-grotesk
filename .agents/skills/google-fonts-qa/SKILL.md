# /google-fonts-qa

Run and document Google Fonts QA for a font family. This skill covers the
repeatable checks that should happen before packaging, and it keeps drawing
quality separate from packaging mechanics.

## Usage
`/google-fonts-qa [fontspector|glyphsets|proof|kerning|metadata|all]`

Default: `all`

## Fontspector

1. Build fonts from the active sources.
2. Run Fontspector's `googlefonts` profile on the generated TTFs.
3. Save the report in a durable location under `documentation/`.
4. Classify every FAIL and WARN:
   - fix now,
   - drawing/source blocker,
   - maintainer decision,
   - reviewer-approved exception,
   - false positive or tool limitation with evidence.
5. Do not treat a warning as harmless just because the build succeeds.

Portable command shape:

```bash
make test
# or:
fontspector check-googlefonts fonts/variable/*.ttf fonts/ttf/*.ttf
```

## Glyphset Coverage

1. Determine intended script scope for the first submission.
2. Compare generated font cmaps against `googlefonts/glyphsets`.
3. Track missing codepoints by glyphset and by source glyph work needed.
4. For non-Latin scripts, also track marks, anchors, shaping behavior, and
   script-specific review requirements. Cmap coverage alone is not enough.
5. Keep reusable reports for:
   - missing Latin Core,
   - missing script-specific core set,
   - source work checklist,
   - shaping smoke test,
   - mark/anchor readiness.

## Visual Proof Review

1. Generate proof output after build-output, spacing, kerning, or scope changes.
2. Use `gftools qa --proof` when preparing for Google Fonts review.
3. Confirm every expected instance and proof type exists.
4. Keep a human review checklist that records:
   - proof generation date,
   - fonts reviewed,
   - proof files reviewed,
   - spacing findings,
   - kerning findings,
   - script-specific findings,
   - accepted deferrals.

Portable command shape:

```bash
gftools qa --proof fonts/variable/FamilyName[wght].ttf fonts/ttf/*.ttf
```

If `gftools qa --proof` needs live catalog access for comparisons, note that
network/auth failures are environmental and should not be confused with font
QA results.

## Kerning

1. Check source kerning in every master.
2. Check built GPOS `kern` coverage in every output font.
3. Run proof output and review visually.
4. Either finish kerning before the first PR or record an explicit maintainer
   deferral and explain the Google Fonts review impact in the issue/PR handoff.
5. Do not mark kerning final until both source data and proof review agree.

## Variable Font Metadata

Review at least:

- `name` table family/style/full/PostScript names,
- license strings and URLs,
- version strings,
- `OS/2.fsType`,
- `OS/2` vendor ID,
- `fvar` axis tags, bounds, default, and instance names,
- `STAT` table presence and style linking,
- `meta` `dlng` and `slng` when script metadata is needed,
- `avar` decision for variable axes.

## Final QA Evidence

Before handoff, there should be a current evidence chain from generated fonts
to reports:

- build output exists and is fresh,
- Fontspector report exists and has classified results,
- glyphset coverage reports exist,
- proof output exists and has human review status,
- metadata reports reflect generated binaries, not source assumptions,
- final blocker report points to every relevant report.

