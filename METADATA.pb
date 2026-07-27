# PLACEHOLDER metadata — drafted 2026-07-26 from the project blog.
# Validate / regenerate with `gftools packager` at submission time; the
# date_added, subsets, and instance list should be confirmed by the GF tooling.
name: "Virtua Grotesk"
designer: "Eli Heuer"
license: "OFL"
category: "SANS_SERIF"
date_added: "2026-07-26"
fonts {
  name: "Virtua Grotesk"
  style: "normal"
  weight: 400
  filename: "VirtuaGrotesk[wght].ttf"
  post_script_name: "VirtuaGrotesk-Regular"
  full_name: "Virtua Grotesk Regular"
  copyright: "Copyright 2025 The Virtua Grotesk Project Authors (https://github.com/eliheuer/virtua-grotesk)"
}
subsets: "menu"
subsets: "latin"
subsets: "latin-ext"
axes {
  tag: "wght"
  min_value: 400
  max_value: 700
}
source {
  repository_url: "https://github.com/eliheuer/virtua-grotesk"
  branch: "main"
  config_yaml: "sources/config.yaml"
  archive_url: ""
}
primary_script: "Latn"
