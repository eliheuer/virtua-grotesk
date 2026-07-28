//! Virtua Grotesk — README specimen (Regular).
//!
//! DrawBot-style manual layout: you pick the dimensions, the font size, and the
//! line height, then place the rows. Because `line_height` is a power of two and
//! the block is snapped to the grid, every baseline lands on a grid line.
//! Two colors only (theme ground + ink), no furniture.
//!
//!   designbot documentation/readme-images/specimen-regular.rs

use designbot::prelude::*;

fn main() {
    let t = Theme::dark();
    let (w, h) = (1024.0, 1280.0); // you choose the dimensions
    let m = 64.0; // margin (a multiple of 64, the grid step)

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk");

    ctx.background(t.ground);

    const SHOW_GRID: bool = true; // on to see the baselines sit on the grid
    if SHOW_GRID {
        Grid::upm(1024.0).structural(64.0).margin(m).color(t.grid).draw(&mut ctx, w, h);
    }

    // --- the two knobs you tune by hand ---
    let size = 116.0; // font size; bigger = bigger type
    let line_height = 128.0; // baseline-to-baseline; a power of two → on the grid

    ctx.fill(t.ink).font("Virtua Grotesk").font_size(size);

    let rows = [
        "ABCDEFGHIJ",
        "KLMNOPQRS",
        "TUVWXYZ",
        "1234567890",
        "abcdefghijk",
        "lmnopqrstu",
        "vwxyz.,!?",
    ];

    // Center the block vertically and snap the first baseline to the grid, so
    // every row (stepping down by line_height) stays on a grid line.
    let block = (rows.len() as f64 - 1.0) * line_height;
    let mut y = ((h + block) / 2.0 / 64.0).round() * 64.0;
    for row in rows {
        ctx.text(row, m, y); // left-aligned at the margin
        y -= line_height; // step down one line
    }

    // (For flowing paragraphs, designbot also has DrawBot's textBox + lineHeight:
    //  ctx.line_height(line_height); ctx.text_box(&rows.join("\n"), m, m, w-2.0*m, h-2.0*m); )

    r.render_to_png(&ctx, "documentation/readme-images/specimen-regular.png").unwrap();
}
