//! Virtua Grotesk — landscape specimen (1.91:1, X / LinkedIn card).
//!
//! Render from the repo root:
//!   designbot documentation/specimen-landscape.rs
//!
//! The wide canvas reflows the charset into three long rows. Edit the strings
//! + the explicit layout numbers below by hand.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark(); // try Theme::light() / Theme::black()
    let f = Format::Landscape;
    let (w, h) = (f.w(), f.h());
    let m = f.margin();

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font("fonts/ttf/VirtuaGrotesk-Regular.ttf").expect("Virtua Grotesk");
    r.load_font("/Users/eli/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf")
        .expect("Geist Mono");

    ctx.background(t.ground);

    // corner furniture (mono)
    ctx.font("Geist Mono").font_size(30.0).fill(t.furniture);
    ctx.text_align(TextAlign::Left).text("Font.Garden/virtua", m, h - m);
    ctx.text_align(TextAlign::Right).text("Open Font License OFL v1.1", w - m, h - m);
    ctx.text_align(TextAlign::Left).text("Virtua Grotesk Regular v0.1", m, m);
    ctx.text_align(TextAlign::Right).text("github.com/eliheuer/virtua-grotesk", w - m, m);

    ctx.no_fill().stroke(t.rule).stroke_width(2.0);
    ctx.line(m, h - m - 52.0, w - m, h - m - 52.0);
    ctx.line(m, m + 60.0, w - m, m + 60.0);

    // three long rows fill the width — explicit numbers, edit freely
    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);
    let (size, lead) = (128.0, 330.0);
    let mut y = h - m - 190.0;
    for row in ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789"] {
        ctx.font_size(size).text(row, m, y);
        y -= lead;
    }

    r.render_to_png(&ctx, "documentation/specimen-landscape.png").expect("render");
}
