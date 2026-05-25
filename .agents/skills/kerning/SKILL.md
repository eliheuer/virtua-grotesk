# /kerning

Manage kerning pairs and groups in the UFO sources.

## Usage
`/kerning <add|list|test|init-regular> [options]`

## Actions

### `list`
Read and display the current kerning data:
1. Read `sources/VirtuaGrotesk-Bold.ufo/kerning.plist` and `groups.plist`
2. Check if Regular has kerning: look for `sources/VirtuaGrotesk-Regular.ufo/kerning.plist`
3. Display a summary: number of pairs, groups, and a formatted table of all kern pairs with their values

Format groups as: `kern1.A [A] → kern2.T [T]: -128`

### `add <left> <right> <value> [--master bold|regular|both]`
Add or update a kerning pair:
1. Parse arguments: left side (glyph or group name), right side, integer value
2. If using group names, verify the group exists in `groups.plist`
3. Read the current `kerning.plist`
4. Add/update the pair using the Edit tool
5. If `--master both`, apply to both masters (with appropriate value scaling if desired)
6. Report the change

Group name shorthand: if the user says `kern1.A` interpret as `public.kern1.A`.

### `test`
Build and render a kerning test:
1. Build the font: `./build.sh`
2. Create a temporary designbot script that renders common kerning test strings:
   - `AV AW AT AY VA WA TA YA`
   - `To Te Ta Tr Tu Ty Tw`
   - `Vo Va Ve Vu Vy`
   - `ff fi fl ffi ffl`
   - `oo oc oe og oq`
   - `"A" 'A' "T" 'T'`
3. Render and read the PNG to evaluate kerning quality
4. Report findings

### `init-regular`
Create kerning for the Regular master based on Bold:
1. Read Bold's `groups.plist` and `kerning.plist`
2. Copy `groups.plist` to `sources/VirtuaGrotesk-Regular.ufo/groups.plist` (groups must be identical)
3. Create `sources/VirtuaGrotesk-Regular.ufo/kerning.plist` with scaled values:
   - Scale each Bold kern value to ~65% (Regular needs less kerning)
   - Round to nearest multiple of 8
   - Preserve zero values as zero
   - Clamp small values (if |scaled| < 4, set to 0)
4. Report the number of pairs created and suggest testing with `/kerning test`

## Plist Editing Notes
- Use the Edit tool to modify plist XML
- Maintain proper XML indentation (tabs)
- All kern values must be `<integer>` elements
- Group arrays must contain `<string>` elements
- Preserve the XML declaration and DOCTYPE
