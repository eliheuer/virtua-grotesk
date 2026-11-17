//! Glyph detail: one glyph for each page, large, on the grid of the design,
//! with the vertical metrics of the font as labelled lines. The glyphs are the
//! `words` of this format in brand.toml.

use designbot::prelude::*;

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round();
    let small = (w.min(h) / 40.0).round();
    let grid_color = Color::rgba(255, 255, 255, 22);
    let line_color = Color::rgba(255, 255, 255, 90);

    for (page, glyph) in b.words.iter().enumerate() {
        if page > 0 {
            ctx.new_page();
        }
        ctx.background(b.ground);

        // The em is as high as the space between the head line and the foot line.
        let (top, bottom) = (y + h - m - small * 3.0, y + m + small * 3.0);
        let size = (top - bottom) / (b.ascender - b.descender);
        let baseline = bottom - b.descender * size;
        let unit = size / b.upm;
        let step = b.grid * unit;

        // The grid of the design, in font units from the baseline and the center.
        let center = x + w / 2.0;
        ctx.no_fill().stroke(grid_color).stroke_width(1.0);
        let mut gx = center % step;
        while gx < b.width {
            ctx.line(gx, 0.0, gx, b.height);
            gx += step;
        }
        let mut gy = baseline % step;
        while gy < b.height {
            ctx.line(0.0, gy, b.width, gy);
            gy += step;
        }

        // The vertical metrics.
        let lines = [("ascender", b.ascender), ("cap height", b.cap), ("x-height", b.x_height),
                     ("baseline", 0.0), ("descender", b.descender)];
        for (name, value) in lines {
            let line_y = baseline + value * size;
            ctx.no_fill().stroke(line_color).stroke_width(2.0);
            ctx.line(x + m, line_y, x + w - m, line_y);
            ctx.no_stroke().fill(b.ink).font(&b.family).font_size(small);
            ctx.clear_font_variations().font_variation("wght", b.weight.0).text_align(TextAlign::Left);
            ctx.text(name, x + m, line_y + small * 0.4);
            ctx.text_align(TextAlign::Right);
            ctx.text(&format!("{:.0}", value * b.upm), x + w - m, line_y + small * 0.4);
        }

        // The glyph, in the heaviest weight behind and the lightest weight in front.
        ctx.no_stroke().font(&b.family).font_size(size).text_align(TextAlign::Center);
        if b.weight.1 > b.weight.0 {
            ctx.fill(b.accent.with_alpha(70)).clear_font_variations().font_variation("wght", b.weight.1);
            ctx.text(glyph, center, baseline);
        }
        ctx.fill(b.ink).clear_font_variations().font_variation("wght", b.weight.0);
        ctx.text(glyph, center, baseline);

        // The head line and the foot line.
        ctx.font_size(small).text_align(TextAlign::Left);
        ctx.text(&b.family, x + m, y + h - m - small * b.cap);
        ctx.text(&format!("{:.0} units of the em, grid of {:.0}", b.upm, b.grid), x + m, y + m);
        ctx.text_align(TextAlign::Right);
        ctx.text(&format!("{} of {}", page + 1, b.words.len()), x + w - m, y + h - m - small * b.cap);
        b.overlay(&mut ctx);
    }
    b.save(&r, &ctx);
}
