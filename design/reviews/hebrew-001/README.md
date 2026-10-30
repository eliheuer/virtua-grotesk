# HEB-001 — Hebrew baseline and first proposed pair

Date: 2026-10-19. Status: **candidate v1 applied; weight direction provisional**.
The four reviewed outlines were applied on 2026-10-19 following Eli’s approval. No review colors changed.

Latest specimens: [DesignBot editorial revision](#editorial-layout-refinement--2026-10-19),
with both gray polarities and Virtua labels. Earlier sections retain historical evidence.

## Evidence

Columns: Virtua Grotesk / Rubik / Noto Sans Hebrew. The same text is shaped in
all fonts, at the labeled pixels per em, default width axes, and weights. There
is no individual glyph auto-fit and no optical weight matching. A common baseline
and scale preserve real width/height differences. Matching weight numbers are
useful checkpoints, not a claim that the fonts have equal apparent darkness.

- [Regular overview](regular.png)
- [Bold overview](bold.png)
- [Dalet/resh at 400, 550, 700, including reading-size context](dalet-resh.png)
- [Evidence identities and source inventory](evidence.json)
- [Overview recipe](../../../documentation/proofs/hebrew-reference-samples.json)
- [Pair recipe](../../../documentation/proofs/hebrew-dalet-resh-samples.json)

At the initial read-only review, source files matched the built snapshot in
`out/qa/2026-10-18/applied-hebrew-remaining/manifest.json`; VF hash verified.
No rebuild was needed for that initial read-only review. References reuse the hashed
October 18 cache. The Noto binary originated at a mutable Google Fonts main URL;
its SHA-256, not that URL's future content, identifies this review's reference.
Do not call these the latest reference releases without checking.

## Observations, not approved design rules

1. **Dalet and resh are too similar in Virtua Regular.** Both have an almost
   rectangular upper-right junction, with only small size/spacing differences.
   In both references dalet has a top bar projecting to the right of its stem;
   resh has a rounded shoulder. At reading size that distinction remains clear.
2. **The Bold texture is unfinished.** Exactly 22 of the 27 U+05D0–U+05EA
   source outlines are identical across masters. This is source-outline equality,
   not a claim that every anchor/advance or final raster is identical. In the
   Bold proof, heavy resh/vav/yod/final nun interrupt largely Regular-weight text.
3. **Dalet/resh weight growth is particularly inconsistent.** At y=300, dalet's
   straight stem is 100 Regular / 106 Bold; resh's is 104 / 200. Dalet's top bar
   at x=200 is 96 / 108; resh's is 104 / 200. Both advances are 568 / 624.
4. Rubik is the closer geometric visual reference here; Noto offers another
   structural comparison. Virtua's chamfers and own design contract remain the
   authority. The references do not establish a target width or weight by copying.

## First candidate — scratch preparation authorized

Scope: `dalet-hb` and `resh-hb`, Regular and Bold (four GLIFs).
Regular labels are orange; Bold labels are red. Neither is a green reference.

- Dalet: create a clear rightward top-bar projection by insetting the upper stem,
  preserving the recognizable chamfered construction. Establish a real Bold
  version with a weight progression coherent with its partner.
- Resh: replace the square upper-right elbow with a controlled rounded shoulder,
  using compatible cubics in both masters. Retain chamfers on appropriate exposed
  terminals; do not imitate Rubik's generally softened corners.
- Begin with the existing 576 height and 568/624 advances. Any necessary spacing
  or anchor change must be reported and justified separately. Do not prescribe
  exact optical offsets until the shape direction is accepted.
- Check related forms (dalet/resh dagesh composites and the wide dalet draft), vowel/rafe and
  cantillation attachment, along with words and the weight midpoint. These are
  proof targets, not permission to edit more sources.

This pair tests two decisions: should the dalet/resh distinction use a projected
bar versus a rounded shoulder, and what regular-to-bold thickness relationship
fits Virtua? The first candidate should answer those before expanding the scope.

## Feedback and outcome

| Date | User feedback | Interpretation and scope | State / follow-up |
| --- | --- | --- | --- |
| 2026-10-19 | Build reference sheets, pick the first Hebrew group, record corrections, and start with small loops. | Authorized rendering, investigation, and repository feedback workflow. | Implemented; does not approve the proposed dalet/resh drawings. |
| 2026-10-19 | “make the dalet and resh candidate in both masters ... keep it in scratch for now” | Authorizes only four scratch GLIF outline edits and candidate builds/proofs; no active-source application. | Candidate v1 ready; active sources unchanged. |
| 2026-10-19 | “the big problem ... is the weight ... use the basic a-z and A-Z latin drawings ... core latin green graded glyphs” | Green Virtua Latin is the weight/style reference. External fonts guide Hebrew distinction, not stroke targets. | Measure live green Latin; preserve it unchanged. |
| 2026-10-19 | “The weight looks good, apply” and “not 100% sure ... keep this flexible”; specimens are “sloppy and hard to read”. | Apply only the reviewed pair in both masters; retain cross-script weight as OPEN; redesign comparison sheets with a disciplined grid. | Applied and verified. Three-sheet layout ready for feedback; no final weight contract or green grading. |

Current next step: [HEB-002](../hebrew-002/README.md), the he/het/tav comparison. The refined specimen layout is approved. Candidate v1 is applied; cross-script weight remains provisional and no further glyph scope is assumed.


## Candidate v1 — Latin-weight reference (2026-10-19)

[Four-column before / candidate / Rubik / Noto proof](candidate-v1-comparison.png),
[Latin weight context](candidate-v1-latin-weight.png), and
[mark/related-form proof](candidate-v1-marks.png). Proof JSON sidecars capture the
actual final-built font hashes and shaping. [Candidate evidence](candidate-v1-evidence.json)
records source scope, reference hashes and validation. The four candidate GLIFs
are preserved under `candidate-v1-sources/` for review, not as active build inputs.

This candidate implements the requested weight/style reference direction:

| Measurement | Regular | Bold | Live green reference |
| --- | ---: | ---: | --- |
| Both Hebrew stems | 96 | 192 | n straight stems |
| Both Hebrew top bars | 96 | 168 | E horizontal bars |
| Terminal chamfers | 16 | 16 | n / E / H exposed corners |
| Dalet rightward bar projection | 64 | 64 | Proposed structural distinction, not copied from another font |
| Height | 576 | 576 | Existing Hebrew flat height, retained |
| Advances | 568 | 624 | Existing advances, retained |

Resh's outer upper-right cubic is the green n shoulder translated without scaling
(Regular x−16/y−16; Bold x−88/y−16). The inner arc adapts n's structure on the
8-unit grid to connect the chosen stem and bar weights with axial tangents.
Dalet insets the stem beneath its bar and gains a full Bold stem. Its rightmost
ink shifts 484→480 Regular and 502→504 Bold (sidebearings therefore change by
4/−2 units); advances remain fixed. Anchors and colors are byte-equivalent outside
the replaced outline XML. No Latin source was changed.

Live references differ from old tables: green H currently has 100/192-unit stems,
E has 100/200, and n has 96/192. The chosen Hebrew stem target follows n, matching
its 576-unit design scale; the horizontal target follows E. These are candidate
choices for review, not a newly approved family-wide Hebrew contract. No existing
OPEN Latin decision or DESIGN.md dimension table was silently revised.

Validation: four scratch GLIF outlines changed; all active source hashes unchanged;
zero master-compatibility blockers; both curve-lint runs clean; 20 regression tests
pass; scratch `make preflight` succeeds. Across 6,048 variable glyph/weight
comparisons (seven weights), only plain dalet/resh outlines differ and every advance
is unchanged. Scoped Fontspector checks (outline, overlaps, interpolation) on all
five candidate fonts yield 19 PASS / 13 WARN / 8 SKIP, identical finding sets to the
baseline. This is not a new full Google Fonts release audit.

Correction to the initial dependency assumption: daletdagesh-hb and reshdagesh-hb
are standalone purple outlines, not component composites. They therefore retain
their older designs; wide dalet is also unchanged. Their inconsistency is visible
in the related-form proof and must be addressed under a later named scope if this
plain-letter direction is accepted. The baseline build was also regenerated for
verification; active source drawings remain unchanged.

**Agent visual assessment:** the pair is much more distinct, the midpoint no longer
mixes a heavy resh with a Regular-weight dalet, and Bold relates more closely to the
green Latin. Bold's compact junction/shoulder density and the dalet projection are
the primary optical decisions for Eli. No human drawing approval is inferred.

Reproduction: `prepare_candidate.py --output out/qa/<new-directory> --write`
creates a new scratch snapshot only, checks the recorded target/reference source
hashes, and writes four candidate outlines. Run `./build.sh` from that scratch
root, never by assuming the command changes directory itself. The proof recipes
are also retained in the candidate JSON sidecars. No apply script is provided.


## Application authorization and weight qualification — 2026-10-19

Eli: “The weight looks good, apply the dalet and resh candidate to both masters.”
Eli also said “I am not 100% sure on the weight yet so keep this flexible”, explaining
that Latin lowercase/capitals have a small weight distinction and the appropriate
Hebrew/Arabic relationship on this grid remains unresolved.

Interpretation: apply the reviewed four GLIF outlines exactly. This accepts the
candidate for continued development, not a final cross-script weight standard or
green grading. Retain 96/192 stems and 96/168 bars as the current provisional trial;
future review must compare both Latin cases and Hebrew/Arabic at useful reading
sizes. No instruction to change Latin weights, unify cases, or propagate these
numbers throughout Hebrew or Arabic. Reference supplied by Eli:
https://elih.net/blog/virtua-grotesk/ (read 2026-10-19, especially section 03).

Specimen feedback: the existing sheets are “sloppy and hard to read”. Redesign with
a disciplined modular grid, strong hierarchy, consistent baselines and purposeful
whitespace in the Swiss modernist tradition, retaining the approved gray palette.
Keep the before/after and reference evidence, but separate detail, text, and
cross-script weight questions into clear sheets. This is a layout direction;
Eli has not yet approved the new specimen design.


## Applied result and specimen redesign — 2026-10-19

The four active GLIFs now exactly match candidate v1. Source hashing checked
1,759 files against the frozen baseline: only those four differ. Colors, anchors,
and advances remain unchanged. Regular/Bold curve lint is clean; active preflight
and all 20 regression tests pass. All five compiled fonts match the candidate
at table level after normalizing only head timestamps/checksum adjustment.
See [application and verification identities](applied-v1-evidence.json).

The new specimen set uses a 1600 × 1280 frame, 80-pixel margins and a 40-pixel
module, flush-left hierarchy, restrained red navigation accents, and the approved
gray palette. Font comparisons keep a shared origin and baseline; the layout does
not optically align or resize individual glyphs. Neutral Helvetica captions are
separate from the actual font samples. This revision changes presentation, not
any glyph beyond the approved pair.

1. [Letterform comparison](specimen-v2-01-form.png): before / applied / Rubik / Noto,
   at 400, 550, 700 and a fixed 192 pixels per em.
2. [Reading texture](specimen-v2-02-text.png): the same four columns, with 44/32/24
   pixel-per-em samples. Other Hebrew drafts remain visibly unfinished.
3. [Latin / Hebrew weight](specimen-v2-03-weight.png): live green lowercase n/o and
   capitals H/O alongside applied dalet/resh, all at 176 pixels per em. The script
   relationship is explicitly provisional.

All three final pages were visually inspected; grid-overlay inspection checked
alignment and the third sheet's pagination. The shared renderer also passed an
identical-font zero-difference check, a seven-row/three-page pagination check, and
an oversize rejection check. It fails with a useful size message instead of
silently fitting oversized samples.

[Recipe](../../../documentation/proofs/hebrew_review.py), [render identities](specimen-v2-evidence.json),
and [rendering instructions](../../../documentation/qa.md#standard-designbot-comparison-workflow) make the design
repeatable. The retained PNGs are selected evidence; large scratch backups remain
under `out/qa/2026-10-19/applied-dalet-resh/`. Eli's review of this new layout is
still pending. This is acceptance of a provisional pair, not final script grading.


Online full Google Fonts QA was refreshed after application: the five-font run
has 530 PASS / 28 WARN / 1 FAIL / 39 INFO / 294 SKIP; the downstream package has
162 PASS / 6 WARN / 9 FAIL / 10 INFO / 41 SKIP. Neither has ERROR/FATAL results.
Finding IDs and codes match the preceding applied-Hebrew baseline. No exclusions
were added. Initial sandboxed attempts could not reach network resources and
are superseded by the separate `full-qa-online/` and `package-qa-online/` reports.
The font is still not release-ready; this design acceptance does not waive QA debt.


## Specimen feedback and rendering discussion — 2026-10-19

Eli confirmed the modular sheets are “much more readable and clear”. Requested
changes: only light/dark gray, no red; reversible light/dark presentation for
judging difficult drawings; title case instead of all-caps labels. This qualifies
the earlier layout approval, not the provisional glyph-weight direction.

Eli also reported uneven label rendering: a heavier E at bottom left and an I
at a different cap height in the top line. The root cause is not established.
The v2 headings/captions use Pillow ImageDraw with macOS Helvetica.ttc faces 0/1
(verified as Regular/Bold); font samples use explicit HarfBuzz shaping and
unhinted FreeType rasterization. These sheets do not currently use DesignBot.
Do not treat a caption-rendering symptom as evidence to edit Virtua's outlines.

Before fixes, Eli requested discussion of moving these sheets to DesignBot Rust
scripts. Local source inspection confirms Parley layout, Swash outline scaling,
Kurbo paths and AnyRender/Vello CPU rendering, with font loading, variation axes,
text measurement and multiple-page PNG support. Current Swash scaling hardcodes
hinting on. Font selection is by family name after registration: before/after
files share a family, so an implementation must isolate their font contexts or
provide exact face selection, never assume load order identifies the column.
Use `designbot --raw` for QA exports; default CLI social processing is unsuitable
for evaluating faithful weight/color. Local source evidence:
`~/GH/repos/designbot/designbot-render/src/renderer.rs` and
`~/GH/repos/designbot/designbot-cli/src/main.rs`.

Recommended next step: a small DesignBot diagnostic of the reported caption
strings and one Hebrew comparison at identical sizes/baselines, in both gray
polarities. Verify face identity, glyph positions, variation coordinates and
hinting behavior before porting the three-sheet recipe. Preserve original v2
PNGs and hashes. No renderer change, font-source edit, or assertion that migration
alone fixes the artifacts was made during this discussion.


## DesignBot diagnostic and Virtua captions — 2026-10-19

Eli authorized the diagnostic Rust script and light/dark versions, then requested
Virtua instead of Helvetica. All current headings/captions now use the applied
Virtua variable font at Regular (400). Only the upper-left frozen control panel
uses Pillow; it renders the same Virtua file at the same sizes/baselines as the
upper-right DesignBot panel. All other text and the complete layout use DesignBot.
The uppercase E/I/H/T line is a literal glyph test, not all-caps page furniture.

- [Light diagnostic](designbot-diagnostic-light.png)
- [Dark diagnostic](designbot-diagnostic-dark.png)
- [Rust script](../../../documentation/proofs/designbot_diagnostic.rs)
- [Control generator](../../../documentation/proofs/designbot_diagnostic_control.py)
- [Hashes and measured results](designbot-diagnostic-evidence.json)

The diagnostic has a fixed 1600 × 1280 grid with 80-pixel margins and a 40-pixel
module. Only #dedede and #444444 are specified; antialiasing produces intermediate
neutral grays. Pixel checks confirm opaque images with equal R/G/B channels and
no values outside 68–222 in both final outputs. Final light/dark PNGs and the
layout overlay were visually inspected. Before/after Hebrew uses independent
font contexts to prevent same-family collisions, with 400/700 instances at
192 pixels per em and reading text at 32. No Virtua source or build was changed.

Findings:

- In the original Helvetica file, E/I/H/T outlines all reach 1469/2048 units.
  Both Pillow and DesignBot render I at 14 pixels versus 15 for E/H/T at 20 px.
  Removing hint instructions in a local scratch Helvetica face makes all four
  reach 15 pixels in DesignBot. This isolates a hint-dependent result; changing
  the rendering engine alone did not eliminate it. That scratch system font
  remains ignored local diagnostic material, not a distributable project asset.
- With Virtua, all four letters align in each renderer at 18, 20 and 40 px.
  DesignBot heights are 14/15/30 pixels. Pillow heights are 14/16/30, showing a
  whole-row rasterization difference at 20 px rather than an isolated short I.
  No separate heavier-E defect was established by this test; perceived weight
  still depends on size, rasterization and polarity. Do not claim every rendering
  issue fixed from these four glyphs.
- Transparent DesignBot frames contain premultiplied RGB in the tested backend,
  while image_rgba expects straight alpha. An initial composition produced dark
  edge halos. The script restores the known monochrome ink RGB while preserving
  coverage before compositing, and final grayscale-range checks pass. This is
  local script handling; the DesignBot repository was not modified.

The current diagnostic leaves DesignBot hinting enabled and uses --raw, avoiding
social-media processing. It proves the focused workflow, not complete Arabic/
Hebrew shaping parity. The remaining specimens have not been ported. Next review:
Eli's preference between the two polarities and approval of the Virtua-caption
presentation; then port the existing three-sheet recipe with explicit font
identities, instance coordinates and rendering policy.

Reproduce from the repo root (substitute an explicitly frozen before font if the
ignored local cache is unavailable; never recreate “before” from today's source):

```sh
.venv/bin/python documentation/proofs/designbot_diagnostic_control.py \
  --font 'fonts/variable/VirtuaGrotesk[wght].ttf' \
  --output-dir out/qa/2026-10-19/designbot-diagnostic

# Change light to dark in the mode, output and control arguments for dark mode.
designbot --raw documentation/proofs/designbot_diagnostic.rs \
  --output out/qa/2026-10-19/designbot-diagnostic/light.png -- light \
  'out/qa/2026-10-19/hebrew-dalet-resh-v1/before-fonts/variable/VirtuaGrotesk[wght].ttf' \
  'fonts/variable/VirtuaGrotesk[wght].ttf' \
  'fonts/variable/VirtuaGrotesk[wght].ttf' \
  out/qa/2026-10-19/designbot-diagnostic/pillow-light.rgba
```

Set GRID_VIEW=1 for the overlay; PROBE_DIR to a scratch directory exports isolated
E/I/H/T coverage probes as 320 × 80 RGBA buffers. The Rust script targets Virtua
labels; the archived Helvetica investigation predates that user-directed change.


## DesignBot standard workflow — 2026-10-19

Eli: “Looks good, let's port the three comparison sheets to DesignBot Rust scripts
using Virtua for the labels, title case, and the two grays. Keep both light and dark
versions and record this as our standard workflow.” Additional direction:
“for the larger headlines lets track the text in a bit tighter.”

Implemented: [`hebrew_review.rs`](../../../documentation/proofs/hebrew_review.rs) now renders the
entire three-sheet set. [`hebrew_review.py`](../../../documentation/proofs/hebrew_review.py) only
orchestrates DesignBot and records/verifies evidence; no Pillow text or sample
rendering remains in this set. The same Rust layout supports `form`, `text`, and
`weight` modes, `applied`/`candidate` labels, and both polarities. Run instructions
are in the [standard workflow](../../../documentation/qa.md#standard-designbot-comparison-workflow).

| Sheet | Light | Dark |
| --- | --- | --- |
| Dalet / Resh | [Light](designbot-v1-01-form-light.png) | [Dark](designbot-v1-01-form-dark.png) |
| Reading Texture | [Light](designbot-v1-02-text-light.png) | [Dark](designbot-v1-02-text-dark.png) |
| Latin / Hebrew | [Light](designbot-v1-03-weight-light.png) | [Dark](designbot-v1-03-weight-dark.png) |

The 64 px headlines use −0.02 em tracking (−1.28 px), an initial interpretation
of “a bit tighter”, not a separately approved numerical contract. Other labels
and specimen text use zero added tracking. Compared with zero-tracking controls,
all three sheets differ only within their headline regions; sample and caption
pixels are identical. The value remains adjustable through the runner.

All six final PNGs and all three light grid overlays were visually inspected.
Checks pass for font family, weight ranges, required cmap coverage, sample
advances/ink bounds, and opaque neutral-grayscale pixels within 68–222. Before
and after are isolated font contexts; native-size alpha composition retains
coverage without dark halos. Hinting remains enabled and exports use --raw.
These are current DesignBot renders, not claims of raster identity with the old
FreeType sheets or exhaustive script-shaping acceptance.

[Evidence](designbot-v1-evidence.json) records the fonts, Rust source, runner,
compiled renderer, output hashes, and headline-isolation checks. A guard checked
1,759 source files against the already-applied dalet/resh snapshot: no font source
changes in this presentation pass. No build or release QA rerun was required.
The previous full QA findings and provisional Hebrew weight remain unchanged.

This method is recorded in the design-review preferences, QA instructions, and
canonical render-specimen/specimen-grid-layout skills. The standard workflow is
approved; the specific −0.02 em headline adjustment is ready for visual feedback.


## Editorial layout refinement — 2026-10-19

Eli approved the direction of the DesignBot set, then noted “we are overusing /
here” and requested a cleaner Swiss editorial layout. Recorded as P012 in the
shared preferences. Interpretation: use placement and type hierarchy to separate
information, with fewer separators and less repeated metadata.

The new revision separates font names from Before, Applied and Reference roles.
It removes redundant column numbers, gives each page a simple folio, states the
rendering size once, and aligns weight names beside their numeric coordinates.
Titles use “and” instead of slashes. Headings remain title case; explanatory
footnotes now use sentence case for quieter reading. The two grays, Virtua labels,
64 px headlines and −0.02 em headline tracking remain unchanged.

| Sheet | Light | Dark |
| --- | --- | --- |
| Dalet and Resh | [Light](designbot-v2-01-form-light.png) | [Dark](designbot-v2-01-form-dark.png) |
| Reading Texture | [Light](designbot-v2-02-text-light.png) | [Dark](designbot-v2-02-text-dark.png) |
| Latin and Hebrew | [Light](designbot-v2-03-weight-light.png) | [Dark](designbot-v2-03-weight-dark.png) |

All six final pages and three light grid overlays were visually inspected. The
three specimen regions on every page are pixel-identical to DesignBot v1; only
page furniture changed. All 1,759 source files match the already-applied snapshot.
Palette, coverage, font identity and ink-bound checks pass. No font build or
release QA rerun was needed. [Evidence](designbot-v2-evidence.json) records these
checks and input/output identities. Earlier images remain as historical evidence.

Agent assessment: separating names from roles makes the comparison easier to
scan and lets the specimens dominate. This revision implements the requested
direction; its specific layout is ready for Eli's feedback. No new glyph changes,
weight approval or grading are implied.


### Layout approval

Eli, 2026-10-19: “Looks good, let’s keep this as the standard and get back to the Hebrew.”
The editorial v2 layout is now approved as the standard. Continue with
[HEB-002](../hebrew-002/README.md); the glyph-weight relationship remains provisional.
