//! Weight axis: the first word of brand.toml changes from the lightest weight
//! to the heaviest and back. A loop of 3 seconds.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round();
    let small = (w.min(h) / 30.0).round();
    let word = &b.words[0];
    let size = b.fit(&r, word, w - 2.0 * m, b.weight.1).min(h * 0.6 / b.cap);
    let frames = 90;
    ctx.frame_duration(1.0 / 30.0);

    for i in 0..frames {
        if i > 0 {
            ctx.new_page();
        }
        let weight = b.weight_at(ease_in_out_sine(ping_pong(i as f64 / frames as f64)));
        ctx.background(b.ground);
        ctx.fill(b.ink).no_stroke().font(&b.family).text_align(TextAlign::Left);

        ctx.font_size(size).clear_font_variations().font_variation("wght", weight);
        ctx.text(word, x + m, y + (h - size * b.cap) / 2.0);

        ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
        ctx.text(&b.family, x + m, y + h - m - small * b.cap);
        ctx.text(&format!("wght {:.0}", weight), x + m, y + m);

        // The position on the axis, as a line.
        let t = ((weight - b.weight.0) / (b.weight.1 - b.weight.0)) as f64;
        let (x0, x1, line_y) = (x + m + small * 6.0, x + w - m, y + m + small * b.cap / 2.0);
        ctx.fill(b.accent).rect(x0, line_y - 2.0, (x1 - x0) * t, 4.0);
        b.overlay(&mut ctx);
    }
    b.save(&r, &ctx);
}
