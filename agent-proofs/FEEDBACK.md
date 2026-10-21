# Design review and feedback

This is the persistent record for Eli's propose → feedback → revise loop.
The [Virtua Design Review entry point](README.md) connects this record to the
current handoff, drawing rules, live proof, agent procedures and recovery paths.
Start here before a design-review batch. The design authority remains
[DESIGN.md](../DESIGN.md); color permissions remain in
[AGENTS.md](../AGENTS.md). Build/proof mechanics live in
[Build and QA](../documentation/qa.md#chat-proof-workflow), and release blockers remain in
[Google Fonts onboarding](../documentation/google-fonts/README.md). This record does not
replace those documents or establish release readiness.

## Confirmed preferences

Only explicit user feedback belongs in this table. Agent findings and proposed
rules belong in an individual review until Eli confirms them. Do not turn one
glyph-specific correction into a family-wide rule without evidence and agreement.

| ID | Confirmed preference | Scope and source |
| --- | --- | --- |
| P001 | Two base colors only: light gray `#dedede` and dark gray `#444444`; allow swapping paper/ink for light or dark review. No red accents. | Eli, 2026-10-19 specimen feedback. Supersedes the earlier colored-overlay preference for standard specimens. Existing v2 images remain historical evidence; the DesignBot workflow keeps both polarities. |
| P002 | Begin with small edits and tight feedback loops; grow batch size as the documented design knowledge improves. | Work method. Eli, 2026-10-19: “start off with ... smaller edits and corrections” and “pick up speed and do larger chunks of work as we go”. This does not pre-authorize broader drawing edits. |
| P003 | Record feedback in the Virtua repository so later sessions reuse preferences, references, and working methods. | Work method. Eli, 2026-10-19: “documentation and reference and skills ... improve with every feedback”. |
| P004 | Aim for the finish and consistency of Rubik and Google Fonts release quality. | Quality goal. Eli, 2026-10-19. This is not permission to copy Rubik's outlines or replace Virtua's visual identity. |
| P005 | Use Virtua’s green core Latin a–z/A–Z drawings as weight and drawing-style references for the new Hebrew work. | Eli, 2026-10-19, HEB-001 candidate authorization. Measure live sources; external fonts supply script comparison, not weight targets. |
| P006 | The dalet/resh weight is accepted provisionally; Hebrew/Arabic weight relative to Latin lowercase and capitals remains OPEN. | Eli, 2026-10-19 application approval. Do not promote the pair’s numbers into a final script-wide contract. |
| P007 | Specimens need clearer hierarchy, a strict modular grid and more readable comparisons, inspired by Müller-Brockmann. | Eli, 2026-10-19. Eli subsequently confirmed this layout is more readable and clear; retain its hierarchy while revising color, casing and rendering. |
| P008 | Use title case in specimen headings and labels; avoid all-caps furniture. Literal glyph-test alphabets retain their intended case. | Eli, 2026-10-19: “I like to do title case instead of all caps.” |
| P009 | Discuss and evaluate DesignBot Rust scripts as the canonical specimen renderer before fixing the reported label artifacts. | Eli, 2026-10-19. Initial discussion request; superseded by P011 after the diagnostic and hinting investigation. |
| P010 | Use Virtua Grotesk for specimen headings and captions, beginning with the Regular instance. | Eli, 2026-10-19: “can we maybe just use Virtua Grotesk for this instead of Helvetica?” Supersedes the neutral external-caption-font choice. |
| P011 | Use DesignBot Rust scripts as the standard comparison-sheet workflow, with Virtua labels, title case and both gray polarities. Tighten large headlines without altering sample spacing. | Eli, 2026-10-19: “Looks good, let’s port the three comparison sheets ... record this as our standard workflow” and “track the text in a bit tighter”. The first implementation uses −0.02 em at 64 px; this numeric setting is an adjustable agent choice. |
| P012 | Reduce repeated slash separators and use alignment, spacing and typographic hierarchy to organize specimens. Keep the presentation clean and restrained. | Eli, 2026-10-19: “we are overusing / here”; asked for another Swiss editorial layout pass. Subsequently approved: “Looks good, let’s keep this as the standard.” |
| P013 | Finish Hebrew in small glyph groups, then review long mixed Latin–Hebrew text across sizes beside Rubik and Noto; follow with Arabic using the same process. Record recurring weight and spacing corrections. | Eli, 2026-10-19. The long-text specimen will be designed with Eli after the alphabet pass. This is a sequence and workflow preference, not blanket drawing approval. |
| P014 | Hebrew and Arabic must share the live green Virtua construction: consistent straight chamfers and smooth curves. Rubik and Noto are script references, not the drawing-style authority. | Eli, 2026-10-19 HEB-002 candidate request and outline screenshot; recorded in DESIGN.md. Weight remains provisional under P006. |
| P015 | New machine drawings default to the 8-unit structural lattice; track power-of-two measurement decompositions and preserve draft-to-green corrections for training. Mathematical compliance does not assign a grade. | Eli, 2026-10-19, referring to the Virtua article. DESIGN.md distinguishes point lattice from descriptive popcount. HEB-002 v2 is the first candidate checked with the explicit draft gate. |
| P016 | Keep labels close to the samples they identify; use a coherent Swiss editorial grid and purposeful negative space. Earlier specimen approval does not freeze a layout with these problems. | Eli, 2026-10-19 after HEB-002 application approval: labels are too far away and the whole layout needs care. The revised rail-and-column layout is an agent proposal awaiting review. |
| P017 | Use the supplied editorial/poster references for clear modular blocks, shared alignments, consistent gutters, close captions and deliberate empty space. Make the underlying grid toggleable. | Eli, 2026-10-19, eight screenshot references. Existing two-gray and title-case preferences remain; reference colors and all-caps are not new instructions. |
| P018 | Use live font rendering for interactive web review; do not shrink specimen images into the panel. Keep crisp, readable labels, adjustable sizes and weights, references, and before/after switching. | Eli, 2026-10-19: “why don’t we just render everything crisp and clear in a web view … we don’t have to do the images.” Supersedes image-first presentation for interactive reviews. Existing DesignBot proofs remain historical evidence; Eli then confirmed the live web proof as the default and requested an intensive UI/UX pass before resuming Hebrew; the implementation is still being refined. |

| P019 | The live web proof’s font-name headline and study headline share the same size and style. Dark mode uses a neutral gray matching the supplied browser address bar, interpreted from screenshot pixels as `#282828`, with `#dedede` ink. | Eli, 2026-10-19, 14:57:27 and 15:00:31 screenshots. The darker paper supersedes P001’s `#444444` dark background for the live web proof; historical fixed exports retain their recorded palette. |
| P020 | Simplify the proof interface to core comparison information. State settings once and organize controls through alignment; move supporting review metadata into Details. | Eli, 2026-10-19: “simplify this and just show the core important information in a clean way”. Removing preset rows and duplicate summaries is the current implementation choice, subject to feedback. |

| P021 | Fit live proof samples responsively to the available space by default. Use one shared actual em size across the comparison and display it; retain an explicit fixed-size inspection mode. | Eli, 2026-10-19, 15:15:45 screenshot: “there is a lot of clipping … make this responsive to fit the available space”. This supersedes default horizontal scrolling for live comparisons; per-font fitting remains inappropriate. |

| P022 | Use the side margin as the live proof’s spacing unit U. Derive gaps from U and its halves/multiples throughout; balance the visible space around type and sliders rather than accumulating arbitrary paddings and font line-box whitespace. | Eli, 2026-10-19, annotated 15:23:23 screenshot. Current responsive U values and component mappings are implementation choices documented in the web-proof guide. The shared sample baseline and equal em scale remain required. |

| P023 | Include substantial running text during glyph review, because isolated forms alone do not reveal reading behavior. Use identical Hebrew and mixed Latin–Hebrew passages in Virtua before/applied, Rubik and Noto at explicit reading sizes. | Eli, 2026-10-19, 15:34:30 reference. Pulls the first running-text prototype forward into the current UI pass rather than waiting until the alphabet pass is finished. |
| P024 | Identify review glyphs with their Hebrew form, Latin name and Unicode together, including the study heading and individual selector entries. | Eli, 2026-10-19, 15:37:46 and 15:37:56 references; example ת (Tav). Current hierarchy places the code point beneath the heading’s form/name pair. |

| P025 | Name the live proof modes Compare, Toggle, Size and Text. Separate the mode bar from the glyph identities with a horizontal rule above it. | Eli, 2026-10-19, 15:52:11 screenshot. The bar uses U/2 inset above/below its labels; internal mode identifiers remain stable. |

| P026 | Inset the masthead rule to the same page margins as other rules. Keep the Text control area free of explanatory reflow copy and avoid its extra vertical spacing; place rendering information in Review Details. | Eli, 2026-10-19, 16:18:46 screenshot. The slider-to-caption interval returns to U, matching the interval above its track. |
| P027 | Use one shared text size for navigation, primary control labels, selected values and font captions. Combine family and review role inline with a center dot; remove the Applied underline and the visible px suffix from Size. | Eli, 2026-10-19, 16:41:41 screenshot: fewer different sizes and a simpler Swiss modernist hierarchy. Live browser UI; supersedes stacked name/role captions here. The shared UI size is currently 14 CSS px; specimen sizes remain independent. |
| P028 | Refine dropdowns to fit the proof's restrained grid and two-gray design; reduce oversized checkbox marks and give them breathing room inside their boxes. | Eli, 2026-10-19, 16:46:35 screenshot. The custom menu, thin ticks and 12 CSS px boxes are implementation choices awaiting visual feedback, not a final approved component design. |
| P029 | Smaller checkbox marks means more clearance inside the box, not thinner strokes. Unicode identities use the same UI text size as navigation; avoid additional small-label sizes throughout the interface. | Eli, 2026-10-19, 16:52:20 screenshot. Corrects the thin-tick interpretation of P028 and extends P027 to Unicode labels. Tick dimensions and stroke below are implementation choices awaiting review. |
| P030 | Default Compare fitting should fill the available column width so small drawing details are visible; widen and enlarge the samples when References is off. | Eli, 2026-10-19, 16:58:19 and 16:58:50 screenshots. Removes the earlier fixed-size cap on automatic fitting. Equal comparison scale and shared baselines remain required; fixed-size inspection stays separate. |

| P031 | Light-mode paper should be closer to mid-tone gray; the previous background was too bright. | Eli, 2026-10-19. Live proof paper now proposed as `#a8a8a8`, retaining `#444444` ink. Supersedes P001’s light paper for this interface; dark mode and historical exports retain their palettes. |

| P032 | Give light and dark modes independent palettes. Darken the light-mode charcoal toward the surrounding app area, and keep all colors pure neutral gray with equal RGB channels. | Eli, 2026-10-19, 17:05:32 screenshot. Proposed light ink and dark paper are `#181818`, approximating sampled surrounding values 23–25; light paper stays `#a8a8a8`, dark ink `#dedede`. Supersedes the corresponding live-proof values in P019/P031; exact choices remain reviewable. |

| P033 | Light-mode ink should sit halfway between the earlier charcoal and P032’s darker value. | Eli, 2026-10-19. `#2e2e2e` is the RGB-channel midpoint of `#444444` and `#181818`. Supersedes only P032’s light ink; other theme colors stay unchanged. |
| P034 | Compare is satisfactory for now; focus the next UI pass on Toggle's broken margins and spacing. | Eli, 2026-10-19, 17:17:24 attachment name (file unavailable; live view inspected). Moving revision controls into Sample's slider row and using three equal proof columns is the current proposal, not yet approved. |
| P035 | Stretch Before/Applied across the Sample column with equal halves. Keep a visible “Press B to toggle” hint in the mode bar between Text and References. | Eli, 2026-10-19, follow-up to Toggle spacing. The hint is specific to Toggle; it wraps below the tabs in narrow layouts. |
| P036 | All text in the horizontal mode bar shares one size and baseline, including References and the keyboard hint. | Eli, 2026-10-19, 17:28:30 screenshot. Use actual baseline alignment and shared UI type, not independent vertical offsets. |
| P037 | Rename Size to Waterfall. Label the fonts once at the top, start with the largest common size fitting the available width, and descend to small samples without repeated headings or pixel-size labels. Simplify the broken top controls. | Eli, 2026-10-19, 17:29:24 screenshot. Supersedes P025's Size tab name and the earlier ascending size rows. Eight logarithmic steps ending at 16 px and two equal control columns are current implementation choices for review. |

| P038 | Simplify comparison captions to Before, Applied, Rubik and Noto Sans Hebrew. Omit repeated Virtua family names and redundant Reference suffixes to reduce text and wrapping. | Eli, 2026-10-19, 17:38:13 screenshot. Supersedes P027’s combined family/role captions in the live proof; full identities stay in Review Details. |

| P039 | Use a filled, inverted active mode tab, similar to Before/Applied, instead of the underline that developed a gap above the rule. | Eli, 2026-10-19, 17:45:48 screenshot. Retain shared text size and baseline across the bar. |

| P040 | Changing selected-mode styling must preserve the established text grid, including Compare flush with the left margin. Verify existing alignments across modes before considering a UI change complete. | Eli, 2026-10-19, correction after P039. Layout padding shifted labels; selection fill now paints around the text without adding layout width. |
| P041 | Make Your Text a coherent, usable editor section: separate it from the sliders with a margin-aligned rule, use consistent thin rules/focus treatment, remove the resize handle and preserve the established margins. | Eli, 2026-10-19, 17:54:51 screenshot. Auto-growing height with bounded scrolling and U-based insets is the current implementation for review. |

| P042 | Replace inverted active-mode fills with a thick underline at the bottom rule. Keep the indicator within the tab text width and preserve the page margin. | Eli, 2026-10-19, 19:12:10 screenshot: the inverse selection breaks left containment. Supersedes P039 and the fill implementation described in P040; P040's alignment requirement remains. |

Confirmed 2026-10-19, 19:47: Eli requests divider strokes twice as thick,
preferably with rounded ends, and compact control-section vertical spacing
comparable to the mode bar (P043). This supersedes the 1px rules and roomy
slider-band spacing. Existing page margins and shared UI type remain.

## The loop

1. Read confirmed preferences, the latest open review, relevant design contracts,
   current source colors, and actual dirty state. Check source/binary freshness.
2. Choose a small named scope. Render current Virtua beside relevant references,
   then distinguish measurements, visual observations, and proposed corrections.
   State the question the candidate would test. No candidate column until it exists.
3. Record Eli's response **before continuing the next edit**: retain the wording
   or a faithful short quotation, your interpretation, exact scope/masters, and
   whether it approves preparation, application, rejects, or requests revision.
   If ambiguous, preserve the uncertainty; do not invent approval.
4. Make only the authorized candidate in scratch sources. Capture a reversible
   before state and source hashes; render candidate and baseline at equal scale.
   Check interpolation, inherited forms, marks, and reading-size texture.
5. Record the outcome: accepted/revised/rejected, which sources actually changed,
   tests and visual review, unresolved issues, and the next bounded question.
   Passing QA never assigns green/purple; final grading stays with Eli.
6. Promote confirmed reusable lessons to the right owner: this table for workflow
   preferences; DESIGN.md for agreed design rules; the relevant glyph worklog for
   local decisions; a skill/script for a demonstrated repeatable procedure. Link
   back to the review evidence. Keep superseded decisions with their replacement
   IDs so another session does not resurrect a rejected approach.

A correction record should contain: date, review ID, user's feedback, interpretation,
exact glyph/master scope, before/candidate identities, proposal state, application
state, observed result, rule scope, destination, and unresolved questions. Use the
current review's feedback table; do not scatter duplicate logs across files.
For image-sheet/tracing corrections, also update the canonical anchor-sheet
LESSONS.md as its skill requires, linking to the same review.

Increasing batch size is a deliberate decision after successful related loops,
not an automatic reward for passing tests. No model training or hidden learning
is implied: this system improves through explicit repository records and tools.

## Reviews

| Review | Scope | Current state |
| --- | --- | --- |
| [HEB-001](cases/hebrew-001/README.md) | Dalet/resh in both masters; specimen redesign | Candidate v1 applied; weight provisional; refined DesignBot layout approved |
| [HEB-002](cases/hebrew-002/README.md) | He, het and tav in both masters | Candidate v2 applied; UI pass ready to move on; next font scope to be selected |

| [HEB-003](cases/hebrew-003/README.md) | Bet, Kaf and Final Kaf in both masters | Candidate v2 applied; protected marked forms remain follow-up |

| [HEB-004](cases/hebrew-004/README.md) | Pe and Final Pe in both masters | Candidate v1 approved and applied; protected marked forms remain follow-up |

| [HEB-005](cases/hebrew-005/README.md) | Mem, Final Mem and Samekh in both masters | V5 approved and applied to both masters; v4 rejected |

| [HEB-006](cases/hebrew-006/README.md) | Yod, Vav, Zayin, Nun and Final Nun in both masters | V2 installed for Eli’s hand corrections; not final approval |

## Next phases

**Current phase: resume font review through Virtua Design Review.** On 2026-10-19,
after the custom-text editor pass, Eli said the system was better and ready to
move on. HEB-002 is applied. Read the [central handoff](README.md) and choose
the next bounded scope; this does not grant blanket approval for new drawings.
The [web-proof guide](app/README.md) owns UI implementation.

After the proofing interface is ready, work through the Hebrew alphabet and
final forms in related, reviewable groups. Recheck related marked forms before
calling a family complete; later grouping remains adaptable to feedback.

Eli subsequently requested running text during the current UI pass (P023), so
the first Reading view is available now. Continue refining it with identical
Hebrew and mixed Latin–Hebrew passages in Virtua, Rubik and Noto at reading
sizes and weights. Keep paragraph width, leading, scale and rendering policy explicit.
Include script transitions, Latin capitals/lowercase, numbers and punctuation.
Verify bidirectional order and actual font selection before diagnosing spacing;
never let silent fallback masquerade as a font comparison. Distinguish natural
reflow for reading texture from matched-line comparisons for local spacing.
The initial implementation uses natural paragraph reflow; matched-line comparisons
and further reading layouts remain open design questions.

For each accepted correction, retain the passage, size, weight, affected glyphs
or pairs, before/after evidence, Eli’s response and scope of the lesson. Repeated
confirmed patterns can then become rules or skill guidance. Once Hebrew reaches
a good state, repeat the glyph and running-text process for Arabic, including
joining forms and mixed-script behavior.

## Evidence retention

Keep concise review notes, recipes, font/source hashes, and the key displayed
PNGs here under version control. Full builds, raw manifests, temporary variations,
and scratch UFO backups remain in ignored `out/qa/`. External reference fonts
remain cached locally; record origin, license, and exact binary hash. A missing
cache is not permission to silently substitute a different version. Rebuild or
fetch the recorded reference, verify it, and label any intentional update.

P044 (2026-10-19): Open proofs in dark mode by default, including the initial
HTML paint. The Dark checkbox still allows switching to the neutral light palette.

HEB-005 Samekh (2026-10-19): Eli finds v3 too organic/humanist and requests a
more geometric neo-grotesk construction. Revise Samekh only; preserve the v3
trial and the unchanged Mem/Final Mem candidates for comparison. Not applied.

HEB-005 correction (2026-10-19): v4 rejected as a different, worse design.
“More geometric” meant slight contour cleanup of v3, with Rubik as a reference,
not a rectangular replacement. Restore v3 and make only restrained handle edits.
Preserve skeleton, on-curve points and metrics; do not generalize feedback into
an unrequested redesign.

HEB-005 approval (2026-10-19): Eli approved Mem, Final Mem and refined Samekh
v5 for application to both masters. Exact reviewed sources applied and rebuilt;
see `cases/hebrew-005/application-v5.json`.

HEB-006 Zayin (2026-10-20): Eli finds the angled v1 construction overcomplicated
and requests a simpler form closer to Rubik. Trial a level head with a clean
stem connection, retaining Virtua chamfers. Other four candidates unchanged.

HEB-006 hand-edit baseline (2026-10-20): Eli requested applying the current
drawings, committing and pushing them so he can edit on top. Preserve v2 as
the comparison baseline; do not treat installation as final drawing approval.

HEB-006 manual correction (2026-10-20): Eli saved a local Regular Zayin neck
refinement: tangent right-hand arrival into the flat head underside, and an
8-unit chamfer before the left curve. Preserve the saved outline. The exact
before/after geometry and limits of this glyph-specific lesson are recorded in
[cases/hebrew-006/README.md](cases/hebrew-006/README.md#elis-saved-regular-zayin-correction--2026-10-20).
Bold adaptation remains open; this does not approve a family-wide construction rule.

## Manual correction library

This index routes agents to exact examples; case files own the evidence.
Read the relevant pair before drawing, and record whether the next candidate
actually benefited from it. Keep observations, proposed generalizations, and
Eli-confirmed reusable rules distinct. A saved source is evidence of what Eli
drew, not permission to reproduce every detail across the family.

| Example | Find by | Scope and evidence | Reuse status |
| --- | --- | --- | --- |
| HEB-005 Samekh v3 → v5 | bowl, curve tension, cleanup, preserve skeleton | [Case](cases/hebrew-005/README.md): restrained handles, rejected rectangular redesign retained | Approved in both masters; exact geometry remains glyph-specific |
| HEB-006 correction 01 | Zayin, neck, head/stem, tangent, chamfer, asymmetric junction | [Case and exact saved Regular](cases/hebrew-006/README.md#elis-saved-regular-zayin-correction--2026-10-20): committed v2 → Eli’s hand edit | V3 transferred structure, but Eli corrected its tall right turn; see correction 02 |
| HEB-006 correction 02 | Zayin Bold, machined, geometric turn, square extent, equal handles, weight adaptation | [Case](cases/hebrew-006/README.md#manual-correction-02--bold-geometric-turn-2026-10-20): v3 → saved Bold; only three points changed | Human correction recorded; next reuse not yet tested |
| HEB-007 correction 01 | Gimel, foot, tangent continuation, terminal landings, inner shelf, chamfer landing | [Case](cases/hebrew-007/README.md#manual-correction-01--regular-gimel-2026-10-20): exact saved Regular and v3 source; measured join angles | V4 Bold transfer accepted as good enough for continuation; no final grading |
| HEB-008 correction 01 | Final Tsadi, quarter-turn, equal handles, tangent landing, diagonal terminal, junction cut | [Case and measured pair](cases/hebrew-008/README.md#manual-correction-01--regular-final-tsadi) | Human Regular preserved; v7 transfer accepted as better and requested for commit, without grading |

For each new manual correction, preserve the starting revision/source and saved
GLIF, identify the actual geometric/spacing changes separately from editor
rewrites, and record Eli’s explanation when available. Infer intent cautiously.
Retain the proof settings and result of subsequent reuse. Retrieve only the
examples relevant to the next glyph rather than loading the entire archive.

As examples accumulate, consolidate recurring confirmed patterns into DESIGN.md
and concise skill instructions, with links to examples and exceptions. Keep
one-off measurements local. Check proposed rules against earlier accepted and
rejected forms before broad use. This is explicit, portable repository context;
it does not retrain a model or guarantee improvement merely from example count.

Confirmed 2026-10-20 — machined construction: Eli explicitly rejects the sloppy,
humanist quality of Bold Zayin v3 and asks for clean neo-modernist forms with
mathematical precision. Correction 02 shows a 56×56 right turn with equal
40-unit handles replacing a 56×104 transition. Grid compliance and tangency
were already present in the rejected candidate, so neither is sufficient to
establish the requested character. Exact dimensions remain local; see DESIGN.md
for the stated style direction and the case for measured evidence.

## Standing drawing authorization — 2026-10-20

Eli authorized continuing Hebrew development directly in the active Regular and
Bold UFOs, then Arabic after Hebrew. Do not ask for per-batch application approval.
Preserve a before snapshot, check source colors and current file hashes, make
bounded compatible edits, rebuild and show the comparison with Rubik. Active
sources are the working drawings visible in Runebender; application does not
mean final visual approval, green grading, or release readiness. Preserve manual
corrections and unrelated edits. Keep recording exact correction pairs and
promote measured lessons into DESIGN.md and the shared skills.

HEB-007 working batch (2026-10-20): Gimel, Lamed and Qof are written to both
active masters under standing authorization. The first rendered pass caught
a Bold Qof stroke collision and an uneven Bold Gimel foot; v2 corrects these.
This is agent verification, not a new human-approved rule. See the case for
exact source snapshots and remaining reader/marked-form review.

HEB-007 Gimel direction trial (2026-10-20): Eli requested trying a left-sweeping
foot like Rubik/Noto instead of the separate downward left leg, in both masters.
V3 implements this while preserving the head, main-stem approach and metrics.
Record as a requested alternative pending feedback, not a universal design rule.

HEB-007 clarification (2026-10-20): Eli explicitly confirmed the 8-unit flat
between Gimel’s lower foot curve and main stem is intentional: keep it.
Do not smooth this shelf away. This confirms the local construction detail,
not the entire Bold v4 trial or a rule for unrelated glyphs.

HEB-008 revision v6 (2026-10-20): Eli rejects the current Shin and Final Tsadi
forms and requests constructions closer to Rubik. This specifically authorizes
revising those two letters in both masters; it is not a generic instruction to
replace other Hebrew designs. See the [case](cases/hebrew-008/README.md#revision-v6--shin-and-final-tsadi).


HEB-009 exception (2026-10-20): Eli explicitly approved rebuilding the 29
presentation forms named in [HEB-009](cases/hebrew-009/README.md) in both masters
from current bases and existing marks. Preserve standalone mark drawings and
all grades. This closes the named purple-protection exception only; it is not
blanket permission to revise protected marks or infer human grading.
