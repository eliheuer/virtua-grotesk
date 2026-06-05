#!/usr/bin/env python3
"""Generate a Google Fonts Add Font issue draft from current readiness data."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
TEMPLATE_RELATIVE = Path(".github/ISSUE_TEMPLATE/1_add-font.md")
OUTPUT_DEFAULT = Path("documentation/google-fonts/google-fonts-add-font-issue-draft.md")


def read_text(relative: Path | str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def ahead_behind(repo: Path, left: str, right: str) -> str:
    output = git_output(repo, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    parts = output.split()
    if len(parts) != 2:
        return "unknown"
    ahead, behind = parts
    return f"{ahead} ahead, {behind} behind"


def frontmatter_value(key: str, text: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*'?([^'\n]+)'?\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def first_line_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def first_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else default


def fontspector_fail_count(report_text: str) -> int:
    match = re.search(
        r"### Summary\s*\n(?P<header>\|[^\n]*\|)\s*\n\|[^\n]*\|\s*\n(?P<values>\|[^\n]*\|)",
        report_text,
        flags=re.MULTILINE,
    )
    if not match:
        return 0
    headers = [cell.strip() for cell in match.group("header").strip("|").split("|")]
    values = [cell.strip() for cell in match.group("values").strip("|").split("|")]
    counts = dict(zip(headers, values, strict=False))
    return int(counts.get("🔥 FAIL", 0))


def arabic_category_counts(report_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for heading in [
        "Arabic letters",
        "Arabic marks",
        "Arabic numbers",
        "Arabic punctuation and symbols",
        "Shared punctuation and symbols",
    ]:
        counts[heading] = first_int(rf"## {re.escape(heading)}\s*\n\s*Missing: (\d+)", report_text)
    return counts


def requirement_lines(template_text: str) -> list[str]:
    return [
        line.strip()[6:].strip()
        for line in template_text.splitlines()
        if line.strip().startswith("- [ ] ")
    ]


def issue_requirement_note(requirement: str, reports: dict[str, str]) -> str:
    family_name = reports["family_name"]
    upstream = reports["upstream"]
    latin = reports["latin"]
    authorship = reports["authorship"]
    pua = reports["pua"]
    fontspector_fails = fontspector_fail_count(reports["fontspector"])

    if "entire font project" in requirement:
        return "Local evidence: public canonical upstream URL is recorded."
    if "source files are available" in requirement:
        return "Blocked until the final release/archive exposes every `source.files` input."
    if "sole copyright author" in requirement:
        return (
            "Local evidence: copyright-authorship and AI-use wording is recorded."
        )
    if "Reserved Font Names" in requirement:
        rfn_status = first_line_value(r"^- OFL Reserved Font Name status: (.+)$", family_name)
        trademark_status = first_line_value(r"^- Trademark/catalog-name clearance: (.+)$", family_name)
        return f"Local evidence: {rfn_status}; trademark/catalog-name clearance: {trademark_status}."
    if "namecheck.fontdata.com" in requirement:
        status = first_line_value(r"^- Namecheck confirmation: (.+)$", family_name)
        return f"Maintainer confirmation: {status}."
    if "app menus" in requirement:
        present = first_line_value(
            r"^- App-menu family name candidate appears in built names: (yes|no)$",
            family_name,
        )
        return f"Local evidence: app-menu candidate appears in built names: {present}."
    if "Latin Core" in requirement:
        missing = first_int(r"Missing codepoints: (\d+)", latin)
        return f"Blocked by drawing/source work: GF Latin Core missing codepoints: {missing}."
    if "preferred upstream repo structure" in requirement:
        mandatory = first_line_value(r"^- Mandatory upstream paths present: (.+)$", upstream)
        return f"Local evidence: {mandatory}."
    if "contributing requirements" in requirement:
        return (
            "Blocked until documented final blockers are resolved or accepted; "
            f"{fontspector_fails} FAIL results."
        )
    if "maintain the repository" in requirement:
        return "Maintainer confirmation required before opening the issue."
    if "private-use" in requirement or "PUA" in requirement:
        return first_line_value(r"^- PUA codepoints present: (.+)$", pua)
    if "AI" in requirement:
        return first_line_value(r"^- AI-use disclosure recorded: (.+)$", authorship)
    return "Review against current generated reports before checking."


def markdown_report(gf_repo: Path) -> str:
    template_path = gf_repo / TEMPLATE_RELATIVE
    template_text = template_path.read_text(encoding="utf-8")
    title_pattern = frontmatter_value("title", template_text)
    labels = frontmatter_value("labels", template_text)
    requirements = requirement_lines(template_text)
    reports = {
        "fontspector": read_text("documentation/google-fonts/fontspector-googlefonts-report.md"),
        "family_name": read_text("documentation/google-fonts/family-name-readiness.md"),
        "upstream": read_text("documentation/google-fonts/upstream-structure-readiness.md"),
        "latin": read_text("documentation/google-fonts/missing-gf-latin-core.md"),
        "arabic": read_text("documentation/google-fonts/missing-gf-arabic-core.md"),
        "arabic_marks": read_text("documentation/glyph-review/arabic-mark-readiness.md"),
        "arabic_review": read_text("documentation/glyph-review/arabic-review-packet.md"),
        "arabic_shaping": read_text("documentation/glyph-review/arabic-shaping-smoke-test.md"),
        "numeric": read_text("documentation/google-fonts/numeric-feature-readiness.md"),
        "authorship": read_text("documentation/google-fonts/authorship-disclosure-readiness.md"),
        "designer_profile": read_text("documentation/google-fonts/designer-profile-readiness.md"),
        "designer_profile_package": read_text("documentation/google-fonts/designer-profile-package-draft.md"),
        "pua": read_text("documentation/google-fonts/pua-scope.md"),
        "vendor": read_text("documentation/google-fonts/vendor-id-readiness.md"),
        "kerning": read_text("documentation/google-fonts/kerning-readiness.md"),
        "kerning_proof_review": read_text("documentation/google-fonts/kerning-proof-review.md"),
        "avar": read_text("documentation/google-fonts/avar-readiness.md"),
        "warnings": read_text("documentation/google-fonts/fontspector-warnings.md"),
        "package_dry_run": read_text("documentation/google-fonts/package-dry-run-readiness.md"),
        "downstream_metadata_diff": read_text("documentation/google-fonts/downstream-metadata-diff.md"),
        "packager_source_strategy": read_text("documentation/google-fonts/packager-source-strategy.md"),
    }
    status = git_output(gf_repo, ["status", "--short", "--branch"]).splitlines()
    status_line = status[0] if status else "unknown"
    description = (
        "Virtua Grotesk is a variable geometric grotesk with a Weight axis "
        "and Latin plus Arabic support in preparation."
    )
    labels_line = labels or "I New Font, II Submission"
    arabic_missing = first_int(r"Missing codepoints: (\d+)", reports["arabic"])
    arabic_counts = arabic_category_counts(reports["arabic"])
    arabic_mark_missing = first_int(r"Missing from current variable-font cmap: (\d+)", reports["arabic_marks"])
    dotted_circle = first_line_value(
        r"^- U\+25CC dotted circle present: (yes|no)$",
        reports["arabic_marks"],
    )
    mark_features = first_line_value(
        r"^- Built mark/mkmk GPOS features present: (yes|no)$",
        reports["arabic_marks"],
    )
    gsub_ready_fonts = len(re.findall(r"GSUB has `arab/dflt`: `true`", reports["arabic_shaping"]))
    gpos_ready_fonts = len(re.findall(r"GPOS has `arab/dflt`: `true`", reports["arabic_shaping"]))
    numeric_default_digits = first_line_value(
        r"^- Default ASCII digits present in every built font: (yes|no)$",
        reports["numeric"],
    )
    numeric_default_proportional = first_line_value(
        r"^- Default ASCII digits are proportional in every built font: (yes|no)$",
        reports["numeric"],
    )
    numeric_tnum_feature = first_line_value(
        r"^- `tnum` feature present in every built font: (yes|no)$",
        reports["numeric"],
    )
    numeric_tnum_coverage = first_line_value(
        r"^- `tnum` substitutes all ten ASCII digits in every built font: (yes|no)$",
        reports["numeric"],
    )
    numeric_tnum_tabular = first_line_value(
        r"^- `tnum` substitutes to equal-width digits in every built font: (yes|no)$",
        reports["numeric"],
    )
    numeric_ready = first_line_value(
        r"^- Numeric feature requirement ready: (yes|no)$",
        reports["numeric"],
    )
    profile_candidates = first_int(
        r"AUTHORS catalog-credit candidates: (\d+)",
        reports["designer_profile"],
    )
    profile_missing = first_int(
        r"Candidate profiles missing: (\d+)",
        reports["designer_profile"],
    )
    metadata_final_designers = first_line_value(
        r"^- Final metadata designer strings present: (yes|no)$",
        reports["designer_profile"],
    )
    metadata_pending_placeholders = first_int(
        r"Pending metadata designer placeholders: (\d+)",
        reports["designer_profile"],
    )
    designer_string = first_line_value(
        r"^- Designer string: `([^`]+)`$",
        reports["designer_profile_package"],
    )
    designer_slug = first_line_value(
        r"^- Catalog slug: `([^`]+)`$",
        reports["designer_profile_package"],
    )
    designer_profile_dir = first_line_value(
        r"^- Downstream directory: `([^`]+)`$",
        reports["designer_profile_package"],
    )
    designer_profile_exists = first_line_value(
        r"^- Target profile directory already exists: (yes|no)$",
        reports["designer_profile_package"],
    )
    designer_profile_files = first_line_value(
        r"^- Expected profile files already present: (.+)$",
        reports["designer_profile_package"],
    )
    designer_profile_placeholders = first_int(
        r"Draft placeholders still unresolved: (\d+)",
        reports["designer_profile_package"],
    )
    source_vendor = first_line_value(r"^- Source UFO vendor IDs: `?([^`\n]+)`?$", reports["vendor"])
    generated_vendor = first_line_value(r"^- Generated font vendor IDs: `?([^`\n]+)`?$", reports["vendor"])
    vendor_warnings = first_int(r"Fontspector `googlefonts/vendor_id` warnings: (\d+)", reports["vendor"])
    vendor_decision = first_line_value(r"^- Decision log status: (.+)$", reports["vendor"])
    kerning_every_master = first_line_value(
        r"^- Source kerning exists in every master: (yes|no)$",
        reports["kerning"],
    )
    static_kern = first_line_value(
        r"^- All built static fonts expose GPOS `kern`: (yes|no)$",
        reports["kerning"],
    )
    kerning_warnings = first_int(r"Fontspector `gpos_kerning_info` warnings: (\d+)", reports["kerning"])
    kerning_proof_output = first_line_value(
        r"^- Latest `gftools qa --proof` HTML output present: (yes|no)$",
        reports["kerning"],
    )
    kerning_proof_instances = first_line_value(
        r"^- Latest proof covers expected instances: (yes|no)$",
        reports["kerning"],
    )
    kerning_proof_review_files = first_line_value(
        r"^- Expected HTML proofs present: (.+)$",
        reports["kerning_proof_review"],
    )
    kerning_decision = first_line_value(r"^- Decision status: (.+)$", reports["kerning"])
    has_avar = first_line_value(r"^- Has `avar`: (yes|no)$", reports["avar"])
    avar_warnings = first_int(r"Fontspector `mandatory_avar_table` warnings: (\d+)", reports["avar"])
    avar_decision = first_line_value(r"^- Current decision: (.+)$", reports["avar"])
    pua_codepoints = first_int(r"Variable font PUA codepoints: (\d+)", reports["pua"])
    unreachable_glyph_warnings = first_int(r"\| `unreachable_glyphs` \| (\d+) \|", reports["warnings"])
    unreachable_subsetting_warnings = first_int(
        r"\| `googlefonts/metadata/unreachable_subsetting` \| (\d+) \|",
        reports["warnings"],
    )
    package_source_mode = first_line_value(r"^- Source mode: `?([^`\n]+)`?$", reports["package_dry_run"])
    package_can_reach = first_line_value(r"^- Wrapper can reach Packager: (yes|no)$", reports["package_dry_run"])
    package_first_blocker = first_line_value(r"^- First blocker: (.+)$", reports["package_dry_run"])
    package_auth = first_line_value(r"^- GitHub API credentials ready: (yes|no)$", reports["package_dry_run"])
    package_inputs_tracked = first_line_value(
        r"^- Required local package inputs tracked: (.+)$",
        reports["package_dry_run"],
    )
    package_inputs_untracked = first_line_value(
        r"^- Required local package inputs untracked: (.+)$",
        reports["package_dry_run"],
    )
    default_untracked_blocker = "public branch must expose untracked source files" in reports["package_dry_run"]
    latest_untracked_blocker = "release/archive must include untracked local source files" in reports["package_dry_run"]
    build_untracked_blocker = "build-from-source inputs are missing, ignored, or untracked" in reports["package_dry_run"]
    metadata_starter = first_line_value(
        r"^- Actual downstream METADATA\.pb is starter template: (yes|no)$",
        reports["downstream_metadata_diff"],
    )
    missing_expected_lines = first_line_value(
        r"^- Expected metadata lines missing from actual downstream file: (.+)$",
        reports["downstream_metadata_diff"],
    )
    metadata_ready_to_apply = first_line_value(
        r"^- Ready to apply preview via helper: (yes|no)$",
        reports["downstream_metadata_diff"],
    )
    metadata_apply_blockers = first_line_value(
        r"^- Prepare helper blocking findings: (\d+)$",
        reports["downstream_metadata_diff"],
    )
    source_strategy_matrix = first_line_value(
        r"^- Recommended first pass: (.+)$",
        reports["packager_source_strategy"],
        "review `documentation/google-fonts/packager-source-strategy.md`",
    )

    lines = [
        "# Google Fonts Add Font Issue Draft",
        "",
        "This generated draft follows the current Add Font issue template from the",
        "local `google/fonts` checkout. It is intentionally not ready to paste until",
        "the open maintainer decisions and drawing/source blockers are resolved.",
        "",
        "## Template Evidence",
        "",
        f"- Template path: `{template_path}`",
        f"- Template commit: `{git_output(gf_repo, ['rev-parse', '--short', 'HEAD']) or 'unknown'}`",
        f"- Template checkout status: `{status_line}`",
        f"- Alignment with `upstream/main`: `{ahead_behind(gf_repo, 'main', 'upstream/main')}`",
        f"- Alignment with `origin/main`: `{ahead_behind(gf_repo, 'main', 'origin/main')}`",
        f"- Title pattern: `{title_pattern or 'missing'}`",
        f"- Default labels: `{labels_line}`",
        f"- Requirement checkbox count: {len(requirements)}",
        "",
        "## Issue Title",
        "",
        "```text",
        "Add Virtua Grotesk",
        "```",
        "",
        "## Labels",
        "",
        "```text",
        labels_line,
        "```",
        "",
        "Request Arabic/RTL script labeling only after Arabic coverage, shaping,",
        "and proof review are ready for Google Fonts review.",
        "",
        "## Draft Body",
        "",
        "**Font Project Git Repo URL:**",
        "",
        "https://github.com/eliheuer/virtua-grotesk",
        "",
        "**Super short description of the Font Family:**",
        "",
        description,
        "",
        "**Requirements:**",
        "",
        "By opening this issue, I confirm the project meets the following requirements:",
        "",
    ]

    for requirement in requirements:
        lines.append(f"- [ ] {requirement}")
        lines.append(f"  - Draft status: {issue_requirement_note(requirement, reports)}")

    lines.extend(
        [
            "",
            "**Image:**",
            "",
        "Attach `documentation/assets/readme-specimen.png` or an updated specimen image",
        "after final drawing/source work is complete.",
        "",
        "## Arabic Scope Status",
        "",
        "Arabic support is in first-submission scope. Do not ask for Arabic/RTL",
        "review labels until these generated reports show the coverage and layout",
        "work is ready for review.",
        "",
        f"- GF Arabic Core missing codepoints: {arabic_missing}.",
        f"- Arabic letters missing: {arabic_counts['Arabic letters']}.",
        f"- Arabic marks missing from GF Arabic Core: {arabic_mark_missing}.",
        f"- U+25CC dotted circle present: {dotted_circle}.",
        f"- Built mark/mkmk GPOS features present: {mark_features}.",
        f"- Fonts with `arab/dflt` GSUB smoke coverage: {gsub_ready_fonts} / 5.",
        f"- Fonts with `arab/dflt` GPOS smoke coverage: {gpos_ready_fonts} / 5.",
        "- Required evidence: `documentation/glyph-review/arabic-review-packet.md`,",
        "  `documentation/google-fonts/missing-gf-arabic-core.md`,",
        "  `documentation/glyph-review/arabic-mark-readiness.md`, and",
        "  `documentation/glyph-review/arabic-shaping-smoke-test.md`.",
        "",
        "## Numeric Feature Status",
        "",
        "Google Fonts expects default ASCII digits to be proportional and",
        "complemented by a Tabular Numbers (`tnum`) feature.",
        "",
        f"- Default ASCII digits present in every built font: {numeric_default_digits}.",
        f"- Default ASCII digits are proportional in every built font: {numeric_default_proportional}.",
        f"- `tnum` feature present in every built font: {numeric_tnum_feature}.",
        f"- `tnum` substitutes all ten ASCII digits in every built font: {numeric_tnum_coverage}.",
        f"- `tnum` substitutes to equal-width digits in every built font: {numeric_tnum_tabular}.",
        f"- Numeric feature requirement ready: {numeric_ready}.",
        "- Required evidence: `documentation/google-fonts/numeric-feature-readiness.md`.",
        "",
        "## Designer Profile Status",
        "",
        "The final downstream `designer` string needs a matching Google Fonts",
        "`catalog/designers` profile, or a profile request prepared alongside",
        "the family submission.",
        "",
        f"- Current candidate designer string: `{designer_string}`.",
        f"- Candidate catalog slug: `{designer_slug}`.",
        f"- Candidate downstream profile directory: `{designer_profile_dir}`.",
        f"- AUTHORS catalog-credit candidates: {profile_candidates}.",
        f"- Candidate designer profiles missing: {profile_missing}.",
        f"- Final metadata designer strings present: {metadata_final_designers}.",
        f"- Pending metadata designer placeholders: {metadata_pending_placeholders}.",
        f"- Target profile directory already exists: {designer_profile_exists}.",
        f"- Expected profile files already present: {designer_profile_files}.",
        f"- Draft profile inputs still unresolved: {designer_profile_placeholders}.",
        "- Required evidence: `documentation/google-fonts/designer-profile-readiness.md` and",
        "  `documentation/google-fonts/designer-profile-package-draft.md`.",
        "",
        "## Decision-Linked Warning Status",
        "",
        "These are not glyph drawing tasks, but they need a maintainer decision",
        "or explicit deferral before checking the Add Font requirements.",
        "",
        f"- Vendor ID: source UFO IDs `{source_vendor}`; generated fonts use",
        f"  `{generated_vendor}`; Fontspector vendor warnings: {vendor_warnings};",
        f"  decision: {vendor_decision}.",
        f"- Kerning: source kerning in every master: {kerning_every_master};",
        f"  static GPOS `kern`: {static_kern}; warnings: {kerning_warnings};",
        f"  GF visual proof output: {kerning_proof_output};",
        f"  proof covers expected instances: {kerning_proof_instances};",
        f"  proof review packet files: {kerning_proof_review_files};",
        f"  decision: {kerning_decision}.",
        f"- `avar`: table present: {has_avar}; warning count: {avar_warnings};",
        f"  decision: {avar_decision}.",
        f"- PUA/reachability: PUA codepoints: {pua_codepoints};",
        f"  `unreachable_glyphs` warnings: {unreachable_glyph_warnings};",
        "  `googlefonts/metadata/unreachable_subsetting` warnings:",
        f"  {unreachable_subsetting_warnings}; decide whether private-use glyphs",
        "  ship in the first submission.",
        "- Required evidence: `documentation/google-fonts/vendor-id-readiness.md`,",
        "  `documentation/google-fonts/kerning-readiness.md`,",
        "  `documentation/google-fonts/kerning-proof-review.md`,",
        "  `documentation/google-fonts/avar-readiness.md`,",
        "  `documentation/google-fonts/pua-scope.md`, and",
        "  `documentation/google-fonts/fontspector-warnings.md`.",
        "",
        "## Package Dry-Run Status",
        "",
        "Do not open the downstream PR from this state. The first package pass",
        "should stay as a no-PR local dry run until the release/archive,",
        "metadata, and GitHub auth blockers are cleared.",
        "",
        f"- Selected Packager source mode: `{package_source_mode}`.",
        f"- Wrapper can reach Packager: {package_can_reach}.",
        f"- First package dry-run blocker: {package_first_blocker}.",
        f"- GitHub API credentials ready: {package_auth}.",
        f"- Required local package inputs tracked: {package_inputs_tracked}.",
        f"- Required local package inputs untracked: {package_inputs_untracked}.",
        f"- Default branch mode has untracked source-file blocker: {'yes' if default_untracked_blocker else 'no'}.",
        f"- Latest-release/archive mode has untracked source-file blocker: {'yes' if latest_untracked_blocker else 'no'}.",
        f"- Build-from-source mode has untracked build-input blocker: {'yes' if build_untracked_blocker else 'no'}.",
        f"- Downstream METADATA.pb is starter template: {metadata_starter}.",
        f"- Expected metadata lines missing from downstream file: {missing_expected_lines}.",
        f"- Downstream metadata preview ready to apply: {metadata_ready_to_apply}.",
        f"- Downstream metadata apply blockers: {metadata_apply_blockers}.",
        f"- Source strategy note: {source_strategy_matrix}.",
        "- Run `make downstream-metadata-check` before applying final metadata,",
        "  using the same `GFT_PACKAGER_SOURCE_MODE` planned for Packager so",
        "  `source.config_yaml` and `source.archive_url` are validated against",
        "  the selected source mode. For `latest-release`, `source.archive_url`",
        "  must be a GitHub release download URL ending in `.zip`,",
        "  then use `scripts/prepare_downstream_metadata.py --apply` only after",
        "  the dry run reports `Ready to apply: yes`.",
        "- Required evidence: `documentation/google-fonts/package-dry-run-readiness.md`,",
        "  `documentation/google-fonts/downstream-metadata-diff.md`, and",
        "  `documentation/google-fonts/packager-source-strategy.md`.",
        "",
        "## Finalize Before Opening",
            "",
            "- Confirm the public repository URL still matches the final release source.",
            "- Keep the approved authorship and AI-use disclosure wording synchronized.",
            "- Confirm the family name at `namecheck.fontdata.com`.",
            "- Clear the package dry-run blocker stack or document the reviewed",
            "  no-PR Packager result.",
            "- Resolve or explicitly document accepted Fontspector FAILs.",
            "- Regenerate this draft with `make preflight` after final source,",
            "  metadata, or Google Fonts template changes.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_add_font_issue_draft.py [google_fonts_repo] [output.md]")
    if len(argv) == 1:
        return DEFAULT_GF_REPO, OUTPUT_DEFAULT
    if len(argv) == 2:
        return DEFAULT_GF_REPO, Path(argv[1])
    return Path(argv[1]), Path(argv[2])


def main(argv: list[str]) -> int:
    gf_repo, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(gf_repo), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
