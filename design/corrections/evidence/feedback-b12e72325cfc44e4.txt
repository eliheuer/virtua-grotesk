# ARB-006 — Autonomous Arabic first pass

## Supervised review resumed — 2026-10-28

Current scope supersedes the historical autonomous authorization below: refresh
the proof, compare references, and propose one glyph before changing outlines.
No drawing approval or timed-loop restart is implied.

The saved UFOs were rebuilt into the VF and four statics; all 3,134 source-file
hashes remained unchanged. Current VF SHA-256:
`59076661e210022035f203cb815c3c6d7f47312bc944bc673dc6917d12b650fe`.
The live proof retains the previous handoff as Before and labels the fresh build
Current saved drawings. Reproducible local review inputs and renders are in
ignored `out/arabic-review-current/`; these are disposable review artifacts, not
a durable backup or correction pair.

**Proposed first target, awaiting Eli's decision:** `kaf-ar.medi` in Regular
(orange) and Bold (red). Neither target has components or component consumers.
Basic alphabet and joining-form sheets were inspected at 400/700 against IBM
Plex Sans Arabic, Noto Sans Arabic, Readex Pro and Rubik; the selected medial
form was also inspected at 400/550/700 and in `مكتب مكتبة` at the endpoints.
Virtua's upright with a separate internal stroke differs from the diagonal
connecting construction in all four references; the internal stroke nearly
closes in Bold. Proposed direction: review the medial structure, open space and
entry/exit transitions while retaining Virtua's weight and terminal language.
This is a design proposal, not a native-reader verdict or outline approval.
Yeh/Maksura and Heh also need review, but green donors and human reservations
must be respected. No glyph, grade, feature or metric was changed in this review.

## Medial Kaf scratch candidate — 2026-10-28

Eli answered “yes please” to preparing `kaf-ar.medi` in Regular and Bold on
scratch and showing it before application. This approves only that preparation.
The initial target proposal above is now superseded by this bounded approval;
active application and final visual grading remain unapproved.

The candidate replaces the upright/internal stroke with a single connected
22-point diagonal contour, two cubic transitions and a level joining bar.
Advances 808/844 and all anchors are exact; only candidate grades are purple.
Green x/u supplied construction and weight guidance, not copied reference-font
outlines. No other glyphs or component donors changed. Exact before/candidate
GLIFs and a compact receipt are retained in [the source pair](kaf-medial-2026-10-28/receipt.json).
Large binaries, screenshots and disposable scripts remain in ignored
`out/arabic-kaf-medial-candidate/` to avoid adding build copies to Git.

Compiled comparison is open at http://127.0.0.1:60272/ with **Current saved
drawings** versus **Scratch candidate · Not applied**. Complete joined forms,
words and marks were inspected at 400/550/700; enlarged endpoint silhouettes
and signed curvature combs were inspected. Bold's weight, the flat bar's length,
and the angular upper turn remain design questions for Eli. G1 transitions
retain curvature jumps; numerical checks do not approve their appearance.

Both masters are compatible. Five sampled weights have no proper contour
crossings; 8,162 non-target outline/advance comparisons and 180 shaping samples
are unchanged. All 3,134 active source hashes remain exact. The grid-8 report
retains inherited anchor exceptions and Bold's 844-unit advance/boundary;
it is not a zero-findings result. Scratch binaries were built with the canonical
snapshot/VF-instancing path; metadata fixing completed after copying the missing
scratch OFL. No active build, full package QA or release-readiness claim.

## Historical autonomous handoff — superseded

Eli authorized this pass on 2026-10-21 while repairing Runebender component
editing. Do not wait for per-batch feedback. Apply reversible working drawings
in the active UFOs; retain human grading for the later review. No publication
or release approval is implied.

Baseline checkpoint: `05b8d2e1`, including Beh bases, circular single dots,
scrollbar repair and the updated authorization. Before fonts and exact sources
are saved per batch; full source hashes detect concurrent editor changes.

## Quality hold resolved for continuation — 2026-10-21

Batch 04 was rejected; batch 05 fixed crossings and joining defects, and batch
06 corrects the medial loop after further feedback. Endpoint/intermediate
raster inspection and source checks are complete. Eli explicitly requested
resuming independent base-family work without awaiting his feedback. Human
review remains pending; this does not approve the drawings or mark them green.

## Concurrent human editing — 2026-10-21

Eli has finished the component-editor repair and is manually editing `ببب ب`.
Reserve the Beh isolated/initial/medial/final forms in both masters and their
recursive component donors, including shared dots. Do not modify their geometry,
metrics, anchors, placements or grades. Recompute dependencies before other
batches and exclude any shared donor that could change this human work.

## Current progress

