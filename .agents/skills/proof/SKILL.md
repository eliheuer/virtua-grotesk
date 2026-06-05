# /proof

Generate a multi-page PDF proof document for the font.

## Usage
`/proof [font-path]`

Default font: `fonts/ttf/VirtuaGrotesk-Regular.ttf`

## Instructions

1. Use the project Python environment at `./venv/bin/python`.

2. Check that the font file exists:
   - If no argument given, check `fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - If the font is missing, tell the user to run `/build-font` first

3. Run the proof generator:
   ```bash
   make proof-only
   ```
   Default output: `documentation/proofs/proof.pdf`

4. Read the generated PDF and summarize its contents:
   - Number of pages
   - What each page contains (title, alphabet, numerals, waterfall, spacing, paragraph, kerning, character set, Arabic if present)

5. Report the output path so the user can open it for detailed review

## Notes
- Proof generation uses the local `eliheuer/drawbot-skia` fork at `/Users/eli/GH/repos/drawbot-skia` via `PYTHONPATH`
- The proof includes: title page, alphabet display, numerals & punctuation, size waterfall, spacing proof, paragraph setting, kerning pairs, full character set grid
- For variable font proofs, pass `fonts/variable/VirtuaGrotesk[wght].ttf` to `scripts/build_general_proof.py`
- Output defaults to `documentation/proofs/proof.pdf`
