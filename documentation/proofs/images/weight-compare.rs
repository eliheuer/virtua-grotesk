//! Virtua Grotesk — weight-comparison proof images vs Inter and Geist.
//!
//! Square 2048 canvas, split horizontally: the SAME comparison on a dark
//! ground (top) and a light ground (bottom), because perceived weight flips
//! with polarity. Exactly two colors in the image — a near-black dark gray
//! and a 25% light gray — swapping roles as ground/ink per half.
//!
//! Reference fonts are normalized to Virtua's x-height (cap height for the
//! caps mode), the same normalization scripts/normalize_metrics.py uses, then
//! the whole set is scaled so the widest row fills the content width. Equal
//! 64 px margins (one grid unit) on all sides. Tracking is never set — all
//! rows shape at the fonts' default spacing.
//!
//!   designbot --render documentation/proofs/images/weight-compare.rs \
//!       --output documentation/proofs/images/weight-hono.png -- hono
//!
//! Modes: hono | basic | text    GRID_VIEW=1 for the layout grid.
//!
//! Inter/Geist load from the local google-fonts checkout (absolute paths —
//! machine-local proofing tool, not a build artifact).

use designbot::prelude::*;
use std::env;

const W: f64 = 2048.0;
const H: f64 = 2048.0;
const M: f64 = 64.0; // one grid unit, equal on all sides
const CW: f64 = W - 2.0 * M;

// The only two colors in the image.
const DARK: Color = Color { r: 28, g: 28, b: 28, a: 255 }; // near-black gray
const LIGHT: Color = Color { r: 191, g: 191, b: 191, a: 255 }; // 25% gray

const LABEL_FONT: &str = "Menlo";
const LABEL_SIZE: f64 = 28.0;

const WGHT: u32 = u32::from_be_bytes(*b"wght");

struct Fam {
    family: &'static str,
    label: &'static str,
    upm: f64,
    xh: f64,
    cap: f64,
}

// Helvetica Neue joins only the text mode (system font, no file to load).
const HELVETICA: Fam =
    Fam { family: "Helvetica Neue", label: "Helvetica Neue", upm: 1000.0, xh: 517.0, cap: 714.0 };

const FAMS: [Fam; 3] = [
    Fam { family: "Virtua Grotesk", label: "Virtua Grotesk", upm: 1024.0, xh: 576.0, cap: 768.0 },
    Fam { family: "Inter", label: "Inter", upm: 2048.0, xh: 1118.0, cap: 1490.0 },
    Fam { family: "Geist", label: "Geist", upm: 1000.0, xh: 530.0, cap: 710.0 },
];

fn main() {
    let mode = env::args().nth(1).unwrap_or_else(|| "hono".into());
    let grid_view = env::var("GRID_VIEW").map(|v| v == "1").unwrap_or(false);

    let mut r = Renderer::new(W as u32, H as u32);
    r.load_font(find_up("fonts/variable/VirtuaGrotesk[wght].ttf")).expect("Virtua");
    r.load_font("/Users/eli/GH/repos/google-fonts/ofl/inter/Inter[opsz,wght].ttf").expect("Inter");
    r.load_font("/Users/eli/GH/repos/google-fonts/ofl/geist/Geist[wght].ttf").expect("Geist");

    let mut ctx = Canvas::new(W, H);
    ctx.background(DARK);
    ctx.fill(LIGHT);
    ctx.rect(0.0, 0.0, W, H / 2.0);

    if grid_view {
        Grid::upm(1024.0).structural(64.0).margin(M).draw(&mut ctx, W, H);
    }

    // (half bottom y, ink color for that half)
    for (y0, ink) in [(H / 2.0, LIGHT), (0.0, DARK)] {
        match mode.as_str() {
            "hono" => rows(&mut ctx, &r, ink, y0, "HOnoHOnoHOno", false),
            "basic" => basic(&mut ctx, &r, ink, y0),
            "text" => paragraphs(&mut ctx, ink, y0),
            m => panic!("unknown mode {m}"),
        }
    }

    r.render_to_png(&ctx, "out.png").expect("render");
}

/// Normalized size for one family: `ref_px` of x-height (or cap height).
fn norm_size(f: &Fam, ref_px: f64, use_cap: bool) -> f64 {
    ref_px * f.upm / if use_cap { f.cap } else { f.xh }
}

