---
paths:
  - "sources/**/*.glif"
  - "sources/**/*.ufo/**"
---

# Design Philosophy & Outline Drawing Conventions

## What Kind of Typeface Is This?

Virtua Grotesk is a **geometric grotesk** with a signature detail: **chamfered (beveled) corners** at every sharp junction. It sits between the geometric sans tradition (Futura, DIN) and rationalist grotesks (Helvetica, Univers), but the chamfers give it a distinct retro-futuristic, technical character — like something from a 1980s computer interface or architecture signage, redrawn with modern precision.

## Core Design Principles

### 1. Monolinear Stroke Weight
Stems, crossbars, and curves all have consistent stroke thickness. There is no visible thick/thin contrast. Weight is achieved purely through stroke width, not stress or modulation.

### 2. The 16-Unit Chamfer
The signature feature. Every sharp corner where two straight segments meet gets a **16-unit diagonal bevel** (in the Regular master). This appears at:
- Stem-baseline junctions: e.g., in `n`, points (80,0)→(144,0)→(160,16)
- Stem-cap height junctions
- Crossbar ends in `A`, `H`, `E`, etc.
- Apex of `A`: both the outer peak and the inner crossbar corners

The chamfer is always a pair of line segments creating a 45-degree cut. In the Bold master, the chamfer size scales proportionally with the heavier weight.

The pattern in coordinates: if a stem meets the baseline at x=160, you'll see three points — `(x-16-stem, 0)`, `(x-16, 0)`, `(x, 16)` — creating the bevel.

### 3. Organic Curves Inside a Geometric Frame
Round forms (O, C, G, e, o, etc.) use smooth cubic Bezier curves with minimal off-curve points. The outer contour is precisely geometric — the O outer is a near-perfect superellipse. But counters are slightly organic, creating visual warmth within the rigid framework.

### 4. Weight Through Counter Reduction
When going from Regular to Bold, the outer contour often stays **identical** (confirmed in O, and similar in other round forms). All weight gain comes from shrinking the inner counter — the walls thicken inward. This is a deliberate interpolation strategy: the font's silhouette stays stable across the weight axis while the interior fills in.

For straight-stemmed letters (n, A, etc.), the stems widen and counters shrink, but the same principle applies — weight is added symmetrically inward.

### 5. Generous Counters and Open Apertures
Regular has wide, open counters. Even the Bold maintains readable counter space. Apertures in `c`, `e`, `s`, `a` are generous — this is not a closed, high-contrast grotesk.

## How to Draw New Outlines

### Straight Stems
1. Draw the stem as a rectangle at the correct width (Regular stems ~96 units, Bold ~160+ units)
2. Add 16-unit chamfers at every corner where the stem meets a horizontal (baseline, x-height, cap height)
3. Chamfer pattern: replace each sharp corner with two points offset 16 units along each edge

### Round Forms
1. Construct the outer path using 4 curve segments (one per quadrant), 4 on-curve extrema, and 8 off-curve points
2. Place on-curve points at the exact horizontal/vertical extremes
3. Overshoots: round forms extend ~16 units below baseline (y=-16) and ~16 units above alignment zones (cap height 784 instead of 768, x-height 592 instead of 576)
4. Counter: inset the outer shape by the stem width, maintaining proportional curves
5. Winding direction: outer contour clockwise, inner counter counter-clockwise

### Mixed Forms (n, a, e, etc.)
1. Start with the straight stem(s), including chamfers
2. Attach curves at the stem-to-arch junction using smooth connections
3. The arch of `n`/`m`/`h` springs from the stem at about 85% of x-height, with off-curve points controlling the shoulder shape
4. Open terminals (like the bottom of `a`'s bowl or `e`'s aperture) get the same chamfer treatment where they terminate

### Spacing Conventions
- Left sidebearing (LSB) and right sidebearing (RSB) are typically balanced for symmetrical letters
- Round forms (O, C, etc.) have tighter sidebearings than straight stems (H, I) — standard optical spacing
- The `a` has LSB=24, suggesting tight left fitting for the bowl shape
- Advance widths are round numbers, often multiples of 8 or 16

### Coordinate Rules
- All coordinates are integers, preferably multiples of 2
- Key measurements use multiples of 8: stem widths, sidebearings, counter sizes
- The 16-unit chamfer is non-negotiable — every new glyph must have it
- Overshoots are typically 16 units (baseline overshoot at y=-16, cap overshoot at y=784)

## Weight Axis Interpolation

When drawing a glyph for both masters:
1. **Same structure**: identical contours, point counts, point types
2. **Same outer boundary** for round forms (only counter changes)
3. **Proportional stem growth** for straight forms
4. **Scale chamfers** with weight (Bold chamfers are larger than Regular's 16-unit default)
5. **Crossbars may shift vertically** — Bold `A` has a lower crossbar than Regular, for optical balance at heavier weight
6. **Test interpolation** at intermediate weights (Medium=500, Semi-Bold=600) to ensure smooth transitions
