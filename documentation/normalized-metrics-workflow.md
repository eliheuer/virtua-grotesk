# Normalized metrics workflow

How to compare Virtua's drawings against reference fonts (Inter, Geist) in a
**scale-independent** way, so you can reason about weight, spacing, and
proportion — especially the relationship *between* groups of glyphs (caps vs
lowercase, round vs straight). This is the reusable version of the ad-hoc
measurement done during the lowercase n/o design pass.

Tool: `scripts/normalize_metrics.py` · shortcut: `make metrics`

---

## Why ratios, not raw numbers

Raw font-unit sizes are meaningless across fonts. Inter is drawn on a
1118-unit x-height, Virtua on 576, Geist on 530 — a stem of "180" in Inter and
"96" in Virtua tells you nothing on its own. What a designer actually tunes is
**relationships**, and relationships survive scaling:

- contrast — round stroke vs straight stroke (`o side / n stem`)
- case relationship — how much heavier/looser caps are than lowercase
  (`H stem / n stem`, `H sb / n sb`)
- openness — sidebearing relative to counter or stroke (`n sb / n counter`)
- overshoot — round top thickness vs its side (`O crown / O side`)
- proportion — `cap height / x-height`, `O width / o width`

Every row of the report is a ratio. Read it **across the row**: Virtua's value
next to Inter's. Inter is the north star for "text typeface that behaves"; the
gap tells you whether Virtua is heavier, tighter, more open, and by how much.
The gap is information, not a verdict — Virtua is intentionally tighter and
more display-leaning than Inter, so some divergence is on purpose. The table
tells you *where* and *how much*; whether that's right is a design call.

## How the measurement works

For each glyph we cast a **scan line** and read the crossings:

- **Horizontal scan** at a fixed fraction of the glyph's reference height
  (x-height for lowercase, cap-height for caps). Two uprights (`H`, `n`) give
  4 crossings → `stem, counter, stem`. A round (`O`, `o`) also gives 4 →
  `side, counter, side`. So `weight = xs[1]-xs[0]`, `counter = xs[2]-xs[1]`.
- **Vertical scan** at the horizontal center of a round gives the **crown**
  (top overshoot thickness) = `ys[-1]-ys[-2]`.
- **Sidebearings** come from the glyph bbox and advance width:
  `sbL = xmin`, `sbR = advance - xmax`.

Everything (UFO cubics, TTF quads) is flattened to polylines first, so one
crossing routine serves every source. Variable reference fonts are instanced
to `wght=400` before measuring.

### The one gotcha: extrema tangency

A round's side extremum sits *exactly* at its vertical center, so a scan line
placed there grazes the outline tangentially and finds **zero** crossings (a
vertex lands on the line). The `robust()` helper handles this: if a scan
doesn't yield enough crossings, it nudges the line by ±2, ±4 … up to ±12
units. A stroke's thickness is near-constant right next to its extremum, so
the small offset gives the true value while dodging the tangency. If you ever
see `nan` in the weight/crown columns, this is why — widen the offsets or
check the glyph has the expected number of contours.

## Running it

```sh
make metrics                                   # H O n o  vs Inter, Geist
python3 scripts/normalize_metrics.py --glyphs H O n o l I
python3 scripts/normalize_metrics.py --master Bold
python3 scripts/normalize_metrics.py --refs inter        # just one reference
```

(Use the repo venv: `./.venv/bin/python scripts/normalize_metrics.py`, or
`make metrics` which points at it.)

The report has two parts:

1. **Ratio tables**, grouped `[WEIGHT] [SPACING] [PROPORTION]`, columns
   `Virtua | Inter | Geist`.
2. **RAW** font units per glyph — *not* comparable across fonts, but useful
   for spotting which side of a ratio moved (e.g. is `O/o` high because O is
   heavy or o is light?) and for setting an actual coordinate once you've
   decided the target ratio.

## Adding glyphs or reference fonts

- **New glyph**: add it to `GLYPH_SPEC` in the script as
  `glyph: (case, kind, hfrac)` where `case` is `cap`/`lc`, `kind` is
  `stem`/`round`, and `hfrac` is where to cast the horizontal scan as a
  fraction of the reference height. Pick a band **clear of crossbars and
  arches** — `H`'s stems are scanned at 0.72 (above its mid crossbar), `n` at
  0.45 (below its arch).
- **New reference**: add a name → TTF path to `REF_FONTS`. Variable fonts are
  instanced to `wght=400` automatically.
- **New ratio row**: add to `build_rows()`. Each row declares the glyphs it
  needs, so rows silently drop when you measure a smaller glyph set.

## The workflow, end to end

1. Draw / edit the glyph in Runebender (the live measurement HUD shows
   handle/stem/counter/sidebearing lengths and popcount colors as you work).
2. Save the UFO.
3. `make metrics` (add `--glyphs` for whatever you're comparing).
4. Read each ratio against Inter. Decide the **target ratio** for anything
   that's off in a way you don't intend.
5. Convert the target ratio back to a coordinate using the RAW numbers, keep
   it on the 2-unit grid and popcount-friendly, edit, save, re-measure.
6. Continuity/smoothness still outranks popcount — see `DESIGN.md`. The metric
   table is about *proportion*; it doesn't see curve quality. Use it alongside
   `make lint-curves` and the Runebender curvature tools, not instead of them.

Findings from specific passes (e.g. the H/O/n/o cap-vs-lowercase study) live
in `documentation/design-pass-worklog.md`, not here — this file is the method.
