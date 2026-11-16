# Google Fonts release

The Google Fonts requirements change over time. This file holds only the
facts of this project and the open decisions. For each requirement, read the
current official page.

## Project facts

| Item | Value |
| --- | --- |
| Family name | Virtua Grotesk |
| Upstream repository | https://github.com/eliheuer/virtua-grotesk |
| Scripts in the first release | Latin, Arabic, Hebrew |
| Styles | Upright only. Weight axis `wght` 400 to 700. Instances Regular, Medium, SemiBold, Bold. |
| License | SIL Open Font License 1.1 (`OFL.txt`) |
| Build | `make build` (`fgtools build` with `sources/config.yaml`, then `scripts/fix_gf_metadata.py`) |
| QA | `fgtools qa --full` (full Fontspector profile), `fgtools qa --package <directory>` |
| About text | `documentation/article/ARTICLE.en_us.html` |
| AI use | Disclosed in the README and the article. Eli draws and approves the glyphs. |

## Open decisions

- Cyrillic: requested on 2026-10-21 for Rubik-level coverage. It is not in
  the current scope.
- Italic: not in the first release, unless Eli decides otherwise.
- README image: commit an image under `documentation/` in place of the
  external URL.
- Release tag: none yet.

## Build

`make build` runs `fgtools build`, which builds one variable TTF and four
static TTFs with `gftools builder` and fontc. Then
`scripts/fix_gf_metadata.py` applies three fixes that have no source setting.
A plain `gftools builder sources/config.yaml`, as the Google Fonts packager
runs it, builds the same fonts with fontmake, without those fixes.
`fgtools diff --fontmake` checks that fontc and fontmake give the same glyph
and word images.

## QA

| Command | Use |
| --- | --- |
| `make qa` | Development profile, offline, without the checks in `[qa.exclude]` of `CONTEXT.md`. The CI gate. |
| `fgtools qa --full` | Full profile with network checks and no exclusions. |
| `fgtools qa --package <directory>` | Full profile on a package with `METADATA.pb`, `OFL.txt` and the article. |

The profile is the Google Fonts profile plus the Font.Garden requirements: a
1024-unit em, masters on the 2-unit grid, the vendor ID FTGD and the OFL 1.1.
The reports are in `output/qa/<mode>/`. Read the JSON report, and count unique
findings, not one finding for each font. A FAIL needs a fix or an exception
that Eli approves. A WARN needs a decision by Eli. Outline warnings are
listed for Eli by glyph name and are not corrected. Do not add exclusions,
remove cmap entries or reduce the script scope to get a cleaner result.

Coverage and table presence do not prove shaping. Look at mark attachment,
joining, right-to-left and mixed text, spacing and the intermediate weights
in a rendered proof.

## Package

1. Work in a directory under `output/`. Copy the reviewed TTFs and `OFL.txt`
   into `ofl/virtuagrotesk/` and run `gftools add-font` on it.
2. Copy `documentation/article/ARTICLE.en_us.html` and its image to
   `article/`. `weight-specimen.rs` renders the image with DesignBot.
3. Check the generated metadata: names, designer, category, axes, subsets,
   primary script, date and source. Keep the Arabic and Hebrew subsets even
   if the subset detection leaves one out.
4. Run `fgtools qa --package <directory>`.

Read `gftools packager --help` before you use it. Some of its modes commit,
push or open a pull request. Use only a local preview unless Eli authorizes
publication.

## Before the Add Font issue

1. Every glyph is green in both masters (`make status`).
2. `fgtools qa --full` reports no FAIL, except
   `googlefonts/repo/dirname_matches_nameid_1`, which applies to the
   google/fonts package directory and not to this repository.
3. The copyright holders have signed the Google CLA.
4. Search the existing issues, then draft the Add Font issue from its
   template. Leave the copyright, CLA and image-license attestations
   unchecked: only Eli can confirm them. The issue comes before a pull
   request.

Do not post, push, tag or publish without Eli's authorization. Report what
is local, drafted, submitted and published as separate states.

## Official sources

| Subject | Link |
| --- | --- |
| Guide (all chapters) | https://googlefonts.github.io/gf-guide/ |
| Upstream repository structure | https://googlefonts.github.io/gf-guide/upstream.html |
| Onboarding a new font | https://googlefonts.github.io/gf-guide/onboarding.html |
| Font file requirements | https://googlefonts.github.io/gf-guide/requirements.html |
| Variable fonts | https://googlefonts.github.io/gf-guide/variable.html |
| Outline quality | https://googlefonts.github.io/gf-guide/outlines.html |
| Diacritics | https://googlefonts.github.io/gf-guide/diacritics.html |
| QA and Fontspector | https://googlefonts.github.io/gf-guide/qa.html |
| METADATA file | https://googlefonts.github.io/gf-guide/metadata.html |
| Article | https://googlefonts.github.io/gf-guide/article.html |
| Packaging | https://googlefonts.github.io/gf-guide/package.html |
| Making a pull request | https://googlefonts.github.io/gf-guide/making-pr.html |
| Project template | https://github.com/googlefonts/googlefonts-project-template |
| Add Font issue template | https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md |
| Google Fonts repository | https://github.com/google/fonts |
| Fontspector | https://github.com/fonttools/fontspector |
| gftools (builder, packager) | https://github.com/googlefonts/gftools |
| Glyph sets | https://github.com/googlefonts/glyphsets |
| Contributor License Agreement | https://cla.developers.google.com/ |
