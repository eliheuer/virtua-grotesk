# Arabic Bold — the weight contract

The green Arabic is byte-identical in both masters, so the Arabic has never
been emboldened. This is the measured basis for doing it.

Two references were measured, and they disagree — deliberately, the font's
own Latin wins.

## What Rubik does (reference for BEHAVIOUR only)

`scripts/rubik_weight_deltas.py`, Rubik Light (300) vs Black (900), UPM 1000:

| Quantity | Light → Black | ratio |
|---|---|---|
| Vertical stem (alef, lam) | 60 → 180 | ×3.0 |
| Horizontal / round strokes | 60–66 → 155–210 | ×2.5–3.1 |
| Dots | 94 → 188 | ×2.0 |
| Advance | median | ×1.11 (+70) |
| Tooth top (behDotless.init) | 354 → 473 | +119 |
| hah bowl top | 344 → 519 | +175 |
| Ascender (alef, lam) | 750 → 750 | unchanged |

Rubik's Light→Black is a far wider range than Virtua's 400→700, so the
ratios are not transferable. What IS informative:

- **The silhouette grows outward.** Rubik does not hold the outer contour
  and shrink the counter; every bound expands.
- **Ascender height is held**, but the *tooth and bowl heights rise* with
  weight. This is a real Arabic convention — the small forms grow toward
  the tall ones so the texture stays even.
- **Dots grow with the stroke** (×2 here), they do not stay a fixed size.
- **Advances grow modestly**, about a tenth.

## What Virtua's own Latin does (the rule to follow)

`scripts/latin_weight_deltas.py`, Regular vs Bold, UPM 1024:

| Stroke | Regular → Bold | delta |
|---|---|---|
| lc stem (n, m, l) | 96 → 192 | **+96** |
| lc round, left/right (o) | 98 → 196 | **+98** |
| lc round, top/bottom (o) | 85 → 153 | **+68** |
| cap crossbar (H), cap horizontals (E) | 96 → 168 | **+72** |

Vertical zones are held exactly: `n` is 0..592 in both masters, `H` is
0..768 in both. The left sidebearing is held (72 in both). The glyph grows
to the right, and the advance absorbs it (median ×1.10).

**The model this implies** is an anisotropic (elliptical) outline offset:
grow ink by **+48 per side horizontally** and **+36 per side vertically**.

Check against the measurements:

| Stroke | Regular | model | actual Bold |
|---|---|---|---|
| lc stem (vertical edges, 2 × 48) | 96 | 192 | 192 ✓ |
| cap horizontal (2 × 36) | 96 | 168 | 168 ✓ |
| o sides (2 × 48) | 98 | 194 | 196 ✓ |
| o top/bottom (2 × 36) | 85 | 157 | 153 ✓ |

So **dx = 48, dy = 36** reproduces Virtua's Latin bold to within a couple of
units across every stroke class. That is the contract for the Arabic.

## Arabic-specific constraints

These are what make the Arabic harder than the Latin, and they override the
plain offset:

1. **Joining must not break.** Every joining glyph carries a bar along the
   baseline (Regular y 0..104) and an entry stub at x = −16 with the run
   (0,0) (−16,16) (−16,88) (0,104). Every glyph that joins must agree on
   these to the unit, so they are canonicalised after emboldening rather
   than offset: Bold bar **y 0..176**, stub **x −16 with y 16..160**.
2. **The baseline is hard.** Ink must not grow below y = 0 where it sits on
   the baseline, or joined letters step.
3. **The vertical envelope is hard**: WinAscent 1094 / WinDescent 438.
4. **Master compatibility**: point count, point type and component list must
   stay identical to Regular. The offset moves points; it never adds them.

## What was actually applied

**dx 36 / dy 27**, not the Latin's 48 / 36.

The Latin amounts were tried first and produced a Black, not a Bold: the
Arabic forms are about a quarter shorter than the Latin (tooth top 432
against x-height 576), so the same absolute offset ate their counters —
`meem-ar`'s knot counter went to a slit and `hah-ar.init`'s nearly closed.
Scaling the offset by that height ratio (×0.75) gives 36 / 27, which is
what shipped. Arabic vertical stems go 96 → 168 against the Latin's 192,
which is also the conventional relationship: Arabic set slightly lighter
than Latin reads as the same colour because it is denser.

Command:

```sh
./.venv/bin/python scripts/embolden.py --dx 36 --dy 27
```

It reads Regular and writes Bold every time, so it is idempotent and safe
to re-run with different amounts.

### Three guards the offset needs

Found the hard way; each is now in the script.

1. **Winding is not uniform in the green Arabic.** Some outer contours are
   CW, some CCW. Rotating the tangent by a fixed −90° therefore pointed
   INTO the ink for part of the set and *thinned* those glyphs. `away_sign`
   decides per contour from its own winding and nesting depth.
2. **Coincident points.** `ain-ar.medi`, `seen-ar.init` and `reh-ar` repeat
   a point at a notch vertex. Offsetting the copies independently turns the
   zero-length segment between them into a reversed one — an open corner,
   which `EraseOpenCornersFilter` then DELETES at build time, silently
   breaking master compatibility. `unify_coincident` keeps them together.
3. **Open corners generally.** Rather than guess which corners are unsafe,
   the script runs the real `EraseOpenCornersPen` as an oracle and backs
   the offset off for that glyph until the filter leaves it alone. The same
   loop also enforces the vertical envelope.

### Glyphs that could not take the full offset

15 of 146, listed by the script on every run. These are shapes with a
detail too small to offset — the reh tail's hook, the below-dot clusters
which are already near the descent limit:

| ×0.10–0.18 | threedotsdownbelow, threedotsupbelow, twodotsverticalbelow |
| ×0.40 | heh.medi, jeh.fina, **reh, reh.fina**, rreh.fina |
| ×0.55–0.85 | hamzabelow, damma, fehDotless.init, hehGoal(.fina), hehDoachashmee(.fina) |

**`reh-ar` and `reh-ar.fina` matter most** — reh is common, and at ×0.40 it
reads lighter than its neighbours in Bold text. The honest fix is to redraw
the reh tail for Bold by hand; offsetting cannot invent the room.

## Open for Eli

- **Is 36 / 27 the right weight?** The script makes any other value a
  one-line re-run. 48 / 36 matches the Latin exactly but is too black for
  these forms as drawn.
- **Should the Arabic zones rise with weight?** Rubik raises the tooth
  (+119) and bowl (+175) precisely so counters survive the weight. Virtua's
  Latin holds its zones, and this pass followed the Latin. Raising the
  Arabic tooth from 432 in Bold is the lever that would let the Arabic
  carry the full Latin weight without closing up.
- **The 5 reduced non-mark glyphs** (reh family, heh.medi) want hand
  redrawing for Bold.
