# /proof

Generate a multi-page PDF proof document for the font.

## Usage
`/proof [font-path]`

Default font: `fonts/ttf/VirtuaGrotesk-Regular.ttf`

## Instructions

1. Use the configured DrawBot Python, preferably through Make:
   ```bash
   make proof
   ```
   The Makefile uses the local `eliheuer/drawbot-skia` fork at
   `/Users/eli/GH/repos/drawbot-skia` from the project virtualenv.

2. Check that the font file exists:
   - If no argument given, check `fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - If the font is missing, tell the user to run `make build` first

3. Run the proof generator:
   ```bash
   PYTHONPATH="/Users/eli/GH/repos/drawbot-skia/src${PYTHONPATH:+:$PYTHONPATH}" \
     ./venv/bin/python proof.py [font-path] [output-path]
   ```
   Default output: `proof.pdf`

4. Read the generated PDF and summarize its contents:
   - Number of pages
   - What each page contains (title, alphabet, numerals, waterfall, spacing, paragraph, kerning, character set, Arabic if present)

5. Report the output path so the user can open it for detailed review

## Notes
- The proof script uses DrawBot-style APIs through `drawbot_skia.drawing.Drawing`
  from the local `eliheuer/drawbot-skia` fork. Treat that fork as the supported
  proof runtime for this repo.
- The proof includes: title page, alphabet display, numerals & punctuation, size waterfall, spacing proof, paragraph setting, kerning pairs, full character set grid
- For variable font proofs, pass `fonts/variable/VirtuaGrotesk[wght].ttf`
- Output defaults to `proof.pdf` in the project root
