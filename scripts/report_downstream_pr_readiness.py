#!/usr/bin/env python3
"""Generate a downstream Google Fonts PR readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/downstream-pr-readiness.md")
GF_REPO_PATH = Path("/Users/eli/GH/forks/fonts")
FAMILY_PATH = Path("ofl/virtuagrotesk")
EXPECTED_BRANCH = "gftools_packager_ofl_virtuagrotesk"
EXPECTED_PR_TITLE = "Virtua Grotesk : 1.000 added"
EXPECTED_PR_BODY = "Taken from the upstream repo <repo-url> at commit <commit-url>."


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def text_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def yes_no_from_line(pattern: str, text: str) -> str:
    return text_value(pattern, text, "unknown")


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def git_ahead_behind(repo: Path, left: str, right: str) -> tuple[str, str]:
    output = git_output(repo, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    parts = output.split()
    if len(parts) != 2:
        return "unknown", "unknown"
    return parts[0], parts[1]


def dirty_paths(repo: Path) -> list[str]:
    if not (repo / ".git").exists():
        return []
    return git_output(repo, ["status", "--porcelain"]).splitlines()


def family_files(repo: Path) -> list[str]:
    family_dir = repo / FAMILY_PATH
    if not family_dir.exists():
        return []
    return sorted(
        path.relative_to(repo).as_posix()
        for path in family_dir.rglob("*")
        if path.is_file()
    )


def path_from_status(line: str) -> str:
    return line[3:] if len(line) > 3 else line


def markdown_report() -> str:
    handoff = read_text("documentation/google-fonts/google-fonts-submission-handoff.md")
    handoff_readiness = read_text("documentation/google-fonts/submission-handoff-readiness.md")
    package_dry_run = read_text("documentation/google-fonts/package-dry-run-readiness.md")
    pr_identity = read_text("documentation/google-fonts/pr-identity-readiness.md")
    downstream_diff = read_text("documentation/google-fonts/downstream-metadata-diff.md")
    add_font_issue = read_text("documentation/google-fonts/google-fonts-add-font-issue-draft.md")
    release_source = read_text("documentation/google-fonts/release-source-readiness.md")

    gf_exists = (GF_REPO_PATH / ".git").exists()
    gf_branch = git_output(GF_REPO_PATH, ["rev-parse", "--abbrev-ref", "HEAD"]) if gf_exists else "missing"
    gf_origin = git_output(GF_REPO_PATH, ["remote", "get-url", "origin"]) if gf_exists else "missing"
    gf_upstream = git_output(GF_REPO_PATH, ["remote", "get-url", "upstream"]) if gf_exists else "missing"
    gf_tracking = git_output(GF_REPO_PATH, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]) if gf_exists else "missing"
    origin_ahead, origin_behind = git_ahead_behind(GF_REPO_PATH, "main", "origin/main") if gf_exists else ("missing", "missing")
    upstream_ahead, upstream_behind = git_ahead_behind(GF_REPO_PATH, "main", "upstream/main") if gf_exists else ("missing", "missing")
    gf_dirty_paths = dirty_paths(GF_REPO_PATH)
    dirty_outside_family = [
        line for line in gf_dirty_paths if not path_from_status(line).startswith(str(FAMILY_PATH) + "/")
    ]
    dirty_inside_family = [
        line for line in gf_dirty_paths if path_from_status(line).startswith(str(FAMILY_PATH) + "/")
    ]
    current_family_files = family_files(GF_REPO_PATH) if gf_exists else []
    family_dir_exists = (GF_REPO_PATH / FAMILY_PATH).exists()
    metadata_exists = (GF_REPO_PATH / FAMILY_PATH / "METADATA.pb").exists()
    fork_base_ready = (
        gf_exists
        and gf_branch == "main"
        and gf_tracking == "origin/main"
        and origin_ahead == "0"
        and origin_behind == "0"
        and upstream_ahead == "0"
        and upstream_behind == "0"
        and not dirty_outside_family
    )

    issue_pending = "Google Fonts issue: pending" in handoff
    issue_draft_current = yes_no_from_line(r"Issue draft title is current: (yes|no)", handoff_readiness)
    issue_labels_current = yes_no_from_line(r"Issue draft labels are current: (yes|no)", handoff_readiness)
    issue_boxes_unchecked = yes_no_from_line(r"Issue draft leaves boxes unchecked: (yes|no)", handoff_readiness)
    metadata_starter = yes_no_from_line(r"Actual downstream METADATA\.pb is starter template: (yes|no)", downstream_diff)
    starter_only_family_dir = (
        metadata_starter == "yes"
        and current_family_files == [f"{FAMILY_PATH}/METADATA.pb"]
    )
    metadata_ready_to_apply = yes_no_from_line(
        r"Ready to apply preview via helper: (yes|no)",
        downstream_diff,
    )
    metadata_apply_blockers = text_value(
        r"Prepare helper blocking findings: (\d+)",
        downstream_diff,
    )
    package_reaches = yes_no_from_line(r"Wrapper can reach Packager: (yes|no)", package_dry_run)
    package_first_blocker = text_value(r"First blocker: ([^\n]+)", package_dry_run)
    api_ready = yes_no_from_line(r"GitHub API credentials ready: (yes|no)", package_dry_run)
    source_git_identity = yes_no_from_line(r"Source repo git identity complete: (yes|no)", pr_identity)
    source_git_name_match = yes_no_from_line(
        r"Source repo git user\.name matches expected CLA/author name: (yes|no)",
        pr_identity,
    )
    gf_git_identity = yes_no_from_line(r"google/fonts fork git identity complete: (yes|no)", pr_identity)
    gf_git_name_match = yes_no_from_line(
        r"google/fonts fork git user\.name matches expected CLA/author name: (yes|no)",
        pr_identity,
    )
    final_commit_identity = yes_no_from_line(r"Final downstream commit identity ready: (yes|no)", pr_identity)
    cla_status = text_value(r"Google CLA status: ([^\n]+)", pr_identity)
    gh_auth = text_value(r"GitHub CLI auth status: `([^`]+)`", pr_identity)
    release_tag_exists = yes_no_from_line(r"Suggested tag exists locally: (yes|no)", release_source)
    release_tree_clean = yes_no_from_line(r"Working tree clean: (yes|no)", release_source)
    upstream_url_pending = (
        "Pending decision" in add_font_issue
        and "public canonical repository URL" in add_font_issue
    )

    handoff_has_pr_title = EXPECTED_PR_TITLE in handoff
    handoff_has_pr_body = EXPECTED_PR_BODY in handoff
    handoff_has_issue_first = "Google Fonts issue exists" in handoff or "issue exists" in handoff
    handoff_has_one_dir_rule = "one changed directory" in handoff
    handoff_has_expected_branch = EXPECTED_BRANCH in handoff
    handoff_has_compare_forks = "compare across forks" in handoff or "fork" in handoff

    lines = [
        "# Downstream PR Readiness",
        "",
        "This generated report turns the Google Fonts PR guide into local",
        "preflight evidence for the eventual downstream `google/fonts` pull",
        "request. It does not open an issue, push a branch, or write to the",
        "local `google/fonts` checkout.",
        "",
        "## Summary",
        "",
        f"- Google Fonts issue pending: {yes_no(issue_pending)}",
        f"- Issue draft current: {issue_draft_current}",
        f"- Issue labels current: {issue_labels_current}",
        f"- Issue requirement boxes still unchecked: {issue_boxes_unchecked}",
        f"- Expected downstream family path: `{FAMILY_PATH}`",
        f"- Downstream family directory exists locally: {yes_no(family_dir_exists)}",
        f"- Downstream METADATA.pb exists locally: {yes_no(metadata_exists)}",
        f"- Downstream METADATA.pb still starter template: {metadata_starter}",
        f"- Downstream metadata preview ready to apply: {metadata_ready_to_apply}",
        f"- Downstream metadata apply blockers: {metadata_apply_blockers}",
        f"- Expected Packager branch: `{EXPECTED_BRANCH}`",
        f"- Current google/fonts branch: `{gf_branch}`",
        f"- google/fonts tracking branch: `{gf_tracking}`",
        f"- google/fonts main vs origin/main: {origin_ahead} ahead, {origin_behind} behind",
        f"- google/fonts main vs upstream/main: {upstream_ahead} ahead, {upstream_behind} behind",
        f"- google/fonts fork base ready for downstream branch: {yes_no(fork_base_ready)}",
        f"- Dirty google/fonts paths inside family dir: {len(dirty_inside_family)}",
        f"- Dirty google/fonts paths outside family dir: {len(dirty_outside_family)}",
        f"- Current downstream family file count: {len(current_family_files)}",
        f"- Current downstream family files starter-only: {yes_no(starter_only_family_dir)}",
        f"- Package dry run reaches Packager: {package_reaches}",
        f"- Package dry-run first blocker: {package_first_blocker}",
        f"- GitHub API credentials ready: {api_ready}",
        f"- GitHub CLI auth status: `{gh_auth}`",
        f"- Source repo git identity complete: {source_git_identity}",
        f"- Source repo git name matches CLA/author name: {source_git_name_match}",
        f"- google/fonts fork git identity complete: {gf_git_identity}",
        f"- google/fonts fork git name matches CLA/author name: {gf_git_name_match}",
        f"- Final downstream commit identity ready: {final_commit_identity}",
        f"- Google CLA status: {cla_status}",
        f"- Public upstream URL still pending in issue draft: {yes_no(upstream_url_pending)}",
        f"- Release tag exists locally: {release_tag_exists}",
        f"- Source tree clean for final commit/tag: {release_tree_clean}",
        "",
        "## Expected PR Shape",
        "",
        f"- Branch name: `{EXPECTED_BRANCH}`",
        f"- Family directory: `{FAMILY_PATH}`",
        f"- PR title: `{EXPECTED_PR_TITLE}`",
        f"- PR body provenance line: `{EXPECTED_PR_BODY}`",
        "- Open or link the Google Fonts Add Font issue before creating the PR.",
        "- Keep the PR scoped to this one family directory.",
        "- Compare from the branch on the `eliheuer/fonts` fork unless a Google",
        "  Fonts team member asks for a direct upstream branch.",
        "",
        "## Handoff Coverage",
        "",
        f"- Handoff names expected Packager branch: {yes_no(handoff_has_expected_branch)}",
        f"- Handoff includes exact downstream PR title: {yes_no(handoff_has_pr_title)}",
        f"- Handoff includes exact PR provenance body line: {yes_no(handoff_has_pr_body)}",
        f"- Handoff records issue-first rule: {yes_no(handoff_has_issue_first)}",
        f"- Handoff records one-family-directory rule: {yes_no(handoff_has_one_dir_rule)}",
        f"- Handoff records fork comparison path: {yes_no(handoff_has_compare_forks)}",
        "",
        "## google/fonts Fork Evidence",
        "",
        f"- Fork path: `{GF_REPO_PATH}`",
        f"- Origin: `{gf_origin}`",
        f"- Upstream: `{gf_upstream}`",
        f"- Tracking branch: `{gf_tracking}`",
        f"- Alignment with `origin/main`: `{origin_ahead} ahead, {origin_behind} behind`",
        f"- Alignment with `upstream/main`: `{upstream_ahead} ahead, {upstream_behind} behind`",
        f"- Safe to branch after removing or replacing only `{FAMILY_PATH}`: {yes_no(fork_base_ready)}",
        "",
        "Dirty paths inside family dir:",
        "",
    ]
    lines.extend(f"- `{line}`" for line in dirty_inside_family) if dirty_inside_family else lines.append("- None")
    lines.extend(["", "Dirty paths outside family dir:", ""])
    lines.extend(f"- `{line}`" for line in dirty_outside_family) if dirty_outside_family else lines.append("- None")
    lines.extend(["", "Current files inside downstream family dir:", ""])
    lines.extend(f"- `{path}`" for path in current_family_files) if current_family_files else lines.append("- None")
    lines.extend(
        [
            "",
            "## Apply Before Opening Downstream PR",
            "",
            "- Open the Google Fonts Add Font issue and record its URL or number in",
            "  the handoff before using Packager with `-p`.",
            "- Resolve maintainer decisions, drawing/source blockers, and Fontspector",
            "  FAILs, or document reviewer-approved exceptions in the issue.",
            "- Confirm Google CLA status and the local `google/fonts` fork git",
            "  identity before committing downstream package changes.",
            "- Refresh GitHub CLI auth or export `GH_TOKEN` before the no-PR",
            "  Packager pass.",
            "- Replace the starter downstream `METADATA.pb` with the checked preview",
            "  only after `make downstream-metadata-check` reports `Ready to apply: yes`.",
            "- Review the expanded downstream family file list above before branching;",
            "  the current starter-only state must be replaced by Packager output",
            "  before opening the PR.",
            "- Rerun `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` without `-p` after the checked metadata",
            "  is applied and GitHub API auth is restored.",
            "- Review the generated package so the final PR changes only",
            "  `ofl/virtuagrotesk` and uses the expected title/body.",
            "",
            "## Safe Local Sequence",
            "",
            "Use this only after final drawing/source work, release metadata, and",
            "the Add Font issue are ready. The first Packager pass still omits `-p`",
            "so the generated package can be reviewed before any PR update.",
            "",
            "```bash",
            "gh auth status -h github.com",
            "make github-auth-check",
            "git -C /Users/eli/GH/forks/fonts config user.name \"Eli Heuer\"",
            "git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check",
            "./venv/bin/python scripts/prepare_downstream_metadata.py --apply",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
            "```",
            "",
            "Only after reviewing the no-PR package and recording the issue number",
            "should the final Packager run use `-p -i ISSUE_NUMBER`.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/onboarding.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_downstream_pr_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
