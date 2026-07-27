//! Vertical reel/story (1080x1920), seamless loop: "glyphs as data". A scan
//! band sweeps up and back down the glyph, sampling the 8-unit grid — the
//! visual argument that every point is a labeled sample on a powers-of-two
//! grid (blog §05 / §08).
//!
//! Renders a numbered PNG frame sequence into `out/frames/reel_grid/`. The loop
//! is seamless because the scan uses a ping-pong ramp: frame 0 == frame N.
//! `render.sh` encodes it to a looping mp4.
//!
//!     cargo run --release --bin reel_grid

use std::path::PathBuf;

use designbot_render::Renderer;
use virtua_grotesk_social::*;

const FPS: usize = 30;
const SECONDS: f64 = 5.0;
const FORMAT: Format = Format::Vertical;
const GRID_UNIT: f64 = 8.0;

fn main() {
    let mono_path = inputs::geist_mono();
    let mut renderer = Renderer::new(FORMAT.w() as u32, FORMAT.h() as u32);
    let mono = load_family(&mut renderer, mono_path.to_str().unwrap());

    let o = load_outline(&inputs::regular_ufo().join("glyphs"), "n");
    let bb = bbox(&o);
    let bottom = bb.y0 - 16.0;
    let top = bb.y1 + 16.0;

    let tech = TechnicalStyle::section_three()
        .with_grid_level_points()
        .with_grid(GRID_UNIT, line::FINE)
        .with_point_size(26.0);

    let out_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("out/frames/reel_grid");
    let _ = std::fs::remove_dir_all(&out_dir);

    let frames = FPS * SECONDS as usize;
    let m = FORMAT.margin();
    let band_top = 360.0;
    let band_bottom = 320.0;

    for frame in 0..frames {
        let phase = frame as f64 / frames as f64;
        let scan = loop_pingpong(phase); // 0 -> 1 -> 0, seamless
        let scan_y = lerp(bb.y0, bb.y1, scan); // source-space row being sampled

        let f = tech.frame(FORMAT, o.width, bottom, top, band_top, band_bottom);
        let mut sheet = new_sheet(&renderer, &mono, FORMAT);
        sheet.ctx.line_cap("round");

        // grid + glyph body (points drawn after the band so they stay crisp)
        tech.grid(&mut sheet, &f, &[(&o, 0.0)], bottom, top);
        draw_body(&mut sheet, &o, &f, role::figure::yellow(), role::figure::pen(), tech.pen);

        // translucent scan band (+/- 1.5 grid units around the sampled row)
        let half = 1.5 * GRID_UNIT;
        let y_hi = f.y(scan_y + half);
        let x0 = f.x(0.0);
        let x1 = f.x(o.width);
        sheet.ctx.no_stroke().fill(with_alpha(role::figure::green(), 46));
        sheet.ctx.rect(x0, y_hi, x1 - x0, 2.0 * half * f.s);

        // bright sampled row line + readout value
        sheet.ctx.no_fill().stroke(role::figure::green()).stroke_width(line::STRONG);
        sheet.ctx.line(x0, f.y(scan_y), x1, f.y(scan_y));

        // points on top, colored by grid membership
        tech.points(&mut sheet, &o, &f);

        // headline (top band) + caption (bottom band), y-up
        let head_y = FORMAT.h() - m - 96.0;
        sheet.label_weighted("GLYPHS", m, head_y, role::text::TITLE, role::figure::green(), -1, 700.0);
        sheet.label_weighted("AS DATA", m, head_y - 88.0, role::text::TITLE, role::figure::green(), -1, 700.0);

        let sample = ((scan_y / GRID_UNIT).round() * GRID_UNIT) as i64;
        sheet.label_weighted(
            &format!("sampling row  y = {sample}"),
            FORMAT.w() / 2.0,
            m + 150.0,
            role::text::LABEL,
            role::figure::pen(),
            0,
            500.0,
        );
        sheet.label_weighted(
            "every point is a labeled sample on the 2^k grid",
            FORMAT.w() / 2.0,
            m + 88.0,
            role::text::CAPTION,
            role::figure::pen(),
            0,
            400.0,
        );

        sheet.save(&out_dir.join(format!("{frame:04}.png")));
    }
    println!("wrote {frames} frames -> {}", out_dir.display());
}
