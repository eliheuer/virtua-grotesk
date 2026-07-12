# Google Fonts Workflow Porting Checklist

Copy this file into another font repo when using Virtua Grotesk as the model
for an AI-assisted Google Fonts preparation workflow. The goal is to copy the
system, not the family-specific data.

## 1. Decide The Source Contract

- [ ] Active source format is clear: designspace plus UFOs, Glyphs file, or
      another single source of truth.
- [ ] Generated outputs are not treated as source.
- [ ] Build output directories are gitignored (`fonts/`, `build/`,
      `sources/instance_ufos/`, `build.ninja`, `.ninja_log`).
- [ ] The source family name, style names, axis tags, instances, and output
      filenames are documented.
- [ ] Master compatibility expectations are explicit before drawing work starts.

Virtua Grotesk model:

- `sources/config.yaml`
- `sources/*.designspace`
- `sources/*.ufo`
- `sources/README.md`
- `documentation/source-guides/`

## 2. Copy The Minimal Workflow Files

Copy and adapt these files from Virtua Grotesk:

- [ ] `Makefile`
- [ ] `build.sh`
- [ ] `requirements.in`
- [ ] `requirements.txt`
- [ ] `scripts/check_gf_fonts.sh`
- [ ] `scripts/fix_gf_metadata.py`
- [ ] `scripts/preflight.py`
- [ ] `scripts/run_reports.py`
- [ ] `scripts/report_source_metadata.py`
- [ ] `scripts/report_generated_font_metadata.py`
- [ ] `scripts/report_master_compatibility.py`
- [ ] `scripts/build_general_proof.py`
- [ ] `scripts/build_print_spacing_specimen.py`
- [ ] `scripts/build_readme_images.py`
- [ ] `scripts/build_social_images.py`
- [ ] `scripts/grid_system.py`
- [ ] `documentation/core-qa-process.md`
- [ ] `documentation/manual-cleanup-handoff.md`
- [ ] `.agents/`
- [ ] `AGENTS.md`

Do not copy archived generated report/script folders unless you are deliberately
reviving one tool:

- `documentation/archive/agent-generated-reports/`
- `documentation/archive/agent-generated-scripts/`

## 3. Set Up The Build

- [ ] Create or adapt `sources/config.yaml` for `gftools builder`.
- [ ] Confirm output goes to `fonts/`.
- [ ] Confirm the build creates:
  - [ ] `fonts/variable/<Family>[axis].ttf`
  - [ ] `fonts/ttf/<Family>-Regular.ttf`
  - [ ] all expected static styles.
- [ ] Keep `flattenComponents: false` and
      `decomposeTransformedComponents: false` unless the source requires a
      different policy.
- [ ] Update `build.sh` with the new family paths and expected outputs.
- [ ] Run `make setup`.
- [ ] Run `make build`.

## 4. Set Up Proofs And Specimens

- [ ] Use `.venv/` in the repo root.
- [ ] Render proofs and specimens with designbot (`make proof` / `make specimen`).
- [ ] Adapt `scripts/grid_system.py` to the new font's UPM, ascender,
      descender, cap height, x-height, and design grid.
- [ ] Adapt `scripts/build_general_proof.py`.
- [ ] Adapt `scripts/build_print_spacing_specimen.py`.
- [ ] Adapt `scripts/build_readme_images.py`.
- [ ] Adapt `scripts/build_social_images.py`.
- [ ] Run:
  - [ ] `make proof`
  - [ ] `make specimen`
  - [ ] `make readme-images`
  - [ ] `make social-images`
- [ ] Confirm generated artifacts exist:
  - [ ] `documentation/proofs/proof.pdf`
  - [ ] `documentation/proofs/print-spacing-specimen.pdf`
  - [ ] README PNGs under `documentation/assets/readme/`

## 5. Set Up Reports And Preflight

- [ ] Adapt `scripts/run_reports.py` to the new family paths and font outputs.
- [ ] Adapt `scripts/preflight.py` required files.
- [ ] Run `make reports`.
- [ ] Confirm reports exist:
  - [ ] `documentation/source/source-ufo-metadata.md`
  - [ ] `documentation/source/generated-font-metadata.md`
  - [ ] `documentation/source/master-compatibility.md`
- [ ] Run `make preflight`.
- [ ] Treat a passing `make preflight` as the normal agent handoff gate, not as
      final Google Fonts readiness.

## 6. Set Up Google Fonts QA

- [ ] Install Fontspector in the local toolchain.
- [ ] Adapt `scripts/check_gf_fonts.sh` font paths.
- [ ] Keep exclusions small, documented, and temporary.
- [ ] Every excluded check has:
  - [ ] a reason,
  - [ ] an owner or drawing/metadata phase,
  - [ ] a condition for removing the exclusion.
- [ ] Run `make qa` or `make test`.
- [ ] The release bar is: **zero FAIL and zero WARN output from `make qa`**.
- [ ] Anything WARN/FAIL printed by `make qa` is a regression unless it is
      intentionally excluded with a documented reason.

## 7. Copy The Agent Operating Rules

- [ ] Copy `AGENTS.md` and rewrite family-specific sections.
- [ ] Copy `.agents/skills/` and remove skills that do not apply.
- [ ] Keep the reusable Google Fonts skills:
  - [ ] `.agents/skills/google-fonts-onboarding/SKILL.md`
  - [ ] `.agents/skills/google-fonts-qa/SKILL.md`
  - [ ] `.agents/skills/google-fonts-packaging/SKILL.md`
  - [ ] `.agents/skills/google-fonts-nonlatin-drawing/SKILL.md`
- [ ] Make `make preflight` and `make test` obvious in `AGENTS.md`.
- [ ] Tell agents that generated outlines, generated reports, and temporary AI
      review files are not source unless explicitly promoted.

## 8. Drawing And Source QA

- [ ] Missing glyphs are separated from bad drawings.
- [ ] Hand-drawn glyphs are protected from bulk replacement.
- [ ] Script coverage is treated as one family design, not an add-on.
- [ ] Both masters keep identical glyph structure for interpolation.
- [ ] Every drawing batch ends with:
  - [ ] `make build`
  - [ ] `make proof` or `make specimen`
  - [ ] `make reports`
  - [ ] `make preflight`
- [ ] Before final submission, run `make test` and clear all WARN/FAIL output.

## 9. README And Public Repo Polish

- [ ] README shows current specimen images and no dead image links.
- [ ] README explains the family, axes, source format, build command, and QA
      command.
- [ ] `OFL.txt`, `AUTHORS.txt`, and `CONTRIBUTORS.txt` are present and current.
- [ ] Root directory is small and understandable.
- [ ] Large generated PDFs/PNGs are intentional.
- [ ] Old generated AI report farms are archived or deleted, not presented as
      current instructions.

## 10. Final Local Gate

Run these before calling the repo ready for a Google Fonts submission pass:

```bash
make clean
make setup
make build
make proof
make specimen
make readme-images
make social-images
make reports
make preflight
make test
```

Required result:

- [ ] Build succeeds.
- [ ] Proofs/specimens render.
- [ ] Reports are current.
- [ ] Preflight passes.
- [ ] `make test` / `make qa` prints no FAIL and no WARN output.
- [ ] Remaining blockers are only human decisions or documented drawing work,
      not missing workflow infrastructure.
