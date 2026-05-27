# Kerning Proof Review

This generated packet makes the Google Fonts visual QA proof review
auditable for humans and agents. It does not approve spacing or
kerning by itself; it records the proof files that must be opened and
reviewed after `make kerning-proof-check`.

## Summary

- Proof directory: `documentation/gftools-qa/Proof`
- Proof directory exists: yes
- Expected HTML proofs present: 16 / 16
- Expected instances covered: yes
- Embedded proof font exists: yes
- Review status: pending human visual review

## Expected Proof Files

| Instance | Proof type | Present | Size | Review focus |
| --- | --- | --- | --- | --- |
| Regular | `glyphs` | yes | 25661 bytes | missing, blank, malformed, clipped, or wrong-codepoint glyphs |
| Regular | `proofer` | yes | 28518 bytes | tight/loose pairs, sidebearing rhythm, and weight-specific spacing |
| Regular | `text` | yes | 11152 bytes | texture breaks, script fallback, and awkward repeated patterns |
| Regular | `waterfall` | yes | 9872 bytes | size-specific spacing, weight balance, and interpolation jumps |
| Medium | `glyphs` | yes | 25658 bytes | missing, blank, malformed, clipped, or wrong-codepoint glyphs |
| Medium | `proofer` | yes | 28440 bytes | tight/loose pairs, sidebearing rhythm, and weight-specific spacing |
| Medium | `text` | yes | 11149 bytes | texture breaks, script fallback, and awkward repeated patterns |
| Medium | `waterfall` | yes | 9851 bytes | size-specific spacing, weight balance, and interpolation jumps |
| SemiBold | `glyphs` | yes | 25664 bytes | missing, blank, malformed, clipped, or wrong-codepoint glyphs |
| SemiBold | `proofer` | yes | 28596 bytes | tight/loose pairs, sidebearing rhythm, and weight-specific spacing |
| SemiBold | `text` | yes | 11155 bytes | texture breaks, script fallback, and awkward repeated patterns |
| SemiBold | `waterfall` | yes | 9893 bytes | size-specific spacing, weight balance, and interpolation jumps |
| Bold | `glyphs` | yes | 25652 bytes | missing, blank, malformed, clipped, or wrong-codepoint glyphs |
| Bold | `proofer` | yes | 28284 bytes | tight/loose pairs, sidebearing rhythm, and weight-specific spacing |
| Bold | `text` | yes | 11143 bytes | texture breaks, script fallback, and awkward repeated patterns |
| Bold | `waterfall` | yes | 9809 bytes | size-specific spacing, weight balance, and interpolation jumps |

## Review Checklist

- Open every `*-diffbrowsers_proofer.html` file and inspect common
  kerning pairs, uppercase/lowercase rhythm, punctuation spacing,
  numeral spacing, and mixed-script strings.
- Open every `*-diffbrowsers_text.html` file and inspect paragraph
  texture for uneven color, fallback glyphs, missing Arabic shaping,
  and excessive sidebearings.
- Open every `*-diffbrowsers_waterfall.html` file and inspect size
  changes, weight interpolation, and spacing at small and large sizes.
- Open every `*-diffbrowsers_glyphs.html` file and inspect blank,
  malformed, clipped, duplicate, or wrongly encoded glyphs.
- Compare Regular, Medium, SemiBold, and Bold before accepting a
  kerning deferral; the proof can show weight-specific spacing
  problems even when automated checks are unchanged.
- Rerun `make kerning-check` and `make preflight` after review notes
  are resolved or after an explicit kerning deferral is recorded.

## Proof Types

| Proof type | Purpose |
| --- | --- |
| `glyphs` | glyph-by-glyph outline and encoding scan |
| `proofer` | browser-style strings for spacing, rhythm, and kerning |
| `text` | paragraph/text texture and fallback review |
| `waterfall` | size progression and weight interpolation review |

## Commands

```bash
make kerning-proof-check
make kerning-proof-review-check
make kerning-check
make preflight
```

References:

- https://googlefonts.github.io/gf-guide/onboarder-workflow.html
- https://googlefonts.github.io/gf-guide/testing.html
- https://googlefonts.github.io/gf-guide/tools.html
- https://github.com/googlefonts/gftools
