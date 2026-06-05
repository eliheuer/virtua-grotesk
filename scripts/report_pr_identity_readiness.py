#!/usr/bin/env python3
"""Report local PR identity and GitHub auth readiness for Google Fonts."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/pr-identity-readiness.md")
GF_REPO_PATH = Path(os.environ["GF_REPO_PATH"]) if os.environ.get("GF_REPO_PATH") else Path("GF_REPO_PATH_NOT_CONFIGURED")


def display_path(path: Path) -> str:
    if path == ROOT:
        return "."
    if path == GF_REPO_PATH and path != Path("GF_REPO_PATH_NOT_CONFIGURED"):
        return "$GF_REPO_PATH"
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def git_config(repo: Path, key: str) -> str:
    if not (repo / ".git").exists():
        return ""
    _, output = run(["git", "config", "--get", key], cwd=repo)
    return output.strip()


def redact_email(email: str) -> str:
    if "@" not in email:
        return "configured, not an email-shaped value" if email else "missing"
    local, domain = email.split("@", 1)
    if not local:
        return f"*@{domain}"
    return f"{local[0]}***@{domain}"


def gh_status_summary(status_output: str, returncode: int) -> tuple[str, str, str]:
    account_match = re.search(r"account ([^ ]+)", status_output)
    account = account_match.group(1) if account_match else "unknown"
    if returncode == 0:
        status = "valid"
    elif "token" in status_output.lower() and "invalid" in status_output.lower():
        status = "invalid token"
    elif "not logged" in status_output.lower():
        status = "not logged in"
    else:
        status = "unknown failure"
    sanitized = re.sub(r"\s+", " ", status_output).strip()
    return status, account, sanitized


def github_api_credentials() -> tuple[bool, str, str]:
    if os.environ.get("GH_TOKEN"):
        return True, "explicit GH_TOKEN", "GH_TOKEN is set in the environment"
    token_returncode, token_output = run(["gh", "auth", "token"])
    if token_returncode == 0 and token_output:
        return True, "valid gh token", "gh auth token returned a token"
    status_returncode, status_output = run(["gh", "auth", "status", "-h", "github.com"])
    detail = re.sub(r"\s+", " ", status_output).strip() or f"gh auth status exit {status_returncode}"
    return False, "unavailable", detail


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def cla_status() -> str:
    decisions = (ROOT / "documentation/google-fonts/google-fonts-decisions.md").read_text(encoding="utf-8")
    match = re.search(
        r"## Family name, namecheck, trademarks, and CLA\s+Status: ([a-z]+)",
        decisions,
    )
    if match and match.group(1) == "decided":
        return "confirmed by maintainer for the copyright holder"
    return "pending maintainer confirmation"


def expected_cla_name() -> str:
    decisions = (ROOT / "documentation/google-fonts/google-fonts-decisions.md").read_text(encoding="utf-8")
    match = re.search(
        r"## Author/contact lines\s+Status: decided\s+Decision:\s+```text\s+([^`]+?)\s+```",
        decisions,
        flags=re.DOTALL,
    )
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else "Eli Heuer"


def identity_lines(repo_label: str, repo_path: Path, expected_name: str) -> tuple[list[str], dict[str, bool | str]]:
    git_name = git_config(repo_path, "user.name")
    git_email = git_config(repo_path, "user.email")
    repo_exists = (repo_path / ".git").exists()
    identity_complete = bool(git_name and git_email)
    name_matches_cla = git_name == expected_name
    state: dict[str, bool | str] = {
        "exists": repo_exists,
        "identity_complete": identity_complete,
        "name_matches_cla": name_matches_cla,
        "name": git_name,
        "email": git_email,
    }
    lines = [
        f"### {repo_label}",
        "",
        f"- Repo path: `{display_path(repo_path)}`",
        f"- Git checkout present: {yes_no(repo_exists)}",
        f"- git user.name configured: {yes_no(bool(git_name))}",
        f"- git user.email configured: {yes_no(bool(git_email))}",
        f"- git identity complete: {yes_no(identity_complete)}",
        f"- git user.name matches expected CLA/author name: {yes_no(name_matches_cla)}",
        f"- git user.name: `{git_name or 'missing'}`",
        f"- git user.email: `{redact_email(git_email)}`",
        "",
    ]
    return lines, state


def markdown_report() -> str:
    gh_returncode, gh_output = run(["gh", "auth", "status"])
    gh_status, gh_account, gh_summary = gh_status_summary(gh_output, gh_returncode)
    api_ready, credential_source, credential_detail = github_api_credentials()
    cla = cla_status()
    expected_name = expected_cla_name()
    source_lines, source_state = identity_lines("Source repo identity", ROOT, expected_name)
    gf_lines, gf_state = identity_lines("google/fonts fork identity", GF_REPO_PATH, expected_name)
    final_commit_identity_ready = (
        bool(gf_state["identity_complete"])
        and bool(gf_state["name_matches_cla"])
        and cla.startswith("confirmed")
    )

    lines = [
        "# PR Identity Readiness",
        "",
        (
            "This generated report records local Git and GitHub CLI identity "
            "state for the future Google Fonts issue and downstream PR. It reads "
            "the maintainer-confirmed Google CLA decision from the canonical "
            "decision log."
        ),
        "",
        "## Summary",
        "",
        f"- Expected CLA/author name: `{expected_name}`",
        f"- Source repo git identity complete: {yes_no(bool(source_state['identity_complete']))}",
        f"- Source repo git user.name matches expected CLA/author name: {yes_no(bool(source_state['name_matches_cla']))}",
        f"- google/fonts fork git checkout present: {yes_no(bool(gf_state['exists']))}",
        f"- google/fonts fork git identity complete: {yes_no(bool(gf_state['identity_complete']))}",
        f"- google/fonts fork git user.name matches expected CLA/author name: {yes_no(bool(gf_state['name_matches_cla']))}",
        f"- Final downstream commit identity ready: {yes_no(final_commit_identity_ready)}",
        f"- GitHub CLI auth status: `{gh_status}`",
        f"- GitHub CLI account: `{gh_account}`",
        f"- GitHub API credentials ready: {yes_no(api_ready)}",
        f"- GitHub API credential source: `{credential_source}`",
        f"- Google CLA status: {cla}",
        "",
        "## Git Identity Evidence",
        "",
        *source_lines,
        *gf_lines,
        "## GitHub CLI Evidence",
        "",
        f"- `gh auth status` exit code: {gh_returncode}",
        f"- Sanitized status: `{gh_summary or 'no output'}`",
        f"- Credential detail: `{credential_detail}`",
        "",
        "## Why This Matters",
        "",
        "- The Google Fonts PR guide asks contributors to sign the Google CLA.",
        "- The same guide asks contributors to configure Git commits with the",
        "  name and email that match the signed CLA identity.",
        "- The downstream Google Fonts commit will be made from the local",
        f"  `{GF_REPO_PATH}` checkout, so that repo's git identity is the final",
        "  commit-identity gate.",
        "- The local Packager dry run needs GitHub API access through `GH_TOKEN`",
        "  or equivalent authenticated GitHub CLI credentials.",
        "- The final downstream PR should not be opened until this identity state",
        "  matches the confirmed CLA identity.",
        "",
        "## Apply Before Downstream PR",
        "",
        "- Confirm the final commit identity matches the signed Google CLA identity.",
        "- Confirm the source repo and local `google/fonts` fork git name and",
        "  email match the CLA identity before making release or downstream commits.",
        f"- If the signed CLA identity should be `{expected_name}`, update the",
        "  repo-local identities before making downstream `google/fonts` commits:",
        "",
        "```bash",
        f"git config user.name \"{expected_name}\"",
        f"git -C {GF_REPO_PATH} config user.name \"{expected_name}\"",
        "```",
        "",
        "- Refresh GitHub CLI authentication before using `gh auth token` or",
        "  running `make package-dry-run` with API-backed downloads.",
        "- Alternatively, export a short-lived `GH_TOKEN` for the Packager dry",
        "  run if you do not want to refresh stored GitHub CLI credentials.",
        "- Rerun `make reports-only` after changing local Git or GitHub auth state.",
        "",
        "## Local Auth Commands",
        "",
        "These commands are intentionally local and do not open an issue, push a",
        "branch, or create a downstream PR:",
        "",
        "```bash",
        "gh auth status -h github.com",
        "gh auth login -h github.com",
        "make github-auth-check",
        "```",
        "",
        "If using a short-lived token instead of stored GitHub CLI credentials,",
        "set `GH_TOKEN` only for the command that needs it:",
        "",
        "```bash",
        "GH_TOKEN=<token> make github-auth-check",
        "GH_TOKEN=<token> GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run",
        "```",
        "",
        "References:",
        "",
        "- https://googlefonts.github.io/gf-guide/making-pr.html",
        "- https://googlefonts.github.io/gf-guide/onboarding.html",
        "- https://googlefonts.github.io/gf-guide/package.html",
        "",
    ]
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_pr_identity_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
