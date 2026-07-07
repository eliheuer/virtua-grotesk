// Canvas toolchain for the AI glyph-completion harness (designbot script).
//
// One coordinate frame, implemented once. Agents run these modes and never
// do pixel<->font-unit math themselves. Spec: plans/ai-font-completion-harness.md §4b.
//
//   1024 x 1536 px, 1 font unit = 1 px, drawing band ascender..descender,
//   224 px top/bottom margins. row = MARGIN + (ASCENDER - y).
//   Machine-facing graphics: pure green #00ff00 (chroma-key), ink black,
//   ghost light gray.
//
// Usage (always through the designbot CLI, from the repo root):
//   designbot --render harness/designbot/glyph_canvas.rs --output OUT.png -- template
//   designbot --render harness/designbot/glyph_canvas.rs --output OUT.png -- \
//       sheet sources/VirtuaGrotesk-Regular.ufo o,n,H,O,e,s,comma
//   designbot --render harness/designbot/glyph_canvas.rs --output OUT.png -- \
//       ghost SKETCH.png baseline:cap MASK_OUT.png
//   designbot --render harness/designbot/glyph_canvas.rs --output OUT.png -- \
//       glyphbox sources/VirtuaGrotesk-Regular.ufo question
//
// Modes:
//   template  Blank canvas template (metric lines, labels, fiducials).
//   sheet     Style sheet: named glyphs from a UFO at 1:1 scale on the frame.
//   ghost     Template + sketch registered into a vertical band as a light
//             gray ghost; also writes the drawing-band mask PNG (RGBA,
//             transparent = editable) for masked image-API edits.
//   glyphbox  One glyph from a UFO on the template with its advance box —
//             machine-facing sanity render of current source state.

use designbot::prelude::*;
use designbot::kurbo::{Affine, BezPath};
use designbot::{image, norad};

const W: f64 = 1024.0;
const H: f64 = 1536.0;
const MARGIN: f64 = 224.0;

const ASCENDER: f64 = 832.0;
const CAP: f64 = 768.0;
const XHEIGHT: f64 = 576.0;
const BASELINE: f64 = 0.0;
const DESCENDER: f64 = -256.0;

const ZONES: [(&str, &str, f64); 5] = [
    ("ascender", "asc", ASCENDER),
    ("cap", "cap", CAP),
    ("xheight", "x-height", XHEIGHT),
    ("baseline", "baseline", BASELINE),
    ("descender", "desc", DESCENDER),
];

const FIDUCIAL: f64 = 16.0;
const GREEN: (u8, u8, u8) = (0, 255, 0);
const GHOST_GRAY: (u8, u8, u8) = (200, 200, 200);

fn row(y_units: f64) -> f64 {
    MARGIN + (ASCENDER - y_units)
}

fn parse_zone(s: &str) -> f64 {
    for (name, _, v) in ZONES {
        if s == name {
            return v;
        }
    }
    s.parse::<f64>().unwrap_or_else(|_| {
        eprintln!("bad zone {s:?}: use ascender/cap/xheight/baseline/descender or a number");
        std::process::exit(1);
    })
}

fn parse_band(spec: &str) -> (f64, f64) {
    let (a, b) = spec.split_once(':').unwrap_or_else(|| {
        eprintln!("bad band {spec:?}: expected lo:hi");
        std::process::exit(1);
    });
    let (a, b) = (parse_zone(a), parse_zone(b));
    (a.min(b), a.max(b))
}

fn green() -> Color {
    Color::rgb(GREEN.0, GREEN.1, GREEN.2)
}

fn paint_frame(ctx: &mut Canvas, width: f64) {
    ctx.background(Color::rgb(255, 255, 255));
    ctx.stroke(green());
    ctx.stroke_width(2.0);
    ctx.no_fill();
    for (_, _, y) in ZONES {
        let r = row(y);
        ctx.line(0.0, r, width, r);
    }
    ctx.no_stroke();
    ctx.fill(green());
    for fx in [8.0, width - FIDUCIAL - 8.0] {
        for fy in [8.0, H - FIDUCIAL - 8.0] {
            ctx.rect(fx, fy, FIDUCIAL, FIDUCIAL);
        }
    }
    ctx.font_size(24.0);
    for (_, label, y) in ZONES {
        ctx.text(label, 40.0, row(y) - 8.0);
    }
}

fn ufo_affine(t: &norad::AffineTransform) -> Affine {
    Affine::new([t.x_scale, t.xy_scale, t.yx_scale, t.y_scale, t.x_offset, t.y_offset])
}

/// Glyph outline (components resolved) as a BezPath in font units, y-up.
fn glyph_path(font: &norad::Font, name: &str, depth: u8) -> BezPath {
    if depth > 4 {
        eprintln!("component nesting too deep at {name:?}");
        std::process::exit(1);
    }
    let glyph = font.get_glyph(name).unwrap_or_else(|| {
        eprintln!("glyph {name:?} not found in UFO");
        std::process::exit(1);
    });
    let mut path = BezPath::new();
    // Build segments from raw points (norad's to_kurbo() returns a different
    // kurbo version's BezPath than designbot's canvas API takes).
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
                        eprintln!("unsupported segment in {name:?} ({k} offcurves)");
                        std::process::exit(1);
                    }
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

/// Place a font-unit path onto the canvas frame at pen position x0 (px).
fn to_canvas(mut path: BezPath, x0: f64) -> BezPath {
    path.apply_affine(Affine::new([1.0, 0.0, 0.0, -1.0, x0, MARGIN + ASCENDER]));
    path
}

fn load_font(ufo: &str) -> norad::Font {
    norad::Font::load(ufo).unwrap_or_else(|e| {
        eprintln!("failed to load UFO {ufo:?}: {e}");
        std::process::exit(1);
    })
}

