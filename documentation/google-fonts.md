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
| Build | `make build` (`scripts/build.sh` with `sources/config.yaml`) |
| QA | `make qa-full` (full Fontspector profile), `make qa-package PACKAGE=<directory>` |
| About text | `documentation/article/ARTICLE.en_us.html` |
| AI use | Disclosed in the README and the article. Eli draws and approves the glyphs. |

## Open decisions

- Cyrillic: requested on 2026-10-21 for Rubik-level coverage. It is not in
  the current scope.
- Italic: not in the first release, unless Eli decides otherwise.
- README image: commit an image under `documentation/` in place of the
  external URL.
- Release tag: none yet.

## Before the Add Font issue

1. Every glyph is green in both masters (`make status`).
2. `make qa-full` reports no FAIL that applies to this repository.
3. The copyright holders have signed the Google CLA.
4. Search the existing issues, then open the Add Font issue from its template.

For an agent, the full procedure is the task contract
[`.agents/tasks/google-fonts-release.md`](../.agents/tasks/google-fonts-release.md).

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
| Project template | https://github.com/googlefonts/googlefonts-project-template |
| Add Font issue template | https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md |
| Google Fonts repository | https://github.com/google/fonts |
| Fontspector | https://github.com/fonttools/fontspector |
| gftools (builder, packager) | https://github.com/googlefonts/gftools |
| Glyph sets | https://github.com/googlefonts/glyphsets |
| Contributor License Agreement | https://cla.developers.google.com/ |
