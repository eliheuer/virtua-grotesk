//! Fixed-em comparison diagnostic. Run through render-detail.py.
use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;
const W: u32 = 1600;
const WGHT: u32 = u32::from_be_bytes(*b"wght");
fn main() {
    let a: Vec<String> = env::args().collect();
    assert!(a.len() >= 10 && (a.len() - 6) % 4 == 0, "weight size sample title label-font followed by path/family/label/weight groups");
    let count = (a.len() - 6) / 4;
    let height = 208 + count.div_ceil(2) as u32 * 304;
    let weight: f32 = a[1].parse().unwrap();
    let size: f64 = a[2].parse().unwrap();
    let ink = Color { r: 222, g: 222, b: 222, a: 255 };
    let mut renderer = Renderer::new(W, height);
    renderer.load_font(&a[5]).expect("Working label font");
    let mut page = Canvas::new(W as f64, height as f64);
    page.background(Color { r: 24, g: 24, b: 24, a: 255 });
    page.fill(ink).font("Virtua Grotesk").font_size(32.0)
        .font_variation("wght", 400.0).text(&a[4], 64.0, height as f64 - 70.0);
    page.font_size(22.0).text(&format!("Weight {weight:.0} · {size:.0} px/em · Working drawings"), 64.0, height as f64 - 110.0);
    for i in 0..count {
        let actual_weight: f32 = a[9 + i*4].parse().unwrap();
        let x = 64.0 + (i % 2) as f64 * 752.0;
        let y = 156.0 + (i / 2) as f64 * 304.0;
        let width = 720.0;
        page.fill(ink).rect(x, height as f64 - y, width, 2.0);
        page.font_size(24.0).text(&a[8 + i*4], x, height as f64 - y - 38.0);
        // Isolate each snapshot: identical family names must never resolve to another file.
        let mut r = Renderer::new(W, height);
        r.load_font(&a[6 + i*4]).expect("Explicit sample font");
        let advance = r.text_width(&a[3], Some(&a[7 + i*4]), size, &[(WGHT, actual_weight)]);
        assert!(advance <= width - 48.0, "Sample too wide; reduce the shared size");
        let mut c = Canvas::new(W as f64, height as f64);
        c.background(Color { r: 0, g: 0, b: 0, a: 0 });
        c.fill(ink).font(&a[7 + i*4]).font_variation("wght", actual_weight)
            .font_size(size).text(&a[3], x + 24.0, height as f64 - y - 196.0);
        let mut pixels = r.render_frames(&c).remove(0).0;
        let mut visible = 0;
        for (j, p) in pixels.chunks_exact_mut(4).enumerate() {
            if p[3] != 0 {
                visible += 1;
                let px = (j % W as usize) as f64;
                let py = (j / W as usize) as f64;
                assert!(px >= x && px < x+width && py > y+54.0 && py < y+280.0,
                    "Sample ink leaves panel {i}: ({px}, {py}), expected x={x}, y={y}; adjust shared size/layout");
            }
            // Backend pixels are premultiplied; image_rgba expects straight alpha.
            p[0] = ink.r; p[1] = ink.g; p[2] = ink.b;
        }
        assert!(visible > 0, "Empty sample render");
        page.image_rgba(pixels, W, height, 0.0, 0.0, 1.0);
    }
    renderer.render_to_png(&page, "out.png").expect("Raw diagnostic PNG");
}
