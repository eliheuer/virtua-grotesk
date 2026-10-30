# RUNBOOK — Anchor-Sheet Glyph Production

Operating procedure for adding or rebuilding glyphs in Virtua Grotesk from
reference images or donor glyphs. Written for any coding agent (Codex,
Claude Code, etc.). The canonical rules live in
`.agents/skills/anchor-sheet-glyphs/SKILL.md` and its **`LESSONS.md`** —
read both before every session; LESSONS outranks everything here.

## Ground rules (violations = rejected work)

1. **FLAT RULE** — sources are figure and ground. NO overlapping contours,
   ever. Compose from donors, then flatten with a boolean union
   (`booleanOperations`, cubic-aware) and clean up.
2. **Winding** — outer contours counter-clockwise, counters clockwise.
3. **START RULE** — every contour starts at its lower-left on-curve point
   (leftmost, then lowest).
4. **EXTREMA RULE** — on-curve points sit AT curve extrema with
   axis-aligned tangents; segments between extrema are monotonic. No
   redundant points.
5. **G2** — smooth curve-curve joints target curvature continuity;
   line↔curve joints must be tangent; kinks are bugs.
6. **Grammar** — 2-unit grid (all coordinates even), 16-unit 45° bevels on
   terminals/corners, 8-unit notch flats, stroke weights from the class
   palette (see SKILL.md constants). Math axis 352, math stroke 72/132.
7. **Master compatibility** — Regular and Bold must have identical
   contour/point structure. Donor copies keep donor point order
   (`normalize=False` in `symbol_gen.write`); never re-rotate start
   points independently per master.
8. **Never** save UFOs through defcon/ufoLib/norad full-font saves — write
   individual `.glif` files only (see CLAUDE.md/AGENTS.md footguns).
9. **Mark protocol** — finished work is marked **blue**
   (`0.27,0.44,1,1` markColor) = awaiting Eli's grade. Only Eli makes
   things green. If Eli reviewed something as deficient, it is orange.
10. **When Eli corrects your output**: diff his edit, extract the rule,
    APPEND it to LESSONS.md in the same session, and teach the generator
    to reproduce his file exactly (round-trip test).

## The pipeline, per glyph class

- **Line-grammar glyphs** (math, punctuation, arrows, bars): generate
  parametrically in `scripts/symbol_gen.py` — add a `gen_<name>()`,
  register it in `GENERATORS`. Never trace these.
- **Derivations**: when a mirror/family/scale partner exists green, derive:
  mirror (backslash←slash), rotate 180° (¡←!, ¿←?), scale (ª←a, º←o,
  ©-inner←c), compose+union ($←S+bar). Mirror about ink center for mark
  components (grave←acute).
- **Organic/curvy glyphs** (Arabic, §-class): trace with img2bez from an
  anchor-calibrated crop, then style-refit (in progress — raw traces are
  marked orange until the refit stage lands).

## Commands

```sh
# 1. Calibrate a sheet (image with a known green glyph, usually n, first):
./.venv/bin/python scripts/anchor_sheet.py SHEET.png n glypha glyphb:2 ... \
    --json /Users/eli/Temp/sheet.json
# name:N = glyph spans N image columns (dieresis:2). Cross-check one
# measured stroke against a system expectation before trusting the sheet.

# 2a. Parametric/derived: add gen_<name>() to scripts/symbol_gen.py, then
./.venv/bin/python scripts/symbol_gen.py <name> ...

# 2b. Traced (img2bez): crop the glyph span, PASTE ONTO WHITE (padding must
# not bleed neighbor ink), synth-bold by PIL MinFilter if no Bold source
# (start at kernel 27; verify counters survive), then:
export IMG2BEZ_LOG="$HOME/.img2bez/virtua-grotesk-traces.jsonl"
img2bez masters sources/VirtuaGrotesk.designspace --glyph NAME --unicode XXXX \
  --image Regular=crop.png --image Bold=crop-bold.png \
  --fit " <bottom>:<top>" --lsb 32 --rsb 32 --profile clean --report r.json
# fit band = the sheet-calibrated extent. Read the report: compatible must
# be true; lowConfidence=true means review carefully.

# 3. Gates (ALL must pass before showing anything):
./.venv/bin/python scripts/curve_continuity.py Regular <names>   # exit 0
./.venv/bin/python scripts/curve_continuity.py Bold <names>      # exit 0
./.venv/bin/python scripts/curve_lint.py Regular <names>         # curves only
make build                                                        # compat
# 4. Visual proof at both weights (shaped text via uharfbuzz on the BUILT
# font — render big, look at it before showing Eli). Save renders to
# ~/Temp/. A render you did not look at does not count as verification.
```

## Verification checklist per glyph

- [ ] bbox / advance / axis match the plan (assert numerically)
- [ ] stroke scans at two heights hit the class palette values
- [ ] continuity gate exit 0 both masters
- [ ] `make build` green (this is the master-compatibility check)
- [ ] rendered big at wght 400 and 700 and actually looked at
- [ ] marked blue; committed with a descriptive message (no AI credits)

## Current queue (2026-07-29)

1. Flatten the remaining overlay constructions per the FLAT RULE, ONE AT A
   TIME with full gates: `yen`, `euro`, `cent`, `sterling`, `registered`.
   Follow the dollar precedent in LESSONS (union hazards: per-master
   sliver segments, rounding-induced kinks).
2. Parametric leftovers: guillemets (chevron grammar), `degree`, `macron`.
3. Refresh stale W/Y accent composites (re-center marks, re-mark blue).
4. Sheets from Eli as they arrive: asterisk, paragraph, at, orange polish
   set, Bold accent marks.

## Do not touch

- Makefile render/proof targets, designbot scripts, `documentation/proofs`
  tooling (owned by a parallel designbot-migration workstream).
- Kerning beyond what a glyph's advance change strictly requires.
- Anything marked GREEN (graded, locked) — derive from it, never edit it.