- Batch 01: Bold Dal and Reh isolated/final outlines, plus five inherited
  wrapper advances. Applied; build/preflight, curve checks, 98 shaping
  comparisons and endpoint/intermediate browser proofs completed. Human
  review remains pending. See [batch evidence](batches/01-dal-reh/README.md).
- Batch 02: Bold Waw isolated/final and two inherited wrapper advances applied.
  Both endpoint raster sheets inspected; build/preflight and 133 shaping checks
  passed. See [Waw evidence](batches/02-waw/README.md).
- Batch 03: Bold Noon / ghunna shared bowls and two wrapper advances applied.
  Raster inspection exposed and resolved the final dot/stem collision. Both
  endpoint sheets inspected; build/preflight and 161 shaping checks passed.
  See [Noon evidence](batches/03-noon/README.md).
- Batch 04: Bold initial/medial Feh–Qaf shared heads and 14 wrapper advances
  applied. Four endpoint raster sheets, two source-scale renders and the 550
  browser proof inspected; build/preflight and 217 shaping checks passed.
  See [shared-head evidence](batches/04-feh-qaf-heads/README.md).
- Batch 05: repaired the full Bold Feh/Qaf family and circular two/three-dot
  donors. 308 shaping comparisons, scoped regression checks and preflight pass.
  Final visual review remains incomplete at the requested Git checkpoint.
  See [repair evidence](batches/05-feh-qaf-repair/README.md).
- Batch 06: medial Feh/Qaf and final Feh loop revised, with 400/550/700 raster
  inspection, 210 shaping checks and preflight. See [loop evidence](batches/06-medial-loop/README.md).
- Batch 07: Bold Lam isolated/initial/medial repaired with five wrapper advances;
  252 shaping checks, 400/550/700 and large raster inspection, preflight.
  Final Lam and Lam–Alef structure remain unresolved; see [Lam evidence](batches/07-lam/README.md).
- Batch 08: final Lam candidate in both masters addresses Eli’s continuing
  complaint. Built and checked at 400/550/700 with 70 shaping comparisons.
  **Applied** after Eli explicitly approved both masters including green Regular;
  active-source build, preflight and 70 shaping checks passed.
  See [candidate evidence](batches/08-lam-final/README.md).
- Batch 09: four Bold Meem forms repaired; final advance gap closed, medial
  shoulders raised and joined. 287 shaping checks, 400/550/700 plus large raster
  inspection and preflight. Green Regular medial construction remains a
  follow-up; see [Meem evidence](batches/09-meem/README.md).
- Regular final Lam changed under Eli’s named green exception. Other green
  drawings and Eli’s manual hamza are preserved.
- The full Arabic first pass is **in progress**, not complete or human-approved.

- Batch 10: four Bold Hah bases repaired with shared head/bowl geometry and
  matching Jeem/Khah/Tcheh wrapper advances. Jeem/Khah dot placements adjusted
  without changing donors. 336 shaping checks, 400/550/700 rasters, large detail,
  compatibility and preflight verified. Regular unchanged; inherited Tcheh
  initial and dot-placement problems remain explicit. See
  [batch evidence](batches/10-hah-family/README.md).

- Batch 11: Tcheh initial base reconciled to Hah in both masters; three-dot
  groups moved below joins / inside bowls using an exclusive circular donor.
  Explicit top anchors preserve base attachment. 364 shaping comparisons,
  400/550/700 rasters, marked endpoint proofs, sampled clearance and preflight
  passed. All Beh reservations unchanged. Readex Pro U+0686 is explicitly
  unavailable. See [Tcheh evidence](batches/11-tcheh/README.md).

- Batch 12: Bold initial Ain and Ghain repaired; tangent kinks and unintended
  reversal removed, mouth opened, wrapper width matched and dot centered.
  385 shaping checks and 400/550/700 rasters with all four references inspected.
  Regular and Beh reservations unchanged. **Other Ain/Ghain forms remain
  unfinished.** See [initial evidence](batches/12-ain-initial/README.md).

- Batch 13: Bold medial Ain/Ghain repaired; 176-unit joins, a 160-unit crown,
  cleaned counter turns, matched advances and locally centered dot. 413 shaping
  comparisons, 400/550/700 reference rasters, large and marked proofs, and preflight
  completed. All Regular and Beh sources unchanged. Final/isolated forms remain
  unfinished. See [medial evidence](batches/13-ain-medial/README.md).

- Batch 14: Bold final Ain/Ghain repaired; reversing shelf and tangent kinks
  removed, 160-unit bowl extrema/terminal, 176-unit join, matched 912 advances
  and centered Ghain dot. 434 shaping comparisons, 400/550/700 reference rasters,
  large/marked proofs and preflight completed. Regular and Beh unchanged.
  See [final evidence](batches/14-ain-final/README.md).

