//! Virtua Grotesk — README specimen (Regular).
//!
//! Powers-of-two canvas: 2048 x 1024. Height == the font's UPM (1024), width =
//! 2 UPM — so a 64px grid (UPM / 16) tiles it exactly (32 x 16 cells, no
//! cut-off) and lines up with the font's own coordinate system. Wide enough for
//! X / LinkedIn. Two colors only (theme ground + ink), no furniture, so a theme
//! swap re-skins the whole thing.
//!
//!   designbot documentation/readme-images/specimen-regular.rs
//!
//! Try Theme::dark() / Theme::light(). Edit the rows, margin, and grid below.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark(); // background = t.ground, type = t.ink
    let (w, h) = (2048.0, 1024.0); // powers of two; h == UPM
    let m = 128.0; // margin — a power of two, two 64-cells in

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    // find_up walks up from the current dir, so this works whether you run
    // designbot from the repo root or from this script's folder.
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk");

    ctx.background(t.ground);

    // Flip on while laying things out; off for the final image.
    const SHOW_GRID: bool = true;
    if SHOW_GRID {
        // Powers-of-two grid: 64px cells (= UPM / 16), 32px sub-lines,
        // full-bleed so every line lands exactly on 2048 x 1024.
        Grid::unit(64.0).subdivisions(2).color(t.grid).border(false).draw(&mut ctx, w, h);
        // Swiss / Müller-Brockmann alternative (columns x rows, gutter):
        // Grid::modular(16, 8).margin(0.0).gutter(0.0).color(t.grid).draw(&mut ctx, w, h);
    }

    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);

    let rows = [
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "1234567890 ß &?!£$(.,;:)",
    ];

    // One size for all rows: fit the widest (uppercase) to the margins.
    let content_w = w - 2.0 * m;
    let size = content_w / r.text_width(rows[1], Some("Virtua Grotesk"), 1.0, &[]);
    let cap = size * 0.72; // Virtua cap height as a fraction of the em

    // Distribute the three rows evenly down the live area (y-up: first highest).
    let slot = (h - 2.0 * m) / rows.len() as f64;
    for (i, row) in rows.iter().enumerate() {
        let baseline = (h - m) - slot * (i as f64 + 0.5) - cap / 2.0;
        ctx.font_size(size).text(row, m, baseline);
    }

    r.render_to_png(&ctx, "documentation/readme-images/specimen-regular.png").unwrap();
}
