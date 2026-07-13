# Design-pass worklog — sources vs the blog contract

Running log of the glyph-by-glyph review of A–Z and a–z against the
design contract published in the Virtua Grotesk blog post
(`~/GH/repos/elih.net/src/content/blog/virtua-grotesk/index.mdx`,
§03). Goal: everything conforms to the contract **before the next
training run**, so the corpus teaches the model the system, not the
exceptions.

**How to use this file (humans and agents):** one entry per glyph as
it is reviewed. Record measurements, contract verdicts, decisions Eli
made (and WHY), and anything still open. Decisions here are design
decisions — agents never resolve an OPEN item by editing sources;
they measure, propose, and log. Append; don't rewrite history — if a
decision is reversed, add a dated follow-up entry.

## The contract being checked (blog §03, quick reference)

- UPM 1024, drawing grid 2. Ascender 768, cap height 768,
  x-height 576, descender −256. Chamfers 16u.
- Two-lattice rule: **8u grid = machine/structural** (stems,
  sidebearings, chamfers, tool offsets); **2u = human optical
  corrections**. A point off-8-but-on-2 self-labels as a deliberate
  optical correction.
- Stroke table (Regular / Bold): lowercase stem 96/192, lowercase
  bar 88/152, uppercase stem 104/200, uppercase bar 96/160,
  lowercase curve vert 100/196, lowercase curve horiz 92/156,
  uppercase curve vert 110/192, uppercase curve horiz 102/184.

## Cross-glyph issues (apply to many entries)

- **C1 — off-8 points in machine drafts pollute the self-labeling
  rule.** Ungraded (orange) Bold drafts carry off-8 points introduced
  by the transfer tool. Until graded, those wear the "human optical
  correction" label falsely. Resolution during grading: snap each
  back to 8, or move it deliberately and own it. Status: OPEN,
  resolves glyph-by-glyph as the pass proceeds.
