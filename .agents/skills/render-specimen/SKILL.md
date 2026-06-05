# /render-specimen

Render a font specimen image using DesignBot.

## Usage
`/render-specimen [001|002|--text "custom text"]`

Default: `001`

## Instructions

### For numbered scripts (001, 002, etc.):
1. Check that the font exists: `ls fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - If missing, tell the user to run `/build-font` first
2. Run: `designbot --render designbot/NNN.rs --output designbot/NNN.png`
3. Read the rendered PNG file to describe what you see
4. Report the result to the user

### For custom text (`--text "..."`)
1. Read `designbot/001.rs` as a template
2. Create a temporary script at `designbot/tmp_specimen.rs` that:
   - Uses the same canvas setup (2048x2048, dark background)
   - Loads `../fonts/ttf/VirtuaGrotesk-Regular.ttf`
   - Renders the user's custom text at a readable size, centered
3. Run: `designbot --render designbot/tmp_specimen.rs --output designbot/tmp_specimen.png`
4. Read the rendered PNG to describe it
5. Clean up: delete `designbot/tmp_specimen.rs` (keep the PNG for the user to view)

### Image description guidelines
When reading the rendered PNG, describe:
- Overall layout and composition
- Character rendering quality (clean outlines, proper spacing)
- Any visible issues (overlapping glyphs, missing characters, spacing problems)
- How the font looks at the rendered size
