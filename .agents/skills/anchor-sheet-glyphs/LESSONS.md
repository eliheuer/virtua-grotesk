# Lessons — anchor-sheet glyph generation

Running log of optical corrections and workflow findings. Newest first.
Every entry: date, glyph(s), what was wrong, the rule, where it's encoded.
These rules OUTRANK the generator formulas — when in doubt, match the
latest graded (green) example of the same construction.

---

## 2026-08-04 — Arabic completion: derive from green, don't trace the reference

**The finding that made the pass cheap.** A 244-glyph "Arabic cleanup"
was not 244 drawings. It was ~30 skeletons plus rules, because Arabic is
a component script and the green set already contained the init/medi form
of nearly every family. Before generating anything, classify:

1. **recompose** — skeleton + mark component (133 glyphs here)
2. **derive** — a scripted edit on a donor: splice off a joining bar, swap
   a stub for a tail, copy a sibling form (52)
3. **skeleton** — genuinely new drawing (43)
4. **symbol** — parametric digits/punctuation (21)

`scripts/arabic_lanes.py` is the pattern: a rule table over glyph names
that must cover 100% of targets and shouts about anything unmatched. Write
the manifest before the first outline; it turns "a huge amount of work"
into a work-list with a cost per item.

**Two reference roles, never mixed.** Rubik supplied topology and
proportion only (which way a tail sweeps, how deep a bowl goes, what the
positional-form inventory is). The green in-font glyphs supplied every
number. Tracing a rendered reference of a different typeface would have
imported its style and maximized cleanup — the opposite of the goal.

**Recover the placement rule from the graded examples, don't invent it.**
Reading five green composites showed one consistent convention (mark ink
centre → base `topDots`/`bottomDots` anchor x; above-mark ink bottom at
anchor y + 112). Encoding that one rule generated 133 composites. Any time
several graded glyphs share a construction, the rule is in there — measure
it out before hand-tuning offsets.

**Splice helpers beat per-glyph drawing.** `_bowl_replacing_stub` swaps a
donor's left joining stub for a tail for ANY donor that arrives on the bar
bottom at (jx, 0) and leaves on the bar top at (jx, 104). Once a family's
init/medi is green, its isol/fina cost is one function call. Generalize on
the joint, not on the letter.

**Splice bug that costs an hour if you don't gate it:** a replacement run's
first point must inherit the *type* of the donor point it replaces. Give it
`type="curve"` when the preceding donor point is a line and you produce a
curve segment with zero off-curve points; cu2qu then dies with a bare
`IndexError: list index out of range` and no glyph name. `scripts/glif_lint.py`
now names it, along with nested components and master mismatches. **Run
glif_lint before make build** — it is seconds instead of minutes and it
tells you which glyph.

**Google Fonts rejects nested components.** Generated composites nest
easily (mark over a ligature, tanwin built from two harakat). Flatten one
level at write time (`arabic_recompose.flatten()`), not afterwards.

**Auto-placement must be clamped to the font's vertical envelope.** Stacking
marks by an anchor rule happily produced ink at y = −1176 against a declared
WinDescent of 438, which fails `family/win_ascent_and_descent`. Read
`openTypeOS2WinAscent`/`WinDescent` from fontinfo and clamp. Also: for a
glyph with a deep bowl (hah, jeem, ain, qaf) the below-dot belongs INSIDE
the bowl, so the `bottomDots` anchor goes at the bowl's inner edge, not at
the ink bottom — anchoring at the ink bottom pushes the dot below the tail.

**Verify in shaped words, not just glyph sheets.** Per-glyph renders looked
fine while positional forms and mark attachment were still unproven.
`harness/designbot/arabic_words.rs` renders real words from the BUILT
variable font — that is what caught that everything actually joins. For any
script with contextual shaping, this render is the gate, not the sheet.

**Winding normalization is free quality.** `scripts/normalize_winding.py`
fixes outer-CCW/holes-CW by nesting parity as a mechanical edit (shapes
verified unchanged) and only touches blue files, so green stays untouched.
It cut `outline_direction` warnings by two thirds. Note the reverse must be
segment-aware: in glif order a point's type marks the segment ENDING at it,
so a naive `reversed()` corrupts curves. There is a round-trip test for it.

## 2026-07-29 — dollar must use uppercase S (Eli correction)

**Wrong:** the first flattened dollar used lowercase `s` exactly (Regular
advance 560, body bounds x 40..520 / y -16..592), so the body sat at x-height
and the -96..848 bar looked much too long. The `n$` sheet clearly specifies a
cap-height dollar body: about 4/3 the `n` height.

