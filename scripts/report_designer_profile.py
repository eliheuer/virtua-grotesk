#!/usr/bin/env python3
"""Audit Google Fonts designer profile readiness."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path(os.environ["GF_REPO_PATH"]) if os.environ.get("GF_REPO_PATH") else Path("GF_REPO_PATH_NOT_CONFIGURED")
OUTPUT_DEFAULT = Path("documentation/google-fonts/designer-profile-readiness.md")


@dataclass(frozen=True)
class DesignerProfile:
    designer: str
    path: Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def person_lines(path: Path) -> list[str]:
    names: list[str] = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(re.sub(r"\s*<[^>]+>\s*$", "", line).strip())
    return names


def metadata_designer_strings() -> list[str]:
    texts = [
        read_text(ROOT / "documentation/google-fonts/google-fonts-metadata-review.md"),
        read_text(ROOT / "documentation/google-fonts/google-fonts-downstream-package-preview.md"),
    ]
    values: list[str] = []
    for text in texts:
        for match in re.finditer(r'designer:\s*"([^"]+)"', text):
            value = match.group(1).strip()
            if value not in values:
                values.append(value)
    return values


def pending_values(values: list[str]) -> list[str]:
    return [value for value in values if value.lower().startswith("pending decision")]


def designer_entities(designer_string: str) -> list[str]:
    return [part.strip() for part in designer_string.split(",") if part.strip()]


def profile_slug(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", ascii_name.lower())


def designer_profiles(gf_repo: Path) -> list[DesignerProfile]:
    catalog = gf_repo / "catalog" / "designers"
    profiles: list[DesignerProfile] = []
    if not catalog.exists():
        return profiles
    for info_path in sorted(catalog.glob("*/info.pb")):
        text = read_text(info_path)
        match = re.search(r'designer:\s*"([^"]+)"', text)
        if match:
            profiles.append(DesignerProfile(match.group(1), info_path.parent))
    return profiles


def profile_match(name: str, profiles: list[DesignerProfile]) -> DesignerProfile | None:
    for profile in profiles:
        if profile.designer == name:
            return profile
    slug = profile_slug(name)
    for profile in profiles:
        if profile.path.name == slug:
            return profile
    return None


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def markdown_report(gf_repo: Path) -> str:
    authors = person_lines(ROOT / "AUTHORS.txt")
    contributors = person_lines(ROOT / "CONTRIBUTORS.txt")
    metadata_designers = metadata_designer_strings()
    pending_metadata_designers = pending_values(metadata_designers)
    final_metadata_designers = [value for value in metadata_designers if value not in pending_metadata_designers]
    final_metadata_entities: list[str] = []
    for designer_string in final_metadata_designers:
        for entity in designer_entities(designer_string):
            if entity not in final_metadata_entities:
                final_metadata_entities.append(entity)
    profiles = designer_profiles(gf_repo)
    catalog_exists = (gf_repo / "catalog" / "designers").exists()
    profile_names = [profile.designer for profile in profiles]

    candidate_sources: list[tuple[str, str]] = []
    for name in authors:
        if name not in [candidate for candidate, _ in candidate_sources]:
            candidate_sources.append((name, "AUTHORS.txt"))
    for name in contributors:
        if name not in [candidate for candidate, _ in candidate_sources]:
            candidate_sources.append((name, "CONTRIBUTORS.txt"))
    missing_candidate_profiles = sum(
        1 for name, _ in candidate_sources if profile_match(name, profiles) is None
    )

    lines = [
        "# Designer Profile Readiness",
        "",
        "This generated report tracks Google Fonts designer-profile readiness for",
        "the downstream `METADATA.pb` designer string. The Google Fonts metadata",
        "guide says each designer listed in `METADATA.pb` needs a matching",
        "`catalog/designers/*/info.pb` entry, and the designer profile guide says",
        "that profile name must be spelled exactly the same as the metadata",
        "designer string.",
        "",
        "## Local Google Fonts Checkout",
        "",
        f"- Path: `{gf_repo}`",
        f"- Designer catalog exists: {yes_no(catalog_exists)}",
        f"- Designer profiles read: {len(profiles)}",
        f"- AUTHORS catalog-credit candidates: {len(authors)}",
        f"- Contributor-only candidates: {sum(1 for name in contributors if name not in authors)}",
        f"- Candidate profiles missing: {missing_candidate_profiles}",
        "",
        "## Current Upstream Names",
        "",
        f"- AUTHORS.txt: {', '.join(f'`{name}`' for name in authors) if authors else 'none'}",
        f"- CONTRIBUTORS.txt: {', '.join(f'`{name}`' for name in contributors) if contributors else 'none'}",
        f"- Metadata preview designer strings: {', '.join(f'`{name}`' for name in metadata_designers) if metadata_designers else 'none'}",
        f"- Final metadata designer strings present: {yes_no(bool(final_metadata_designers))}",
        f"- Final comma-separated designer entities present: {yes_no(bool(final_metadata_entities))}",
        f"- Pending metadata designer placeholders: {len(pending_metadata_designers)}",
        "",
        "## Candidate Designer Profiles",
        "",
        "| Candidate | Source | Expected catalog slug | Exact profile found | Matching profile path |",
        "| --- | --- | --- | --- | --- |",
    ]

    if candidate_sources:
        for name, source in candidate_sources:
            match = profile_match(name, profiles)
            exact = name in profile_names
            lines.append(
                f"| `{name}` | `{source}` | `{profile_slug(name)}` | {yes_no(exact)} | "
                f"{'`' + str(match.path.relative_to(gf_repo)) + '`' if match else 'missing'} |"
            )
    else:
        lines.append("| none | none | none | no | missing |")

    lines.extend(
        [
            "",
            "## Metadata Designer String Status",
            "",
            "| Metadata designer string | Final value | Profile found |",
            "| --- | --- | --- |",
        ]
    )
    if metadata_designers:
        for name in metadata_designers:
            is_pending = name in pending_metadata_designers
            match = None if is_pending else profile_match(name, profiles)
            lines.append(
                f"| `{name}` | {yes_no(not is_pending)} | "
                f"{'n/a - pending decision' if is_pending else yes_no(match is not None)} |"
            )
    else:
        lines.append("| none | no | n/a |")

    lines.extend(
        [
            "",
            "## Final Metadata Designer Entity Status",
            "",
            "| Designer entity | Source metadata string | Profile found | Matching profile path |",
            "| --- | --- | --- | --- |",
        ]
    )
    if final_metadata_entities:
        for entity in final_metadata_entities:
            source_strings = [
                value for value in final_metadata_designers if entity in designer_entities(value)
            ]
            match = profile_match(entity, profiles)
            lines.append(
                f"| `{entity}` | {', '.join(f'`{value}`' for value in source_strings)} | "
                f"{yes_no(match is not None)} | "
                f"{'`' + str(match.path.relative_to(gf_repo)) + '`' if match else 'missing'} |"
            )
    else:
        lines.append("| none | n/a | n/a | n/a |")

    lines.extend(
        [
            "",
            "## Before Final Packaging",
            "",
            "- Confirm the final `METADATA.pb` `designer` string and designer order.",
            "- Treat `AUTHORS.txt` names as the catalog-credit candidates; use",
            "  `CONTRIBUTORS.txt` to review whether any additional credited",
            "  contributors belong in the metadata designer string.",
            "- Confirm every comma-separated designer/foundry in that string has a",
            "  matching Google Fonts designer profile or a profile request prepared.",
            "- Confirm any new `catalog/designers` profile uses third-person English",
            "  biography text, an image, and an `info.pb` designer string that exactly",
            "  matches `METADATA.pb`.",
            "- Re-run this report after profile files, metadata, or catalog checkout",
            "  state change.",
            "",
            "References:",
            "",
            "- https://googlefonts.github.io/gf-guide/metadata.html",
            "- https://googlefonts.github.io/gf-guide/profile.html",
            "- https://googlefonts.github.io/gf-guide/googlefonts.html",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_designer_profile.py [google_fonts_repo] [output.md]")
    if len(argv) == 1:
        return DEFAULT_GF_REPO, OUTPUT_DEFAULT
    if len(argv) == 2:
        return DEFAULT_GF_REPO, Path(argv[1])
    return Path(argv[1]), Path(argv[2])


def main(argv: list[str]) -> int:
    gf_repo, output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(gf_repo), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
