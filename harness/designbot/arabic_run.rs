// Render joined Arabic runs from a UFO, glyph names in VISUAL order
// (left to right on the page). Dot components are drawn in a second colour
// so seam collisions between neighbouring clusters are unmissable.
//
// Usage (from the repo root):
//   designbot --render harness/designbot/arabic_run.rs --output OUT.png -- \
//       sources/VirtuaGrotesk-Regular.ufo \
//       "beh-ar.fina beh-ar.medi beh-ar.init" \
//       "yeh-ar.fina teh-ar.medi teh-ar.init"
//
// Each quoted argument after the UFO is one line of the render.

use designbot::prelude::*;
use designbot::kurbo::{Affine, BezPath};
use designbot::norad;

const SCALE: f64 = 0.55;
const LINE_H: f64 = 1024.0 * SCALE + 120.0;
const MARGIN: f64 = 80.0;

const BG: (u8, u8, u8) = (26, 26, 26);
const INK: (u8, u8, u8) = (176, 176, 176);
const DOT: (u8, u8, u8) = (232, 116, 96);
const RULE: (u8, u8, u8) = (58, 58, 58);
const SEAM: (u8, u8, u8) = (70, 110, 70);

fn is_dot(name: &str) -> bool {
    (name.contains("dot") || name.contains("Dot")) && name.ends_with("-ar")
}

fn ufo_affine(t: &norad::AffineTransform) -> Affine {
    Affine::new([t.x_scale, t.xy_scale, t.yx_scale, t.y_scale, t.x_offset, t.y_offset])
}

fn contours_path(glyph: &norad::Glyph) -> BezPath {
    let mut path = BezPath::new();
    for contour in &glyph.contours {
        let pts = &contour.points;
        let Some(start) = pts
            .iter()
            .position(|p| !matches!(p.typ, norad::PointType::OffCurve))
        else {
            continue;
        };
        let n = pts.len();
        let first = &pts[start];
        path.move_to((first.x, first.y));
        let mut pending: Vec<(f64, f64)> = Vec::new();
        for i in 1..=n {
            let p = &pts[(start + i) % n];
            match p.typ {
                norad::PointType::OffCurve => pending.push((p.x, p.y)),
                norad::PointType::Line | norad::PointType::Move => {
                    path.line_to((p.x, p.y));
                    pending.clear();
                }
                _ => match pending.len() {
                    2 => {
                        path.curve_to(pending[0], pending[1], (p.x, p.y));
                        pending.clear();
                    }
                    0 => path.line_to((p.x, p.y)),
                    k => {
                        eprintln!("unsupported segment in {:?} ({k} offcurves)", glyph.name());
                        std::process::exit(1);
                    }
                },
            }
        }
        path.close_path();
    }
    path
}

/// Resolve a glyph into (body, dots) paths in font units, splitting off any
/// component whose base is a dot mark.
fn split_paths(font: &norad::Font, name: &str, depth: u8) -> (BezPath, BezPath) {
    if depth > 4 {
        eprintln!("component nesting too deep at {name:?}");
        std::process::exit(1);
    }
    let glyph = font.get_glyph(name).unwrap_or_else(|| {
        eprintln!("glyph {name:?} not found in UFO");
        std::process::exit(1);
    });
    let mut body = contours_path(glyph);
    let mut dots = BezPath::new();
    for component in &glyph.components {
        let base = component.base.as_str();
        let (sub_body, sub_dots) = split_paths(font, base, depth + 1);
        let xf = ufo_affine(&component.transform);
        let target = if is_dot(base) { &mut dots } else { &mut body };
        let mut b = sub_body;
        b.apply_affine(xf);
        target.extend(b.elements().iter().copied());
        let mut d = sub_dots;
        d.apply_affine(xf);
        dots.extend(d.elements().iter().copied());
    }
    (body, dots)
}

fn advance(font: &norad::Font, name: &str) -> f64 {
    font.get_glyph(name).map(|g| g.width).unwrap_or(0.0)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let ufo = &args[0];
    let lines: Vec<Vec<String>> = args[1..]
        .iter()
        .map(|l| l.split_whitespace().map(String::from).collect())
        .collect();

    let font = norad::Font::load(ufo).unwrap_or_else(|e| {
        eprintln!("failed to load UFO {ufo:?}: {e}");
        std::process::exit(1);
    });

    let widths: Vec<f64> = lines
        .iter()
        .map(|l| l.iter().map(|n| advance(&font, n)).sum::<f64>() * SCALE)
        .collect();
    let w = widths.iter().cloned().fold(0.0, f64::max) + MARGIN * 2.0;
    let h = LINE_H * lines.len() as f64 + MARGIN;

    let mut ctx = Canvas::new(w, h);
    ctx.background(Color::rgb(BG.0, BG.1, BG.2));

    for (li, names) in lines.iter().enumerate() {
        // Baseline for this line, measured down from the top.
        let base_y = h - MARGIN - LINE_H * li as f64 - 320.0 * SCALE;

        ctx.no_fill();
        ctx.stroke(Color::rgb(RULE.0, RULE.1, RULE.2));
        ctx.stroke_width(1.0);
        ctx.line(MARGIN, base_y, w - MARGIN, base_y);

        // Seam ticks: every advance boundary, where the neighbour's ink starts.
        let mut pen = MARGIN;
        ctx.stroke(Color::rgb(SEAM.0, SEAM.1, SEAM.2));
        for name in names {
            ctx.line(pen, base_y - 300.0 * SCALE, pen, base_y + 520.0 * SCALE);
            pen += advance(&font, name) * SCALE;
        }
        ctx.line(pen, base_y - 300.0 * SCALE, pen, base_y + 520.0 * SCALE);
        ctx.no_stroke();

        let mut pen = MARGIN;
        for name in names {
            let (body, dots) = split_paths(&font, name, 0);
            let place = Affine::translate((pen, base_y)) * Affine::scale_non_uniform(SCALE, SCALE);
            for (path, col) in [(body, INK), (dots, DOT)] {
                if path.elements().is_empty() {
                    continue;
                }
                let mut p = path;
                p.apply_affine(place);
                ctx.fill(Color::rgb(col.0, col.1, col.2));
                ctx.draw_path(p);
            }
            pen += advance(&font, name) * SCALE;
        }

        ctx.fill(Color::rgb(120, 120, 120));
        ctx.font_size(20.0);
        ctx.text_box(&names.join("  "), MARGIN, base_y - 300.0 * SCALE - 30.0, w - MARGIN * 2.0, 28.0);
    }

    let renderer = Renderer::new(w as u32, h as u32);
    renderer.render_to_png(&ctx, "arabic_run.png").unwrap();
}
