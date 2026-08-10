//! Runebender — DVD-logo reel (9:16, Instagram Reels).
//!
//! The Runebender editor screenshot (`rb-ss-001.png`, transparent PNG,
//! co-located with this script) bounces around the frame like the classic
//! idle DVD logo. Behind it, a full-bleed grid of repeated "runebender.org"
//! in the manner of the 1962 *Capital* magazine cover: near-black ground,
//! most words a barely-there dark gray, a shifting subset lit in warm cream.
//!
//!   designbot --render documentation/social-assets/reels/runebender-dvd.rs \
//!             --output documentation/social-assets/reels/runebender-dvd.mp4   # needs ffmpeg
//!
//! Coordinates are y-up (origin bottom-left), like DrawBot.

use designbot::image::imageops::FilterType;
use designbot::prelude::*;

const FAMILY: &str = "Virtua Grotesk";
const WORD: &str = "runebender.org";

// --- deterministic PRNG (no external crate) ---------------------------------
struct Rng(u64);
impl Rng {
    fn unit(&mut self) -> f64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 11) as f64) / ((1u64 << 53) as f64)
    }
}

/// One epoch's on/off pattern for the word grid: deterministic per epoch,
/// roughly `share` of the cells lit.
fn pattern(epoch: u64, cells: usize, share: f64) -> Vec<bool> {
    let mut rng = Rng(0xA076_1D64_78BD_642F ^ epoch.wrapping_mul(0x9E37_79B9_7F4A_7C15));
    (0..cells).map(|_| rng.unit() < share).collect()
}

fn main() {
    let f = Format::Vertical; // 1080 x 1920, Reels
    let (w, h) = (f.w(), f.h());

    // Capital-cover palette: near-black ground, ghost gray, warm cream.
    let bg = Color::rgb(0x14, 0x14, 0x12);
    let dim = Color::rgb(0x38, 0x38, 0x34);
    let lit = Color::rgb(0xc4, 0xbf, 0xae);

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk Regular");

    // --- the bouncing screenshot (transparent PNG, resized once) -------------
    // macOS screenshots carry a wide soft drop shadow + transparent padding;
    // trim to the near-opaque bounding box so the window itself fills the
    // rectangle we bounce (the faint shadow spill just reads as haze).
    let full = designbot::image::open(find_up(
        "documentation/social-assets/reels/rb-ss-001.png",
    ))
    .expect("rb-ss-001.png")
    .to_rgba8();
    let (mut x0, mut y0, mut x1, mut y1) = (u32::MAX, u32::MAX, 0u32, 0u32);
    for (px, py, p) in full.enumerate_pixels() {
        if p.0[3] >= 96 {
            x0 = x0.min(px);
            y0 = y0.min(py);
            x1 = x1.max(px);
            y1 = y1.max(py);
        }
    }
    let trimmed =
        designbot::image::imageops::crop_imm(&full, x0, y0, x1 - x0 + 1, y1 - y0 + 1).to_image();
    let th = (920.0 * trimmed.height() as f64 / trimmed.width() as f64).round() as u32;
    let img = designbot::image::imageops::resize(&trimmed, 920, th, FilterType::Lanczos3);
    let (iw, ih) = (img.width(), img.height());
    let pixels = img.into_raw();
    let (fw, fh) = (iw as f64, ih as f64);

    // --- the word grid: 2 columns of "runebender.org", full-bleed rows -------
    // Size the word so two columns + a gap fill the width inside the margins,
    // like the Capital cover's aligned columns.
    let margin = 56.0;
    let gap = 64.0;
    let usable = w - 2.0 * margin - gap;
    let w100 = r.text_width(WORD, Some(FAMILY), 100.0, &[]);
    let word_size = 100.0 * (usable / 2.0) / w100;
    let line_h = word_size * 1.42;
    let cols = 2;
    let rows = (h / line_h).ceil() as usize + 1;
    let cells = cols * rows;

    // --- DVD-logo motion state ------------------------------------------------
    let inset = 20.0; // the image's own transparent padding does the rest
    let (mut x, mut y) = (96.0, 420.0); // bottom-left anchor of the image
    let (mut vx, mut vy) = (104.0, 134.0); // px/s, slow drift, irrational-ish ratio

    // --- simulate + draw ------------------------------------------------------
    let fps = 30.0;
    let dt = 1.0 / fps;
    let seconds = 24.0;
    let frames = (seconds * fps) as usize;
    let epoch_frames = 84; // re-roll the lit words every 2.8s
    let fade_frames = 12.0; // crossfade into each new pattern
    ctx.frame_duration(dt);

    for frame in 0..frames {
        if frame > 0 {
            ctx.new_page();
        }

        // bounce
        x += vx * dt;
        y += vy * dt;
        if x < inset {
            x = inset;
            vx = vx.abs();
        }
        if x + fw > w - inset {
            x = w - inset - fw;
            vx = -vx.abs();
        }
        if y < inset {
            y = inset;
            vy = vy.abs();
        }
        if y + fh > h - inset {
            y = h - inset - fh;
            vy = -vy.abs();
        }

        // which words are lit: crossfade from the previous epoch's pattern
        let epoch = (frame / epoch_frames) as u64;
        let prev = pattern(epoch.saturating_sub(1), cells, 0.28);
        let cur = pattern(epoch, cells, 0.28);
        let t = ((frame % epoch_frames) as f64 / fade_frames).min(1.0);

        // draw
        ctx.background(bg);
        ctx.no_stroke().font(FAMILY).font_size(word_size).tracking(0.0).auto_line_height();
        ctx.text_align(TextAlign::Left);
        for row in 0..rows {
            let base = h - (row as f64 + 0.7) * line_h;
            for col in 0..cols {
                let i = row * cols + col;
                let a = lerp(
                    if prev[i] { 1.0 } else { 0.0 },
                    if cur[i] { 1.0 } else { 0.0 },
                    ease_in_out_sine(t),
                );
                let color = Color::rgb(
                    lerp(dim.r as f64, lit.r as f64, a) as u8,
                    lerp(dim.g as f64, lit.g as f64, a) as u8,
                    lerp(dim.b as f64, lit.b as f64, a) as u8,
                );
                ctx.fill(color);
                ctx.text(WORD, margin + col as f64 * (usable / 2.0 + gap), base);
            }
        }

        // the bouncing editor, on top
        ctx.image_rgba(pixels.clone(), iw, ih, x, y, 1.0);
    }

    r.render_to_mp4(&ctx, "documentation/social-assets/reels/runebender-dvd.mp4").expect("render");
    println!("{} frames", ctx.page_count());
}
