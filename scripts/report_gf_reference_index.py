#!/usr/bin/env python3
"""Generate a Google Fonts reference-to-local-evidence index."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/google-fonts-reference-index.md")

REFERENCES = [
    {
        "source": "Adding & Upgrading Fonts to Google Fonts",
        "url": "https://googlefonts.github.io/gf-guide/onboarding.html",
        "local": [
            "documentation/google-fonts/google-fonts-add-font-issue-draft.md",
            "documentation/google-fonts/google-fonts-production-requirements.md",
            "documentation/google-fonts/final-submission-blockers.md",
        ],
        "use": "tracks issue-first submission, OFL, public repo, source, TTF, glyphset, and QA requirements",
    },
    {
        "source": "Upstream repository structure",
        "url": "https://googlefonts.github.io/gf-guide/upstream.html",
        "local": [
            "documentation/google-fonts/upstream-structure-readiness.md",
            "documentation/google-fonts/package-source-files-audit.md",
            "documentation/google-fonts/project-template-automation-readiness.md",
        ],
        "use": "checks mandatory upstream paths, source/build layout, public repo shape, and project-template deltas",
    },
    {
        "source": "Overall font files requirements",
        "url": "https://googlefonts.github.io/gf-guide/requirements.html",
        "local": [
            "documentation/google-fonts/google-fonts-production-requirements.md",
            "documentation/google-fonts/missing-gf-latin-core.md",
            "documentation/google-fonts/missing-gf-arabic-core.md",
            "documentation/google-fonts/numeric-feature-readiness.md",
        ],
        "use": "tracks family naming, embedding, glyphset coverage, OpenType feature expectations, and required shared glyphs",
    },
    {
        "source": "Production requirements",
        "url": "https://googlefonts.github.io/gf-guide/production.html",
        "local": [
            "documentation/google-fonts/google-fonts-production-requirements.md",
            "documentation/core-qa-process.md",
            "documentation/google-fonts/numeric-feature-readiness.md",
        ],
        "use": "keeps scalable-font production, local QA, and web-serving assumptions visible before final submission",
    },
    {
        "source": "Variable fonts specifics",
        "url": "https://googlefonts.github.io/gf-guide/variable.html",
        "local": [
            "documentation/google-fonts/variable-font-metadata.md",
            "documentation/google-fonts/avar-readiness.md",
            "documentation/google-fonts/google-fonts-axis-registry-audit.md",
            "documentation/google-fonts/google-fonts-production-requirements.md",
        ],
        "use": "checks the wght axis, fvar/static instance expectations, avar warning state, and axis registry alignment",
    },
    {
        "source": "Build the fonts",
        "url": "https://googlefonts.github.io/gf-guide/build.html",
        "local": [
            "sources/config.yaml",
            "documentation/google-fonts/upstream-structure-readiness.md",
            "documentation/google-fonts/packager-source-strategy.md",
            "documentation/google-fonts/google-fonts-production-requirements.md",
        ],
        "use": "anchors the gftools builder config, build-from-source fallback, and public build-input review",
    },
    {
        "source": "Package the fonts",
        "url": "https://googlefonts.github.io/gf-guide/package.html",
        "local": [
            "documentation/google-fonts/package-dry-run-readiness.md",
            "documentation/google-fonts/packager-source-strategy.md",
            "documentation/google-fonts/downstream-metadata-diff.md",
            "documentation/google-fonts/downstream-pr-readiness.md",
        ],
        "use": "maps Packager source modes, no-PR dry-run flow, downstream branch naming, and source.files/archive strategy",
    },
    {
        "source": "METADATA file",
        "url": "https://googlefonts.github.io/gf-guide/metadata.html",
        "local": [
            "documentation/google-fonts/google-fonts-downstream-package-preview.md",
            "documentation/google-fonts/downstream-metadata-readiness.md",
            "documentation/google-fonts/downstream-metadata-diff.md",
            "documentation/google-fonts/generated-font-metadata.md",
        ],
        "use": "validates family metadata, variable font records, subsets, primary_script, source block, and final pending fields",
    },
    {
        "source": "Article file",
        "url": "https://googlefonts.github.io/gf-guide/article.html",
        "local": [
            "documentation/google-fonts/article-readiness.md",
            "documentation/google-fonts/google-fonts-metadata-review.md",
            "documentation/google-fonts/google-fonts-package-checklist.md",
            "documentation/google-fonts/google-fonts-template-and-pr-audit.md",
        ],
        "use": "checks ARTICLE.en_us.html, image/license assets, downstream article mapping, and package checklist wording",
    },
    {
        "source": "Lang Metadata System",
        "url": "https://googlefonts.github.io/gf-guide/lang.html",
        "local": [
            "documentation/google-fonts/google-fonts-language-metadata.md",
            "documentation/glyph-review/arabic-review-packet.md",
            "documentation/google-fonts/missing-gf-arabic-core.md",
        ],
        "use": "ties Arabic script metadata, primary_script, subsets, and GF Arabic Core coverage evidence together",
    },
    {
        "source": "Making a PR to Google Fonts",
        "url": "https://googlefonts.github.io/gf-guide/making-pr.html",
        "local": [
            "documentation/google-fonts/pr-identity-readiness.md",
            "documentation/google-fonts/downstream-pr-readiness.md",
            "documentation/google-fonts/google-fonts-submission-handoff.md",
        ],
        "use": "keeps issue-first rule, CLA/git identity, one-family-directory scope, PR title, and provenance body aligned",
    },
    {
        "source": "Tools and Dependencies",
        "url": "https://googlefonts.github.io/gf-guide/tools.html",
        "local": [
            "documentation/python-tooling-notes.md",
            "documentation/google-fonts/local-workflow-readiness.md",
            "documentation/core-qa-process.md",
        ],
        "use": "documents the local venv, gftools, Fontspector, gftools QA, and reproducible command assumptions",
    },
    {
        "source": "Onboarder workflow guide",
        "url": "https://googlefonts.github.io/gf-guide/onboarder-workflow.html",
        "local": [
            "documentation/google-fonts/submission-handoff-readiness.md",
            "documentation/google-fonts/kerning-proof-review.md",
            "documentation/google-fonts/next-actions.md",
        ],
        "use": "keeps generated QA/proof review, Traffic Jam/PR workflow notes, and handoff status visible",
    },
    {
        "source": "google/fonts repository explained",
        "url": "https://googlefonts.github.io/gf-guide/googlefonts.html",
        "local": [
            "documentation/google-fonts/google-fonts-language-metadata.md",
            "documentation/google-fonts/designer-profile-readiness.md",
            "documentation/google-fonts/packager-source-strategy.md",
            "documentation/google-fonts/downstream-pr-readiness.md",
        ],
        "use": "maps downstream family directories, designer catalog files, lang metadata, and upstream.yaml expectations",
    },
    {
        "source": "Designer profile guide",
        "url": "https://googlefonts.github.io/gf-guide/profile.html",
        "local": [
            "documentation/google-fonts/designer-profile-readiness.md",
            "documentation/google-fonts/designer-profile-package-draft.md",
            "documentation/google-fonts/designer-profile-candidate/info.pb",
            "documentation/google-fonts/designer-profile-candidate/bio.html",
        ],
        "use": "tracks designer profile slug, info.pb, bio.html, avatar filename, profile request route, and pending approvals",
    },
    {
        "source": "google/fonts Add Font issue template",
        "url": "https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
        "local": [
            "documentation/google-fonts/google-fonts-add-font-template-audit.md",
            "documentation/google-fonts/google-fonts-add-font-issue-draft.md",
            "documentation/google-fonts/submission-handoff-readiness.md",
        ],
        "use": "keeps labels, requirement checkboxes, maintenance commitment, and issue text synced with the current template",
    },
    {
        "source": "googlefonts/gftools",
        "url": "https://github.com/googlefonts/gftools",
        "local": [
            "Makefile",
            "scripts/package_gf_dry_run.sh",
            "scripts/check_gf_fonts.sh",
            "documentation/google-fonts/kerning-proof-review.md",
        ],
        "use": "anchors local builder, packager, Fontspector, and gftools QA proof commands to the current toolchain",
    },
]


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def markdown_report() -> str:
    lines = [
        "# Google Fonts Reference Index",
        "",
        "This generated index maps official Google Fonts documentation and",
        "Google Fonts GitHub references to the local reports and gates used for",
        "Virtua Grotesk onboarding. Use it as the audit map before changing",
        "handoff, metadata, package, QA, or designer-profile workflows.",
        "",
        "## Summary",
        "",
        f"- References tracked: {len(REFERENCES)}",
        f"- References with local evidence: {sum(1 for item in REFERENCES if item['local'])} / {len(REFERENCES)}",
        "- Official-doc references only: yes",
        "- Google Fonts GitHub references included: yes",
        "",
        "## Reference Map",
        "",
        "| Source | URL | Local evidence | Current local use |",
        "| --- | --- | --- | --- |",
    ]

    for item in REFERENCES:
        local = "<br>".join(f"`{path}`" for path in item["local"])
        lines.append(f"| {item['source']} | {item['url']} | {local} | {item['use']} |")

    lines.extend(
        [
            "",
            "## Local Evidence Files",
            "",
            "| Local evidence | Exists | Referenced by |",
            "| --- | --- | --- |",
        ]
    )
    all_paths = sorted({path for item in REFERENCES for path in item["local"]})
    for path in all_paths:
        sources = ", ".join(item["source"] for item in REFERENCES if path in item["local"])
        lines.append(f"| `{path}` | {yes_no((ROOT / path).exists())} | {sources} |")

    lines.extend(
        [
            "",
            "## Maintenance Policy",
            "",
            "- Update this index when a local gate starts relying on a new Google",
            "  Fonts guide page, Google Fonts repository file, or gftools behavior.",
            "- Keep generated readiness reports linked here instead of relying on",
            "  memory of prior onboarding work.",
            "- Rerun `make preflight` after changing this index so the reference map",
            "  stays synchronized with the rest of the handoff evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_gf_reference_index.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
