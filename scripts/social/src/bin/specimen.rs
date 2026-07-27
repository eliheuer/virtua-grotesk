//! Foundry specimen card — the Font.Garden house style, theme-swappable.
//!
//! Ground/ink/furniture all come from the ACTIVE theme, so the exact same
//! layout renders as a dark card or a light card with only `--theme`. Quiet
//! monospace furniture in the four corners (⊞ wordmark + license up top,
//! family + repo below); the whole character set drawn as vectors from the
//! UFO fills the frame. Calm and type-first — the reference-set language.
//!
//!     cargo run --release --bin specimen                     # dark, default formats
//!     cargo run --release --bin specimen -- --theme light    # light
//!     cargo run --release --bin specimen -- --format square --scratch
//!
//! The 7-row full-charset layout suits the tall canvases (square, portrait);
//! landscape/vertical get their own compositions in a later bin.

use designbot_render::Renderer;
use kurbo::Affine;
use virtua_grotesk_social::*;

/// Specimen rows as glyph *names* (digits are `zero`..`nine` on disk).
/// Tall canvases get the 7-row full-charset block; wide landscape reflows the
/// charset into three long rows so it fills the width.
fn rows(format: Format) -> Vec<Vec<&'static str>> {
    let digits = vec![
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ];
    match format {
        Format::Landscape => vec![
            "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(' ').collect(),
            "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(' ').collect(),
            digits,
        ],
        _ => vec![
            "A B C D E F G H I J".split(' ').collect(),
            "K L M N O P Q R".split(' ').collect(),
            "S T U V W X Y Z".split(' ').collect(),
            digits,
            "a b c d e f g h i j".split(' ').collect(),
            "k l m n o p q r".split(' ').collect(),
            "s t u v w x y z".split(' ').collect(),
        ],
    }
}

fn main() {
    let cli = Cli::parse();
    let mono_path = inputs::geist_mono();
    let glyphs_dir = inputs::regular_ufo().join("glyphs");

    for format in cli.formats_or(&Format::all()) {
        // renderer must match the canvas size, so build one per format
        let mut renderer = Renderer::new(format.w() as u32, format.h() as u32);
        let mono = load_family(&mut renderer, mono_path.to_str().unwrap());
        let sheet = render(&renderer, &mono, &glyphs_dir, format);
        let out = cli.out("specimen", "regular", format);
        sheet.save(&out);
        println!("[{}] {}", cli.theme.name, out.display());
    }
}

fn render<'a>(renderer: &'a Renderer, mono: &str, glyphs_dir: &std::path::Path, format: Format) -> Sheet<'a> {
    let mut sheet = new_sheet(renderer, mono, format);
    sheet.ctx.background(role::canvas::background());
    let m = format.margin();
    let (w, h) = (format.w(), format.h());
    let furn = role::canvas::furniture();
    let footer_l = format!("{} Regular {}", inputs::PROJECT, inputs::VERSION);

    // --- corner furniture (y-up: header high, footer low) ---
    // Fit the mono size so a left + right label never collide on a narrow
    // canvas: each label must fit within its half, minus a center gutter.
    let gutter = 48.0;
    let max_half = (w - 2.0 * m - gutter) / 2.0;
    let base = role::text::CAPTION;
    let mark_w = base * 0.86 + 16.0; // ⊞ mark + gap ahead of the wordmark
    let widest = [
        mark_w + sheet.mono_width(inputs::FOUNDRY, base),
        sheet.mono_width(inputs::LICENSE, base),
        sheet.mono_width(&footer_l, base),
        sheet.mono_width(inputs::REPO, base),
    ]
    .into_iter()
    .fold(0.0_f64, f64::max);
    let cap_size = base * (max_half / widest).min(1.0);

    let head_y = h - m - 6.0;
    let foot_y = m - 6.0;
    let mk = cap_size * 0.86;
    sheet.ctx.no_fill().stroke(furn).stroke_width(line::THIN);
    sheet.ctx.rect(m, head_y, mk, mk);
    sheet.ctx.line(m + mk / 2.0, head_y, m + mk / 2.0, head_y + mk);
    sheet.ctx.line(m, head_y + mk / 2.0, m + mk, head_y + mk / 2.0);
    sheet.label_weighted(inputs::FOUNDRY, m + mk + 16.0, head_y, cap_size, furn, -1, 400.0);
    sheet.label_weighted(inputs::LICENSE, w - m, head_y, cap_size, furn, 1, 400.0);
    sheet.label_weighted(&footer_l, m, foot_y, cap_size, furn, -1, 400.0);
    sheet.label_weighted(inputs::REPO, w - m, foot_y, cap_size, furn, 1, 400.0);

    // thin rules under header / over footer
    let rule_top = head_y - 34.0;
    let rule_bot = foot_y + cap_size + 22.0;
    sheet.ctx.no_fill().stroke(role::canvas::rule()).stroke_width(line::FINE);
    sheet.ctx.line(m, rule_top, w - m, rule_top);
    sheet.ctx.line(m, rule_bot, w - m, rule_bot);

    // --- specimen block: left-aligned rows, fit to whichever bind is tighter ---
    let content_w = w - 2.0 * m;
    let band_top = rule_top - 60.0; // high y
    let band_bot = rule_bot + 60.0; // low y
    let band_h = band_top - band_bot;
    let rows = rows(format);
    let n = rows.len() as f64;
    let pitch = band_h / n;

    let cap = bbox(&load_outline(glyphs_dir, "H")).height();
    let mut adv: Vec<f64> = Vec::new();
    for row in &rows {
        adv.push(row.iter().map(|nme| load_outline(glyphs_dir, nme).width).sum());
    }
    let widest = adv.iter().cloned().fold(0.0, f64::max);
    let scale_w = content_w / widest;
    let scale_h = 0.62 * pitch / cap;
    let scale = scale_w.min(scale_h);

    let ink = role::canvas::ink();
    for (i, row) in rows.iter().enumerate() {
        let slot_bottom = band_top - (i as f64 + 1.0) * pitch;
        let baseline = slot_bottom + (pitch - cap * scale) / 2.0;
        let mut pen = 0.0;
        for name in row {
            let o = load_outline(glyphs_dir, name);
            let place = Affine::new([scale, 0.0, 0.0, scale, m + pen * scale, baseline]);
            sheet.ctx.fill(ink).no_stroke();
            sheet.ctx.draw_path(place * o.path.clone());
            pen += o.width;
        }
    }
    sheet
}
