//! Run from the repository root with make twitter-animation.
use designbot::prelude::*;

fn main() {
    let mut renderer = Renderer::new(1920, 1080);
    renderer.load_font(find_up("fonts/variable/VirtuaGrotesk[GRAD,opsz,wght].ttf")).unwrap();
    let folder = find_up("output").join("twitter");
    std::fs::create_dir_all(&folder).unwrap();

    renderer.set_grain(0.0);
    for variant in ["clean", "grid", "crt"] {
        renderer.set_crt(variant == "crt");
        let mut page = Canvas::new(1920.0, 1080.0);
        for frame in 0..256 {
            if frame > 0 { page.new_page(); }
            page.frame_duration(1.0 / 30.0).background(Color::rgb(0, 0, 0));
            let ink = Color::rgb(196, 196, 196);
            page.no_stroke().fill(ink).font("Virtua Grotesk")
                .font_size(76.0).font_variation("opsz", 144.0);

            // At 80 px Arabic reaches 95 px above and 25 px below the baseline.
            // Every second Arabic baseline meets every third outer baseline.
            for (word, align, x, count, leading, offset) in [
                ("Virtua Grotesk", TextAlign::Left, 32.0, 13, 78.0, 0.0),
                ("ڤيرتوا غروتسك", TextAlign::Center, 960.0, 9, 117.0, 0.5),
                ("וירטואה גרוטסק", TextAlign::Right, 1888.0, 13, 78.0, 0.0),
            ] {
                for row in 0..count {
                    let depth = row as f64 * leading;
                    let phase = (frame as f64 / 256.0 - depth / 1080.0 + offset).rem_euclid(1.0);
                    let weight = lerp(100.0, 900.0, ease_in_out_sine(1.0 - (2.0 * phase - 1.0).abs()));
                    page.font_variation("wght", weight as f32);
                    page.text_align(align).text(word, x, 975.0 - depth);
                }
            }
            if variant == "grid" {
                page.no_fill().stroke(Color::rgb(112, 36, 40)).stroke_width(1.0);
                for x in (0..=1920).step_by(64) { page.line(x as f64, 0.0, x as f64, 1080.0); }
                for y in (28..=1052).step_by(64) { page.line(0.0, y as f64, 1920.0, y as f64); }
            }
        }
        let name = match variant {
            "grid" => "weight-axis-grid.mp4",
            "crt" => "weight-axis-crt.mp4",
            _ => "weight-axis.mp4",
        };
        renderer.render_to_mp4(&page, folder.join(name).to_str().unwrap()).unwrap();
    }
}
