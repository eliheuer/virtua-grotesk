#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GF_REPO_PATH:-}" ]]; then
    echo "Set GF_REPO_PATH to a local google/fonts checkout."
    echo "The Makefile defaults to /Users/eli/GH/forks/fonts when you run:"
    echo "GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run"
    echo "Override example: GF_REPO_PATH=/path/to/fonts GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run"
    echo "Fallback review: GFT_PACKAGER_SOURCE_MODE=default or build-from-source"
    exit 2
fi

ensure_github_token() {
    if [[ -n "${GH_TOKEN:-}" ]]; then
        return 0
    fi
    if ! command -v gh >/dev/null 2>&1; then
        echo "GH_TOKEN is required for Packager GitHub API downloads, and gh is not installed."
        echo "Set GH_TOKEN, or install/authenticate GitHub CLI before running GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run."
        exit 2
    fi
    local token
    if ! token="$(gh auth token 2>/dev/null)" || [[ -z "$token" ]]; then
        echo "GH_TOKEN is required for Packager GitHub API downloads."
        echo "GitHub CLI does not currently provide a usable token."
        echo "Refresh auth with: gh auth login -h github.com"
        echo "Then rerun: GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run"
        exit 2
    fi
    export GH_TOKEN="$token"
}

if [[ ! -d "$GF_REPO_PATH/.git" ]]; then
    echo "GF_REPO_PATH is not a git checkout: $GF_REPO_PATH"
    exit 2
fi

origin_url="$(git -C "$GF_REPO_PATH" remote get-url origin 2>/dev/null || true)"
upstream_url="$(git -C "$GF_REPO_PATH" remote get-url upstream 2>/dev/null || true)"

case "$origin_url" in
    *github.com:google/fonts.git|*github.com/google/fonts.git|*github.com/google/fonts)
        has_google_fonts_remote=true
        ;;
    *)
        has_google_fonts_remote=false
        ;;
esac

case "$upstream_url" in
    *github.com:google/fonts.git|*github.com/google/fonts.git|*github.com/google/fonts)
        has_google_fonts_upstream=true
        ;;
    *)
        has_google_fonts_upstream=false
        ;;
esac

if [[ "$has_google_fonts_remote" != true && "$has_google_fonts_upstream" != true ]]; then
    echo "GF_REPO_PATH must be the google/fonts repo or a fork with upstream set to google/fonts."
    echo "origin: ${origin_url:-<missing>}"
    echo "upstream: ${upstream_url:-<missing>}"
    exit 2
fi

current_branch="$(git -C "$GF_REPO_PATH" rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "main" ]]; then
    echo "GF_REPO_PATH must be on main before a package dry run."
    echo "current branch: $current_branch"
    exit 2
fi

if ! git -C "$GF_REPO_PATH" rev-parse --verify --quiet upstream/main >/dev/null; then
    echo "GF_REPO_PATH is missing upstream/main. Fetch upstream first:"
    echo "git -C \"$GF_REPO_PATH\" fetch upstream"
    exit 2
fi

main_upstream_counts="$(git -C "$GF_REPO_PATH" rev-list --left-right --count main...upstream/main)"
if [[ "$main_upstream_counts" != "0	0" ]]; then
    echo "GF_REPO_PATH main is not aligned with upstream/main."
    echo "ahead/behind main...upstream/main: $main_upstream_counts"
    echo "Update with: git -C \"$GF_REPO_PATH\" merge --ff-only upstream/main"
    exit 2
fi

if git -C "$GF_REPO_PATH" rev-parse --verify --quiet origin/main >/dev/null; then
    main_origin_counts="$(git -C "$GF_REPO_PATH" rev-list --left-right --count main...origin/main)"
    if [[ "$main_origin_counts" != "0	0" ]]; then
        echo "GF_REPO_PATH main is not aligned with origin/main."
        echo "ahead/behind main...origin/main: $main_origin_counts"
        exit 2
    fi
fi

package_dir="ofl/virtuagrotesk"
metadata_path="$GF_REPO_PATH/$package_dir/METADATA.pb"
# Retain this old placeholder as a guard so an existing downstream METADATA.pb
# from an earlier dry run cannot be reused after the final URL decision.
stale_placeholder_upstream_url="https://github.com/fontgarden/virtua-grotesk"
starter_template_markers=(
    'designer: "UNKNOWN"'
    'repository_url: "https://github.com/user/repo"'
    'fonts/variable/MyFont[wght].ttf'
    'primary_script: "Deva"'
)
unresolved_metadata_markers=(
    "Pending decision"
    "Pending:"
    "Pending final"
)
prohibited_optional_metadata_fields=(
    "languages"
    "display_name"
    "minisite_url"
    "classifications"
    "sample_text"
    "tags"
)
dirty_outside_package="$(git -C "$GF_REPO_PATH" status --porcelain | grep -vE "^(.. )?${package_dir}/" || true)"
if [[ -n "$dirty_outside_package" ]]; then
    echo "google/fonts checkout has changes outside $package_dir. Commit, stash, or clean them before packaging."
    echo "$dirty_outside_package"
    exit 2
fi

for required_path in \
    "fonts/variable/VirtuaGrotesk[wght].ttf" \
    "OFL.txt" \
    "documentation/ARTICLE.en_us.html" \
    "documentation/readme-specimen.png" \
    "sources/config.yaml"
do
    if [[ ! -e "$required_path" ]]; then
        echo "Missing required package input: $required_path"
        echo "Run make handoff before package-dry-run."
        exit 2
    fi
done

