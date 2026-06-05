#!/usr/bin/env python3
"""Report whether the guarded Packager dry run can start."""

from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/package-dry-run-readiness.md")
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
PACKAGE_DIR = Path("ofl/virtuagrotesk")
METADATA_PATH = GF_REPO_PATH / PACKAGE_DIR / "METADATA.pb"
PLACEHOLDER_UPSTREAM_URL = "https://github.com/fontgarden/virtua-grotesk"
STARTER_TEMPLATE_MARKERS = [
    'designer: "UNKNOWN"',
    'repository_url: "https://github.com/user/repo"',
    'fonts/variable/MyFont[wght].ttf',
    'primary_script: "Deva"',
]
UNRESOLVED_METADATA_MARKERS = [
    "Pending decision",
    "Pending:",
    "Pending final",
]
PROHIBITED_OPTIONAL_FIELDS = [
    "languages",
    "display_name",
    "minisite_url",
    "classifications",
    "sample_text",
    "tags",
]
CONFIG_YAML_LINE = 'config_yaml: "sources/config.yaml"'
ARCHIVE_URL_PATTERN = re.compile(
    r'^\s*archive_url:\s+"https://github\.com/[^/"]+/[^/"]+/releases/download/[^/"]+/[^"]+\.zip"\s*$',
    re.MULTILINE,
)
DATE_ADDED_PATTERN = re.compile(r'^\s*date_added:\s+"([^"]+)"\s*$', re.MULTILINE)
SOURCE_COMMIT_PATTERN = re.compile(r'^\s*commit:\s+"([^"]+)"\s*$', re.MULTILINE)
EXPECTED_SOURCE_MODES = {"default", "latest-release", "build-from-source", ""}
REQUIRED_PACKAGE_INPUTS = [
    "fonts/variable/VirtuaGrotesk[wght].ttf",
    "OFL.txt",
    "documentation/google-fonts/ARTICLE.en_us.html",
    "documentation/assets/readme-specimen.png",
    "sources/config.yaml",
]
PACKAGE_WRAPPER = ROOT / "scripts/package_gf_dry_run.sh"
DOWNSTREAM_PREVIEW = ROOT / "documentation/google-fonts/google-fonts-downstream-package-preview.md"
RELEASE_ARCHIVE_VERIFIER = ROOT / "scripts/verify_release_archive.py"


def run(command: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def git(path: Path, args: list[str]) -> str:
    if not (path / ".git").exists():
        return "missing"
    _, output = run(["git", "-C", str(path), *args])
    return output or "missing"


def github_repo_slug(url: str) -> str:
    """Return owner/repo for GitHub remotes in SSH or HTTPS form."""
    match = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?/?$", url.strip())
    return match.group(1) if match else "unknown"


def remote_is_google_fonts(url: str) -> bool:
    return github_repo_slug(url) == "google/fonts"


def remote_is_fonts_fork_candidate(url: str) -> bool:
    slug = github_repo_slug(url)
    return slug != "unknown" and slug != "google/fonts" and slug.endswith("/fonts")


def rev_exists(path: Path, rev: str) -> bool:
    if not (path / ".git").exists():
        return False
    returncode, _ = run(["git", "-C", str(path), "rev-parse", "--verify", "--quiet", rev])
    return returncode == 0


def branch_alignment(path: Path, left: str, right: str) -> str:
    if not rev_exists(path, left) or not rev_exists(path, right):
        return "missing"
    return git(path, ["rev-list", "--left-right", "--count", f"{left}...{right}"])


def dirty_outside_package(path: Path) -> list[str]:
    if not (path / ".git").exists():
        return []
    status = git(path, ["status", "--porcelain"])
    if status == "missing" or not status:
        return []
    package_prefix = f"{PACKAGE_DIR}/"
    dirty = []
    for line in status.splitlines():
        path_part = line[3:] if len(line) > 3 else ""
        if not path_part.startswith(package_prefix):
            dirty.append(line)
    return dirty


def dirty_inside_package(path: Path) -> list[str]:
    if not (path / ".git").exists():
        return []
    status = git(path, ["status", "--porcelain"])
    if status == "missing" or not status:
        return []
    package_prefix = f"{PACKAGE_DIR}/"
    dirty = []
    for line in status.splitlines():
        path_part = line[3:] if len(line) > 3 else ""
        if path_part.startswith(package_prefix):
            dirty.append(line)
    return dirty


def github_auth_state() -> tuple[str, str]:
    if os.environ.get("GH_TOKEN"):
        return "explicit GH_TOKEN", "GH_TOKEN is set in the environment"
    if not shutil_which("gh"):
        return "missing gh", "GitHub CLI is not installed or not on PATH"
    token_returncode, _ = run(["gh", "auth", "token"])
    if token_returncode == 0:
        return "valid gh token", "gh auth token returned a token"
    status_returncode, status_output = run(["gh", "auth", "status"])
    status = "invalid token" if "invalid" in status_output.lower() else "unavailable"
    summary = re.sub(r"\s+", " ", status_output).strip() or f"gh auth status exit {status_returncode}"
    return status, summary


def shutil_which(command: str) -> bool:
    return any((Path(part) / command).exists() for part in os.environ.get("PATH", "").split(os.pathsep))


def source_mode() -> str:
    return os.environ.get("GFT_PACKAGER_SOURCE_MODE", "default") or "default"


def wrapper_command(mode: str) -> str:
    if mode == "latest-release":
        return "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run"
    if mode == "build-from-source":
        return "GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run"
    return "make package-dry-run"


def wrapper_required_inputs() -> list[str]:
    if not PACKAGE_WRAPPER.exists():
        return []
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    match = re.search(r"for required_path in \\\n(?P<body>.*?)\ndo", text, flags=re.DOTALL)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group("body"))


