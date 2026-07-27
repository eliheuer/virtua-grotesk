//! Instagram carousel for the blog's §03 "Dyadic Self-Labeling Grid Systems".
//!
//! Renders portrait 1080x1350 slides into `out/carousel/03-dyadic-grid/` in the
//! section-03 technical-drawing language. One rich section, taught in 6 slides:
//! the two grids, points colored by grid membership, powers-of-two dimensions,
//! and the optical-correction idea.
//!
//!     cargo run --release --bin carousel
//!
//! Content and layout live here; the drawing language lives in `technical.rs`
//! and `lib.rs`; the palette lives in `style.rs`.

use std::path::PathBuf;

use designbot::prelude::Color;
use designbot_render::Renderer;
use virtua_grotesk_social::*;

const FORMAT: Format = Format::Portrait;
const SLIDES: usize = 6;

struct Ctx<'a> {
    renderer: &'a Renderer,
    mono: String,
    reg: PathBuf,
    out: PathBuf,
}

fn main() {
    let mono_path = inputs::geist_mono();
    let mut renderer = Renderer::new(FORMAT.w() as u32, FORMAT.h() as u32);
    let mono = load_family(&mut renderer, mono_path.to_str().unwrap());

    let out = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("out/carousel/03-dyadic-grid");
    let _ = std::fs::remove_dir_all(&out);

    let c = Ctx {
        renderer: &renderer,
        mono,
        reg: inputs::regular_ufo().join("glyphs"),
        out,
    };

    slide_title(&c, 1);
    slide_two_grids(&c, 2);
    slide_points(&c, 3);
    slide_dimensions(&c, 4);
    slide_correction(&c, 5);
    slide_closing(&c, 6);

    println!("wrote {SLIDES} slides -> {}", c.out.display());
}

// --- shared slide chrome -----------------------------------------------------

fn chrome(sheet: &mut Sheet, idx: usize) {
    let m = FORMAT.margin();
    let (w, h) = (FORMAT.w(), FORMAT.h());
    // header + footer hairlines
    sheet.ctx.no_fill().stroke(role::grid::standard()).stroke_width(line::THIN);
    sheet.ctx.line(m, h - m - 40.0, w - m, h - m - 40.0);
    sheet.ctx.line(m, m + 40.0, w - m, m + 40.0);
    // running head (top) and page marker (bottom), y-up
    sheet.label_weighted("§03  DYADIC GRID", m, h - m - 14.0, role::text::CAPTION, role::figure::green(), -1, 600.0);
    sheet.label_weighted(inputs::BRAND, w - m, h - m - 14.0, role::text::CAPTION, role::figure::green(), 1, 600.0);
    sheet.label_weighted(inputs::BRAND_URL, m, m + 14.0, role::text::CAPTION, role::figure::pen(), -1, 400.0);
    sheet.label_weighted(&format!("{idx:02} / {SLIDES:02}"), w - m, m + 14.0, role::text::CAPTION, role::figure::pen(), 1, 500.0);
}

/// A two-swatch legend row centered at (cx, y), y-up baseline.
fn legend(sheet: &mut Sheet, cx: f64, y: f64) {
    let size = role::text::LABEL;
    let t1 = "on 8 = structure";
    let t2 = "off 8, on 2 = correction";
    let w1 = sheet.mono_width(t1, size);
    let w2 = sheet.mono_width(t2, size);
    let gap = 56.0;
    let dot = 26.0;
    let total = dot + 16.0 + w1 + gap + dot + 16.0 + w2;
    let mut x = cx - total / 2.0;
    // green
    sheet.ctx.fill(role::figure::green()).stroke(role::figure::pen()).stroke_width(line::MEDIUM);
    sheet.ctx.oval(x, y - dot + 6.0, dot, dot);
    x += dot + 16.0;
    sheet.label(t1, x, y, size, role::figure::pen(), -1);
    x += w1 + gap;
    // red
    sheet.ctx.fill(role::figure::red()).stroke(role::figure::pen()).stroke_width(line::MEDIUM);
    sheet.ctx.oval(x, y - dot + 6.0, dot, dot);
    x += dot + 16.0;
    sheet.label(t2, x, y, size, role::figure::pen(), -1);
}

fn save(c: &Ctx, sheet: &Sheet, idx: usize) {
    sheet.save(&c.out.join(format!("slide-{idx:02}.png")));
}

