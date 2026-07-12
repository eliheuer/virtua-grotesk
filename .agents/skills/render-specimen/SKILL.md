---
name: render-specimen
description: Render font specimen and proof output with designbot (main proof or landscape spacing specimen).
---

# /render-specimen

Render font specimen/proof output with designbot (the Rust renderer; scripts in scripts/designbot/).

## Usage
`/render-specimen [proof|spacing]`

Default: `proof`

## Instructions

### For `proof` or default:
1. Check that the font exists: `ls fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - If missing, run `/build-font` first
2. Run `make proof`
3. Report `documentation/proofs/proof.pdf`

### For `spacing`:
1. Check that static fonts exist under `fonts/ttf/`
2. Run `make specimen`
3. Report `documentation/proofs/print-spacing-specimen.pdf`

### Image description guidelines
When reviewing the rendered PDF, describe:
- Overall layout and composition
- Character rendering quality (clean outlines, proper spacing)
- Any visible issues (overlapping glyphs, missing characters, spacing problems)
- How the font looks at the rendered size
