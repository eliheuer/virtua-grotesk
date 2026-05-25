#!/usr/bin/env python3
"""Generate a review packet for gftools QA proof HTML output."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/kerning-proof-review.md")
GFT_QA_PROOF_DIR = Path("documentation/gftools-qa/Proof")
EXPECTED_INSTANCES = ["Regular", "Medium", "SemiBold", "Bold"]
EXPECTED_PROOF_TYPES = ["glyphs", "proofer", "text", "waterfall"]
GF_ONBOARDER_WORKFLOW = "https://googlefonts.github.io/gf-guide/onboarder-workflow.html"
GF_TESTING_GUIDE = "https://googlefonts.github.io/gf-guide/testing.html"
GF_TOOLS_GUIDE = "https://googlefonts.github.io/gf-guide/tools.html"
GF_GITHUB_GFTTOOLS = "https://github.com/googlefonts/gftools"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def proof_path(instance: str, proof_type: str) -> Path:
    return GFT_QA_PROOF_DIR / f"{instance}-diffbrowsers_{proof_type}.html"


def file_size(path: Path) -> int:
    full_path = ROOT / path
    return full_path.stat().st_size if full_path.exists() else 0


def proof_type_purpose(proof_type: str) -> str:
    return {
        "glyphs": "glyph-by-glyph outline and encoding scan",
        "proofer": "browser-style strings for spacing, rhythm, and kerning",
        "text": "paragraph/text texture and fallback review",
        "waterfall": "size progression and weight interpolation review",
    }[proof_type]


def review_focus(proof_type: str) -> str:
    return {
        "glyphs": "missing, blank, malformed, clipped, or wrong-codepoint glyphs",
        "proofer": "tight/loose pairs, sidebearing rhythm, and weight-specific spacing",
        "text": "texture breaks, script fallback, and awkward repeated patterns",
        "waterfall": "size-specific spacing, weight balance, and interpolation jumps",
    }[proof_type]


def markdown_report() -> str:
    proof_dir = ROOT / GFT_QA_PROOF_DIR
    expected_paths = [
        (instance, proof_type, proof_path(instance, proof_type))
        for instance in EXPECTED_INSTANCES
        for proof_type in EXPECTED_PROOF_TYPES
    ]
    present_count = sum(1 for _, _, path in expected_paths if (ROOT / path).exists())
    expected_count = len(expected_paths)
    proof_font = GFT_QA_PROOF_DIR / "VirtuaGrotesk[wght].ttf"

    lines = [
        "# Kerning Proof Review",
        "",
        "This generated packet makes the Google Fonts visual QA proof review",
        "auditable for humans and agents. It does not approve spacing or",
        "kerning by itself; it records the proof files that must be opened and",
        "reviewed after `make kerning-proof-check`.",
        "",
        "## Summary",
        "",
        f"- Proof directory: `{GFT_QA_PROOF_DIR}`",
        f"- Proof directory exists: {yes_no(proof_dir.exists())}",
        f"- Expected HTML proofs present: {present_count} / {expected_count}",
        f"- Expected instances covered: {yes_no(all((ROOT / proof_path(instance, 'proofer')).exists() for instance in EXPECTED_INSTANCES))}",
        f"- Embedded proof font exists: {yes_no((ROOT / proof_font).exists())}",
        "- Review status: pending human visual review",
        "",
        "## Expected Proof Files",
        "",
        "| Instance | Proof type | Present | Size | Review focus |",
        "| --- | --- | --- | --- | --- |",
    ]

    for instance, proof_type, path in expected_paths:
        lines.append(
            f"| {instance} | `{proof_type}` | {yes_no((ROOT / path).exists())} | "
            f"{file_size(path)} bytes | {review_focus(proof_type)} |"
        )

    lines.extend(
        [
            "",
            "## Review Checklist",
            "",
            "- Open every `*-diffbrowsers_proofer.html` file and inspect common",
            "  kerning pairs, uppercase/lowercase rhythm, punctuation spacing,",
            "  numeral spacing, and mixed-script strings.",
            "- Open every `*-diffbrowsers_text.html` file and inspect paragraph",
            "  texture for uneven color, fallback glyphs, missing Arabic shaping,",
            "  and excessive sidebearings.",
            "- Open every `*-diffbrowsers_waterfall.html` file and inspect size",
            "  changes, weight interpolation, and spacing at small and large sizes.",
            "- Open every `*-diffbrowsers_glyphs.html` file and inspect blank,",
            "  malformed, clipped, duplicate, or wrongly encoded glyphs.",
            "- Compare Regular, Medium, SemiBold, and Bold before accepting a",
            "  kerning deferral; the proof can show weight-specific spacing",
            "  problems even when automated checks are unchanged.",
            "- Rerun `make kerning-check` and `make preflight` after review notes",
            "  are resolved or after an explicit kerning deferral is recorded.",
            "",
            "## Proof Types",
            "",
            "| Proof type | Purpose |",
            "| --- | --- |",
        ]
    )

    for proof_type in EXPECTED_PROOF_TYPES:
        lines.append(f"| `{proof_type}` | {proof_type_purpose(proof_type)} |")

    lines.extend(
        [
            "",
            "## Commands",
            "",
            "```bash",
            "make kerning-proof-check",
            "make kerning-proof-review-check",
            "make kerning-check",
            "make preflight",
            "```",
            "",
            "References:",
            "",
            f"- {GF_ONBOARDER_WORKFLOW}",
            f"- {GF_TESTING_GUIDE}",
            f"- {GF_TOOLS_GUIDE}",
            f"- {GF_GITHUB_GFTTOOLS}",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_kerning_proof_review.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
