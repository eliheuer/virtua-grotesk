#!/usr/bin/env python3
"""Summarize recent local google/fonts package examples."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GF_REPO = Path("/Users/eli/GH/forks/fonts")
OUTPUT_DEFAULT = Path("documentation/google-fonts/recent-google-fonts-packages.md")

RECENT_FAMILIES = [
    ("Pliant", "ofl/pliant", "google/fonts#10546", "2026-05-22"),
    ("Scheherazade New", "ofl/scheherazadenew", "google/fonts#10455", "2026-05-01"),
    ("Akt", "ofl/akt", "google/fonts#10468", "2026-04-29"),
    ("Estedad", "ofl/estedad", "google/fonts#10401", "2026-04-16"),
]

# Cached from the public GitHub upstream repos at the exact commits cited in
# the downstream METADATA.pb rows above. This keeps the local report
# reproducible; refresh these fields after updating RECENT_FAMILIES.
UPSTREAM_REPO_SNAPSHOTS = {
    "Pliant": {
        "repository": "https://github.com/TheJonassss/Pliant",
        "commit": "dc119b45f0b60597305af387b97b2f5a94b2e1e4",
        "root_authors": True,
        "root_contributors": True,
        "root_description": False,
        "documentation_description": True,
        "article": False,
        "fonts_variable": True,
        "fonts_ttf": True,
        "fonts_webfonts": True,
        "sources_config": True,
        "source_format": "Glyphs",
        "build_entrypoint": "Makefile",
        "requirements": True,
        "ci_template": True,
        "template_refresh": True,
        "renovate": True,
    },
    "Akt": {
        "repository": "https://github.com/dimgrenev/akt",
        "commit": "b3935082b52ae393aef02a679505c028a5256c72",
        "root_authors": False,
        "root_contributors": False,
        "root_description": False,
        "documentation_description": False,
        "article": True,
        "fonts_variable": True,
        "fonts_ttf": True,
        "fonts_webfonts": True,
        "sources_config": True,
        "source_format": "Glyphs",
        "build_entrypoint": "makefile + tools/build.sh",
        "requirements": True,
        "ci_template": False,
        "template_refresh": False,
        "renovate": False,
    },
    "Estedad": {
        "repository": "https://github.com/aminabedi68/Estedad",
        "commit": "69e879f78a4a1c7c4594baf7da13ba1c9f65ffd3",
        "root_authors": True,
        "root_contributors": True,
        "root_description": True,
        "documentation_description": False,
        "article": False,
        "fonts_variable": True,
        "fonts_ttf": True,
        "fonts_webfonts": True,
        "sources_config": True,
        "source_format": "Glyphs",
        "build_entrypoint": "scripts",
        "requirements": True,
        "ci_template": False,
        "template_refresh": False,
        "renovate": False,
    },
}


@dataclass(frozen=True)
class PackageSummary:
    family: str
    path: str
    pr: str
    merged: str
    exists: bool
    font_files: tuple[str, ...]
    article: bool
    upstream_yaml: bool
    upstream_info: bool
    source_repository_url: str
    source_commit: str
    source_archive_url: str
    source_branch: str
    config_yaml: str
    primary_script: str
    subsets: tuple[str, ...]
    axes: tuple[str, ...]
    stroke: str
    tags_field: bool


@dataclass(frozen=True)
class RecentMerge:
    commit: str
    merged: str
    pr: str
    path: str
    subject: str


def git_output(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def ahead_behind(repo: Path, left: str, right: str) -> str:
    output = git_output(repo, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    if not output:
        return "unknown"
    parts = output.split()
    if len(parts) != 2:
        return "unknown"
    ahead, behind = parts
    return f"{ahead} ahead, {behind} behind"


def first_value(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def all_values(pattern: str, text: str) -> tuple[str, ...]:
    return tuple(re.findall(pattern, text))


def package_summary(gf_repo: Path, family: str, family_path: str, pr: str, merged: str) -> PackageSummary:
    path = gf_repo / family_path
    metadata_path = path / "METADATA.pb"
    if not metadata_path.exists():
        return PackageSummary(
            family=family,
            path=family_path,
            pr=pr,
            merged=merged,
            exists=False,
            font_files=(),
            article=False,
            upstream_yaml=False,
            upstream_info=False,
            source_repository_url="",
            source_commit="",
            source_archive_url="",
            source_branch="",
            config_yaml="",
            primary_script="",
            subsets=(),
            axes=(),
            stroke="",
            tags_field=False,
        )

    metadata = metadata_path.read_text(encoding="utf-8")
    font_files = tuple(sorted(item.name for item in path.glob("*.ttf")))
    return PackageSummary(
        family=family,
        path=family_path,
        pr=pr,
        merged=merged,
        exists=True,
        font_files=font_files,
        article=(path / "article" / "ARTICLE.en_us.html").exists(),
        upstream_yaml=(path / "upstream.yaml").exists(),
        upstream_info=(path / "upstream_info.md").exists(),
        source_repository_url=first_value(r'repository_url: "([^"]+)"', metadata),
        source_commit=first_value(r'commit: "([^"]+)"', metadata),
        source_archive_url=first_value(r'archive_url: "([^"]+)"', metadata),
        source_branch=first_value(r'branch: "([^"]+)"', metadata),
        config_yaml=first_value(r'config_yaml: "([^"]+)"', metadata),
        primary_script=first_value(r'primary_script: "([^"]+)"', metadata),
        subsets=all_values(r'subsets: "([^"]+)"', metadata),
        axes=all_values(r'tag: "([^"]+)"', metadata),
        stroke=first_value(r'stroke: "([^"]+)"', metadata),
        tags_field=bool(re.search(r"^tags\s*:", metadata, flags=re.MULTILINE)),
    )


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def root_has(path: str) -> bool:
    return (ROOT / path).exists()


def any_path(root: Path, pattern: str) -> bool:
    return any(root.glob(pattern))


def path_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "check-ignore", "--quiet", path],
        check=False,
    )
    return result.returncode == 0


def normalized_origin_url() -> str:
    origin = git_output(ROOT, ["remote", "get-url", "origin"])
    if not origin:
        return "unknown"
    if origin.startswith("git@github.com:") and origin.endswith(".git"):
        slug = origin.removeprefix("git@github.com:").removesuffix(".git")
        return f"https://github.com/{slug}"
    if origin.startswith("https://github.com/"):
        return origin.removesuffix(".git")
    return origin


def virtua_snapshot() -> dict[str, object]:
    return {
        "repository": normalized_origin_url(),
        "commit": "pending final source commit",
        "root_authors": root_has("AUTHORS.txt"),
        "root_contributors": root_has("CONTRIBUTORS.txt"),
        "root_description": False,
        "documentation_description": root_has("documentation/google-fonts/DESCRIPTION.en_us.html"),
        "article": root_has("documentation/google-fonts/ARTICLE.en_us.html"),
        "fonts_variable": any_path(ROOT / "fonts/variable", "*.ttf"),
        "fonts_ttf": any_path(ROOT / "fonts/ttf", "*.ttf"),
        "fonts_webfonts": any_path(ROOT / "fonts/webfonts", "*.woff2"),
        "sources_config": root_has("sources/config.yaml"),
        "source_format": "UFO + designspace",
        "build_entrypoint": "build.sh + Makefile",
        "requirements": root_has("requirements.txt"),
        "ci_template": root_has(".github/workflows"),
        "template_refresh": root_has(".templaterc.json"),
        "renovate": root_has("renovate.json"),
        "fonts_variable_ignored": path_ignored("fonts/variable/VirtuaGrotesk[wght].ttf"),
    }


def recent_packager_merges(gf_repo: Path, limit: int = 8) -> tuple[RecentMerge, ...]:
    if not gf_repo.exists():
        return ()
    output = git_output(
        gf_repo,
        [
            "log",
            "--first-parent",
            "--merges",
            "--since=2026-03-01",
            "--date=short",
            "--pretty=format:%h%x09%ad%x09%s",
            "--grep=gftools_packager_ofl_",
        ],
    )
    merges: list[RecentMerge] = []
    for line in output.splitlines():
        commit, merged, subject = (line.split("\t", 2) + ["", "", ""])[:3]
        pr_match = re.search(r"#(\d+)", subject)
        path_match = re.search(r"gftools_packager_ofl_([a-z0-9_]+)", subject)
        if not pr_match or not path_match:
            continue
        family_dir = path_match.group(1).replace("_", "")
        merges.append(
            RecentMerge(
                commit=commit,
                merged=merged,
                pr=f"google/fonts#{pr_match.group(1)}",
                path=f"ofl/{family_dir}",
                subject=subject,
            )
        )
        if len(merges) >= limit:
            break
    return tuple(merges)


def newest_selected_example() -> tuple[str, str, str]:
    family, _family_path, pr, merged = max(RECENT_FAMILIES, key=lambda item: item[3])
    return family, pr, merged


def markdown_report(gf_repo: Path) -> str:
    summaries = [
        package_summary(gf_repo, family, family_path, pr, merged)
        for family, family_path, pr, merged in RECENT_FAMILIES
    ]
    existing_summaries = [summary for summary in summaries if summary.exists]
    recent_merges = recent_packager_merges(gf_repo)
    commit = git_output(gf_repo, ["rev-parse", "--short", "HEAD"]) if gf_repo.exists() else ""
    status = git_output(gf_repo, ["status", "--short", "--branch"]) if gf_repo.exists() else ""
    status_lines = status.splitlines()
    dirty_lines = [line for line in status_lines[1:] if line.strip()]
    virtua_dirty_lines = [
        line for line in dirty_lines if "ofl/virtuagrotesk" in line
    ]
    upstream_alignment = ahead_behind(gf_repo, "main", "upstream/main") if gf_repo.exists() else "unknown"
    origin_alignment = ahead_behind(gf_repo, "main", "origin/main") if gf_repo.exists() else "unknown"
    newest_family, newest_pr, newest_date = newest_selected_example()
    newest_merge = recent_merges[0] if recent_merges else None
    newer_packager_merges = [
        merge for merge in recent_merges if merge.merged > newest_date
    ]

    lines = [
        "# Recent Google Fonts Package Audit",
        "",
        "This generated report reads selected recently merged new-font examples from",
        "the local `google/fonts` checkout. It keeps the template/PR audit tied to",
        "actual downstream package files instead of a hand-written memory of recent",
        "PRs.",
        "",
        "## Local Checkout",
        "",
        f"- Path: `{gf_repo}`",
        f"- Exists: {yes_no(gf_repo.exists())}",
        f"- Current commit: `{commit or 'unknown'}`",
        f"- Status: `{status_lines[0] if status_lines else 'unknown'}`",
        f"- Dirty paths: {len(dirty_lines)}",
        f"- Dirty `ofl/virtuagrotesk` paths: {len(virtua_dirty_lines)}",
        f"- Alignment with `upstream/main`: `{upstream_alignment}`",
        f"- Alignment with `origin/main`: `{origin_alignment}`",
        f"- Sample package directories present: {len(existing_summaries)} / {len(summaries)}",
        f"- Newest selected package example: {newest_pr} ({newest_family}, {newest_date})",
        f"- Newest Packager merge found locally: {newest_merge.pr if newest_merge else 'none'} ({newest_merge.merged if newest_merge else 'none'})",
        f"- Packager merges newer than selected examples: {len(newer_packager_merges)}",
        "",
        "## Package Examples",
        "",
        "| PR | Family | Merged | Path | Present | Fonts | Article | upstream.yaml | upstream_info.md | primary_script | Subsets | Axes | Source repo | Source commit | archive_url | Source branch | config_yaml | tags field |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for summary in summaries:
        lines.append(
            "| {pr} | {family} | {merged} | `{path}` | {present} | {fonts} | {article} | {upstream_yaml} | {upstream_info} | {primary_script} | {subsets} | {axes} | {repo} | {commit} | {archive_url} | {branch} | {config_yaml} | {tags} |".format(
                pr=summary.pr,
                family=summary.family,
                merged=summary.merged,
                path=summary.path,
                present=yes_no(summary.exists),
                fonts=", ".join(f"`{font}`" for font in summary.font_files) if summary.font_files else "missing",
                article=yes_no(summary.article),
                upstream_yaml=yes_no(summary.upstream_yaml),
                upstream_info=yes_no(summary.upstream_info),
                primary_script=f"`{summary.primary_script}`" if summary.primary_script else "none",
                subsets=", ".join(f"`{subset}`" for subset in summary.subsets) if summary.subsets else "missing",
                axes=", ".join(f"`{axis}`" for axis in summary.axes) if summary.axes else "missing",
                repo=f"`{summary.source_repository_url}`" if summary.source_repository_url else "missing",
                commit=f"`{summary.source_commit}`" if summary.source_commit else "missing",
                archive_url=f"`{summary.source_archive_url}`" if summary.source_archive_url else "none",
                branch=f"`{summary.source_branch}`" if summary.source_branch else "missing",
                config_yaml=f"`{summary.config_yaml}`" if summary.config_yaml else "none",
                tags=yes_no(summary.tags_field),
            )
        )

    lines.extend(
        [
            "",
            "## Recent Packager Merges",
            "",
            "This section is derived from the local `google/fonts` first-parent merge history",
            "for `gftools_packager_ofl_*` branches. It is a recency check; the package",
            "examples above remain the detailed comparison set.",
            "",
            "| PR | Merged | Path | Commit | Merge subject |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    if recent_merges:
        for merge in recent_merges:
            lines.append(
                f"| {merge.pr} | {merge.merged} | `{merge.path}` | `{merge.commit}` | {merge.subject} |"
            )
    else:
        lines.append("| missing | missing | missing | missing | missing |")

    lines.extend(
        [
            "",
            "## Upstream Repo Comparison",
            "",
            "This section compares the public upstream GitHub repositories cited by",
            "the recent downstream packages above with the current Virtua Grotesk",
            "repo shape. The recent upstream rows are cached from GitHub trees at",
            "the exact commits recorded in their downstream `METADATA.pb` files.",
            "",
            "| Family | Upstream repo | Commit | AUTHORS | CONTRIBUTORS | Description | Article | Variable fonts | Static TTFs | Webfonts | sources/config.yaml | Source format | Build entrypoint | Requirements | CI/template automation | Renovate |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for summary in summaries:
        snapshot = UPSTREAM_REPO_SNAPSHOTS.get(summary.family)
        if not snapshot:
            continue
        description = "root" if snapshot["root_description"] else "documentation" if snapshot["documentation_description"] else "no"
        lines.append(
            "| {family} | `{repo}` | `{commit}` | {authors} | {contributors} | {description} | {article} | {variable} | {ttf} | {webfonts} | {config} | {source_format} | {build} | {requirements} | {ci} | {renovate} |".format(
                family=summary.family,
                repo=snapshot["repository"],
                commit=str(snapshot["commit"])[:12],
                authors=yes_no(bool(snapshot["root_authors"])),
                contributors=yes_no(bool(snapshot["root_contributors"])),
                description=description,
                article=yes_no(bool(snapshot["article"])),
                variable=yes_no(bool(snapshot["fonts_variable"])),
                ttf=yes_no(bool(snapshot["fonts_ttf"])),
                webfonts=yes_no(bool(snapshot["fonts_webfonts"])),
                config=yes_no(bool(snapshot["sources_config"])),
                source_format=snapshot["source_format"],
                build=snapshot["build_entrypoint"],
                requirements=yes_no(bool(snapshot["requirements"])),
                ci=yes_no(bool(snapshot["ci_template"] or snapshot["template_refresh"])),
                renovate=yes_no(bool(snapshot["renovate"])),
            )
        )
    virtua = virtua_snapshot()
    virtua_description = (
        "root"
        if virtua["root_description"]
        else "documentation"
        if virtua["documentation_description"]
        else "no"
    )
    lines.append(
        "| Virtua Grotesk | `{repo}` | `{commit}` | {authors} | {contributors} | {description} | {article} | {variable} | {ttf} | {webfonts} | {config} | {source_format} | {build} | {requirements} | {ci} | {renovate} |".format(
            repo=virtua["repository"],
            commit=virtua["commit"],
            authors=yes_no(bool(virtua["root_authors"])),
            contributors=yes_no(bool(virtua["root_contributors"])),
            description=virtua_description,
            article=yes_no(bool(virtua["article"])),
            variable=f"{yes_no(bool(virtua['fonts_variable']))} (ignored: {yes_no(bool(virtua['fonts_variable_ignored']))})",
            ttf=yes_no(bool(virtua["fonts_ttf"])),
            webfonts=yes_no(bool(virtua["fonts_webfonts"])),
            config=yes_no(bool(virtua["sources_config"])),
            source_format=virtua["source_format"],
            build=virtua["build_entrypoint"],
            requirements=yes_no(bool(virtua["requirements"])),
            ci=yes_no(bool(virtua["ci_template"] or virtua["template_refresh"])),
            renovate=yes_no(bool(virtua["renovate"])),
        )
    )

    lines.extend(
        [
            "",
            "## Upstream Repo Implications For Virtua Grotesk",
            "",
            "- Recent merged upstream repos vary in automation: Pliant follows more of the project-template automation, while Akt and Estedad do not. Virtua Grotesk does not need to copy CI, Renovate, or template refresh tooling for the first submission.",
            "- The sampled upstream repos expose built fonts under `fonts/`, including `fonts/variable/` for variable examples. Virtua Grotesk currently generates those files locally but keeps them ignored, so the Packager source strategy still needs an explicit decision.",
            "- Pliant, Akt, and Estedad include `sources/config.yaml`; Virtua Grotesk already matches that shape with `sources/config.yaml` and `gftools builder`.",
            "- Estedad is the closest Arabic-script comparison: its downstream package keeps `primary_script: \"Arab\"` and records `source.config_yaml`. That supports keeping Virtua's `source.config_yaml` only if the final source strategy is build-from-source.",
            "- Scheherazade New is the closest recent Arabic package for Virtua's selected release/archive path: its downstream `source.archive_url` points to a GitHub release download `.zip`, and its `source.files` map release-archive members directly into the family directory.",
            "- Akt shows that some recent upstream repos use an `article/` path upstream, while Pliant and Estedad keep images/descriptions under `documentation/`. Virtua's downstream preview can still map `documentation/google-fonts/ARTICLE.en_us.html` into downstream `article/ARTICLE.en_us.html` through `source.files`.",
            "",
            "## Virtua Grotesk Implications",
            "",
            "- Keep `article/ARTICLE.en_us.html` in the downstream package unless Google Fonts asks for the legacy description flow.",
            "- Keep `primary_script: \"Arab\"` while Arabic is the primary non-Latin support target.",
            "- Keep `source.repository_url`, `source.commit`, `source.branch`, and optional `source.config_yaml` internally consistent.",
            "- Keep `source.config_yaml` only if it points at a reproducible builder config; recent `google/fonts` commits removed non-buildable `config_yaml` fields from Bitcount packages and misleading override configs from Oxygen/Neuton.",
            "- Virtua Grotesk's `sources/config.yaml` is a real `gftools builder` config today, so the field is valid only if the final source strategy uses the reproducible build path.",
            "- For the selected `latest-release` path, mirror the Scheherazade New pattern: use a final GitHub release download `.zip` in `source.archive_url`, omit `source.config_yaml`, and make every `source.files` entry resolve inside that archive.",
            "- Recent packages record exact upstream commits in `source.commit`; Virtua Grotesk should do the same after the public source state is final.",
            "- Review generated `upstream.yaml` if Packager emits it; the current Google Fonts guide documents it as the downstream file that links packaged fonts back to upstream for future upgrades.",
            "- Treat `upstream_info.md` as optional because recent examples are mixed; Estedad has it, Pliant and Akt do not.",
            "- Treat new-font `tags` as issue/PR review metadata rather than a `METADATA.pb` field unless Google Fonts tooling generates it.",
            "- The local checkout may contain Virtua Grotesk dry-run artifacts; they do not affect the sampled package examples above, but they must be reviewed or discarded before the final Packager pass.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) > 3:
        raise SystemExit("usage: report_recent_gf_packages.py [google_fonts_repo] [output.md]")
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
