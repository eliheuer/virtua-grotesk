//! Font.Garden — seven repeating rows in Virtua Grotesk Regular.
//!
//! 2048 px square: light gray type on a black background with generous margins.
//! Run from the repository root after `make build`:
//!   designbot --raw documentation/social-assets/posts/font-garden.rs
//! Grid review:
//!   GRID_VIEW=1 designbot --raw documentation/social-assets/posts/font-garden.rs \
//!     --output /tmp/font-garden-grid.png

use designbot::prelude::*;

const SIDE: f64 = 2048.0;
const FAMILY: &str = "Virtua Grotesk";
const TEXT: &str = "Font.Garden";
const ROWS: usize = 7;

fn main() {
    let margin = SIDE / 16.0;
    let unit = margin / 2.0;
    let inset = margin + unit;
    let ink_width = SIDE - 2.0 * inset;
    // A quarter-unit subdivision keeps the dense rows close to a square.
    let leading = 3.75 * unit;

    let mut canvas = Canvas::new(SIDE, SIDE);
    let mut renderer = Renderer::new(SIDE as u32, SIDE as u32);
    renderer.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf"))
        .expect("build Virtua Grotesk Regular first");

    canvas.background(Color::rgb(0, 0, 0));
    canvas.no_stroke();

    // Measured in the built Regular font with fontTools: 1024 UPM,
    // F left bearing 80, final n right bearing 72, ink y = -16..784.
    // Remove the outside bearings when fitting; preserve natural shaping.
    let upm = 1024.0;
    let left_bearing = 80.0;
    let right_bearing = 72.0;
    let width_at_upm = renderer.text_width(TEXT, Some(FAMILY), upm, &[]);
    let size = ink_width * upm / (width_at_upm - left_bearing - right_bearing);
    let x = inset - left_bearing * size / upm;
    let ink_midpoint = (-16.0 + 784.0) / 2.0 * size / upm;
    let first_baseline = SIDE / 2.0 + (ROWS - 1) as f64 * leading / 2.0 - ink_midpoint;

    canvas.fill(Color::rgb(220, 220, 220)).font(FAMILY).font_size(size);
    for row in 0..ROWS {
        canvas.text(TEXT, x, first_baseline - row as f64 * leading);
    }

    if std::env::var("GRID_VIEW").as_deref() == Ok("1") {
        Grid::upm(upm).structural(unit).margin(inset)
            .color(Color::rgba(255, 74, 61, 100)).draw(&mut canvas, SIDE, SIDE);
    }

    renderer.render_to_png(&canvas, "documentation/social-assets/posts/font-garden.png")
        .expect("render Font.Garden");
}
