#!/usr/bin/env python3
"""Generate a Google Fonts release/source strategy readiness report."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/release-source-readiness.md")
GF_REPO_DEFAULT = Path(os.environ["GF_REPO_PATH"]) if os.environ.get("GF_REPO_PATH") else Path("GF_REPO_PATH_NOT_CONFIGURED")
PREVIEW = Path("documentation/google-fonts/google-fonts-downstream-package-preview.md")
PACKAGE_AUDIT = Path("documentation/google-fonts/package-source-files-audit.md")
PUBLIC_UPSTREAM = Path("documentation/google-fonts/public-upstream-readiness.md")
RELEASE_METADATA = Path("documentation/google-fonts/release-metadata.md")
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"
PACKAGE_DIR = Path("ofl/virtuagrotesk")


@dataclass(frozen=True)
class GitEvidence:
    branch: str
    commit: str
    short_commit: str
    origin_url: str
    normalized_origin_url: str
    upstream_name: str
    upstream_counts: str
    origin_counts: str
    dirty_paths: list[str]
    suggested_tag: str
    suggested_tag_exists: bool


def run_git(args: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def source_files_from_preview() -> list[str]:
    text = read_text(PREVIEW)
    return re.findall(r'source_file:\s*"([^"]+)"', text)


def source_mappings_from_preview() -> list[tuple[str, str]]:
    text = read_text(PREVIEW)
    mappings: list[tuple[str, str]] = []
    for block in re.findall(r"files\s*\{(.*?)\n\s*\}", text, flags=re.DOTALL):
        source_match = re.search(r'source_file:\s*"([^"]+)"', block)
        dest_match = re.search(r'dest_file:\s*"([^"]+)"', block)
        if source_match and dest_match:
            mappings.append((source_match.group(1), dest_match.group(1)))
    return mappings


def suggested_tag_from_release_metadata() -> str:
    match = re.search(r"Suggested first-submission tag: `([^`]+)`", read_text(RELEASE_METADATA))
    return match.group(1) if match else ""


def source_version_from_release_metadata() -> str:
    match = re.search(r"Source version: `([^`]+)`", read_text(RELEASE_METADATA))
    return match.group(1) if match else ""


def normalize_github_url(url: str) -> str:
    ssh_match = re.fullmatch(r"git@github\.com:([^/]+/[^.]+)(?:\.git)?", url)
    if ssh_match:
        return f"https://github.com/{ssh_match.group(1)}"
    https_match = re.fullmatch(r"https://github\.com/([^/]+/[^.]+)(?:\.git)?", url)
    if https_match:
        return f"https://github.com/{https_match.group(1)}"
    return ""


def git_evidence() -> GitEvidence:
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    commit = run_git(["rev-parse", "HEAD"]) or "unknown"
    short_commit = run_git(["rev-parse", "--short", "HEAD"]) or "unknown"
    origin_url = run_git(["remote", "get-url", "origin"]) or "missing"
    upstream_name = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    upstream_counts = (
        run_git(["rev-list", "--left-right", "--count", f"{branch}...{upstream_name}"])
        if upstream_name
        else "missing upstream"
    )
    origin_ref = f"origin/{branch}"
    origin_counts = (
        run_git(["rev-list", "--left-right", "--count", f"{branch}...{origin_ref}"])
        if run_git(["rev-parse", "--verify", "--quiet", origin_ref])
        else "missing origin branch"
    )
    dirty_paths = [line for line in run_git(["status", "--porcelain"]).splitlines() if line]
    suggested_tag = suggested_tag_from_release_metadata()
    suggested_tag_exists = bool(suggested_tag and run_git(["rev-parse", "--verify", "--quiet", suggested_tag]))
    return GitEvidence(
        branch=branch,
        commit=commit,
        short_commit=short_commit,
        origin_url=origin_url,
        normalized_origin_url=normalize_github_url(origin_url),
        upstream_name=upstream_name or "missing",
        upstream_counts=upstream_counts,
        origin_counts=origin_counts,
        dirty_paths=dirty_paths,
        suggested_tag=suggested_tag,
        suggested_tag_exists=suggested_tag_exists,
    )


def google_fonts_fork_evidence() -> tuple[bool, str, str, str, str, list[str]]:
    if not (GF_REPO_DEFAULT / ".git").exists():
        return (False, "missing", "missing", "missing", "missing", [])
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], GF_REPO_DEFAULT)
    origin = run_git(["remote", "get-url", "origin"], GF_REPO_DEFAULT)
    upstream = run_git(["remote", "get-url", "upstream"], GF_REPO_DEFAULT)
    upstream_counts = (
        run_git(["rev-list", "--left-right", "--count", "main...upstream/main"], GF_REPO_DEFAULT)
        if run_git(["rev-parse", "--verify", "--quiet", "upstream/main"], GF_REPO_DEFAULT)
        else "missing upstream/main"
    )
    dirty = [line for line in run_git(["status", "--porcelain"], GF_REPO_DEFAULT).splitlines() if line]
    return (True, branch, origin, upstream, upstream_counts, dirty)


def dirty_inside_package(dirty: list[str]) -> list[str]:
    prefix = f"{PACKAGE_DIR}/"
    return [line for line in dirty if len(line) > 3 and line[3:].startswith(prefix)]


def dirty_outside_package(dirty: list[str]) -> list[str]:
    prefix = f"{PACKAGE_DIR}/"
    return [line for line in dirty if not (len(line) > 3 and line[3:].startswith(prefix))]


def markdown_report() -> str:
    source_files = source_files_from_preview()
    source_mappings = source_mappings_from_preview()
    package_audit = read_text(PACKAGE_AUDIT)
    public_upstream = read_text(PUBLIC_UPSTREAM)
    release_metadata = read_text(RELEASE_METADATA)
    preview_text = read_text(PREVIEW)
    git = git_evidence()
    gf_exists, gf_branch, gf_origin, gf_upstream, gf_counts, gf_dirty = google_fonts_fork_evidence()
    gf_dirty_inside = dirty_inside_package(gf_dirty)
    gf_dirty_outside = dirty_outside_package(gf_dirty)
    source_version = source_version_from_release_metadata()
    expected_tag = f"v{source_version}" if source_version else ""
    suggested_tag_matches_version = bool(expected_tag and git.suggested_tag == expected_tag)
    normalized_origin_ready = bool(git.normalized_origin_url and git.normalized_origin_url != PLACEHOLDER_URL)
    expected_packager_branch = re.search(r"Expected Packager branch name: `([^`]+)`", package_audit)
    ignored_source_files = re.findall(r"\| `([^`]+)` \| `[^`]+` \| [^|]+ \| yes \| yes \|", package_audit)
    missing_source_files = re.findall(r"\| `([^`]+)` \| `[^`]+` \| [^|]+ \| no \|", package_audit)
    destination_mapping_ok = "Destination mapping matches expected downstream layout: yes" in package_audit
    variable_first_ok = "Variable-font-first source mapping: yes" in package_audit
    placeholder_present = PLACEHOLDER_URL in preview_text
    pending_source_fields = [
        line.strip()
        for line in preview_text.splitlines()
        if "Pending final release/source commit" in line
        or "Pending final upstream branch" in line
        or "Pending decision: public upstream URL" in line
    ]

    lines = [
        "# Release Source Readiness",
        "",
        "This generated report ties the final Google Fonts Packager source",
        "strategy to the current git state, release tag recommendation,",
        "downstream `source.files`, and local `google/fonts` fork. It is the",
        "handoff check for the source state that `METADATA.pb` will claim.",
        "",
        "## Summary",
        "",
        f"- Current repo branch: `{git.branch}`",
        f"- Current repo commit: `{git.commit}`",
        f"- Origin URL: `{git.origin_url}`",
        f"- Normalized GitHub origin candidate: `{git.normalized_origin_url or 'unavailable'}`",
        f"- Normalized origin differs from placeholder: {yes_no(normalized_origin_ready)}",
        f"- Source version from release metadata: `{source_version or 'unknown'}`",
        f"- Suggested tag from release metadata: `{git.suggested_tag or 'unknown'}`",
        f"- Suggested tag matches source version: {yes_no(suggested_tag_matches_version)}",
        f"- Suggested tag exists locally: {yes_no(git.suggested_tag_exists)}",
        f"- Working tree clean: {yes_no(not git.dirty_paths)}",
        f"- Branch upstream: `{git.upstream_name}`",
        f"- Ahead/behind branch upstream: `{git.upstream_counts}`",
        f"- Ahead/behind origin branch: `{git.origin_counts}`",
        f"- Placeholder upstream URL still present: {yes_no(placeholder_present)}",
        f"- Pending source fields in downstream preview: {len(pending_source_fields)}",
        f"- Downstream `source.files` entries: {len(source_files)}",
        f"- Downstream source destination mapping ready: {yes_no(destination_mapping_ok)}",
        f"- Downstream source mapping is variable-font-first: {yes_no(variable_first_ok)}",
        f"- Missing local `source.files`: {len(missing_source_files)}",
        f"- Ignored/generated `source.files`: {len(ignored_source_files)}",
        f"- Expected Packager branch: `{expected_packager_branch.group(1) if expected_packager_branch else 'unknown'}`",
        f"- Local google/fonts fork exists: {yes_no(gf_exists)}",
        f"- Local google/fonts branch: `{gf_branch}`",
        f"- Local google/fonts main vs upstream/main: `{gf_counts}`",
        f"- Local google/fonts worktree clean: {yes_no(not gf_dirty)}",
        f"- Local google/fonts dirty paths inside `{PACKAGE_DIR}`: {len(gf_dirty_inside)}",
        f"- Local google/fonts dirty paths outside `{PACKAGE_DIR}`: {len(gf_dirty_outside)}",
        f"- Local google/fonts dirty state isolated to `{PACKAGE_DIR}`: {yes_no(bool(gf_dirty_inside) and not gf_dirty_outside)}",
        "",
        "## Current Repo Git State",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| branch | `{git.branch}` |",
        f"| commit | `{git.commit}` |",
        f"| short commit | `{git.short_commit}` |",
        f"| origin | `{git.origin_url}` |",
        f"| normalized GitHub origin candidate | `{git.normalized_origin_url or 'unavailable'}` |",
        f"| upstream | `{git.upstream_name}` |",
        f"| upstream ahead/behind | `{git.upstream_counts}` |",
        f"| origin ahead/behind | `{git.origin_counts}` |",
        f"| source version | `{source_version or 'unknown'}` |",
        f"| suggested tag | `{git.suggested_tag or 'unknown'}` |",
        f"| suggested tag matches source version | {yes_no(suggested_tag_matches_version)} |",
        f"| suggested tag exists | {yes_no(git.suggested_tag_exists)} |",
        "",
        "## Current Dirty State",
        "",
    ]
    if git.dirty_paths:
        lines.extend(f"- `{line}`" for line in git.dirty_paths[:80])
        if len(git.dirty_paths) > 80:
            lines.append(f"- ... {len(git.dirty_paths) - 80} more entries omitted")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Downstream Source Mapping",
            "",
            "| Source file | Destination file | Local status |",
            "| --- | --- | --- |",
        ]
    )
    for source_file, dest_file in source_mappings:
        if source_file in missing_source_files:
            status = "missing"
        elif source_file in ignored_source_files:
            status = "ignored/generated"
        else:
            status = "present and not ignored"
        lines.append(f"| `{source_file}` | `{dest_file}` | {status} |")

    lines.extend(
        [
            "",
            "## Pending Downstream Source Fields",
            "",
        ]
    )
    if pending_source_fields:
        lines.extend(f"- `{line}`" for line in pending_source_fields)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Local google/fonts Fork",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| path | `{GF_REPO_DEFAULT}` |",
            f"| exists | {yes_no(gf_exists)} |",
            f"| branch | `{gf_branch}` |",
            f"| origin | `{gf_origin}` |",
            f"| upstream | `{gf_upstream}` |",
            f"| main vs upstream/main | `{gf_counts}` |",
            f"| dirty entries | {len(gf_dirty)} |",
            f"| dirty inside `{PACKAGE_DIR}` | {len(gf_dirty_inside)} |",
            f"| dirty outside `{PACKAGE_DIR}` | {len(gf_dirty_outside)} |",
            f"| dirty isolated to `{PACKAGE_DIR}` | {yes_no(bool(gf_dirty_inside) and not gf_dirty_outside)} |",
            "",
            "## Apply Before Final Packager Run",
            "",
            "- Keep the decided public upstream URL synchronized with OFL, source",
            "  metadata, Article links, handoff text, and downstream metadata.",
            "- Use the selected release/archive source strategy for the first",
            "  Packager pass unless Google Fonts review asks for another mode.",
            "- Ensure the final release archive contains every mapped",
            "  `source.files` path before the latest-release Packager run.",
            "- Create or update the final upstream tag only after drawing/source",
            "  work and maintainer decisions are complete.",
            "- Record the final repository URL, commit, branch, GitHub release download `.zip` URL, and source mode in",
            "  `documentation/google-fonts/google-fonts-downstream-package-preview.md`.",
            "- Rerun `make preflight` so proof evidence and generated reports",
            "  stay synchronized, then run",
            "  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` from",
            "  an aligned local `google/fonts` fork.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    # Keep these strings visible for preflight so the report stays tied to its inputs.
    assert "Source version:" in release_metadata
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_release_source_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
