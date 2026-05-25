#!/usr/bin/env python3
"""Generate a Google Fonts authorship and AI-disclosure readiness report."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/authorship-disclosure-readiness.md")
CONTACT_LINE_RE = re.compile(r"^[^<>]+ <[^<>]+>$")


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def entries(relative: str) -> list[str]:
    return [
        line.strip()
        for line in read_text(relative).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def contact_formatted_entries(lines: list[str]) -> list[str]:
    return [line for line in lines if CONTACT_LINE_RE.match(line)]


def first_line(relative: str) -> str:
    return read_text(relative).splitlines()[0].strip()


def decision_status(decisions_text: str) -> str:
    match = re.search(
        r"## Copyright authorship and AI disclosure\s*\n\nStatus: ([^\n]+)",
        decisions_text,
    )
    return match.group(1).strip() if match else "unknown"


def decision_section(decisions_text: str) -> str:
    match = re.search(
        r"## Copyright authorship and AI disclosure\s*\n(?P<section>.*?)(?=^## |\Z)",
        decisions_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group("section") if match else ""


def approved_authorship_statement(decisions_text: str) -> str:
    section = decision_section(decisions_text)
    bullets: list[str] = []
    current = ""
    for line in section.splitlines():
        if line.startswith("- "):
            if current:
                bullets.append(current.strip())
            current = line.removeprefix("- ").strip()
        elif current and line.startswith("  "):
            current += " " + line.strip()
        elif current and not line.strip():
            continue
        elif current:
            bullets.append(current.strip())
            current = ""
    if current:
        bullets.append(current.strip())
    author = next((line for line in bullets if "sole copyright author/controller" in line), "")
    ai = next((line for line in bullets if line.startswith("AI-use disclosure:")), "")
    if author and ai:
        return f"{author} {ai}"
    return ""


def ai_disclosure_recorded(decisions_text: str, handoff_text: str) -> bool:
    pending_markers = [
        "No AI-use disclosure has been recorded yet.",
        "AI-use disclosure: pending maintainer confirmation",
        "confirm copyright authorship and AI-use disclosure before checking this",
    ]
    combined = f"{decisions_text}\n{handoff_text}"
    if any(marker in combined for marker in pending_markers):
        return False
    return "AI-use disclosure:" in combined


def markdown_report() -> str:
    authors = entries("AUTHORS.txt")
    contributors = entries("CONTRIBUTORS.txt")
    author_contacts = contact_formatted_entries(authors)
    contributor_contacts = contact_formatted_entries(contributors)
    ofl_copyright = first_line("OFL.txt")
    decisions_text = read_text("documentation/google-fonts-decisions.md")
    handoff_text = read_text("documentation/google-fonts-submission-handoff.md")
    template_text = read_text("documentation/google-fonts-add-font-template-audit.md")
    status = decision_status(decisions_text)
    approved_statement = approved_authorship_statement(decisions_text)
    combined_checkbox = (
        "sole copyright author" in template_text and "AI tools were used" in template_text
    )
    disclosure_recorded = ai_disclosure_recorded(decisions_text, handoff_text)
    project_author_copyright = "The Virtua Grotesk Project Authors" in ofl_copyright

    lines = [
        "# Authorship And AI Disclosure Readiness",
        "",
        "This generated report tracks the Google Fonts Add Font issue requirement",
        "that copyright authorship and AI-use disclosure are confirmed together.",
        "It records local evidence separately from maintainer confirmations that",
        "cannot be inferred from the source tree.",
        "",
        "## Summary",
        "",
        f"- AUTHORS.txt entries: `{', '.join(authors) if authors else 'none'}`",
        f"- CONTRIBUTORS.txt entries: `{', '.join(contributors) if contributors else 'none'}`",
        f"- AUTHORS.txt contact-formatted entries: {len(author_contacts)} / {len(authors)}",
        f"- CONTRIBUTORS.txt contact-formatted entries: {len(contributor_contacts)} / {len(contributors)}",
        f"- Contact-formatted credit lines absent by current decision: {'yes' if len(author_contacts) != len(authors) or len(contributor_contacts) != len(contributors) else 'no'}",
        f"- OFL copyright line: `{ofl_copyright}`",
        f"- OFL uses project-author copyright holder: {'yes' if project_author_copyright else 'no'}",
        f"- Combined Add Font checkbox present: {'yes' if combined_checkbox else 'no'}",
        f"- AI-use disclosure recorded: {'yes' if disclosure_recorded else 'no'}",
        f"- Approved authorship/AI statement recorded: {'yes' if approved_statement else 'no'}",
        "- Email/contact line change required now: no",
        f"- Decision status: {status}",
        "",
        "## Current Evidence",
        "",
        "- `AUTHORS.txt` is the current copyright-author source of truth for",
        "  Google Fonts review.",
        "- `CONTRIBUTORS.txt` is the current contributor-attribution source of",
        "  truth.",
        "- The local file comments ask for `Name <email address>` lines, and",
        "  the Google Fonts upstream guide describes both files as contact",
        "  information files.",
        "- The official Authors and Contributors guide's templates use",
        "  `Name or Organization <email address>` for authors and",
        "  `Name <email address>` for contributors; the maintainer has chosen",
        "  to keep the current display-only names unless Google Fonts asks for",
        "  email/contact-formatted credit lines.",
        "- `OFL.txt` currently uses a collective project-author copyright line,",
        "  while the local author and contributor files each contain one named",
        "  person.",
        "- The current `google/fonts` Add Font issue template combines sole",
        "  copyright-author authority and AI-use disclosure into one checkbox.",
        "- Final AI-use disclosure wording is recorded in",
        "  `documentation/google-fonts-decisions.md` and synchronized into",
        "  the submission handoff.",
        "",
        "## Approved Add Font Statement",
        "",
        "```text",
        approved_statement or "missing",
        "```",
        "",
        "## Maintainer Input Checklist",
        "",
        "| Input | Current value | Needed before Add Font issue |",
        "| --- | --- | --- |",
        "| Copyright-author authority | `Eli Heuer` sole copyright author/controller statement recorded | Keep synchronized with Add Font issue text. |",
        f"| AI-use disclosure | {'Recorded' if disclosure_recorded else 'No final disclosure recorded'} | Keep synchronized with Add Font issue text. |",
        f"| Email/contact-formatted credit lines | AUTHORS.txt: {len(author_contacts)} / {len(authors)}; CONTRIBUTORS.txt: {len(contributor_contacts)} / {len(contributors)} | Keep current display-only names unless Google Fonts asks for contact-formatted lines. |",
        f"| OFL copyright holder | `{ofl_copyright}` | Keep current project-author wording unless the copyright-holder model changes. |",
        "| Add Font checkbox wording | Combined copyright-authorship and AI-use checkbox is present in current template | Use the approved statement above in the Google Fonts Add Font issue. |",
        "",
        "Decision-safe default: keep `AUTHORS.txt`, `CONTRIBUTORS.txt`, and",
        "`OFL.txt` unchanged because the maintainer-approved Add Font statement",
        "is already recorded and no email/contact line change is required now.",
        "",
        "## Apply After Maintainer Confirmation",
        "",
        "- Use the approved copyright-authorship and AI-use statement above in the",
        "  Add Font issue.",
        "- Keep the copyright-authorship and AI-use disclosure answer as one",
        "  combined maintainer-approved statement.",
        "- Update `AUTHORS.txt`, `CONTRIBUTORS.txt`, and `OFL.txt` if the confirmed",
        "  authorship or copyright-holder wording differs from the current files.",
        "- Add email/contact strings to `AUTHORS.txt` and `CONTRIBUTORS.txt` only",
        "  if Google Fonts asks for explicit contact-formatted credit lines.",
        "- Rerun `make preflight` after any authorship, copyright, or disclosure",
        "  wording change.",
        "",
        "References:",
        "",
        "- https://googlefonts.github.io/gf-guide/onboarding.html",
        "- https://googlefonts.github.io/gf-guide/upstream.html",
        "- https://googlefonts.github.io/gf-guide/making-pr.html",
        "- https://openfontlicense.org",
        "",
    ]
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_authorship_disclosure_readiness.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
