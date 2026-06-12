---
name: compare-reference
description: Compare a reference image against the current font rendering and propose specific glyph edits. Use when given a reference or target image for a glyph.
---

# /compare-reference

Compare a reference image to the current font rendering and suggest specific edits.

## Usage
`/compare-reference <image-path>`

The image path should point to a reference image (PNG, JPG, etc.) showing the desired font appearance.

## Instructions

Execute these five phases in order:

### Phase 1: Read Reference Image
Read the reference image file at the provided path. Describe in detail:
- What characters/text are shown
- Overall style: stroke weight, proportions, contrast
- Specific features: terminal shapes, counter sizes, serif presence
- Spacing density

### Phase 2: Build & Render Matching Specimen
1. Determine what text is shown in the reference image
2. Build the font if needed: `./build.sh`
3. Render the closest current proof: `make proof` for a general PDF or `make specimen` for spacing/weight review
4. Use the generated PDF pages in `documentation/proofs/` as the current rendering

### Phase 3: Read Current Rendering
Read the generated proof/specimen output and describe the same attributes as Phase 1.

### Phase 4: Compare
Create a detailed comparison covering:
- **Proportions:** Width differences per character, cap-height vs x-height ratio
- **Stroke weight:** Stem thickness, thin/thick contrast
- **Counter shapes:** Open vs closed, round vs angular
- **Terminals:** Flat, angled, rounded
- **Spacing:** Overall density, specific tight/loose pairs
- **Specific characters:** Call out individual glyphs that differ most

### Phase 5: Generate Edit Plan
Produce a prioritized list of changes, from highest to lowest impact:

For each change, specify:
1. Which glyph(s) to edit
2. Which master(s) (Regular, Bold, or both)
3. What specifically to change (advance width, point coordinates, sidebearings)
4. Approximate values if possible (e.g., "widen advance width by ~40 units")

Format as a numbered action list the user can work through with `/edit-glyph`.

**Important:** Remind the user that structural changes (adding/removing points) must be done in both masters to maintain compatibility.
