# Google Fonts Downstream Package Preview

This preview describes the expected downstream `google/fonts` package after
drawing work, QA, and open decisions are resolved. It is not a generated package
and should not replace a `gftools packager` run; it is the review target for
the first local packaging pass.

Current dry-run status, 2026-05-24: Packager has been wired to the local fork at
`$GF_REPO_PATH`, but cannot complete the download/copy pass until
the final GitHub release archive exposes the files listed in `source.files`,
especially the served variable font. The chosen source strategy is
release/archive packaging; the local wrapper should use
`GFT_PACKAGER_SOURCE_MODE=latest-release`.

## Expected downstream path

```text
ofl/virtuagrotesk
```

## Expected files

Variable-font-first package:

```text
ofl/virtuagrotesk/METADATA.pb
ofl/virtuagrotesk/OFL.txt
ofl/virtuagrotesk/VirtuaGrotesk[wght].ttf
ofl/virtuagrotesk/article/ARTICLE.en_us.html
ofl/virtuagrotesk/article/readme-specimen.png
```

Include static TTFs only if Google Fonts asks for them in the downstream
package. The upstream build still generates static TTFs for local QA, proofs,
and release review.

The Article image is stored at `documentation/assets/readme-specimen.png` and documented in
`documentation/assets/image-license.txt`. Copy it alongside `ARTICLE.en_us.html` if
the final package uses the Article flow.

Legacy description fallback:

```text
ofl/virtuagrotesk/DESCRIPTION.en_us.html
```

Use the legacy description only if Google Fonts review asks for it instead of
the Article flow.

Optional provenance note:

```text
ofl/virtuagrotesk/upstream.yaml
ofl/virtuagrotesk/upstream_info.md
```

The current Google Fonts repository guide documents `upstream.yaml` as the
downstream file Packager uses to link packaged fonts back to upstream for
future upgrades. Review it if Packager emits it. Some older/current
`google/fonts` directories also include `upstream_info.md` as a human-readable
provenance record; treat that file as optional unless Google Fonts review asks
for it.

## Expected METADATA.pb shape

```text
name: "Virtua Grotesk"
designer: "Eli Heuer"
license: "OFL"
category: "SANS_SERIF"
date_added: "Pending final Google Fonts date_added"
fonts {
  name: "Virtua Grotesk"
  style: "normal"
  weight: 400
  filename: "VirtuaGrotesk[wght].ttf"
  post_script_name: "VirtuaGrotesk-Regular"
  full_name: "Virtua Grotesk Regular"
  copyright: "Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)"
}
subsets: "arabic"
subsets: "latin"
subsets: "menu"
axes {
  tag: "wght"
  min_value: 400.0
  max_value: 700.0
}
source {
  repository_url: "https://github.com/eliheuer/virtua-grotesk"
  commit: "Pending final release/source commit"
  archive_url: "https://github.com/eliheuer/virtua-grotesk/releases/download/v1.000/VirtuaGrotesk-1.000.zip"
  files {
    source_file: "OFL.txt"
    dest_file: "OFL.txt"
  }
  files {
    source_file: "fonts/variable/VirtuaGrotesk[wght].ttf"
    dest_file: "VirtuaGrotesk[wght].ttf"
  }
  files {
    source_file: "documentation/google-fonts/ARTICLE.en_us.html"
    dest_file: "article/ARTICLE.en_us.html"
  }
  files {
    source_file: "documentation/assets/readme-specimen.png"
    dest_file: "article/readme-specimen.png"
  }
  branch: "main"
}
primary_script: "Arab"
stroke: "SANS_SERIF"
```

Do not add a `tags` field to this `METADATA.pb` preview unless Google Fonts
changes the metadata schema or Packager generates one. The current metadata
guide documents `category`, `stroke`, and optional `classifications`; recent PR
checklists treat new-font tags as a PR/release-review item.
Omit `source.config_yaml` for the chosen release/archive path unless Google
Fonts review asks for build metadata. Recent `google/fonts` commits removed
`config_yaml` fields that pointed at non-buildable or misleading configs, and
release/archive examples such as Scheherazade New, Amiri, and Kedebideri fetch
prebuilt files from `source.archive_url` without `source.config_yaml`.
For `GFT_PACKAGER_SOURCE_MODE=latest-release`, keep the final GitHub release
`archive_url` in the `source` block before applying this preview into the local
`google/fonts` fork.
Do not add custom `sample_text` unless Google Fonts review asks for it or the
default Arabic specimen text is unsuitable; `sample_text` is a catalog specimen
override, not a proofing substitute.

## Review checks

- Confirm `source.repository_url` matches `OFL.txt`, source UFO metadata, and
  `documentation/google-fonts/ARTICLE.en_us.html`.
- Replace the pending commit and final `date_added` value before opening the
  downstream PR.
- Confirm the `axes` min/max values match `documentation/google-fonts/variable-font-metadata.md`.
  The built font's default `wght=400` is reviewed in `fvar`; recent
  `google/fonts` variable metadata examples do not add a `default_value` field.
- Confirm final subsets after drawing: `arabic`, `latin`, and `menu`. Add
  `latin-ext` only after the font supports enough of that broad Google Fonts
  subset to avoid an unsupported-subset warning.
- Confirm `documentation/google-fonts/google-fonts-language-metadata.md` still finds the
  local `google/fonts` Arabic script record, Arabic Core language records, and
  recent Arabic packages using `primary_script: "Arab"`.
- Confirm Article image assets referenced by `ARTICLE.en_us.html` are present
  in `ofl/virtuagrotesk/article/` and meet Google Fonts image-size limits.
- Confirm the `source.files` mapping includes `OFL.txt`, the served variable
  font, `article/ARTICLE.en_us.html`, and every referenced Article image.
- Confirm `documentation/google-fonts/package-source-files-audit.md` agrees with the final
  source strategy, especially for generated font binaries.
- Confirm `source.config_yaml` is absent for the chosen release/archive source
  mode unless Google Fonts review asks for build metadata.
- Confirm `source.archive_url` points at the final public GitHub release
  archive.
- Keep `primary_script: "Arab"` while Arabic is the primary non-Latin support
  target.
- Confirm whether `vietnamese` or another subset appears after final Latin
  coverage; include only subsets supported by the built font.
- Confirm whether static TTF entries are omitted or included, based on Google
  Fonts reviewer guidance.
- Confirm new-font tags are handled in the linked issue or PR review checklist,
  not inserted into `METADATA.pb` unless generated by Google Fonts tooling.
- Confirm no custom `sample_text` block is present unless the need is recorded
  in `documentation/google-fonts/google-fonts-decisions.md`.
- Confirm the linked Google Fonts issue and PR have the Arabic/RTL script label.
- Confirm the downstream PR body cites the public upstream repository and exact
  commit.
- If Packager emits `upstream.yaml`, confirm it maps the final upstream archive,
  branch, and source files to the downstream package files.
- If Google Fonts asks for `upstream_info.md`, confirm it records the canonical
  repository URL, source commit, branch, config path, and binary provenance.

## References

- https://googlefonts.github.io/gf-guide/metadata.html
- https://googlefonts.github.io/gf-guide/package.html
- https://googlefonts.github.io/gf-guide/making-pr.html
- https://github.com/google/fonts/pull/10401
- https://github.com/google/fonts/pull/10546