- Batch 15: Bold isolated Ain/Ghain repaired; reversing inner curve and
  tangent kinks removed, 16-unit terminal cuts and matched 784 advances.
  455 shaping comparisons, 400/550/700 reference rasters, large/marked proofs
  and preflight completed. Existing Ain/fatha collision is recorded for the
  attachment pass. Regular and Beh unchanged. See
  [isolated evidence](batches/15-ain-isolated/README.md).

- Batch 16: Bold Seen initial/medial teeth repaired with matching Sheen and
  seenSixdots wrapper advances and local dot placement. Regular and Beh unchanged.
  400/550/700 reference rasters, large details, compiled joins, 525 shaping checks and preflight
  checked. Final/isolated forms, final Sheen gap, low fatha and the inherited
  incomplete U+069C dot construction remain explicit. See
  [teeth evidence](batches/16-seen-teeth/README.md).

- Batch 17: Bold Seen/Sheen final and isolated forms repaired with consistent
  teeth/bowl weight and matched wrapper advances. Two orange Regular final
  wrappers have advance-only gap corrections; drawings and grades unchanged.
  525 shaping checks, 400/550/700 four-reference rasters, large/word/marked
  proofs and preflight completed. Beh preserved. See
  [bowl evidence](batches/17-seen-bowls/README.md).

- **Batch 18 — Bold Sad/Dad four-form repair:** all eight Bold bases/wrappers
  repaired with consistent 160-unit weights, 176-unit joins, open counters and
  local dot placement. Four Regular Dad advances now match their bases; Regular
  ink/grades remain intact, with two collinear points added in isolated Sad for
  compatible Bold chamfers. 581 shaping checks, 400/550/700 reference rasters,
  large/word/join/marked proofs and preflight completed. Beh/manual hamza preserved.
  Sad final's inherited top anchor is displaced; attachment remains deferred.
  See [Sad/Dad evidence](batches/18-sad-dad/README.md).

- **Batch 19 — Bold Tah/Zah four-form repair:** counters opened, stems/caps
  regularized, stem/bowl trough replaced with a direct machined connection and
  local Zah dots lowered/centered. Three collinear Regular additions preserve
  geometry; isolated Regular Zah advance matches Tah. 637 shaping comparisons,
  endpoint/intermediate reference rasters, large/word/marked proofs and preflight
  completed. Beh/manual hamza unchanged. The Regular trough and high dots remain
  a recorded refinement; see [Tah/Zah evidence](batches/19-tah-zah/README.md).

- **Batch 20 — Bold Kaf isolated/final:** bowl reversals and malformed cuts
  repaired; inner signs made smaller and open; final baseline joins continuously.
  All Regular and Beh sources unchanged. 679 shaping comparisons, 400/550/700
  four-reference rasters, large/word/join/marked proofs and preflight completed.
  Initial/medial Kaf remain structurally unlike the references; Regular initial
  is green. See [Kaf evidence](batches/20-kaf-isolated-final/README.md).

- **Batch 21 — Keheh/Gaf final forms, both masters:** corrected the duplicated
  upright Kaf construction to angled heads, retained bowls/joins, and added Gaf's
  missing upper bar. 728 shaping comparisons, 400/550/700 reference rasters,
  endpoint full-form/marked/word proofs and large details checked. Readex lacks
  U+06A9/U+06AF and is explicitly unavailable. Four inherited Bold anchor grid
  exceptions remain. Other forms stay on the queue; Beh/manual hamza untouched.
  See [final-form evidence](batches/21-keheh-gaf-final/README.md).

- **Batch 22 — isolated Keheh/Gaf, both masters:** corrected the upright Kaf
  duplicates to angled heads and isolated bowls; Gaf retains a Keheh component
  plus a local bar. Three-dot wrappers receive advance-only fixes. 777 shaping
  comparisons and endpoint/intermediate reference rasters checked. All shared
  donors, Beh and manual corrections preserved. Existing Gaf propagated anchors
  are retained explicitly and remain on the attachment queue. See
  [isolated-form evidence](batches/22-keheh-gaf-isolated/README.md).

- **Batch 23 — initial/medial Keheh/Gaf, both masters:** replaced the wrong
  upright Kaf/internal sign and shared S-like Gaf donor with the angled family
  head and separate bar. Fourteen sources; initial/medial advances 704/832 and
  23/21-point bases. Four three-dot wrappers have advance-only fixes. All other
  sources, Beh18 and manual hamza unchanged. 805 shaping comparisons, full rows
  at 400/550/700, endpoint word/medial/marked proofs, large details and preflight.
  Gaf propagated anchors preserved explicitly; their excessive height and 143
  inherited grid findings remain scoped in the
  [joining-form evidence](batches/23-keheh-gaf-joining/README.md).

