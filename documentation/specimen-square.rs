//! Virtua Grotesk — square specimen (1:1).
//!
//! Rendered with designbot. Run from the repo root:
//!   designbot --render documentation/specimen-square.rs \
//!             --output documentation/specimen-square.png --social
//!
//! Everything reusable (theme, palette, canonical size) lives in designbot.
//! Edit the strings and the explicit layout numbers below by hand.

use designbot::prelude::*;

fn main() {
    // design system + canvas
    let t = Theme::dark(); // try Theme::light() / Theme::black()
    let f = Format::Square;
    let (w, h) = (f.w(), f.h());
    let m = f.margin();

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font("fonts/ttf/VirtuaGrotesk-Regular.ttf").expect("Virtua Grotesk");
    r.load_font("/Users/eli/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf")
        .expect("Geist Mono");

    ctx.background(t.ground);

    // corner furniture (mono)
    ctx.font("Geist Mono").font_size(32.0).fill(t.furniture);
    ctx.text_align(TextAlign::Left).text("Font.Garden/virtua", m, h - m);
    ctx.text_align(TextAlign::Right).text("Open Font License OFL v1.1", w - m, h - m);
    ctx.text_align(TextAlign::Left).text("Virtua Grotesk Regular v0.1", m, m);
    ctx.text_align(TextAlign::Right).text("github.com/eliheuer/virtua-grotesk", w - m, m);

    // hairline rules
    ctx.no_fill().stroke(t.rule).stroke_width(2.0);
    ctx.line(m, h - m - 56.0, w - m, h - m - 56.0);
    ctx.line(m, m + 64.0, w - m, m + 64.0);

    // specimen rows — explicit numbers, edit freely
    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);
    let (size, lead) = (210.0, 214.0);
    let mut y = h - m - 200.0;
    for row in [
        "ABCDEFGHIJ", "KLMNOPQR", "STUVWXYZ", "0123456789", "abcdefghij", "klmnopqr", "stuvwxyz",
    ] {
        ctx.font_size(size).text(row, m, y);
        y -= lead;
    }

    r.render_to_png(&ctx, "documentation/specimen-square.png").expect("render");
}
