---
name: bowl-from-o
description: Construct or fix the round-bowl lowercase (b d p q g, and relatives like a's bowl) by reusing the o's exact round-half geometry, then closing it with a stem. Use when drawing, unifying, or reviewing any bowl letter against the o.
---

# /bowl-from-o

Build a lowercase bowl (b d p q g) so its round side **is** the o — not
"like" the o, the same curve — then close the far side with a stem.

Codified from Eli's hand-drawn `d` (commit 88b4aa2), compared against an
agent's approximated `d` that only *shifted* the old bowl. The agent
version measured "close" but was wrong in the ways that matter. The rules
below are what the hand pass did differently.

## Usage
`/bowl-from-o <glyph>`  — e.g. `/bowl-from-o d`

## The one idea
A neo-grotesque bowl is the **o's round half, copied coordinate-for-
coordinate**, joined to a stem. The counter is the only free variable;
the round curve, the wall, and the vertical extent are not up for
negotiation — they come from the o verbatim. Do not translate, scale, or
"re-snap" the old bowl into place. Copy the o.

## Recipe

1. **Copy the o's round half verbatim.** Take the o's outer arc and inner
   arc for the side the bowl lives on (left for d/q, right for b/p, and
   the upper bowl for g) and paste those exact points. For Virtua Regular
   the o's canonical numbers are:
   - outer left arc handles: **(40, 96)** and **(40, 480)**, extremum
     **(40, 288)** smooth; wall origin at x=40.
   - inner left column: **x=138** at **y = 160 / 288 / 416** (288 smooth).
   - round wall = **98** (inner extremum − outer extremum = 138 − 40).
   - inner vertical extent **68 .. 508**; outer **−16 .. 592**.
   (Mirror x for a right-side bowl; the o is symmetric so the right arc is
   the same numbers reflected about the o's center.)

2. **Advance = the o's advance (624). Sidebearings 40 / 64.** Round-bowl
   lowercase share the o's advance. The round side keeps the o's **40**
   sidebearing; the stem side gets **64**. The advance falls out of
   40 + bowl-width + 64 — do not invent a bespoke uniform advance.

3. **Counter ≈ 0.95× the o counter — the free variable.** o counter is
   348; the bowl comes in a touch tighter, ~**330** (0.95×), because the
   closed stem side reads heavier than the open o and wants a hair less
   counter. This is the ONLY dimension you set by eye. Everything else is
   inherited. (Cross-check: Inter/Geist run 0.96–0.97; Virtua's tighter
   rhythm supports the low end.)

4. **Draw the bowl↔stem junction — don't translate it.** Where the bowl
   springs off the stem, the transition handles move in **x and y both**.
   In the hand `d` the junction on-curve sits at y≈72 and its handle dips
   to y≈6 (vs a naive shift that kept the old y). Tune these for a smooth,
   even tangent as the bowl leaves the stem; expect to nudge y, not just x.

5. **Keep the round inner's small bulge (~4u) past the straight stem
   line.** The bowl's inner curve, at its extremum, naturally exceeds the
   stem's vertical inner edge by a few units (hand `d`: inner extremum 468
   vs stem edge 464 = **4u bulge**). This is roundness, not error — do NOT
   flatten the counter wall onto the stem line. (An agent pass wrongly
   "fixed" b's 8u bulge to 0; that removes the roundness.)

6. **Symmetry is optical, not mechanical.** Top and bottom of the bowl may
   differ by a few units; don't force mirror symmetry on the vertical axis
   just because the numbers look tidier.

## Verify
- `scripts/curve_lint.py Regular <glyph>` → clean.
- `tmp/bowl_vs_o.py` (or equivalent): round-side sidebearing ratio to o
  **= 1.00**; counter ratio to o **≈ 0.95–0.96**, and the SAME across all
  bowl letters.
- Eyeball `obdpqg` at ~180px: bowls must be indistinguishable from the o
  on the round side.

## Anti-patterns (what "measured close but wrong" looks like)
- Rigidly shifting the existing bowl by +Δ so the counter hits target: the
  round curve keeps its old handles/wall (100 not 98) and old vertical
  extent (500 not 508). Numbers pass; the curve isn't the o.
- Picking a uniform advance (e.g. 636) instead of the o's 624.
- Flattening the inner bulge to make the wall a constant thickness.
- Forcing the counter crest to exact center when the bowl wants a slight
  optical offset.

## Scope note
The agent unification pass (commit 8e35588) brought b p q g into a shared
geometry by shifting, not by copying the o. They are candidates for the
same o-verbatim treatment this skill describes — re-derive each from the o
rather than trusting the shifted version. `d` is the reference example.
