# Contour Cleanup Batches

This generated batch sheet turns the remaining Fontspector contour-count
warnings into short hand-edit sessions. It is designed for Runebender
cleanup plus AI comparison notes. Rubik is a structural reference only;
do not copy outlines from it into Virtua Grotesk.

- Source report: `documentation/fontspector-contour-count.md`
- Visual proof: `documentation/contour-cleanup-proof.html`
- Source edit runlist: `documentation/contour-cleanup-source-edit-runlist.md`
- First edit batch: `documentation/contour-cleanup-first-edit-batch.md`
- Detailed prompt cards: `documentation/arabic-cleanup-drawing-briefs.md`
- Unique review items: 4
- All-font finding rows: 4

## Recommended Session Order

1. Component-only source forms: decide whether the component structure is
   intentional or should be decomposed/redrawn in both masters.
2. Referenced Arabic marks and ligatures: use Rubik only to understand
   expected structure and mark stacking behavior.
3. Dot-stack helpers: check Bold collisions and readability first.
4. Arabic letterform review: judge skeleton, joins, counters, and chamfers.
5. Shared punctuation: keep Latin and Arabic text behavior aligned.
6. Source-outline judgment calls: accept, defer, or redraw deliberately.

After each batch:

```bash
make contour-cleanup-proof
make preflight-only
```

## 1. Component-only source forms

- Items: 1

| Source glyph | Fontspector glyph | Actual | Expected | Source structure | Reference | Command | First decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dad-ar.init` | `uni0636.init` | 2 | 3, 5 | Regular: `c0/p0/comp2`<br>Bold: `c0/p0/comp2` | no | `/edit-glyph dad-ar.init --master both` | Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence? |

AI batch prompt:

```text
Review the 1 Virtua Grotesk glyphs in the '1. Component-only source forms' batch. Use the contour proof and Rubik only as structure references. Do not copy outlines. For each glyph, classify the warning as fix now, accept as style divergence, or defer for Arabic native-reader review, and explain the minimal two-master edit if a fix is needed.
```

## 6. Source-outline judgment calls

- Items: 3

| Source glyph | Fontspector glyph | Actual | Expected | Source structure | Reference | Command | First decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `hah-ar.fina` | `uni062D.fina` | 3 | 1, 2 | Regular: `c3/p67/comp0`<br>Bold: `c3/p67/comp0` | no | `/edit-glyph hah-ar.fina --master both` | Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence? |
| `jeem-ar.fina` | `uni062C.fina` | 4 | 2, 3 | Regular: `c4/p83/comp0`<br>Bold: `c4/p83/comp0` | no | `/edit-glyph jeem-ar.fina --master both` | Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence? |
| `sad-ar.init` | `uni0635.init` | 1 | 2 | Regular: `c1/p49/comp0`<br>Bold: `c1/p49/comp0` | no | `/edit-glyph sad-ar.init --master both` | Is the compiled contour-count warning pointing at a real source drawing problem or an acceptable style divergence? |

AI batch prompt:

```text
Review the 3 Virtua Grotesk glyphs in the '6. Source-outline judgment calls' batch. Use the contour proof and Rubik only as structure references. Do not copy outlines. For each glyph, classify the warning as fix now, accept as style divergence, or defer for Arabic native-reader review, and explain the minimal two-master edit if a fix is needed.
```
