# /proof

Generate a multi-page PDF proof document for the font.

## Usage
`/proof [font-path]`

Default font: `fonts/VirtuaGrotesk-Regular.ttf`

## Instructions

1. Activate the Python environment:
   ```bash
   source ~/Py/venvs/basic-fonts/bin/activate
   ```

2. Check that the font file exists:
   - If no argument given, check `fonts/VirtuaGrotesk-Regular.ttf`
   - If the font is missing, tell the user to run `/build-font` first

3. Run the proof generator:
   ```bash
   python proof.py [font-path] [output-path]
   ```
   Default output: `proof.pdf`

4. Read the generated PDF and summarize its contents:
   - Number of pages
   - What each page contains (title, alphabet, numerals, waterfall, spacing, paragraph, kerning, character set, Arabic if present)

5. Report the output path so the user can open it for detailed review

## Notes
- The proof script uses DrawBot (Python library) — it must be available in the venv
- The proof includes: title page, alphabet display, numerals & punctuation, size waterfall, spacing proof, paragraph setting, kerning pairs, full character set grid
- For variable font proofs, you can pass the VF file: `/proof fonts/VirtuaGrotesk-VF.ttf`
- Output defaults to `proof.pdf` in the project root
