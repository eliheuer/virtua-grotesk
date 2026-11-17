//! Scripts: one page for each line of the `words` of this format in
//! brand.toml, for example one line in each script of the font.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round();
    let small = (w.min(h) / 36.0).round();

    for (page, line) in b.words.iter().enumerate() {
        if page > 0 {
            ctx.new_page();
        }
        ctx.background(b.ground);
        ctx.fill(b.ink).no_stroke().font(&b.family);
        ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
        ctx.text_align(TextAlign::Left);
        ctx.text(&b.family, x + m, y + h - m - small * b.cap);
        ctx.text(&b.tagline, x + m, y + m);
        ctx.text_align(TextAlign::Right);
        ctx.text(&format!("{} of {}", page + 1, b.words.len()), x + w - m, y + h - m - small * b.cap);

        // The line in the lightest and the heaviest weight, each as wide as the safe area.
        let space = h - 2.0 * m - small * 6.0;
        let mut top = y + h - m - small * 3.0;
        let weights = if b.weight.1 > b.weight.0 { vec![b.weight.0, b.weight.1] } else { vec![b.weight.0] };
        for weight in &weights {
            let size = b.fit(&r, line, w - 2.0 * m, *weight).min(space / weights.len() as f64 / 1.3);
            let row = space / weights.len() as f64;
            ctx.font_size(size).clear_font_variations().font_variation("wght", *weight);
            ctx.text_align(TextAlign::Center);
            ctx.text(line, x + w / 2.0, top - row / 2.0 - size * b.cap / 2.0);
            top -= row;
        }
        b.overlay(&mut ctx);
    }
    b.save(&r, &ctx);
}
