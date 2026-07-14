// "The model drew the Bold" — demo image for the Virtua Grotesk blog post
// and social media, in the house poster format (see social_images.rs).
//
// The Bold `a` shown is the raw output of the v0.7 GlyphLM (trained on the
// system-pass corpus, 39 Regular->Bold pairs): the model saw the human
// Regular a and predicted every Bold point. It never saw a Bold a.
//
//   designbot --render scripts/designbot/model_demo.rs \
//     --output documentation/assets/social/square/model-bolden-a.png \
//     -- square:bolden-a
//
//   formats  square (2048x2048)  landscape (2048x1152)
use designbot::prelude::*;

const VF_PATH: &str = "fonts/variable/VirtuaGrotesk[wght].ttf";
const VG_FAMILY: &str = "Virtua Grotesk";
const LOGO: char = '\u{E008}';

fn col(r: f64, g: f64, b: f64) -> Color {
    Color::rgb(
        (r * 255.0).round() as u8,
        (g * 255.0).round() as u8,
        (b * 255.0).round() as u8,
    )
}
fn paper() -> Color { col(0.055, 0.055, 0.055) }
fn white() -> Color { col(0.96, 0.96, 0.94) }
fn muted() -> Color { col(0.56, 0.56, 0.53) }
fn rule() -> Color { col(0.30, 0.30, 0.28) }
fn red() -> Color { col(1.0, 0.29, 0.24) }

fn vg(ctx: &mut Canvas, txt: &str, x: f64, baseline: f64, wght: f32,
      size: f64, color: Color, align: TextAlign) {
    ctx.font(VG_FAMILY)
        .clear_font_variations()
        .font_variation("wght", wght)
        .font_size(size)
        .fill(color)
        .text_align(align)
        .text(txt, x, baseline);
    ctx.text_align(TextAlign::Left);
}

fn main() {
    let arg = std::env::args().skip(1).next().unwrap_or_else(|| "square:bolden-a".to_string());
    let (fmt, _image) = arg.split_once(':').unwrap_or(("square", "bolden-a"));
    let (w, h): (f64, f64) = match fmt {
        "landscape" => (2048.0, 1152.0),
        _ => (2048.0, 2048.0),
    };
    let mut renderer = Renderer::new(w as u32, h as u32);
    renderer.load_font(VF_PATH).expect("run ./build.sh first");

    let mut ctx = Canvas::new(w, h);
    ctx.background(paper());
    let margin = w * 0.0625; // house grid margin

    // corner captions (poster idiom)
    let cap = w * 0.017;
    vg(&mut ctx, "Font.Garden", margin, h - margin * 0.72, 500.0f32, cap, muted(), TextAlign::Left);
    vg(&mut ctx, &LOGO.to_string(), w - margin, h - margin * 0.72, 500.0f32, cap, muted(), TextAlign::Right);
    vg(&mut ctx, "a neural net drew the bold", margin, margin * 0.55, 500.0f32, cap, muted(), TextAlign::Left);
    vg(&mut ctx, "virtua grotesk \u{00B7} virtua v0.1", w - margin, margin * 0.55, 500.0f32, cap, muted(), TextAlign::Right);

    // the two glyphs on a shared baseline
    let size = h * 0.52;
    let baseline = h * 0.30;
    let lx = w * 0.28;
    let rx = w * 0.72;
    vg(&mut ctx, "a", lx, baseline, 400.0f32, size, white(), TextAlign::Center);
    vg(&mut ctx, "a", rx, baseline, 700.0f32, size, red(), TextAlign::Center);

    // arrow between them on the optical mid-height
    let ay = baseline + size * 0.21;
    let ax0 = w * 0.455;
    let ax1 = w * 0.545;
    ctx.stroke(rule()).stroke_width(w * 0.004)
        .line(ax0, ay, ax1, ay)
        .line(ax1, ay, ax1 - w * 0.018, ay + w * 0.014)
        .line(ax1, ay, ax1 - w * 0.018, ay - w * 0.014);

    // labels under each glyph
    let ly = baseline - h * 0.10;
    let lab = w * 0.022;
    vg(&mut ctx, "regular \u{2014} drawn by hand", lx, ly, 500.0f32, lab, muted(), TextAlign::Center);
    vg(&mut ctx, "bold \u{2014} drawn by the model", rx, ly, 500.0f32, lab, red(), TextAlign::Center);

    renderer.render_to_png(&ctx, "out.png");
}
