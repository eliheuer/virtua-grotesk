// Shaped-Arabic proof sheet for the completion pass.
//
// Renders real Arabic words from the BUILT variable font, so what you see
// is what shaping actually produces (positional forms, mark attachment,
// ligatures) rather than what the sources look like glyph by glyph.
//
// Usage (from the repo root):
//   designbot --render harness/designbot/arabic_words.rs \
//       --output ~/Temp/arabic-words.png
//
// Dark-mode house style: dark gray ground, light gray ink.

use designbot::prelude::*;

const W: f64 = 1600.0;
const ROW: f64 = 150.0;
const MARGIN: f64 = 80.0;

const WORDS: [(&str, &str); 12] = [
    ("كتاب", "kitab / book"),
    ("سلام", "salaam / peace"),
    ("العربية", "al-arabiyya"),
    ("محمد", "muhammad"),
    ("جميل", "jamil / beautiful"),
    ("شمس", "shams / sun"),
    ("قمر", "qamar / moon"),
    ("طريق", "tariq / road"),
    ("مكتبة", "maktaba / library"),
    ("خط عربي", "khatt arabi"),
    ("٠١٢٣٤٥٦٧٨٩", "arabic-indic digits"),
    ("بَ بِ بُ بّ بْ", "harakat on beh"),
];

fn main() {
    let h = MARGIN * 2.0 + ROW * WORDS.len() as f64;
    let mut ctx = Canvas::new(W, h);
    ctx.background(Color::rgb(28, 28, 30));

    let mut renderer = Renderer::new(W as u32, h as u32);
    if let Err(e) = renderer.load_font("fonts/variable/VirtuaGrotesk[wght].ttf")
    {
        eprintln!("could not load the built variable font: {e}");
        eprintln!("run `make build` first");
        std::process::exit(1);
    }
    ctx.font("Virtua Grotesk");

    for (i, (word, gloss)) in WORDS.iter().enumerate() {
        let y = h - MARGIN - ROW * (i as f64 + 1.0) + 40.0;

        // gloss on the left, small and dim
        ctx.fill(Color::rgb(120, 120, 126));
        ctx.font_size(24.0);
        ctx.text(gloss, MARGIN, y);

        // the Arabic, right-aligned so the RTL text reads off the margin
        ctx.fill(Color::rgb(226, 226, 230));
        ctx.font_size(96.0);
        ctx.text_align(TextAlign::Right);
        ctx.text(word, W - MARGIN, y);
        ctx.text_align(TextAlign::Left);
    }

    renderer.render_to_png(&ctx, "arabic_words.png").unwrap();
}
