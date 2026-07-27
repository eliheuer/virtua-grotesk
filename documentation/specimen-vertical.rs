//! Virtua Grotesk — vertical specimen (9:16, Reels / Stories).
//!
//! Render from the repo root:
//!   designbot documentation/specimen-vertical.rs
//!
//! Everything reusable lives in designbot; edit the strings + the explicit
//! layout numbers below by hand.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark(); // try Theme::light() / Theme::black()
    let f = Format::Vertical;
    let (w, h) = (f.w(), f.h());
    let m = f.margin();

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font("fonts/ttf/VirtuaGrotesk-Regular.ttf").expect("Virtua Grotesk");
    r.load_font("/Users/eli/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf")
        .expect("Geist Mono");

    ctx.background(t.ground);

    // corner furniture (mono) — smaller on this narrow canvas
    ctx.font("Geist Mono").font_size(22.0).fill(t.furniture);
    ctx.text_align(TextAlign::Left).text("Font.Garden/virtua", m, h - m);
    ctx.text_align(TextAlign::Right).text("Open Font License OFL v1.1", w - m, h - m);
    ctx.text_align(TextAlign::Left).text("Virtua Grotesk Regular v0.1", m, m);
    ctx.text_align(TextAlign::Right).text("github.com/eliheuer/virtua-grotesk", w - m, m);

    ctx.no_fill().stroke(t.rule).stroke_width(2.0);
    ctx.line(m, h - m - 40.0, w - m, h - m - 40.0);
    ctx.line(m, m + 48.0, w - m, m + 48.0);

    // specimen rows — explicit numbers, edit freely
    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);
    let (size, lead) = (150.0, 232.0);
    let mut y = h - m - 180.0;
    for row in [
        "ABCDEFGHIJ", "KLMNOPQR", "STUVWXYZ", "0123456789", "abcdefghij", "klmnopqr", "stuvwxyz",
    ] {
        ctx.font_size(size).text(row, m, y);
        y -= lead;
    }

    r.render_to_png(&ctx, "documentation/specimen-vertical.png").expect("render");
}