def wrapper_starter_markers() -> list[str]:
    if not PACKAGE_WRAPPER.exists():
        return []
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    match = re.search(r"starter_template_markers=\(\n(?P<body>.*?)\n\)", text, flags=re.DOTALL)
    if not match:
        return []
    return re.findall(r"'([^']+)'", match.group("body"))


def wrapper_unresolved_markers() -> list[str]:
    if not PACKAGE_WRAPPER.exists():
        return []
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    match = re.search(r"unresolved_metadata_markers=\(\n(?P<body>.*?)\n\)", text, flags=re.DOTALL)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group("body"))


def wrapper_source_modes() -> set[str]:
    if not PACKAGE_WRAPPER.exists():
        return set()
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    modes = set(re.findall(r"^\s{4}([A-Za-z0-9_-]+)\)", text, flags=re.MULTILINE))
    if 'default|"")' in text:
        modes.add("default")
        modes.add("")
    return modes


def wrapper_has_source_mode_metadata_gates() -> bool:
    if not PACKAGE_WRAPPER.exists():
        return False
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    expected_snippets = [
        "prohibited_optional_metadata_fields=(",
        "metadata_has_config_yaml",
        "metadata_has_archive_url",
        "source.config_yaml",
        "source.archive_url",
        "release download URL ending in .zip",
        "final valid date_added",
        "lowercase 40-character source.commit hash",
        "review-gated optional field",
    ]
    return all(snippet in text for snippet in expected_snippets)


def wrapper_has_release_archive_gate() -> bool:
    if not PACKAGE_WRAPPER.exists():
        return False
    text = PACKAGE_WRAPPER.read_text(encoding="utf-8")
    return "scripts/verify_release_archive.py --quiet" in text and "make release-archive-build" in text


def release_archive_ready() -> bool:
    if not RELEASE_ARCHIVE_VERIFIER.exists():
        return False
    returncode, _ = run(["./venv/bin/python", str(RELEASE_ARCHIVE_VERIFIER.relative_to(ROOT)), "--quiet"])
    return returncode == 0


