# Google Fonts Template and Recent PR Audit

This audit records the extra comparison pass against the official Google Fonts
project template and recently merged `google/fonts` pull requests. It keeps the
upstream repo aligned with current practice without blindly copying optional
template automation.

The generated companion report
`documentation/google-fonts/recent-google-fonts-packages.md` reads the selected downstream
family directories from the local `google/fonts` fork so these recent-package
patterns can be refreshed with `make reports-only`. It also derives a current
`gftools_packager_ofl_*` merge list from the local `google/fonts` first-parent
history, so this audit can distinguish detailed package examples from the
latest local merge evidence.

## Official project template

Evidence sources:

- `googlefonts/googlefonts-project-template`
- Google Fonts upstream repository structure guide
- generated local comparison in `documentation/google-fonts/recent-google-fonts-packages.md`

The template and guide agree on the required upstream shape:

- `AUTHORS.txt`
- `CONTRIBUTORS.txt`
- `OFL.txt`
- `README.md`
- `documentation/`
- `sources/`
- `requirements.txt`
- `.gitignore`
- a one-command build path through `sources/config.yaml` and/or `build.sh`

The current template root also includes `.github/`, `.templaterc.json`,
`renovate.json`, `scripts/`, and Make targets for template customization,
template updates, dependency updates, images, proofing, and GitHub
Actions/GitHub Pages publication. Those are template conveniences rather than
minimum upstream requirements.

Virtua Grotesk now has each required artifact. The repo does not copy the
template wholesale because this project already has UFO/designspace sources,
DrawBot proofing, DesignBot specimens, and local readiness reports that need a
more specific workflow.
The canonical builder config now lives at `sources/config.yaml`, matching the
template convention where source paths are relative to the `sources/`
directory.

Template features not added yet:

- GitHub Actions build/proof/report publishing.
- GitHub Pages publishing of proof and QA output.
- Automated release bundle publishing.
- Renovate dependency-update configuration.
- `.templaterc.json` plus `make update-project-template` / `npx
  update-template` maintenance flow.

Those are useful but optional. The upstream guide says the project template
automations are not mandatory; the required part is the public upstream
structure and reproducible build. The maintainer decision for the first
submission is to defer CI, Pages, Renovate, and template-maintenance
automation; that decision is tracked in
`documentation/google-fonts/google-fonts-decisions.md` and summarized in
`documentation/google-fonts/project-template-automation-readiness.md`.
If CI is adopted, adapt it to this repo's current Fontspector-based `make test`
gate instead of copying the older FontBakery-oriented template workflow.
The live project-template README and the GF guide's upstream-structure page
still describe FontBakery in their older prose about template automations, so
use the current QA guide and local `google/fonts` workflow evidence when
choosing QA tooling.

Current local equivalent:

- `make build` builds the variable and static TTFs.
- `make test` runs Fontspector's `googlefonts` profile.
- `make reports` regenerates local audit reports.
- `make preflight` checks the repo while allowing only documented
  drawing/source blockers, after rebuilding, regenerating the PDF proof, and
  regenerating reports from that proof evidence.
- `make handoff` uses the same proof-before-report path for final handoff
  review.

## Recent merged `google/fonts` PRs

The detailed package evidence is generated from the local `google/fonts`
checkout in `documentation/google-fonts/recent-google-fonts-packages.md`. Refresh that
report with `make reports-only` after syncing `/Users/eli/GH/forks/fonts`.

Recent merged new-font examples:

| PR | Family | Merged | Relevant pattern |
| --- | --- | --- | --- |
| `google/fonts#10546` | Pliant | 2026-05-22 | Downstream package includes variable TTFs, `METADATA.pb`, `OFL.txt`, and `article/` content. PR body cites upstream repo and exact commit. |
| `google/fonts#10455` | Scheherazade New | 2026-05-01 | Arabic package uses `primary_script: "Arab"` and a GitHub release download `.zip` in `source.archive_url`, matching Virtua's selected release/archive source strategy. |
| `google/fonts#10468` | Akt | 2026-04-29 | Downstream package includes a variable TTF, `METADATA.pb`, `OFL.txt`, and `article/` content. PR body cites upstream repo and exact commit. |
| `google/fonts#10401` | Estedad | 2026-04-16 | Arabic new-font package includes `primary_script: "Arab"`, `subsets: "arabic"`, source commit, `config_yaml`, and `article/` content. |

