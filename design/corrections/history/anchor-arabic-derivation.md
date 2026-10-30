# 2026-08-04 — Arabic completion: derive from green, don't trace the reference

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


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
