// README PNG specimen images (designbot port)
//
// Rust port of scripts/build_readme_images.py (drawbot-skia). The Python
// script writes three 2048x1024 PNGs; the designbot CLI rewrites every
// render_to_* path to its single --output flag, so this script takes a MODE
// argument (after --) selecting which image to draw and renders exactly one
// PNG. Invoke it once per image:
//
//   designbot --render scripts/designbot/readme_images.rs \
//       --output documentation/assets/readme/glyphset-overview.png -- glyphset
//   designbot --render scripts/designbot/readme_images.rs \
//       --output documentation/assets/readme/aa-grid.png -- aa-grid
//   designbot --render scripts/designbot/readme_images.rs \
//       --output documentation/assets/readme/text-sizes.png -- text-sizes
//
// Fonts: the Python original loads the four static TTFs by path; the statics
// share ambiguous family naming (Regular and Bold are both family "Virtua
// Grotesk"), so this port loads the variable font once and selects weights
// via the wght axis (Regular=400, Medium=500, SemiBold=600, Bold=700 — the
// statics are instances of the same VF). Run `make build` first if
// fonts/variable/ is missing.
//
// Layout note: designbot is y-DOWN / top-left origin; the drawbot original
// is y-UP / bottom-left with text() taking the BASELINE y. All layout math
// below keeps the original drawbot y-up baseline coordinates and converts at
// the draw call: top_of_line = (HEIGHT - y_up) - baseline_offset(size),
// where baseline_offset mirrors parley's line metrics (calibrated
// pixel-exactly against designbot output for both Virtua Grotesk and
// Helvetica).

use designbot::prelude::*;
use std::env;
use std::fs;

const WIDTH: f64 = 2048.0;
const HEIGHT: f64 = 1024.0;
const MARGIN: f64 = 96.0;

const VF_PATH: &str = "fonts/variable/VirtuaGrotesk[wght].ttf";
const VG_FAMILY: &str = "Virtua Grotesk";

// Helvetica (macOS system font, used for captions/labels like the Python
// original): hhea ascender 1577 / descender -471, upm 2048.
const HELV_ASC: f64 = 1577.0 / 2048.0;
const HELV_DESC: f64 = 471.0 / 2048.0;

// Palette: the Python original uses float RGB; designbot uses u8
// (value = round(float * 255)).
fn ink() -> Color {
    Color::rgb(219, 219, 209) // (0.86, 0.86, 0.82)
}
fn paper() -> Color {
    Color::rgb(33, 33, 33) // (0.13, 0.13, 0.13)
}
fn muted() -> Color {
    Color::rgb(148, 148, 138) // (0.58, 0.58, 0.54)
}
fn rule() -> Color {
    Color::rgb(87, 87, 82) // (0.34, 0.34, 0.32)
}
fn grid_minor() -> Color {
    Color::rgb(56, 56, 54) // (0.22, 0.22, 0.21)
}
fn grid_major() -> Color {
    Color::rgb(107, 107, 99) // (0.42, 0.42, 0.39)
}
fn accent() -> Color {
    Color::rgb(184, 184, 173) // (0.72, 0.72, 0.68)
}
fn blue() -> Color {
    Color::rgb(199, 199, 189) // (0.78, 0.78, 0.74)
}

fn wght(style: &str) -> f32 {
    match style {
        "Medium" => 500.0,
        "SemiBold" => 600.0,
        "Bold" => 700.0,
        _ => 400.0,
    }
}

// ---------------------------------------------------------------------------
// Minimal SFNT parsing (the Python original uses fontTools for this)
// ---------------------------------------------------------------------------

fn be16(d: &[u8], o: usize) -> u32 {
    ((d[o] as u32) << 8) | d[o + 1] as u32
}

fn be32(d: &[u8], o: usize) -> u32 {
    ((d[o] as u32) << 24) | ((d[o + 1] as u32) << 16) | ((d[o + 2] as u32) << 8) | d[o + 3] as u32
}

fn i16be(d: &[u8], o: usize) -> i32 {
    be16(d, o) as u16 as i16 as i32
}

fn find_table(data: &[u8], tag: &[u8; 4]) -> Option<usize> {
    let num_tables = be16(data, 4) as usize;
    for i in 0..num_tables {
        let rec = 12 + 16 * i;
        if rec + 16 > data.len() {
            break;
        }
        if &data[rec..rec + 4] == tag {
            return Some(be32(data, rec + 8) as usize);
        }
    }
    None
}

