//! Editable visual system for the DesignBot social compositions.
//!
//! PORTABLE CORE: no project-specific names live here; it is copied verbatim
//! into a new repo. Only `inputs.rs` and the content binaries change per repo.
//!
//! This is a faithful port of the blog-figure crate's `style.rs`
//! (`~/GH/repos/elih.net/scripts/virtua-grotesk/src/style.rs`). Keeping the
//! color-management layer identical is a deliberate handoff requirement from
//! that crate's README: the social assets must begin from the same reviewed
//! OKLCH palette as the inline blog figures so the two families read as one.
//!
//! Work from top to bottom:
//! 1. `color` — context-free illustration swatches (appearance names only).
//! 2. `line` and `type_size` — context-free numeric scales.
//! 3. `role` — maps those primitives to drawing jobs.
//!
//! Binaries under `src/bin/` should use `role`/`color`/`line`/`type_size`
//! values instead of embedding RGB or line-width literals. Layout and content
//! belong in each binary.

use designbot::prelude::Color;

// --- perceptual color -------------------------------------------------------

/// Convert an OKLCH swatch to 8-bit sRGB, reducing chroma at constant
/// lightness and hue when the requested color falls outside the sRGB gamut.
/// See the blog-figure crate's `style.rs` for the full rationale; the short
/// version is that equal OKLCH chroma is a far better starting point for an
/// even-intensity palette than equal HSL saturation or clamped RGB channels.
fn oklch_srgb(lightness: f64, requested_chroma: f64, hue_degrees: f64) -> Color {
    fn linear_srgb(lightness: f64, chroma: f64, hue_degrees: f64) -> [f64; 3] {
        let hue = hue_degrees.to_radians();
        let a = chroma * hue.cos();
        let b = chroma * hue.sin();

        let l_root = lightness + 0.396_337_777_4 * a + 0.215_803_757_3 * b;
        let m_root = lightness - 0.105_561_345_8 * a - 0.063_854_172_8 * b;
        let s_root = lightness - 0.089_484_177_5 * a - 1.291_485_548 * b;
        let l = l_root.powi(3);
        let m = m_root.powi(3);
        let s = s_root.powi(3);

        [
            4.076_741_662_1 * l - 3.307_711_591_3 * m + 0.230_969_929_2 * s,
            -1.268_438_004_6 * l + 2.609_757_401_1 * m - 0.341_319_396_5 * s,
            -0.004_196_086_3 * l - 0.703_418_614_7 * m + 1.707_614_701 * s,
        ]
    }

    fn in_srgb_gamut(rgb: [f64; 3]) -> bool {
        rgb.into_iter().all(|channel| (0.0..=1.0).contains(&channel))
    }

    fn encode_srgb(channel: f64) -> u8 {
        let encoded = if channel <= 0.003_130_8 {
            12.92 * channel
        } else {
            1.055 * channel.powf(1.0 / 2.4) - 0.055
        };
        (encoded.clamp(0.0, 1.0) * 255.0).round() as u8
    }

    let mut low = 0.0;
    let mut high = requested_chroma;
    let mut rgb = linear_srgb(lightness, requested_chroma, hue_degrees);
    if !in_srgb_gamut(rgb) {
        for _ in 0..24 {
            let middle = (low + high) / 2.0;
            let candidate = linear_srgb(lightness, middle, hue_degrees);
            if in_srgb_gamut(candidate) {
                low = middle;
                rgb = candidate;
            } else {
                high = middle;
            }
        }
    }

    Color::rgb(encode_srgb(rgb[0]), encode_srgb(rgb[1]), encode_srgb(rgb[2]))
}

// --- primitive line-width scale ---------------------------------------------
//
// Scaled up relative to the 2520x1320 blog card: social canvases are viewed
// small on a phone, so the drawing pen and grid are a touch heavier.

pub mod line {
    pub const HAIRLINE: f64 = 1.0;
    pub const FINE: f64 = 2.0;
    pub const THIN: f64 = 2.5;
    pub const MEDIUM: f64 = 3.0;
    pub const STRONG: f64 = 4.0;
    pub const CURVE: f64 = 4.5;
    pub const REGULAR: f64 = 5.0;
    pub const HEAVY: f64 = 6.0;
    pub const HERO: f64 = 8.0;
    pub const BOX: f64 = 10.0;
    pub const EXTRA_HEAVY: f64 = 12.0;
}

// --- primitive type-size scale ----------------------------------------------

pub mod type_size {
    pub const XS: f64 = 30.0;
    pub const SM: f64 = 34.0;
    pub const MD: f64 = 40.0;
    pub const LG: f64 = 48.0;
    pub const XL: f64 = 60.0;
    pub const XXL: f64 = 80.0;
    pub const DISPLAY: f64 = 120.0;
}

// --- primitive color swatches ------------------------------------------------
// Names describe appearance only. No swatch name encodes a drawing purpose.

pub mod color {
    use super::{oklch_srgb, Color};

    const FIGURE_CHROMA: f64 = 0.16;
    const RED_OPTICAL_CHROMA_BOOST: f64 = 0.015;