**Cause:** `symbol_gen._read_glyph("S")` guessed `S.glif`; on the
case-insensitive macOS filesystem that resolved to `s.glif`. UFO glyph names
must be resolved through `contents.plist` (`S` -> `S_.glif`), never by guessed
filenames. The same rule protects uppercase `C` and `R` donors.

**Rule / encoded:** dollar = the real green uppercase `S` verbatim + centered
64/104 bar, y -96..848, cubic-aware union. `symbol_gen._read_glyph` now uses
`contents.plist`; `gen_dollar` unions and removes the two Bold-only sliver
structures so both masters are 3 contours with 45/7/7 points and identical
point types. Regular advance/bounds are 704 / x 40..664; Bold 704 /
x 16..680.

## 2026-07-28 — chevron tips need a flat (Eli correction)

**Glyphs:** less, greater (first generated batch).
**Wrong:** generated tips ended edge → 16u bevel → vertical face; the tip
read too pointy.
**Rule:** diagonal-arm tips land on a **16u axis-aligned flat** before the
bevel: outer edge → 16u flat → 16u bevel → face. Same anatomy as V/W/v
baseline terminals. Applies to any arm tip on a line-grammar glyph.
**Encoded:** `symbol_gen.chevron_left` (TIP_FLAT), round-trips Eli's
corrected files exactly.
**Also noted:** Eli kept the notch at its original x (182/322) rather than
the strict inner-parallel recomputation (194 would match the new outer
slope) — a slight arm taper toward the apex is acceptable; don't "fix" it.

## 2026-07-28 — pilot findings (n < = > sheet)

- **Anchor calibration works**: n px-height ↔ 592u gave scale + baseline;
  symbol stroke measured from the sheet (71.2) matched the system-derived
  expectation (hyphen 88 × HN 64/80 = 70.4) within 1u. Always run this
  cross-check; agreement = trust the sheet.
- **The sheet is authoritative**: the pilot sheet was NOT Helvetica Neue
  (HN math axis ≈ 282 vs the sheet's 352). Refs fill gaps (e.g. Bold
  stroke ratio when no Bold sheet exists); they never override the sheet.
- **Math class values set**: axis 352, stroke 72/132, advance 600,
  equal-bar centers ±100 R / ±132 B (gap≈1.78×bar R, ≈1×bar B, per HN).
- **Bold hyphen is unbolded** (88 = Regular value) — on the red list; do
  not use it as the Bold symbol-class anchor until fixed.

## 2026-07-28 — second batch (n [ \ ] ^ _ ` sheet)

- **Mirror-partner rule**: when a glyph's mirror or family partner already
  exists green, DERIVE it instead of tracing: backslash := slash mirrored
  in its advance; greater := less mirrored. Encoded in
  `symbol_gen._mirror_of_source`.
- **Mark components mirror about the INK CENTER, not the advance**: grave
  := acute mirrored about acute's ink center (164), which also matched the
  old grave's center — so every grave-composite's xOffset stayed valid.
  Accent-family consistency (grave matches acute) OUTRANKS the sheet.
