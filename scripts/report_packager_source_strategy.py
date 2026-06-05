#!/usr/bin/env python3
"""Generate a Packager source-strategy decision matrix."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/packager-source-strategy.md")
PACKAGE_AUDIT = Path("documentation/google-fonts/package-source-files-audit.md")
RELEASE_SOURCE = Path("documentation/google-fonts/release-source-readiness.md")
PREVIEW = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")
PUBLIC_UPSTREAM = Path("documentation/google-fonts/public-upstream-readiness.md")
PACKAGE_DRY_RUN = Path("documentation/google-fonts/package-dry-run-readiness.md")
LATEST_RELEASE_ARCHIVE_URL_PATTERN = re.compile(
    r'archive_url:\s*"https://github\.com/[^/"]+/[^/"]+/releases/download/[^/"]+/[^"]+\.zip"'
)


def read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def first_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def summary_value(label: str, text: str, default: str = "unknown") -> str:
    return first_value(rf"^- {re.escape(label)}: (.+)$", text, default=default)


def local_files_rows(package_audit: str) -> list[tuple[str, str, str, str, str]]:
    rows = []
    in_table = False
    for line in package_audit.splitlines():
        if line.startswith("| Source file | Destination file |"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        source_file = cells[0].strip("`")
        dest_file = cells[1].strip("`")
        exists = cells[3]
        ignored = cells[4]
        tracked = cells[5]
        rows.append((source_file, dest_file, exists, ignored, tracked))
    return rows


def build_input_summary(package_audit: str) -> tuple[int, int]:
    total = 0
    ready = 0
    in_table = False
    for line in package_audit.splitlines():
        if line.startswith("| Path | Exists locally | Ignored by git | Tracked by git |"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        total += 1
        if cells[1] == "yes" and cells[2] == "no" and cells[3] == "yes":
            ready += 1
    return ready, total


def build_input_rows(package_audit: str) -> list[tuple[str, str, str, str]]:
    rows = []
    in_table = False
    for line in package_audit.splitlines():
        if line.startswith("| Path | Exists locally | Ignored by git | Tracked by git |"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows.append((cells[0].strip("`"), cells[1], cells[2], cells[3]))
    return rows


def blocker_list(*items: tuple[bool, str]) -> str:
    blockers = [label for condition, label in items if condition]
    return "<br>".join(blockers) if blockers else "none in current local evidence"


def markdown_report() -> str:
    package_audit = read_text(PACKAGE_AUDIT)
    release_source = read_text(RELEASE_SOURCE)
    preview = read_text(PREVIEW)
    public_upstream = read_text(PUBLIC_UPSTREAM)
    package_dry_run = read_text(PACKAGE_DRY_RUN)

    source_files = local_files_rows(package_audit)
    build_inputs = build_input_rows(package_audit)
    build_ready, build_total = build_input_summary(package_audit)
    placeholder_present = summary_value("Placeholder upstream URL still present", release_source) == "yes"
    dirty_tree = summary_value("Working tree clean", release_source) == "no"
    tag_exists = summary_value("Suggested tag exists locally", release_source) == "yes"
    pending_source_fields = int(summary_value("Pending source fields in downstream preview", release_source, "0"))
    ignored_files = int(summary_value("Ignored/generated `source.files`", release_source, "0"))
    missing_files = int(summary_value("Missing local `source.files`", release_source, "0"))
    tracked_files = int(summary_value("Tracked `source.files`", package_audit, "0 / 0").split("/")[0].strip())
    untracked_files = int(summary_value("Untracked local `source.files`", package_audit, "0"))
    build_script_uses_builder = summary_value("Build script uses `gftools builder sources/config.yaml`", package_audit) == "yes"
    build_script_uses_metadata_fix = summary_value("Build script runs metadata post-processing", package_audit) == "yes"
    builder_config_outputs_fonts = summary_value("Builder config outputs to `fonts/`", package_audit) == "yes"
    gf_fork_topology_ready = (
        summary_value("Local google/fonts branch", release_source).strip("`") == "main"
        and summary_value("Local google/fonts main vs upstream/main", release_source).strip("`") == "0\t0"
    )
    gf_fork_clean = summary_value("Local google/fonts worktree clean", release_source) == "yes"
    gf_dirty_outside_family = summary_value("Dirty paths outside `ofl/virtuagrotesk`", package_dry_run, "unknown")
    downstream_starter_template = (
        summary_value("Existing downstream METADATA.pb is starter template", package_dry_run, "no") == "yes"
    )
    branch_field_present = "branch` field present for default/source-build mode: yes" in package_audit
    archive_present = "`archive_url` present for selected release/archive strategy: yes" in package_audit
    archive_url_ready = bool(LATEST_RELEASE_ARCHIVE_URL_PATTERN.search(preview))
    config_yaml_present = 'config_yaml: "sources/config.yaml"' in preview
    variable_ignored = any(
        source_file == "fonts/variable/VirtuaGrotesk[wght].ttf" and ignored == "yes"
        for source_file, _, _, ignored, _ in source_files
    )
    normalized_candidate = summary_value("Normalized GitHub origin candidate", release_source).strip("`")
    source_file_count = len(source_files)
    public_branch_trackable_files = [
        source_file
        for source_file, _, exists, _ignored, tracked in source_files
        if exists == "yes" and tracked == "no"
    ]
    public_branch_gitignore_exceptions = [
        source_file
        for source_file, _, exists, ignored, tracked in source_files
        if exists == "yes" and ignored == "yes" and tracked == "no"
    ]
    untracked_build_inputs = [
        path
        for path, exists, _ignored, tracked in build_inputs
        if exists == "yes" and tracked == "no"
    ]
    archive_required_files = [source_file for source_file, *_ in source_files]

    def inline_paths(paths: list[str]) -> str:
        return ", ".join(f"`{path}`" for path in paths) if paths else "none"

    lines = [
        "# Packager Source Strategy Matrix",
        "",
        (
            "This generated report compares the source modes available for the "
            "final Google Fonts Packager dry run. The maintainer-selected "
            "first-submission path is latest release/archive; the other modes "
            "remain documented fallback paths if Google Fonts review asks for "
            "a different source strategy."
        ),
        "",
        "## Current Evidence",
        "",
        f"- Normalized upstream candidate: `{normalized_candidate}`",
        f"- Placeholder upstream URL still present: {yes_no(placeholder_present)}",
        f"- Working tree clean: {yes_no(not dirty_tree)}",
        f"- Suggested release tag exists locally: {yes_no(tag_exists)}",
        f"- Pending downstream source fields: {pending_source_fields}",
        f"- Local `source.files` entries: {source_file_count}",
        f"- Missing local `source.files`: {missing_files}",
        f"- Ignored/generated `source.files`: {ignored_files}",
        f"- Tracked source.files: {tracked_files} / {source_file_count}",
        f"- Untracked local source.files: {untracked_files}",
        f"- Build-from-source inputs present and tracked: {build_ready} / {build_total}",
        f"- Build script uses GF builder config: {yes_no(build_script_uses_builder)}",
        f"- Build script runs metadata post-processing: {yes_no(build_script_uses_metadata_fix)}",
        f"- Builder config outputs package fonts directory: {yes_no(builder_config_outputs_fonts)}",
        f"- Downstream preview includes `source.config_yaml`: {yes_no(config_yaml_present)}",
        f"- `source.config_yaml` is reproducible-builder-only: {yes_no(config_yaml_present and build_script_uses_builder and builder_config_outputs_fonts)}",
        f"- Downstream preview includes release `archive_url`: {yes_no(archive_present)}",
        f"- Downstream preview `archive_url` is GitHub release download `.zip`: {yes_no(archive_url_ready)}",
        "- Selected first-submission source mode: `latest-release`",
        f"- Local google/fonts fork topology ready: {yes_no(gf_fork_topology_ready)}",
        f"- Local google/fonts checkout clean: {yes_no(gf_fork_clean)}",
        f"- Dirty paths outside `ofl/virtuagrotesk`: {gf_dirty_outside_family}",
        f"- Downstream METADATA.pb starter template present: {yes_no(downstream_starter_template)}",
        "",
        "## Strategy Matrix",
        "",
        "| Strategy | Dry-run command | Needs | Current blockers | Best fit |",
        "| --- | --- | --- | --- | --- |",
        "| Default branch `source.files` | `make package-dry-run` | Public branch exposes every listed `source_file`; final `branch` and `commit` recorded | {} | Best if final public branch commits the served variable TTF or otherwise exposes it at the listed path |".format(
            blocker_list(
                (placeholder_present, "replace placeholder public URL"),
                (pending_source_fields > 0, "replace pending commit/branch fields"),
                (variable_ignored, "served variable TTF is ignored/generated locally"),
                (untracked_files > 0, "commit or otherwise expose untracked source files"),
                (dirty_tree, "finish/commit source tree before citing a commit"),
                (missing_files > 0, "fix missing local source files"),
            )
        ),
        "| Latest release/archive | `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` | Public GitHub release download `.zip` exposes the expected files; final `archive_url` and tag strategy recorded | {} | Best if generated fonts should stay out of `main` but be published as release assets |".format(
            blocker_list(
                (placeholder_present, "replace placeholder public URL"),
                (not tag_exists, "create final release tag after source work"),
                (not archive_url_ready, "record final GitHub release download .zip URL in metadata preview"),
                (pending_source_fields > 0, "replace pending commit/branch fields"),
                (untracked_files > 0, "commit or package untracked source files into release archive"),
                (dirty_tree, "finish/commit source tree before tagging"),
            )
        ),
        "| Build from source | `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` | Public repo build path is reproducible and accepted by Google Fonts; source/build inputs tracked | {} | Best if Google Fonts accepts building from `sources/config.yaml` instead of fetching generated font binaries |".format(
            blocker_list(
                (placeholder_present, "replace placeholder public URL"),
                (build_ready != build_total, "make every build input public and tracked"),
                (not build_script_uses_builder, "wire build script to gftools builder sources/config.yaml"),
                (not build_script_uses_metadata_fix, "keep generated metadata fix in the reproducible build path"),
                (not builder_config_outputs_fonts, "keep builder output aligned with package font paths"),
                (not branch_field_present, "keep branch/config metadata available"),
                (pending_source_fields > 0, "replace pending commit/branch fields"),
                (dirty_tree, "finish/commit source tree before citing a commit"),
            )
        ),
        "",
        "## Source Files To Expose",
        "",
        "| Source file | Downstream destination | Exists locally | Ignored/generated locally | Tracked locally |",
        "| --- | --- | --- | --- | --- |",
    ]
    for source_file, dest_file, exists, ignored, tracked in source_files:
        lines.append(f"| `{source_file}` | `{dest_file}` | {exists} | {ignored} | {tracked} |")

    lines.extend(
        [
            "",
            "## Selected Latest-Release Action Plan",
            "",
            (
                "The maintainer-selected first-submission strategy keeps generated "
                "fonts out of the public branch and publishes the Packager inputs "
                "through a GitHub release archive. The next mechanical work is:"
            ),
            "",
            "1. Keep the public upstream URL and release/archive metadata preview synchronized.",
            "2. Finish drawing/source work and make the final `v1.000` source commit.",
            "3. Create a GitHub release archive that contains every listed `source.files` path.",
            "4. Keep `source.config_yaml` omitted unless Google Fonts asks for build metadata.",
            "5. Regenerate reports, run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`, then run a no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.",
            "",
            f"- Release archive files currently present but untracked: {', '.join(f'`{path}`' for path in public_branch_trackable_files) if public_branch_trackable_files else 'none'}",
            f"- Release archive files currently blocked by `.gitignore`: {', '.join(f'`{path}`' for path in public_branch_gitignore_exceptions) if public_branch_gitignore_exceptions else 'none'}",
            "- `make package-dry-run` now defaults to `GFT_PACKAGER_SOURCE_MODE=latest-release`; set `GFT_PACKAGER_SOURCE_MODE=default` or `build-from-source` only for fallback review.",
            "",
            "## Per-Strategy Mechanical Checklist",
            "",
            "These are conditional checklists. Apply only the section that matches the maintainer-approved source strategy.",
            "",
            "### If Default Public-Branch Packaging Is Chosen",
            "",
            "1. Apply the final public upstream URL everywhere reported by `make public-upstream-url-check`.",
            "2. Add a narrow `.gitignore` exception for the served variable font only.",
            f"3. Track the current untracked source files: {inline_paths(public_branch_trackable_files)}.",
            "4. Remove `source.config_yaml` from the downstream metadata preview unless Google Fonts review asks for build metadata.",
            "5. Regenerate reports, verify `GFT_PACKAGER_SOURCE_MODE=default make downstream-metadata-check`, then run the no-PR `GFT_PACKAGER_SOURCE_MODE=default make package-dry-run`.",
            "",
            "### If Latest Release Or Archive Packaging Is Chosen",
            "",
            "1. Keep generated fonts out of the public branch if that is the selected policy.",
            f"2. Ensure the release archive contains every mapped source file: {inline_paths(archive_required_files)}.",
            "3. Create the final release tag only after drawing/source work and metadata decisions are complete.",
            "4. Add the final GitHub release download `.zip` `source.archive_url` to the downstream metadata preview.",
            "5. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` before opening the downstream PR.",
            "",
            "### If Build-From-Source Packaging Is Chosen",
            "",
            "1. Keep `source.config_yaml: \"sources/config.yaml\"` in the downstream metadata preview.",
            f"2. Track every currently untracked build input: {inline_paths(untracked_build_inputs)}.",
            "3. Keep `build.sh` on `gftools builder sources/config.yaml` followed by `scripts/fix_gf_metadata.py`.",
            "4. Confirm Google Fonts accepts this family using the reproducible build path before treating the dry run as final.",
            "5. Run `GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run` without `-p` before opening the downstream PR.",
            "",
            "## Decision Notes",
            "",
            "- Do not run Packager with `-p` until the Google Fonts issue exists, final QA is reviewed, and the selected release/archive source is public.",
            "- Keep the local no-PR dry run on `$GF_REPO_PATH` before opening or updating a downstream PR.",
            "- The local dry-run wrapper accepts an explicit `GH_TOKEN` or exports one from a valid `gh auth token` before invoking Packager.",
            "- Keep `source.config_yaml` only for the build-from-source path. Recent `google/fonts` commits removed non-buildable or misleading `config_yaml` fields, so default branch or release/archive packaging should omit it unless Google Fonts specifically asks for build metadata.",
            "- Latest-release packaging must add the final GitHub release download `.zip` `archive_url` to the downstream metadata preview before `make downstream-metadata-check` can be ready.",
            "- If the strategy changes, update `documentation/google-fonts/google-fonts-downstream-package-preview.md` first, then regenerate reports.",
            "- If `upstream.yaml` is emitted, review it against the selected source mode before opening the PR.",
            "",
            "## References",
            "",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/googlefonts.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_packager_source_strategy.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
