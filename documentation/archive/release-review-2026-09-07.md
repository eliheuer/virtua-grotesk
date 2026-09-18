# Virtua Grotesk: Google Fonts release checklist

Reviewed 2026-09-07 against source commit `3fcaaf2` (`update drawings`).
This is the project-specific execution checklist requested by Eli. Reusable
onboarding policy remains in `.agents/google-fonts-onboarding-checklists.md`;
`DESIGN.md` and the human design worklog govern design decisions. Historical
readiness claims are not evidence that a current checkbox is complete.

## Review verdict and evidence

**Not ready to submit.** The current sources build, but exported blank visible
glyphs, unreviewed masters, incomplete QA, stale proofs, and a release workflow
that tolerates QA failure remain. Fix the evidence pipeline first, then use it
to finish small glyph batches. Packaging alone will not make this font ready.

Verified in this review:

- [x] Identified the actual font project: Virtua Grotesk, not runebender-core.
- [x] Working tree was clean before review; source commit is recorded above.
- [x] `make build` succeeded: one wght 400–700 variable TTF and four static TTFs.
- [x] Ran Fontspector 1.6.0 (`42bfc355`) on all five new TTFs, without excludes,
  with `--skip-network`: **6 FAIL, 58 WARN, 491 PASS, 39 INFO, 310 SKIP** result
  severities. These are reported result counts, not unique glyph counts.
- [x] Classified the six failures: `contour_count` on five binaries includes
  real blank visible glyphs; the sixth is an upstream directory-name mismatch
  (`ttf` versus `virtuagrotesk`), to recheck in downstream package context.
- [x] Confirmed U+2010 HYPHEN, U+0591, U+05C0 and U+FB1D have zero contours in
  the newly built variable font. Many additional Hebrew source entries are blank.
- [x] Counted 863 glyph entries in each master; built VF has 858 glyphs and 647
  cmap entries. These counts include work in progress, not promised coverage.
- [x] Confirmed GPOS includes kern/mark/mkmk, and GSUB includes Arabic forms,
  locl, rlig, rclt and tnum. Table presence does not prove correct shaping.
- [x] Ran `scripts/preflight.py`: fails because
  `documentation/proofs/print-spacing-specimen.pdf` is missing.
- [x] Reviewed the existing 24-page landscape Letter proof as a contact sheet,
  with closer inspection of diacritics (p9) and joining forms (p14).
  Its page date is 2026-08-14: it is historical evidence, not this build's proof.
- [x] Rendered a fresh Regular diacritic comparison against the locally available
  Rubik. It is useful but needs normalized scale, more weights and more contexts.

Evidence is in [`documentation/release-audit/`](release-audit-2026-09-07/):
`build.log`, `fontspector.log`, `fontspector-findings.json`, `font-sha256.json`,
`diacritics-vs-rubik.png`, and `historical-proof-contact.png`. The JSON retains
full offending-glyph metadata where supplied. This audit did not run network
checks, package QA, a clean-machine install, exhaustive visual review, or a
physical print review. No source glyphs were edited or graded.

## P0 — Make readiness truthful and repeatable

- [ ] **R01: reconcile entrypoints.** Update AGENTS.md, readiness.md, development
  QA checklist and Makefile help to agree with actual targets. Remove stale
  statements that metadata is absent, all Latin is finished, zero excludes
  guarantees release, or Rubik/diffenator appearance guarantees GF acceptance.
  Keep one project backlog, one reusable policy, one design decision log.
- [ ] **R02: repair preflight.** Decide whether the main print proof replaces the
  old spacing specimen or implement the missing artifact. `make specimen`
  currently deliberately exits 1; preflight requires its obsolete filename but
  does not build it. Acceptance: documented clean-checkout command succeeds and
  fails on missing, stale, wrong-font or incomplete artifacts.
