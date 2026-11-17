//! Specimen poster: the words of brand.toml, each as wide as the safe area,
//! from the lightest weight at the top to the heaviest at the bottom.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round(); // margin inside the safe area
    let small = (w.min(h) / 36.0).round();

    ctx.background(b.ground);
    ctx.fill(b.ink).no_stroke().font(&b.family);

    // The head line and the foot line.
    ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
    ctx.text(&b.family, x + m, y + h - m - small * b.cap);
    ctx.text_align(TextAlign::Right);
    ctx.text(&format!("{:.0} to {:.0}", b.weight.0, b.weight.1), x + w - m, y + h - m - small * b.cap);
    ctx.text(&b.url, x + w - m, y + m);
    ctx.text_align(TextAlign::Left);
    ctx.text(&b.tagline, x + m, y + m);

    // The words: as many as fit between the two lines.
    let (top, bottom) = (y + h - m - small * 3.0, y + m + small * 3.0);
    // A line is as high as the capitals and the descenders of its size.
    let line = |size: f64| size * (b.cap + 0.26);
    let mut sizes = Vec::new();
    let mut used = 0.0;
    for (i, word) in b.words.iter().enumerate() {
        let weight = b.weight_at(i as f64 / (b.words.len().max(2) - 1) as f64);
        // A word is never higher than the space between the two lines.
        let size = b.fit(&r, word, w - 2.0 * m, weight).min((top - bottom) / (b.cap + 0.26));
        if used + line(size) > top - bottom + 0.5 {
            break;
        }
        used += line(size);
        sizes.push((word, weight, size));
    }
    let mut line_top = (top + bottom) / 2.0 + used / 2.0 - 0.13 * sizes.first().map_or(0.0, |s| s.2);
    for (word, weight, size) in sizes {
        ctx.font_size(size).clear_font_variations().font_variation("wght", weight);
        ctx.text(word, x + m, line_top - size * b.cap);
        line_top -= line(size);
    }

    b.overlay(&mut ctx);
    b.save(&r, &ctx);
}