def metadata_source_mode_errors(metadata: str, mode: str) -> list[str]:
    if not metadata:
        return []
    errors: list[str] = []
    has_config_yaml = CONFIG_YAML_LINE in metadata
    has_archive_url = bool(ARCHIVE_URL_PATTERN.search(metadata))
    date_match = DATE_ADDED_PATTERN.search(metadata)
    commit_match = SOURCE_COMMIT_PATTERN.search(metadata)
    date_value = date_match.group(1) if date_match else ""
    commit_value = commit_match.group(1) if commit_match else ""
    for field in PROHIBITED_OPTIONAL_FIELDS:
        if re.search(rf"^\s*{re.escape(field)}\s*:", metadata, flags=re.MULTILINE):
            errors.append(f"review-gated optional field present: {field}")
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        errors.append("date_added missing or not a final valid YYYY-MM-DD date")
    if not re.fullmatch(r"[0-9a-f]{40}", commit_value):
        errors.append("source.commit missing or not a lowercase 40-character git hash")
    if mode in {"default", ""} and has_config_yaml:
        errors.append("source.config_yaml present for default source mode")
    if mode == "latest-release":
        if has_config_yaml:
            errors.append("source.config_yaml present for latest-release source mode")
        if not has_archive_url:
            errors.append("source.archive_url missing for latest-release source mode")
    if mode == "build-from-source" and not has_config_yaml:
        errors.append("source.config_yaml missing for build-from-source source mode")
    return errors


def preview_text() -> str:
    return DOWNSTREAM_PREVIEW.read_text(encoding="utf-8") if DOWNSTREAM_PREVIEW.exists() else ""


def source_files_from_preview(text: str) -> list[str]:
    return re.findall(r'source_file:\s*"([^"]+)"', text)


def ignored_by_git(relative_path: str) -> bool:
    returncode, _ = run(["git", "check-ignore", "--quiet", relative_path])
    return returncode == 0


def tracked_by_git(relative_path: str) -> bool:
    returncode, _ = run(["git", "ls-files", "--error-unmatch", "--", relative_path])
    return returncode == 0


def mode_gate_rows(
    text: str,
    source_files: list[str],
    metadata_ready: bool,
    auth_ready: bool,
    gf_ready: bool,
) -> list[dict[str, str]]:
    has_config_yaml = 'config_yaml: "sources/config.yaml"' in text
    has_archive_url = "archive_url:" in text
    pending_values = bool(re.search(r"Pending decision|Pending final|fontgarden/virtua-grotesk", text))
    ignored_source_files = [source_file for source_file in source_files if ignored_by_git(source_file)]
    untracked_source_files = [
        source_file
        for source_file in source_files
        if (ROOT / source_file).exists() and not tracked_by_git(source_file)
    ]
    build_inputs = [
        "sources/config.yaml",
        "sources/VirtuaGrotesk.designspace",
        "sources/VirtuaGrotesk-Regular.ufo",
        "sources/VirtuaGrotesk-Bold.ufo",
        "build.sh",
        "requirements.txt",
    ]
    untracked_build_inputs = [
        path
        for path in build_inputs
        if (ROOT / path).exists() and not tracked_by_git(path)
    ]
    build_inputs_ready = all(
        (ROOT / path).exists() and not ignored_by_git(path) and tracked_by_git(path)
        for path in build_inputs
    )
    archive_ready = release_archive_ready()

    shared_blockers: list[str] = []
    if not gf_ready:
        shared_blockers.append("local google/fonts checkout not ready")
    if not metadata_ready:
        shared_blockers.append("downstream METADATA.pb is not populated")
    if not auth_ready:
        shared_blockers.append("GitHub API credentials unavailable")
    if pending_values:
        shared_blockers.append("preview still has pending/placeholder source fields")

    rows = []
    default_blockers = list(shared_blockers)
    if ignored_source_files:
        default_blockers.append(
            "public branch must expose ignored/generated source files: "
            + ", ".join(f"`{item}`" for item in ignored_source_files)
        )
    if untracked_source_files:
        default_blockers.append(
            "public branch must expose untracked source files: "
            + ", ".join(f"`{item}`" for item in untracked_source_files)
        )
    if has_config_yaml:
        default_blockers.append("remove `source.config_yaml` unless GF review asks for build metadata")
    rows.append(
        {
            "mode": "default",
            "command": "make package-dry-run",
            "ready": yes_no(not default_blockers),
            "blockers": "; ".join(default_blockers) if default_blockers else "none",
        }
    )

    latest_blockers = list(shared_blockers)
    if not has_archive_url:
        latest_blockers.append("add final `source.archive_url`")
    if not archive_ready:
        latest_blockers.append("verify local release archive with `make release-archive-build`")
    if untracked_source_files:
        latest_blockers.append(
            "release/archive must include untracked local source files: "
            + ", ".join(f"`{item}`" for item in untracked_source_files)
        )
    if has_config_yaml:
        latest_blockers.append("remove `source.config_yaml` unless latest-release is explicitly paired with build metadata")
    rows.append(
        {
            "mode": "latest-release",
            "command": "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
            "ready": yes_no(not latest_blockers),
            "blockers": "; ".join(latest_blockers) if latest_blockers else "none",
        }
    )

    build_blockers = list(shared_blockers)
    if not has_config_yaml:
        build_blockers.append("keep `source.config_yaml` for build-from-source")
    if not build_inputs_ready:
        build_blockers.append(
            "build-from-source inputs are missing, ignored, or untracked"
            + (
                ": " + ", ".join(f"`{item}`" for item in untracked_build_inputs)
                if untracked_build_inputs
                else ""
            )
        )
    rows.append(
        {
            "mode": "build-from-source",
            "command": "GFT_PACKAGER_SOURCE_MODE=build-from-source make package-dry-run",
            "ready": yes_no(not build_blockers),
            "blockers": "; ".join(build_blockers) if build_blockers else "none",
        }
    )
    return rows