- [ ] **R03: separate development and release gates.** Retain an explicit debt
  baseline for daily work, but add an unrestricted package-context release run.
  Do not equate a suppressed warning with a reviewed exception. Record each
  exception's check, affected glyphs, rationale, owner, evidence and review date.
  Report SKIP and unavailable checks. No silent new excludes or dropped subsets.
- [ ] **R04: enforce exit semantics.** `--loglevel warn` only filters logging;
  Fontspector defaults to exiting on FAIL. The script's claim that every printed
  WARN is a regression is not enforced. Use an explicit severity policy or a
  structured baseline diff; test with a deliberate warning and failure fixture.
- [ ] **R05: block release on failed QA.** CI currently has `continue-on-error`
  for QA and its tag job can publish regardless. Require release QA and reviewed
  artifacts before publishing. Keep diagnostic uploads available after failure.
  Never push a tag merely to test this publishing workflow.
- [ ] **R06: refresh tooling deliberately.** Local Fontspector is 1.6.0 from April;
  record/pin the version used for the release, compare current GF tooling, and
  regenerate the baseline after any upgrade. Pin designbot revision and CI setup
  actions; its current install is unpinned and cache key is a fixed `v1`.
- [ ] **R07: reproduce from a fresh worktree.** Bootstrap Python, fontspector,
  designbot and any browser dependencies without a pre-existing user venv or
  sibling checkout. Preserve requirements pins and document lock regeneration.
  Test the supported macOS/Linux path. Compare repeated build hashes, accounting
  explicitly for timestamps; preserve build command, logs and source revision.
- [ ] **R08: strengthen CI artifacts and permissions.** Replace `write-all` with
  per-job minimum permissions; include reports, QA JSON, proof manifest and
  checksums with binaries. Inspect release ZIP contents and license inclusion;
  avoid an optional failed article copy producing an apparently complete bundle.

## P1 — Inventory scope and repair actual missing drawings

- [ ] **G01: record first-release scope.** Existing plans say Latin + Arabic;
  sources now also include Hebrew. Inventory actual supported scripts and
  languages. Eli chooses whether Hebrew ships now or stays development-only.
  Do not silently remove intended support or claim blank placeholders as coverage.
  An italic is optional scope, not an automatic GF prerequisite.
- [ ] **G02: generate a source-to-binary map.** Follow each UFO's contents.plist,
  designspace rules, skip-export entries, components and production naming.
  Explain the 863-source/858-built difference. Detect dangling or cyclic
  components, duplicate Unicode assignments and encoded alternates.
- [ ] **G03: repair blank visible glyphs.** Begin with `uni2010` in both masters,
  checking its design relationship to hyphen. Queue Hebrew `uni05BD`, `uni05BF`,
  `uni05C0`, `uni05C3`, `uni05C6`, presentation forms and the broader blank set.
  Read glyph colors before editing; preserve legitimate spaces/joiners/control
  characters. Acceptance: no unexplained blank visible cmap entry in any output.
- [ ] **G04: regenerate glyphset coverage.** Verify current GF Latin Core and
  every selected script set using pinned glyphsets; save missing codepoints.
  Check exported binaries, not only source presence. Report coverage separately
  from language shaping and human approval. Refresh the old 319-codepoint claim.
- [ ] **G05: regenerate the grading inventory.** The old 690-glyph scoreboard and
  246-blue statements need refreshing. Current exact red color `1,0.29,0.24,1`
  occurs on 34 Regular and 246 Bold glyphs, but several other color values exist.
  Resolve the authoritative palette rather than guessing color meanings. Track
  green, draft, red, uncolored and dependency-blocked status in both masters.
- [ ] **G06: classify each outline finding.** Start from saved Fontspector JSON:
  contour counts, direction, jagged/collinear/semi-vertical segments, overlaps,
  GDEF marks, language shaping and suspicious sidebearings. Distinguish actual
  missing ink from contour heuristics. Do not redraw a valid design to match a
  statistical contour count. Map every finding to source glyph and proof crop.
