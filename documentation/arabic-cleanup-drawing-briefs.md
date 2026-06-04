# Arabic Cleanup Drawing Briefs

These generated briefs are prompt cards for the remaining manual Arabic
drawing cleanup. They are meant for Runebender review, AI-assisted
comparison notes, and hand editing. Do not copy outlines from Rubik or
any other reference font into Virtua Grotesk.

- Source report: `documentation/fontspector-contour-count.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Edit plan: `documentation/contour-cleanup-edit-plan.md`
- Source edit runlist: `documentation/contour-cleanup-source-edit-runlist.md`
- First edit batch: `documentation/contour-cleanup-first-edit-batch.md`
- Reference font availability: `/Users/eli/GH/forks/fonts/ofl/rubik/Rubik[wght].ttf`
- Briefs: 4

## How To Use

For each brief:

1. Open the source glyph in both masters with the listed command.
2. Compare Virtua against the proof HTML and reference only for structure cues.
3. Decide whether the warning is a real drawing issue, an acceptable style divergence, or a deferral.
4. If editing, preserve master compatibility and rerun the batch commands.

## 1. dad-ar.init

- Priority: P1 source-structure check
- Category: source outline review
- Fontspector glyph: `uni0636.init`
- Codepoint: unencoded
- Built fonts flagged: `VirtuaGrotesk[wght].ttf`
- Actual contour count(s): 2
- Expected contour count(s): 3, 5
- Rubik reference glyph: not available
- Command: `/edit-glyph dad-ar.init --master both`

Source structure:

- Regular: `c0/p0/comp2` in `dad-ar.init.glif`; components: `sad-ar.init`, `dotabove-ar`
- Bold: `c0/p0/comp2` in `dad-ar.init.glif`; components: `sad-ar.init`, `dotabove-ar`

Review question:

- Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence?

AI comparison prompt:

```text
Review Virtua Grotesk `dad-ar.init` in Regular and Bold. Fontspector flags `uni0636.init` with contour count 2 where it expects 3, 5. Compare the current drawing to the family style and to Rubik only as a structural reference. Do not copy reference outlines. Identify whether this should be fixed now, accepted as a style divergence, or deferred for Arabic native-reader review.
```

Acceptance criteria:

- Compiled output and source structure tell the same story after review.
- Any component decomposition or contour addition is intentional and mirrored.
- Regular and Bold keep matching contour, point, and component structure.
- `make contour-cleanup-proof` reflects the intended decision after editing.
- `make preflight-only` still passes with only documented blockers.

Batch commands after edits:

```bash
make contour-cleanup-proof
make preflight-only
```

## 2. hah-ar.fina

- Priority: P1 source-structure check
- Category: source outline review
- Fontspector glyph: `uni062D.fina`
- Codepoint: unencoded
- Built fonts flagged: `VirtuaGrotesk[wght].ttf`
- Actual contour count(s): 3
- Expected contour count(s): 1, 2
- Rubik reference glyph: not available
- Command: `/edit-glyph hah-ar.fina --master both`

Source structure:

- Regular: `c3/p67/comp0` in `hah-ar.fina.glif`; components: none
- Bold: `c3/p67/comp0` in `hah-ar.fina.glif`; components: none

Review question:

- Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence?

AI comparison prompt:

```text
Review Virtua Grotesk `hah-ar.fina` in Regular and Bold. Fontspector flags `uni062D.fina` with contour count 3 where it expects 1, 2. Compare the current drawing to the family style and to Rubik only as a structural reference. Do not copy reference outlines. Identify whether this should be fixed now, accepted as a style divergence, or deferred for Arabic native-reader review.
```

Acceptance criteria:

- Compiled output and source structure tell the same story after review.
- Any component decomposition or contour addition is intentional and mirrored.
- Regular and Bold keep matching contour, point, and component structure.
- `make contour-cleanup-proof` reflects the intended decision after editing.
- `make preflight-only` still passes with only documented blockers.

Batch commands after edits:

```bash
make contour-cleanup-proof
make preflight-only
```

## 3. jeem-ar.fina

- Priority: P1 source-structure check
- Category: source outline review
- Fontspector glyph: `uni062C.fina`
- Codepoint: unencoded
- Built fonts flagged: `VirtuaGrotesk[wght].ttf`
- Actual contour count(s): 4
- Expected contour count(s): 2, 3
- Rubik reference glyph: not available
- Command: `/edit-glyph jeem-ar.fina --master both`

Source structure:

- Regular: `c4/p83/comp0` in `jeem-ar.fina.glif`; components: none
- Bold: `c4/p83/comp0` in `jeem-ar.fina.glif`; components: none

Review question:

- Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence?

AI comparison prompt:

```text
Review Virtua Grotesk `jeem-ar.fina` in Regular and Bold. Fontspector flags `uni062C.fina` with contour count 4 where it expects 2, 3. Compare the current drawing to the family style and to Rubik only as a structural reference. Do not copy reference outlines. Identify whether this should be fixed now, accepted as a style divergence, or deferred for Arabic native-reader review.
```

Acceptance criteria:

- Compiled output and source structure tell the same story after review.
- Any component decomposition or contour addition is intentional and mirrored.
- Regular and Bold keep matching contour, point, and component structure.
- `make contour-cleanup-proof` reflects the intended decision after editing.
- `make preflight-only` still passes with only documented blockers.

Batch commands after edits:

```bash
make contour-cleanup-proof
make preflight-only
```

## 4. sad-ar.init

- Priority: P1 source-structure check
- Category: source outline review
- Fontspector glyph: `uni0635.init`
- Codepoint: unencoded
- Built fonts flagged: `VirtuaGrotesk[wght].ttf`
- Actual contour count(s): 1
- Expected contour count(s): 2
- Rubik reference glyph: not available
- Command: `/edit-glyph sad-ar.init --master both`

Source structure:

- Regular: `c1/p49/comp0` in `sad-ar.init.glif`; components: none
- Bold: `c1/p49/comp0` in `sad-ar.init.glif`; components: none

Review question:

- Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence?

AI comparison prompt:

```text
Review Virtua Grotesk `sad-ar.init` in Regular and Bold. Fontspector flags `uni0635.init` with contour count 1 where it expects 2. Compare the current drawing to the family style and to Rubik only as a structural reference. Do not copy reference outlines. Identify whether this should be fixed now, accepted as a style divergence, or deferred for Arabic native-reader review.
```

Acceptance criteria:

- Compiled output and source structure tell the same story after review.
- Any component decomposition or contour addition is intentional and mirrored.
- Regular and Bold keep matching contour, point, and component structure.
- `make contour-cleanup-proof` reflects the intended decision after editing.
- `make preflight-only` still passes with only documented blockers.

Batch commands after edits:

```bash
make contour-cleanup-proof
make preflight-only
```
