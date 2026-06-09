#!/usr/bin/env python3
"""Generate a Google Fonts designer-profile draft package checklist."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DEFAULT = Path("documentation/google-fonts/designer-profile-package-draft.md")
DEFAULT_GF_REPO = Path(os.environ["GF_REPO_PATH"]) if os.environ.get("GF_REPO_PATH") else Path("GF_REPO_PATH_NOT_CONFIGURED")
GF_PROFILE_GUIDE = "https://googlefonts.github.io/gf-guide/profile.html"
GF_METADATA_GUIDE = "https://googlefonts.github.io/gf-guide/metadata.html"
GF_DESIGNERS_TREE = "https://github.com/google/fonts/tree/main/catalog/designers"
GF_ADD_FONT_GUIDE = "https://googlefonts.github.io/gf-guide/onboarding.html"
GF_PROFILE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSehvbqqgL5Dlv9WG0mmBVNfFAjoMIx-2d1YJNrU7C-zKBNkcw/viewform"
IMAGE_VALIDATOR = Path("scripts/validate_designer_profile_image.py")
BIO_VALIDATOR = Path("scripts/validate_designer_profile_bio.py")
INFO_VALIDATOR = Path("scripts/validate_designer_profile_info.py")
PREPARE_HELPER = Path("scripts/prepare_designer_profile.py")
BIO_CANDIDATE = Path("documentation/google-fonts/designer-profile-candidate/bio.html")
INFO_CANDIDATE = Path("documentation/google-fonts/designer-profile-candidate/info.pb")
IMAGE_CANDIDATE = Path("documentation/google-fonts/designer-profile-candidate/eliheuer.png")
TEMPORARY_PROFILE_LINK = "https://github.com/eliheuer"


def gf_repo_display() -> str:
    return "$GF_REPO_PATH" if DEFAULT_GF_REPO != Path("GF_REPO_PATH_NOT_CONFIGURED") else "GF_REPO_PATH_NOT_CONFIGURED"


def display_line(text: str, gf_repo: str) -> str:
    text = text.replace(str(ROOT), ".")
    text = text.replace(str(DEFAULT_GF_REPO), gf_repo)
    return text


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


def decision_status(decision_name: str) -> str:
    text = read_text(ROOT / "documentation/google-fonts/google-fonts-decisions.md")
    pattern = rf"^## {re.escape(decision_name)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return "unknown"
    status_match = re.search(r"^Status: ([a-z]+)$", match.group("body"), flags=re.MULTILINE)
    return status_match.group(1) if status_match else "unknown"


def metadata_pending_lines() -> list[str]:
    texts = [
        read_text(ROOT / "documentation/google-fonts/google-fonts-metadata-review.md"),
        read_text(ROOT / "documentation/google-fonts/google-fonts-downstream-package-preview.md"),
        read_text(ROOT / "documentation/google-fonts/downstream-metadata-readiness.md"),
    ]
    pending: list[str] = []
    for text in texts:
        for line in text.splitlines():
            if "Pending decision" in line or "Pending final" in line:
                stripped = line.strip()
                if stripped and stripped not in pending:
                    pending.append(stripped)
    return pending


def profile_slug(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", ascii_name.lower())


def command_available(command: list[str]) -> bool:
    try:
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        return False
    return result.returncode == 0


def command_success(command: list[str]) -> bool:
    try:
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        return False
    return result.returncode == 0


def command_output(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except OSError as error:
        return str(error)
    return result.stdout


def yes_no_from_output(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else "unknown"


def blocker_lines(output: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"^- (.+)$", output, flags=re.MULTILINE)
    ]


def blocker_contains(blockers: list[str], fragment: str) -> bool:
    return any(fragment in blocker for blocker in blockers)


def info_link(path: Path) -> str:
    match = re.search(r'^\s*link:\s*"([^"]*)"', read_text(path), flags=re.MULTILINE)
    return match.group(1) if match else ""


def bio_hrefs(path: Path) -> list[str]:
    return re.findall(r'<a\b[^>]*\bhref="([^"]+)"', read_text(path), flags=re.IGNORECASE)


def markdown_report() -> str:
    authors = person_lines(ROOT / "AUTHORS.txt")
    designer = authors[0] if authors else "Eli Heuer"
    slug = profile_slug(designer)
    image_name = f"{slug}.png"
    profile_dir = f"catalog/designers/{slug}"
    gf_profile_dir = DEFAULT_GF_REPO / profile_dir
    designers_dir = DEFAULT_GF_REPO / "catalog/designers"
    gf_repo = gf_repo_display()
    profile_exists = gf_profile_dir.exists()
    author_decision_status = decision_status("Author/contact lines")
    pending_lines = metadata_pending_lines()
    metadata_designer_blocked = any("designer" in line and "Pending decision" in line for line in pending_lines)
    metadata_commit_blocked = any("Pending final" in line for line in pending_lines)
    slug_is_ascii = slug.isascii()
    slug_has_hyphen = "-" in slug
    slug_matches_image = image_name.startswith(slug)
    add_designer_available = command_available(["./.venv/bin/gftools", "add-designer", "--help"])
    image_validator_exists = (ROOT / IMAGE_VALIDATOR).exists()
    bio_validator_exists = (ROOT / BIO_VALIDATOR).exists()
    info_validator_exists = (ROOT / INFO_VALIDATOR).exists()
    prepare_helper_exists = (ROOT / PREPARE_HELPER).exists()
    prepare_helper_text = read_text(ROOT / PREPARE_HELPER)
    bio_candidate = ROOT / BIO_CANDIDATE
    bio_candidate_exists = bio_candidate.exists()
    bio_candidate_valid = bio_candidate_exists and command_success(
        ["./.venv/bin/python", str(BIO_VALIDATOR), str(BIO_CANDIDATE)]
    )
    info_candidate = ROOT / INFO_CANDIDATE
    info_candidate_exists = info_candidate.exists()
    info_candidate_valid = info_candidate_exists and command_success(
        [
            "./.venv/bin/python",
            str(INFO_VALIDATOR),
            str(INFO_CANDIDATE),
            designer,
            image_name,
        ]
    )
    candidate_info_link = info_link(info_candidate)
    candidate_bio_links = bio_hrefs(bio_candidate)
    candidate_link_consistent = (
        bool(candidate_info_link) and candidate_info_link in candidate_bio_links
    ) or not candidate_info_link
    prepare_helper_checks_link_consistency = "info.pb link should match one bio.html link" in prepare_helper_text
    expected_files = [
        gf_profile_dir / "info.pb",
        gf_profile_dir / "bio.html",
        gf_profile_dir / image_name,
    ]
    prepare_output = command_output(["./.venv/bin/python", str(PREPARE_HELPER)])
    prepare_ready = yes_no_from_output(r"Ready to apply: (yes|no)", prepare_output)
    prepare_blocker_lines = [
        display_line(line, gf_repo)
        for line in blocker_lines(prepare_output)
    ]
    prepare_blockers = len(prepare_blocker_lines)
    prepare_missing_image = blocker_contains(prepare_blocker_lines, "image file does not exist:")
    prepare_dirty_checkout = blocker_contains(
        prepare_blocker_lines,
        "google/fonts checkout has dirty paths outside the designer profile path:",
    )
    profile_input_ready = (
        info_candidate_valid
        and bio_candidate_valid
        and not prepare_missing_image
    )
    downstream_profile_checkout_ready = (
        DEFAULT_GF_REPO.exists()
        and designers_dir.exists()
        and not profile_exists
        and not prepare_dirty_checkout
    )
    existing_expected_files = [path for path in expected_files if path.exists()]
    missing_inputs = [
        "designer profile link decision",
        "maintainer-approved biography",
        "square 100-300px profile image",
    ]
    downstream_branch = "designer/eli-heuer-profile"
    family_branch = "virtuagrotesk"

    lines = [
        "# Designer Profile Package Draft",
        "",
        "This generated draft prepares the Google Fonts designer-profile files",
        "for maintainer review. It is not a finished downstream profile until",
        "the biography text and square image are approved.",
        "",
        "## Readiness Status",
        "",
        "| Gate | Current state | Required before action |",
        "| --- | --- | --- |",
        f"| Author/contact decision | {author_decision_status} | decided |",
        f"| Downstream metadata designer string | {'blocked by pending decision' if metadata_designer_blocked else 'not blocked by pending decision'} | exact final string |",
        f"| Final source commit/tag | {'blocked by pending release commit' if metadata_commit_blocked else 'not blocking profile draft'} | required for family package, not for profile draft |",
        f"| Local designer profile path | {'exists' if profile_exists else 'missing'} | inspect existing profile or create one |",
        f"| Profile inputs | {len(missing_inputs)} unresolved | final link, biography, and image |",
        "",
        "## Target Profile",
        "",
        f"- Designer string: `{designer}`",
        f"- Catalog slug: `{slug}`",
        f"- Catalog slug ASCII-only: {'yes' if slug_is_ascii else 'no'}",
        f"- Catalog slug has hyphen: {'yes' if slug_has_hyphen else 'no'}",
        f"- Downstream directory: `{profile_dir}`",
        f"- Avatar filename matches slug: {'yes' if slug_matches_image else 'no'}",
        "- Profile PR scope: one designer profile only",
        f"- Local google/fonts checkout: `{gf_repo}`",
        f"- Local designers directory exists: {'yes' if designers_dir.exists() else 'no'}",
        f"- `gftools add-designer` available: {'yes' if add_designer_available else 'no'}",
        f"- Candidate info.pb validator present: {'yes' if info_validator_exists else 'no'}",
        f"- Candidate info.pb draft exists: {'yes' if info_candidate_exists else 'no'}",
        f"- Candidate info.pb draft passes validator: {'yes' if info_candidate_valid else 'no'}",
        f"- Candidate info.pb link: `{candidate_info_link or 'blank'}`",
        f"- Candidate image validator present: {'yes' if image_validator_exists else 'no'}",
        f"- Candidate image validator enforces filename: {'yes' if image_validator_exists else 'no'}",
        f"- Candidate bio validator present: {'yes' if bio_validator_exists else 'no'}",
        f"- Candidate bio validator enforces third-person voice: {'yes' if bio_validator_exists else 'no'}",
        f"- Candidate bio draft exists: {'yes' if bio_candidate_exists else 'no'}",
        f"- Candidate bio draft passes validator: {'yes' if bio_candidate_valid else 'no'}",
        f"- Candidate bio links: {', '.join(f'`{link}`' for link in candidate_bio_links) if candidate_bio_links else 'none'}",
        f"- Candidate info/bio link consistency: {'yes' if candidate_link_consistent else 'no'}",
        f"- Designer profile prepare helper present: {'yes' if prepare_helper_exists else 'no'}",
        f"- Designer profile prepare helper checks info/bio link consistency: {'yes' if prepare_helper_checks_link_consistency else 'no'}",
        f"- Designer profile prepare helper dry-run ready: {prepare_ready}",
        f"- Designer profile prepare helper blocking findings: {prepare_blockers}",
        f"- Prepare blocker is missing approved image input: {'yes' if prepare_missing_image else 'no'}",
        f"- Prepare blocker is downstream checkout cleanliness: {'yes' if prepare_dirty_checkout else 'no'}",
        f"- Approved profile inputs ready to apply: {'yes' if profile_input_ready else 'no'}",
        f"- Downstream profile checkout ready to apply: {'yes' if downstream_profile_checkout_ready else 'no'}",
        f"- Target profile directory already exists: {'yes' if profile_exists else 'no'}",
        f"- Expected profile files already present: {len(existing_expected_files)} / {len(expected_files)}",
        f"- Profile path collision risk: {'yes' if profile_exists else 'no'}",
        f"- Draft placeholders still unresolved: {len(missing_inputs)}",
        f"- Missing final inputs: {', '.join(missing_inputs)}",
        "- Profile link may be blank if the approved Google Fonts profile uses",
        "  `link: \"\"`; many current `google/fonts` designer profiles do this.",
        f"- Suggested profile branch: `{downstream_branch}`",
        f"- Expected family package branch: `{family_branch}`",
        "- Profile timing default: create or update the designer profile before",
        "  the family package if Google Fonts review needs a catalog match first;",
        "  keep it separate unless reviewers ask for a combined patch.",
        "",
        "## Required Downstream Files",
        "",
        f"- `{profile_dir}/info.pb`",
        f"- `{profile_dir}/bio.html`",
        f"- `{profile_dir}/{image_name}`",
        "",
        "## Local google/fonts Collision Check",
        "",
        "| Downstream path | Exists locally |",
        "| --- | --- |",
    ]
    for path in expected_files:
        lines.append(
            f"| `{path.relative_to(DEFAULT_GF_REPO)}` | {'yes' if path.exists() else 'no'} |"
        )

    lines.extend(
        [
            "",
            "If the target directory exists before the profile decision is applied,",
            "inspect it manually and decide whether the existing profile can be reused",
            "or needs a separate update PR.",
            "",
            "## Guarded Prepare Helper",
            "",
            "Use the guarded helper after the profile link, biography, and image",
            "are approved. It validates `info.pb`, `bio.html`, and the avatar image,",
            "requires any non-empty `info.pb` link to appear in `bio.html`,",
            "checks the local `google/fonts` checkout, and writes files only when",
            "`--apply` is passed.",
            "",
            "```bash",
            "make designer-profile-prepare-check",
            f"./.venv/bin/python {PREPARE_HELPER} --image path/to/{image_name} --apply",
            "```",
            "",
            f"- Default info candidate: `{INFO_CANDIDATE}`",
            f"- Default bio candidate: `{BIO_CANDIDATE}`",
            f"- Default image candidate: `{IMAGE_CANDIDATE}`",
            f"- Candidate info/bio link consistency: {'yes' if candidate_link_consistent else 'no'}",
            f"- Link consistency check implemented in prepare helper: {'yes' if prepare_helper_checks_link_consistency else 'no'}",
            f"- Current dry-run ready: {prepare_ready}",
            f"- Current dry-run blocking findings: {prepare_blockers}",
            f"- Missing approved image input blocks prepare helper: {'yes' if prepare_missing_image else 'no'}",
            f"- Downstream checkout cleanliness blocks prepare helper: {'yes' if prepare_dirty_checkout else 'no'}",
            f"- Approved profile inputs ready to apply: {'yes' if profile_input_ready else 'no'}",
            f"- Downstream profile checkout ready to apply: {'yes' if downstream_profile_checkout_ready else 'no'}",
            "- Current dry-run blocker details:",
            *(
                [f"  - {line}" for line in prepare_blocker_lines]
                if prepare_blocker_lines
                else ["  - none"]
            ),
            "",
            "## Exact Downstream Worktree Plan",
            "",
            "Use this only after the biography, link, and image are approved.",
            "Keep this work separate from the family package branch unless a",
            "Google Fonts reviewer explicitly asks for a combined patch.",
            "",
            "```bash",
            f"cd {gf_repo}",
            "git switch main",
            "git pull --ff-only upstream main",
            f"git switch -c {downstream_branch}",
            "```",
            "",
            "Before creating files in the downstream checkout, confirm the target",
            "profile path is still absent and the worktree is clean outside any",
            "intentional profile files:",
            "",
            "```bash",
            f"test ! -e {gf_repo}/{profile_dir}",
            f"git -C {gf_repo} status --short -- catalog/designers/{slug}",
            f"git -C {gf_repo} status --short",
            "```",
            "",
            "Create the profile with `gftools add-designer`, then hand-edit",
            "`info.pb` and `bio.html` to match the approved profile text:",
            "",
            "```bash",
            f"./.venv/bin/gftools add-designer {gf_repo}/catalog/designers \"{designer}\" --img_path path/to/{image_name}",
            "```",
            "",
            "Validate the profile inputs from this repo before committing the",
            "downstream profile files:",
            "",
            "```bash",
            "cd /path/to/virtua-grotesk",
            f"./.venv/bin/python scripts/validate_designer_profile_info.py {gf_repo}/{profile_dir}/info.pb \"{designer}\" {image_name}",
            f"./.venv/bin/python scripts/validate_designer_profile_image.py {gf_repo}/{profile_dir}/{image_name} {image_name}",
            f"./.venv/bin/python scripts/validate_designer_profile_bio.py {gf_repo}/{profile_dir}/bio.html",
            "make reports",
            "```",
            "",
            "Expected downstream commit scope:",
            "",
            f"- `{profile_dir}/info.pb`",
            f"- `{profile_dir}/bio.html`",
            f"- `{profile_dir}/{image_name}`",
            "",
        "## Maintainer Input Checklist",
        "",
        "| Input | Current value | Needed before downstream profile work |",
        "| --- | --- | --- |",
        f"| Final `METADATA.pb` designer string | `{designer}` applied in downstream preview | Keep profile `info.pb` spelling exactly matched. |",
        f"| Designer profile link | candidate `{TEMPORARY_PROFILE_LINK}`; maintainer approval pending | Approve this URL, provide one canonical website/social URL, or deliberately leave `link: \"\"` in `info.pb`. |",
        f"| Biography | candidate draft in `{BIO_CANDIDATE}`; maintainer approval pending | Approve or replace a third-person `bio.html` snippet that passes `make designer-profile-bio-check`; if `info.pb` uses a non-empty link, include that same URL in the bio links. |",
        f"| Profile image | `path/to/{image_name}` placeholder | Provide a square 100-300px image that passes `make designer-profile-image-check`. |",
        "| PR timing | profile missing in local google/fonts checkout | Decide whether this profile PR should land before, alongside, or after the family PR. |",
        "",
        "Decision-safe default:",
        "",
        "- Use `Eli Heuer` as the profile name because it is the decided",
        "  downstream metadata designer string and the only current AUTHORS",
        "  catalog-credit candidate.",
        "- Keep this as a separate designer-profile draft; do not create files in",
        "  `$GF_REPO_PATH/catalog/designers` until the biography and",
        "  image are approved.",
        "- If the family package has intentional dirty files under",
        "  `$GF_REPO_PATH/ofl/virtuagrotesk`, either commit, stash,",
        "  or review that work before applying a separate designer-profile branch.",
        "",
        "## Candidate `bio.html`",
        "",
        f"A validator-ready but unapproved biography draft lives at `{BIO_CANDIDATE}`.",
        "It uses the GitHub profile as a temporary profile link; replace the link",
        "if a website or different social profile should be the canonical",
        "Google Fonts designer-profile URL.",
        "",
        "Validate the candidate before using it downstream:",
        "",
        "```bash",
        f"make designer-profile-bio-check BIO={BIO_CANDIDATE}",
        "```",
        "",
        "The candidate passes local validation now, but it still needs",
        "maintainer approval before it is copied into `google/fonts`.",
        "",
        "## Candidate `info.pb`",
        "",
        f"A validator-ready but unapproved `info.pb` draft lives at `{INFO_CANDIDATE}`.",
        "It uses the GitHub profile as a temporary `link` value; replace it",
        "if a website or different social profile should be the canonical",
        "Google Fonts designer-profile URL, or set `link: \"\"` if no public",
        "profile link should be shown.",
        "",
        "Validate the candidate before using it downstream:",
        "",
        "```bash",
        f"make designer-profile-info-check INFO={INFO_CANDIDATE}",
        "```",
        "",
        "The candidate passes local validation now, but the profile `link`",
        "is still temporary until the canonical public URL is approved or",
        "the blank-link option is explicitly chosen.",
        "If `link` is non-empty, the guarded prepare helper requires the same",
        "URL to appear in `bio.html`; this keeps the visible biography link and",
        "`info.pb` profile link from drifting.",
        "",
        "Current candidate shape:",
        "",
        "```proto",
        f"designer: \"{designer}\"",
        f"link: \"{TEMPORARY_PROFILE_LINK}\"",
        "avatar {",
        f"  file_name: \"{image_name}\"",
        "}",
        "```",
        "",
        "The `designer` value must exactly match the final downstream",
        "`METADATA.pb` designer string.",
        "The avatar `file_name` must match the image file inside the same",
        "profile directory.",
        "",
        "Validate the final candidate `info.pb` before committing the designer",
        "profile:",
        "",
        "```bash",
        f"./.venv/bin/python scripts/validate_designer_profile_info.py {gf_repo}/{profile_dir}/info.pb \"{designer}\" {image_name}",
        "```",
        "",
        "## `bio.html` Requirements",
        "",
        "- Maintainer-authored English biography.",
        "- Third-person voice.",
        "- First-person pronouns are rejected by the local validator.",
        "- More than 200 characters and less than 1000 characters.",
        "- Around 100 words.",
        "- One or two links to a website or social profile.",
        "- HTML snippet using paragraph tags, not a complete HTML document.",
        "- Links should use real `http` or `https` URLs, visible link text,",
        "  and `target=\"_blank\"`.",
        "- If `info.pb` uses a non-empty `link`, include that exact URL in one",
        "  biography link.",
        "- Social links should be labeled by service name, such as `GitHub`,",
        "  `Instagram`, `LinkedIn`, `Twitter`, or `X`.",
        "- Website link text should omit the `http://` or `https://` protocol,",
        "  using only the readable domain or site name.",
        "",
        "Draft shape:",
        "",
        "```html",
        f"<p>{designer} is ...</p>",
        "",
        "<p><a href=\"https://REPLACE-WITH-APPROVED-URL\" target=\"_blank\">REPLACE-WITH-APPROVED-LABEL</a></p>",
        "```",
        "",
        "Validate the final candidate biography before creating or updating the",
        "designer profile:",
        "",
        "```bash",
        "make designer-profile-bio-check BIO=path/to/bio.html",
        "```",
        "",
        "## Image Requirements",
        "",
        f"- Filename: `{image_name}`",
        "- Filename must match the profile directory slug exactly.",
        "- PNG or JPEG.",
        "- Square 1:1 image.",
        "- Between 100px and 300px.",
        "- Crops cleanly as a circle.",
        "",
        "## Suggested Local Creation Command",
        "",
        "Validate the final candidate image before running `gftools add-designer`:",
        "",
        "```bash",
        f"make designer-profile-image-check IMAGE=path/to/{image_name}",
        "```",
        "",
        "Use `gftools add-designer` to create the initial downstream profile",
        "directory once the final image is available, then hand-edit",
        "`bio.html` as needed:",
        "",
        "```bash",
        f"./.venv/bin/gftools add-designer {gf_repo}/catalog/designers \"{designer}\" --img_path path/to/{image_name}",
        "```",
        "",
        "## Relationship To Family Package",
        "",
        "- The designer profile does not unblock the local release archive by",
        "  itself; that still needs the final source commit/tag.",
        "- The designer profile does unblock the downstream `METADATA.pb` designer",
        "  profile check because the final metadata designer string is already",
        "  applied.",
        "- The family package should still be limited to",
        "  `ofl/virtuagrotesk/*`; the profile path belongs in a separate",
        "  `catalog/designers/*` PR unless Google Fonts asks otherwise.",
        "- Google Fonts also accepts designer profile additions or updates through",
        "  the official profile form; if that route is chosen, keep this draft as",
        "  the local evidence packet and record the submitted profile link, bio,",
        "  and image before final packaging.",
        "",
        "## Profile Request Form Packet",
        "",
        "Use this packet if the profile is submitted through the Google Fonts",
        "designer-profile form instead of a direct `catalog/designers` PR.",
        "",
        f"- Form: {GF_PROFILE_FORM}",
        f"- Name: `{designer}`",
        f"- Linked family: `Virtua Grotesk`",
        f"- Canonical profile link: pending maintainer input, or explicit blank-link choice",
        f"- Biography: pending maintainer-approved `bio.html` text",
        f"- Image: pending validated square `{image_name}`",
        "- Keep the submitted profile text and image in sync with the downstream",
        "  `METADATA.pb` designer string.",
        "- The profile guide says platform updates appear after team review; allow",
        "  roughly 2-4 weeks after merge/registration before expecting the public",
        "  profile to appear.",
        "",
        "## Before Profile PR",
        "",
        "- Confirm the profile `designer` value still exactly matches the final",
        "  downstream `METADATA.pb` designer string.",
        "- Replace the draft biography with maintainer-approved text.",
        "- Add the final square profile image.",
        "- Run this repo's Google Fonts preflight.",
        "- Add or update one designer profile per PR if Google Fonts asks for",
        "  the profile before or alongside the family submission.",
        "- Mention the linked font family in the designer-profile PR.",
        "- Request the `Designer profile` and `Ready for review` labels.",
        "- Add the PR to Traffic Jam if following the Google Fonts onboarder",
        "  workflow.",
        "",
        "References:",
        "",
        f"- {GF_PROFILE_GUIDE}",
        f"- {GF_METADATA_GUIDE}",
        f"- {GF_ADD_FONT_GUIDE}",
        f"- {GF_DESIGNERS_TREE}",
        f"- {GF_PROFILE_FORM}",
        "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> Path:
    if len(argv) > 2:
        raise SystemExit("usage: report_designer_profile_package.py [output.md]")
    return Path(argv[1]) if len(argv) == 2 else OUTPUT_DEFAULT


def main(argv: list[str]) -> int:
    output_path = parse_args(argv)
    output = ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown_report(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
