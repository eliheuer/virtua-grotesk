//! Character set: one page for each group of characters, in the lightest and
//! the heaviest weight.

use designbot::prelude::*;

const PAGES: &[(&str, &[&str])] = &[
    ("Capital letters", &["ABCDEFG", "HIJKLMN", "OPQRSTU", "VWXYZ"]),
    ("Small letters", &["abcdefgh", "ijklmnop", "qrstuvwx", "yz"]),
    ("Figures and punctuation", &["0123456789", ".,:;!?&@#", "()[]{}/*", "$%+-=<>"]),
];

fn main() {
    let b = brief::load();
    let mut ctx = b.canvas();
    let r = b.renderer();
    let (x, y, w, h) = b.safe;
    let m = (w.min(h) / 16.0).round();
    let small = (w.min(h) / 36.0).round();
    let mut first = true;

    for (title, rows) in PAGES {
        for weight in [b.weight.0, b.weight.1] {
            if !first {
                ctx.new_page();
            }
            first = false;
            ctx.background(b.ground);
            ctx.fill(b.ink).no_stroke().font(&b.family).text_align(TextAlign::Left);
            ctx.font_size(small).clear_font_variations().font_variation("wght", b.weight.0);
            ctx.text(&format!("{}  ·  {}", b.family, title), x + m, y + h - m - small * b.cap);
            ctx.text(&format!("wght {:.0}", weight), x + m, y + m);

            // One size for the page: the widest row is as wide as the safe area.
            let size = rows.iter().map(|row| b.fit(&r, row, w - 2.0 * m, weight)).fold(f64::INFINITY, f64::min);
            let leading = size * 1.25;
            let block = (rows.len() - 1) as f64 * leading + size * b.cap;
            let mut baseline = y + (h + block) / 2.0 - size * b.cap;
            ctx.font_size(size).clear_font_variations().font_variation("wght", weight);
            for row in rows.iter() {
                ctx.text(row, x + m, baseline);
                baseline -= leading;
            }
            b.overlay(&mut ctx);
        }
    }
    b.save(&r, &ctx);
}