- **Batch 24 — Bold isolated/final Heh:** aligned bowl handles and opened the
  pinched counters; restored final stem and cuts, with 160-unit extremum weights
  and 176-unit incoming join. Advances576/608; final Teh Marbuta advance-only
  correction704→608. Three files; all Regular, Beh18 and manual hamza unchanged.
  840 shaping comparisons,400/550/700 all-four-reference rasters, large and
  endpoint full-form/word/marked proofs and preflight. Six inherited Bold grid
  findings remain anchors/dot offsets. Initial/medial Heh still need repair;
  the marked proof retains an old Beh damma / adjacent Teh Marbuta dot collision.
  See [bowl repair evidence](batches/24-heh-bowls/README.md).

- **Batch 25 — Bold joining Heh:** repaired initial and medial curves/counters,
  keeping green Regular and all other source bytes unchanged. Advances992/704,
  joins176, matching49/56-point topology. No sampled reversals, tangent kinks or
  intersections; 833 shaping comparisons and400/550/700 all-four-reference
  rasters, endpoint word/carrier/marked proofs, large details and preflight.
  Increased initial size and medial depth need human review. Existing initial
  fatha collision remains; preserved anchor findings are scoped in
  [joining repair evidence](batches/25-heh-joining/README.md).

- **Batch26 — Bold isolated Goal:** repaired bowl/counter/cap with original18/12
  topology,160-unit extrema and576 advance. Two wrappers match the advance;
  local hamza centered and raised to80-unit cap clearance without changing its
  manual donor.896 shaping comparisons,400/550/700 rasters, large/word/marked
  proofs and preflight checked. All Regular, Beh18 and other source bytes unchanged.
  Rubik/Readex missing coverage is explicit. Final trial withdrawn: references
  expose an open-terminal structural mismatch; initial/medial need structural
  follow-up too, with green Regular protected. Dots remain close/left; four
  inherited Bold grid findings retained. See [evidence](batches/26-goal-bowls/README.md).

- **Batch27 — Bold medial Doachashmee:** one independent source, matching
  12/12/32-point topology,160-unit loop extrema and176-unit join, advance704.
  All Regular, Beh18, manual hamza and other sources unchanged.875 shaping
  comparisons,400/550/700 rasters, large/carrier/marked proofs and preflight
  checked. Eight inherited anchor findings retained. Baseline references expose
  wrong isolated/final single bowls and a different initial construction; those
  need paired-master structural repair. Rubik/Readex lack U+06BE, explicitly
  unavailable. See [evidence](batches/27-doachashmee/README.md).

## Remaining queue

Use `inventory.py` / `inventory.json` to check exact names, source grades and
component dependencies. Recompute before each batch. A component change affects
its descendants even when their files do not change; protect green descendants.
The old `scripts/arabic_*` builders contain historical color semantics and
Bold-equals-Regular recipes. Do not run them wholesale.

1. Feh/Qaf repair is ready for later human review; preserve its evidence.
2. Meem Bold first pass is saved in batch 09. Green Regular medial sits lower
   than the other forms; a named exception is needed for that construction.
   Final Lam is repaired in batch 08. Lam–Alef still has structural issues
   involving green Regular drawings; keep that follow-up open.
3. Tcheh base and dot first pass is saved in batch 11. Bold Ain/Ghain four-form repairs
   are saved in batches 12–15, pending human review. Regular Jeem final dot collision and Khah dot
   heights remain placement follow-ups; preserve protected base drawings.
4. Seen/Sheen Bold first-pass bases are saved in batches 16–17; human review
   pending. Sad/Dad Bold first pass is saved in batch 18 and Tah/Zah in batch 19.
   Orange Regular Tah/Zah trough/dot heights remain a refinement; preserve
   the current exact evidence when preparing that follow-up.
5. Yeh/Maksura/Barree next; recompute Beh dependency reservation.
   Doachashmee Bold medial is repaired in batch27; isolated/initial/final
   need paired-master structural follow-up. Detect green by RGBA and markLabel.
   Goal isolated Bold is repaired in batch26. Its initial/medial/final need
   structural follow-up against covered references; Regular initial/medial are green.
   All four Bold Heh bases are repaired in batches24–25, awaiting human review.
   Keheh/Gaf initial/medial and the shared bar are repaired in batch 23.
   Isolated forms and local wrappers are repaired in batch 22.
   Both final forms are repaired in batch 21; the separate three-dot final
   Keheh remains a base follow-up; Gaf attachment remains later work. Kaf isolated/final Bold repair is in batch 20;
   initial/medial contextual construction remains unresolved. Regular initial
   Kaf is green; preserve it.