/// Three rows (one per family), height-normalized, then scaled together so
/// the widest row spans the full content width. Baselines at 256/512/768
/// within the half (pure 4-unit grid), caption on the 64 margin seat below.
fn rows(ctx: &mut Canvas, r: &Renderer, ink: Color, y0: f64, s: &str, use_cap: bool) {
    // Probe at a reference height of 100 px, then fit the widest to CW.
    let widest = FAMS
        .iter()
        .map(|f| r.text_width(s, Some(f.family), norm_size(f, 100.0, use_cap), &[(WGHT, 400.0)]))
        .fold(0.0f64, f64::max);
    let ref_px = 100.0 * CW / widest;

    let mut y = y0 + 768.0; // top row first, stepping down 256
    for f in &FAMS {
        ctx.font(f.family);
        ctx.clear_font_variations();
        ctx.font_variation("wght", 400.0f32);
        ctx.fill(ink);
        ctx.font_size(norm_size(f, ref_px, use_cap));
        ctx.text(s, M, y);
        y -= 256.0;
    }
    caption(ctx, ink, y0, "Virtua Grotesk / Inter / Geist",
        if use_cap { "cap-height normalized" } else { "x-height normalized" });
}

/// A-Z and a-z per family, both lines at the SAME per-font size (so the
/// cap/lowercase relationship is the font's own), normalized across fonts by
/// cap height, fit so the widest line fills the content width. Six rows on a
/// uniform 128 px (2-unit) pitch.
fn basic(ctx: &mut Canvas, r: &Renderer, ink: Color, y0: f64) {
    const UC: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const LC: &str = "abcdefghijklmnopqrstuvwxyz";
    let widest = FAMS
        .iter()
        .flat_map(|f| {
            let size = norm_size(f, 100.0, true);
            [
                r.text_width(UC, Some(f.family), size, &[(WGHT, 400.0)]),
                r.text_width(LC, Some(f.family), size, &[(WGHT, 400.0)]),
            ]
        })
        .fold(0.0f64, f64::max);
    let ref_px = 100.0 * CW / widest;

    let mut y = y0 + 832.0; // six baselines: 832 down to 192, step 128
    for f in &FAMS {
        ctx.font(f.family);
        ctx.clear_font_variations();
        ctx.font_variation("wght", 400.0f32);
        ctx.fill(ink);
        ctx.font_size(norm_size(f, ref_px, true));
        ctx.text(UC, M, y);
        ctx.text(LC, M, y - 128.0);
        y -= 256.0;
    }
    caption(ctx, ink, y0, "Virtua Grotesk / Inter / Geist", "cap-height normalized");
}

/// Text-size color blocks: a two-line paragraph per family, 24 px x-height,
/// 64 px leading. Four families (system Helvetica Neue joins), pitch 224.
fn paragraphs(ctx: &mut Canvas, ink: Color, y0: f64) {
    let para = "Grumpy wizards make toxic brew for the evil queen and jack \
while 26 zebras vex him. HAMBURG Hamburg motorway MOTORWAY vexing OQENDS \
Gerangel quickly.";
    let mut yb = y0 + 928.0; // label baseline; box of 2 lines hangs below
    let fams: [&Fam; 4] = [&FAMS[0], &FAMS[1], &FAMS[2], &HELVETICA];
    for f in fams {
        ctx.fill(ink);
        label_style(ctx);
        ctx.text(f.label, M, yb);
        ctx.font(f.family);
        ctx.clear_font_variations();
        ctx.font_variation("wght", 400.0f32);
        ctx.font_size(norm_size(f, 24.0, false));
        ctx.line_height(64.0);
        ctx.text_box(para, M, yb - 160.0, CW, 128.0);
        yb -= 224.0;
    }
    caption(ctx, ink, y0, "Virtua Grotesk / Inter / Geist / Helvetica Neue", "x-height normalized");
}

/// One quiet caption per half, in the bottom margin band: order + method.
fn caption(ctx: &mut Canvas, ink: Color, y0: f64, who: &str, norm: &str) {
    ctx.fill(ink);
    label_style(ctx);
    ctx.text(&format!("{} — {}", who, norm), M, y0 + M);
}

/// Every auxiliary label: one mono font, one size, seated off the same
/// margins the type uses (x = left margin; caption baseline one margin
/// unit above each half's bottom edge).
fn label_style(ctx: &mut Canvas) {
    ctx.font(LABEL_FONT);
    ctx.clear_font_variations();
    ctx.font_size(LABEL_SIZE);
}
