# Google Fonts Decision Questions

These are the remaining non-drawing decisions before treating the Google Fonts
handoff as final. Record answers here first, then update
`documentation/google-fonts-decisions.md` and the affected source metadata.

## 1. Public Upstream URL

Question:

What public canonical repository URL should Google Fonts use for Virtua
Grotesk?

Current placeholder:

```text
https://github.com/eliheuer/virtua-grotesk
```

Current local evidence:

- Origin-derived candidate:
  `https://github.com/eliheuer/virtua-grotesk`
- Replacement surface and preview:
  `documentation/public-upstream-readiness.md`

Why it matters:

- Used in the `OFL.txt` first line and generated name ID 0.
- Used in downstream `METADATA.pb` `source.repository_url`.
- Used in the Google Fonts issue and PR text.
- Packager fetches source files from this URL; the final URL and branch must
  contain the files listed in downstream `METADATA.pb`.

## 2. Packager Source Strategy

Question:

How should Google Fonts Packager access the files listed in downstream
`METADATA.pb` `source.files`, especially
`fonts/variable/VirtuaGrotesk[wght].ttf`?

Options:

| Strategy | What changes upstream | Packager mode |
| --- | --- | --- |
| Commit built fonts | Track generated `fonts/` binaries in the public repo. | Default branch fetch |
| Release/archive assets | Keep `fonts/` generated locally, but publish the expected files in a release archive. | `--latest-release` or archive metadata |
| Build from source | Keep binaries generated, and have Packager build from public source files. | `--build-from-source` |

Current local evidence:

- `documentation/package-source-files-audit.md` currently reports
  `source.files` as 1/4 tracked, with 3 untracked local entries.
- The served variable TTF exists locally, but is ignored/generated and not
  tracked by git.
- `documentation/ARTICLE.en_us.html` and
  `documentation/readme-specimen.png` exist locally, but are not tracked by git.
- Build-from-source inputs are 4/6 tracked; `sources/config.yaml` and
  `requirements.txt` exist locally, but are not tracked by git.
- Default branch mode cannot be final until every listed `source_file` is
  available from the public branch/commit recorded in downstream metadata.
- Build-from-source mode cannot be final until every build input is public and
  tracked, and Google Fonts accepts this family using `source.config_yaml`.
- `documentation/recent-google-fonts-packages.md` compares recent merged
  Google Fonts packages and their cited upstream repos. All three sampled
  upstream repos expose built fonts under `fonts/`, including
  `fonts/variable/`; Virtua currently generates the variable font locally but
  keeps it ignored.
- The same recent-package comparison shows Estedad as the closest Arabic-script
  example: its downstream package keeps `primary_script: "Arab"` and records
  `source.config_yaml`, supporting build-from-source only as a deliberate
  source-strategy choice.

Recommended answer:

Selected answer: use the release/archive strategy for the first submission.
Keep generated fonts out of the public branch, create a GitHub release/archive
for the final source state, and run Packager with
`GFT_PACKAGER_SOURCE_MODE=latest-release`. Omit `source.config_yaml` for this
path unless Google Fonts review asks for build metadata.

Default public-branch packaging remains a fallback only if generated binaries
are intentionally exposed from the public branch. Build-from-source remains a
separate review choice because it requires all build inputs to be public/tracked
and Google Fonts to accept `source.config_yaml` for this family.

Why it matters:

- `build.sh` deletes and recreates `fonts/` to avoid stale binaries.
- Packager can use upstream files or release assets, depending on the final
  source strategy.
- `documentation/package-source-files-audit.md` currently shows that the served
  variable TTF exists locally but is ignored/generated.
- The same audit currently shows `source.files` as 1/4 tracked and
  build-from-source inputs as 4/6 tracked, so either final source strategy must
  commit, publish, or otherwise expose the untracked local inputs before
  packaging.
- Recent merged upstream repos in `documentation/recent-google-fonts-packages.md`
  expose built fonts in `fonts/`, so generated-font handling is not just a local
  cleanup detail; it determines whether Packager can reproduce the recent
  package pattern.
- The latest dry run proved the current placeholder URL is not enough:
  Packager could not fetch `fonts/variable/VirtuaGrotesk[wght].ttf` from
  branch `main`.

## 3. Author and Contributor Strings

Question:

What exact display strings should be used in `AUTHORS.txt`,
`CONTRIBUTORS.txt`, and downstream `METADATA.pb`?

Current placeholder:

```text
Eli Heuer
```

Why it matters:

- Google Fonts metadata needs a stable designer string.
- `AUTHORS.txt` and `CONTRIBUTORS.txt` should not ship with temporary
attribution.

## 4. Family Name, Namecheck, Trademarks, and CLA

Question:

Is `Virtua Grotesk` confirmed as the final public family name, does it pass
`namecheck.fontdata.com`, are there no trademark or Reserved Font Name
concerns, and have the copyright holders signed the Google CLA?

Current preliminary check:

