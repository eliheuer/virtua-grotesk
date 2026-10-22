# LAT-001 batch17 — crossed T/t

Adds **Ŧ U+0166 / ŧ U+0167** in Regular and Bold. Four new GLIFs plus four
registration plists; every previous GLIF is byte-identical. The existing green
T/t remain components, with one local eight-point bar, 16-unit cuts and explicit
on8 top/bottom anchors. Purple denotes a draft awaiting human review.

The full reverse-consumer inventory is retained in `dependencies.json`; all326
Arabic reserved sources/master are unchanged. Label- and RGBA-detected greens
are independently hashed in `final-identity.json`. All1775 other existing source
files are unchanged. No kerning, features, existing grades or Arabic proof state
changed. Baseline HEAD: fd73d7d7. Local only; no push.

## Construction and review

- Ŧ bars: Regular x128..552/y304..400; Bold x112..536/y288..416. Advances680/648,
  matching their T donors; outer bearings32/32 and8/8.
- ŧ bars: Regular x32..344/y288..352; Bold x24..392/y248..344. Advances376/416,
  outer bearings32/32 and24/24. Regular's new bar extends4 units beyond the
  unchanged t foot/crossbar; its advance is4 units wider than the human t372.
  This permits on8 outer spacing without altering that protected optical exception.
- Lower-bar separation from the existing t crossbar is136/80 units. It remains
  open at400/550/700 and at enlarged224px endpoints. New polygons are convex;
  all new points, anchors and advances are on8. Compatible component+8line
  topology is retained. No donor curves were edited. The21 grid findings are
  inherited T/t component points, anchors and the Regular t advance; no new
  coordinate/outer-bearing finding.
- Viewed actual pinned Rubik before drawing (`reference-before.png`), then all
  eight final complete images: forms/reading400,550,700 and large400,700.
  Compiled FreeType/RAQM proofs include above/below/stacked marks. DesignBot
  calls ran sequentially. Before panels explicitly say these characters were
  unavailable; no fallback glyphs stand in for missing letters.
- Full silhouettes are legible as crossed T/t and retain Virtua's heavier Bold
  stem and squared foot. Bar placement, weight balance and the relatively short
  inherited t ascender still await human review; reference comparison is not
  approval of the protected base proportions.

## Verification

`verify.py`:130 scoped checks at400/475/550/625/700; all old compiled outlines
and advances are exact, cmap gains only0166/0167, both new glyphs are GDEF bases,
mark stacks clear, old Latin/Hebrew/Arabic contexts are unchanged, and master
inventories/topologies match. Ten Latin unittest methods pass against scratch
and active builds. Frozen engineering comparison reproduces exactly216 existing
Hebrew failing subcases, zero new/resolved. The whole suite does not pass.

Active preflight completed (artifact presence only); all five active font tables
match scratch except head timestamps. Source, font and inspected image hashes
are recorded. Curve lint reports no flags; local bars contain only lines and
this is not a curve-quality verdict on the inherited green t curves.

The pinned Rubik coverage comparison now has **six** missing Latin codepoints:
ĸ ŉ ſ ƒ ﬁ ﬂ. Other missing-script groups are unchanged; these are not language
counts or reader approval.

## Exact unresolved work

New Ŧ/ŧ currently use default spacing, with no inherited T/t kerning. Their new
mid-stem collision envelope requires its own pair proof. Blindly copying Bold
`t–t` class kerning(-64) would put adjacent ŧ bar extents16 units into each other;
Regular T also has large direct exceptions(-128..-208), including off8 legacy
values. Preserve those existing sources; evaluate new pairs independently on8.

Other retained blockers:216 Hebrew baseline failures, generic green-g comma
collision,40 compound-ogonek subset samples, narrow I/l overhangs and optical
K/c/k/t exceptions, fresh Fontspector/package QA, legacy Windows line spacing,
remaining coverage and human drawing/reader review. This is a coverage draft,
not a release-ready milestone.
