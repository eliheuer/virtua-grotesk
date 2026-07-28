//! Virtua Grotesk — README specimen (Regular).
//!
//! Portrait card, type sized to fill the width and LEFT-ALIGNED (ragged),
//! stacked to fill the height — the classic specimen layout. Portrait because a
//! full character set is a *tall* block (many short rows); matching the canvas
//! shape to the content is what makes it fall into place, no justification or
//! fussing. Two colors only (theme ground + ink), no furniture, so a theme swap
//! re-skins the whole thing.
//!
//!   designbot documentation/readme-images/specimen-regular.rs

use designbot::prelude::*;

fn main() {
    let t = Theme::dark();
    let (w, h) = (1024.0, 1280.0); // grid-clean 4:5 portrait; width == UPM
    let m = 64.0; // margin (keep a multiple of 64 so the grid stays aligned)

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk");

    ctx.background(t.ground);

    const SHOW_GRID: bool = false;
    if SHOW_GRID {
        Grid::upm(1024.0).structural(64.0).margin(m).color(t.grid).draw(&mut ctx, w, h);
    }

    // Natural chunks of the character set, roughly even in length (~10/row).
    let rows = [
        "ABCDEFGHIJ",
        "KLMNOPQRS",
        "TUVWXYZ",
        "1234567890",
        "abcdefghijk",
        "lmnopqrstu",
        "vwxyz.,!?",
    ];

    // One size: fit the widest row to the width (which binds on a portrait card,
    // so the type fills edge to edge), capped at one row per vertical slot so
    // adding rows never overflows.
    let content_w = w - 2.0 * m;
    let content_h = h - 2.0 * m;
    let n = rows.len() as f64;
    let widest = rows
        .iter()
        .map(|row| r.text_width(row, Some("Virtua Grotesk"), 1.0, &[]))
        .fold(0.0_f64, f64::max);
    let size = (content_w / widest).min(content_h / n);
    let cap = size * 0.72; // cap height, for vertical centering only

    // Left-aligned (ragged, like the reference), distributed down the height.
    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);
    let slot = content_h / n;
    for (i, row) in rows.iter().enumerate() {
        let baseline = (h - m) - slot * (i as f64 + 0.5) - cap / 2.0;
        ctx.font_size(size).text(row, m, baseline);
    }

    r.render_to_png(&ctx, "documentation/readme-images/specimen-regular.png").unwrap();
}