if [[ -f "$metadata_path" ]]; then
    package_input="$metadata_path"
    if grep -qF "$stale_placeholder_upstream_url" "$metadata_path"; then
        echo "Existing downstream METADATA.pb still uses the stale placeholder upstream URL:"
        echo "$stale_placeholder_upstream_url"
        echo "Replace it with the decided public upstream URL before rerunning Packager from METADATA.pb."
        echo "See documentation/google-fonts-decisions.md and documentation/open-placeholder-audit.md."
        exit 2
    fi
    for marker in "${unresolved_metadata_markers[@]}"; do
        if grep -qF "$marker" "$metadata_path"; then
            echo "Existing downstream METADATA.pb still contains unresolved metadata:"
            echo "$marker"
            echo "Run make downstream-metadata-check, then apply only after every pending field has a final value."
            echo "Use scripts/prepare_downstream_metadata.py --apply when the preview is ready."
            exit 2
        fi
    done
    for marker in "${starter_template_markers[@]}"; do
        if grep -qF "$marker" "$metadata_path"; then
            echo "Existing downstream METADATA.pb is still the Packager starter template:"
            echo "$marker"
            echo "Populate /Users/eli/GH/forks/fonts/$package_dir/METADATA.pb before rerunning Packager from METADATA.pb."
            echo "Use documentation/google-fonts-downstream-package-preview.md as the current local preview."
            exit 2
        fi
    done
    source_mode="${GFT_PACKAGER_SOURCE_MODE:-default}"
    if [[ -z "$source_mode" ]]; then
        source_mode="default"
    fi
    metadata_has_config_yaml=false
    if grep -qE '^[[:space:]]*config_yaml:[[:space:]]*"sources/config.yaml"' "$metadata_path"; then
        metadata_has_config_yaml=true
    fi
    metadata_has_archive_url=false
    if grep -qE '^[[:space:]]*archive_url:[[:space:]]*"https://github\.com/[^/"]+/[^/"]+/releases/download/[^/"]+/[^"]+\.zip"' "$metadata_path"; then
        metadata_has_archive_url=true
    fi
    for field in "${prohibited_optional_metadata_fields[@]}"; do
        if grep -qE "^[[:space:]]*${field}[[:space:]]*:" "$metadata_path"; then
            echo "Existing downstream METADATA.pb contains a review-gated optional field:"
            echo "$field"
            echo "Remove it or record explicit Google Fonts reviewer approval before running Packager."
            exit 2
        fi
    done
    case "$source_mode" in
        default|latest-release)
            if [[ "$metadata_has_config_yaml" == true ]]; then
                echo "Existing downstream METADATA.pb has source.config_yaml, but $source_mode mode should omit it unless Google Fonts review asks for build metadata."
                echo "Use build-from-source mode, or remove config_yaml before rerunning Packager."
                exit 2
            fi
            ;;
        build-from-source)
            if [[ "$metadata_has_config_yaml" != true ]]; then
                echo "Existing downstream METADATA.pb is missing source.config_yaml for build-from-source mode:"
                echo 'config_yaml: "sources/config.yaml"'
                exit 2
            fi
            ;;
    esac
    if [[ "$source_mode" == "latest-release" && "$metadata_has_archive_url" != true ]]; then
        echo "Existing downstream METADATA.pb is missing a valid source.archive_url for latest-release mode."
        echo "Record the final GitHub release download URL ending in .zip before rerunning Packager."
        exit 2
    fi
    metadata_date_added="$(grep -E '^[[:space:]]*date_added:[[:space:]]*"[^"]+"' "$metadata_path" | head -n 1 | sed -E 's/.*"([^"]+)".*/\1/' || true)"
    if [[ ! "$metadata_date_added" =~ ^20[0-9]{2}-[0-9]{2}-[0-9]{2}$ ]] || ! ./venv/bin/python -c 'from datetime import datetime; import sys; datetime.strptime(sys.argv[1], "%Y-%m-%d")' "$metadata_date_added" 2>/dev/null; then
        echo 'Existing downstream METADATA.pb is missing a final valid date_added value.'
        echo 'Expected: date_added: "YYYY-MM-DD"'
        exit 2
    fi
    metadata_source_commit="$(grep -E '^[[:space:]]*commit:[[:space:]]*"[0-9A-Za-z]+"' "$metadata_path" | head -n 1 | sed -E 's/.*"([^"]+)".*/\1/' || true)"
    if [[ ! "$metadata_source_commit" =~ ^[0-9a-f]{40}$ ]]; then
        echo 'Existing downstream METADATA.pb is missing a final lowercase 40-character source.commit hash.'
        echo 'Expected: commit: "0123456789abcdef0123456789abcdef01234567"'
        exit 2
    fi
    if [[ "$source_mode" == "latest-release" ]]; then
        if ! ./venv/bin/python scripts/verify_release_archive.py --quiet; then
            echo "Local release archive is not ready for latest-release mode."
            echo "Run: make release-archive-build"
            echo "Then rerun: GFT_PACKAGER_SOURCE_MODE=latest-release make package-dry-run"
            exit 2
        fi
    fi
    if [[ -z "${GH_TOKEN:-}" ]]; then
        ensure_github_token
    fi
else
    package_input="Virtua Grotesk"
fi

ensure_github_token

packager_args=("$package_input" "$GF_REPO_PATH")
case "${GFT_PACKAGER_SOURCE_MODE:-default}" in
    default|"")
        ;;
    latest-release)
        packager_args+=("--latest-release")
        ;;
    build-from-source)
        packager_args+=("--build-from-source")
        ;;
    *)
        echo "Unsupported GFT_PACKAGER_SOURCE_MODE: $GFT_PACKAGER_SOURCE_MODE"
        echo "Use one of: default, latest-release, build-from-source."
        exit 2
        ;;
esac

./venv/bin/gftools packager "${packager_args[@]}"

echo ""
echo "Packager dry run finished. Review $GF_REPO_PATH/$package_dir before using -p."