A quick web search on 2026-05-22 for `"Virtua Grotesk" font`,
`"Virtua Grotesk" typeface`, and `"VirtuaGrotesk"` did not show another obvious
typeface using the same family name. This is only a project-screening note; it
is not legal or trademark clearance.

Why it matters:

- Google Fonts requires the family name to be acceptable and unambiguous.
- The current `google/fonts` Add Font issue template explicitly asks for the
  family name to be unique according to `namecheck.fontdata.com`.
- The same template asks for the app-menu family name to be definitive and to
  avoid copyright holder full names or acronyms.
- Google Fonts strongly discourages Reserved Font Names in OFL submissions.
- The Google CLA must be signed before the downstream PR can be accepted.

## 5. PUA Icon Block

Question:

Should the private-use icon block ship in the first Google Fonts submission?

Recommended answer:

Defer or remove the PUA icon block for the first submission unless there is a
clear product reason to keep it.

Current local evidence:

- `documentation/pua-scope.md` reports 23 encoded PUA codepoints in every
  built font and both active source UFOs.
- The encoded PUA set currently uses selected codepoints in U+E000 through
  U+E021, plus U+F000 through U+F003; it is not a continuous encoded range.
- The local `google/fonts` checkout shows PUA precedent in shipped packages,
  including `ScheherazadeNew` and `Kedebideri` at U+F130/U+F131, but that is
  precedent for explicit rationale, not a blanket approval.
- `documentation/glyph-reachability.md` reports 19 unique unreachable glyphs;
  those warnings are mostly Arabic helper/mark glyphs plus one source-cleanup
  glyph, not the encoded PUA glyphs.
- If the PUA block ships, the Google Fonts issue/PR should explain why private
  encoded symbols belong in the public catalog package.
- If the PUA block is deferred, remove or unencode it in both masters and
  regenerate `documentation/pua-scope.md`, `documentation/glyph-reachability.md`,
  and `documentation/fontspector-warnings.md`.

Why it matters:

- The current generated report, `documentation/pua-scope.md`, records 23 currently encoded PUA codepoints in the built variable font.
- PUA glyphs complicate subsetting and reachability review.
- If kept, they need an explicit rationale in the Google Fonts issue/PR.

## 6. Vendor ID

Question:

Should Virtua Grotesk use a registered four-character vendor ID now, or leave
`NONE` until one is registered?

Recommended answer:

Register and use a real four-character vendor ID before the first Google Fonts
PR if the family/foundry identity is settled.

Why it matters:

- Fontspector currently reports `googlefonts/vendor_id`.
- A real vendor ID removes one warning across every generated font.

## 7. Kerning Scope

Question:

Should kerning be completed before the first Google Fonts PR?

Recommended answer:

Yes, if this is intended as a polished first public submission. If not, record
the deferral explicitly in the Google Fonts issue.

Current local evidence:

- `documentation/kerning-readiness.md` reports source kerning in Bold only:
  Regular has no `kerning.plist`; Bold has 77 pairs, 46 left groups, and 43
  right groups.
- The generated variable font exposes a GPOS `kern` feature.
- The generated static TTFs do not expose GPOS `kern`.
- Fontspector currently reports 4 `gpos_kerning_info` warnings.
- `make kerning-proof-check` runs Google Fonts `gftools qa --proof` and the
  latest HTML proof output covers Regular, Medium, SemiBold, and Bold.
- If kerning is completed now, source kerning needs to be compatible across
  masters and generated variable/static fonts should expose GPOS `kern`.
- If kerning is deferred, the deferral should be explicit in
  `documentation/google-fonts-decisions.md`, the Add Font issue, and the
  submission handoff, and the generated `gftools qa --proof` output should
  still be reviewed as the visual spacing/kerning proof.

Why it matters:

- Fontspector reports `gpos_kerning_info`.
- The generated variable font exposes GPOS `kern`, but the generated static
  TTFs do not.
- The Regular UFO has no source kerning yet, while the Bold UFO has source
  kerning data.
- Google Fonts visual spacing/kerning review is tracked through
  `make kerning-proof-check` and `documentation/kerning-readiness.md`.

## 8. Copyright Authorship and AI Disclosure

Question:

Can the Google Fonts issue truthfully state that the entire font project is
available under the OFL, that the listed copyright author or authors control the
project rights, and whether AI tools were used in creating the project?

Recommended answer:

Confirm the exact copyright-author statement and add a short AI-use disclosure
to the Google Fonts issue text, even if the disclosure is simply that no AI
tools were used for glyph design. The current Add Font template combines these
into one checkbox, so answer them as one maintainer-approved statement.

Why it matters:

- The current `google/fonts` Add Font issue template asks submitters to confirm
  that they are the sole copyright author, or that all other copyright authors
  have licensed their work under the OFL.
- The same template now asks submitters to clearly disclose whether AI tools
  were used in creating the project.
- This is separate from visual drawing readiness; it is a submission/legal
  representation that should come from the maintainer.
