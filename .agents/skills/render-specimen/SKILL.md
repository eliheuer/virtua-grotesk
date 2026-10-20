---
name: render-specimen
description: Launch and inspect the default live web proof for Virtua design review, or render fixed DesignBot proofs when requested.
---

# Render specimen

For the complete **Virtua Design Review** loop and current handoff, read
[START-HERE](../../../agent-proofs/README.md).
Default interactive entry point: `make proof-web`. Read
[the web-proof guide](../../../agent-proofs/app/README.md) for
launching, source files, snapshot recovery and the current UI/UX work plan.
Eli confirmed this default on 2026-10-19 and, after the UI pass, said it was ready
to move on. Follow the central handoff and current case for the next scope;
preserve the proof layout and distinguish UI acceptance from drawing approval.

For the main PDF, run `make proof` from the repository root and inspect
`documentation/proofs/proof.pdf`.

For browser spacing review, run `make review` and inspect the Diffenator3
report under `out/review/`.

`make specimen` is an unimplemented marketing-specimen target. Do not promise
or report a landscape spacing PDF from that command. If the user requests a
custom specimen, inspect the existing scripts under `documentation/` and
choose or adapt one for the requested format.

Render and inspect the actual result before describing layout, spacing,
missing glyphs, collisions, or drawing quality. Report the output path.

For interactive before/after and reference review, Eli now prefers live browser
font rendering (P018, 2026-10-19). Follow
[the live browser workflow](../../../documentation/qa.md#live-browser-review).
Use actual verified font files, separate family aliases, readable labels and
explicit size/weight controls. Do not shrink a specimen PNG into the browser.
Preserve two grays, title case, grid organization and recorded feedback. Check
font loading and coverage before drawing conclusions. Capture screenshots as
review evidence; browser shaping/rasterization can differ from DesignBot.

For requested fixed exports or historical reproduction, follow
[the standard DesignBot workflow](../../../documentation/qa.md#standard-designbot-comparison-workflow).
The canonical three-sheet layout is `documentation/proofs/hebrew_review.rs`;
`hebrew_review.py` only runs DesignBot and verifies/records evidence. Use this fixed-export workflow rather than the historical Python/Pillow presentation scripts.

Use Virtua Regular labels, title case headings, two grays (#dedede/#444444), and retain
both light and dark outputs. Large 56 px headlines start at −0.02 em tracking;
keep captions and sample runs at zero added tracking. Always export with --raw.
Organize metadata through alignment and hierarchy, avoiding repeated slash
separators. Put names above roles and use sentence case for explanatory footnotes.
Use the correct applied/candidate label; isolate before/after font contexts.
Keep fixed em scale, origins and baselines, and inspect every output plus a grid
version. Do not infer aesthetic approval from pixel metrics or QA counts.

For iterative design work, read
[Design review and feedback](../../../agent-proofs/FEEDBACK.md)
and the latest open review. Record Eli's correction, interpretation, exact scope,
and proposal/application state before the next edit. Keep agent suggestions
separate from confirmed rules. Retain the selected images and input/output hashes
with the review. The Hebrew/Arabic weight relationship remains provisional.

`scripts/proof_compare.py` remains an optional pixel-difference diagnostic;
`scripts/proof_reference.py` can reproduce older/ad hoc comparisons. Their old
presentation is not the standard. Preserve historical images rather than silently
regenerating them through a different renderer. The focused DesignBot diagnostic
and alpha/hinting findings are recorded under HEB-001.

The rendering workflow is approved; the v3 layout is a proposal after Eli
rejected distant labels and unconsidered negative space (P016). Use a dedicated
weight-label rail adjacent to the rows, close column captions, and a coherent
comparison field. The grid must explain relationships, not merely constrain
coordinates. Review the result before calling it approved. Follow the phase sequence in
`agent-proofs/FEEDBACK.md#next-phases`: Hebrew glyph groups, then
long mixed Latin–Hebrew text at multiple sizes beside Rubik and Noto, then Arabic.
Record accepted corrections and their scope; do not treat proposed optical
patterns as established rules. Check bidi order and font selection before using
future mixed-script text to diagnose spacing.
