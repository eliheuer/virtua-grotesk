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

**Batch 3 DONE (rounds, commit cab0b31):** c (horiz 92/140, Bold
side 196, terminals on-8, Reg adv 584), C/G (horiz 100/148, Bold
sides 204 = O), Reg Q outer kappa = O, Bold Q remapped to O frame
(adv 848). FLAG: G bar/spur 96/96 Reg, 136/136 Bold — design call.

**Batch 4 DONE (bowls):** b d p q both masters — Bold stems all were
176/184 -> 192; bowls to o values (sides 196, horiz 140 Bold; 100/92
Reg); Reg d was 80/80/104 (!) -> 92/92/100; p/q seams = n exactly;
Reg p adv 616 + outer 584 (= o), Bold p adv 688 (= o); Reg q stem
normalized 464..560 (was straddling 460/468), adv 624; Bold q stem
448..640, adv 704 (RSB 64 = n). All rendered + inspected.

**Batch 5 DONE (commit pending):** g both masters (edges on-8:
bowl left 32/132 Reg + 32/228 Bold, right col 552, inner right
96/196; horizontals 92/140 incl. loop; seams gap-8; Reg adv 616);
k (Reg adv 544 + endpoint snap; Bold stem 168->192 with junctions
+24, endpoint 52->48); E F (mid arm = H bar EXACTLY 360..456 Reg /
312..480 Bold; top arm 96/168; Bold stems 192->200 edge 280);
j (Reg stem 72..168 + dot 96 = stem per C5, adv 232, matching Eli's
fixed i at 224/64..160/dot 96; Bold stem+dot 56..248 = 192, adv 312,
hook micro-fillet rebuilt). All rendered + inspected.

**FLAG — Bold a is byte-identical to Regular a** (never boldened;
adv 576 both). Needs a real boldening session (the a.bold shape-swap
history applies). Not attempted in this pass.

**Remaining worklist:** s S (spine pathology, redraw allowed);
diagonals v w x y z A V W X Y Z N M (snap off-8-not-4 endpoints,
optical stroke, endpoints on-8; N adv 774 off-8, Z adv 604 off-8,
x adv 514, y adv 524, v/w Reg off8 pts); bowl caps B D P R U
(B adv 716, D adv 756, R adv 668 off-8; conform bowls to O DNA,
Bold stems 200); final full audit + DESIGN.md refresh.

## Reference round 2: e f g (2026-07-14, Eli's NHG image)

Measured (x-height calibrated): e ink 608 = ours EXACTLY; e bar
top/thickness match; g bowl counter 229x285 vs ours 224x304 = match;
f stem/width: ours 344 vs ref 380 (flag), stems by-design darker.
Fixes applied (blue): e outer crests to round-part mid 336 + tension
normalized; g counter sides to y-mid 300, crests 340; p q handle
normalization (their remaining tension breaks are bowl-to-seam
anatomy -- Eli's polish queue). Lint sharpened: crest checks only on
pure round extrema (off-curve neighbors both sides).

**JUDGMENT CALL FLAGGED -- f/t bar weight:** NHG Bold f bar is ~0.63
of stem (would be ~128 for us); ours is 152 (0.79), which matches
Regular's near-monolinear ratio (80/96 = 0.83). Kept 152: Virtua's
monolinearity is identity, NHG's contrast is NHG's. Eli's eye
decides; 128 is the quanta-legal alternative (Regular 80 + 48).
## The lumpy-counters incident + curve fairness lint (2026-07-14)

Eli caught egg-shaped b/d counters at zoom that ALL existing checks
missed. Root cause: after the reference-driven widening, counter
crests sat 14u off the counter's center (and side crests 12u off the
y-mid) — and nothing measured curve GEOMETRY: stroke/grid lints check
values, sheet renders hide 10u curve errors. PROCESS FIX:
scripts/curve_lint.py (crest centering + curvature tension breaks at
smooth joints), `make lint-curves`, and the CLAUDE.md rule: after
curve edits, lint + render the single glyph LARGE (glyphbox), never
just sheets. b/d counters recentered (crests on grid mids), lint
clean. Interpretation note: the lint is a REVIEW tool — asymmetric
bowls (Arabic, apertures like c/e) flag by design; the actionable
Latin residue after b/d: small (10-16u) counter offsets in p, g,
e inner + tension breaks in a(draft)/e/g/p — sweep queued.

