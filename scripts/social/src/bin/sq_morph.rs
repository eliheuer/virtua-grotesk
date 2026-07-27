//! Square (2048x2048) weight-interpolation animation: the Regular `n` morphing
//! to the Bold `n` and back, in the section-03 technical-drawing language.
//!
//! Renders a numbered PNG frame sequence (seamless loop: last frame == first)
//! into `out/frames/sq_morph/`. `render.sh` encodes the sequence to mp4 + gif.
//!
//!     cargo run --release --bin sq_morph
//!
//! The morph is a real master interpolation: Regular and Bold are
//! point-compatible, so every on-curve point, off-curve handle, and the advance
//! width animate together. Point color stays truthful to grid membership
//! (green on the 8-unit grid, red off it) at every frame.

use std::path::PathBuf;

use designbot::prelude::Color;
use designbot_render::Renderer;
use virtua_grotesk_social::*;

const FPS: usize = 30;
const SECONDS: f64 = 4.0;
const FORMAT: Format = Format::Square;

fn mix(a: Color, b: Color, t: f64) -> Color {
    Color::rgb(
        lerp(a.r as f64, b.r as f64, t).round() as u8,
        lerp(a.g as f64, b.g as f64, t).round() as u8,
        lerp(a.b as f64, b.b as f64, t).round() as u8,
    )
}

fn main() {
    let mono_path = inputs::geist_mono();
    let mut renderer = Renderer::new(FORMAT.w() as u32, FORMAT.h() as u32);
    let mono = load_family(&mut renderer, mono_path.to_str().unwrap());

    let reg = load_raw(&inputs::regular_ufo().join("glyphs"), "n");
    let bold = load_raw(&inputs::bold_ufo().join("glyphs"), "n");

    // Fit to the widest / tallest of the two masters so nothing clips mid-morph.
    let ro = reg.to_outline();
    let bo = bold.to_outline();
    let rb = bbox(&ro);
    let bb = bbox(&bo);
    let run = ro.width.max(bo.width);
    let bottom = rb.y0.min(bb.y0) - 24.0;
    let top = rb.y1.max(bb.y1) + 24.0;

    let tech = TechnicalStyle::section_three()
        .with_grid_level_points()
        .with_grid(32.0, line::THIN)
        .with_point_size(30.0);

    let out_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("out/frames/sq_morph");
    let _ = std::fs::remove_dir_all(&out_dir);

    let frames = FPS * SECONDS as usize;
    let band_top = 300.0; // headline band
    let band_bottom = 200.0; // weight readout + attribution band

    for frame in 0..frames {
        let phase = frame as f64 / frames as f64;
        let t = loop_pingpong(phase); // 0 -> 1 -> 0, eased, seamless
        let glyph = interp_raw(&reg, &bold, t).to_outline();

        let f = tech.frame(FORMAT, run, bottom, top, band_top, band_bottom);
        let mut sheet = new_sheet(&renderer, &mono, FORMAT);
        sheet.ctx.line_cap("round");

        // Background source grid + baseline metric.
        tech.grid(&mut sheet, &f, &[(&glyph, 0.0)], bottom, top);
        metric_rules(&mut sheet, &f, 0.0, glyph.width, &[0.0], &[top - 24.0], role::figure::blue(), line::MEDIUM);

        // Body fill lerps yellow (Regular) -> blue (Bold), matching fig-model.
        let fill = mix(role::figure::yellow(), role::figure::blue(), t);
        draw_body(&mut sheet, &glyph, &f, fill, role::figure::pen(), tech.pen);
        tech.points(&mut sheet, &glyph, &f);

        // Headline (top band, y-up so top = large y) + live weight readout
        // (bottom band).
        let m = FORMAT.margin();
        let head_y = FORMAT.h() - m - 96.0;
        sheet.label_weighted("WEIGHT AS", m, head_y, role::text::TITLE, role::figure::green(), -1, 600.0);
        sheet.label_weighted("INTERPOLATION", m, head_y - 92.0, role::text::TITLE, role::figure::green(), -1, 600.0);

        let wght = lerp(400.0, 700.0, t).round() as i64;
        let readout = format!("wght {wght}");
        sheet.label_weighted(&readout, FORMAT.w() / 2.0, m + 128.0, role::text::HEAD, role::figure::pen(), 0, 500.0);
        sheet.label_weighted(
            "Regular <-> Bold  /  one delta, every point moves",
            FORMAT.w() / 2.0,
            m + 56.0,
            role::text::LABEL,
            role::figure::pen(),
            0,
            400.0,
        );

        let out = out_dir.join(format!("{frame:04}.png"));
        sheet.save(&out);
    }
    println!("wrote {frames} frames -> {}", out_dir.display());
}
