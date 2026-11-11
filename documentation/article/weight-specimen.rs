//! Virtua Grotesk: the image for the Google Fonts About text.
//!
//! Renders the variable font at four weights as outlined SVG. Run it from the
//! repository root after `make build`:
//!
//!   designbot documentation/article/weight-specimen.rs \
//!       --output documentation/article/weight-specimen.svg
//!
//! Coordinates are y-up, with the origin at the bottom left.

use designbot::prelude::*;

fn main() {
    let (w, h) = (1600.0, 900.0);
    let ground = Color::rgb(0xee, 0xea, 0xe1);
    let ink = Color::rgb(0x20, 0x25, 0x1f);
    let label = Color::rgb(0x52, 0x63, 0x4a);
    let rule = Color::rgb(0xb4, 0xb9, 0xaa);

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/variable/VirtuaGrotesk[wght].ttf")).expect("Virtua Grotesk VF");
    ctx.background(ground);

    let line = |ctx: &mut Canvas, text: &str, x: f64, y: f64, size: f64, wght: f32, color: Color| {
        ctx.fill(color)
            .font("Virtua Grotesk")
            .font_size(size)
            .clear_font_variations()
            .font_variation("wght", wght);
        ctx.text(text, x, h - y);
    };

    line(&mut ctx, "VIRTUA GROTESK", 80.0, 105.0, 28.0, 600.0, ink);
    line(&mut ctx, "Form follows rhythm", 80.0, 264.0, 128.0, 400.0, ink);
    for (i, wght) in [400.0_f32, 500.0, 600.0, 700.0].iter().enumerate() {
        let y = 405.0 + i as f64 * 126.0;
        ctx.fill(rule).rect(80.0, h - (y - 83.0), 1440.0, 1.0);
        line(&mut ctx, &format!("{}", *wght as i32), 80.0, y, 28.0, 400.0, label);
        line(&mut ctx, "Aa Bb Gg 0123456789", 250.0, y, 80.0, *wght, ink);
    }

    r.render_to_svg(&ctx, "documentation/article/weight-specimen.svg").unwrap();
}
