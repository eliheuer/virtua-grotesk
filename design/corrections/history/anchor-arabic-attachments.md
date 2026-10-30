# 2026-08-05 — the Arabic anchor system: dots and harakat are DIFFERENT slots

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


**Wrong:** of 128 Arabic composites carrying a dot or mark, only 47 sat
where their anchors said. 8 of the 14 marks had no attachment anchor at
all, so placement fell back to a homegrown "mark ink centre + base anchor
+ 112" rule and drifted — some by over 1000 units. The anchors were
decoration; the dots were free-floating.

**Rubik's model, now adopted.** The idea worth stealing is that dots and
vowel marks use SEPARATE slots:

| slot | for | sits |
|---|---|---|
| `topDots` / `bottomDots` | the letter's own dots | close to the letter |
| `top` / `bottom` | harakat | clear above/below everything |

Marks carry the matching `_topDots` / `_bottomDots` / `_top` / `_bottom`,
plus a plain `top`/`bottom` for stacking. A composite's stored offset is
then exactly `base.slot - mark._slot`. In Rubik every pair checks out to
the unit: teh-ar.init stores (-90,-194); base `topDots` (110,326) minus
mark `_topDots` (200,520) is (-90,-194).

The payoff is automatic: a composite inherits the base's slots but pushes
its own `top` up past whatever it added, so a haraka clears the dots.
`noon-ar.init`'s `top` ends at 720 and `theh-ar.init`'s at 896, against
the dotless `behDotless-ar.init`'s 432 — exactly what Rubik does when it
raises teh-ar.init's `top` from 520 to 556.

**Derive the constant from GREEN, not from the reference.** The 112 gap is
Virtua's own: `behDotless-ar.init` has `topDots` at y=448, and green
`noon-ar.init` places dotabove-ar at yOffset −128, so its ink bottom lands
at 688−128 = 560 = 448+112. So `_topDots` on a mark = (ink centre,
ink_bottom − 112), and every green placement stays put.

**Green is the source of truth.** The script never moves an existing
anchor — it only adds missing ones — and when recomputing would shift a
green composite it keeps the offset and REPORTS the drift instead. 16 of
those surfaced; they are Eli's graded optical corrections, not bugs.

**Two traps:**

- **The base/mark anchor pair is wrong for MARK-ON-MARK.** Applied between
  two marks (dammatan = damma over damma) it threw the second one to
  y=1516 against a 1094 ceiling. Stacking marks needs its own tight rule
  plus an envelope clamp.
- **A below-dot must not drag the `top` anchor sideways.** Setting a
  composite's `top` from its resolved ink centre moved beh-ar.init's `top`
  x from 144 to 54, because the below-dot widened the bbox. Keep the
  base's x, move only y.

**Pipeline order matters:** `embolden` then `arabic_anchors` then build.
Emboldening regenerates Bold glyphs and can drop an anchor (dad-ar lost
`bottomDots` that way, and fontmake rejects masters with differing anchor
sets), so the anchor pass has to run last.
