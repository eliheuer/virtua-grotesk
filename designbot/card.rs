use designbot::prelude::*;

// Card dimensions for website: 3072x2048 (3:2 ratio, power-of-2 friendly)
const W: f64 = 3072.0;
const H: f64 = 2048.0;
const U: f64 = 64.0;        // Unit / cell size (power of 2)
const M: f64 = U * 2.0;     // Margin = 2 units = 128px
const COLS: usize = 48;     // W / U
const ROWS: usize = 32;     // H / U

// Toggle grid on/off
const SHOW_GRID: bool = false;

fn main() {
    let mut ctx = Canvas::new(W, H);
    let mut renderer = Renderer::new(W as u32, H as u32);
    ctx.background(Color::rgb(20, 20, 20));

    // Load the font
    renderer.load_font(
        "../fonts/VirtuaGrotesk-Regular.ttf"
    ).unwrap();

    // Draw grid: 48 cols x 32 rows of 64px squares, covering entire canvas
    if SHOW_GRID {
        ctx.stroke(Color::rgb(50, 50, 50)).stroke_width(1.0);
        ctx.no_fill();

        // Vertical lines
        for i in 0..=COLS {
            let x = i as f64 * U;
            ctx.line(x, 0.0, x, H);
        }

        // Horizontal lines
        for i in 0..=ROWS {
            let y = i as f64 * U;
            ctx.line(0.0, y, W, y);
        }
    }

    // Set font
    ctx.font("Virtua Grotesk");
    ctx.text_align(TextAlign::Left);

    // Uppercase and lowercase specimen
    ctx.fill(Color::rgb(200, 200, 200));
    ctx.font_size(290.0);

    let mut y = M + U * 3.0;

    // Uppercase
    ctx.text("ABCDEFGHIJKLM", M, y);
    y += U * 4.5;
    ctx.text("NOPQRSTUVWXYZ", M, y);
    y += U * 4.5;

    // Lowercase
    ctx.text("abcdefghijklm", M, y);
    y += U * 4.5;
    ctx.text("nopqrstuvwxyz", M, y);
    y += U * 4.5;

    // Numbers
    ctx.text("0123456789", M, y);

    renderer.render_to_png(&ctx, "card.png").unwrap();
}
