#!/usr/bin/env python3
"""Generate a GitHub release draft for the selected Google Fonts archive path."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/github-release-draft.md")
RELEASE_NOTES_DEFAULT = Path("documentation/github-release-notes.md")
LOCAL_ARCHIVE = Path("dist/VirtuaGrotesk-1.000.zip")
DOWNSTREAM_PREVIEW = Path("documentation/google-fonts-downstream-package-preview.md")


def read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8") if (ROOT / path).exists() else ""


def text_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def git_value(args: list[str], default: str = "unknown") -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else default


def git_ok(args: list[str]) -> bool:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def archive_source_files(preview_text: str) -> list[str]:
    return re.findall(r'source_file:\s*"([^"]+)"', preview_text)


def release_context() -> dict[str, str | list[str] | bool]:
    release_metadata = read_text(Path("documentation/release-metadata.md"))
    release_source = read_text(Path("documentation/release-source-readiness.md"))
    release_archive = read_text(Path("documentation/release-archive-manifest.md"))
    preview_text = read_text(DOWNSTREAM_PREVIEW)
    version = text_value(r"Source version: `([^`]+)`", release_metadata, "1.000")
    tag = text_value(r"Suggested first-submission tag: `([^`]+)`", release_metadata, f"v{version}")
    upstream_url = text_value(
        r"Normalized GitHub origin candidate: `([^`]+)`",
        release_source,
        "https://github.com/eliheuer/virtua-grotesk",
    )
    commit = git_value(["rev-parse", "HEAD"])
    short_commit = git_value(["rev-parse", "--short", "HEAD"])
    branch = git_value(["rev-parse", "--abbrev-ref", "HEAD"])
    tag_exists = git_ok(["rev-parse", "-q", "--verify", f"refs/tags/{tag}"])
    working_tree_clean = not bool(git_value(["status", "--porcelain"], ""))
    archive_url = text_value(r'archive_url:\s*"([^"]+)"', preview_text, "pending")
    source_commit_value = text_value(r'commit:\s*"([^"]+)"', preview_text, "missing")
    release_notes_source_commit_final = (
        source_commit_value == commit
        and not source_commit_value.startswith("Pending")
        and source_commit_value != "missing"
    )
    archive_exists = (ROOT / LOCAL_ARCHIVE).is_file()
    archive_contains_expected = text_value(
        r"Local release archive contains expected files: (yes|no)",
        release_archive,
        "unknown",
    )
    archive_hashes_match = text_value(
        r"Local release archive hashes match source files: (yes|no)",
        release_archive,
        "unknown",
    )
    archive_metadata_deterministic = text_value(
        r"Local release archive metadata deterministic: (yes|no)",
        release_archive,
        "unknown",
    )
    archive_sha256 = text_value(
        r"Local release archive SHA-256: `([^`]+)`",
        release_archive,
        "unknown",
    )
    archive_filename_matches = text_value(
        r"Preview archive filename matches local archive: (yes|no)",
        release_archive,
        "unknown",
    )
    archive_unsafe = text_value(
        r"Local release archive has unsafe paths: (yes|no)",
        release_archive,
        "unknown",
    )
    release_title = f"Virtua Grotesk {version}"
    source_files = archive_source_files(preview_text)
    return {
        "version": version,
        "tag": tag,
        "upstream_url": upstream_url,
        "commit": commit,
        "short_commit": short_commit,
        "branch": branch,
        "tag_exists": tag_exists,
        "working_tree_clean": working_tree_clean,
        "archive_url": archive_url,
        "source_commit_value": source_commit_value,
        "release_notes_source_commit_final": release_notes_source_commit_final,
        "archive_exists": archive_exists,
        "archive_contains_expected": archive_contains_expected,
        "archive_hashes_match": archive_hashes_match,
        "archive_metadata_deterministic": archive_metadata_deterministic,
        "archive_sha256": archive_sha256,
        "archive_filename_matches": archive_filename_matches,
        "archive_unsafe": archive_unsafe,
        "release_title": release_title,
        "source_files": source_files,
    }


def release_notes_text(context: dict[str, str | list[str] | bool]) -> str:
    source_files = context["source_files"]
    assert isinstance(source_files, list)
    lines = [
        f"Virtua Grotesk {context['version']} release candidate for Google Fonts onboarding.",
        "",
        "This release archive contains the files referenced by downstream",
        "`METADATA.pb` `source.files` for the selected latest-release Packager",
        "path.",
        "",
        f"Source commit: {context['commit']}",
        "Google Fonts source mode: latest-release",
        "",
        "Archive contents:",
    ]
    lines.extend(f"- `{source_file}`" for source_file in source_files)
    lines.append("")
    return "\n".join(str(line) for line in lines)


def markdown_report(context: dict[str, str | list[str] | bool]) -> str:
    source_files = context["source_files"]
    assert isinstance(source_files, list)

    lines = [
        "# GitHub Release Draft",
        "",
        "This generated draft records the GitHub release command and checks needed",
        "for the selected Google Fonts `latest-release` Packager path. It does",
        "not create a tag, push a tag, publish a release, or contact GitHub.",
        "",
        "## Summary",
        "",
        f"- Upstream URL: `{context['upstream_url']}`",
        f"- Current branch: `{context['branch']}`",
        f"- Current commit: `{context['commit']}`",
        f"- Current short commit: `{context['short_commit']}`",
        f"- Source version: `{context['version']}`",
        f"- Release tag: `{context['tag']}`",
        f"- Release title: `{context['release_title']}`",
        f"- Local tag already exists: {yes_no(bool(context['tag_exists']))}",
        f"- Working tree clean: {yes_no(bool(context['working_tree_clean']))}",
        f"- Local archive: `{LOCAL_ARCHIVE}`",
        f"- Local archive exists: {yes_no(bool(context['archive_exists']))}",
        f"- Local archive contains expected files: {context['archive_contains_expected']}",
        f"- Local archive hashes match source files: {context['archive_hashes_match']}",
        f"- Local archive metadata deterministic: {context['archive_metadata_deterministic']}",
        f"- Local archive SHA-256: `{context['archive_sha256']}`",
        f"- Local archive has unsafe paths: {context['archive_unsafe']}",
        f"- Preview archive filename matches local archive: {context['archive_filename_matches']}",
        f"- Release notes file: `{RELEASE_NOTES_DEFAULT}`",
        f"- Release notes source commit final: {yes_no(bool(context['release_notes_source_commit_final']))}",
            f"- Downstream preview archive URL: `{context['archive_url']}`",
            "- Downstream preview archive URL contract: GitHub release download `.zip`",
        f"- Downstream preview source commit: `{context['source_commit_value']}`",
        "",
        "## Release Asset Contract",
        "",
        "| Source path in archive | Required by downstream `source.files` |",
        "| --- | --- |",
    ]
    for source_file in source_files:
        lines.append(f"| `{source_file}` | yes |")

    lines.extend(
        [
            "",
            "## Draft Release Notes",
            "",
            "```markdown",
            release_notes_text(context).strip(),
            "```",
            "",
            "## Final Command Draft",
            "",
            "Run this only after drawing/source work is complete, the final source",
            "commit is made, the `v1.000` tag is created and pushed, and",
            "`make release-archive-verify` plus `make downstream-metadata-check`",
            "both pass, the generated release notes `Source commit` matches the",
            "final downstream `source.commit`, and the archive SHA-256 above is",
            "the intended release asset.",
            "",
            "```bash",
            f"gh release create {context['tag']} {LOCAL_ARCHIVE} \\",
            f"  --repo eliheuer/virtua-grotesk \\",
            f"  --title \"{context['release_title']}\" \\",
            f"  --notes-file {RELEASE_NOTES_DEFAULT}",
            "```",
            "",
            "## Post-Publish Verification",
            "",
            "Run these checks after the GitHub release asset is uploaded and",
            "before applying downstream metadata or running Packager. They verify",
            "that the public release URL resolves to the same archive reviewed",
            "locally.",
            "",
            "```bash",
            f"gh release view {context['tag']} --repo eliheuer/virtua-grotesk",
            f"gh release download {context['tag']} --repo eliheuer/virtua-grotesk --pattern {LOCAL_ARCHIVE.name} --dir /tmp/virtua-grotesk-release-check",
            f"shasum -a 256 /tmp/virtua-grotesk-release-check/{LOCAL_ARCHIVE.name}",
            f"unzip -l /tmp/virtua-grotesk-release-check/{LOCAL_ARCHIVE.name}",
            f"./venv/bin/python scripts/verify_release_archive.py --archive /tmp/virtua-grotesk-release-check/{LOCAL_ARCHIVE.name} --expected-sha256 {context['archive_sha256']}",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check",
            "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
            "```",
            "",
            f"Expected SHA-256: `{context['archive_sha256']}`",
            "",
            "The downloaded archive must contain exactly the `source.files` paths",
            "listed in the Release Asset Contract above, and the downstream",
            "`source.archive_url` must point at this uploaded GitHub release",
            "download `.zip` asset before the no-PR Packager dry run.",
            "",
            "## Before Publishing",
            "",
            "1. Run `make preflight` from the final source commit.",
            "2. Run `make release-archive-build` and `make release-archive-verify`.",
            "3. Create and push the final tag with the same value recorded in downstream metadata.",
            "4. Replace the pending downstream `source.commit` value with the final commit hash.",
            "5. Regenerate this draft so the release notes `Source commit` matches the final downstream `source.commit`.",
            "6. Confirm `source.archive_url` points to the uploaded GitHub release download `.zip` asset.",
            "7. Run `GFT_PACKAGER_SOURCE_MODE=latest-release make downstream-metadata-check`.",
            "8. Run the no-PR `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_github_release_draft.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    context = release_context()
    output_path.write_text(markdown_report(context), encoding="utf-8")
    notes_path = ROOT / RELEASE_NOTES_DEFAULT
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(release_notes_text(context), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