Recent `google/fonts` source-metadata cleanup also matters for Virtua Grotesk:
commits in May 2026 removed `config_yaml` fields that pointed at non-buildable
or misleading configs. Keep Virtua's downstream `source.config_yaml` only if
the final package uses a reproducible build-from-source strategy through
`sources/config.yaml`; omit it for default branch or release/archive packaging
unless Google Fonts review asks for build metadata.

Local `google/fonts` audit note: the current Google Fonts repository guide
documents `upstream.yaml` as the Packager-linked downstream upgrade file, while
many family directories also contain older human-readable `upstream_info.md`
provenance notes. Recent Pliant and Akt packages do not include
`upstream_info.md`; keep that file optional for Virtua Grotesk unless Google
Fonts review asks for it.
Regenerate `documentation/google-fonts/recent-google-fonts-packages.md` after updating the
local `google/fonts` fork to refresh the exact downstream package evidence.

The current PR checklist pattern also expects:

- Traffic Jam Board placement.
- Correct labels, including language/script labels.
- A linked Google Fonts issue.
- Fontspector checks reviewed with upstream.
- OFL license URL checked.
- `primary_script` for primary non-Latin support.
- subset definitions matching actual font support, alphabetized where possible.
- designer catalog/bio tracking and designer order review.
- `tags` for new fonts.

Virtua Grotesk implications:

- The downstream PR should cite the public upstream repository and exact commit.
- Because Arabic is in first-submission scope, request/review the
  `II Arabic / Hebrew / Semitic / RTL` label and keep `primary_script: "Arab"`
  in `METADATA.pb` unless Google Fonts review requests otherwise.
- For the selected `latest-release` strategy, mirror the Scheherazade New
  downstream pattern: `source.archive_url` points at a final GitHub release
  download `.zip`, `source.config_yaml` is omitted, and every `source.files`
  entry resolves inside the release archive.
- Expected first-submission subsets are `arabic`, `latin`, and `menu` after
  drawing coverage is complete. Add `latin-ext` only after enough coverage
  exists to serve that broader subset cleanly.
- The metadata review needs explicit designer order and designer-profile
  tracking, even for a single-designer project.
- Treat new-font `tags` as an issue/PR review item, not a `METADATA.pb` field,
  unless Google Fonts tooling generates schema support for it. Recent Pliant
  and Estedad metadata packages include `category`/`stroke` fields but no
  `tags` field.
- The Article flow is the decided first-submission path. The guide says
  non-Noto families can use an expanded `article/ARTICLE.en_us.html`; recent
  new-font PRs commonly do. Use `documentation/google-fonts/ARTICLE.en_us.html` as the
  upstream draft and map it into downstream `article/ARTICLE.en_us.html`.
- The final downstream PR should be created from `gftools packager`, reviewed
  locally first, and only pushed after the linked issue and final QA are ready.
- If Packager emits `upstream.yaml`, review it against the final upstream
  release/source strategy before opening or updating the downstream PR.
- If `upstream_info.md` is requested, make it match the `METADATA.pb`
  `source { ... }` repository, commit, branch, and config path rather than
  treating it as a separate source of truth.
- Recent merged PR evidence confirms that current downstream review is using
  FontSpector reports in practice. For example, `google/fonts#10468` includes a
  GitHub Actions `FontSpector report` with `fontspector version: 1.6.0`. Keep
  this repo's `make test` path on Fontspector even when older guide/template
  text still mentions FontBakery-era automation.

## References

- https://googlefonts.github.io/gf-guide/upstream.html
- https://googlefonts.github.io/gf-guide/article.html
- https://googlefonts.github.io/gf-guide/making-pr.html
- https://googlefonts.github.io/gf-guide/package.html
- https://github.com/googlefonts/googlefonts-project-template
- https://github.com/google/fonts/pull/10546
- https://github.com/google/fonts/pull/10468
- https://github.com/google/fonts/pull/10401