- **C2 — overshoot policy is real in the sources but absent from the
  blog.** Round crowns/basins exceed flat heights by 16u (one chamfer
  unit), on the 8-grid, both masters. Candidate blog addition: one
  Dimensions-table row ("Overshoot: 16"). Status: OPEN (blog edit is
  Eli's, via the blog agent).
- **C3 — Bold lowercase stems measure 184 mid-glyph across many
  drafts** (see documentation/grading-worklist.md) vs contract 192.
  **RESOLVED 2026-07-12: contract stands at 192; drafts are
  systematically 8u light and get corrected during the pass.**
  Eli's call, after this analysis (keep for the blog / future agents):
  - **Interpolation stays on-grid only with 192.** wght 400–700 with
    Medium/SemiBold at t=1/3, 2/3: stems 96→192 (delta 96) give
    instance stems of exactly 128 and 160 — every named weight on the
    8-grid. 96→184 (delta 88) gives 125.33 at Medium: off-grid,
    non-integer. The two-lattice thesis holds across the whole
    variable space only if master stems differ by a multiple of 24
    (and of 8): 96 works.
  - **UC−lc stem gap stays parallel**: Regular 104−96=8, Bold
    200−192=8. At 184 the Bold gap would be 16 for no stated reason.
  - **Bold = exactly 2× Regular** — the kind of relationship the
    system celebrates; 184 is legal (23×8) but meaningless.
  - Counterargument acknowledged: 2× is dark for a 400→700 grotesk
    and Bold counters lose ~35% vs Regular. Remedy is advance width /
    counter, not an off-system stem (8u ≈ only 4% lighter anyway).
  First application: Bold n redrawn (see entry) — counters opened by
  widening the advance to 704, exactly the predicted remedy.
- **C5 — co-centered elements must differ in width by a multiple of
  16, or one of them leaves the 8-grid.** Discovered on Regular i
  (see entry). An element of width w centered at c has edges on the
  8-grid iff c ≡ w/2 (mod 8). Two elements sharing a center (stem +
  dot of i/j, stem + diacritics, etc.) can therefore both sit on the
  8-grid only when their widths are congruent mod 16. Stem 96 +
  dot 104 (Δ8) is structurally impossible; dot 96 or 112 (Δ0/Δ16)
  works. This is a theorem of the system, not a taste call — worth a
  line in DESIGN.md and possibly the blog. Status: rule established;
  sweep dot/mark widths for compliance (i j dotlessi period colon
  semicolon exclam question dieresis dotaccent...).
- **C4 — shoulder-basin anatomy consistency** (h vs n arch springing
  differs by ~28u; check m, u too). Both legal per the grid; optics
  question. Status: OPEN.

- **C6 — how much does the Bold WIDEN? The masters currently follow
  three different rules.** Advance growth Regular→Bold: O +0 (848→848,
  identical outer per DESIGN.md counter-reduction), H +48 (768→816),
  o +48 draft (632→680), n +112 (592→704, Eli's redraw). Counter
  loss: O −30%, H −36%, n −29%, o −35%. DESIGN.md says round forms
  keep an "often identical" outer contour — Bold O honors it, but the
  new wide Bold n makes a fixed-width Bold o/O look pinched next to
  it. Needs one rule (or one deliberate exception list) across OHno
  before the rest of the Bold is graded. Status: OPEN — Eli decides
  while drawing Bold o.
- **C8 — Bold BAR values break the on-grid-instances property.**
  The instance math that makes stems/bowls land on the 8-grid at
  Medium/SemiBold needs Regular→Bold deltas that are multiples of 24.
  Stems (96) and bowls (96) comply. Bars don't: cap bar 96→160 and
  lc bar 88→152 are delta 64 → Medium bars = 117.33/109.33,
  non-integer. Options: Bold bars +8 (cap 168, lc 160; delta 72 →
  instances 120/144 and 112/136, all on-8; makes the Bold rule
  "bar = stem − 32" in both cases, vs Regular's "bar = stem − 8"),
  or accept rounded instance bars and soften the blog claim.
  **H RESOLVED 2026-07-13 (agent edit, Eli-directed, pending his
  eyeball):** Regular bar moved down 8 to 352..448 (center 400 =
  cap center + 16 — joins the font's +16 constant family; edges on
  the 32-grid). Bold bar 304..472 = 168 thick (center 388). Edge
  deltas −48/+24 (multiples of 24) → instance bars 336..456 (120)
  and 320..464 (144), all edges on-8 at every named weight:
  96→120→144→168. Bar center drifts +16→+4 across the axis
  (conventional: heavy bars sit nearer true center). DESIGN.md cap
  bar updated 160→168 same commit. STILL OPEN for lowercase bars
  (88→152, delta 64): e/f/t/A-bar etc. need the same treatment when
  reviewed.
  **FINAL 2026-07-13: Eli's eye read the +16 lift as low; both bars
  moved up 8 in the editor. Final: Regular 360..456 (center 408 =
  +24), Bold 312..480 (center 396). Deltas −48/+24 unchanged, so the
  instance property is intact (96/120/144/168, edges on-8). Blog
  lesson: the grid offered two legal positions; the eye picked —
  the division of labor working as designed.**
- **C7 target numbers (2026-07-13), for the Bold O redraw:** keep
  outer 48..800 / −16..784; inner x extrema at **252 and 596** (bowl
  204 = cap stem 200 + 4, edges off-8-by-4, self-labeling); inner y
  extrema at **152 and 616** (horizontal 168 = new cap bar exactly,
  matching the Regular's "curve horizontal = bar" rule: 96=96,
  88=88). Instance check: bowl 108→204 (delta 96) gives 140/172 =
  instance cap stems 136/168 + 4 — the +4 rule propagates for caps
  exactly as it does for the lowercase; inner-y deltas +72/−72 also
  multiples of 24. Regular O already conforms (bowl 108 = 104+4,
  horiz 96 = bar) — no Regular changes needed.
- **C7 — Bold cap round is LIGHTER than the cap stem.** Regular
  follows "rounds slightly wider than flats" (+6 UC, +4 lc). Bold
  lowercase follows it (+4: 192→196). Bold uppercase inverts it:
  stem 200, O bowl 192 in the table, 188 at the extremum in the
  green source. One weight class contradicts the stated principle —
  either intentional (big bold rounds self-compensate) or drift.
  Status: OPEN.

## THE core example of the two-lattice system (Eli, 2026-07-12)

The Regular n/o pair is the canonical illustration of the blog's
optical-correction thesis — use it everywhere (blog, DESIGN.md,
teaching agents):

- n stem = **96** — pure ladder, machine lattice, every edge on 8.
- o bowl side = **100** — curves need to be a touch heavier than
  flats to read as equal, so the eye adds **+4: exactly half an
  8-unit**, the smallest meaningful step of the human lattice.
- The coordinates tell the story by themselves: o outer edge x=32
  (on 8, structural), inner edge x=132 (off-8 by 4, on 2 — the
  point self-labels as the optical correction). The machine drew the
  outside; the human moved the inside.
- Same constant uppercase: O inner edge 156, off-8 by 4; bowl at the
  extremum 108 = cap stem 104 + 4. **Regular rule: curve = stem + 4
  at the extremum.** (DESIGN.md's table value 110 for the O is a
  chord scan @ y=500, not the extremum — both true, different
  measuring points.)
- TODO for the blog (Eli / blog agent): add this as the flagship
  example in §03. Status: OPEN.

## H spacing + cap-stem rationale (2026-07-13) — BLOG ILLUSTRATION MATERIAL

Eli confirmed Regular H stem 104 and SB 80 during the OHno pass.
The reasons, mined for blog illustrations:

- **Cap stem 104 = lowercase stem + 8**, and the Regular→Bold delta
  is 96 for BOTH (104→200, 96→192) — so at Medium/SemiBold (t=1/3,
  2/3) cap stems hit 136/168 and lc stems 128/160: the "+8 caps"
  relationship holds at every instance, all on the 8-grid.
- **The H square**: SB 80 makes the Regular H advance
  80+104+400+104+80 = 768 = cap height. The H occupies a perfect
  square. (Illustration: H inside a 768×768 box.)
- **One-sentence spacing rule**: caps get one 16-unit more air than
  their lowercase counterparts (H 80 = n 64 + 16; O 48 = o 32 + 16),
  and rounds get 32 less than flats in both cases (64→32, 80→48).
- **80 is optically conservative, not loose**: SB/counter ratio is
  n 64/272 ≈ 0.235 vs H 80/400 = 0.20 — caps at 80 are already
  relatively tighter than the lowercase; 72 would read cramped in
  cap-heavy settings.
- **The +4 curve rule propagates through interpolation**: o bowl
  100→196 (delta 96, same as stems) gives instance bowls 132/164 =
  instance stems 128/160 + 4. The optical correction survives the
  whole axis, off-8-by-4 at every weight. (Strong illustration:
  the correction as a constant ribbon across the axis.)

## FULL A–Z a–z GRID PASS (started 2026-07-13) — Eli-directed

Mandate: snap all 52 to the system, HOno = source of truth for
weight (DESIGN.md may be stale — verify against sources, update
table as we go). Greens may be edited (go blue). Redraws allowed.
Diagonals: optical weight, endpoints on-grid. Handle lengths prefer
16/8 when tension shift is imperceptible, else 4/2.

**Derived truth (measured from HOno sources, both masters):**
stems lc 96/192, caps 104/200; curve-vert = stem+4 (100/196,
108/204); curve-horiz lc 92/140, caps 100/148; bars lc 80/152
(NOT 88 — DESIGN/blog value was stale; e/f/t sources say 80; the
"adopt 160" decision was corrected to 152 = 80+72, keeping
cap bar = lc bar + 16 in both masters: 96/80, 168/152);
growth quanta: curve-horiz +48, bars +72, verticals +96;
SB flat 64 lc / 80 cap, round 32 lc / 48 cap; overshoot ±16;
chamfer 16, joint chamfer 8; n seam = (264,512)(256,512)(248,560)
(232,576) Bold / (168..136, 512..576) Regular.

**Audit result (2026-07-13):** zero floats, zero off-2 points, zero
master incompatibilities in A–Z a–z. Debt = 17 off-8 advances +
off-8-not-4 points + stroke misfits (Bold lowercase transfer drafts
have stems 168–184 and three different bar values).

**Batch 1 DONE (blue):** u := rot180(n) in BOTH masters — exact
construction from the anchor (Reg adv 592, basin 92; Bold adv 704,
basin 140); Regular e (adv 608, side 100, horizontals 92 = o's);
Regular f (adv 352, bar-end RSB 16 = t); Regular r (arm 92);
Bold t (stem 192, bar 152, tail top 152 = bar, junk fillet
rebuilt, foot handles on-8); Bold f (stem 192, bar 152, adv 384,
hook junction rebuilt); Bold r (stem 192, arm 140, seam = n's).
All verified: strokes exact, on-2 everywhere, structures match.

**Open flags:** f hook horizontal is 80/128 (matches bar in
Regular, matches nothing in Bold) vs curve-horiz 92/140 — left
as-is, Eli decides. Regular t foot handle (96,32)(128,0) fine.

**Batch 2 CORRECTION (2026-07-13):** the first Bold e attempt
(bar 152 + right side +32) MANGLED the glyph — Eli caught it against
NHG Bold. Reverted, redone minimally: **the e bar is its OWN value,
not the f/t bar** (NHG Bold e bar ≈ 0.55 stem): Regular 80 → Bold
104 (delta 24, instances 88/96). Final Bold e: side 196, top/bottom
140, bar 104 (248..352), width UNCHANGED (adv 640; the o-parity
widening is dropped — e ink vs o ink differs 16 Reg / 48 Bold,
logged as an open proportion question for Eli). PROCESS RULE
re-learned: render (glyph_canvas glyphbox/sheet) and LOOK after
every outline edit before committing — numeric checks alone missed
this completely.

**Batch 2 DONE (blue):** m both masters (stems 104/184 -> 96/192 at
64/408/752-anchored positions, counters equalized 248/248 Reg and
152/152 Bold, crowns 92/140, seams = n exactly, adv 912/1008);
Bold e (side 196, horizontals 140, bar 152 at 200..352, ink +32 ->
32..640, adv 680 so SBs 32/40 match Regular). All verified.

**Remaining worklist:** rounds c C G Q (align to o/O DNA);
b d p q g (bowl+stem hybrids; d/p/q/b relate by rotation like u/n);
straights E F L I J (bars/arms vs 96/168); diagonals A V W X Y K k
v w x y z N M Z (optical, endpoints on-8); two-story a, S/s
(redraw allowed), B D P R U (bowl caps). Advances to snap: K 676,
g 618, p 618, A 692, B 716, c 580, k 540, q 628, x 514, y 524,
N 774, D 756, R 668, Z 604, j 244.

## Reference proportions: Inter / Geist / Helvetica (measured 2026-07-13)

Measured from local sources (google-fonts checkout, system Helvetica)
per Eli's rule: when unsure on HOno, check the core references.
Remarkably tight consensus across all three:

| metric | refs Regular | refs Bold | Virtua R | Virtua B |
| --- | --- | --- | --- | --- |
| n ink / x-height | 0.79–0.82 | 0.90–0.91 | **0.81 ✓** | 1.00 (wide: display-dark bold) |
| o ink / x-height | 0.91–0.93 | 0.98–1.02 | 0.96 | 1.08 |
| o ink / n ink | 1.13–1.15 | 1.07–1.14 | 1.19 | 1.08 |
| o adv / n adv | 0.99–1.02 | 0.99–1.01 | 1.04 | **0.98 ✓** |
| O w/h | 0.86–0.92 | 0.91–0.93 | 0.94 | 0.94 |

Findings:
- **"Is the Regular o too narrow?" — NO.** At ink 552 it is already
  a notch WIDER than every reference (0.96 vs 0.91–0.93 of x-height).
  The agent's 576 experiment overshot; reverted to Eli's 552.
  Virtua's identity: rounds run ~one notch rounder than the
  neo-grotesk baseline at every weight (O 0.94 vs refs 0.86–0.92,
  o likewise) — consistent, intentional, keep.
- **Regular n is reference-perfect** (0.806 vs Helvetica 0.815).
- **Bold o widened 608→624 ink (adv 688) KEPT**: brings o_adv/n_adv
  to 0.98 (dead-on refs), relieves the slit counter by 16, and keeps
  the one-notch-rounder identity in the Bold.
- Virtua Bold n reads wide vs refs (1.00 vs 0.90) but Virtua's Bold
  is much darker than any reference 700 (stem/xh 0.33 vs ~0.28) —
  extra width is the legitimate cost of extra weight. Not a defect.
- Helvetica falsified the agent's earlier "o is the roundest glyph"
  claim: Helvetica's o (0.875) is NARROWER than its O (0.923).
  Inter/Geist keep them equal. No reference makes o rounder than O.

## Pass 2: curve-tension unification (2026-07-13) — the "two designs" fix

Eli's observation on the NHG comparison: Regular and Bold O read as
DIFFERENT DESIGNS, where NHG reads as one design extrapolated.
Diagnosis: the superellipse tension was INVERTED between masters —
Regular O outer κ (0.55 sides, 0.64 crown) vs Bold (0.62, 0.58).

Fix (Bold O, Bold o; Regulars untouched):
- **Bold O outer contour is now IDENTICAL to Regular O outer,
  coordinate for coordinate** — counter-reduction in its purest
  form; the Bold O is the Regular O with a smaller counter. The
  outer contour is static across the entire weight axis.
- Bold O inner handles set to the Regular counter's κ (0.657 crown,
  0.587 side): handles 312/536 (x), 236/532 (y).
- Bold o outer side handles → dy 176 = exactly the Regular o's
  handle offset (uniform κ 0.58 all around, both masters); inner
  handles to Regular-counter κ (0.558, 0.604): 276/396, 188/388.
- Verified: Bold O outer == Regular O outer True; all points on the
  2-grid; structures unchanged.
- BLOG MATERIAL: "the bold is the regular with smaller counters" is
  now literally true for O — one outline never moves, weight is
  purely counter reduction.

Left deliberately for Eli's pass (design calls): Bold o/O counter
size (the "slit" — the width lever, C6), n shoulder taper (NHG
thins the shoulder into the joints; Virtua joins at near-full
thickness and clots — needs a design decision on how taper is
expressed in the system).

## Agent system pass on n o H O (2026-07-13) — MARKED BLUE, Eli grades

Eli-directed pass to make all four reference glyphs fit the system
maximally; his edit pass follows. H untouched in both masters
(already conformant). Regular O untouched (it SET the rules).
Changes (all marked blue 0.27,0.44,1,1):

- **Regular o**: horizontals 88→92 (inner y 76/500). The "+4
  everywhere" rule Eli's Regular-O redraw established (curve = flat
  + 4 in BOTH axes), and the value the blog table already claimed.
- **Regular n**: arch crown 88→92 (crest trio y 504→500) — n crown
  must equal o crown; they sit adjacent in text.
- **Bold o**: horizontals 128→140 (inner y 124/452, side handles
  rescaled). See growth-quanta rule below.
- **Bold n**: arch crown 152→140 (crest trio 440→452, spring handles
  408→416). Before this pass Bold n (152) and Bold o (128)
  disagreed by 24 — they must match; 140 sits exactly between
  Eli's two eyeballed values.
- **Bold O (the C7 fix)**: bowls 188→204 = cap stem 200 + 4 (inner
  x 252/596, off-8-by-4 self-labeling); horizontals 160→148 (inner
  y 132/636); all eight inner handles rescaled to preserve curve
  tension (side κ≈0.55, crown κ≈0.67, matching the prior shape).
  Outer contour untouched (Eli's superellipse).

**The growth-quanta rule (new, now in DESIGN.md):** Regular→Bold
stroke growth comes in quanta of 24 — curve horizontals +48, bars
+72, verticals +96 — so every named instance lands on the grid, and
the +4 curve correction rides on top at every weight. Chosen because
delta-24 is what makes Medium/SemiBold land on-8, and 140 for the
Bold lc horizontal happened to bisect Eli's two hand values (128 o,
152 n) — the system and the eye converged.

Verified after the pass: every point in all 8 glyphs on the 2-grid;
master point structures identical; strokes exact. Instance
predictions: lc horiz 92/108/124/140; cap horiz 100/116/132/148;
bowls: lc 100/132/164/196, cap 108/140/172/204 = instance stems + 4
throughout. C7 RESOLVED (pending Eli's eye). C6 note: Bold O outer
deliberately kept identical to Regular (DESIGN.md counter-reduction)
— the caps absorb weight inward; only lowercase rounds widened.

## Method: O H n o first (logged 2026-07-12)

Classical anchor-glyph method, now in DESIGN.md ("Reference glyphs"):
perfect O, H, n, o on the grid system in both masters FIRST; all
other Latin glyphs derive stems, curve weights, spacing class, and
overshoot from them. The current pass is exactly this. Measure new
work against the live OHno, not stale tables; re-measure the
Dimensions table whenever one of the four changes.

**n and o redrawn by Eli in BOTH masters 2026-07-12 — the lowercase
anchors are settled** (pending two float advances, below). Remaining
OHno work: Bold O weight check (C7).

Current OHno state (2026-07-12, after Eli's n+o redraws):

| glyph | Reg adv | Reg ink w | Bold adv | Bold ink w | status |
| --- | --- | --- | --- | --- | --- |
| O | 848 | 752 | 848 | 752 | green/green |
| H | 768 (=cap: square!) | 608 | 816 | 656 | green/green |
| n | 592 | 464 | 704 | 576 | anchor ✓ |
| o | 616* | 552 | 672* | 608 | anchor ✓ (*float advance, snap to 616/672) |

Anchor verification (2026-07-12): all four n/o outlines are fully
compliant — every point (handles included) on the 2-grid, every
on-curve point on the 8-grid EXCEPT exactly the four +4 bowl-side
optical points (Reg o 132/484, Bold o 228/444 — the canonical
example, now symmetric in both masters); strokes n 96/192,
o 196 = 192+4 in Bold and 100 = 96+4 in Regular (the +4 rule holds
across the axis); SB n 64/64, o 32/32; overshoot ±16 everywhere;
point-type sequences identical across masters (27/24 pts).
**C6 data point from the redraws: straights grew +112 ink, rounds
+56 — rounds widen at half the rate of straights** (H also +48).
Advance relationship flips across the axis (Reg o = n + 24;
Bold o = n − 32) — legitimate consequence of round-fits-tighter
(SB 32 vs 64) with rounds gaining less ink.

Facts worth keeping: Regular H advance = cap height = 768 (perfect
square — candidate blog beat). Overshoot ±16 on O and o, both
masters, symmetric ✓. Regular o = n + 40 advance; Bold draft
currently INVERTS it (o 680 < n 704) — fix expected with Bold o
redraw (→ C6). Regular o has a 2u ink bulge past the on-curve
extremum (ink 602 vs point 600, makes right SB read 30) — missing
true extremum, tiny cleanup. O is 8 on-curve points total (pure
4-extrema construction, no chamfers).

---

## Glyph entries

### n (U+006E) — reviewed 2026-07-12

**Regular** — advance 592, sidebearings 64/64, 19 on-curve pts.
- 100% on the 8-grid (zero optical corrections). Both stems exactly
  96 ✓. Arch horizontal ~92 at crown ✓. Crown at 592 = x-height + 16
  overshoot (→ C2).
- Verdict: contract-clean. Poster child.

**Bold** — advance 688, sidebearings 64/64, 19 on-curve pts,
point-compatible with Regular ✓. Arch spring heights (344/376)
identical to Regular ✓.
- **11 points off the 8-grid**, clustered in the shoulder junction
  (e.g. 282,440 / 256,514) — machine-introduced, glyph ungraded
  (→ C1).
- **Right stem 184** (outer 624, inner on-curve 440) vs left stem
  192 vs contract 192 (→ C3). The off-8 cluster sits exactly at this
  junction.
- Overshoot 16, same as Regular — classic wisdom wants slightly more
  in the bold; Eli's call whether to differentiate.
- Decisions: PENDING (Eli's editor pass in progress).

**Bold — REDRAWN by Eli 2026-07-12.** Now: advance 704 (was 688),
sidebearings 64/64, stems 64..256 and 448..640 — both exactly **192**
(C3 resolved), counter between stems exactly 192 (stem = counter).
The 184-vs-192 and off-8-cluster findings above are historical.

### i (U+0069) — reviewed 2026-07-12

**Regular** (green, needs rework) — advance 232.
- Stem is 96 wide but sits at x 68..164 — **off the 8-grid** (68 ≡ 4
  mod 8), because stem and dot (104 wide, x 64..168) were both
  centered at 116 = advance/2. Root cause is C5: widths 96 and 104
  differ by 8, so no shared center puts both on the grid — the flaw
  was never "SB 64 + stem 96" (64+96+64 = 224 is fully on-grid, and
  matches n's left stem at 64..160 exactly).
- Fix options (Eli to pick): dot width 96 (= stem; what the Bold
  already does) or 112 (= stem + one 16u chamfer unit, edges 56..168
  overhanging the stem 8u per side like an overshoot). Either way:
  stem 64..160, advance 224, SB 64/64.
- Dot gap above x-height: 80 (656−576) — recheck after resize.

**Bold** (green) — advance 320, SB 64/64, stem 64..256 = 192 ✓ ALL
on the 8-grid; dot width = stem width (192), which is why it works —
the Bold i already embodies the C5 rule. Dot 192×144, gap 48 above
x-height (624−576) vs Regular's 80 — cross-master dot-gap consistency
worth a look when Regular i is redone.

<!-- Template for new entries:

### X (U+0000) — reviewed YYYY-MM-DD

**Regular** — advance, sidebearings, on-curve count.
- measurements vs contract; off-8 points and whether they're owned.
- Verdict / decisions / OPEN items.

**Bold** — same.
-->