6. Reconcile duplicated Beh-family outlines (Teh/Peh/Tteh/Yeh extensions)
   with the shared roots; inspect separately drawn Dal/Reh variants too.
7. Dot groups and wrapper placements after base silhouettes stabilize.
   U+069C seenSixdots currently lacks its below group; its old upper donor
   curves also need repair. Seen fatha placement is low after the taller Bold teeth.
8. Diacritics, composite attachment, stacking and spacing. Isolated Ain/fatha
   collides at the existing top anchor (Bold y392); preserve the batch 15 marked
   proof for this repair. Arabic/Farsi digits,
   punctuation and remaining signs. Keep script uncertainties explicit.
9. Whole-script proof and technical QA, then hand back for human edits/grading.

Inspect both masters, but green Regular shapes are fixed construction evidence.
Orange/yellow shapes may be refined without replacing their design. Do not
invent a grade for uncolored glyphs. Preserve the saved manual Bold hamza and
all Hebrew corrections. Newly redrawn outlines use purple, never green.

## Batch contract

Name targets, preserve before state, prepare exact compatible outlines, profile
curves/joins, inspect large renders, and apply only after source hash checks.
Use the 8-unit machine grid and 16-unit exposed / 8-unit small chamfers; do not
snap protected optical coordinates or force equal handles. Existing anchors
are recorded exceptions until the placement phase, not silently repaired.

Build, inspect compiled endpoint/intermediate proofs with Rubik, Noto Sans Arabic,
IBM Plex Sans Arabic and Readex Pro. Use joined-plus-isolated forms such as
`ببب ب`, and right-joining contexts such as `بد د بر ر`. Verify substitutions,
clusters, metrics changes and component closure. Run preflight and preserve
its scope: passing does not mean release-ready or visually approved.

Update this progress section and each batch record at every checkpoint. Commit
only owned paths. If a human source edit arrives, preserve it and refresh the
baseline for the affected family; independent families may continue. Stop only
for a genuine unresolved dependency/decision, not routine application approval.

## Continuation and proof tools

The thread heartbeat `virtua-arabic-first-pass` resumes under Eli’s renewed authorization;
its configured recurrence is 5 minutes (Eli requested tighter unattended continuation)
for continuation while Eli works on the editor. Keep it quiet except meaningful
milestones, completion or blockers; the queue above remains the durable handoff.
Final Lam is applied after Eli’s named Regular green exception. Batch27 Bold medial
Doachashmee repair is the current Working proof.
Next bounded repair: Yeh/Maksura/Barree. Beh and its component donors are
reserved for Eli.
Preserve green Regular initial/medial Feh bases. Regular Noon final dot is low
and remains a recorded follow-up for the placement pass.

The live proof now includes Arabic alphabet, joining forms, all-script samples
and the Working font's encoded repertoire. Fixed DesignBot detail PNGs and their
font-hash receipts live with batch 01; use the shared app/render-detail.py runner
for later batches. Preserve current before/working identity when updating proofs.

## Quality hold and focused Heh retry — 2026-10-21

Eli rejected the batch27 four-form drawing as visibly bumpy and structurally wrong.
Automation is PAUSED. Earlier technical pass counts and "repaired" labels do not
establish acceptable drawing quality. Batch28 Maksura has baseline proof assets
only and no source edits. Do not continue the queue until this hold is explicitly
lifted. Focused retry: identify the intended Heh family, compare complete forms
and their negative spaces against references and live green Virtua construction,
then prepare and inspect a coherent whole-image candidate. Preserve green source
protection and Beh's reservation. Human review is still required.

## Human Heh handoff — 2026-10-21

Eli chose to draw the pictured Doachashmee himself because the retry was taking
too long, and authorized moving to other Arabic bases. Reserve both masters of
ordinary Heh and Doachashmee, all four forms and recursive component donors,
alongside the existing Beh reservation. `human-reservations.json` records the
handoff hashes; always preserve newer editor saves. Batch29 remains scratch-only
and unapplied. The automation remains paused; this handoff permits focused work
on independent bases, not automatic resumption of the old broad queue.

The whole-image gate rejected the proposed next Maksura smoothing loop before
editing: its vertical right terminal is structurally unlike the returning bowl
in all four references. Batch28 still contains baseline assets only. Next focused
candidate: final three-dot Keheh, whose separate old Kaf construction lacks its
dots and differs from its other forms. Inspect that complete form before applying
anything. Do not treat the existing purple Keheh base as human-approved.

## Final three-dot Keheh — 2026-10-21

