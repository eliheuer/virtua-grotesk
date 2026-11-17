//! Link card: the picture that a link to the font shows on a platform.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (h / 8.0).round();
    let small = (h / 18.0).round();

    ctx.background(b.ground);
    ctx.fill(b.ink).no_stroke().font(&b.family).text_align(TextAlign::Left);
    let size = b.fit(&r, &b.family, w - 2.0 * m, b.weight.1);
    ctx.font_size(size).clear_font_variations().font_variation("wght", b.weight.1);
    ctx.text(&b.family, x + m, y + (h - size * b.cap) / 2.0);
    ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
    ctx.text(&b.tagline, x + m, y + m);
    ctx.text(&b.designer, x + m, y + h - m - small * b.cap);
    ctx.text_align(TextAlign::Right);
    ctx.text(&b.url, x + w - m, y + h - m - small * b.cap);

    b.overlay(&mut ctx);
    b.save(&r, &ctx);
}
