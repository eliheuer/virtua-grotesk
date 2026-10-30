# AT-001 — broad-curve and paired-stroke learning case

2026-10-23. Scope: `at`, Regular and Bold, scratch only. Eli requested a smaller
italic a and a double spiral, with the smoothness and even apparent weight of
his supplied 11:05 screenshot (conversation attachment). The earlier
[10:04 reference image](initial-reference.png) is retained here; the 11:05
Desktop path is no longer available, so it is not falsely archived as that file. Eli subsequently authorized application, rebuild and push, while judging it
“looks better, but still bad.” It is applied for his hand editing, not visually
approved. The timed task remains stopped.

## Human judgments and retained examples

- `original/`: exact source at before this experiment. The original is the
  user-selected optical reference; its red/orange grades were not changed.
- `rejected-r2/`: italic a restored, local curve diagnostics improved, but Eli
  rejected the still-lumpy drawing. Fixing traced on-curves constrained the repair.
- `rejected-r3/`: paired stroke fitting improved local widths; Eli still rejected
  its broad flow. Even width cannot rescue a poor path through the whole turn.
- `candidate-r4/`: new broad paths, paired boundaries and paired grid rounding.
  **Eli: “looks better, but still bad.”** Applied at his request for hand editing;
  this remains a negative quality verdict, not a positive training example.

[Compiled comparison](candidate-r4/review.png): original, rejected r3, new r4;
400/550/700 and text contexts. [Signed comb](candidate-r4/comb.png) is diagnostic.
The screenshots were inspected; this does not replace Eli's judgment.

## What changed in r4

The two spiral boundaries were reconstructed around long shared sweeps instead
of retaining the traced turning points. The selected width varies with direction
and tapers into the a and terminal. Both boundaries round together at cardinal
positions; independent rounding had thinned the crown by eight units. Long
handles and explicit extrema replace flat stretches followed by abrupt bends.
The a section and its counter are exactly preserved from r3. Advancing a
construction model did not authorize moving the a, copying another font or
changing any active glyph.

The generator is a local experimental construction, not a universal optical
optimizer. The final curves are not mathematically constant-width or all-G2.
The initial spline and offset fit are subsequently adjusted for the grid and
extrema; their theoretical continuity does not describe the final outlines.

The durable lesson has three parts: judge broad flow, adjacent joins, and paired
stroke mass separately. Show a plain filled comparison first. Preserve the
accepted design intent, not accidental tracing nodes. Optical differences need
an explained visual purpose, not an automatic variance-minimizing objective.

## Evidence and limitations

Compatible 76+12-point contours; all proposed coordinates/spacing on8, zero grid
findings. 1847 active source files unchanged; 2736 non-at glyph/weight outline
and advance comparisons exact at400/550/700. Fifteen compiled shaping samples
contain no missing glyphs. Ten contour/weight samples have no sampled proper
crossings. Signed curvature and lint reports retain remaining G1 jumps and
intentional a/terminal corners. These are engineering observations, not a grade.
Full package QA/preflight was not rerun for this unapplied scratch experiment.

The complete reproducible scratch packet remains in
`.glyph-ai-runs/at-double-spiral-2026-10-23/revision4/`, including the guarded
`redraw.py`, `trace/VirtuaGrotesk.designspace`, canonical build log, fonts,
normal-width reports and lint output. Do not replay the generator over a human
save. `review.json` records exact hashes and separates human rejection from
pending review. No model was trained or weights updated.

## Reusable harness diagnostic

`harness/paired_stroke_report.py` reads a GLIF and a hash-bound JSON plan of
manually identified opposing cubic branches. It refuses stale plans, reports
ambiguous/missing normal intersections, and never guesses the nearest spiral
turn. Its width ranges are local measurements, with no automatic quality grade.

```
.venv/bin/python harness/paired_stroke_report.py \
  agent-proofs/cases/at-001/candidate-r4/Regular-at.glif \
  agent-proofs/cases/at-001/candidate-r4/Regular-pairs.json \
  --output /tmp/at-width-report.json
```

Use alongside `scripts/curve_profile.py` and actual compiled proofs. Keep
optical intent explicit in the plan. When Eli corrects this candidate, retain
that exact source and add his verdict before changing the skill's examples.

## Applied for hand editing — 2026-10-23

Eli explicitly requested saving this exact candidate into Virtua, rebuilding,
updating `~/GH/repos/job-tools/business-card`, and committing/pushing Virtua.
Both active at GLIFs now match r4 exactly and remain purple. 1845 other source
files are exact; no human glyph save or grade was overwritten. The rebuilt VF
and four statics are local build outputs (ignored by Git). Five-weight compiled
checks match the reviewed scratch; all old non-at outlines/advances remain exact.

Preflight proof/reports/artifact checks completed. This is not a fresh full
Fontspector package pass. The business-card Regular font hash matches the new
static, both existing card PDFs were regenerated, and the plain PDF was rasterized
and inspected. The preexisting blob GLIF edit is byte-identical.
See [application receipt](application/verification.json). The card repository's
font update is local; no card-repository commit or push was requested.