Eli explicitly authorized the final three-dot Keheh in both weights and required
whole-image inspection with all four reference slots. Batch30 applies only
`kehehThreedotsabove-ar.fina` in Regular and Bold: existing angled final Keheh
base plus existing three-dot component, width960. Whole-row inspection caught
and corrected an initially too-high dot group. Both endpoints,550, large details
and joined contexts inspected; component compatibility,30 shaping comparisons,
compiled-change scope and scratch preflight passed. Rubik/Readex lack U+0763 and
are shown unavailable. Dots remain large/widely spaced; old top anchor below
dot crown remains attachment work. This is a working draft, not human approval.
Heh/Doachashmee, Beh, manual hamza and all donor source bytes remain unchanged.
The live proof is batch30. Automation stays paused.

## Renewed first-pass scope — 2026-10-21

Eli asked to get the whole Arabic to a good-enough state for his manual drawing.
Resume independent bounded repairs and whole-script image review; the 5-minute
continuation is active again. This does not lift green protection or the Beh/Heh
reservations, and does not approve the rejected Doachashmee candidate. Prioritize
wrong skeletons, broken joins, missing dots and visible curve faults. Stop after
a finite first pass and hand back a concise list of protected/unresolved forms.
Current next batch:31 Yeh Barree isolated/final, inspecting actual references
before changing either master. Batch30 is the last applied proof/checkpoint.

## Batch31 — Yeh Barree isolated/final

Applied in both masters: isolated left return and connected final lower bowl,
replacing identical disconnected L constructions. Four sources,960/704 widths,
22/20point contours. Whole400/550/700 images, enlarged endpoints and joined
contexts inspected;30 shaping comparisons, sampled intersections at five weights
and preflight passed. Noto/Plex available; Rubik/Readex unavailable forU06D2.
The angular isolated terminal and width remain human-review choices. Twelve
inherited anchor grid findings and misplaced top832,320 remain attachment work.
All green/Beh34/Heh/manualhamza source bytes preserved. Next: mismatched advances
in non-green component wrappers, which leave visible gaps or excess overlaps.
Do not modify reserved Beh source files or donors; inspect each wrapper closure.

## Batch32 — Core wrapper joining widths

Nineteen advance-only corrections in non-green wrappers are applied. The
Regular final Jeem gap is closed; initial Ghain/Khah/Noon/Qaf/Feh/Sheen/Theh and
selected Yeh/Waw/Alef composites now match their existing joining bases. All
compiled ink is identical at400/550/700;30 shaping comparisons and scratch
preflight passed. Whole-row rasters inspected against all four references.
All34 reserved files, all other source bytes and human grades are unchanged.
The proof visibly retains wrong Yeh returns, crowded Theh dots and Alef-below-
hamza/Beh-dot collision; green Jeem initial/medial and reserved Beh metrics remain.
Live proof:batch32. Next independent cleanup: missing U069C below-dot group and
non-green extension wrappers, followed by whole-alphabet/word images and a finite
manual handoff. The first pass is not yet complete or visually approved.

## Batch33 — Six-dot Seen composition

All four seenSixdots-ar wrappers in both masters now contain six small round
dots: upward triangle above and downward triangle below, with Seen bases and
all shared donors untouched. Regular initial/medial advances match the base.
Whole400/550/700 rows, enlarged endpoints and joining context inspected;50
shaping comparisons, local dot curvature/intersection checks and preflight pass.
Rubik/Readex explicitly unavailable forU069C. All34 human reservations unchanged.
The inherited Regular Seen underside cusps and Bold tooth/bowl proportions remain
review issues; this composition fix does not approve them.124 inherited grid
findings retained. Live proof:batch33. Checkpoints31/32:bab08e8f.
Next: remaining non-green extension wrapper join mismatches, then attachment
collisions independent of reserved sources and whole-script/digit image review.
Do not reattempt protected Maksura/Yeh, Kaf, Lam-Alef or human-reserved Heh.

## Batch34 — Extension joining widths

Twenty non-green wrapper advance fixes applied (19Regular, BoldYeh.init.ctr).
Compiled ink unchanged at400/550/700;45 shaping comparisons and preflight pass.
All34 reservations unchanged. Complete shaped rows inspected. Next immediately:
fehDotmovedbelow-ar.fina and fehThreedotsbelow-ar.fina in both masters use the
wrong Qaf bowl and their below-dots collide with it. Prepare a paired-master
composition using the proper Feh final, preserving donors. Do not call these
forms acceptable merely because their join widths now match. Tteh small-Tah
marks are also absent/replaced with dots; retain as structural follow-up.
Eli specifically wants the final whole alphabet in400/700 with all four refs,
plus contextual forms and a concise manual-work list. First pass still active.

## Batch35 — Feh below-dot construction

