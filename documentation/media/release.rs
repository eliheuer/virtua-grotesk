//! Release: the name, the version and the facts of the font, read from the
//! font file.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round();
    let small = (w.min(h) / 30.0).round();

    ctx.background(b.ground);
    ctx.fill(b.ink).no_stroke().font(&b.family).text_align(TextAlign::Left);

    // The name, one word for each line, in the heaviest weight.
    let words: Vec<&str> = b.family.split(' ').collect();
    let size = words.iter().map(|word| b.fit(&r, word, w - 2.0 * m, b.weight.1)).fold(f64::INFINITY, f64::min)
        .min(h * 0.22 / b.cap);
    let mut baseline = y + h - m - small * 3.0 - size * b.cap;
    ctx.font_size(size).clear_font_variations().font_variation("wght", b.weight.1);
    for word in &words {
        ctx.text(word, x + m, baseline);
        baseline -= size * (b.cap + 0.22);
    }

    // The facts, from the font file.
    let weights = if b.weight.1 > b.weight.0 {
        format!("Weights {:.0} to {:.0}, one variable font", b.weight.0, b.weight.1)
    } else {
        format!("Weight {:.0}", b.weight.0)
    };
    let facts = [format!("Version {}", b.version), weights,
                 format!("{} glyphs, {} characters", b.glyphs, b.characters), b.tagline.clone()];
    ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
    let mut line_y = y + m + small * 1.6 * (facts.len() as f64 + 1.0);
    for fact in facts.iter() {
        ctx.text(fact, x + m, line_y);
        line_y -= small * 1.6;
    }
    ctx.fill(b.accent);
    ctx.text(&b.url, x + m, y + m);
    ctx.fill(b.ink);
    ctx.text(&b.designer, x + m, y + h - m - small * b.cap);
    ctx.text_align(TextAlign::Right);
    ctx.text("SIL Open Font License", x + w - m, y + h - m - small * b.cap);

    b.overlay(&mut ctx);
    b.save(&r, &ctx);
}
