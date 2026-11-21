//! Run from the repository root with make twitter-animation.
use designbot::prelude::*;

fn main() {
    let mut renderer = Renderer::new(1920, 1080);
    renderer.load_font(find_up("fonts/variable/VirtuaGrotesk[GRAD,opsz,wght].ttf")).unwrap();
    let folder = find_up("output").join("twitter");
    std::fs::create_dir_all(&folder).unwrap();

    for grid in [false, true] {
        let mut page = Canvas::new(1920.0, 1080.0);
        for frame in 0..256 {
            if frame > 0 { page.new_page(); }
            page.frame_duration(1.0 / 30.0).background(Color::rgb(32, 32, 32));
            let ink = Color::rgb(224, 224, 224);
            page.no_stroke().fill(ink).font("Virtua Grotesk")
                .font_size(80.0).font_variation("opsz", 144.0);

            // Ink extents at 80 px, measured at the four weight masters.
            for (word, align, x, count, ascents, descents) in [
                ("Virtua Grotesk", TextAlign::Left, 16.0, 14, [61.,61.,62.,61.], [2.,2.,2.,2.]),
                ("ڤيرتوا غروتسك", TextAlign::Center, 960.0, 9, [79.,80.,90.,95.], [20.,21.,24.,25.]),
                ("וירטואה גרוטסק", TextAlign::Right, 1904.0, 13, [52.;4], [14.,15.,15.,15.]),
            ] {
                let mut rows = Vec::with_capacity(count);
                let mut total_ink = 0.0;
                for row in 0..count {
                    let phase = (frame as f64 / 256.0 - row as f64 / count as f64).rem_euclid(1.0);
                    let weight = lerp(100.0, 900.0, ease_in_out_sine(1.0 - (2.0 * phase - 1.0).abs()));
                    let masters = [100., 400., 700., 900.];
                    let i = if weight <= 400. { 0 } else if weight <= 700. { 1 } else { 2 };
                    let t = (weight - masters[i]) / (masters[i+1] - masters[i]);
                    let ascent = lerp(ascents[i], ascents[i+1], t);
                    let descent = lerp(descents[i], descents[i+1], t);
                    total_ink += ascent + descent;
                    rows.push((weight, ascent, descent));
                }
                let gap = (1080.0 - 32.0 - total_ink) / (count - 1) as f64;
                let mut top = 1080.0 - 16.0;
                for (weight, ascent, descent) in rows {
                    page.font_variation("wght", weight as f32);
                    page.text_align(align).text(word, x, top - ascent);
                    top -= ascent + descent + gap;
                }
            }
            if grid {
                page.no_fill().stroke(Color::rgb(100, 80, 80)).stroke_width(1.0);
                for x in (0..=1920).step_by(64) { page.line(x as f64, 0.0, x as f64, 1080.0); }
                for y in (28..=1052).step_by(64) { page.line(0.0, y as f64, 1920.0, y as f64); }
            }
        }
        let name = if grid { "weight-axis-grid.mp4" } else { "weight-axis.mp4" };
        renderer.render_to_mp4(&page, folder.join(name).to_str().unwrap()).unwrap();
    }
}