- [ ] **G07: respect authored shapes.** Read design-pass-worklog before Latin
  edits. Keep green glyphs and unresolved human design choices unchanged; make
  reviewable proposals for them. Preserve chamfers, curve continuity and weight
  intent. Do not blanket-snap off-grid points or normalize winding without
  respecting UFO versus TrueType conventions and composite behavior.

## P1 — Diacritics and shaping

- [ ] **D01: replace unsafe blanket accent repair.** `fix_accent_offsets.py`
  assumes `name.glif`, regexes point bounds, ignores component transforms and
  protected colors, and writes immediately. Use UFO-aware component/anchor
  resolution, true curve bounds, dry-run diffs, explicit glyph selection and
  transactional paired-master writes. Test filename mappings, nested components,
  optical exceptions, rollback and a second run producing no changes.
- [ ] **D02: inspect all mark classes.** Audit anchors and composites across
  capitals/lowercase, narrow/wide/round bases, dotless i/j, acute/grave, tilde,
  caron, breve, macron, circumflex, ring, dieresis and double acute. Include
  ogonek, cedilla and comma below; they do not all belong at a geometric center.
  Preserve language-specific construction, e.g. L/d/l/t carons and Romanian
  comma versus cedilla. Compare mark weight, gap, optical centering and clearance.
- [ ] **D03: NFC/NFD equivalence.** Shape paired precomposed/decomposed strings;
  compare glyphs, positions and rendered ink with explicit script/language.
  Test stacked marks, mark-to-mark, dot removal and combining class order.
  Cover every language claimed by the selected release scope.
- [ ] **D04: repair GDEF/GPOS semantics.** Investigate `GDEF_mark_chars` and
  `base_has_width` warnings by codepoint and shaping role. Check combining mark
  advance widths and attachment coverage; a spacing accent is not the same
  semantic object as a combining mark. Recheck every generated instance.
- [ ] **D05: finish Arabic in context.** Proof isolated/initial/medial/final
  forms; joining and nonjoining boundaries; lam-alef; dots, hamza and harakat;
  mark stacks; ZWJ/ZWNJ; Arabic/Persian/Urdu distinctions only where claimed;
  mixed RTL/LTR text, punctuation and digits. Check no .notdef or fallback.
  Verify actual harfbuzz output, not just feature declarations.
- [ ] **D06: inspect Arabic weight behavior.** Review historical reduced-offset
  Bold cases (including reh tails) against current sources. Investigate
  `uni066F.fina` sidebearing/advance variation in the current QA JSON at wght
  near 500, 600 and 700. Large LTR sidebearing metrics alone are not a fix order.
- [ ] **D07: give Hebrew an explicit QA path if shipping.** Separate letters,
  niqqud, cantillation, punctuation and presentation forms. Add Hebrew shaping
  and mark-stack proofs and a qualified reader's review. Existing Arabic proof
  coverage cannot certify Hebrew. Keep documented development placeholders out
  of release claims; scope changes need the maintainer decision from G01.

## P1 — Interpolation, spacing and binary engineering

- [ ] **V01: verify compatibility deeply.** Check contours, point types/order,
  components/transforms and anchors across both masters; run interpolation
  diagnostics and inspect for twisting, collapsing counters and self-crossings.
  Successful compilation alone is insufficient.
- [ ] **V02: sample the whole axis.** Render 400, 450, 500, 550, 600, 650, 700,
  plus just below/at/above every actual designspace substitution threshold.
  Compare statics to equivalent VF instances, including rclt bracket alternates
  such as a.bold. Track dependent accented forms through substitutions.
- [ ] **V03: finish spacing before pair tweaks.** Review O/H/n/o control strings,
  all letters and figures, punctuation, quotes, brackets, currency and accents.
  Check groups and pairs for parity, missing members, duplicates and exceptions.
  Compare kern on/off; inspect real paragraphs at reading and display sizes.
