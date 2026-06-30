# Goal: Virtua Grotesk → Google Fonts (Roman + Italic, wght 400–700)

A goal document for the Codex `/goal` command. Drive this autonomously; the
success signal is a clean, unexcluded `make test` for both styles plus a
packaged, PR-ready family. Read `AGENTS.md` and
`documentation/google-fonts-readiness.md` first — this goal builds on them, it
does not repeat them.

## Objective

Ship Virtua Grotesk to Google Fonts as a complete, professional grotesk family
that is a usable alternative to Inter and Geist: an upright (**Roman**) and an
**Italic**, each a variable font over a constrained Weight axis (**wght 400–700,
Regular to Bold**). Done means both styles pass Google Fonts QA with no deferred
checks, and the family is packaged and PR-ready.

## Definition of done (the measurable target)

1. **Roman** — `make test` (Fontspector `googlefonts`) is clean with **no
   excludes** in `scripts/check_gf_fonts.sh`; every currently-deferred check
   passes.
2. **Italic** — an Italic variable font `fonts/variable/VirtuaGrotesk-Italic[wght].ttf`
   (wght 400–700) exists, interpolates, and passes the same `googlefonts` QA with
   no excludes.
3. **Family** — `METADATA.pb` declares the family with Roman + Italic linked
   (italic flag set), the downstream `ofl/virtuagrotesk/` layout exists, and the
   package passes Google Fonts onboarding QA.
4. Master compatibility is clean within each style; variable + static builds are
   clean; proofs reviewed.

The exclude list in `check_gf_fonts.sh` is the burn-down for the Roman; reaching
the same zero-exclude state for the Italic is its burn-down.

## Scope & constraints (do not deviate without asking the maintainer)

- **Weight axis only, 400–700**, for both Roman and Italic. Do NOT add Thin /
  Black weights or any other axis.
- **The Italic is a SEPARATE variable font** (Roman VF + Italic VF), linked in
  `METADATA.pb` — not a single VF with an `ital` axis. This avoids forcing
  roman↔italic outline compatibility.
- **Design language is fixed**: 16-unit chamfered corners, monolinear strokes,
  counter-reduction weight gain (`documentation/source-guides/design-philosophy.md`).
  The Italic must keep this character.
- **Master compatibility is sacred**: within each style, Regular and Bold masters
  must be structurally identical (same contours, point counts, point types).
  Mirror every structural edit across both masters.
- **Never re-add a QA exclude to force a green gate.** The excludes are the
  to-do list, not a setting.

## Decisions to confirm with the maintainer before Phase 2

1. **Italic style.** Recommended for launch: a **corrected oblique** (sloped
   roman, ~10°, with optical corrections to round and diagonal forms) — the
   fastest path to a shippable, on-character italic, and what many respected
   grotesks ship. A true cursive italic (single-story `a`, cursive `e`/`f`/`g`)
   is more competitive with Inter but much more work; treat it as an explicit
   fast-follow pass, not a launch blocker. **Confirm oblique vs true italic
   before drawing.**
2. **Slant angle** (default 10°) and whether to add a `slnt`/`ital` STAT linkage
   now or just ship the two linked VFs.

## Phase 1 — Finish the Roman for Google Fonts (do this first)

Work the current worklist in `documentation/google-fonts-readiness.md`, in order:

1. Fix `whitespace_widths`: set `nbspace` to the same width as `space` in both
   masters.
2. Remove the two already-passing Arabic excludes (`outline_colinear_vectors`,
   `outline_semi_vertical`) after verifying them on the full gate.
3. Snap the ~16 off-baseline Arabic on-curve points (1–2.5 units off) to Y=0 in
   both masters.
4. Fix the 4 `contour_count` Arabic glyphs — `uni062C.fina`/`uni062D.fina` have
   extra contours (remove the overlap), `uni0635.init`/`uni0636.init` are missing
   a contour (add it). Re-trace via `img2bez masters` from a clean reference, or
   hand-clean in Runebender; mirror both masters.
5. Address Latin `googlefonts/glyphsets/shape_languages` (mark anchors over
   ogonek / dotaccent bases, breve / macron composites).
6. **Delete each exclude as its check passes. Phase 1 is done when `make test` is
   clean with zero outline/shape excludes.**

Per-glyph loop: edit → `make reports` (master-compat clean) → `make build` →
`make proof` → re-run the gate.

## Phase 2 — Add the Italic

1. **Create the Italic masters.** Produce `VirtuaGrotesk-Italic-Regular.ufo` and
   `VirtuaGrotesk-Italic-Bold.ufo` by slanting the corresponding Roman masters
   (~10°) and applying optical corrections; keep the chamfer character. Use the
   project's source conventions (do not `font.save()` through defcon — see
   `CLAUDE.md`). The two italic masters must be structurally compatible with each
   other.
2. **Wire the build.** Add an Italic designspace (or extend `sources/config.yaml`)
   so `make build` also produces `fonts/variable/VirtuaGrotesk-Italic[wght].ttf`
   over wght 400–700.
3. **Draw / correct glyph by glyph.** For glyphs the slant breaks (rounds,
   crossbars, diagonals, terminals — plus any cursive substitutions the
   maintainer approved), correct in Runebender or regenerate via the AI-glyph
   harness (OpenAI image-gen → `img2bez` trace), mirrored across both italic
   masters.
4. **Space & kern the Italic** — its own sidebearings and kerning (`/kerning`).
5. **QA the Italic to the same bar** — build + `googlefonts` Fontspector with no
   excludes, master-compat clean, proofs reviewed.
6. **Phase 2 is done when the Italic VF passes the gate clean and interpolates.**

## Phase 3 — Package & submit

1. Run `/google-fonts-packaging` to produce `METADATA.pb` (Roman + Italic linked,
   italic flag set) and the downstream `ofl/virtuagrotesk/` layout.
2. Confirm `DESCRIPTION.en_us.html`, `ARTICLE.en_us.html`, `OFL.txt`,
   `AUTHORS.txt`, `CONTRIBUTORS.txt`, and the designer profile are in place.
3. Run `/google-fonts-onboarding` and `/google-fonts-qa`; resolve everything they
   flag.
4. Open the PR to `google/fonts`. The goal is met when onboarding QA is green and
   the PR is ready for review.

## Tools & loop (the means)

- **Draw / fix glyphs** — `img2bez masters` (trace from reference images,
  including OpenAI image-gen via `/glyph-ai-harness`); Runebender (`make
  runebender`) for visual review/edit. Skills: `/draw-outline`, `/edit-glyph`,
  `/compare-reference`, `/glyph-ai-harness`.
- **Build / QA** — `make build`, `make test`, `make proof` / `make specimen`,
  `make preflight`; `/font-qa`.
- **Package** — `/google-fonts-packaging`, `/google-fonts-onboarding`,
  `/google-fonts-qa`.
- `AGENTS.md` holds the conventions (master compatibility, glif-editing rules,
  metrics).

## Guardrails — stop and ask the maintainer if

- A fix would break master compatibility and you cannot mirror it across both
  masters.
- The Italic style, slant, or axis structure is ambiguous (see Decisions).
- A QA check can only be made to pass by excluding it.
- Adding a glyph, axis, or script would push the family beyond this goal's scope.
