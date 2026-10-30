# 2026-08-04 — even terminals: don't borrow a tooth height (Eli correction)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


**Wrong:** the isolated `behDotless-ar` (beh boat) rose to 288 on the left
and **432** on the right. 432 is the height of the *joining tooth* in
`behDotless-ar.init/.medi`, and it got borrowed for the isolated form's
right terminal because that number was already in the family. The result
was lopsided — one end a tall tooth, the other a short tip.

**Eli's fix:** drop the right terminal to **288**, so both ends match and
the boat is exactly mirror symmetric about its centre. His words: *"this
kind of neo-grotesk design needs to be simpler and more even and
geometric."*

**Rule / encoded:** a free-standing terminal on an isolated boat or cup
rises to **288**, with a 16-chamfer and a 64 flat, and BOTH ends of a
symmetric form use it. **432 is a TOOTH height, not a terminal height** —
teeth belong to joining forms (beh.init/medi) and to seen/sad, where the
teeth are the letter's identity. Never reach for a number just because it
exists elsewhere in the family; ask what that number *means* first.

Same mistake, same fix, found by grepping the family for terminal-flat
heights: `noonghunna-ar` (right lip 432 → 288, now a symmetric cup) and
`behDotless-ar.fina`, which had a whole medial-style tooth in the middle
of a FINAL form. A final beh has no tooth at all — it is the isolated boat
with its right terminal replaced by the joining bar. Rubik confirms:
its `behDotless-ar.fina` is 342 tall with no tooth.

**Generalisation worth keeping:** after any correction, grep the family for
the *number* that was wrong, not just the glyph. One probe over all
boat/cup glyphs ("what are the terminal-flat heights?") surfaced both other
offenders immediately.

**Also:** Runebender writes `<unicode>` BEFORE `<advance>`; the generator
now matches, so regenerating a glyph does not churn against a Runebender
save. After encoding a correction, verify the generator reproduces the
human's file **byte for byte** before propagating — otherwise the next
regeneration quietly reverts the correction.
