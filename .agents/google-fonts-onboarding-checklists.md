# Google Fonts Onboarding Checklists

These checklists collect the reusable parts of the Virtua Grotesk onboarding
work so another font project can start from a stronger baseline. Copy this file
and the related `.agents/skills/google-fonts-*` skills into the next repo, then
replace family-specific paths, names, scripts, and source strategy values.

## 1. Repo Baseline

- Public upstream URL chosen and recorded.
- OFL or other accepted license present.
- `AUTHORS.txt` and `CONTRIBUTORS.txt` present when applicable.
- Reserved Font Name status explicit.
- Active sources live in a clear source directory.
- Generated build outputs are ignored unless the packaging strategy requires
  committing them.
- Build command documented and reproducible.
- Source archive or release strategy documented.
- README explains build, QA, proof, and handoff commands.
- Agent entrypoint points to the Google Fonts skills/checklists.

## 2. Decision Log

Create one canonical decision log with status, answer, rationale, and apply-to
surfaces. Track at least:

- public upstream URL,
- source packaging strategy,
- version and tag,
- family name, trademarks, namecheck, and RFN status,
- copyright holder and CLA identity,
- AI-use disclosure,
- designer profile identity,
- first-submission script scope,
- custom sample text,
- Article versus legacy description,
- variable-axis and `avar` decisions,
- vendor ID,
- kerning scope,
- private-use glyph scope,
- project-template automation.

## 3. Build And Binary QA

- Build variable fonts and expected static instances.
- Confirm generated file names and locations.
- Inspect name table, version, license, `OS/2.fsType`, vendor ID, `fvar`,
  `STAT`, and script metadata.
- Run Fontspector `googlefonts` profile.
- Save the report in `documentation/`.
- Classify every FAIL and WARN.
- Keep a final blocker summary that distinguishes drawing/source blockers from
  onboarding mechanics.

## 4. Glyphset And Script QA

- Identify intended first-submission script scope.
- Check Latin Core coverage.
- Check each non-Latin core glyphset needed for the submission.
- Generate missing-codepoint reports.
- Convert codepoint gaps into source glyph work by master.
- Verify mark glyphs, anchors, and mark/mkmk support when needed.
- Run shaping smoke tests for joining scripts.
- Keep script review packets linked from the Add Font issue draft.

## 5. Visual QA

- Generate proof PDF or equivalent local proof.
- Generate `gftools qa --proof` HTML output.
- Confirm proof coverage for every expected instance and proof type.
- Review spacing, kerning, diacritics, and script-specific behavior.
- Record review status and accepted deferrals.
- Rerun proofs after spacing, kerning, glyph, source, or scope changes.

## 6. Metadata

- Generate downstream `METADATA.pb` from built fonts and decisions.
- Check family and designer strings.
- Check `category`, `subsets`, and `primary_script`.
- Confirm `date_added` is final before applying downstream.
- Confirm `source.repository_url` is public and final.
- Confirm `source.commit` is a final 40-character lowercase commit.
- Include `source.archive_url` only when release/archive mode is selected.
- Include `source.config_yaml` only for build-from-source mode or reviewer
  request.
- Avoid custom `languages`, `sample_text`, or `tags` unless review asks.

## 7. Article And Images

- Decide Article versus legacy description.
- Keep `ARTICLE.en_us.html` valid and package-ready.
- Keep `DESCRIPTION.en_us.html` available if needed.
- Track image paths, size limits, and provenance/license.
- Use real font specimens or relevant visuals, not placeholder art.
- Confirm article assets appear in the selected package source strategy.

## 8. Designer Profile

- Compare final designer strings to existing `google/fonts` catalog profiles.
- Prepare `info.pb`, `bio.html`, and a square image when a profile is missing.
- Validate links, biography HTML, and image dimensions/format.
- Check for path collisions in the local `google/fonts` fork.
- Keep the designer-profile request plan linked from the Add Font issue draft.

## 9. Release And Package Strategy

- Choose default branch, latest-release/archive, or build-from-source.
- Verify every source file exists locally.
- Reject unsafe or duplicate source and destination paths.
- If using release/archive mode, build the archive from a manifest and verify
  contents plus hashes.
- Do not mark the archive URL final until the GitHub tag and release asset
  exist publicly.
- Keep fallback paths documented for Google Fonts reviewer requests.

## 10. Local google/fonts Fork

- Local fork exists.
- `origin` points to the maintainer fork.
- `upstream` points to `google/fonts`.
- Main branch is synced with both remotes.
- No dirty paths outside the target family directory.
- Current target family directory contents are listed explicitly.
- Starter `METADATA.pb` state is clearly marked when present.
- Git user name/email align with CLA and final downstream commit identity.
- GitHub API auth is ready before Packager calls that need GitHub.

## 11. Add Font Issue

- Refresh the current Add Font issue template from `google/fonts`.
- Use current template labels.
- Leave requirement checkboxes unchecked until opening the actual issue.
- Include the public repo URL.
- Include short description, namecheck status, maintenance commitment, license,
  source, TTF, glyphset, and QA status.
- Include AI-use disclosure when applicable.
- Include script-specific scope and known blockers.
- Link evidence reports instead of pasting long generated output.

## 12. Packager And PR

- Run Packager without PR mode first.
- Review generated downstream changes.
- Confirm changes are scoped to one family directory.
- Confirm metadata, fonts, article, image assets, license, and upstream linkage.
- Open or link the Add Font issue before PR mode.
- Use the expected PR title/body/provenance.
- Use `-p -i ISSUE_NUMBER` only after the no-PR package is reviewed.

## 13. Final Handoff

Before final issue/PR work, the repo should have current reports for:

- reference index,
- production requirements,
- decision readiness,
- final blockers,
- next actions,
- generated font metadata,
- glyphset coverage,
- language metadata,
- Fontspector results,
- proof review,
- package source files,
- source strategy,
- release archive manifest,
- downstream metadata,
- package dry-run readiness,
- Add Font issue draft,
- PR identity/auth,
- downstream PR readiness,
- designer profile readiness.

## 14. Copy-To-Next-Font Notes

When copying to another font repo:

- replace family name, style names, axes, source paths, and downstream directory,
- remove Virtua-specific Arabic, PUA, and release decisions unless they apply,
- refresh official Google Fonts docs and templates before relying on copied
  wording,
- rebuild report scripts around that repo's actual source structure,
- keep final gates strict enough to fail on stale generated evidence.

