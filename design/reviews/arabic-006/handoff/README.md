# Arabic first-pass manual handoff

The autonomous drawing pass has reached its manual-review handoff. **The Arabic
is not visually finished or approved.** Whole images still show substantial
structural and optical defects; the following list is the next drawing agenda,
not a list of minor release polish. No green grades were assigned.

Latest source checkpoint: `650b557a` (Tteh). The frozen Working font is
`../batches/36-tteh/assets/after.ttf`, SHA256
`11cf1a31805b5dc4013a81d38f4a131d56c652b539d368ad73a6f83fff8563df`.
The interactive proof's Before is the actual pre-batch01 font, not a rebuild.
All34 Beh/Heh reserved sources, manual Bold hamza, and other non-target sources
were preserved during batch36. No Runebender changes.

## Whole-image proofs

All28 core letters are present. Five stacked panels show Working, Rubik,
Noto Sans Arabic, IBM Plex Sans Arabic and Readex Pro at the same em size.
All core alphabet/word/mark panels have real coverage. Extensions show explicit
unavailability. Readex covers the Arabic digit row but not the Persian row.

| View | Regular400 | Bold700 | Intermediate550 |
| --- | --- | --- | --- |
| Isolated alphabet | [Image](alphabet-400.png) | [Image](alphabet-700.png) | [Image](alphabet-550.png) |
| Joining1: Alef–Khah | [Image](forms1-400.png) | [Image](forms1-700.png) | — |
| Joining2: Dal–Sad | [Image](forms2-400.png) | [Image](forms2-700.png) | — |
| Joining3: Dad–Qaf | [Image](forms3-400.png) | [Image](forms3-700.png) | — |
| Joining4: Kaf–Yeh | [Image](forms4-400.png) | [Image](forms4-700.png) | — |
| Words | [Image](words-400.png) | [Image](words-700.png) | [Image](words-550.png) |
| Marks/composites | [Image](marks-400.png) | [Image](marks-700.png) | [Image](marks-550.png) |
| Arabic/Persian digits | [Image](digits-400.png) | [Image](digits-700.png) | [Image](digits-550.png) |
| Selected extensions | [Image](extensions-400.png) | [Image](extensions-700.png) | — |

Joining samples use `ببب ب` for dual-joining letters. Right-joining letters use
Meem plus the target and its isolated form, e.g. `مد د`, so final forms are
actually exercised. The digit rows run0–9 left-to-right in separate cells.
DesignBot stacked the all-Arabic-numeral string even in reference fonts; the
cell render avoids that renderer issue. It does not repair or approve digits.
Every PNG has a JSON receipt with actual font hashes, text, size and coverage.
Plex550 is explicitly labeled500, its nearest supplied static face.

The [live proof](http://127.0.0.1:60272/) retains the existing layout and exposes
Arabic alphabet, Arabic joining forms, All scripts and Encoded repertoire.
[Browser capture](browser-700.png) records the selected700/48px alphabet view.
These are frozen snapshots; later editor saves require a new build/proof.

## Manual drawing priorities from the complete images

| Priority | Visible issue | Scope/protection |
| --- | --- | --- |
|1|Yeh/Maksura isolated and final have the wrong return/bowl skeleton; the raised hump does not perform the expected terminal sweep.|Regular Maksura isolated/final green; paired-master redesign needs the named exception or Eli's manual edit. Yeh inherits it.|
|1|Arabic initial/medial Kaf looks like a horizontal S or upright/sign construction rather than the contextual angled head. Lam–Alef resembles a narrow crossed loop.|Protected Regular Kaf and Lam–Alef structures; preserve pending manual repair.|
|1|Heh/Doachashmee forms are inconsistent: wrong single-bowl Doachashmee isolated/final, malformed initial construction, and disproportionate loops. Goal joining skeleton also differs from covered references.|Heh/Doachashmee reserved for Eli in both masters; some Regular Goal forms green. Rejected retry was never applied.|
|2|Seen/Sheen Regular underside has repeated cusps; Bold teeth, long flat joining bands and bowl mass are too mechanical and uneven. Sad/Dad bowls and counters need optical proportion review; Tah/Zah Regular stem-to-bowl trough remains.|Existing drafts, not human approved. Do not treat compatible topology or smooth extrema as an optical pass.|
|2|Dal/Dhal and Reh/Zain are very upright and box-like. Reh/Waw terminal sweeps and Hah-family head/return proportions need a whole-word review. Regular medial Meem sits low among its neighbors.|Some green sources, including Regular Dal and medial Meem; inspect colors and descendants before any revision.|
|2|Theh dots crowd and merge across joined forms, especially Bold. Teh/Noon/Qaf dot groups are large relative to the counters; dotted wrappers have uneven horizontal placement.|Shared dot donors are reserved through Beh. Use local wrapper corrections only or wait for Eli's donor changes.|
|3|Ain/fatha touches the crown in Bold. Shadda is box-like, damma too large, and hamza/mark counters close up. Alef-below-hamza still risks neighboring below-dot collisions.|Attachment/mark work remains after bases settle. Preserve manual Bold hamza. Existing high Gaf anchors, Sad final top x1684 and Barree final top x832 also remain unresolved.|
|3|Arabic/Persian digits2,3,4,5,6 have construction problems; Bold3 fills between teeth and7/8 become narrow wedges with cramped interiors. Arabic5 counter becomes tiny.|Digits are reviewed in images, not repaired or approved in this base-letter pass. Separate paired-master drawing work needed.|
|3|Rreh has a literal T-like mark, Ddal lacks a proper small Tah mark, and Goal/Doachashmee extension silhouettes still need redesign.|Tteh is fixed locally; malformed `smallHighTah-ar` and its consumers remain untouched.|

The word sheets also show uneven overall rhythm: broad flat bottoms, congested
joins and large dots compete with small counters at700. These need optical
judgment across complete words, not another bulk coordinate pass. No source
was changed merely to match the slant or outlines of a reference font.

## Verification and limits

Batch36 used exact before snapshots, scratch sources, all-source hash guards,
compatible17/9point local mark contours and unchanged Beh components. Fifty
shaping comparisons across400/475/550/625/700 restricted compiled differences
to the four Tteh forms. Signed curvature found no sampled local-mark reversals
or tangent kinks. Scratch build/preflight completed with no blocking master
compatibility mismatches. Preflight confirms artifact presence, not aesthetics.

Whole-sheet inspection covers the22 delivered raster plates and the live view.
`verification.json` ties the handoff to current sources, fonts and image hashes,
and checks the whole-sheet strings for missing glyphs with HarfBuzz. It does not
establish full language coverage, mark correctness, release readiness or human
approval. The recurring first-pass task is paused at this finite handoff.
