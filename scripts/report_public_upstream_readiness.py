#!/usr/bin/env python3
"""Generate a public upstream URL decision-readiness report."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/public-upstream-readiness.md")
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"
PLACEHOLDER_DISPLAY_URL = "github.com/fontgarden/virtua-grotesk"

SEARCH_PATHS = [
    "OFL.txt",
    "sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist",
    "sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist",
    "scripts/fix_gf_metadata.py",
    "documentation/ARTICLE.en_us.html",
    "documentation/google-fonts-decision-questions.md",
    "documentation/google-fonts-decisions.md",
    "documentation/google-fonts-downstream-package-preview.md",
    "documentation/google-fonts-metadata-review.md",
    "documentation/google-fonts-package-checklist.md",
    "documentation/google-fonts-submission-handoff.md",
]
STALE_GUARD_PATHS = [
    "scripts/package_gf_dry_run.sh",
]
APPLY_HELPER = ROOT / "scripts" / "apply_public_upstream_url.py"


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def normalize_github_url(remote: str) -> str:
    remote = remote.strip()
    ssh_match = re.match(r"git@github\.com:([^/]+/[^.]+)(?:\.git)?$", remote)
    if ssh_match:
        return f"https://github.com/{ssh_match.group(1)}"
    https_match = re.match(r"https://github\.com/([^/]+/[^.]+)(?:\.git)?$", remote)
    if https_match:
        return f"https://github.com/{https_match.group(1)}"
    return remote


def placeholder_findings() -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for relative in SEARCH_PATHS:
        path = ROOT / relative
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if PLACEHOLDER_URL in line or "Pending decision: public upstream URL" in line:
                findings.append((relative, line_number, line.strip()))
    return findings


def stale_guard_findings() -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for relative in STALE_GUARD_PATHS:
        path = ROOT / relative
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if PLACEHOLDER_URL in line:
                findings.append((relative, line_number, line.strip()))
    return findings


def helper_target_files() -> list[str]:
    if not APPLY_HELPER.exists():
        return []
    tree = ast.parse(APPLY_HELPER.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "TARGET_FILES" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value
    return []


def candidate_text(text: str, normalized_origin: str) -> str:
    display_origin = normalized_origin.replace("https://", "")
    return (
        text.replace(PLACEHOLDER_URL, normalized_origin)
        .replace(PLACEHOLDER_DISPLAY_URL, display_origin)
        .replace("Pending decision: public upstream URL", normalized_origin)
    )


def markdown_report() -> str:
    origin_fetch = git_output("remote", "get-url", "origin")
    origin_push = git_output("remote", "get-url", "--push", "origin")
    current_branch = git_output("branch", "--show-current") or "unknown"
    normalized_origin = normalize_github_url(origin_fetch)
    findings = placeholder_findings()
    stale_guards = stale_guard_findings()
    helper_targets = helper_target_files()
    report_target_set = set(SEARCH_PATHS)
    helper_target_set = set(helper_targets)
    missing_from_helper = sorted(report_target_set - helper_target_set)
    extra_in_helper = sorted(helper_target_set - report_target_set)
    differs = "yes" if normalized_origin and normalized_origin != PLACEHOLDER_URL else "no"

    lines = [
        "# Public Upstream URL Readiness",
        "",
        "This generated report keeps the public upstream URL decision tied to the",
        "current git remote and the exact files that still carry placeholder or",
        "pending downstream URL text.",
        "",
        "## Current Local Git Evidence",
        "",
        f"- Current branch: `{current_branch}`",
        f"- Origin fetch URL: `{origin_fetch or 'unset'}`",
        f"- Origin push URL: `{origin_push or 'unset'}`",
        f"- Normalized GitHub origin candidate: `{normalized_origin or 'unset'}`",
        f"- Placeholder URL: `{PLACEHOLDER_URL}`",
        f"- Origin candidate differs from placeholder: {differs}",
        f"- Apply helper: `{APPLY_HELPER.relative_to(ROOT)}`",
        f"- Report/helper target lists match: {'yes' if not missing_from_helper and not extra_in_helper else 'no'}",
        "",
        "## Replacement Surface",
        "",
        f"- Placeholder or pending URL findings: {len(findings)}",
        "",
        "| File | Line | Text |",
        "| --- | ---: | --- |",
    ]

    for relative, line_number, text in findings:
        escaped = text.replace("|", "\\|")
        lines.append(f"| `{relative}` | {line_number} | `{escaped}` |")

    lines.extend(
        [
            "",
            "## Candidate Replacement Preview",
            "",
            "This preview does not apply the decision. It shows the exact replacement",
            "target if the normalized origin candidate is approved as the canonical",
            "public upstream URL.",
            "",
            f"- Candidate URL: `{normalized_origin or 'unset'}`",
            f"- Candidate copyright line: `Copyright 2025 The Virtua Grotesk Project Authors ({normalized_origin or 'unset'})`",
            f"- Placeholder URL replacements: {sum(1 for _, _, text in findings if PLACEHOLDER_URL in text)}",
            f"- Pending URL field replacements: {sum(1 for _, _, text in findings if 'Pending decision: public upstream URL' in text)}",
            "",
            "| File | Line | Candidate text |",
            "| --- | ---: | --- |",
        ]
    )
    for relative, line_number, text in findings:
        escaped = candidate_text(text, normalized_origin or "unset").replace("|", "\\|")
        lines.append(f"| `{relative}` | {line_number} | `{escaped}` |")

    lines.extend(
        [
            "",
            "## Apply Helper Alignment",
            "",
            "The dry-run/apply helper and this report must stay aligned so the",
            "maintainer-approved URL replacement cannot miss a public metadata",
            "surface that the readiness report already identified.",
            "",
            f"- Report target files: {len(SEARCH_PATHS)}",
            f"- Helper target files: {len(helper_targets)}",
            f"- Missing from helper: {', '.join(f'`{path}`' for path in missing_from_helper) if missing_from_helper else 'none'}",
            f"- Extra in helper: {', '.join(f'`{path}`' for path in extra_in_helper) if extra_in_helper else 'none'}",
            "",
            "## Stale Placeholder Guards",
            "",
            "These internal guards intentionally retain the old placeholder URL so",
            "stale downstream metadata from earlier dry runs cannot be reused after",
            "the final public URL decision is applied. Do not replace these with the",
            "final canonical URL.",
            "",
            f"- Internal stale-placeholder guards: {len(stale_guards)}",
            "",
            "| File | Line | Guard text |",
            "| --- | ---: | --- |",
        ]
    )
    for relative, line_number, text in stale_guards:
        escaped = text.replace("|", "\\|")
        lines.append(f"| `{relative}` | {line_number} | `{escaped}` |")

    lines.extend(
        [
            "",
            "## Apply Before Final Packaging",
            "",
            "- Keep the normalized origin candidate as the public canonical",
            "  upstream URL for Google Fonts.",
            "- Replace the placeholder URL consistently in `OFL.txt`, UFO font",
            "  metadata, generated metadata patching, downstream package preview,",
            "  and handoff docs.",
            "- Rebuild fonts so generated name ID 0 and generated metadata reports",
            "  carry the final URL.",
            "- Rerun `make preflight` so proof evidence and generated reports",
            "  stay synchronized, then run",
            "  `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run` after",
            "  the selected release/archive exposes all `source.files` paths.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/upstream.html",
            "- https://googlefonts.github.io/gf-guide/package.html",
            "- https://googlefonts.github.io/gf-guide/making-pr.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_public_upstream_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
