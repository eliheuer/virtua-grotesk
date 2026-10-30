# ARB-006 batch 05 — Bold Feh/Qaf repair

Progress checkpoint, 2026-10-21. Eli authorized fixing the rejected batch 04
proof, then requested committing and pushing progress. Human visual review is
pending; the autonomous heartbeat remains paused.

## Scope and construction

Eight Bold drawing roots: the four `fehDotless-ar` forms, isolated/final
`qafDotless-ar`, `twodotshorizontalabove-ar`, and `threedotsupabove-ar`.
The manifest records 34 edited GLIFs including wrapper widths and upper-dot
placement, and a 61-glyph dependency closure. Regular, green drawings, manual
Bold hamza and unrelated sources remain unchanged. New root drawings are purple;
wrapper grades were preserved. No outlines were copied from reference fonts.

Replaced the pinched 136×32 initial return with a 64×64 turn; rebuilt isolated
and final counters; repaired final Qaf's joining advance; matched the upper
curve joins; rebuilt two/three-dot donors from the accepted circular single-dot
construction. A second raster iteration reduced excess medial/final bottom
mass: counter floor 256 to 192, with the joining bar at 176. The first repair
trial is retained under `trial-01/`; it is not the current candidate.

## Evidence and limits

- `before-sources/`, `candidate-sources/`, `candidate.json`, `applied.json`:
  exact sources and guarded hashes. `prepare.py` reproduces the final geometry.
- `verification.json`: 308 shaping comparisons at 400/450/500/550/600/650/700.
  Glyph identities and clusters are stable; width changes are declared, and
  changed mark offsets must match the interpolated upper-dot component shift.
- `quality-check.py` / JSON: case-specific regression checks for smooth-join
  curvature jumps, return proportions and sampled proper segment crossings.
  The rejected baseline has 67 findings, the repair zero. These are diagnostic
  findings, not 67 separately identified visual faults or a universal grade.
- `grid.json`: nine preserved off-grid anchor findings; new outline points and
  advances follow the 8-unit grid. Anchors were not silently snapped.
- Build and `make preflight` completed; zero blocking master-structure mismatches.
  Preflight checks artifact presence, not release readiness.
- `feh-700.png` and `qaf-700.png` were inspected with all four references:
  crossing artifacts and the Qaf connection gap are removed; the second trial
  reduces the heavy mass below medial counters. These remain working designs.
- Endpoint 400 sheets, Veh 700 and large individual renders are saved. Their
  final inspection and a fresh 550 browser inspection remain pending at this
  requested progress checkpoint. Do not infer approval from image generation.

All four references remain Rubik, Noto Sans Arabic, IBM Plex Sans Arabic and
Readex Pro. Continue targeted visual review before another drawing family.

## Concurrent human work

Eli is now editing Beh's four forms (`ببب ب`) in RuneBender. Reserve both masters
of the Beh wrappers, `behDotless-ar` bases and every recursively used component
(including shared dot donors). Do not change those drawings, placements, widths,
anchors or grades while this reservation is active. Recompute dependencies and
source hashes before each independent batch, and exclude any donor that affects
these forms. Preserve human saves; refresh baselines rather than overwriting.
