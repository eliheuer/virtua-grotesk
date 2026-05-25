#!/usr/bin/env python3
"""Report local workflow readiness for Google Fonts handoff work."""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = ROOT / "documentation/local-workflow-readiness.md"
GF_REPO_PATH = Path(os.environ.get("GF_REPO_PATH", "/Users/eli/GH/forks/fonts"))
DRAWBOT_SKIA_REPO = Path("/Users/eli/GH/repos/drawbot-skia")
FONTSPECTOR_HOME = Path.home() / ".fontspector"
PROOF_PDF = ROOT / "proof.pdf"
GFT_QA_OUTPUT = ROOT / "documentation/gftools-qa/Proof"
EXPECTED_FONTS = [
    ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
EXPECTED_TARGETS = [
    "decisions",
    "decision-readiness-check",
    "next-actions",
    "blockers",
    "issue-draft",
    "handoff-readiness-check",
    "release-check",
    "release-archive-check",
    "release-archive-build",
    "release-archive-verify",
    "release-archive-test",
    "release-draft-check",
    "source-strategy-check",
    "package-readiness-check",
    "recent-gf-check",
    "family-name-check",
    "authorship-check",
    "pr-readiness-check",
    "vendor-id-check",
    "kerning-check",
    "kerning-proof-check",
    "kerning-proof-review-check",
    "pua-scope-check",
    "avar-check",
    "warnings-check",
    "github-auth-check",
    "designer-profile-check",
    "designer-profile-prepare-check",
    "designer-profile-info-check",
    "designer-profile-image-check",
    "designer-profile-bio-check",
    "designer-profile-validator-test",
    "public-upstream-url-check",
    "downstream-metadata-check",
    "downstream-metadata-helper-test",
    "package-wrapper-test",
    "build",
    "test",
    "reports",
    "reports-only",
    "preflight",
    "preflight-only",
    "proof",
    "proof-only",
    "handoff",
    "package-dry-run",
    "clean",
]
EXPECTED_REPORTS = [
    "documentation/final-submission-blockers.md",
    "documentation/next-actions.md",
    "documentation/package-dry-run-readiness.md",
    "documentation/drawbot-runtime-readiness.md",
    "documentation/submission-handoff-readiness.md",
    "documentation/release-archive-manifest.md",
    "documentation/github-release-draft.md",
    "documentation/github-release-notes.md",
    "documentation/missing-gf-arabic-core.md",
    "documentation/arabic-mark-readiness.md",
    "documentation/arabic-shaping-smoke-test.md",
    "documentation/fontspector-googlefonts-report.md",
]
PYTHON_PACKAGES = [
    "diffenator2",
    "fontTools",
    "glyphsets",
    "git",
    "uharfbuzz",
    "yaml",
]
EXPECTED_DIRECT_REQUIREMENTS = {
    "fontmake",
    "fonttools",
    "gftools[qa]",
    "GitPython",
    "glyphsets",
    "PyYAML",
    "uharfbuzz",
}


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def importable(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def requirement_name(line: str) -> str:
    name = re.split(r"==|>=|<=|~=|!=|<|>|;", line.strip(), maxsplit=1)[0]
    return name.split("[", 1)[0]


def meaningful_requirement_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def make_targets() -> set[str]:
    makefile = (ROOT / "Makefile").read_text()
    targets: set[str] = set()
    for line in makefile.splitlines():
        if not line or line.startswith("\t") or line.startswith("."):
            continue
        if ":" not in line:
            continue
        head = line.split(":", 1)[0].strip()
        if head and " " not in head and "=" not in head:
            targets.add(head)
    return targets


def make_target_recipe(makefile_text: str, target: str) -> str:
    marker = f"{target}:"
    start = makefile_text.find(marker)
    if start == -1:
        return ""
    recipe_lines: list[str] = []
    for line in makefile_text[start + len(marker) :].splitlines()[1:]:
        if line and not line.startswith("\t"):
            break
        if line.startswith("\t"):
            recipe_lines.append(line)
    return "\n".join(recipe_lines)


def command_safety_rows(makefile_text: str) -> list[tuple[str, bool, str]]:
    package_recipe = make_target_recipe(makefile_text, "package-dry-run")
    package_test_recipe = make_target_recipe(makefile_text, "package-wrapper-test")
    designer_profile_test_recipe = make_target_recipe(makefile_text, "designer-profile-validator-test")
    release_archive_test_recipe = make_target_recipe(makefile_text, "release-archive-test")
    metadata_recipe = make_target_recipe(makefile_text, "downstream-metadata-check")
    metadata_test_recipe = make_target_recipe(makefile_text, "downstream-metadata-helper-test")
    proof_recipe = make_target_recipe(makefile_text, "proof-only")
    package_script = (ROOT / "scripts/package_gf_dry_run.sh").read_text()
    metadata_helper = (ROOT / "scripts/prepare_downstream_metadata.py").read_text()
    return [
        (
            "GF_REPO_PATH defaults to local google/fonts fork",
            "GF_REPO_PATH ?= /Users/eli/GH/forks/fonts" in makefile_text,
            "`GF_REPO_PATH ?= /Users/eli/GH/forks/fonts`",
        ),
        (
            "package-dry-run target invokes local wrapper",
            "scripts/package_gf_dry_run.sh" in package_recipe,
            "`make package-dry-run` -> `scripts/package_gf_dry_run.sh`",
        ),
        (
            "package-dry-run target omits PR creation flags",
            "-p" not in package_recipe and "--pr" not in package_recipe,
            "Make target does not pass `-p` or `--pr`.",
        ),
        (
            "package-dry-run wrapper does not add PR creation flags",
            'packager_args+=("-p")' not in package_script
            and 'packager_args+=("--pr")' not in package_script,
            "Wrapper builds Packager args without PR flags.",
        ),
        (
            "package wrapper metadata gates have a local test",
            "scripts/test_package_gf_dry_run_gates.sh" in package_test_recipe,
            "`make package-wrapper-test` exercises source-mode metadata blockers.",
        ),
        (
            "designer profile validators and prepare helper have a local test",
            "scripts/test_designer_profile_validators.sh" in designer_profile_test_recipe,
            "`make designer-profile-validator-test` exercises info.pb, image, bio, and guarded prepare-helper blockers.",
        ),
        (
            "release archive path-safety gates have a local test",
            "scripts/test_release_archive_gates.sh" in release_archive_test_recipe,
            "`make release-archive-test` exercises unsafe source/destination paths, duplicate source/destination mappings, deterministic metadata, and SHA mismatch blockers.",
        ),
        (
            "downstream-metadata-check target is preview-only",
            "--apply" not in metadata_recipe,
            "`make downstream-metadata-check` does not pass `--apply`.",
        ),
        (
            "downstream metadata apply remains explicit",
            "--apply" in metadata_helper and "Dry run only" in metadata_helper,
            "Use `scripts/prepare_downstream_metadata.py --apply` only after review.",
        ),
        (
            "downstream metadata helper final-value gates have a local test",
            "scripts/test_downstream_metadata_helper.sh" in metadata_test_recipe,
            "`make downstream-metadata-helper-test` checks final date and source commit validation.",
        ),
        (
            "Packager source mode is surfaced",
            "GFT_PACKAGER_SOURCE_MODE" in makefile_text
            and "GFT_PACKAGER_SOURCE_MODE" in package_script
            and "GFT_PACKAGER_SOURCE_MODE" in metadata_helper,
            "`GFT_PACKAGER_SOURCE_MODE` is shared by metadata preview and Packager dry run.",
        ),
        (
            "proof target uses eliheuer/drawbot-skia fork",
            "$(DRAWBOT_SKIA_REPO)/src" in proof_recipe and "$(DRAWBOT_PYTHON)" in proof_recipe,
            "`make proof-only` runs the fork venv with the fork source on `PYTHONPATH`.",
        ),
    ]


def git_value(repo: Path, args: list[str]) -> str:
    if not (repo / ".git").exists():
        return "missing"
    result = run(["git", "-C", str(repo), *args], ROOT)
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip()


def git_ahead_behind(repo: Path, left: str, right: str) -> tuple[str, str]:
    if not (repo / ".git").exists():
        return "missing", "missing"
    output = git_value(repo, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    parts = output.split()
    if len(parts) != 2:
        return "unknown", "unknown"
    return parts[0], parts[1]


def gh_auth_ready() -> tuple[bool, str]:
    gh = shutil.which("gh")
    if gh is None:
        return False, "gh not installed"
    token = os.environ.get("GH_TOKEN", "").strip()
    if token:
        return True, "GH_TOKEN set"
    token_result = run([gh, "auth", "token"])
    if token_result.returncode == 0:
        return True, "gh auth token returned a token"
    status_result = run([gh, "auth", "status", "-h", "github.com"])
    detail = " ".join((status_result.stdout + " " + status_result.stderr).split())
    return False, detail or "gh auth token failed"


def command_output(command: list[str]) -> str:
    if not command[0]:
        return "missing"
    result = run(command)
    if result.returncode != 0:
        return "unavailable"
    return " ".join(result.stdout.split()) or "no output"


def read_existing_report(path: str) -> str:
    report_path = ROOT / path
    if not report_path.exists():
        return ""
    return report_path.read_text(encoding="utf-8")


def report_value(pattern: str, text: str, default: str = "unknown") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def pdf_page_count(path: Path) -> int:
    if not path.exists():
        return 0
    data = path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page\b", data))


def gftools_proof_html_count() -> int:
    return len(list(GFT_QA_OUTPUT.glob("*.html")))


def gftools_proof_covers_expected_instances() -> bool:
    expected_instances = {"Regular", "Medium", "SemiBold", "Bold"}
    proof_instances = {
        html.name.split("-diffbrowsers_", 1)[0]
        for html in GFT_QA_OUTPUT.glob("*-diffbrowsers_proofer.html")
    }
    return expected_instances.issubset(proof_instances)


def main() -> int:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_DEFAULT
    if len(sys.argv) > 2:
        raise SystemExit("usage: report_local_workflow_readiness.py [output.md]")

    targets = make_targets()
    makefile_text = (ROOT / "Makefile").read_text()
    safety_rows = command_safety_rows(makefile_text)
    safety_ready = all(row[1] for row in safety_rows)
    missing_targets = [target for target in EXPECTED_TARGETS if target not in targets]
    missing_reports = [path for path in EXPECTED_REPORTS if not (ROOT / path).exists()]
    missing_fonts = [path for path in EXPECTED_FONTS if not path.exists()]
    missing_packages = [name for name in PYTHON_PACKAGES if not importable(name)]
    direct_requirement_lines = meaningful_requirement_lines(ROOT / "requirements.in")
    pinned_requirement_lines = meaningful_requirement_lines(ROOT / "requirements.txt")
    direct_requirements = set(direct_requirement_lines)
    pinned_requirement_names = {requirement_name(line) for line in pinned_requirement_lines}
    expected_install_packages = {
        requirement_name(requirement)
        for requirement in EXPECTED_DIRECT_REQUIREMENTS
    }
    direct_requirements_expected = direct_requirements == EXPECTED_DIRECT_REQUIREMENTS
    pinned_requirements_all_pinned = all("==" in line for line in pinned_requirement_lines)
    pinned_requirements_include_transitives = len(pinned_requirement_lines) > len(direct_requirement_lines)
    pinned_requirements_include_direct = expected_install_packages.issubset(pinned_requirement_names)
    direct_requirements_include_fontbakery = any(
        requirement_name(line).lower() == "fontbakery" for line in direct_requirement_lines
    )
    pinned_requirements_include_fontbakery = "fontbakery" in {
        name.lower() for name in pinned_requirement_names
    }
    fontbakery_transitive_only = (
        pinned_requirements_include_fontbakery and not direct_requirements_include_fontbakery
    )
    requirements_ready = (
        direct_requirements_expected
        and pinned_requirements_all_pinned
        and pinned_requirements_include_transitives
        and pinned_requirements_include_direct
    )
    package_dry_run_text = read_existing_report("documentation/package-dry-run-readiness.md")
    package_report_reaches_packager = report_value(
        r"Wrapper can reach Packager: (yes|no)",
        package_dry_run_text,
    )
    package_report_first_blocker = report_value(
        r"First blocker: ([^\n]+)",
        package_dry_run_text,
    )
    package_report_blocking_findings = report_value(
        r"Blocking findings: ([^\n]+)",
        package_dry_run_text,
    )
    package_report_auth_ready = report_value(
        r"GitHub API credentials ready: (yes|no)",
        package_dry_run_text,
    )
    package_report_gf_ready = report_value(
        r"Local google/fonts fork ready: (yes|no)",
        package_dry_run_text,
    )
    package_report_inputs_ready = report_value(
        r"Required local package inputs ready: (yes|no)",
        package_dry_run_text,
    )

    fontspector = shutil.which("fontspector")
    fontspector_version = command_output([fontspector, "--version"]) if fontspector else "missing"
    fontspector_templates = FONTSPECTOR_HOME / "templates"
    fontspector_templates_ready = (
        (fontspector_templates / "markdown/main.markdown").exists()
        and (fontspector_templates / "html/main.html").exists()
    )
    designbot = shutil.which("designbot")
    gftools_builder = importable("gftools.builder")
    gftools_packager = importable("gftools.packager")
    gftools_qa_ready = importable("diffenator2") and (ROOT / "venv/bin/gftools").exists()
    gftools_proof_count = gftools_proof_html_count()
    gftools_proof_output = gftools_proof_count > 0
    gftools_proof_instances = gftools_proof_covers_expected_instances()

    gh_ready, gh_detail = gh_auth_ready()
    package_auth_ready = package_report_auth_ready == "yes"
    drawbot_python = DRAWBOT_SKIA_REPO / ".venv/bin/python"
    drawbot_src = DRAWBOT_SKIA_REPO / "src"
    drawbot_ready = DRAWBOT_SKIA_REPO.exists() and drawbot_python.exists() and drawbot_src.exists()
    proof_pdf_exists = PROOF_PDF.exists()
    proof_pdf_size = PROOF_PDF.stat().st_size if proof_pdf_exists else 0
    proof_pdf_pages = pdf_page_count(PROOF_PDF)
    gf_branch = git_value(GF_REPO_PATH, ["rev-parse", "--abbrev-ref", "HEAD"])
    gf_tracking = git_value(GF_REPO_PATH, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    gf_origin_ahead, gf_origin_behind = git_ahead_behind(GF_REPO_PATH, "main", "origin/main")
    gf_upstream_ahead, gf_upstream_behind = git_ahead_behind(GF_REPO_PATH, "main", "upstream/main")
    gf_status = git_value(GF_REPO_PATH, ["status", "--porcelain"])
    gf_dirty_outside_family = [
        line
        for line in gf_status.splitlines()
        if len(line) > 3 and not line[3:].startswith("ofl/virtuagrotesk/")
    ]
    gf_ready = (
        (GF_REPO_PATH / ".git").exists()
        and git_value(GF_REPO_PATH, ["remote", "get-url", "upstream"]) == "https://github.com/google/fonts.git"
        and gf_branch == "main"
        and gf_tracking == "origin/main"
        and gf_origin_ahead == "0"
        and gf_origin_behind == "0"
        and gf_upstream_ahead == "0"
        and gf_upstream_behind == "0"
        and not gf_dirty_outside_family
    )

    preflight_ready = (
        not missing_targets
        and not missing_reports
        and not missing_fonts
        and not missing_packages
        and requirements_ready
        and bool(fontspector)
        and gftools_builder
        and gftools_packager
    )
    proof_ready = drawbot_ready
    package_ready = preflight_ready and package_report_reaches_packager == "yes"

    lines = [
        "# Local Workflow Readiness",
        "",
        "This generated report summarizes whether the local checkout can run the main Google Fonts handoff commands. It is intentionally local-state focused and does not run a build, proof, Fontspector, or Packager.",
        "",
        "## Summary",
        "",
        f"- Python executable: `{sys.executable}`",
        f"- Expected project venv: `{ROOT / 'venv/bin/python'}`",
        f"- Main Make targets present: {yes_no(not missing_targets)}",
        f"- Built font outputs present: {yes_no(not missing_fonts)}",
        f"- Required generated reports present: {yes_no(not missing_reports)}",
        f"- Python package imports ready: {yes_no(not missing_packages)}",
        f"- requirements.in direct dependencies expected: {yes_no(direct_requirements_expected)}",
        f"- requirements.in direct dependencies: {len(direct_requirement_lines)}",
        f"- requirements.txt pinned packages: {len(pinned_requirement_lines)}",
        f"- requirements.txt fully pinned: {yes_no(pinned_requirements_all_pinned)}",
        f"- requirements.txt includes transitive dependencies: {yes_no(pinned_requirements_include_transitives)}",
        f"- requirements.txt includes direct dependency package names: {yes_no(pinned_requirements_include_direct)}",
        f"- requirements.in directly includes FontBakery: {yes_no(direct_requirements_include_fontbakery)}",
        f"- requirements.txt includes FontBakery transitively: {yes_no(fontbakery_transitive_only)}",
        f"- Automated QA entrypoint remains Fontspector: {yes_no(bool(fontspector) and not direct_requirements_include_fontbakery)}",
        f"- Fontspector command available: {yes_no(bool(fontspector))}",
        f"- Fontspector command path: `{fontspector or 'missing'}`",
        f"- Fontspector version: `{fontspector_version}`",
        f"- Fontspector home exists: {yes_no(FONTSPECTOR_HOME.exists())}",
        f"- Fontspector local templates ready: {yes_no(fontspector_templates_ready)}",
        f"- gftools builder importable: {yes_no(gftools_builder)}",
        f"- gftools packager importable: {yes_no(gftools_packager)}",
        f"- gftools QA proof tooling ready: {yes_no(gftools_qa_ready)}",
        f"- gftools QA proof output present: {yes_no(gftools_proof_output)}",
        f"- gftools QA proof HTML files: {gftools_proof_count}",
        f"- gftools QA proof covers expected instances: {yes_no(gftools_proof_instances)}",
        f"- DrawBot fork runtime ready: {yes_no(proof_ready)}",
        f"- Proof PDF artifact present: {yes_no(proof_pdf_exists)}",
        f"- Proof PDF page count: {proof_pdf_pages}",
        f"- Local google/fonts fork ready: {yes_no(gf_ready)}",
        f"- Local google/fonts branch: `{gf_branch}`",
        f"- Local google/fonts tracking branch: `{gf_tracking}`",
        f"- Local google/fonts main vs origin/main: {gf_origin_ahead} ahead, {gf_origin_behind} behind",
        f"- Local google/fonts main vs upstream/main: {gf_upstream_ahead} ahead, {gf_upstream_behind} behind",
        f"- Local google/fonts dirty paths outside `ofl/virtuagrotesk`: {len(gf_dirty_outside_family)}",
        f"- GitHub API credentials ready: {yes_no(package_auth_ready)}",
        f"- Local preflight command ready to run: {yes_no(preflight_ready)}",
        f"- Proof command ready to run: {yes_no(proof_ready)}",
        f"- Command safety gates ready: {yes_no(safety_ready)}",
        f"- Package dry-run ready to reach Packager: {yes_no(package_ready)}",
        f"- Package dry-run report says wrapper can reach Packager: {package_report_reaches_packager}",
        f"- Package dry-run first blocker: {package_report_first_blocker}",
        f"- Package dry-run blocking findings: {package_report_blocking_findings}",
        "",
        "## Make Targets",
        "",
        "| Target | Present |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{target}` | {yes_no(target in targets)} |" for target in EXPECTED_TARGETS)
    lines.extend(
        [
            "",
            "## Command Safety Gates",
            "",
            "| Gate | Pass | Evidence |",
            "| --- | --- | --- |",
        ]
    )
    lines.extend(f"| {name} | {yes_no(passed)} | {evidence} |" for name, passed, evidence in safety_rows)
    lines.extend(
        [
        "",
        "## External Commands",
            "",
            f"- `fontspector`: `{fontspector or 'missing'}`",
            f"- `fontspector --version`: `{fontspector_version}`",
            f"- `~/.fontspector`: `{FONTSPECTOR_HOME}`",
            f"- Fontspector templates directory exists: {yes_no(fontspector_templates.exists())}",
            f"- Fontspector markdown template exists: {yes_no((fontspector_templates / 'markdown/main.markdown').exists())}",
            f"- Fontspector HTML template exists: {yes_no((fontspector_templates / 'html/main.html').exists())}",
            f"- `designbot`: `{designbot or 'missing'}`",
            f"- GitHub auth detail: `{gh_detail}`",
            f"- Package report GitHub API credentials ready: {package_report_auth_ready}",
            "",
            "## Python Requirements Snapshot",
            "",
            f"- Direct dependency file: `requirements.in`",
            f"- Direct dependencies match expected onboarding set: {yes_no(direct_requirements_expected)}",
            f"- Direct dependency count: {len(direct_requirement_lines)}",
            f"- Pinned install snapshot: `requirements.txt`",
            f"- Pinned package count: {len(pinned_requirement_lines)}",
            f"- Fully pinned with `==`: {yes_no(pinned_requirements_all_pinned)}",
            f"- Includes transitive dependencies: {yes_no(pinned_requirements_include_transitives)}",
            f"- Includes direct dependency package names: {yes_no(pinned_requirements_include_direct)}",
            f"- Direct FontBakery dependency: {yes_no(direct_requirements_include_fontbakery)}",
            f"- Transitive FontBakery pin from `gftools[qa]`: {yes_no(fontbakery_transitive_only)}",
            "- FontBakery appears in the pinned snapshot only because current `gftools[qa]` depends on it; local automated QA still runs Fontspector.",
            "- Refresh command: `./venv/bin/python -m pip freeze --all > requirements.txt`",
            "",
            "| Direct requirement | Present in pinned snapshot |",
            "| --- | --- |",
        ]
    )
    lines.extend(
        f"| `{requirement}` | {yes_no(requirement_name(requirement) in pinned_requirement_names)} |"
        for requirement in sorted(EXPECTED_DIRECT_REQUIREMENTS, key=str.lower)
    )
    lines.extend(
        [
            "",
            "## Required Generated Reports",
            "",
            "| Report | Present |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{path}` | {yes_no((ROOT / path).exists())} |" for path in EXPECTED_REPORTS)
    lines.extend(
        [
            "",
            "## Built Fonts",
            "",
            "| Font | Present |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{path.relative_to(ROOT)}` | {yes_no(path.exists())} |" for path in EXPECTED_FONTS)
    lines.extend(
        [
            "",
            "## Proof Artifact",
            "",
            f"- Path: `{PROOF_PDF.relative_to(ROOT)}`",
            f"- Exists: {yes_no(proof_pdf_exists)}",
            f"- Size: {proof_pdf_size} bytes",
            f"- Page count: {proof_pdf_pages}",
            f"- Render command: `make proof-only`",
            "",
            "## Google Fonts QA Proof Artifact",
            "",
            f"- Path: `{GFT_QA_OUTPUT.relative_to(ROOT)}`",
            f"- Exists: {yes_no(gftools_proof_output)}",
            f"- HTML files: {gftools_proof_count}",
            f"- Covers Regular, Medium, SemiBold, Bold: {yes_no(gftools_proof_instances)}",
            f"- Tooling ready: {yes_no(gftools_qa_ready)}",
            f"- Render command: `make kerning-proof-check`",
            "",
            "## Local Repository Dependencies",
            "",
            f"- google/fonts path: `{GF_REPO_PATH}`",
            f"- google/fonts origin: `{git_value(GF_REPO_PATH, ['remote', 'get-url', 'origin'])}`",
            f"- google/fonts upstream: `{git_value(GF_REPO_PATH, ['remote', 'get-url', 'upstream'])}`",
            f"- google/fonts branch: `{git_value(GF_REPO_PATH, ['rev-parse', '--abbrev-ref', 'HEAD'])}`",
            f"- Package report google/fonts ready: {package_report_gf_ready}",
            f"- Package report inputs ready: {package_report_inputs_ready}",
            f"- Package report auth ready: {package_report_auth_ready}",
            f"- drawbot-skia path: `{DRAWBOT_SKIA_REPO}`",
            f"- drawbot-skia python exists: {yes_no(drawbot_python.exists())}",
            f"- drawbot-skia src exists: {yes_no(drawbot_src.exists())}",
            "",
            "## Next Actions",
            "",
        ]
    )
    if not preflight_ready:
        lines.append("- Restore the missing local build/report prerequisites, then run `make preflight`.")
    if not requirements_ready:
        lines.append("- Refresh and review `requirements.txt`, then rerun `make preflight-only`.")
    if not proof_ready:
        lines.append("- Restore `/Users/eli/GH/repos/drawbot-skia` and its `.venv` before running `make proof` or `make handoff`.")
    if not package_ready:
        if package_report_first_blocker != "unknown":
            lines.append(f"- Resolve package dry-run first blocker: {package_report_first_blocker}.")
        if package_report_blocking_findings not in {"unknown", "none"}:
            lines.append(f"- Resolve all package dry-run blockers: {package_report_blocking_findings}.")
        lines.append("- Review `documentation/package-dry-run-readiness.md` before running `GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run`.")
    if preflight_ready and proof_ready and package_ready:
        lines.append("- Local command prerequisites are ready; run `make preflight` after drawing, source, or metadata changes.")

    output.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
