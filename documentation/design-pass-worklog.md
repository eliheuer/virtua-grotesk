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
  Either the drafts are systematically 8u light, or the contract
  number should be 184. Status: OPEN — decide once, apply everywhere.
- **C4 — shoulder-basin anatomy consistency** (h vs n arch springing
  differs by ~28u; check m, u too). Both legal per the grid; optics
  question. Status: OPEN.

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

<!-- Template for new entries:

### X (U+0000) — reviewed YYYY-MM-DD

**Regular** — advance, sidebearings, on-curve count.
- measurements vs contract; off-8 points and whether they're owned.
- Verdict / decisions / OPEN items.

**Bold** — same.
-->