struct Metrics {
    upm: i32,
    ascender: i32,  // hhea
    descender: i32, // hhea (negative)
    cap_height: i32,
    x_height: i32,
    asc_frac: f64,  // hhea ascender / upm (for baseline placement)
    desc_frac: f64, // -hhea descender / upm
}

fn font_metrics(path: &str) -> Result<Metrics, String> {
    let data = fs::read(path).map_err(|e| format!("{e}"))?;
    if data.len() < 12 {
        return Err("not an SFNT font".into());
    }
    let head = find_table(&data, b"head").ok_or("no head table")?;
    let hhea = find_table(&data, b"hhea").ok_or("no hhea table")?;
    let os2 = find_table(&data, b"OS/2").ok_or("no OS/2 table")?;
    let upm = be16(&data, head + 18) as i32;
    let ascender = i16be(&data, hhea + 4);
    let descender = i16be(&data, hhea + 6);
    // OS/2 sxHeight / sCapHeight (version >= 2)
    let x_height = i16be(&data, os2 + 86);
    let cap_height = i16be(&data, os2 + 88);
    Ok(Metrics {
        upm,
        ascender,
        descender,
        cap_height,
        x_height,
        asc_frac: ascender as f64 / upm as f64,
        desc_frac: -descender as f64 / upm as f64,
    })
}

// ---------------------------------------------------------------------------
// Baseline conversion helpers
// ---------------------------------------------------------------------------

/// First-line baseline offset from the top of a designbot text line, in
/// pixels. Mirrors parley's line metrics: line height = 1.0 * font size,
/// leading = line height - (ascent + descent), baseline = ascent + leading/2
/// (each rounded to whole pixels, as parley does). Verified pixel-exactly
/// against designbot output for Virtua Grotesk (86 @ 100px) and Helvetica
/// (77 @ 100px).
fn baseline_offset(size: f64, asc: f64, desc: f64) -> f64 {
    let a = (size * asc).round();
    let d = (size * desc).round();
    let leading = size.round() - (a + d);
    (a + leading * 0.5).round()
}

/// Convert a drawbot-style baseline y (measured up from the page bottom)
/// to the designbot top-of-line y for Canvas::text.
fn flip_baseline(y_up: f64, size: f64, asc: f64, desc: f64) -> f64 {
    (HEIGHT - y_up) - baseline_offset(size, asc, desc)
}

/// Flip a plain (non-text) y coordinate.
fn flip(y_up: f64) -> f64 {
    HEIGHT - y_up
}

/// Draw Virtua Grotesk text at (size, wght) with its baseline at y-up `y_up`.
/// Fill color must be set by the caller (matching the Python flow).
fn vg_text(ctx: &mut Canvas, m: &Metrics, s: &str, x: f64, y_up: f64, size: f64, weight: f32) {
    ctx.font(VG_FAMILY);
    ctx.clear_font_variations();
    ctx.font_variation("wght", weight);
    ctx.font_size(size);
    ctx.text(s, x, flip_baseline(y_up, size, m.asc_frac, m.desc_frac));
}

/// Helvetica caption in MUTED, baseline at y-up `y_up` (Python `label`).
fn label(ctx: &mut Canvas, s: &str, x: f64, y_up: f64, size: f64) {
    ctx.save();
    ctx.no_stroke();
    ctx.font("Helvetica");
    ctx.font_size(size);
    ctx.fill(muted());
    ctx.text(s, x, flip_baseline(y_up, size, HELV_ASC, HELV_DESC));
    ctx.restore();
}

/// Page heading: Bold 72 heading, Helvetica 25 subheading, rule underneath.
fn title(ctx: &mut Canvas, m: &Metrics, heading: &str, subheading: &str) {
    ctx.save();
    ctx.no_stroke();
    ctx.fill(ink());
    vg_text(ctx, m, heading, MARGIN, HEIGHT - MARGIN - 24.0, 72.0, 700.0);
    ctx.font("Helvetica");
    ctx.font_size(25.0);
    ctx.fill(muted());
    ctx.text(
        subheading,
        MARGIN,
        flip_baseline(HEIGHT - MARGIN - 68.0, 25.0, HELV_ASC, HELV_DESC),
    );
    ctx.stroke(rule());
    ctx.stroke_width(2.0);
    let y = flip(HEIGHT - MARGIN - 100.0);
    ctx.line(MARGIN, y, WIDTH - MARGIN, y);
    ctx.restore();
}

// ---------------------------------------------------------------------------
// Images
// ---------------------------------------------------------------------------

