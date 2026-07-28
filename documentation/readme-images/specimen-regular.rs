//! Virtua Grotesk — README specimen (Regular). Wide 1.91:1 card for X / LinkedIn.
//!
//! Two colors only: background = theme ground, type = theme ink. No furniture,
//! so swapping the theme re-skins the whole image.
//!
//!   designbot documentation/readme-images/specimen-regular.rs
//!
//! Try Theme::dark() / Theme::light(). Edit the rows, margin, and leading below.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark(); // background = t.ground, type = t.ink
    let f = Format::Landscape; // 2520 x 1320, the X / LinkedIn card ratio
    let (w, h) = (f.w(), f.h());
    let m = 100.0; // outer margin — smaller means bigger type

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font("fonts/ttf/VirtuaGrotesk-Regular.ttf").expect("Virtua Grotesk");

    ctx.background(t.ground);
    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);

    let rows = [
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "1234567890 ß &?!£$(.,;:)",
    ];

    // One size for all three rows: fit the widest (uppercase) to the margins.
    let content_w = w - 2.0 * m;
    let size = content_w / r.text_width(rows[1], Some("Virtua Grotesk"), 1.0, &[]);
    let cap = size * 0.72; // Virtua cap height as a fraction of the em

    // Distribute the three rows evenly down the live area (y-up: first highest),
    // each cap centered in its third, so the card fills top to bottom.
    let slot = (h - 2.0 * m) / rows.len() as f64;
    for (i, row) in rows.iter().enumerate() {
        let baseline = (h - m) - slot * (i as f64 + 0.5) - cap / 2.0;
        ctx.font_size(size).text(row, m, baseline);
    }

    r.render_to_png(&ctx, "documentation/readme-images/specimen-regular.png").unwrap();
}
