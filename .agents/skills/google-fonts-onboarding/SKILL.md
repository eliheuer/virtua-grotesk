---
name: google-fonts-onboarding
description: Prepare a font repository for Google Fonts onboarding, from first audit through handoff. Portable across font repos.
---

# /google-fonts-onboarding

Prepare a font repository for Google Fonts onboarding from first audit through
handoff. This skill is intentionally portable: `{{FAMILY}}`-style tokens are
defined in `.agents/google-fonts-onboarding-checklists.md` (in this repo,
`{{FAMILY}}` = Virtua Grotesk). When copying to another family, fill in that
token table and substitute.

## Usage
`/google-fonts-onboarding [audit|decisions|handoff|all]`

Default: `all`

## Principles

- Treat the current Google Fonts guide and `google/fonts` repository as the
  source of truth. Re-check the docs and templates before final issue or PR
  work because they change.
- Keep one canonical decision log for maintainer choices. Do not bury decisions
  only in generated reports.
- Separate drawing/source blockers from onboarding mechanics. A green handoff
  gate can still be blocked by glyph coverage, outlines, marks, kerning, or
  language quality.
- Prefer generated, repeatable reports for state that can drift: metadata,
  glyphset coverage, package files, release archives, auth, issue drafts, and
  downstream PR readiness.
- Do not open or update a downstream PR until a no-PR Packager run has been
  reviewed and the Google Fonts Add Font issue exists.

## Official References To Refresh

- Google Fonts guide index: https://googlefonts.github.io/gf-guide/
- Onboarding: https://googlefonts.github.io/gf-guide/onboarding.html
- Upstream repository structure: https://googlefonts.github.io/gf-guide/upstream.html
- Production requirements: https://googlefonts.github.io/gf-guide/requirements.html
- Variable fonts: https://googlefonts.github.io/gf-guide/variable.html
- Metadata: https://googlefonts.github.io/gf-guide/metadata.html
- Package guide: https://googlefonts.github.io/gf-guide/package.html
- Article guide: https://googlefonts.github.io/gf-guide/article.html
- Making a PR: https://googlefonts.github.io/gf-guide/making-pr.html
- Add Font issue template:
  https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md
- Google Fonts project template:
  https://github.com/googlefonts/googlefonts-project-template
- Glyphsets: https://github.com/googlefonts/glyphsets

## Audit Flow

1. Identify the active source files, build config, generated fonts, and intended
   downstream family directory.
2. Confirm license and authorship:
   - `OFL.txt` or equivalent license file is present and correct.
   - `AUTHORS.txt` and `CONTRIBUTORS.txt` are present if required.
   - Reserved Font Name status is explicit.
   - Copyright holder and Google CLA identity are known.
3. Confirm build reproducibility:
   - Build command is documented.
   - Variable and static outputs are produced as expected.
   - Generated outputs are ignored unless intentionally committed.
4. Run Fontspector with the Google Fonts profile. Google Fonts currently uses
   Fontspector for QA; only use older FontBakery references if a reviewer asks.
5. Audit glyphset coverage for the planned script scope. Latin Core is the
   minimum Add Font template requirement; non-Latin scope needs matching
   coverage, shaping, proofing, and language metadata review.
6. Audit variable-font metadata:
   - axes match the Google Fonts axis registry,
   - `fvar` instances match intended styles,
   - name table, version, license, `OS/2`, and `STAT` are sane,
   - `avar` warnings are either resolved or intentionally accepted.
7. Audit language metadata:
   - `subsets` includes `menu` and intended script subsets,
   - `primary_script` is present for non-Latin or mixed-script first submissions,
   - avoid custom `languages` and `sample_text` unless review asks for them.
8. Audit visual QA:
   - generate proof PDFs or HTML proofs,
   - review spacing and kerning by instance,
   - keep a written review checklist in the repo.
9. Audit package and release strategy:
   - decide default branch, latest release/archive, or build-from-source,
   - ensure every `source.files` entry is public and safe,
   - verify release archive contents and hashes if using release/archive mode.
10. Audit downstream readiness:
    - local `google/fonts` fork is synced,
    - dirty paths are limited to the target family directory,
    - current downstream family files are listed explicitly,
    - auth and Git identity are ready before commits or PR updates.

## Maintainer Decisions To Capture

Record answers, rationale, and apply-to surfaces for:

- public upstream URL,
- source packaging mode,
- first-submission script scope,
- family name and namecheck result,
- copyright authorship and AI-use disclosure,
- designer profile identity,
- Article vs legacy description,
- version and tag strategy,
- variable-axis and `avar` decisions,
- kerning scope,
- private-use glyph scope,
- project-template automation,
- any reviewer-approved exceptions.

## Handoff Gate

Before opening the issue or PR, the repo should have:

- current blockers and next actions,
- current Fontspector output,
- current visual proof review output,
- a current Add Font issue draft with unchecked template boxes,
- a current downstream metadata preview,
- a current package dry-run readiness report,
- a current downstream PR readiness report,
- release/archive evidence if that source strategy is selected.

For {{FAMILY}}, `make preflight` is the synchronized gate. In another repo,
create an equivalent command that regenerates reports and fails only for
documented, intentional blockers.