fn draw_glyphset_overview(ctx: &mut Canvas, m: &Metrics) {
    title(
        ctx,
        m,
        "Virtua Grotesk",
        "Weight axis overview and core Latin glyph set",
    );

    let mut y = HEIGHT - 290.0;
    let samples: [(&str, &str); 6] = [
        ("Regular", "ABCDEFGHIJKLM"),
        ("Regular", "NOPQRSTUVWXYZ"),
        ("Medium", "abcdefghijklm"),
        ("Medium", "nopqrstuvwxyz"),
        ("SemiBold", "0123456789"),
        ("Bold", ".,:;!?&@#$/()[]{}"),
    ];
    for (style, text) in samples {
        label(ctx, style, MARGIN, y + 20.0, 24.0);
        ctx.no_stroke();
        ctx.fill(ink());
        vg_text(ctx, m, text, MARGIN + 170.0, y, 74.0, wght(style));
        y -= 86.0;
    }

    y -= 8.0;
    ctx.save();
    ctx.stroke(rule());
    ctx.stroke_width(2.0);
    ctx.line(MARGIN, flip(y), WIDTH - MARGIN, flip(y));
    ctx.restore();

    y -= 47.0;
    let lines: [(&str, &str); 4] = [
        ("Regular", "Hamburgefontsiv"),
        ("Medium", "Sphinx of black quartz"),
        ("SemiBold", "Pack my box with five dozen"),
        ("Bold", "The quick brown fox jumps"),
    ];
    for (style, text) in lines {
        label(ctx, &format!("wght {style}"), MARGIN, y + 9.0, 20.0);
        ctx.no_stroke();
        ctx.fill(ink());
        vg_text(ctx, m, text, MARGIN + 170.0, y, 36.0, wght(style));
        y -= 42.0;
    }
}

/// Metric guide line with a small colored Helvetica label above it.
fn draw_metric_line(ctx: &mut Canvas, name: &str, y_up: f64, x0: f64, x1: f64, color: Color) {
    ctx.save();
    ctx.stroke(color);
    ctx.stroke_width(3.0);
    ctx.line(x0, flip(y_up), x1, flip(y_up));
    ctx.no_stroke();
    ctx.font("Helvetica");
    ctx.font_size(18.0);
    ctx.fill(color);
    ctx.text(
        name,
        x0 + 14.0,
        flip_baseline(y_up + 8.0, 18.0, HELV_ASC, HELV_DESC),
    );
    ctx.restore();
}

fn draw_aa_grid(ctx: &mut Canvas, m: &Metrics) {
    title(
        ctx,
        m,
        "Aa Construction",
        "1024 UPM, even coordinates, 16-unit chamfer logic",
    );

    let grid_x = 170.0;
    let grid_y = 115.0; // y-up bottom of the grid box
    let grid_w = 1230.0;
    let grid_h = 720.0;
    let scale = grid_h / (m.ascender - m.descender) as f64;
    let baseline_y = grid_y + (-m.descender) as f64 * scale; // y-up

    // Unit grid
    ctx.save();
    ctx.stroke(grid_minor());
    ctx.stroke_width(1.0);
    let mut unit = m.descender;
    while unit <= m.ascender {
        let y = baseline_y + unit as f64 * scale;
        ctx.line(grid_x, flip(y), grid_x + grid_w, flip(y));
        unit += 64;
    }
    let mut unit = 0;
    while unit <= 1536 {
        let x = grid_x + unit as f64 * scale;
        if x <= grid_x + grid_w {
            ctx.line(x, flip(grid_y), x, flip(grid_y + grid_h));
        }
        unit += 64;
    }
    ctx.stroke(grid_major());
    ctx.stroke_width(2.0);
    let mut unit = 0;
    while unit <= 1536 {
        let x = grid_x + unit as f64 * scale;
        if x <= grid_x + grid_w {
            ctx.line(x, flip(grid_y), x, flip(grid_y + grid_h));
        }
        unit += 128;
    }
    ctx.restore();

    // Metric lines (832 and -256 labels are hardcoded in the original too:
    // they are the UFO design values, while the grid spans hhea asc/desc).
    let x1 = grid_x + grid_w;
    draw_metric_line(ctx, "ascender 832", baseline_y + 832.0 * scale, grid_x, x1, muted());
    draw_metric_line(
        ctx,
        "cap 768",
        baseline_y + m.cap_height as f64 * scale,
        grid_x,
        x1,
        blue(),
    );
    draw_metric_line(
        ctx,
        "x-height 576",
        baseline_y + m.x_height as f64 * scale,
        grid_x,
        x1,
        accent(),
    );
    draw_metric_line(ctx, "baseline", baseline_y, grid_x, x1, ink());
    draw_metric_line(ctx, "descender -256", baseline_y + (-256.0 * scale), grid_x, x1, muted());

    // The big "Aa" sample, baseline on the grid's baseline
    ctx.no_stroke();
    ctx.fill(ink());
    vg_text(ctx, m, "Aa", grid_x + 78.0, baseline_y, m.upm as f64 * scale, 400.0);

    // Numeric notes column on the right
    let x = grid_x + grid_w + 78.0;
    let mut y = grid_y + grid_h - 36.0;
    let notes: [(&str, &str); 4] = [
        ("2", "source grid"),
        ("16", "chamfer module"),
        ("64", "visible guide step"),
        ("128", "major guide step"),
    ];
    for (value, note) in notes {
        ctx.no_stroke();
        ctx.fill(ink());
        vg_text(ctx, m, value, x, y, 48.0, 700.0);
        label(ctx, note, x + 112.0, y + 11.0, 23.0);
        y -= 78.0;
    }

    // 45-degree bevel chevron on the cap line
    ctx.save();
    ctx.stroke(accent());
    ctx.stroke_width(3.0);
    ctx.line(
        grid_x + 210.0,
        flip(baseline_y + 715.0 * scale),
        grid_x + 276.0,
        flip(baseline_y + 768.0 * scale),
    );
    ctx.line(
        grid_x + 286.0,
        flip(baseline_y + 768.0 * scale),
        grid_x + 350.0,
        flip(baseline_y + 715.0 * scale),
    );
    ctx.restore();
    label(ctx, "45-degree bevel joins", x, y - 12.0, 24.0);
}