Applied12 wrappers: isolated/final fehDotmovedbelow-ar and all four
fehThreedotsbelow-ar forms in both masters. Wrong Qaf bases replaced with the
existing Feh bases; below-dots clear the bowl, and all three-dot groups use the
same corrected small round donor. Whole-image inspection caught and corrected
the initial/medial size mismatch before application. No shared donor modified.
50 shaping comparisons at five weights, whole400/550/700 rows, enlarged endpoints
and preflight completed; all34 reservations and non-target bytes unchanged.
102 inherited grid findings retained. Live proof is batch35.
Next: Tteh's wrong plain-dot component should be the small-Tah mark; inspect all
four reference forms and consumers before correction. Then prioritize whole
core alphabet, words, marks and digit plates over further niche extension polish.
The final handoff must show the whole alphabet at400/700 with all four references
and a concise exact manual-work list. First pass remains active, not approved.

## Batch36 — Tteh small Tah

Eight wrappers applied in both masters. Correct small Tah replaces ordinary dots;
initial uses the matching existing BehDotless base. All shared donors and34
reservations unchanged. Local17/9point contours, clear counters and matching
advances. Whole400/550/700, enlarged endpoint and marked joining images inspected;
50 shaping comparisons, signed curvature and scratch preflight checked. The
malformed shared smallHighTah donor/Rreh remain unchanged and need manual repair.
Rubik/Readex explicitly unavailable. Inherited Beh curves are not approved.
Next: whole-alphabet, joining, word, mark and digit image review for finite handoff.

## Whole-script handoff — after batch36

Tteh is checkpointed at650b557a. The finite autonomous drawing pass is now at
manual handoff; recurrence paused. This supersedes historical next-batch queue
instructions above. [Handoff images and exact manual priorities](handoff/README.md)
contain22 inspected plates: whole28-letter alphabet and every joining family at
400/700, word/mark/digit sheets at400/550/700, plus selected extensions. All four
reference slots are present; missing coverage is explicit. Readex Arabic digits
are shown; its Persian row is unavailable. Numeric cells avoid a DesignBot
all-numeric string stacking problem also present in reference-font rendering.
54 whole-sheet shaping checks found no missing Working glyphs. Active source
hashes match the captured baseline plus the eight Tteh changes; all34 reserved
files unchanged. Preflight/master compatibility remains tied to batch36.

The images visibly retain wrong Yeh/Maksura, contextual Arabic Kaf, Lam-Alef,
Heh/Doachashmee and Goal constructions; uneven bowl/tooth proportions; crowded
dots; mark collisions and malformed numeral shapes. These are not approved.
The handoff lists exact protection and ownership. Do not equate the finite pass
ending with a finished font. Live proof is now `handoff/working`, with actual
pre-batch01 Before and batch36 Working. No release/publication work authorized.

## Correction 01 — align the connecting horizontal, 2026-10-28

Eli: “the kaf is slightly taller and not meeting the horizontal like of the
connecting letters.” Screenshot: `Screenshot 2026-10-28 at 1.29.17 PM.png`.
The visible step corresponds to the Regular scratch bar at y104 versus the
current Beh joining edges at y96. Both baselines are y0. Bold matches at y176.
Interpretation: correct the joining stroke height, not the overall head height.
Scope remains scratch medial Kaf only: lower Regular's bar and its horizontal
curve handle by8, retain the8-unit inner cut, preserve Bold and every active
source. This is a local measured join correction, not a universal Arabic weight
rule. The original candidate source pair remains preserved; no application or
visual approval is implied.

Correction 01 rebuilt successfully on scratch. The corrected upper joining edge
is96/116/136/156/176 at400/475/550/625/700, matching the existing Beh join
interpolation; baseline remains0. Compiled shaping and non-target regression
checks pass again. Both tangent endpoints remain aligned; the Regular grid
report retains only the two inherited x364 anchor findings. Joined rasters and
actual browser text were reinspected at400/550; Bold's candidate source is
byte-identical. Exact corrected Regular and updated receipt are retained in
`kaf-medial-2026-10-28/correction1-Regular.glif` and `correction1.json`.
The live proof is refreshed; active sources remain unchanged. No final visual
approval or full package QA claim.

## Final Yeh review closed — preserve intended design, 2026-10-28

Eli: “lets skip this one, it is designed the way i have it, next”. Exact scope:
`yeh-ar.fina` Regular and Bold. The raised return is intentional; the agent's
proposal to replace it with a descending reference-like bowl is withdrawn.
Do not infer that difference from reference fonts is a defect. No outlines,
metrics, anchors or grades changed. Reference comparison only; local assets in
`out/arabic-yeh-final-review/`. This is not a blanket approval of all Yeh variants.

