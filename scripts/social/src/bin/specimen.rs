//! Foundry specimen — a hand-editable DrawBot-style script.
//!
//! This reads top-to-bottom like a DrawBot sketch: set numbers, draw. There is
//! NO auto-fit magic — every size and position is an explicit number you edit
//! and re-render. Glyphs are placed with the DrawBot idiom `save · translate ·
//! scale · draw_path`. Colors come from the active `--theme`.
//!
//!     cargo run --release --bin specimen -- --theme dark
//!     cargo run --release --bin specimen -- --theme light --format square
//!
//! ┌─ WHAT TO EDIT ────────────────────────────────────────────────────────┐
//! │  layout()  — per-format numbers: margin, glyph size, leading, furniture │
//! │  rows()    — which glyphs appear, row by row (glyph NAMES)              │
//! │  the four `label(...)` calls below — the corner text                    │
//! │  colors    — in theme.rs (or pass --theme)                             │
//! └────────────────────────────────────────────────────────────────────────┘

use designbot::prelude::Color;
use designbot_render::Renderer;
use std::path::Path;
use virtua_grotesk_social::*;

const UPM: f64 = 1024.0; // Virtua Grotesk units per em

/// Per-format layout knobs. `size` is the glyph em-size in px (DrawBot's
/// fontSize); `lead` is baseline-to-baseline; `top` is the gap from the top
/// hairline down to the first row's baseline; `furn` is the mono label size.
struct Layout {
    margin: f64,
    furn: f64,
    size: f64,
    lead: f64,
    top: f64,
}

// EDIT HERE — tune each canvas by hand.
fn layout(format: Format) -> Layout {
    match format {
        Format::Square => Layout { margin: 180.0, furn: 32.0, size: 210.0, lead: 214.0, top: 150.0 },
        Format::Portrait => Layout { margin: 96.0, furn: 22.0, size: 150.0, lead: 150.0, top: 70.0 },
        Format::Landscape => Layout { margin: 120.0, furn: 30.0, size: 145.0, lead: 340.0, top: 150.0 },
        Format::Vertical => Layout { margin: 96.0, furn: 22.0, size: 150.0, lead: 232.0, top: 110.0 },
    }
}

// EDIT HERE — the specimen content, row by row, as glyph NAMES
// (digits are spelled: zero one two … nine).
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
    let glyphs = inputs::regular_ufo().join("glyphs");

    for format in cli.formats_or(&Format::all()) {
        let mut renderer = Renderer::new(format.w() as u32, format.h() as u32);
        let mono = load_family(&mut renderer, mono_path.to_str().unwrap());
        let sheet = draw(&renderer, &mono, &glyphs, format);
        let out = cli.out("specimen", "regular", format);
        sheet.save(&out);
        println!("[{}] {}", cli.theme.name, out.display());
    }
}

/// Draw one glyph outline scaled so 1 em = `size` px (DrawBot fontSize) at left
/// edge `x`, baseline `y`. Returns the glyph's advance in px so the caller can
/// step to the next letter.
fn glyph(sheet: &mut Sheet, dir: &Path, name: &str, x: f64, y: f64, size: f64, fill: Color) -> f64 {
    let o = load_outline(dir, name);
    let s = size / UPM;
    sheet.ctx.save();
    sheet.ctx.translate(x, y);
    sheet.ctx.scale(s);
    sheet.ctx.fill(fill).no_stroke();
    sheet.ctx.draw_path(o.path.clone());
    sheet.ctx.restore();
    o.width * s
}

fn draw<'a>(renderer: &'a Renderer, mono: &str, glyphs: &Path, format: Format) -> Sheet<'a> {
    let l = layout(format);
    let (w, h) = (format.w(), format.h());
    let m = l.margin;

    // colors (from the active theme)
    let ground = role::canvas::background();
    let ink = role::canvas::ink();
    let furn = role::canvas::furniture();
    let rule = role::canvas::rule();

    let mut sheet = new_sheet(renderer, mono, format);
    sheet.ctx.background(ground);

    // --- corner furniture (y-up: top is high, bottom is low) ---
    let head_y = h - m; // header label baseline
    let foot_y = m; // footer label baseline
    let footer_l = format!("{} Regular {}", inputs::PROJECT, inputs::VERSION);

    // ⊞ foundry mark, then the wordmark, top-left
    let mk = l.furn * 0.86;
    sheet.ctx.no_fill().stroke(furn).stroke_width(line::THIN);
    sheet.ctx.rect(m, head_y, mk, mk);
    sheet.ctx.line(m + mk / 2.0, head_y, m + mk / 2.0, head_y + mk);
    sheet.ctx.line(m, head_y + mk / 2.0, m + mk, head_y + mk / 2.0);
    sheet.label_weighted(inputs::FOUNDRY, m + mk + 16.0, head_y, l.furn, furn, -1, 400.0);
    sheet.label_weighted(inputs::LICENSE, w - m, head_y, l.furn, furn, 1, 400.0);
    sheet.label_weighted(&footer_l, m, foot_y, l.furn, furn, -1, 400.0);
    sheet.label_weighted(inputs::REPO, w - m, foot_y, l.furn, furn, 1, 400.0);

    // --- hairline rules under header / over footer ---
    let rule_top = head_y - l.furn - 24.0;
    let rule_bot = foot_y + l.furn * 1.3 + 24.0;
    sheet.ctx.no_fill().stroke(rule).stroke_width(line::FINE);
    sheet.ctx.line(m, rule_top, w - m, rule_top);
    sheet.ctx.line(m, rule_bot, w - m, rule_bot);

    // --- specimen rows: start below the top rule, step down by `lead` ---
    let mut y = rule_top - l.top;
    for row in rows(format) {
        let mut x = m;
        for name in &row {
            x += glyph(&mut sheet, glyphs, name, x, y, l.size, ink);
        }
        y -= l.lead;
    }

    sheet
}
