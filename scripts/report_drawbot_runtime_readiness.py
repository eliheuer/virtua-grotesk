#!/usr/bin/env python3
"""Report DrawBot proof runtime readiness."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/drawbot-runtime-readiness.md")
DRAWBOT_SKIA_REPO = Path("/Users/eli/GH/repos/drawbot-skia")
PROJECT_PYTHON = ROOT / "venv/bin/python"
DRAWBOT_SKIA_SRC = DRAWBOT_SKIA_REPO / "src"
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


def git_remote(name: str) -> str:
    if not DRAWBOT_SKIA_REPO.exists():
        return "missing"
    _, output = run(["git", "remote", "get-url", name], cwd=DRAWBOT_SKIA_REPO)
    return output or "missing"


def git_value(command: list[str]) -> str:
    if not DRAWBOT_SKIA_REPO.exists():
        return "missing"
    _, output = run(command, cwd=DRAWBOT_SKIA_REPO)
    return output or "missing"


def import_status() -> tuple[bool, str]:
    if not PROJECT_PYTHON.exists() or not DRAWBOT_SKIA_SRC.exists():
        return False, "project venv Python or drawbot-skia src directory missing"
    returncode, output = run(
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
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(DRAWBOT_SKIA_SRC)
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
        return True, "import ok with fork src on PYTHONPATH"
    return False, (result.stdout or output or "import failed").strip()


def markdown_report() -> str:
    makefile_text = (ROOT / "Makefile").read_text(encoding="utf-8")
    proof_text = (ROOT / "scripts/build_general_proof.py").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    tooling_text = (ROOT / "documentation/python-tooling-notes.md").read_text(encoding="utf-8")
    makefile_repo = "DRAWBOT_SKIA_REPO ?= /Users/eli/GH/repos/drawbot-skia" in makefile_text
    makefile_python = "DRAWBOT_PYTHON ?= $(PYTHON)" in makefile_text
    makefile_pythonpath = 'PYTHONPATH="$(DRAWBOT_SKIA_REPO)/src' in makefile_text
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
            "Virtua Grotesk proofs intentionally use Eli Heuer's local "
            "`drawbot-skia` fork instead of a generic DrawBot runtime."
        ),
        "",
        "## Summary",
        "",
        f"- Local drawbot-skia checkout exists: {yes_no(DRAWBOT_SKIA_REPO.exists())}",
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
        f"- Project venv Python exists: {yes_no(PROJECT_PYTHON.exists())}",
        f"- Project venv Python: `{PROJECT_PYTHON}`",
        f"- drawbot-skia src exists: {yes_no(DRAWBOT_SKIA_SRC.exists())}",
        f"- Drawing API importable: {yes_no(import_ok)}",
        f"- Import status: `{import_summary or 'no output'}`",
        "",
        "## Repository Wiring",
        "",
        f"- Makefile sets `DRAWBOT_SKIA_REPO`: {yes_no(makefile_repo)}",
        f"- Makefile uses project venv Python for DrawBot proofs: {yes_no(makefile_python)}",
        f"- Makefile prepends fork `src` to `PYTHONPATH`: {yes_no(makefile_pythonpath)}",
        f"- `scripts/build_general_proof.py` supports `drawbot_skia.drawing.Drawing`: {yes_no('from drawbot_skia.drawing import Drawing' in proof_text)}",
        f"- `scripts/build_general_proof.py` requires eliheuer/drawbot-skia instead of generic DrawBot: {yes_no(proof_requires_fork)}",
        f"- README documents the fork runtime: {yes_no('eliheuer/drawbot-skia' in readme_text)}",
        f"- Python tooling notes document the fork runtime: {yes_no('eliheuer/drawbot-skia' in tooling_text)}",
        "",
        "## Apply Before Proof Review",
        "",
        "- Keep `/Users/eli/GH/repos/drawbot-skia` synced with the intended",
        "  `eliheuer/drawbot-skia` fork state before regenerating final proofs.",
        "- Regenerate this report with `make preflight` after changing the",
        "  DrawBot runtime, proof script, or local drawbot-skia checkout.",
        "- Use `make proof-only` after a successful font build to regenerate",
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
