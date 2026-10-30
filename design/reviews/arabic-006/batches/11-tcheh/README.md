# Batch 11 — Tcheh base and dots

Applied working drawings under Eli’s autonomous Arabic authorization; human review
is pending. Baseline: `40ba4b4f`. Ten GLIFs changed, five in each master:
`tcheh-ar`, `.init`, `.medi`, `.fina`, and `threedotsdowncenter-ar`.

## Construction and scope

The independent initial lacked dots and did not match the Hah family. It now
uses the corresponding Hah initial plus the Tcheh-only three-dot donor. The
other three forms retain their existing Hah components. Advances follow the
bases: Regular 704 throughout; Bold 784 isolated/initial and 832 medial/final.
No Hah source was changed, including protected Regular drawings.

The exclusive donor uses three near-circular contours, with 40-unit Regular
and 56-unit Bold radii and 24/32-unit quarter handles. New points and offsets
follow the 8-unit grid. Maximum sampled radial deviation is 1.012 units (2.53%)
in Regular and 0.569 units (1.02%) in Bold. The curves have no sampled sign
reversals, zero tangent mismatch and G2 continuity at quadrant joins. These
measurements support inspection, not a claim of perfect mathematical circles.

Dots now sit inside isolated/final bowls and below initial/medial joins. The
first Bold final placement collided with the incoming join. Raster inspection
led to a 24-unit leftward and 24-unit downward adjustment, ending at offset
(168, -352). `refine-clearance.py` records the combined correction.

Moving the donor exposed a compiler anchor-propagation hazard: its top anchor
would incorrectly pull above-marks below the letter. Isolated/medial/final
wrappers now explicitly copy the corresponding Hah top anchor. Initial anchors
remain unchanged. Existing Hah optical coordinates are preserved; this is not
a broad attachment or diacritic redesign. Future component placement changes
must check compiled attachment, not just the unmarked silhouette.

All ten drafts are purple. Exact before/candidate bytes and hashes are retained
in `applied.json` and the source snapshot folders. The recomputed recursive Beh
reservation contains 18 files, all byte-identical. No shared Beh dot donor,
green source, manual hamza correction, feature or unrelated glyph was changed.

## Verification and visual evidence

- `verify.py`: 364 shaping comparisons at 400/450/500/550/600/650/700; same
  glyph substitutions and clusters, no missing glyphs, only declared advances
  and Tcheh mark-placement changes. Compiled outline changes stay within Tcheh
  and its exclusive donor. Both masters have matching component/contour structures.
- `clearance.py`: sampled dot boundaries against base ink for all four forms
  at 400/475/550/625/700; all 20 cases clear. This is sampled, not exact collision
  certification. Large Bold final source render and compiled proofs inspected.
- `tcheh-400.png`, `tcheh-550.png`, `tcheh-700.png`: joined-plus-isolated forms
  inspected against Rubik, Noto Sans Arabic and IBM Plex Sans Arabic. All four
  references remain configured, but Readex Pro lacks U+0686 and its panel explicitly
  says unavailable. No fallback outline is substituted. Plex 550 is labeled
  with the nearest supplied static weight, 500.
- `tcheh-marks-400.png` and `tcheh-marks-700.png` check isolated fatha/damma/kasra
  attachment. The old 700 proof at 96 px clipped its very high Before marks;
  the saved 80 px proof passes the raster bounds guard. Full mark stacking and
  spacing remain later work.
- Signed curvature JSON, comb SVGs and lint output are retained. Grid findings
  are preserved inherited Hah geometry/anchors, not silently snapped green work.
- The preflight rebuild differs from the raster-bound font only in the head
  modification timestamp and derived checksum. `verify.py` checks all other
  tables and head fields exactly; `preflight-build.json` retains both identities.
- `make preflight` passed build, print proof, reports and artifact checks;
  zero blocking master mismatches, 508 expected width-only differences.
- `browser-700.jpg` records the refreshed live proof. Font/image hashes accompany
  the fixed raster proofs. Application and passing checks are not human visual
  approval or release readiness.

Historical apply scripts are reproducibility records; do not rerun them over
later human edits. Next: Ain/Ghain, preserving the Beh reservation and protected
Regular Meem / Lam–Alef follow-ups.
