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
3. Suggest: "Run `make reports-only` to refresh master compatibility, or `make preflight` for a fresh build plus checks"

## Glyph Name Reference
Common mappings: `A` → `A_.glif`, `a` → `a.glif`, `period` → `period.glif`, `comma` → `comma.glif`, `space` → `space.glif`, `zero`–`nine` for digits, `exclam`, `question`, `semicolon`, etc.

For accented characters: `aacute`, `egrave`, `ntilde`, etc.
