use designbot::prelude::*;

// Constants
const W: f64 = 2048.0;
const H: f64 = 2048.0;
const M: f64 = 128.0;   // Margin
const U: f64 = 64.0;    // Unit
const G: f64 = 32.0;    // Number of grid cells

fn main() {
    // Create canvas, renderer, and bg color
    let mut ctx = Canvas::new(W, H);
    let mut renderer = Renderer::new(W as u32, H as u32);
    ctx.background(Color::rgb(20, 20, 20));

    // Load the font
    renderer.load_font(
        "../fonts/VirtuaGrotesk-Regular.ttf"
    ).unwrap();

    // Calculate grid dimensions
    let grid_width = W - (M * 2.0);
    let grid_height = H - (M * 2.0);
    let cell_width = grid_width / G;
    let cell_height = grid_height / G;

    // Set colors
    let white = Color::white();
    let light_gray = Color::rgb(50, 50, 50);

    // Add Auxiliry text bars
    //ctx.fill(Color::rgb(150, 150, 150));
    //ctx.rect(M, M, W-(M*2.0), cell_height*2.0);
    //ctx.rect(M, H-(M*1.875), H-(M*2.0), cell_height*2.0);

    // Draw grid vertical lines
    ctx.stroke(light_gray).stroke_width(2.0);
    for i in 0..=G as usize {
        let x = M + (i as f64 * cell_width);
        //ctx.line(x, M, x, H - M);
    }

    // Draw grid horizontal lines
    for i in 0..=G as usize {
        let y = M + (i as f64 * cell_height);
        //ctx.line(M, y, W - M, y);
    }

    // Set font
    ctx.font("Virtua Grotesk");
    ctx.fill(Color::rgb(175, 175, 175));

    // Auxiliary info
    ctx.font_size(64.0+8.0);
    // Top
    ctx.text("\u{E008} Font.Garden/virtua", M, M*0.95);
    ctx.text_align(TextAlign::Right);
    ctx.text("Open Font License OFL v1.1", W-M, M*0.95);
    // Bottom
    ctx.text_align(TextAlign::Left);
    ctx.text("Virtua Grotesk Regular v0.1", M, H-(M*1.5));
    ctx.text_align(TextAlign::Right);
    ctx.text("$elih on Zora: 0x7ca2", W-M, H-(M*1.5));
    // 0x7ca26c4663860590c29a63c20cfc465b2dcd246b

    // Character sets
    let mut y_pos = H - M - (U * 25.75);
    ctx.text_align(TextAlign::Left);
    ctx.font_size(256.0-8.0);

    // Uppercase letters - line 1
    ctx.fill(Color::rgb(175, 175, 175));
    ctx.text("ABCDEFGHIJ", M-6.0, y_pos);
    y_pos += U * 3.30;

    // Uppercase letters - line 2
    ctx.text("KLMNOPQR", M-20.0, y_pos);
    y_pos += U * 3.30;

    // Uppercase letters - line 3
    ctx.text("STUVWXYZ", M-8.0, y_pos);
    y_pos += U * 3.30;

    // Numbers
    ctx.text("0123456789", M-24.0, y_pos);
    y_pos += U * 3.30;

    // Lowercase letters - line 1
    ctx.text("abcdefghij", M-8.0, y_pos);
    y_pos += U * 3.30;

    // Lowercase letters - line 2
    ctx.text("klmnopqr", M-24.0, y_pos);
    y_pos += U * 3.30;

    // Lowercase letters - line 3
    ctx.text("stuvwxyz", M-16.0, y_pos);

    // Arabic sample text
    //ctx.fill(Color::rgb(255, 255, 255));
    //ctx.text("أشهد يا إلهي بأنك خلقتني", M, (M*4.0) - 16.0);

    // Render to PNG (output path handled by designbot CLI)
    renderer.render_to_png(&ctx, "output.png").unwrap();
}
