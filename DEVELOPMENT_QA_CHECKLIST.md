# Virtua Grotesk — Development QA Checklist

Test as you draw, and match Google Fonts' onboarding review. The GF
onboarders' gold-standard *visual* tool is **diffenator2**; the reference we
match against is **Rubik** (a shipped GF family with Latin/Hebrew/Cyrillic/
Arabic and a proper anchor system). Goal: our diacritics, spacing, and
kerning should look as clean as Rubik's in diffenator2.

All commands run from the repo root with the project venv (`.venv/bin/…`).

---

## 0. Build
```
make build            # -> fonts/ttf/*.ttf, fonts/variable/VirtuaGrotesk[wght].ttf
```

## 1. Fast loop (every drawing session)
```
.venv/bin/python scripts/curve_lint.py Regular <glyphs>   # outline hygiene
make grid-qa                                              # on-grid check
make metrics                                              # normalized vs Inter/Geist
```
Plus a quick PIL/hb render of whatever you touched.

## 2. diffenator2 — the GF onboarders' gold standard  ✅ WIRED UP
What GF reviewers actually use to review submissions. Run via the Makefile
(the targets put the venv on PATH so diffenator2's `_diffbrowsers` helper
resolves — running `.venv/bin/diffenator2` directly fails without that):
```
make review          # Virtua -> out/review/diffenator2-report.html
make review-rubik    # Rubik reference -> out/review-rubik/diffenator2-report.html
```
Open the report in a browser. Each has 4 views per instance:
- **proofer** — the diacritic + spacing view (the important one for accents)
- **glyphs** — the full glyph set
- **waterfall** — sizes; **text** — running text
For before/after regression: `.venv/bin/diffenator2 diff OLD.ttf NEW.ttf -o out/diff`
(also run with the venv on PATH). `out/` is gitignored.

## 3. Match Rubik (the workflow that lets agents do most of the work)
- Built ref: `~/GH/repos/google-fonts/ofl/rubik/Rubik[wght].ttf`
- Source (anchor reference): `~/GH/repos/rubik/sources/Rubik.glyphs`
  ```
  .venv/bin/fontmake -g ~/GH/repos/rubik/sources/Rubik.glyphs -o ufo   # to read anchors
  ```
- **Interim visual compare (works now, until diffenator2 proof is wired):**
  ```
  .venv/bin/python scripts/compare_diacritics.py     # -> out/diacritics-vs-rubik.png
  ```
  Renders Virtua vs Rubik stacked for the accented set. Eyeball (or hand to a
  vision agent) for centering, height consistency, and optical lean.
- **When diffenator2 proof is green:** `proof` Virtua and Rubik separately,
  compare diacritics / spacing / kerning, and match Rubik's placement.

## 4. Diacritic fix + acceptance
Fix tool (deterministic, both masters):
```
.venv/bin/python scripts/fix_accent_offsets.py   # xOffset = base_center - mark_center
```
Rerun this after ANY base-glyph edit — composite offsets are recomputed from
the base centers, so base edits otherwise silently shift accents.

Acceptance (match Rubik in diffenator2):
- [ ] Accents horizontally centered (or optically matched to Rubik)
- [ ] Lowercase accents at one height; caps at one higher height (yOffset 0 / 144)
- [ ] Below-marks (cedilla, ogonek, commaaccent) centered under the base
- [ ] Angled marks (acute/grave) optically nudged toward Rubik
- [ ] No base edit has left an accent off — rerun fix_accent_offsets after base work

## 5. Spec / metadata / coverage (before a PR)
```
.venv/bin/fontbakery check-googlefonts fonts/ttf/*.ttf   # installed 1.1.0
.venv/bin/shaperglot report fonts/ttf/VirtuaGrotesk-Regular.ttf   # language coverage
.venv/bin/gftools qa -f "fonts/variable/VirtuaGrotesk[wght].ttf" --proof -o out/gfqa
```
Note: `fontspector` (newer Rust replacement for fontbakery) is **not installed**
— `pip install fontspector` (or cargo) if you want it.

## 6. Ship
- `GOOGLE_FONTS_PORTING_CHECKLIST.md` (existing) — packaging/metadata/PR.
- GF engineering hub: https://googlefonts.github.io/

---

### Reference: what "gold standard" means here
diffenator2 is the onboarders' review tool, so anything that reads clean in
its proof/diff — measured against Rubik — is what a reviewer will accept.
Agents (and Gemma, once wired per `font-garden-lab/notes/gemma-workflow-
integration.md`) run §3–§4 to flag and fix; Eli does the final cleanup pass.
