#!/usr/bin/env python3
"""Report DrawBot proof runtime readiness."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/drawbot-runtime-readiness.md")
DRAWBOT_SKIA_REPO = Path(os.environ["DRAWBOT_SKIA_REPO"]) if os.environ.get("DRAWBOT_SKIA_REPO") else None
PROJECT_PYTHON = ROOT / ".venv/bin/python"
DRAWBOT_SKIA_SRC = DRAWBOT_SKIA_REPO / "src" if DRAWBOT_SKIA_REPO else None
EXPECTED_ORIGINS = {
    "git@github.com:eliheuer/drawbot-skia.git",
    "https://github.com/eliheuer/drawbot-skia.git",
    "https://github.com/eliheuer/drawbot-skia",
}
EXPECTED_UPSTREAM = "https://github.com/justvanrossum/drawbot-skia.git"


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


def display_path(path: Path | None) -> str:
    if path is None:
        return "not configured"
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        pass
    try:
        return str(path.resolve().relative_to(ROOT))
    except (OSError, ValueError):
        if path == DRAWBOT_SKIA_REPO:
            return "$DRAWBOT_SKIA_REPO"
        if DRAWBOT_SKIA_REPO and path == DRAWBOT_SKIA_SRC:
            return "$DRAWBOT_SKIA_REPO/src"
        return str(path)


def git_remote(name: str) -> str:
    if DRAWBOT_SKIA_REPO is None or not DRAWBOT_SKIA_REPO.exists():
        return "missing"
    _, output = run(["git", "remote", "get-url", name], cwd=DRAWBOT_SKIA_REPO)
    return output or "missing"


def git_value(command: list[str]) -> str:
    if DRAWBOT_SKIA_REPO is None or not DRAWBOT_SKIA_REPO.exists():
        return "missing"
    _, output = run(command, cwd=DRAWBOT_SKIA_REPO)
    return output or "missing"


def import_status() -> tuple[bool, str]:
    if not PROJECT_PYTHON.exists():
        return False, "project .venv Python missing"
    env = os.environ.copy()
    if DRAWBOT_SKIA_SRC and DRAWBOT_SKIA_SRC.exists():
        env["PYTHONPATH"] = str(DRAWBOT_SKIA_SRC) + (
            f":{env['PYTHONPATH']}" if env.get("PYTHONPATH") else ""
        )
    result = subprocess.run(
        [
            str(PROJECT_PYTHON),
            "-c",
            (
                "from drawbot_skia.drawing import Drawing; "
                "db = Drawing(); "
                "assert hasattr(db, 'saveImage')"
            ),
        ],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        if DRAWBOT_SKIA_SRC and DRAWBOT_SKIA_SRC.exists():
            return True, "import ok with configured fork src on PYTHONPATH"
        return True, "import ok from project environment"
    return False, (result.stdout or "import failed").strip()


def markdown_report() -> str:
    makefile_text = (ROOT / "Makefile").read_text(encoding="utf-8")
    proof_text = (ROOT / "scripts/build_general_proof.py").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    tooling_text = (ROOT / "documentation/python-tooling-notes.md").read_text(encoding="utf-8")
    makefile_repo = "DRAWBOT_SKIA_REPO ?=" in makefile_text and "/Users/" not in makefile_text
    makefile_python = "DRAWBOT_PYTHON ?= $(PYTHON)" in makefile_text
    makefile_pythonpath = "DRAWBOT_PYTHONPATH" in makefile_text
    origin = git_remote("origin")
    upstream = git_remote("upstream")
    branch = git_value(["git", "branch", "--show-current"])
    short_head = git_value(["git", "rev-parse", "--short", "HEAD"])
    status = git_value(["git", "status", "--short"])
    import_ok, import_summary = import_status()
    origin_is_fork = origin in EXPECTED_ORIGINS
    proof_requires_fork = (
        "from drawbot_skia.drawing import Drawing" in proof_text
        and "import drawBot as db" not in proof_text
    )

    lines = [
        "# DrawBot Runtime Readiness",
        "",
        (
            "This generated report records the proof-generation runtime. "
            "Virtua Grotesk proofs use `drawbot-skia`. A local fork checkout "
            "can be supplied with `DRAWBOT_SKIA_REPO`, but shared repo files "
            "must not hardcode machine-specific paths."
        ),
        "",
        "## Summary",
        "",
        f"- DRAWBOT_SKIA_REPO configured: {yes_no(DRAWBOT_SKIA_REPO is not None)}",
        f"- Local drawbot-skia checkout exists: {yes_no(bool(DRAWBOT_SKIA_REPO and DRAWBOT_SKIA_REPO.exists()))}",
        f"- Expected fork origin owner/repo: `eliheuer/drawbot-skia`",
        f"- Actual origin: `{origin}`",
        f"- Origin is Eli Heuer fork: {yes_no(origin_is_fork)}",
        f"- Accepted origin URL forms: {', '.join(f'`{value}`' for value in sorted(EXPECTED_ORIGINS))}",
        f"- Expected upstream: `{EXPECTED_UPSTREAM}`",
        f"- Actual upstream: `{upstream}`",
        f"- Upstream is canonical drawbot-skia: {yes_no(upstream == EXPECTED_UPSTREAM)}",
        f"- Local drawbot-skia branch: `{branch}`",
        f"- Local drawbot-skia HEAD: `{short_head}`",
        f"- Local drawbot-skia worktree clean: {yes_no(status == 'missing' or status == '')}",
        f"- Project .venv Python exists: {yes_no(PROJECT_PYTHON.exists())}",
        f"- Project .venv Python: `{display_path(PROJECT_PYTHON)}`",
        f"- drawbot-skia src exists: {yes_no(bool(DRAWBOT_SKIA_SRC and DRAWBOT_SKIA_SRC.exists()))}",
        f"- Drawing API importable: {yes_no(import_ok)}",
        f"- Import status: `{import_summary or 'no output'}`",
        "",
        "## Repository Wiring",
        "",
        f"- Makefile keeps `DRAWBOT_SKIA_REPO` portable: {yes_no(makefile_repo)}",
        f"- Makefile uses project .venv Python for DrawBot proofs: {yes_no(makefile_python)}",
        f"- Makefile supports optional fork `src` on `PYTHONPATH`: {yes_no(makefile_pythonpath)}",
        f"- `scripts/build_general_proof.py` supports `drawbot_skia.drawing.Drawing`: {yes_no('from drawbot_skia.drawing import Drawing' in proof_text)}",
        f"- `scripts/build_general_proof.py` requires eliheuer/drawbot-skia instead of generic DrawBot: {yes_no(proof_requires_fork)}",
        f"- README documents the fork runtime: {yes_no('eliheuer/drawbot-skia' in readme_text)}",
        f"- Python tooling notes document the fork runtime: {yes_no('eliheuer/drawbot-skia' in tooling_text)}",
        "",
        "## Apply Before Proof Review",
        "",
        "- Set `DRAWBOT_SKIA_REPO=/path/to/drawbot-skia` when you want to run",
        "  proofs from a local fork checkout.",
        "- Regenerate this report with `make preflight` after changing the",
        "  DrawBot runtime, proof script, or local drawbot-skia checkout.",
        "- Use `make proof` after a successful font build to regenerate",
        "  `documentation/proofs/proof.pdf` for final visual review.",
        "",
        "References:",
        "",
        "- https://github.com/eliheuer/drawbot-skia",
        "- https://github.com/justvanrossum/drawbot-skia",
        "",
    ]
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_drawbot_runtime_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = ROOT / parse_args(argv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