fn warn_if_not_green(font: &norad::Font, name: &str) {
    let mark = font
        .get_glyph(name)
        .and_then(|g| g.lib.get("public.markColor"))
        .and_then(|v| v.as_string().map(str::to_string));
    if mark.as_deref() != Some("0.09,0.72,0.44,1") {
        eprintln!("warning: {name} is not marked green (markColor={mark:?})");
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mode = args.first().map(String::as_str).unwrap_or("");

    let (mut ctx, width) = match mode {
        "template" => {
            let mut ctx = Canvas::new(W, H);
            paint_frame(&mut ctx, W);
            (ctx, W)
        }
        "sheet" => {
            let (ufo, names) = (&args[1], &args[2]);
            let font = load_font(ufo);
            let names: Vec<&str> = names.split(',').map(str::trim).collect();
            let gap = 48.0;
            let mut x = 64.0;
            let mut placed: Vec<(BezPath, f64)> = Vec::new();
            for name in &names {
                warn_if_not_green(&font, name);
                let advance = font.get_glyph(*name).map(|g| g.width).unwrap_or(0.0);
                placed.push((glyph_path(&font, name, 0), x));
                x += advance + gap;
            }
            let width = (x + 64.0 - gap).ceil();
            let mut ctx = Canvas::new(width, H);
            paint_frame(&mut ctx, width);
            ctx.no_stroke();
            ctx.fill(Color::rgb(0, 0, 0));
            for (path, x0) in placed {
                ctx.draw_path(to_canvas(path, x0));
            }
            (ctx, width)
        }
        "ghost" => {
            let (sketch, band, mask_out) = (&args[1], &args[2], &args[3]);
            let (y_lo, y_hi) = parse_band(band);

            let src = image::open(sketch)
                .unwrap_or_else(|e| {
                    eprintln!("failed to open sketch {sketch:?}: {e}");
                    std::process::exit(1);
                })
                .to_luma8();
            let (sw, sh) = src.dimensions();
            let (mut x0, mut y0, mut x1, mut y1) = (sw, sh, 0u32, 0u32);
            for (px, py, p) in src.enumerate_pixels() {
                if p.0[0] < 128 {
                    x0 = x0.min(px);
                    y0 = y0.min(py);
                    x1 = x1.max(px);
                    y1 = y1.max(py);
                }
            }
            if x1 < x0 {
                eprintln!("no dark pixels found in sketch image");
                std::process::exit(1);
            }
            let crop = image::imageops::crop_imm(&src, x0, y0, x1 - x0 + 1, y1 - y0 + 1).to_image();
            let band_px = (y_hi - y_lo).round() as u32;
            let new_w =
                ((crop.width() as f64) * (band_px as f64) / (crop.height() as f64)).round() as u32;
            let scaled = image::imageops::resize(
                &crop,
                new_w.max(1),
                band_px,
                image::imageops::FilterType::Lanczos3,
            );
            let mut rgba = Vec::with_capacity((scaled.width() * scaled.height() * 4) as usize);
            for p in scaled.pixels() {
                if p.0[0] < 128 {
                    rgba.extend_from_slice(&[GHOST_GRAY.0, GHOST_GRAY.1, GHOST_GRAY.2, 255]);
                } else {
                    rgba.extend_from_slice(&[0, 0, 0, 0]);
                }
            }
            let row_top = row(y_hi);
            let col_left = ((W - new_w as f64) / 2.0).round();

            let mut ctx = Canvas::new(W, H);
            paint_frame(&mut ctx, W);
            ctx.image_rgba(rgba, scaled.width(), scaled.height(), col_left, row_top, 1.0);

            // Drawing-band mask: transparent = editable (image-API convention).
            let mut mask = image::RgbaImage::from_pixel(
                W as u32,
                H as u32,
                image::Rgba([255, 255, 255, 255]),
            );
            for py in (MARGIN as u32)..((H - MARGIN) as u32) {
                for px in 32..(W as u32 - 32) {
                    mask.put_pixel(px, py, image::Rgba([0, 0, 0, 0]));
                }
            }
            mask.save(mask_out).unwrap_or_else(|e| {
                eprintln!("failed to write mask {mask_out:?}: {e}");
                std::process::exit(1);
            });
            eprintln!(
                "ghost: band {y_lo}:{y_hi} -> rows {}..{}, cols {}..{}; mask -> {mask_out}",
                row_top,
                row_top + band_px as f64,
                col_left,
                col_left + new_w as f64
            );
            (ctx, W)
        }
        "glyphbox" => {
            let (ufo, name) = (&args[1], &args[2]);
            let font = load_font(ufo);
            let advance = font.get_glyph(name.as_str()).map(|g| g.width).unwrap_or(0.0);
            let x0 = ((W - advance) / 2.0).round();
            let mut ctx = Canvas::new(W, H);
            paint_frame(&mut ctx, W);
            ctx.stroke(green());
            ctx.stroke_width(2.0);
            ctx.no_fill();
            ctx.line(x0, MARGIN, x0, H - MARGIN);
            ctx.line(x0 + advance, MARGIN, x0 + advance, H - MARGIN);
            ctx.no_stroke();
            ctx.fill(Color::rgb(0, 0, 0));
            ctx.draw_path(to_canvas(glyph_path(&font, name, 0), x0));
            (ctx, W)
        }
        _ => {
            eprintln!("usage: -- template | sheet UFO G1,G2,.. | ghost SKETCH lo:hi MASK.png | glyphbox UFO GLYPH");
            std::process::exit(1);
        }
    };

    let _ = &mut ctx;
    let renderer = Renderer::new(width as u32, H as u32);
    renderer.render_to_png(&ctx, "glyph_canvas.png").unwrap();
}