## Data-quality session for v0.9 (2026-07-14, agent + Eli in parallel)

v0.8 result: OFL-pretrain -> finetune BEATS the mean-delta baseline
20.9 vs 31.3 MAE on all 10 held-out glyphs (control without
pretraining: 32.0 = tie). Gate 0 passed. Public name: Virtua v0.1.

Diagnosis of residual error: NEW calibration report shows x 0.81 /
y 1.01 -- the model under-boldens STEMS specifically (81% of required
x-growth; y-optics perfectly calibrated). Recentered deltas target
exactly this and are the v0.9 model-side variable.

Prepared for v0.9 (all committed in font-garden-lab):
- trim-close encoding (duplicated contour-closing point removed;
  the twins could receive different deltas -- observed failure)
- OFL corpus recentering on its own mean (token semantics align with
  the Virtua-recentered finetune within one grid step)
- 5-fold eval: every trainable pair held out once (runs/v09.sh)
- system_snap post-processor: model deltas pulled to the 8-ladder
  (tol 3), optical residuals preserved; INSTALL-time only
- curve normalizer swept b c (both masters; p q left for Eli's
  orange-polish queue)

Corpus at green+blue = 59 pairs and growing as Eli grades digits +
punctuation (agent first-pass on : ; < = > ? committed, blue).
Launch when Eli's current grading burst is committed:
  cd ~/GH/repos/font-garden-lab && nohup bash runs/v09.sh > runs/v09/run.log 2>&1 &

## AGENT PASS COMPLETE (2026-07-13) — handoff to Eli's pass

Final state after batches 1–7 (commits 6884003..HEAD): **38 of 52
glyphs fully clean** (advances on-8, every point on-2, on-curve
points on-8 or off-by-exactly-4, master structures compatible).
`./build.sh` compiles the VF + 4 statics. All touched glyphs BLUE.

**Batch 6-7:** D conformed to O DNA both masters (Reg outer 712 /
inner 604, horizontals 100; Bold stem 280, outer 760, bowl 204,
horizontals 148, adv 760/808 — RSB 48 = O). Advance snaps: B 720,
R 672, N 776, Z 608, x 512, y 528, A 696, K 680. Straggler off-grid
points snapped in A B K g q z (renders checked).