- [ ] **V04: validate metrics.** Inspect hhea/typo/win metrics and USE_TYPO_METRICS,
  line gaps, tallest/deepest marks and Arabic/Hebrew stacks over the full axis.
  Check clipping in browsers and installed apps. Reconcile AGENTS' ascender 832
  with DESIGN's 768 rather than silently changing the design contract.
- [ ] **V05: review binary metadata.** Validate name IDs/style links/PostScript
  names, copyright and OFL strings, version, fsType, vendor ID, fvar instances,
  STAT, avar and meta script tags against intended scope and current GF tooling.
  Inspect post-build `fix_gf_metadata.py` effects and keep one authoritative
  source for values. Confirm variable default Regular=400 and four named styles.
- [ ] **V06: compare rasterization.** Inspect small sizes on browser and native
  renderers; evaluate current autohintTTF=false intentionally. Check OTS/browser
  loading, outlines after static overlap removal, and feature behavior. Do not
  enable hinting solely to quiet a check without comparing the result.

## P1 — Improve print and screen proofs

- [ ] **P01: keep the useful existing page plan.** Current proof covers character
  set, waterfall, reading sizes, leading/tracking, spacing, figures, diacritics,
  kerning, weights/interpolation and extensive Arabic. Preserve that breadth.
- [ ] **P02: make proof provenance visible.** Every PDF/HTML/crop records source
  commit plus dirty-source digest, font hash, renderer version, instance, size,
  feature flags, script/language and corpus revision. Include a manifest linking
  pages/crops to glyph IDs and source names. Detect font fallback explicitly.
- [ ] **P03: add a practical print review layer.** Offer Letter/A4 layouts with
  safe printer margins, page numbers, section index, room for pencil notes,
  legible labels and a 100%-scale ruler. Use black ink on white for diagnosis;
  retain vector outlines. Add 8–14pt reading text and 24–72pt diagnostics.
  Proof actual printouts at 100%; raster inspection cannot assess paper/ink.
- [ ] **P04: expand the diacritic page.** The historical p9 is mostly small
  isolated rows with ample spare space. Add large base+mark detail, baseline/
  x-height/cap guides, below marks, NFC/NFD pairs and word contexts, across all
  weights. Keep dense coverage sheets separate from readable diagnostic pages.
- [ ] **P05: make comparisons fair.** Extend compare_diacritics beyond three
  Regular rows and a hard-coded absolute Rubik path. Support font arguments,
  reference hashes/licenses, no-fallback coverage checks, identical corpus,
  equal-point-size AND equal-x-height/cap-height views, and selected comparable
  weights. Same wght number does not mean same darkness between families.
  The fresh image shows Virtua taller/heavier at the same size, so it cannot
  alone justify thinning marks or copying Rubik offsets.
- [ ] **P06: use script-appropriate references.** Rubik can inform Latin
  comparison; verify each reference binary's actual cmap before Arabic/Hebrew
  comparisons. Add licensed, verified script references when needed. Reference
  fonts are quality/context controls, not outlines to copy or a replacement for
  Virtua's chamfered geometric identity.
- [ ] **P07: contextualize Arabic diagnostics.** Historical p14 shows isolated
  positional forms; retain it and pair it with real shaped words/joins at larger
  size. Add mark-collision crops with unobtrusive guides. Use stable, attributed
  corpus files; clearly distinguish original text from annotation-stripped
  proof text. Do not claim complete Quranic support from selected passages.
- [ ] **P08: inspect output, not just existence.** Render all PDF pages to a
  contact sheet, inspect every page at readable scale, then targeted crops.
  Check clipping, footer intrusion, missing rows, mislabeled weights and fallback.
  Use browser proofs at named sizes and environments. Automated layout checks
  complement, but cannot replace, this visual review.
- [ ] **P09: implement before/after evidence.** Preserve baseline binaries and
  render same text/settings for each glyph batch: side-by-side, overlay and
  pixel/geometry differences. Inspect unintended dependent glyph changes.
  Record reviewed pages and findings; rendering alone never closes visual QA.
