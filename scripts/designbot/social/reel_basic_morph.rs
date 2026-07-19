// Minimal social animation test: one centered glyph morphing Regular <-> Bold.
//
//   designbot --render scripts/designbot/social/reel_basic_morph.rs \
//       --output documentation/assets/social/video/basic-morph-a.mp4 -- a
//
// The composition deliberately keeps the concept small: one glyph, one grid,
// one motion. The output is a 4-second seamless 30 fps vertical reel.

use designbot::kurbo::{Affine, BezPath, Point, Shape};
use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;
use std::fs;
use std::path::PathBuf;

const W: f64 = 1080.0;
const H: f64 = 1920.0;
const FPS: f64 = 30.0;
const SECONDS: f64 = 4.0;

#[derive(Clone)]
struct Glyph {
    contours: Vec<Vec<(f64, f64, bool)>>,
    width: f64,
}

fn attr(tag: &str, name: &str) -> Option<String> {
    let needle = format!("{name}=\"");
    let start = tag.find(&needle)? + needle.len();
    let rest = &tag[start..];
    Some(rest[..rest.find('"')?].to_string())
}

fn load_glyph(path: &PathBuf) -> Glyph {
    let text = fs::read_to_string(path).expect("read glif");
    let advance = text
        .split("<advance")
        .nth(1)
        .and_then(|s| s.split('>').next())
        .and_then(|s| attr(s, "width"))
        .and_then(|s| s.parse().ok())
        .unwrap_or(600.0);
    let mut contours = Vec::new();
    for chunk in text.split("<contour>").skip(1) {
        let body = &chunk[..chunk.find("</contour>").unwrap_or(chunk.len())];
        let mut points = Vec::new();
        for tag in body.split("<point").skip(1) {
            let tag = &tag[..tag.find("/>").unwrap_or(tag.len())];
            let x = attr(tag, "x").and_then(|v| v.parse().ok()).unwrap_or(0.0);
            let y = attr(tag, "y").and_then(|v| v.parse().ok()).unwrap_or(0.0);
            points.push((x, y, attr(tag, "type").is_none()));
        }
        if !points.is_empty() {
            contours.push(points);
        }
    }
    Glyph { contours, width: advance }
}

fn interp(a: &Glyph, b: &Glyph, t: f64) -> Glyph {
    let contours = a.contours.iter().zip(&b.contours).map(|(ca, cb)| {
        ca.iter().zip(cb).map(|(pa, pb)| {
            (lerp(pa.0, pb.0, t), lerp(pa.1, pb.1, t), pa.2)
        }).collect()
    }).collect();
    Glyph { contours, width: lerp(a.width, b.width, t) }
}

fn path(g: &Glyph) -> BezPath {
    let mut out = BezPath::new();
    for points in &g.contours {
        let n = points.len();
        let Some(start) = points.iter().position(|p| !p.2) else { continue };
        out.move_to(Point::new(points[start].0, points[start].1));
        let mut handles = Vec::new();
        for k in 1..=n {
            let p = points[(start + k) % n];
            if p.2 {
                handles.push(Point::new(p.0, p.1));
            } else if handles.len() == 2 {
                out.curve_to(handles[0], handles[1], Point::new(p.0, p.1));
                handles.clear();
            } else {
                out.line_to(Point::new(p.0, p.1));
                handles.clear();
            }
        }
        out.close_path();
    }
    out
}

fn main() {
    let glyph = env::args().nth(1).unwrap_or_else(|| "a".to_string());
    let glyph_file = if glyph.ends_with(".glif") { glyph.clone() } else { format!("{glyph}.glif") };
    let home = env::var("HOME").expect("HOME");
    let root = PathBuf::from(home).join("GH/repos/virtua-grotesk/sources");
    let reg = load_glyph(&root.join("VirtuaGrotesk-Regular.ufo/glyphs").join(&glyph_file));
    let bold = load_glyph(&root.join("VirtuaGrotesk-Bold.ufo/glyphs").join(&glyph_file));

    let frames = (FPS * SECONDS) as usize;
    let mut ctx = Canvas::new(W, H);
    ctx.frame_duration(1.0 / FPS);
    let grid_view = env::var("GRID_VIEW").ok().as_deref() == Some("1");

    for frame in 0..frames {
        if frame > 0 { ctx.new_page(); }
        let t = frame as f64 / frames as f64;
        let weight = 0.5 - 0.5 * (t * std::f64::consts::TAU).cos();
        let g = interp(&reg, &bold, ease_in_out_sine(weight));
        ctx.background(Color::rgb(16, 16, 16));

        let margin = 64.0;
        let unit = 32.0;
        if grid_view {
            ctx.stroke(Color::rgb(38, 38, 38)).stroke_width(1.0);
            for x in (margin as i32..W as i32 - margin as i32).step_by(unit as usize) {
                ctx.line(x as f64, margin, x as f64, H - margin);
            }
            for y in (margin as i32..H as i32 - margin as i32).step_by(unit as usize) {
                ctx.line(margin, y as f64, W - margin, y as f64);
            }
        }

        let bounds = path(&g).bounding_box();
        let scale = (W * 0.72 / (bounds.x1 - bounds.x0)).min(H * 0.52 / (bounds.y1 - bounds.y0));
        let x = (W - (bounds.x1 - bounds.x0) * scale) / 2.0 - bounds.x0 * scale;
        let y = (H - (bounds.y1 - bounds.y0) * scale) / 2.0 - bounds.y0 * scale;
        ctx.fill(Color::rgb(255, 58, 40)).no_stroke();
        ctx.draw_path(Affine::translate((x, y)) * Affine::scale(scale) * path(&g));
    }

    Renderer::new(W as u32, H as u32)
        .render_to_mp4(&ctx, "basic-morph-a.mp4")
        .expect("render mp4");
    println!("rendered {frames} frames -> basic-morph-a.mp4");
}
