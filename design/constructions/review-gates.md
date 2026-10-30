# Construction review before curve fitting

Use this procedure for a repair rejected for style, silhouette or stroke weight.
It is a local inspection step, not a new source of drawing authorization.

1. Retrieve fresh context. Create a study with `scripts/construction_review.py
   --context out/context.json --init out/study.json --html out/study.html`.
   Keep only the relevant panels in the study: current target, named green donors,
   and exact rejected examples. Label each role. Never treat an external reference
   as a green Virtua donor. The shared-scale SVG shows source construction; retain
   the existing compiled-font proof for reference fonts and actual text rendering.
2. Fill `diagnosis`, `preserve_intent`, and `optical_exceptions`. Identify the
   straight runs, turns, articulation and opposing stroke edges before proposing
   coordinates. Show the study when the construction is unresolved. Empty fields
   are intentional blockers, not text for the agent to rubber-stamp.
3. For a bounded candidate, add `pairs`, each with hash-bound `before` and
   `candidate` paths and `constraints`. Run `--plan out/study.json --check`.
   Available constraints are `metadata`, `preserve_points` (contour and point
   indices), and `straight_run` (contour, adjacent start/end indices, fixed axis,
   minimum length). Every constraint needs a construction reason. Thresholds are
   proposed design choices until Eli confirms them; they are not universal rules.
   A topology change refuses correspondence and requires explicit remapping.
4. Structural success is **not optical approval**. Inspect complete silhouettes,
   matched-size references, counters and reading-size text. Use paired-stroke
   measurements diagnostically, not as an objective that can change the skeleton.
   If the result is visibly wrong, mark it unsuccessful before presenting it as
   an improvement. No tool here approves application or changes a source.

A pair entry is shaped like:

```json
{"before":{"path":"out/before.glif","sha256":"..."},
 "candidate":{"path":"out/candidate.glif","sha256":"..."},
 "constraints":[{"kind":"straight_run","contour":0,"start":41,"end":42,
 "axis":"x","min_length":128,"reason":"Illustrative upright-run constraint; confirm for this glyph/master"}]}
```

Seen v6 is a regression fixture: its Bold first-tooth straight run shrank to16
units while a stroke-distance fit improved. A proposed128-unit minimum detects
that failure, but passing it cannot prove a good Seen. V4's topology change must
not silently invalidate point-index constraints. These examples test the tool's
ability to expose a construction violation, not its ability to judge beauty.

Generated studies live under ignored `out/`. Keep only selected source pairs,
human feedback and small receipts in `design/reviews`/`design/corrections`.
Do not commit duplicate fonts, complete context dumps or every screenshot.
