//! Pinned external inputs for reproducible social renders.
//!
//! Fonts and UFO sources are read from the enclosing project checkout at render
//! time. A slightly-stale font is acceptable for these system illustrations;
//! correctness of the *drawing system* is what these assets demonstrate.
//!
//! THIS IS THE ONLY PROJECT-SPECIFIC FILE in the crate. The rest of `src/`
//! (`style.rs`, `technical.rs`, `lib.rs`) is a portable core that never names a
//! specific font project. To retarget the whole system to another font repo,
//! edit ONLY the constants and paths below (see the README's "Reusing in
//! another repo" section), then write new content binaries under `src/bin/`.

use std::path::PathBuf;

// --- repository identity ------------------------------------------------------
// The project's names/URLs, kept out of the shared drawing code so the content
// binaries' chrome (running head, footer attribution) stays copy-verbatim and
// only these strings change per repo.

/// Running-head brand mark shown in slide/reel chrome (all-caps house style).
pub const BRAND: &str = "VIRTUA GROTESK";
/// Short attribution URL shown in footer chrome.
pub const BRAND_URL: &str = "elih.net/blog/virtua-grotesk";
/// Human-readable family/project name for in-copy references.
pub const PROJECT: &str = "Virtua Grotesk";

// --- specimen furniture (the four mono corner labels) ------------------------
// Portable strings for the foundry-post chrome. A new repo edits only these.

/// Top-left wordmark, drawn after the ⊞ foundry mark.
pub const FOUNDRY: &str = "Font.Garden/virtua";
/// Top-right license line.
pub const LICENSE: &str = "Open Font License OFL v1.1";
/// Bottom-right source URL.
pub const REPO: &str = "github.com/eliheuer/virtua-grotesk";
/// Family version, folded into the bottom-left label.
pub const VERSION: &str = "v0.1";

fn user_root() -> PathBuf {
    std::env::var_os("HOME")
        .map(PathBuf::from)
        .expect("HOME must identify the user checkout root")
}

/// The Virtua Grotesk repository root that contains this crate. Resolved from
/// the crate manifest so the worktree copy is used, not a sibling checkout.
pub fn virtua_repo() -> PathBuf {
    // scripts/social/ -> scripts/ -> <repo root>
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(std::path::Path::parent)
        .expect("crate must live at <repo>/scripts/social")
        .to_path_buf()
}

pub fn virtua_sources() -> PathBuf {
    virtua_repo().join("sources")
}

/// Committed home for rendered social assets (Google Fonts documentation
/// convention). Retarget with the repo in a new project.
pub fn social_assets() -> PathBuf {
    virtua_repo().join("documentation/social-assets")
}

pub fn regular_ufo() -> PathBuf {
    virtua_sources().join("VirtuaGrotesk-Regular.ufo")
}

pub fn bold_ufo() -> PathBuf {
    virtua_sources().join("VirtuaGrotesk-Bold.ufo")
}

/// Geist Mono is the label/typography face across the whole figure family.
pub fn geist_mono() -> PathBuf {
    user_root().join("GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf")
}