- [ ] **P10: confirm current GF review tooling.** Existing diffenator2 targets
  are useful, but refresh official project-template/tool expectations (including
  newer diffenator tooling) at release time. Use GF-style browser proofs as well
  as internal PDFs. Tool success never guarantees onboarding acceptance.

## P2 — Make agent automation dependable

- [ ] **A01: shorten the agent entrypoint.** Keep mission, authoritative files,
  proven commands, color rules and stop conditions in AGENTS.md. Move detailed
  procedures to existing `.agents/skills/`; replace stale slash-command promises
  with runnable CLI examples. Shared rules belong in AGENTS, not CLAUDE-only text.
  Ensure editor instructions honor the user's web-server default.
- [ ] **A02: add a doctor/bootstrap command.** Report versions, executables,
  reference-font coverage, project paths, renderer/browser availability and
  missing dependencies as JSON plus short text. Avoid reliance on `/Users/eli`;
  use explicit config/env for optional sibling tools and references.
- [ ] **A03: one reproducible task packet per batch.** Save source revision,
  permitted glyphs/master paths, glyph colors, dependency closure, evidence,
  suspected defect, proposed change, acceptance checks and current status.
  Statuses: queued, investigating, proposed, verified, needs-human, accepted.
  Do not count 'non-red' as shipped quality or automatically mark glyphs green.
- [ ] **A04: guarded source writes.** Before apply, verify current glyph hashes
  and colors, dry-run both masters, validate structure, stage changes atomically
  and support rollback. Recheck dependent composites. Fail if the editor or
  another task changed a source since inspection. Give each writing task its own
  worktree and make handoff/application explicit.
- [ ] **A05: wrap reliable operations before adding orchestration.** Expose
  inventory, build, QA, proof, compare and propose/apply as deterministic CLIs
  with JSON output and meaningful exit codes. A thin MCP wrapper may expose
  these later; do not build another dashboard before the underlying loop works.
  Runebender remains the visual editing/review surface.
- [ ] **A06: make the visual agent produce evidence.** Every finding names a
  glyph/codepoint, source master, weight, text, proof crop, measured symptom,
  severity, confidence and proposed remedy. Separate optical suggestions from
  verified blank/missing/structural defects. Require the agent to actually open
  images; never infer visual success from file generation or source markup.
- [ ] **A07: evaluate automation on known cases.** Maintain a small test corpus
  with blank hyphen, shifted accent, broken attachment, incompatible masters,
  preserved green glyph and deliberately unusual valid contour examples.
  Measure detection, false alarms, rejected changes and human acceptance.
  Store approved before/after pairs with provenance for later learning; do not
  require a model-training project to release this font.
- [ ] **A08: divide labor by judgment needed.** Use a strong vision/coding model
  for initial diagnosis, script interactions and optical proposals; use a less
  expensive coding model or scripts for bounded mechanical follow-up once
  acceptance is concrete. Proposed initial choice: GPT-6 Astra, high reasoning.
  Model identity does not substitute for qualification in Arabic/Hebrew design.
- [ ] **A09: resume from repository state.** At each completed batch, update this
  checklist and evidence log, commit explicit paths, record the next executable
  step and human decisions separately. Automated runs should pick the next
  unblocked item and stop at a real scope/design decision, not a stale checklist.
  Keep API credentials outside the repository; API automation, if introduced,
  needs explicit spend controls. Local deterministic checks need no LLM call.
- [ ] **A10: schedule only after reliability.** Prefer CI for commit-triggered
  build/QA/proofs. If later requested, add a Codex scheduled follow-up that only
  reports meaningful changes, failures or needed decisions. A newly created
  task starts work once; it is not automatically a persistent scheduled worker.

## P2 — Package, review and submit