**What I did NOT do (Eli's pass / future sessions):**
- **Bold a — still Regular-weight** (byte-identical copy). The big one.
- **s / S** — 4-5 off-8-not-4 pts each (Reg+Bold), the known
  terminal-extreme pathology. Wants a redraw session with renders.
- **Diagonal interiors** (N W X v w x y; Reg mostly): junction points
  off-8 encode diagonal stroke width = LEGAL per the diagonals rule
  (optical stroke, endpoints on grid). Endpoints verified on-8. If
  Eli wants junctions purer, that is a per-glyph redraw.
- **B P R U bowls** — organic constructions left alone beyond
  advance snaps + straggler points; conforming their bowls/arms to
  the E/F/H-bar system needs per-glyph design decisions (B's two-bowl
  balance especially).
- **G bar/spur** (96/96 Reg, 136/136 Bold): internally consistent,
  off-system; design call.
- **f hook** horizontal 80/128 vs curve-horiz 92/140: design call.
- **e width vs o** (Reg -16, Bold -48): refs keep e ≈ o; may want
  Bold e wider eventually (careful: first attempt mangled it).
- **U basin** vs n-crown value: U audit-clean but basin stroke
  unmeasured against 92/140 rule — check during Eli pass.

**Lessons this pass (for the diff-review after Eli's pass):**
1. u := rot180(n) EXACTLY worked; d/p/q/b relate the same way but
   were conformed in place, not derived. Consider full derivation.
2. The e bar is its own value (80/104), NOT the f/t bar (80/152).
3. Bold transfer drafts systematically: stems -8 to -24 light, bars
   chaotic (112/128/136 for the same role), micro-fillet junk at
   junctions (4-unit handles) in t f j.
4. Cap arms (E F) = H bar POSITION exactly, not just thickness.
5. j = i + hook: same stem placement logic, dot = stem width (C5).
6. RENDER EVERY EDIT (glyph_canvas sheet) — numeric checks pass on
   mangled outlines.

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

### grid-qa snap pass — 2026-07-15

First trial of `make grid-qa` as a cleanup driver (Eli-directed experiment).
Fixed the FAIL grades that were pure grid noise — on-curve points off the
8-grid by exactly ±2 — using the PERFECT-graded glyphs as the pattern.
All moves ±2 units, chamfer pairs moved together, smooth-point handles
moved with their on-curve point to stay axis-aligned. No advance widths,
no curve reshaping.

- **Regular:** v, x, W, N, X, w → all now PERFECT. Bonuses found by the
  snaps: W's bottom-right chamfer was 20u and 4u off mirror-symmetry (now
  16u and symmetric); N's right stem was 2u off, sidebearings now 80/80;
  x's terminals now mirror at SB 32/32; w's first inner-vertex flat was
  12u vs the second's 16u (now both 16).
- **Bold:** three, five, six, seven, nine → hard failures cleared (grade
  OK; handle-length polish remains). curve_lint flags on these are
  pre-existing and slightly *improved* by the snaps (three's tension
  ratio 8.6→7.2, six/nine crest offsets 18→16).
- NOT touched (need Eli's call): Regular digit advances off the 8-grid
  (two 594, three 628, four 598, five 604, six 636, seven 548, nine 628 —
  spacing decisions); diagonal-handle FAILs (s, S, two, eight, y, a Bold —
  curve reshaping); four Bold (advance 658).
- **OPEN:** `less` masters are structurally incompatible (Regular 7 pts vs
  Bold 10, contour 0) on committed main — blocks `make build` entirely.
  Pre-existing, not from this pass.
- Note: nearly all glyphs this pass touched were marked green (= done);
  grid-qa disagrees with the green marks. Eli authorized the edits.

### grid-qa pass 2: digits, spines, and `less` — 2026-07-15

Second Eli-directed grid-qa pass; clears every remaining FAIL (124
glyph-masters, 0 FAIL, 63 PERFECT).

- **`less` (blue, both masters) — REDRAWN Bold.** Bold was 10 pts with
  half-chamfered ends and advance 560 vs `greater`'s 7 pts / 600; Regular
  `less` was already `greater`'s exact mirror. Bold `less` is now the exact
  mirror of Bold `greater` (7 pts, advance 600), point-ordered to match
  Regular. This unblocked `make build`.
- **Digit advances (Regular), rounded to the 8-grid, RSB chosen to match
  the Bold master's sidebearing pattern:** two 594→592, three 628→624,
  four 598→600, five 604→600, six 636→640, seven 548→552, nine 628→624;
  Bold four 658→656. All digit off-grid points snapped (same ±2 clusters
  as pass 1); Regular four's whole crossbar band was 2 low.
- **Diagonal-handle FAILs.** Two distinct causes found:
  (a) *tangent seams on diagonals* — s/S spine points, two's neck points,
  y's descender-to-diagonal joints: these are seams, not extrema, so the
  `smooth` flag was removed (zero geometry change; the convention already
  says corner-point handles may be diagonal). (b) *near-axis handles* —
  eight's top/waist handles were 2u off horizontal (782/786/474/470 →
  784/472): flattened. Bold a's bowl-top handle bulged to 624 → flattened
  to 592 (x-height + 16 overshoot, same as Regular a and n's crown); its
  two near-axis counter handles squared up; the genuinely diagonal counter
  seam (264,88) demoted to corner.
- Verified: `make build` green, built hmtx widths match sources, Medium
  instance interpolates, `make preflight` green, curve_lint shows no new
  flags (several pre-existing ones on Bold two vanished), large renders of
  two/eight/s/a clean.
- **Handle-length polish (popcount niceness) deliberately not done** for
  the OK-grade glyphs (zero/C/O/Q/c/e/g/o/b/d/p/q/G/B/D/P/U/m/j/h/t/S/s,
  digits) — that's tension re-tuning, better done with eyes in Runebender.
- Eli plans a manual cleanup pass over all of this; blue/orange marks left
  as-is for that review.

### grid-qa pass 3: handle-length niceness — 2026-07-15

Final cleanup pass: **124/124 glyph-masters at GOOD or better, 74
PERFECT, 0 FAIL** (from 51 PERFECT / 29 FAIL two days ago). No on-curve
points moved this pass — off-curve handles only.

- **Round 1+2 (single-handle snaps, 368 handles):** every graded
  axis-aligned handle with a popcount-4+ length snapped to the nearest
  popcount<=2 (or <=3) even value within ~5% of its length (7% for
  values stuck in the pop<=2 void zones like 98..127). Tool archived at
  `documentation/archive/agent-generated-scripts/nice_handles.py`.
- **Round 3 (compensated pairs, per Eli's rules stated mid-pass):** for
  popcount-3 blockers, redistribute length between the two handles of
  one cubic segment (one longer, one shorter, total preserved +-4) so
  both land nice — form roughly preserved, and segment evenness must not
  degrade (it improved nearly everywhere: C 144/176→160/160, Bold O
  112/144→128/128, six 208/112→192/128). Tool:
  `.../agent-generated-scripts/pair_nice.py`. One reverted case: Bold d,
  where the pair move balanced the segment but worsened contrast across
  the smooth join with its stubby 40u partner handle (curve_lint caught
  it) — d stays GOOD.
- Eli's handle rules recorded this pass: compensated pairs preserve
  form; prefer somewhat-even handles within a segment; handle lengths
  should mirror the glyph's proportions (tall o → side handles longer
  than top).
- **Uneven-pair audit (left for Eli, deliberately untouched):** zero
  R 288/128 and B 320/132 (x4 each), s R 40/96 / B 24/64, eight B 80/32.
  These are numerically clean but break the evenness preference —
  rebalancing them would change the superelliptical character, so they
  are flagged, not fixed.
- **Remaining GOOD (not PERFECT) blockers** are lengths like 208/176/112
  whose nearest pop<=2 partition is >7% away even with pair moves (O, o,
  C, G, Q bowls and similar). Honest ceiling without visible form change.
- Verified: curve_lint net-improved (Bold a and Bold five dropped off
  the flagged list, zero new flags), build green, preflight green, large
  renders of C/O/o/zero/D/six/p clean.

### H O n o — cap vs lowercase weight & spacing study — 2026-07-22

Normalized comparison against Inter (north star) and Geist, via
`make metrics` (`scripts/normalize_metrics.py`; method in
`documentation/normalized-metrics-workflow.md`). Regular master. Raw
Virtua units: H stem 104 / n stem 96; O side 108 / o side 100; O crown
96 / o crown 88; sidebearings H 80 / O 52 / n 64 / o 40.

**Weight — Virtua is internally consistent, caps ~8% heavier everywhere.**
- `H stem / n stem` 1.08 (Inter 1.06, Geist 1.02) — caps a hair heavier
  than lowercase uprights; fine, at the heavier end of normal.
- `O side / o side` **1.08** (Inter **1.01**, Geist 1.02) — the notable
  divergence. Inter keeps *round* weights equal across case; Virtua's O
  is 8% heavier than o, matching its uprights' 8%. So Virtua is
  self-consistent (uniform cap-heaviness) where Inter is not — a real
  fork in philosophy, not an error. Question for Eli: keep uniform +8%
  caps, or follow Inter and equalize the rounds (O side 108 → ~100)?
- Contrast healthy: lc `o/n` 1.04 and cap `O/H` 1.04 both match Inter's
  ~1.02–0.97 band; rounds carry the right optical over-weight.
- Overshoot `o crown/o side` 0.88 = Inter exactly. `O crown/O side` 0.89
  vs Inter 0.95 — Virtua's cap crown is a touch light; minor.

**Spacing — lowercase is deliberately tight; caps read relatively open.**
- `n sb / n counter` 0.25 (Inter 0.30) and `o sb / o side` 0.40 (Inter
  0.57) confirm the intentional tight, display-leaning lowercase.
- `H sb / n sb` 1.25 and `O sb / o sb` 1.30 (Inter 1.14 / 1.17) — caps
  sit **more openly relative to lowercase** than in Inter. Largely a
  consequence of the tight lowercase denominator, but in mixed setting
  (`Ho`, `On`) the caps will have more air than Inter's. Question for
  Eli: pull cap sidebearings in slightly (H 80→72, O 52→48) to tighten
  the cap↔lowercase transition, or leave caps open on purpose?

**Proportion — all close to Inter.** `cap/x-height` 1.33 (Inter 1.33
exactly); `O/o width` 1.38 (Inter 1.30, Virtua O slightly wider);
`H/n width` 1.32 (Inter 1.30). No action.

Two decisions parked for Eli (both aesthetic, not defects): round-weight
philosophy (uniform-heavy vs Inter's equal rounds), and cap spacing
openness. Nothing edited this pass.

**LOCKED 2026-07-22 — H O n o are the master templates.** Resolved:
- Weight: keep caps ~8% heavier everywhere (Swiss/Helvetica, Eli's call) —
  O side 108 / o side 100, H stem 104 / n stem 96.
- Spacing: sidebearings are multiples of 8 (kerning in 8s), counter is the
  free variable that self-labels ([[dyadic-self-labeling-grid]]). Final sb:
  H 80, O 48, n 64, o 40. Cap O pulled in from 52.
- Round aspect (w/h): O 0.86, o 0.895 — the o is drawn ROUNDER than the cap O
  (Inter does the same: o 0.882 > O 0.864), so the lowercase o holds its own
  and doesn't read as a shrunk O. Cap O was narrowed 736→688 (it had bulged
  to 0.92); o was then widened 528→544 for presence.
- Round top-handle tension: O 192/rad 344 = 0.558 (near circular-ideal), o
  128/rad 272 = 0.471 kept SHORT on purpose — 144 made the o look heavy
  (longer top handle = more mass near the top), 128 keeps a lighter, tighter
  top. So the pair intentionally does NOT share top tension; perceived weight
  won over numeric consistency. Side handles ~0.63. No inflections; curve_lint
  clean.
- Round side weight = 108 (cap) / 100 (lc); counters self-label: O 472, o 344.
- Open/accepted: O crown 96 (crown/side 0.89, a touch light vs refs 0.93–0.95)
  left clean-on-8 rather than nudged to off-8 100.

Propagate these to C G Q D (caps) and c e (lowercase): sb mult-of-8, aspect
~0.86/0.87, top-handle tension ~0.55, side 108/100, counter self-labels.
Verify each with `make metrics` and `curve_lint`.

<!-- Template for new entries:

### X (U+0000) — reviewed YYYY-MM-DD

**Regular** — advance, sidebearings, on-curve count.
- measurements vs contract; off-8 points and whether they're owned.
- Verdict / decisions / OPEN items.

**Bold** — same.
-->
