---
name: proof
description: Generate the multi-page PDF proof document for the font. Use to review the current state of drawing, spacing, and rhythm.
---

# /proof

Generate a multi-page PDF proof document for the font.

## Usage
`/proof [font-path]`

Default font: `fonts/ttf/VirtuaGrotesk-Regular.ttf`

## Instructions

1. Use the project Python environment at `./.venv/bin/python`.

2. Check that the font file exists:
   - If no argument given, check `fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - If the font is missing, tell the user to run `/build-font` first

3. Run the proof generator:
   ```bash
   make proof
   ```
   Default output: `documentation/proofs/proof.pdf`

4. Read the generated PDF and summarize its contents:
   - Number of pages
   - What each page contains (title, alphabet, numerals, waterfall, spacing, paragraph, kerning, character set, Arabic if present)

5. Report the output path so the user can open it for detailed review

## Notes
- Proof generation uses **designbot** (Rust): `make proof` runs
  `designbot --render scripts/designbot/general_proof.rs --output documentation/proofs/proof.pdf -- <font_path>`
- The proof includes: title page, alphabet display, numerals & punctuation, size waterfall, spacing proof, paragraph setting, kerning pairs, full character set grid, Arabic
- For variable font proofs, pass `fonts/variable/VirtuaGrotesk[wght].ttf` as the font argument after `--`
- Output defaults to `documentation/proofs/proof.pdf`