- [ ] **S01: finalize project metadata.** Root METADATA.pb explicitly says
  PLACEHOLDER, declares only menu/latin/latin-ext, and uses primary_script Latn.
  Regenerate in real `ofl/virtuagrotesk` package context after G01; verify Arabic
  and any Hebrew scope, axis metadata, source mapping and public immutable source
  provenance. Do not hand-invent date_added or subset rescue entries.
- [ ] **S02: confirm identity and licensing.** OFL, AUTHORS and CONTRIBUTORS are
  present; verify exact copyright/name-table consistency, all contributions and
  reference/AI asset provenance, RFN status, family name availability and the
  human submitter's CLA identity. Do not treat file presence as legal review.
- [ ] **S03: finish public documentation.** README currently is essentially a
  hero image and blog link. Add project status, supported scripts/weights,
  build/proof instructions, license and issue links. Validate the chosen article/
  description format, designer information, specimen and release notes against
  current onboarding requirements.
- [ ] **S04: run a package dry run.** Refresh the packaging skill, assemble the
  downstream layout with correct fonts/license/article/metadata and verify all
  source.files entries and archive contents. Record exact source revision and
  binary hashes. Keep upstream artifacts separate from downstream submission.
- [ ] **S05: final unrestricted QA.** Run the current GF profile in package
  context with network checks available, plus glyphsets, shaping, interpolation,
  browser and print review. Resolve all real failures; retain explicit reviewer
  disposition for justified exceptions. No unexplained or hidden findings.
- [ ] **S06: human acceptance.** Eli signs off design, green/draft decisions,
  print proofs and scope; obtain Arabic/Hebrew reader review for scripts shipped.
  Confirm remaining optically subjective proposals and spelling/corpus accuracy.
- [ ] **S07: prepare submission materials.** Draft the current Add Font issue
  template honestly, listing scope and evidence. Check for an existing issue
  before duplication. Prepare downstream PR only after package review and the
  required onboarding issue. Obtain explicit authorization before posting public
  messages or publishing; local preparation can proceed now.
- [ ] **S08: ship the exact reviewed files.** After authorization and final QA,
  publish the agreed version/tag/archive, submit or update the downstream PR,
  address reviewer feedback, and revalidate changed files. Distinguish local
  readiness, submitted, approved and actually served on Google Fonts.

## Execution order and acceptance

1. R01–R05 and A02–A04: reliable gates, evidence and safe edits.
2. G01–G06 plus P02/P05/P09: current queue and comparable proofs.
3. Fix U+2010 and other unambiguous defects; then small diacritic, Arabic and
   Bold batches using D/V checks. Prepare protected-glyph proposals separately.
4. Complete full visual/script review and repeatable CI; package only the
   declared, reviewed scope. Finish S01–S08 with explicit publication authority.

Each closed checkbox needs a commit/evidence link, command result and review
status. For a glyph batch, done means: correct both-master source diff, compatible
build, relevant QA passing, before/after crops inspected, dependency regressions
checked, and human grading status recorded honestly. An unresolved human-only
item does not prevent independent engineering work on the next item.

## Sources checked for this review

- [GF onboarding](https://googlefonts.github.io/gf-guide/onboarding.html) and
  [production requirements](https://googlefonts.github.io/gf-guide/requirements.html).
- [GF upstream structure](https://googlefonts.github.io/gf-guide/upstream.html),
  [tools](https://googlefonts.github.io/gf-guide/tools.html), and
  [current Add Font template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md).
- [Fontspector](https://github.com/fonttools/fontspector), the FontBakery
  successor. Some guide pages still name FontBakery; reconcile current tooling
  with the live GF workflow at submission rather than copying old commands.
- [OpenAI agent instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
  [skills](https://developers.openai.com/codex/skills), and
  [model guidance](https://developers.openai.com/api/docs/guides/latest-model).
  The workflow above is a project-specific recommendation, not a claim that
  OpenAI or Google certifies automated type-design judgment.