    pub fn black_deep() -> Color {
        Color::rgb(0x0a, 0x0a, 0x0a)
    }
    pub fn gray_950() -> Color {
        Color::rgb(0x10, 0x10, 0x10)
    }
    pub fn gray_925() -> Color {
        Color::rgb(0x18, 0x18, 0x18)
    }
    pub fn gray_900() -> Color {
        Color::rgb(0x1a, 0x1a, 0x1a)
    }
    pub fn gray_890() -> Color {
        Color::rgb(0x23, 0x23, 0x23)
    }
    pub fn gray_850() -> Color {
        Color::rgb(0x28, 0x28, 0x28)
    }
    pub fn gray_800() -> Color {
        Color::rgb(0x30, 0x30, 0x30)
    }
    pub fn gray_700() -> Color {
        Color::rgb(0x3a, 0x3a, 0x3a)
    }
    pub fn gray_650() -> Color {
        Color::rgb(0x40, 0x40, 0x40)
    }
    pub fn gray_600() -> Color {
        Color::rgb(0x4a, 0x4a, 0x4a)
    }
    pub fn gray_550() -> Color {
        Color::rgb(0x5a, 0x5a, 0x5a)
    }
    pub fn gray_500() -> Color {
        Color::rgb(0x60, 0x60, 0x60)
    }
    pub fn gray_475() -> Color {
        Color::rgb(0x66, 0x66, 0x66)
    }
    pub fn gray_400() -> Color {
        Color::rgb(0x78, 0x78, 0x78)
    }
    pub fn gray_350() -> Color {
        Color::rgb(0x92, 0x92, 0x8e)
    }
    pub fn gray() -> Color {
        gray_350()
    }
    pub fn gray_200() -> Color {
        Color::rgb(0xbe, 0xbe, 0xbe)
    }
    pub fn gray_100() -> Color {
        Color::rgb(0xe6, 0xe6, 0xe6)
    }
    pub fn green() -> Color {
        oklch_srgb(0.67, FIGURE_CHROMA, 159.0)
    }
    pub fn orange() -> Color {
        oklch_srgb(0.74, FIGURE_CHROMA, 52.0)
    }
    pub fn yellow() -> Color {
        oklch_srgb(0.88, FIGURE_CHROMA, 92.0)
    }
    pub fn red() -> Color {
        oklch_srgb(0.66, FIGURE_CHROMA + RED_OPTICAL_CHROMA_BOOST, 28.0)
    }
    pub fn blue() -> Color {
        oklch_srgb(0.65, FIGURE_CHROMA, 258.0)
    }
    pub fn purple() -> Color {
        oklch_srgb(0.65, FIGURE_CHROMA, 302.0)
    }
    pub fn pink() -> Color {
        oklch_srgb(0.74, FIGURE_CHROMA, 342.0)
    }
}

pub use color::{blue, gray, green, orange, purple, red, yellow};

// --- semantic mappings -------------------------------------------------------
// These functions contain no RGB values. They assign base swatches to drawing
// jobs, so palette edits and role edits remain separate decisions.

pub mod role {
    /// Shared appearance of the figures, mirroring the blog crate's `figure`
    /// role so social art matches the inline illustrations.
    pub mod figure {
        use super::super::{color, Color};

        pub fn background() -> Color {
            color::gray_350()
        }
        pub fn pen() -> Color {
            color::gray_900()
        }
        pub fn point_fill() -> Color {
            color::gray_200()
        }
        pub fn correction_point_fill() -> Color {
            color::gray_100()
        }
        pub fn red() -> Color {
            color::red()
        }
        pub fn orange() -> Color {
            color::orange()
        }
        pub fn yellow() -> Color {
            color::yellow()
        }
        pub fn green() -> Color {
            color::green()
        }
        pub fn blue() -> Color {
            color::blue()
        }
        pub fn purple() -> Color {
            color::purple()
        }
    }

    pub mod canvas {
        use super::super::{color, Color};

        pub fn background() -> Color {
            color::gray_350()
        }
    }

    pub mod grid {
        use super::super::{color, Color};

        pub fn faint() -> Color {
            color::gray_475()
        }
        pub fn subtle() -> Color {
            color::gray_400()
        }
        pub fn standard() -> Color {
            color::gray_650()
        }
        pub fn major() -> Color {
            color::gray_800()
        }
    }

    pub mod text {
        use super::super::type_size;

        pub const DISPLAY: f64 = type_size::DISPLAY;
        pub const TITLE: f64 = type_size::XXL;
        pub const HEAD: f64 = type_size::XL;
        pub const BODY: f64 = type_size::MD;
        pub const LABEL: f64 = type_size::SM;
        pub const CAPTION: f64 = type_size::XS;
        pub const DIMENSION: f64 = type_size::MD;
    }

    pub mod line {
        use super::super::line;

        pub const GRID: f64 = line::FINE;
        pub const PEN: f64 = line::HERO;
        pub const DIMENSION: f64 = line::STRONG;
    }
}

pub fn with_alpha(color: Color, alpha: u8) -> Color {
    Color::rgba(color.r, color.g, color.b, alpha)
}