Next comparison: `kaf-ar.init` Bold (red); Regular initial Kaf is green and
remains protected. Inspect before proposing any drawing change. Corrected
medial Kaf remains scratch-only and unapplied.

## S-like initial Kaf direction — 2026-10-28

Eli: “I want the more kind of S-like, silly, like old-style cuf” and asks to
keep that design while matching the weight. He then requested that direction
be logged and explicitly authorized a redraft in the live review toggle.
Scope: `kaf-ar.init` Bold only, scratch candidate before application. Regular
is green and fixed. Preserve the S-like flow and rounded turns; strengthen
paired stroke edges, keep the inner spaces open and align the connecting bar
to176 at baseline0. Preserve advance736, ink top680, anchors and36-point
master correspondence. No neighboring glyph, grade or feature changes.
The earlier angular medial Kaf remains unapplied and is not a template or
accepted family direction. Final Yeh remains intentionally as drawn.

Construction references: green Regular initial Kaf supplies the approved
skeleton/topology; green Bold u supplies weight/axis-tangent turn conventions.
Bold Latin s is orange and is not used as an approved donor. The initial trial
uses160 top-bar and176 middle/side/joining weights, keeping the supplied S-like
path with optical differences in its two openings rather than forcing symmetry.
These dimensions are candidate choices, not a new universal Arabic weight rule.

Scratch candidate is ready in the live Toggle at700 (press B). Small source
pairs and verification: [kaf-initial-2026-10-28](kaf-initial-2026-10-28/).
All3134 active source files stayed unchanged. Only scratch Bold initial Kaf
changed; compatible masters,252 shaping cases and zero new grid findings.
All unrelated compiled outlines/advances stayed identical in sampled weights.
Regular source is exact; joint cubic-to-quadratic conversion changes the
compiled Kaf representation even at400, so binary outline identity is not claimed.
The candidate retains both S-like openings; heavy central turns and the narrow
lower opening remain for Eli's visual review. No application or release QA claim.
Live proof: http://127.0.0.1:60272/ ; separate stock Diffenator preview:
http://127.0.0.1:60274/diff3proof/diff3proof.html . Full comparison report is
http://127.0.0.1:60274/diffenator/diffenator.html . Old=saved, New=scratch.

Workflow feedback: Eli wants quicker interactive Arabic review. Show one bounded
scratch candidate after build, compatibility, shaping and focused visual checks;
defer broad reports until an accepted group or explicit QA request. Preserve
hash/color guards and the distinction between preparation and application.

## Accepted initial Kaf application — 2026-10-29

Eli: “this looks good. lets commit this work to the repo and move on”.
Approval applies to the reviewed S-like Bold initial Kaf candidate only.
Apply its exact bytes; preserve green Regular and all other source files.
Purple remains the existing candidate grade; acceptance does not assign green.
Earlier medial Kaf remains unapplied; final Yeh remains intentional.

Application verification: canonical build and preflight passed. All five active
fonts match reviewed scratch tables except head metadata. Exactly one of3134
source files changed; all3133 others remain exact. This carries the reviewed
252 shaping cases and scoped regression evidence to the active build without
claiming whole-script QA or release readiness. Live applied Kaf inspected at700.

Next live inspection: isolated Seen at700 with all four reference fonts. Its
straight underside beneath the teeth meets the returning bowl in an abrupt
step; inspect that transition and weight rhythm before choosing a correction.
Bold forms are purple, Regular isolated/final orange, initial/medial green.
No Seen drawing changed or candidate authorized. Reference slant is not a
reason to replace Virtua's upright geometric character.

## Seen rounded-lobe scratch review — 2026-10-29

Eli approved a scratch revision matching his supplied upright, rounded Arabic
style. [Source pairs and bounded review](seen-2026-10-29/README.md). Bold isolated
Seen only; its two isolated dotted consumers inherit the preview. No active
sources changed. Live Toggle700 is ready for approval; Regular/joining forms
are unchanged.

## Seen bowls v3 applied — 2026-10-29

Eli authorized isolated `seen-ar` in Regular and Bold and direct application.
Both inner and outer broad bowl curves now share turning heights and horizontal
bottom tangents; teeth, advances and anchors are preserved. Both drawings are
purple, awaiting human grading. Isolated Sheen and six-dot Seen inherit the
component change; joining forms and all green sources remain unchanged.
Exact before sources and revision3 are retained in
[the Seen review](seen-2026-10-29/README.md). v1/v2 remain rejected examples.
Build and preflight completed; active five-font tables match verified scratch
except timestamps in head. 306 shaping cases and five-weight geometry checks
passed. Browser silhouettes inspected at400/550/700. This is an applied working
revision for manual review, not final optical approval or release QA.