def markdown_report() -> str:
    mode = source_mode()
    gf_exists = (GF_REPO_PATH / ".git").exists()
    origin = git(GF_REPO_PATH, ["remote", "get-url", "origin"])
    upstream = git(GF_REPO_PATH, ["remote", "get-url", "upstream"])
    origin_slug = github_repo_slug(origin)
    upstream_slug = github_repo_slug(upstream)
    has_google_remote = remote_is_google_fonts(origin)
    has_google_upstream = remote_is_google_fonts(upstream)
    origin_is_fork_candidate = remote_is_fonts_fork_candidate(origin)
    google_fonts_topology_ready = has_google_remote or (origin_is_fork_candidate and has_google_upstream)
    branch = git(GF_REPO_PATH, ["rev-parse", "--abbrev-ref", "HEAD"])
    upstream_main_exists = rev_exists(GF_REPO_PATH, "upstream/main")
    origin_main_exists = rev_exists(GF_REPO_PATH, "origin/main")
    upstream_alignment = branch_alignment(GF_REPO_PATH, "main", "upstream/main")
    origin_alignment = branch_alignment(GF_REPO_PATH, "main", "origin/main") if origin_main_exists else "missing"
    dirty_outside = dirty_outside_package(GF_REPO_PATH)
    dirty_inside = dirty_inside_package(GF_REPO_PATH)
    downstream_preview_text = preview_text()
    preview_source_files = source_files_from_preview(downstream_preview_text)
    wrapper_only_inputs = [
        path for path in REQUIRED_PACKAGE_INPUTS if path not in preview_source_files
    ]
    input_status = [
        (
            path,
            (ROOT / path).exists(),
            ignored_by_git(path),
            tracked_by_git(path),
            "downstream source.files"
            if path in preview_source_files
            else "local wrapper sanity input",
        )
        for path in REQUIRED_PACKAGE_INPUTS
    ]
    metadata_exists = METADATA_PATH.exists()
    metadata_text = METADATA_PATH.read_text(encoding="utf-8") if metadata_exists else ""
    metadata_placeholder = metadata_exists and PLACEHOLDER_UPSTREAM_URL in metadata_text
    metadata_starter_markers = [marker for marker in STARTER_TEMPLATE_MARKERS if marker in metadata_text]
    metadata_unresolved_markers = [marker for marker in UNRESOLVED_METADATA_MARKERS if marker in metadata_text]
    metadata_source_errors = metadata_source_mode_errors(metadata_text, mode)
    metadata_starter_template = bool(metadata_starter_markers)
    auth_state, auth_detail = github_auth_state()
    wrapper_inputs = wrapper_required_inputs()
    wrapper_markers = wrapper_starter_markers()
    wrapper_unresolved = wrapper_unresolved_markers()
    wrapper_modes = wrapper_source_modes()
    wrapper_metadata_gates = wrapper_has_source_mode_metadata_gates()
    wrapper_release_archive_gate = wrapper_has_release_archive_gate()
    archive_ready = release_archive_ready()
    expected_modes_without_empty = {item for item in EXPECTED_SOURCE_MODES if item}
    input_lists_match = set(REQUIRED_PACKAGE_INPUTS) == set(wrapper_inputs)
    marker_lists_match = set(STARTER_TEMPLATE_MARKERS) == set(wrapper_markers)
    unresolved_lists_match = set(UNRESOLVED_METADATA_MARKERS) == set(wrapper_unresolved)
    mode_lists_match = expected_modes_without_empty == {item for item in wrapper_modes if item}
    gf_ready = (
        gf_exists
        and google_fonts_topology_ready
        and branch == "main"
        and upstream_main_exists
        and upstream_alignment == "0\t0"
        and (not origin_main_exists or origin_alignment == "0\t0")
        and not dirty_outside
    )
    package_inputs_ready = all(present for _, present, _, _, _ in input_status)
    package_inputs_tracked = sum(1 for _, present, _, tracked, _ in input_status if present and tracked)
    package_inputs_untracked = [
        path for path, present, _, tracked, _ in input_status if present and not tracked
    ]
    mode_ready = mode in EXPECTED_SOURCE_MODES
    metadata_reusable = (
        not metadata_placeholder
        and not metadata_starter_template
        and not metadata_unresolved_markers
        and not metadata_source_errors
    )
    auth_ready = auth_state in {"explicit GH_TOKEN", "valid gh token"}
    wrapper_can_start_packager = gf_ready and package_inputs_ready and mode_ready and metadata_reusable and auth_ready
    starter_template_quarantined = metadata_starter_template and bool(dirty_inside) and not dirty_outside
    mode_rows = mode_gate_rows(
        downstream_preview_text,
        preview_source_files,
        metadata_reusable,
        auth_ready,
        gf_ready,
    )

    blockers = []
    if not gf_ready:
        blockers.append("local google/fonts fork is not ready")
    if not package_inputs_ready:
        blockers.append("required local package inputs are missing")
    if not mode_ready:
        blockers.append(f"unsupported GFT_PACKAGER_SOURCE_MODE `{mode}`")
    if not metadata_reusable:
        if metadata_starter_template:
            blockers.append("existing downstream METADATA.pb is still the Packager starter template")
        elif metadata_unresolved_markers:
            blockers.append("existing downstream METADATA.pb still contains unresolved metadata")
        elif metadata_source_errors:
            blockers.append("existing downstream METADATA.pb is incompatible with the selected source mode")
        else:
            blockers.append("existing downstream METADATA.pb still uses placeholder upstream URL")
    if not auth_ready:
        blockers.append("GitHub API credentials unavailable")
    first_blocker = blockers[0] if blockers else "none"
    blocking_findings = "; ".join(blockers) if blockers else "none"

    next_actions = []
    if not gf_ready:
        next_actions.append("- Sync and clean the local `google/fonts` fork before running Packager.")
    if not package_inputs_ready:
        next_actions.append("- Regenerate or restore the missing local package inputs.")
    if not mode_ready:
        next_actions.append("- Use `default`, `latest-release`, or `build-from-source` for `GFT_PACKAGER_SOURCE_MODE`.")
    if not metadata_reusable:
        if metadata_starter_template:
            next_actions.append(
                "- Keep the current starter `METADATA.pb` as Packager evidence "
                "until the preview is final, then replace it with the checked "
                "downstream preview."
            )
        elif metadata_source_errors:
            next_actions.append(
                "- Make the existing downstream `METADATA.pb` match the selected "
                "`GFT_PACKAGER_SOURCE_MODE` before rerunning Packager."
            )
        else:
            next_actions.append("- Remove placeholder upstream URLs from the existing downstream `METADATA.pb` before rerunning Packager.")
    if not auth_ready:
        next_actions.extend(
            [
                "- Inspect GitHub CLI auth with `gh auth status -h github.com`.",
                "- Refresh GitHub CLI auth with `gh auth login -h github.com`, or",
                "  set `GH_TOKEN`, before running `make package-dry-run`.",
            ]
        )
    if wrapper_can_start_packager:
        next_actions.append("- The wrapper can reach Packager; keep the first pass as a no-PR dry run.")
    next_actions.extend(
        [
            "- Keep the selected public upstream URL and release/archive source",
            "  strategy synchronized with the final GitHub release before expecting",
            "  Packager to complete successfully.",
            "- Keep the first pass as a no-PR dry run; this wrapper does not pass",
            "  `-p` to Packager.",
        ]
    )

    lines = [
        "# Package Dry-Run Readiness",
        "",
        (
            "This generated report predicts whether the guarded local "
            "`make package-dry-run` command can reach `gftools packager`. It "
            "does not run Packager and does not write to the local "
            "`google/fonts` checkout."
        ),
        "",
        "## Summary",
        "",
        f"- Wrapper command: `{wrapper_command(mode)}`",
        f"- Source mode: `{mode}`",
        f"- Source mode supported by wrapper: {yes_no(mode_ready)}",
        f"- Local google/fonts fork ready: {yes_no(gf_ready)}",
        f"- Required local package inputs ready: {yes_no(package_inputs_ready)}",
        f"- Required local package inputs tracked: {package_inputs_tracked} / {len(REQUIRED_PACKAGE_INPUTS)}",
        f"- Required local package inputs untracked: {len(package_inputs_untracked)}",
        f"- Downstream preview `source.files` inputs: {len(preview_source_files)}",
        f"- Wrapper-only local sanity inputs: {', '.join(f'`{item}`' for item in wrapper_only_inputs) if wrapper_only_inputs else 'none'}",
        f"- Existing downstream METADATA.pb reusable: {yes_no(metadata_reusable)}",
        f"- Existing downstream METADATA.pb has stale placeholder URL: {yes_no(metadata_placeholder)}",
        f"- Existing downstream METADATA.pb has starter-template markers: {yes_no(metadata_starter_template)}",
        f"- Starter template quarantined in downstream package path: {yes_no(starter_template_quarantined)}",
        f"- Existing downstream METADATA.pb has unresolved metadata markers: {yes_no(bool(metadata_unresolved_markers))}",
        f"- Existing downstream METADATA.pb source-mode compatible: {yes_no(not metadata_source_errors)}",
        f"- GitHub API credentials ready: {yes_no(auth_ready)}",
        f"- Wrapper can reach Packager: {yes_no(wrapper_can_start_packager)}",
        f"- First blocker: {first_blocker}",
        f"- Blocking findings: {blocking_findings}",
        f"- Report/wrapper required-input lists match: {yes_no(input_lists_match)}",
        f"- Report/wrapper starter-marker lists match: {yes_no(marker_lists_match)}",
        f"- Report/wrapper unresolved-marker lists match: {yes_no(unresolved_lists_match)}",
        f"- Report/wrapper source-mode lists match: {yes_no(mode_lists_match)}",
        f"- Report/wrapper source-mode metadata gates present: {yes_no(wrapper_metadata_gates)}",
        f"- Report/wrapper final metadata value gates present: {yes_no(wrapper_metadata_gates)}",
        f"- Report/wrapper release-archive gate present: {yes_no(wrapper_release_archive_gate)}",
        f"- Local release archive verified: {yes_no(archive_ready)}",
        "",
        "## Google Fonts Checkout",
        "",
        f"- GF_REPO_PATH: `{GF_REPO_PATH}`",
        f"- Checkout exists: {yes_no(gf_exists)}",
        f"- Origin: `{origin}`",
        f"- Upstream: `{upstream}`",
        f"- Origin GitHub repo: `{origin_slug}`",
        f"- Upstream GitHub repo: `{upstream_slug}`",
        f"- Origin is canonical google/fonts: {yes_no(has_google_remote)}",
        f"- Origin is fork candidate: {yes_no(origin_is_fork_candidate)}",
        f"- Upstream is canonical google/fonts: {yes_no(has_google_upstream)}",
        f"- google/fonts remote topology ready: {yes_no(google_fonts_topology_ready)}",
        f"- Current branch: `{branch}`",
        f"- upstream/main exists: {yes_no(upstream_main_exists)}",
        f"- main vs upstream/main: `{upstream_alignment}`",
        f"- origin/main exists: {yes_no(origin_main_exists)}",
        f"- main vs origin/main: `{origin_alignment}`",
        f"- Dirty paths inside `{PACKAGE_DIR}`: {len(dirty_inside)}",
        f"- Dirty paths outside `{PACKAGE_DIR}`: {len(dirty_outside)}",
        f"- Dirty state is isolated to `{PACKAGE_DIR}`: {yes_no(bool(dirty_inside) and not dirty_outside)}",
        "",
        "## Downstream Starter Template Policy",
        "",
        "The local `google/fonts` checkout may contain a Packager starter",
        "`METADATA.pb` while the upstream release, GitHub release download `.zip` URL, source commit,",
        "and `date_added` are still unresolved. Treat that file as quarantined",
        "evidence only; do not submit it and do not run Packager with `-p` from",
        "that state.",
        "",
        f"- Starter template present: {yes_no(metadata_starter_template)}",
        f"- Starter template quarantined to `{PACKAGE_DIR}`: {yes_no(starter_template_quarantined)}",
        "- Replacement source of truth: `documentation/google-fonts/google-fonts-downstream-package-preview.md`",
        "- Replacement gate: `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`",
        "- Replacement command after blockers clear: `./venv/bin/python scripts/prepare_downstream_metadata.py --apply`",
        "",
        "## Source Mode Gate",
        "",
        "These rows compare the same downstream preview against every supported",
        "Packager source mode. They are a decision aid; the wrapper still uses",
        "`GFT_PACKAGER_SOURCE_MODE` to choose the actual Packager flag.",
        "",
        "| Source mode | Command | Ready now | Mode-specific blockers |",
        "| --- | --- | --- | --- |",
    ]
    for row in mode_rows:
        lines.append(
            f"| `{row['mode']}` | `{row['command']}` | {row['ready']} | {row['blockers']} |"
        )

    lines.extend(
        [
            "",
        "## GitHub API Credentials",
        "",
        f"- Credential source: `{auth_state}`",
        f"- Credential detail: `{auth_detail}`",
        "",
        "Local auth commands:",
        "",
        "```bash",
        "gh auth status -h github.com",
        "gh auth login -h github.com",
        "make github-auth-check",
        "```",
        "",
        "If you prefer not to refresh the persistent GitHub CLI login, export a",
        "short-lived token only for the packaging shell and rerun the same local",
        "checks before Packager:",
        "",
        "```bash",
        "export GH_TOKEN=REPLACE_WITH_SHORT_LIVED_TOKEN",
        "make github-auth-check",
        "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
        "```",
        "",
        "Never put `GH_TOKEN` in tracked files, generated reports, or shell",
        "history snippets committed to the repo.",
        "",
        "## Package Inputs",
        "",
            "| Input | Role | Present locally | Ignored by git | Tracked by git |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for path, present, ignored, tracked, role in input_status:
        lines.append(f"| `{path}` | {role} | {yes_no(present)} | {yes_no(ignored)} | {yes_no(tracked)} |")

    lines.extend(
        [
            "",
            "`sources/config.yaml` is checked here as a local build and repo-shape",
            "sanity input because the wrapper is shared by all source modes. It is",
            "not part of the selected latest-release `source.files` mapping unless",
            "the final strategy changes to build-from-source or Google Fonts review",
            "asks for build metadata.",
        ]
    )

    lines.extend(
        [
            "",
            "## Wrapper Alignment",
            "",
            "This report and `scripts/package_gf_dry_run.sh` must reject the same",
            "known-bad inputs before Packager runs. These checks compare the",
            "report's Python-side constants with the shell wrapper's actual lists.",
            "",
            f"- Required inputs in report: {len(REQUIRED_PACKAGE_INPUTS)}",
            f"- Required inputs in wrapper: {len(wrapper_inputs)}",
            f"- Required inputs missing from wrapper: {', '.join(f'`{item}`' for item in sorted(set(REQUIRED_PACKAGE_INPUTS) - set(wrapper_inputs))) if not input_lists_match else 'none'}",
            f"- Extra required inputs in wrapper: {', '.join(f'`{item}`' for item in sorted(set(wrapper_inputs) - set(REQUIRED_PACKAGE_INPUTS))) if not input_lists_match else 'none'}",
            f"- Starter markers in report: {len(STARTER_TEMPLATE_MARKERS)}",
            f"- Starter markers in wrapper: {len(wrapper_markers)}",
            f"- Starter markers missing from wrapper: {', '.join(f'`{item}`' for item in sorted(set(STARTER_TEMPLATE_MARKERS) - set(wrapper_markers))) if not marker_lists_match else 'none'}",
            f"- Extra starter markers in wrapper: {', '.join(f'`{item}`' for item in sorted(set(wrapper_markers) - set(STARTER_TEMPLATE_MARKERS))) if not marker_lists_match else 'none'}",
            f"- Unresolved markers in report: {len(UNRESOLVED_METADATA_MARKERS)}",
            f"- Unresolved markers in wrapper: {len(wrapper_unresolved)}",
            f"- Unresolved markers missing from wrapper: {', '.join(f'`{item}`' for item in sorted(set(UNRESOLVED_METADATA_MARKERS) - set(wrapper_unresolved))) if not unresolved_lists_match else 'none'}",
            f"- Extra unresolved markers in wrapper: {', '.join(f'`{item}`' for item in sorted(set(wrapper_unresolved) - set(UNRESOLVED_METADATA_MARKERS))) if not unresolved_lists_match else 'none'}",
            f"- Source modes in report: {', '.join(f'`{item}`' for item in sorted(expected_modes_without_empty))}",
            f"- Source modes in wrapper: {', '.join(f'`{item}`' for item in sorted(item for item in wrapper_modes if item))}",
            f"- Release-archive verifier wired in wrapper: {yes_no(wrapper_release_archive_gate)}",
            "",
            "",
            "## Downstream Metadata State",
            "",
            f"- Existing downstream metadata path: `{METADATA_PATH}`",
            f"- Existing downstream METADATA.pb present: {yes_no(metadata_exists)}",
            f"- Existing downstream METADATA.pb has placeholder upstream URL: {yes_no(metadata_placeholder)}",
            f"- Existing downstream METADATA.pb has unresolved markers: {yes_no(bool(metadata_unresolved_markers))}",
            f"- Existing downstream METADATA.pb unresolved markers: {', '.join(f'`{marker}`' for marker in metadata_unresolved_markers) if metadata_unresolved_markers else 'none'}",
            f"- Existing downstream METADATA.pb is starter template: {yes_no(metadata_starter_template)}",
            f"- Existing downstream METADATA.pb starter markers: {', '.join(f'`{marker}`' for marker in metadata_starter_markers) if metadata_starter_markers else 'none'}",
            f"- Existing downstream METADATA.pb source-mode blockers: {', '.join(f'`{error}`' for error in metadata_source_errors) if metadata_source_errors else 'none'}",
            "",
            "Safe local sequence after final release/source metadata is ready:",
            "",
            "```bash",
            "gh auth status -h github.com",
            "make github-auth-check",
            "git -C /Users/eli/GH/forks/fonts status --short -- ofl/virtuagrotesk",
            "git -C /Users/eli/GH/forks/fonts status --short",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check",
            "./venv/bin/python scripts/prepare_downstream_metadata.py --apply",
            "git -C /Users/eli/GH/forks/fonts diff -- ofl/virtuagrotesk/METADATA.pb",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
            "```",
            "",
            "Do not run Packager with `-p` until the no-PR dry run has reached",
            "Packager, the generated `ofl/virtuagrotesk` package has been reviewed,",
            "and the Google Fonts Add Font issue exists.",
            "",
            "## Apply Before Running Packager",
            "",
            *next_actions,
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_package_dry_run_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
