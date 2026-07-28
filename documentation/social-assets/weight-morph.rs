//! Virtua Grotesk — weight morph animation (Regular ⇄ Bold).
//!
//! A seamless loop breathing the variable font's wght axis (400 → 700 → 400)
//! with an eased ping-pong. Two colors only (theme ground + ink).
//!
//!   designbot --render documentation/social-assets/weight-morph.rs \
//!             --output documentation/social-assets/weight-morph.gif
//!   # or .mp4 (needs ffmpeg):
//!   designbot --render documentation/social-assets/weight-morph.rs \
//!             --output documentation/social-assets/weight-morph.mp4
//!
//! Every new_page() is one frame; frame_duration sets the per-frame delay.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark();
    let (w, h) = (1024.0, 1024.0); // square, power of two
    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/variable/VirtuaGrotesk[wght].ttf")).expect("Virtua Grotesk VF");

    let frames = 60; // 2s loop at 30fps
    let size = 560.0;
    ctx.frame_duration(1.0 / 30.0);

    for i in 0..frames {
        if i > 0 {
            ctx.new_page();
        }
        ctx.background(t.ground);

        // wght 400 → 700 → 400 over the loop, eased at the turns.
        let phase = i as f64 / frames as f64;
        let wght = lerp(400.0, 700.0, ease_in_out_sine(ping_pong(phase))) as f32;

        ctx.fill(t.ink)
            .font("Virtua Grotesk")
            .font_size(size)
            .clear_font_variations()
            .font_variation("wght", wght)
            .text_align(TextAlign::Center);
        ctx.text("Aa", w / 2.0, h / 2.0 - size * 0.36); // optically centered
    }

    r.render_to_gif(&ctx, "documentation/social-assets/weight-morph.gif").unwrap();
    println!("{} frames", ctx.page_count());
}
