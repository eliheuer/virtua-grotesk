# 2026-08-04 — a spliced tail must join TANGENTIALLY (Eli correction)

Historical observation. Current grid/color/source policy governs execution; dated pipeline commands and authorization are not current instructions.


**Wrong:** `seen-ar`'s tail met the teeth with a square step. The tail run
turned 90 degrees straight off the junction — the bowl's inner wall ran
vertically up and hit the bar top at a hard corner, and the outer wall did
the same at the baseline. The letter read as two pieces butted together
rather than one stroke. Eli spotted it instantly; Rubik's seen shows the
tail flowing out of the teeth as a single continuous stroke.

**Rule / encoded:** check the donor's TANGENTS at the splice point and
match them. Green `seen-ar.init` arrives at (0,0) from a control at (56,0)
and leaves (0,104) toward a control at (64,104) — both horizontal. So the
replacement must leave horizontally and return horizontally, with both
junction points marked smooth. `seen_tail_run` now does: bar bends down a
120-radius quarter, round U, vertical left wall, terminal at 432 (level
with the teeth, so all four verticals of seen line up).

**Two supporting rules from the same fix:**

- **Tie the construction constants to each other, not to separate
  guesses.** Setting the bowl's side-wall height independently of the
  bend radius put a visible dent in the outer edge. The side walls turn
  into the bowl at the SAME y as the bar's bend, and the inner curve
  turns at the same y as the outer — that is what makes the stroke a true
  constant-width offset round a U.
- **Check proportion against the reference numerically.** The first
  attempt's bowl was 40% deeper than Rubik's equivalent (scaled for cap
  height). Render both at the same size and compare before calling it
  done.

**And the bug the fix exposed — NEVER ASSUME A DONOR'S DIRECTION.**
`scripts/normalize_winding.py` reverses blue contours to get outer-CCW.
A reversed donor arrives at the stub's LAST point first, so the naive
`d[:i0] + run + d[i104+1:]` splice silently produced just the run —
`seen-ar.fina` lost all its teeth and `sad-ar` lost its loop, with no
error. Worse, it fails quietly: the glyph is still valid, just wrong.
`orient_to_stub()` now rotates and if needed reverses the donor so the
stub always runs forward from index 0, and returns the stub's end index
because the stub is 4 points in the beh/seen idiom but 6 in hah/ain
(they step in from the bar first). All four splice helpers use it.

**Corollary:** reversing an outer contour without reversing its counter
flips their relative winding and the counter stops cutting — sad's loop
filled in solid. Running `normalize_winding.py` after any splice fixes
this by nesting parity; make it part of the pipeline, not an afterthought.
