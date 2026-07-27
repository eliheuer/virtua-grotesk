//! Swappable color themes — the heart of the reusable image factory.
//!
//! A [`Theme`] is a complete set of *neutral* roles (ground, ink, furniture,
//! rules, figure pen, grid tiers, point fills) plus the shared semantic hues.
//! Compositions never name a raw color; they read the ACTIVE theme through the
//! `role` layer in `style.rs`. Rendering the same composition under a different
//! theme is therefore free — `--theme light` vs `--theme dark` re-skins every
//! specimen, figure, and animation frame with no change to the drawing code.
//!
//! The semantic hues (green/red/yellow/…) come from the shared OKLCH palette so
//! they read at even intensity on any ground; a theme is free to override them.
//!
//! PORTABLE CORE: no project names here. Add or edit themes freely; this file
//! travels verbatim into any repo that adopts the factory.

use crate::style::color;
use designbot::prelude::Color;
use std::sync::OnceLock;

/// A complete, swappable color scheme.
#[derive(Clone, Copy, Debug)]
pub struct Theme {
    pub name: &'static str,
    // --- neutrals: the theme's whole personality lives here ---
    /// Page background.
    pub ground: Color,
    /// Primary type: specimen fill, big display glyphs.
    pub ink: Color,
    /// Monospace corner furniture (foundry mark, license, family, repo).
    pub furniture: Color,
    /// Hairline rules.
    pub rule: Color,
    /// Drawing pen for technical figures (glyph outline, dimension lines).
    pub pen: Color,
    /// Ground *inside* a technical figure (often == ground; may be a panel).
    pub figure_ground: Color,
    // grid tiers, faint -> major
    pub grid_faint: Color,
    pub grid_subtle: Color,
    pub grid_standard: Color,
    pub grid_major: Color,
    // point language fills (structure vs optical-correction tier)
    pub point_fill: Color,
    pub correction_fill: Color,
    // --- shared semantic hues (OKLCH by default) ---
    pub green: Color,
    pub red: Color,
    pub yellow: Color,
    pub orange: Color,
    pub blue: Color,
    pub purple: Color,
    /// The single brand accent a minimalist card may use (Aeonik-yellow idea).
    pub accent: Color,
}

impl Theme {
    /// Dark ground, light type — the Font.Garden house default.
    pub fn dark() -> Self {
        Theme {
            name: "dark",
            ground: color::gray_900(),  // #1a1a1a
            ink: color::gray_200(),     // #bebebe
            furniture: color::gray_350(), // #92928e
            rule: color::gray_700(),    // #3a3a3a
            pen: color::gray_100(),     // #e6e6e6 (light pen on dark)
            figure_ground: color::gray_900(),
            grid_faint: color::gray_850(),
            grid_subtle: color::gray_800(),
            grid_standard: color::gray_700(),
            grid_major: color::gray_600(),
            point_fill: color::gray_400(),
            correction_fill: color::gray_200(),
            green: color::green(),
            red: color::red(),
            yellow: color::yellow(),
            orange: color::orange(),
            blue: color::blue(),
            purple: color::purple(),
            accent: color::yellow(),
        }
    }

    /// Light ground, dark type — the same cards, flipped.
    pub fn light() -> Self {
        Theme {
            name: "light",
            ground: Color::rgb(0xef, 0xee, 0xea), // warm off-white
            ink: Color::rgb(0x24, 0x24, 0x22),    // near-black type
            furniture: Color::rgb(0x6a, 0x6a, 0x66),
            rule: Color::rgb(0xd6, 0xd5, 0xd0),
            pen: color::gray_950(),               // #101010 dark pen
            figure_ground: Color::rgb(0xe4, 0xe3, 0xdf),
            grid_faint: Color::rgb(0xdd, 0xdc, 0xd7),
            grid_subtle: Color::rgb(0xcd, 0xcc, 0xc6),
            grid_standard: Color::rgb(0xb2, 0xb1, 0xaa),
            grid_major: Color::rgb(0x94, 0x93, 0x8c),
            point_fill: Color::rgb(0xf6, 0xf5, 0xf2),
            correction_fill: Color::rgb(0xff, 0xff, 0xff),
            green: color::green(),
            red: color::red(),
            yellow: color::yellow(),
            orange: color::orange(),
            blue: color::blue(),
            purple: color::purple(),
            accent: color::red(),
        }
    }

    /// Near-black ground, brighter ink — high-contrast variant.
    pub fn black() -> Self {
        Theme {
            name: "black",
            ground: color::black_deep(), // #0a0a0a
            ink: color::gray_100(),      // #e6e6e6
            furniture: color::gray_400(),
            rule: color::gray_800(),
            pen: color::gray_100(),
            figure_ground: color::black_deep(),
            ..Theme::dark()
        }
    }
}

/// Look a theme up by name (used by `--theme <name>`). Unknown -> dark.
pub fn by_name(name: &str) -> Theme {
    match name.trim().to_ascii_lowercase().as_str() {
        "light" => Theme::light(),
        "black" => Theme::black(),
        _ => Theme::dark(),
    }
}

/// Every theme, for "render all" batch scripts and self-documentation.
pub fn all() -> Vec<Theme> {
    vec![Theme::dark(), Theme::light(), Theme::black()]
}

// --- process-global active theme --------------------------------------------
// A render process renders under exactly one theme (chosen by `--theme`), so a
// set-once global is the right model: the `role` layer reads it with no plumbing
// through every drawing call.

static ACTIVE: OnceLock<Theme> = OnceLock::new();

/// Set the active theme once, at program start. Later calls are ignored.
pub fn set_active(theme: Theme) {
    let _ = ACTIVE.set(theme);
}

/// The active theme (defaults to `dark` if none was set).
pub fn active() -> Theme {
    *ACTIVE.get_or_init(Theme::dark)
}
