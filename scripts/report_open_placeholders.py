#!/usr/bin/env python3
"""Report unresolved Google Fonts onboarding placeholders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_URL = "https://github.com/fontgarden/virtua-grotesk"
OUTPUT_DEFAULT = Path("documentation/open-placeholder-audit.md")

INCLUDE_FILES = [
    Path("OFL.txt"),
    Path("AUTHORS.txt"),
    Path("CONTRIBUTORS.txt"),
    Path("README.md"),
    Path("GF_READINESS.md"),
    Path("Makefile"),
    Path("sources/config.yaml"),
    Path("sources/VirtuaGrotesk.designspace"),
    Path("sources/VirtuaGrotesk-Regular.ufo/fontinfo.plist"),
    Path("sources/VirtuaGrotesk-Bold.ufo/fontinfo.plist"),
    Path("scripts/fix_gf_metadata.py"),
    Path("scripts/package_gf_dry_run.sh"),
]
INCLUDE_GLOBS = [
    "documentation/*.md",
    "documentation/*.html",
]
EXCLUDE_FILES = {
    OUTPUT_DEFAULT,
    Path("documentation/generated-font-metadata.md"),
    Path("documentation/source-ufo-metadata.md"),
}
GENERATED_EVIDENCE_FILES = {
    Path("documentation/article-readiness.md"),
    Path("documentation/authorship-disclosure-readiness.md"),
    Path("documentation/decision-application-blockers.md"),
    Path("documentation/designer-profile-readiness.md"),
    Path("documentation/downstream-metadata-readiness.md"),
    Path("documentation/public-upstream-readiness.md"),
}
INTERNAL_GUARD_FILES = {
    Path("scripts/package_gf_dry_run.sh"),
}


@dataclass(frozen=True)
class Finding:
    kind: str
    path: Path
    line_number: int
    text: str


def is_generated_evidence(path: Path) -> bool:
    return path in GENERATED_EVIDENCE_FILES


def iter_input_files() -> list[Path]:
    files = set()
    for path in INCLUDE_FILES:
        if (ROOT / path).exists():
            files.add(path)
    for pattern in INCLUDE_GLOBS:
        for path in ROOT.glob(pattern):
            rel_path = path.relative_to(ROOT)
            if rel_path not in EXCLUDE_FILES:
                files.add(rel_path)
    return sorted(files)


def is_internal_guard(path: Path, line: str) -> bool:
    return "stale_placeholder_upstream_url" in line


def is_internal_metadata_guard(path: Path, line: str) -> bool:
    return path == Path("scripts/package_gf_dry_run.sh") and (
        "unresolved_metadata_markers" in line
        or line.strip() in {'"Pending decision"', '"Pending:"', '"Pending final"'}
    )


def classify_line(path: Path, line: str) -> str | None:
    if is_internal_guard(path, line) and PLACEHOLDER_URL in line:
        return "stale placeholder guard"
    if is_internal_metadata_guard(path, line):
        return "metadata pending guard"
    if PLACEHOLDER_URL in line:
        return "placeholder upstream URL"
    if "Pending decision" in line:
        return "pending decision marker"
    if re.search(r"\b(TODO|FIXME)\b", line):
        return "TODO/FIXME marker"
    return None


def find_placeholders() -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in iter_input_files():
        path = ROOT / rel_path
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            kind = classify_line(rel_path, line)
            if kind:
                findings.append(
                    Finding(
                        kind=kind,
                        path=rel_path,
                        line_number=line_number,
                        text=line.strip(),
                    )
                )
    return findings


def markdown_report(findings: list[Finding]) -> str:
    by_kind: dict[str, list[Finding]] = {}
    for finding in findings:
        by_kind.setdefault(finding.kind, []).append(finding)
    actionable_findings = [finding for finding in findings if not is_generated_evidence(finding.path)]
    guard_findings = [
        finding
        for finding in actionable_findings
        if finding.kind in {"stale placeholder guard", "metadata pending guard"}
    ]
    stale_guard_findings = [
        finding for finding in guard_findings if finding.kind == "stale placeholder guard"
    ]
    metadata_guard_findings = [
        finding for finding in guard_findings if finding.kind == "metadata pending guard"
    ]
    actionable_findings = [
        finding
        for finding in actionable_findings
        if finding.kind not in {"stale placeholder guard", "metadata pending guard"}
    ]
    evidence_echoes = [finding for finding in findings if is_generated_evidence(finding.path)]
    actionable_by_kind: dict[str, list[Finding]] = {}
    for finding in actionable_findings:
        actionable_by_kind.setdefault(finding.kind, []).append(finding)

    lines = [
        "# Open Placeholder Audit",
        "",
        "This generated report tracks unresolved text that must be reviewed before a",
        "public Google Fonts handoff. It deliberately separates known maintainer",
        "decisions from drawing/source blockers so the final package pass is not",
        "blocked by hidden placeholder strings. Internal guard strings are kept",
        "separate because they protect the workflow from stale generated files",
        "and are not public handoff text.",
        "",
        "## Summary",
        "",
        f"- Public placeholder blocker count: {len(actionable_findings)}",
        f"- Placeholder upstream URL occurrences: {len(by_kind.get('placeholder upstream URL', []))}",
        f"- Pending decision markers: {len(by_kind.get('pending decision marker', []))}",
        f"- TODO/FIXME markers: {len(by_kind.get('TODO/FIXME marker', []))}",
        f"- Internal stale-placeholder guards: {len(stale_guard_findings)}",
        f"- Internal metadata guard markers: {len(metadata_guard_findings)}",
        f"- Actionable placeholder upstream URL occurrences: {len(actionable_by_kind.get('placeholder upstream URL', []))}",
        f"- Actionable pending decision markers: {len(actionable_by_kind.get('pending decision marker', []))}",
        f"- Generated evidence echoes: {len(evidence_echoes)}",
        "",
        "## Decision Blockers",
        "",
    ]

    if actionable_findings:
        lines.append(
            "These findings are allowed while the corresponding decision remains open, "
            "but they must be resolved before a final downstream package dry run."
        )
        lines.append("")
        lines.extend(
            [
                "| Kind | File | Line | Text |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for finding in actionable_findings:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No unresolved public placeholder strings were found in the audited files.")

    lines.extend(
        [
            "",
            "## Internal Guards",
            "",
        ]
    )
    if guard_findings:
        lines.append(
            "These strings intentionally retain old placeholder values to reject "
            "stale generated files. They are not public replacement surfaces."
        )
        lines.append("")
        lines.extend(
            [
                "| Kind | File | Line | Text |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for finding in guard_findings:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No internal stale-placeholder guards were found.")

    lines.extend(
        [
            "",
            "## Generated Evidence Echoes",
            "",
        ]
    )
    if evidence_echoes:
        lines.append(
            "These rows are generated reports echoing internal guard evidence or "
            "the public URL replacement audit. They do not create a public handoff "
            "blocker while the public placeholder blocker count is 0."
        )
        lines.append("")
        lines.extend(
            [
                "| Kind | File | Line | Text |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for finding in evidence_echoes:
            escaped_text = finding.text.replace("|", "\\|")
            lines.append(
                f"| {finding.kind} | `{finding.path}` | {finding.line_number} | `{escaped_text}` |"
            )
    else:
        lines.append("No generated report echoes were found.")

    lines.extend(
        [
            "",
            "## Apply Before Downstream Packaging If Public Blockers Appear",
            "",
            "- Replace placeholder upstream URLs in license, source metadata, public docs, and metadata preview files.",
            "- Replace public `Pending decision` markers with final maintainer-approved wording or move them to internal notes.",
            "- Remove public `TODO` or `FIXME` markers from handoff artifacts.",
            "- Keep intentional stale-placeholder guard strings in scripts that reject bad generated files.",
            "- Regenerate this report with `make preflight` after decisions are applied.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_open_placeholders.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    report = markdown_report(find_placeholders())
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