// --- slide 1: title ----------------------------------------------------------

fn slide_title(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();
    let (w, h) = (FORMAT.w(), FORMAT.h());

    // faint full grid backdrop
    let f = Frame { s: 1.0, x0: 0.0, baseline: 0.0 };
    full_grid(&mut sheet, &f, 60.0, role::grid::faint(), line::FINE);

    // giant section number
    sheet.label_weighted("03", m, h - m - 300.0, 360.0, role::figure::pen(), -1, 700.0);

    let maxw = w - 2.0 * m;
    let title_y = h * 0.44;
    sheet.label_fit("DYADIC", m, title_y, role::text::DISPLAY, maxw, role::figure::green(), -1, 700.0);
    sheet.label_fit("SELF-LABELING", m, title_y - 116.0, role::text::DISPLAY, maxw, role::figure::green(), -1, 700.0);
    sheet.label_fit("GRID SYSTEMS", m, title_y - 232.0, role::text::DISPLAY, maxw, role::figure::green(), -1, 700.0);

    sheet.label_fit(
        "A design grid whose numbers carry their",
        m, m + 150.0, role::text::BODY, maxw, role::figure::pen(), -1, 400.0,
    );
    sheet.label_fit(
        "own coordinates, in powers of two.",
        m, m + 150.0 - 52.0, role::text::BODY, maxw, role::figure::pen(), -1, 400.0,
    );
    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- slide 2: two grids ------------------------------------------------------

fn slide_two_grids(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();
    let (w, h) = (FORMAT.w(), FORMAT.h());

    heading(&mut sheet, "TWO GRIDS, ONE GLYPH", "The machine reads an 8-unit grid; the eye needs a finer 2-unit one.");

    let o = load_outline(&c.reg, "n");
    let bb = bbox(&o);
    let f = TechnicalStyle::section_three()
        .with_grid_level_points()
        .frame(FORMAT, o.width, bb.y0 - 16.0, bb.y1 + 16.0, 300.0, 260.0);
    let tech = TechnicalStyle::section_three().with_grid_level_points().with_point_size(26.0);
    tech.grid(&mut sheet, &f, &[(&o, 0.0)], bb.y0 - 16.0, bb.y1 + 16.0);
    tech.glyph(&mut sheet, &o, &f, role::figure::yellow());

    legend(&mut sheet, w / 2.0, m + 150.0);
    let _ = h;
    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- slide 3: points on the grid ---------------------------------------------

fn slide_points(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();

    heading(&mut sheet, "POINTS SNAP TO 8", "Almost every on-curve and handle lands on the coarse machine grid.");

    let o = load_outline(&c.reg, "o");
    let bb = bbox(&o);
    let tech = TechnicalStyle::section_three().with_grid_level_points().with_point_size(26.0);
    let f = tech.frame(FORMAT, o.width, bb.y0 - 16.0, bb.y1 + 16.0, 300.0, 260.0);
    tech.grid(&mut sheet, &f, &[(&o, 0.0)], bb.y0 - 16.0, bb.y1 + 16.0);
    tech.glyph(&mut sheet, &o, &f, role::figure::yellow());

    // count how many on-curve/off points are on the 8-grid, truthfully
    let total = o.points.len();
    let on = o.points.iter().filter(|(x, y, _)| on8(*x, *y)).count();
    let msg = format!("{on} of {total} points on the 8-unit grid");
    sheet.label_weighted(&msg, FORMAT.w() / 2.0, m + 150.0, role::text::LABEL, role::figure::pen(), 0, 500.0);

    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- slide 4: powers-of-two dimensions ---------------------------------------

fn slide_dimensions(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();

    heading(&mut sheet, "MEASURED IN 2^k", "Advance, stem, and counter read out as clean sums of powers of two.");

    let o = load_outline(&c.reg, "n");
    let bb = bbox(&o);
    let tech = TechnicalStyle::section_three().with_grid(16.0, line::FINE).with_point_size(22.0);
    let f = tech.frame(FORMAT, o.width, bb.y0 - 16.0, bb.y1 + 120.0, 340.0, 300.0);
    tech.grid(&mut sheet, &f, &[(&o, 0.0)], bb.y0 - 16.0, bb.y1 + 16.0);
    tech.glyph(&mut sheet, &o, &f, role::figure::yellow());

    // stem width from crossings at mid x-height (red = the measured span)
    let y_mid = (bb.y0 + bb.y1) / 2.0;
    let xs = h_crossings(&o.path, y_mid);
    if xs.len() >= 2 {
        dim_h(&mut sheet, &f, xs[0], xs[1], bb.y0 - 72.0, role::figure::red());
    }
    // advance width along the top
    dim_h(&mut sheet, &f, 0.0, o.width, bb.y1 + 96.0, role::figure::purple());

    // x-height stated as a caption so its long 2^k sum never clips the frame
    let xh = (bb.y1 - bb.y0).round() as i64;
    sheet.label_fit(
        &format!("x-height {}", fmt_val(xh)),
        FORMAT.w() / 2.0,
        m + 150.0,
        role::text::LABEL,
        FORMAT.w() - 2.0 * m,
        role::figure::blue(),
        0,
        500.0,
    );

    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- slide 5: optical correction ---------------------------------------------

fn slide_correction(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();
    let w = FORMAT.w();

    heading(&mut sheet, "WHERE 8 ISN'T ENOUGH", "Round shapes overshoot the flat ones; those points drop to the 2-unit grid.");

    let o = load_outline(&c.reg, "o");
    let bb = bbox(&o);
    let tech = TechnicalStyle::section_three().with_grid_level_points().with_point_size(28.0);
    let f = tech.frame(FORMAT, o.width, bb.y0 - 16.0, bb.y1 + 16.0, 300.0, 300.0);
    tech.grid(&mut sheet, &f, &[(&o, 0.0)], bb.y0 - 16.0, bb.y1 + 16.0);
    tech.glyph(&mut sheet, &o, &f, role::figure::yellow());

    // callout for the top overshoot point (max y)
    if let Some((px, py, _)) = o.points.iter().cloned().max_by(|a, b| a.1.partial_cmp(&b.1).unwrap()) {
        let (cx, cy) = (f.x(px), f.y(py));
        let color = if on8(px, py) { role::figure::green() } else { role::figure::red() };
        sheet.ctx.no_fill().stroke(color).stroke_width(line::STRONG);
        sheet.ctx.line(cx, cy, cx + 120.0, cy + 90.0);
        sheet.label_padded(&format!("y = {}", py.round() as i64), cx + 132.0, cy + 78.0, role::text::LABEL, color, -1);
    }

    legend(&mut sheet, w / 2.0, m + 150.0);
    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- slide 6: closing --------------------------------------------------------

fn slide_closing(c: &Ctx, idx: usize) {
    let mut sheet = new_sheet(c.renderer, &c.mono, FORMAT);
    let m = FORMAT.margin();
    let (w, h) = (FORMAT.w(), FORMAT.h());

    let f = Frame { s: 1.0, x0: 0.0, baseline: 0.0 };
    full_grid(&mut sheet, &f, 60.0, role::grid::faint(), line::FINE);

    let maxw = w - 2.0 * m;
    sheet.label_fit("THE GRID", m, h * 0.60, role::text::DISPLAY, maxw, role::figure::green(), -1, 700.0);
    sheet.label_fit("LABELS ITSELF", m, h * 0.60 - 116.0, role::text::DISPLAY, maxw, role::figure::green(), -1, 700.0);

    for (i, line) in [
        "Coordinates that are already powers of two",
        "give a neural network a self-describing",
        "target: the number is the label. Read the",
        "full essay on Virtua Grotesk.",
    ]
    .iter()
    .enumerate()
    {
        sheet.label_fit(line, m, h * 0.40 - i as f64 * 52.0, role::text::BODY, maxw, role::figure::pen(), -1, 400.0);
    }
    chrome(&mut sheet, idx);
    save(c, &sheet, idx);
}

// --- heading helper ----------------------------------------------------------

fn heading(sheet: &mut Sheet, title: &str, sub: &str) {
    let m = FORMAT.margin();
    let (w, h) = (FORMAT.w(), FORMAT.h());
    let maxw = w - 2.0 * m;
    sheet.label_fit(title, m, h - m - 130.0, role::text::TITLE, maxw, role::figure::green(), -1, 700.0);
    sheet.label_fit(sub, m, h - m - 186.0, role::text::CAPTION, maxw, role::figure::pen(), -1, 400.0);
    let _: Color = role::figure::pen();
}
