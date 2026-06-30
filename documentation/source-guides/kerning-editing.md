---
paths:
  - "sources/**/*kerning*"
  - "sources/**/*groups*"
---

# Kerning Editing Rules

## Current State

- **Both masters are kerned.** Regular and Bold each have `kerning.plist` and
  `groups.plist`, over the same group set (89 groups each, required for
  interpolation). Regular ~84 pairs, Bold ~77 pairs. (This guide previously said
  Regular had no kerning — that is out of date.)

## File Locations

| File | Bold | Regular |
|------|------|---------|
| Kern pairs | `sources/VirtuaGrotesk-Bold.ufo/kerning.plist` | (missing) |
| Kern groups | `sources/VirtuaGrotesk-Bold.ufo/groups.plist` | (missing) |

## Plist Format

### kerning.plist
Nested dict: first key = left side (glyph name or `public.kern1.*` group), second key = right side (glyph name or `public.kern2.*` group), value = integer kern value.

```xml
<key>public.kern1.A</key>
<dict>
    <key>public.kern2.T</key>
    <integer>-128</integer>
    <key>public.kern2.V</key>
    <integer>-128</integer>
</dict>
```

### groups.plist
Maps group names to arrays of glyph names:
```xml
<key>public.kern1.o</key>
<array>
    <string>c</string>
    <string>o</string>
    <string>p</string>
</array>
```

## Group Naming Conventions

- `public.kern1.*` — left-side groups (first glyph of pair). Named after representative glyph.
- `public.kern2.*` — right-side groups (second glyph of pair). Named after representative glyph.
- Groups contain glyphs with similar shapes on the kerning side (e.g., `public.kern1.o` contains c, o, p — all have similar right-side profiles)

## Kerning Hierarchy

Lookup priority (most specific wins):
1. Glyph + Glyph (e.g., `f` → `g`)
2. Glyph + Group (e.g., `f` → `public.kern2.o`)
3. Group + Glyph (e.g., `public.kern1.f` → `g`)
4. Group + Group (e.g., `public.kern1.A` → `public.kern2.T`)

## Value Conventions

- All kern values are integers
- Prefer multiples of 8 for consistency (the Bold master uses 8, 16, 24, 32, 48, 64, 96, 128, etc.)
- Negative values = tighter (most common)
- Positive values = looser (rare, used for optical compensation)
- Typical range: -288 to +16

## Init-Regular Strategy

To create Regular kerning from Bold:
1. Copy Bold's `groups.plist` to Regular (groups should be identical between masters)
2. Copy Bold's `kerning.plist` to Regular as starting point
3. Scale values — Regular typically needs less kerning than Bold (narrower strokes = less white space to compensate). Start at ~60-75% of Bold values, rounded to nearest 8.
4. Fine-tune by building and visually proofing

## Safety Rules

1. Groups must be identical between masters for variable font interpolation
2. If adding a kern pair to one master, add it to the other too (can be value 0 if no kerning needed)
3. Don't create circular or conflicting group memberships (one glyph per kern1 group, one per kern2 group)
4. After editing, run `make preflight` to rebuild, refresh reports, and re-run the local Google Fonts handoff gate
