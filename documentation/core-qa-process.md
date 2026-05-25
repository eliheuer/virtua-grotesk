# Core QA Process

This is the canonical QA checklist for Virtua Grotesk while it is being
prepared for Google Fonts onboarding. It is for both humans and agents; keep it
updated when the build, proofing, Fontspector, or Packager workflow changes.

## Required Local Gates

Run these from the repo root unless a section says otherwise.

| Gate | Command | Purpose | When to run |
| --- | --- | --- | --- |
| Build | `make build` | Builds variable and static TTFs from `sources/config.yaml`. | After source, feature, metadata, or build-script changes. |
| Automated Google Fonts QA | `make test` | Builds, then runs Fontspector's `googlefonts` profile. | Before final submission and after any fix that should reduce Fontspector FAIL/WARN output. |
| Visual spacing and kerning proof | `make kerning-proof-check` | Runs `gftools qa --proof` and writes HTML proof output to `documentation/gftools-qa/`. | After spacing, kerning, built-font, or kerning-scope decision changes. |
| Visual proof review packet | `make kerning-proof-review-check` | Generates `documentation/kerning-proof-review.md`, listing the expected gftools proof files and human review checklist. | After regenerating the gftools proof output or before accepting a kerning deferral. |
| PDF proof | `make proof` | Builds, then renders the DrawBot-style proof PDF with the local `eliheuer/drawbot-skia` fork. | During drawing/source review and before handoff snapshots. |
| Readiness reports | `make reports` | Regenerates generated readiness reports from current built fonts and local checkout state. | After build, metadata, package, or decision changes. |
| Designer profile validators | `make designer-profile-validator-test` | Tests profile `info.pb`, image, bio, and guarded prepare-helper blockers without touching the real `google/fonts` checkout. | After changing designer-profile validators, the prepare helper, or draft-profile rules. |
| Current handoff gate | `make preflight` | Builds, regenerates proof and reports, then allows only documented drawing/source blockers. | Before handing work back or before any packaging/release milestone. |
| Final strict QA | `make test` | Same Fontspector gate, but final submission should have no unexpected FAILs. | After drawing/source blockers are resolved. |

Use `make preflight-only` only when the build outputs and generated reports are
already current. Use `make handoff` when you want the synchronized build,
proof, reports, and preflight path in one command.

## Fontspector Policy

Fontspector is this repo's automated Google Fonts QA entrypoint. The local
scripts use the normal persistent `~/.fontspector` directory and pass
`--skip-network` for repeatable local checks.

Older Google Fonts guide and project-template text may still mention
FontBakery-based automation. Do not replace this repo's Fontspector workflow
with FontBakery unless a Google Fonts reviewer asks for a specific legacy
check. Future CI, if added, should run this repo's Fontspector-based
`make test` path.

## Visual Proof Policy

`make kerning-proof-check` is a core QA step, not an optional artifact
generator. The Google Fonts onboarder workflow calls out generated QA proofs as
part of the packaging/review toolchain, and the local testing guide explicitly
includes kerning and spacing behavior in app and browser review.

`gftools qa --proof` checks `https://fonts.google.com/metadata/fonts` before
rendering proofs, so this step needs network access even though the proof input
font is local. If it fails with a DNS or connection error, rerun the same target
with network access rather than treating the existing HTML files as refreshed.

Before kerning, spacing, or a kerning deferral is considered final:

- Run `make kerning-check`.
- Run `make kerning-proof-check`.
- Run `make kerning-proof-review-check`.
- Review the HTML output in `documentation/gftools-qa/`.
- Use `documentation/kerning-proof-review.md` to make sure every expected
  proof type and weight instance has been inspected.
- Confirm `documentation/kerning-readiness.md` records the current source
  kerning, built GPOS `kern`, Fontspector warning, and proof-output state.
- Rerun `make preflight`.

## Arabic QA Policy

Arabic remains in first-submission scope. The local QA process must continue to
track:

- `GF_Arabic_Core` coverage.
- Arabic GSUB shaping smoke tests.
- Arabic marks, dotted circle, source anchors, and mark/mkmk readiness.
- `primary_script: "Arab"` and Arabic subset metadata.
- Visual proof review after Arabic drawing or positioning changes.

The drawing work can remain incomplete during onboarding preparation, but the
missing Arabic coverage and mark-positioning work must stay visible in
`documentation/final-submission-blockers.md` and `documentation/next-actions.md`.

## Packaging QA Policy

Packaging work is not ready just because `make preflight` passes. Before a
downstream PR:

- Run `make package-readiness-check`.
- Run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`
  with the selected source mode.
- Apply downstream `METADATA.pb` only after the final release/source commit,
  release archive, and `date_added` value are settled.
- Run `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without
  `-p`.
- Review the generated local `google/fonts/ofl/virtuagrotesk` package before
  opening or updating a PR.

## References

- https://googlefonts.github.io/gf-guide/tools.html
- https://googlefonts.github.io/gf-guide/qa.html
- https://googlefonts.github.io/gf-guide/testing.html
- https://googlefonts.github.io/gf-guide/onboarder-workflow.html
- https://googlefonts.github.io/gf-guide/production.html
- https://googlefonts.github.io/gf-guide/package.html
- https://github.com/fonttools/fontspector
- https://github.com/googlefonts/gftools
