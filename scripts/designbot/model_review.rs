// "held-out review" — blog/social image: for each held-out glyph, the human
// Regular (input), the model's generated Bold (output), and the human Bold
// (ground truth). The a column has NO human bold — the model's draft is the
// only bold a that exists. House poster format (see social_images.rs).
//
//   designbot --render scripts/designbot/model_review.rs \
//     --output documentation/assets/social/square/model-review.png -- \
//     square sources/VirtuaGrotesk-Regular.ufo sources/VirtuaGrotesk-Bold.ufo \
//     ../font-garden-lab/runs/v07/pred.ufo
use designbot::norad;
use designbot::prelude::*;
use designbot::kurbo::{Affine, BezPath};

const VF_PATH: &str = "fonts/variable/VirtuaGrotesk[wght].ttf";
const VG_FAMILY: &str = "Virtua Grotesk";
const LOGO: char = '\u{E008}';
const GLYPHS: &[&str] = &["K", "E", "M", "n", "b", "c", "a"];

fn col(r: f64, g: f64, b: f64) -> Color {
    Color::rgb((r * 255.0).round() as u8, (g * 255.0).round() as u8, (b * 255.0).round() as u8)
}
fn paper() -> Color { col(0.055, 0.055, 0.055) }
fn white() -> Color { col(0.96, 0.96, 0.94) }
fn muted() -> Color { col(0.56, 0.56, 0.53) }
fn faint() -> Color { col(0.36, 0.36, 0.34) }
fn red() -> Color { col(1.0, 0.29, 0.24) }

fn ufo_affine(t: &norad::AffineTransform) -> Affine {
    Affine::new([t.x_scale, t.xy_scale, t.yx_scale, t.y_scale, t.x_offset, t.y_offset])
}

fn glyph_path(font: &norad::Font, name: &str, depth: u8) -> BezPath {
    if depth > 4 { std::process::exit(1); }
    let glyph = font.get_glyph(name).unwrap_or_else(|| {
        eprintln!("glyph {name:?} not found"); std::process::exit(1);
    });
    let mut path = BezPath::new();
    for contour in &glyph.contours {
        let pts = &contour.points;
        let Some(start) = pts.iter().position(|p| !matches!(p.typ, norad::PointType::OffCurve)) else { continue };
        let n = pts.len();
        let first = &pts[start];
        path.move_to((first.x, first.y));
        let mut pending: Vec<(f64, f64)> = Vec::new();
        for i in 1..=n {
            let p = &pts[(start + i) % n];
            match p.typ {
                norad::PointType::OffCurve => pending.push((p.x, p.y)),
                norad::PointType::Line | norad::PointType::Move => { path.line_to((p.x, p.y)); pending.clear(); }
                _ => match pending.len() {
                    2 => { path.curve_to(pending[0], pending[1], (p.x, p.y)); pending.clear(); }
                    0 => path.line_to((p.x, p.y)),
                    _ => std::process::exit(1),
                },
            }
        }
        path.close_path();
    }
    for component in &glyph.components {
        let mut sub = glyph_path(font, component.base.as_str(), depth + 1);
        sub.apply_affine(ufo_affine(&component.transform));
        path.extend(sub.elements().iter().copied());
    }
    path
}

fn advance(font: &norad::Font, name: &str) -> f64 {
    font.get_glyph(name).map(|g| g.width).unwrap_or(600.0)
}

fn vg(ctx: &mut Canvas, txt: &str, x: f64, baseline: f64, size: f64, color: Color, align: TextAlign) {
    ctx.font(VG_FAMILY).clear_font_variations().font_variation("wght", 500.0f32)
        .font_size(size).fill(color).text_align(align).text(txt, x, baseline);
    ctx.text_align(TextAlign::Left);
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let fmt = args.get(0).map(String::as_str).unwrap_or("square");
    let reg = norad::Font::load(args.get(1).map(String::as_str).unwrap_or("sources/VirtuaGrotesk-Regular.ufo")).unwrap();
    let bold = norad::Font::load(args.get(2).map(String::as_str).unwrap_or("sources/VirtuaGrotesk-Bold.ufo")).unwrap();
    let pred = norad::Font::load(args.get(3).map(String::as_str).unwrap_or("../font-garden-lab/runs/v07/pred.ufo")).unwrap();

    let (w, h): (f64, f64) = match fmt { "landscape" => (2048.0, 1152.0), _ => (2048.0, 2048.0) };
    let mut renderer = Renderer::new(w as u32, h as u32);
    renderer.load_font(VF_PATH).expect("build fonts first");
    let mut ctx = Canvas::new(w, h);
    ctx.background(paper());
    let margin = w * 0.0625;

    // corner captions
    let cap = w * 0.017;
    vg(&mut ctx, "Font.Garden", margin, h - margin * 0.72, cap, muted(), TextAlign::Left);
    vg(&mut ctx, &LOGO.to_string(), w - margin, h - margin * 0.72, cap, muted(), TextAlign::Right);
    vg(&mut ctx, "held-out glyphs \u{2014} the model never saw these bolds", margin, margin * 0.55, cap, muted(), TextAlign::Left);
    vg(&mut ctx, "virtua grotesk \u{00B7} model v0.7", w - margin, margin * 0.55, cap, muted(), TextAlign::Right);

    // grid: 3 rows x 7 columns of glyphs, row labels at left
    let rows: [(&str, &norad::Font, Color); 3] = [
        ("input \u{2014} human regular", &reg, white()),
        ("output \u{2014} model bold", &pred, red()),
        ("reference \u{2014} human bold", &bold, faint()),
    ];
    let grid_top = h - margin * 2.9;
    let grid_bottom = margin * 2.0;
    let row_h = (grid_top - grid_bottom) / 3.0;
    let cell_w = (w - margin * 2.0) / GLYPHS.len() as f64;
    let scale = (cell_w / 1150.0).min(row_h / 1500.0);
    let label_size = w * 0.015;

    for (ri, (label, font, color)) in rows.iter().enumerate() {
        let base = grid_top - row_h * (ri as f64 + 1.0) + row_h * 0.28;
        vg(&mut ctx, label, margin, base + row_h * 0.62, label_size,
           if ri == 1 { red() } else { muted() }, TextAlign::Left);
        for (ci, name) in GLYPHS.iter().enumerate() {
            if ri == 2 && *name == "a" {
                vg(&mut ctx, "\u{2014}", margin + cell_w * (ci as f64 + 0.5), base + 300.0 * scale,
                   label_size, faint(), TextAlign::Center);
                vg(&mut ctx, "never drawn", margin + cell_w * (ci as f64 + 0.5), base - 40.0 * scale,
                   label_size * 0.8, faint(), TextAlign::Center);
                continue;
            }
            let mut path = glyph_path(font, name, 0);
            let adv = advance(font, name);
            let x0 = margin + cell_w * (ci as f64 + 0.5) - adv * scale / 2.0;
            path.apply_affine(Affine::translate((x0 / scale, base / scale)));
            path.apply_affine(Affine::scale(scale));
            ctx.fill(*color);
            ctx.draw_path(path);
        }
    }
    renderer.render_to_png(&ctx, "out.png").unwrap();
}
