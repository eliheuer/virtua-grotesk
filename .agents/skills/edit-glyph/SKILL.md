---
name: edit-glyph
description: Read, display, and edit a glyph in the UFO sources. Use for inspecting or modifying an existing glyph's outline, advance width, or sidebearings.
---

# /edit-glyph

Read, display, and edit a glyph in the UFO sources.

## Usage
`/edit-glyph <glyph-name> [--master regular|bold|both]`

Default master: `regular`

## Instructions

### Step 1: Locate the Glyph
1. Read `sources/VirtuaGrotesk-Regular.ufo/glyphs/contents.plist`
2. Find the `<key>` matching the glyph name
3. The `<string>` value is the filename (e.g., `A_.glif`)
4. If `--master both` or `--master bold`, also look up in the Bold master's contents.plist

### Step 2: Read & Display Current State
Read the `.glif` file(s) and present:
- **Advance width**
- **Number of contours** and points per contour
- **Bounding box** (min/max x and y from all points)
- **Sidebearings:** LSB = min(x), RSB = advance_width - max(x)
- **Point listing** per contour (formatted as a table with x, y, type)

If showing both masters, display side-by-side and highlight any structural differences.

### Step 3: Wait for Edit Instructions
Ask the user what they'd like to change. Common operations:

**Change advance width:**
Edit the `<advance width="N"/>` value.

**Change left sidebearing:**
Calculate delta = new_LSB - current_LSB. Add delta to ALL x-coordinates in the glyph. This shifts the entire glyph.

**Change right sidebearing:**
Calculate new_width = max(x) + desired_RSB. Update `<advance width>`.

**Move specific points:**
Edit the `x` and `y` attributes of specific `<point>` elements.

**Scale the glyph:**
Multiply all x,y coordinates by a factor. Recalculate advance width.

### Step 4: Apply Edits
1. Use the Edit tool to modify the `.glif` file(s)
2. Ensure all coordinates remain integers (preferably multiples of 2)
3. Preserve XML format and point order exactly

### Step 5: Validate
1. Re-read the edited file(s) to confirm changes
2. If both masters were edited, verify structural compatibility:
   - Same number of contours
   - Same number of points per contour
   - Same point types in same order
3. Suggest: "Run `make reports` to refresh `documentation/source/master-compatibility.md`, or `make preflight` for a full build and gate"

## Glyph Name Reference
Common mappings: `A` → `A_.glif`, `a` → `a.glif`, `period` → `period.glif`, `comma` → `comma.glif`, `space` → `space.glif`, `zero`–`nine` for digits, `exclam`, `question`, `semicolon`, etc.

For accented characters: `aacute`, `egrave`, `ntilde`, etc.

For iterative design work, read
[Design review and feedback](../../../agent-proofs/FEEDBACK.md)
and the latest open review. Record Eli's correction, interpretation, exact scope,
and proposal/application state before the next edit. Keep agent suggestions
separate from confirmed rules. Reference comparisons use
`scripts/proof_reference.py`; preserve selected evidence with the review.

### Machine-draft grid gate

Read the cross-script construction and lattice rules in `DESIGN.md`. For new
or redrawn scratch outlines, run `scripts/draft_grid_check.py` on the named
glyphs in both scratch UFOs. This checks all points/handles, anchors, advances
and ink sidebearings on 8 and records descriptive measurement popcounts.
Do not normalize green optical geometry or infer a human grade from QA.
Retain the source/proof evidence and feedback in `agent-proofs/cases/`.
