---
paths:
  - "sources/**/*.designspace"
---

# Designspace Editing Rules

## Current Configuration

File: `sources/VirtuaGrotesk.designspace` (format 5)

### Axes
| Axis | Tag | Default | Min | Max |
|------|-----|---------|-----|-----|
| Weight | wght | 400 | 400 | 700 |

### Sources (Masters)
| Name | Filename | Weight |
|------|----------|--------|
| Regular | `VirtuaGrotesk-Regular.ufo` | 400 |
| Bold | `VirtuaGrotesk-Bold.ufo` | 700 |

### Instances
| Style | Weight | Style Map |
|-------|--------|-----------|
| Regular | 400 | regular |
| Medium | 500 | regular |
| SemiBold | 600 | regular |
| Bold | 700 | regular |

## Rules for Editing

### Adding an Instance
Add a new `<instance>` element inside `<instances>`. Follow the existing pattern:
```xml
<instance familyname="Virtua Grotesk" stylename="NAME" name="Virtua Grotesk NAME"
          filename="instance_ufo/VirtuaGrotesk-NAME.ufo"
          stylemapfamilyname="Virtua Grotesk NAME" stylemapstylename="regular">
  <location>
    <dimension name="Weight" xvalue="VALUE"/>
  </location>
</instance>
```

### Adding an Axis
1. Add `<axis>` element with name, tag, default, min, max
2. Add `<dimension>` to EVERY `<source>` and `<instance>` location
3. Create additional master UFOs if needed for the new axis extremes
4. Ensure all masters are compatible (see ufo-editing.md)

### Important
- The `filename` paths in sources are relative to the designspace file location
- Instance `filename` paths use `instance_ufo/` subdirectory (these are generated, not source)
- Do not change source filenames without renaming the actual UFO directories
- Weight values must stay within the axis min/max range
- The `default` axis value must match exactly one source's location