fn draw_text_sizes(ctx: &mut Canvas, m: &Metrics) {
    title(
        ctx,
        m,
        "Text Sizes",
        "Regular text proof from display down to interface sizes",
    );

    let samples: [(f64, &str); 7] = [
        (92.0, "Virtua Grotesk"),
        (62.0, "Chamfered corners, monolinear strokes"),
        (42.0, "The quick brown fox jumps over the lazy dog."),
        (30.0, "Pack my box with five dozen liquor jugs."),
        (22.0, "Sphinx of black quartz, judge my vow. 0123456789"),
        (16.0, "Small text remains open, sturdy, and useful for interface systems."),
        (
            12.0,
            "Caption size: regular rhythm, clear counters, compact spacing, and sharp construction detail.",
        ),
    ];
    let mut y = HEIGHT - 304.0;
    for (size, text) in samples {
        label(ctx, &format!("{} px", size as i64), MARGIN, y + size * 0.26, 20.0);
        ctx.no_stroke();
        ctx.fill(ink());
        vg_text(ctx, m, text, MARGIN + 122.0, y, size, 400.0);
        y -= 58.0_f64.max(size * 1.12);
    }

    y -= 6.0;
    ctx.save();
    ctx.stroke(rule());
    ctx.stroke_width(2.0);
    ctx.line(MARGIN, flip(y), WIDTH - MARGIN, flip(y));
    ctx.restore();
    y -= 52.0;

    for style in ["Regular", "Medium", "SemiBold", "Bold"] {
        label(ctx, style, MARGIN, y + 8.0, 20.0);
        ctx.no_stroke();
        ctx.fill(ink());
        vg_text(
            ctx,
            m,
            "Designing software for careful reading.",
            MARGIN + 122.0,
            y,
            38.0,
            wght(style),
        );
        y -= 45.0;
    }
}

// ---------------------------------------------------------------------------

fn main() {
    let args: Vec<String> = env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("");

    let m = match font_metrics(VF_PATH) {
        Ok(m) => m,
        Err(e) => {
            eprintln!("Error: could not read {VF_PATH}: {e}. Run `make build` first.");
            std::process::exit(1);
        }
    };

    let mut ctx = Canvas::new(WIDTH, HEIGHT);
    ctx.background(paper());

    let mut renderer = Renderer::new(WIDTH as u32, HEIGHT as u32);
    if let Err(e) = renderer.load_font(VF_PATH) {
        eprintln!("Error: could not load font into renderer: {e}");
        std::process::exit(1);
    }

    match mode {
        "glyphset" | "glyphset-overview" => draw_glyphset_overview(&mut ctx, &m),
        "aa-grid" => draw_aa_grid(&mut ctx, &m),
        "text-sizes" => draw_text_sizes(&mut ctx, &m),
        other => {
            eprintln!(
                "Usage: designbot --render scripts/designbot/readme_images.rs \
                 --output <png> -- <glyphset|aa-grid|text-sizes> (got: {other:?})"
            );
            std::process::exit(2);
        }
    }

    // The designbot CLI rewrites this literal path to its --output value.
    renderer.render_to_png(&ctx, "out.png").unwrap();
}
