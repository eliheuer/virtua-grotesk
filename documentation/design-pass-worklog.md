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