- **Sheets give ink, not spacing**: glyph boxes/strokes come from the
  sheet; advances and sidebearings come from class rules or refs (a sheet
  cannot express its font's sidebearings).
- **Always check winding**: first caret came out clockwise and rendered
  invisible in the strict checker. `symbol_gen.write()` now asserts CCW
  (positive signed area) on every contour.
- Underscore: kept the sheet's floating width (ink 464 in adv 600) over
  HN's tiling sb-0 convention; HN also never boldens underscore — followed
  (72 both masters). Flag for Eli's grade.
- Also red-listed: acute (and the whole accent-mark set) is UNBOLDED —
  Bold == Regular. Bolding the marks is a future batch; grave inherits
  this (kept consistent with acute rather than "fixed" alone).

## 2026-07-28 — third batch (n { | } ~ ¡ ¢ sheet) + START RULE

- **START RULE (Eli)**: contour start points go at the LOWER-LEFT on-curve
  point (min y, then min x). Now automatic: `symbol_gen.normalize_start`
  runs in `write()`. Applies to all future generation; existing graded
  glyphs left as-is until a cleanup pass.
- **Rotation vs mirror winding**: 180-degree rotation PRESERVES winding
  (transform in order, no reversal); mirrors REVERSE it (reverse the list
  and shift segment types incoming->outgoing). Encoded as
  `reverse_contour` / `mirror`; the write() assertion catches mistakes.
- Derivations this batch: exclamdown := exclam rotated 180 about its
  advance center, top seated at 656 (family consistency with exclam over
  the sheet's taller proportions); cent := c + lc-stem bar (96/192)
  through the ink center, y -96..656 per sheet.
- First CURVED generations: braces (chevron-style beak + cubic hooks,
  bracket band -128..848) and tilde (cubic S centerline, vertical stroke
  offset, center 370 per sheet). Generator now supports typed points
  (line/curve/offcurve, smooth) — expect these to need Eli polish; log
  the corrections here when they land.

## 2026-07-28 — tilde rebuild + extrema rule (Eli correction)

- **EXTREMA RULE (the img2bez discipline)**: on-curve points go AT the
  extremes — every curve extremum (crest, trough, side extreme) is an
  on-curve point with an axis-aligned tangent; segments between extrema
  are monotonic. The first tilde put on-curves mid-slope and was "close
  to unusable." Any parametric curve construction must place extrema
  first, then fill in handles. For curved shapes too complex to
  parametrize confidently, DELEGATE to img2bez on a calibrated sheet crop
  (it gets extrema right by construction) — that is the preferred path
  for organic/curvy glyphs.
- **START RULE clarified**: lower-left = leftmost first, lowest tiebreak
  (min x, then min y). Min-y-first wrongly started the tilde at its
  trough. All generator glyphs regenerated with the corrected rule.

## 2026-07-29 — G2 rule + terminal anatomy (Eli's tilde edit, saved)

- **G2 RULE**: smooth curve-curve joints target G2 (curvature match), not
  just G1. New gate: `scripts/curve_continuity.py` classifies every joint
  (corner / line<->curve / G1 / G2 / KINK) with the same math as
  Runebender web's continuity overlay; exit 0 required before showing.
  Runebender web has harmonize->G2 / balance handles / optimize for hand
  fixes; Eli's graded tilde measures G2 within 1-4% at every smooth.
- **Wave/terminal anatomy** (from the graded tilde, now in
  gen_asciitilde): terminal = face + 16u bevel + 16u flat; the curve
  LEAVES the flat at a deliberate corner (steep takeoff), and ENTERS the
  opposite terminal's 45-degree bevel TANGENTIALLY (last handle at exactly
  45, joint marked smooth). No pointy meets anywhere — where a curve
  would come to a point, there is always a flat.
- **Derive Bold by per-side offset**: same x-skeleton, bottom-path y -30,
  top-path y +30 (stroke 72->132) — continuity classes carry over
  unchanged (identical checker output for both masters).

## 2026-07-29 — fourth batch (n £ ¥ § ¨ © ª sheet)

- **Multi-part glyphs in sheets**: declare span counts explicitly
  (`dieresis:2`) — a smallest-gap merge heuristic merged the wrong pair
  (crowded £¥). Explicit beats clever.
- **Scaled donors preserve G2**: copyright's inner c (green c x0.74) and
  ordfeminine (a x0.87) pass the continuity gate untouched — scaling
  preserves G-class, so derive-by-scale is a first-class construction.
- **Auto-harmonize**: `symbol_gen.harmonize_g2()` scales adjacent handle
  lengths toward matched endpoint curvature (kappa = 2/3 d/l^2), the CLI
  twin of Runebender's harmonize->G2; sterling's hook apexes went G1->G2
  automatically.
- **Winding rules generalized**: outer CCW, counters CW, decided by
  point-in-polygon nesting parity (bbox tests misclassify overlapped ink
  like yen's bars; parity handles ring-inside-ring-inside-c).
- **Degenerate curve types break the build**: a type="curve" point with no
  offcurves compiles in sources but crashes overlap removal on instances.
  (Candidate: assert in glif() that curve points have 2 offcurves.)
- Values: dieresis = two i-tittles at mark-center 180, gap 88/64;
  yen ink 600/adv 664, bars 72/112 at sheet positions; copyright ring
  dia 832 stroke 44/80 + c x0.74; ordfeminine = a x0.87 seated at 256;
  sterling v1 straight base (sheet wave = upgrade candidate), currency
  sb 32. **section DEFERRED** — proposed as the img2bez pilot (too curvy
  to parametrize honestly; current placeholder is two overlaid S
  components).

## 2026-07-29 — yen fix + section: first img2bez glyph + THE PIPELINE

- **Mirror the donor's topology**: yen v1 routed the outer arm edges into
  the notch and the arms crossed like a bowtie. When a structural cousin
  exists green (Y), copy its PATH ORDER, not just its measurements.
- **SECTION = first img2bez glyph.** Recipe that worked: clean crop
  (paste the span onto WHITE — blind padding bled neighbor ink into the
  trace), synthetic Bold via morphological dilation (PIL MinFilter; size
  27 kept the counters open, 39 sealed one -> contour mismatch), then
  `img2bez masters --fit " -208:784"` with the anchor-calibrated band.
  Report: compatible, 62 pts/master. lowConfidence=true -> review flag.
- **THE PIPELINE (Eli)**: TRACE (img2bez, problems fixed UPSTREAM there,
  not papered over in the harness) -> STYLE REFIT (harness rules today;
  virtua-12m as a learned style-transfer/refit stage tomorrow) -> VERIFY
  (gates) -> Eli grades.
- **Refit v1 failure**: running harmonize_g2 naively over traced output
  corrupted it (assumes generator-clean cubic structure; also bypassed
  the winding checks by writing directly). Refit needs its own careful
  pass; traced G1 joints are ACCEPTED for now (blue = review).
- **img2bez UPSTREAM backlog** (from today): (1) normalize contour
  orientation on output — it emitted outer contours CW; UFO wants outer
  CCW/holes CW (fixed by hand this once); (2) `sheet` mode: anchor
  calibration + span segmentation + name:N built in; (3) synthetic-bold
  option (dilate with counter-preservation guard); (4) optional G2
  harmonization / style-refit hooks, or at least extrema+continuity
  report in the trace JSON.

## 2026-07-29 — img2bez upstream fixes #1 and #2 SHIPPED (b5cb87d)

- img2bez now writes surgically (only the target .glif + contents entry
  for new glyphs) and normalizes winding on output (outer CCW/holes CW by
  nesting parity, with a type-shifting Contour::reverse). Verified on the
  section retrace: 2 files touched (was 638), correct winding unaided.
  Three regression tests in img2bez.
- Remaining upstream: sheet mode (anchor calibration + segmentation),
  synthetic-bold with counter guard, extrema/point-economy on traces
  (section's bottom missed an extremum and wastes points), continuity
  report in trace JSON, and normalize_start order (img2bez uses
  bottom-then-left; the font's START RULE is left-then-bottom).
- **section is marked ORANGE** (Eli's review): raw trace lacks Virtua's
  chamfer terminals and runs light — the STYLE-REFIT stage (harness rules
  / virtua-12m, possibly built on img2bez font/refit.rs which already
  does structure-preserving raster refits) is the missing piece and the
  next build.

## 2026-07-29 — lane-1 derivation batch (no sheets needed)

- Eight glyphs derived without reference images: plus (math-grammar
  cross, 8-fillets at concave junctions), periodcentered (period at axis
  352), ordmasculine (o x0.87, twin of ordfeminine), questiondown
  (question rotated, top 656), dollar (S + 64/104 bar, -88..856), euro
  (C + two bars from x8; Bold bar centers +-90, +-60 overlapped),
  registered (ring + R x0.68; 0.60 read spindly), nbspace (advance =
  space).
- **Donor copies must keep donor point order** (write(normalize=False)):
  normalize_start rotated Regular-S and Bold-S to different indices and
  broke master compatibility in dollar. Parametric glyphs still
  normalize (identical structure both masters by construction).
- Containment for winding = ALL on-curve points inside (single-probe
  misread euro's overlapping bars as nested).

## 2026-07-29 — THE FLAT RULE (Eli) + dollar done right

- **FLAT RULE: no overlapping contours in sources, ever.** The viewer sees
  figure and ground; the sources must be the same flat form. Compose from
  donors, then UNION (booleanOperations, cubic-aware) and clean. This
  supersedes the overlay constructions — dollar rebuilt this way;
  yen, euro, cent, sterling, registered still carry overlays and need the
  same flattening pass (queued).
- **Union recipe**: build overlapped construction in a scratch defcon
  glyph -> BooleanOperationManager.union -> extract typed points -> round
  to 2-grid -> write with donor order (normalize=False) -> gates.
- **Union hazards found on dollar**: (1) masters can flatten to DIFFERENT
  structures (Regular got an 8u sliver segment + extra point where Bold's
  curve landed directly on the bar edge) — diff the masters' on-curve
  sequences and merge slivers so counts match; (2) grid-rounding after
  union can tilt a smooth point past tangency (the 4.3-degree kink) —
  the sliver merge fixed both at once. The continuity gate + fontmake
  compatibility check catch both; never skip them on unions.
- Dollar params from the n$ sheet: bar 64/104 wide, y -96..848, centered
  on the S ink; body = the green S verbatim.
