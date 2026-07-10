// Social animation 01 — "Grid as Dataset" (the blog hero, in motion).
//
// One content piece, three formats:
//
//   designbot --render scripts/designbot/social/reel_grid_as_dataset.rs \
//       --output documentation/assets/social/video/grid-as-dataset-reel.mp4 -- reel
//   ... -- feed   (1080x1350, IG feed)
//   ... -- wide   (1920x1080, X / LinkedIn)
//   ... -- reel   (1080x1920, IG Reels / Stories / TikTok)
//
// Timeline (~12 s, 30 fps, loop-friendly):
//   grid draws in -> letter outlines arrive -> points pop (Runebender
//   palette) -> Regular<->Bold morph (greens only) -> settle.
//
// Style follows the elih.net blog figures: near-black ground, powers-of-
// two grid in three grays, outline drawing with smooth/corner/off-curve
// points in the Runebender palette. Letters L A B — all human-graded
// green in BOTH masters, so the morph interpolates approved data only.
//
// Self-contained: parses .glif XML with std only; designbot re-exports
// kurbo and the motion easing helpers.

use designbot::kurbo::{Affine, BezPath, Point};
use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;
use std::fs;
use std::path::PathBuf;

const GLYPH_FILES: &[&str] = &["L_.glif", "A_.glif", "B_.glif"];
const LETTER_SPACE: f64 = 64.0; // font units between advances
const FPS: f64 = 30.0;
const SECONDS: f64 = 12.0;

const BG: (u8, u8, u8) = (10, 10, 10);
const OUTLINE: (u8, u8, u8) = (221, 221, 221);
const SMOOTH: (u8, u8, u8) = (24, 184, 111); // runebender green
const CORNER: (u8, u8, u8) = (255, 159, 26); // runebender orange
const OFFCURVE: (u8, u8, u8) = (140, 108, 255); // runebender purple

#[derive(Clone, Copy, PartialEq)]
enum Role {
    Smooth,
    Corner,
    Off,
}

#[derive(Clone)]
struct Glyph {
    // contours as parsed point runs: (x, y, is_offcurve, smooth)
    contours: Vec<Vec<(f64, f64, bool, bool)>>,
    width: f64,
}

fn attr(tag: &str, name: &str) -> Option<String> {
    let pat = format!("{name}=\"");
    let i = tag.find(&pat)? + pat.len();
    let rest = &tag[i..];
    let j = rest.find('"')?;
    Some(rest[..j].to_string())
}

fn load_glyph(path: &PathBuf) -> Glyph {
    let text = fs::read_to_string(path).expect("read glif");
    let width = attr(
        text.split("<advance").nth(1).map(|s| &s[..s.find('>').unwrap_or(0)]).unwrap_or(""),
        "width",
    )
    .and_then(|w| w.parse().ok())
    .unwrap_or(600.0);

    let mut contours = Vec::new();
    for chunk in text.split("<contour>").skip(1) {
        let body = &chunk[..chunk.find("</contour>").unwrap_or(chunk.len())];
        let mut pts = Vec::new();
        for tag in body.split("<point").skip(1) {
            let tag = &tag[..tag.find("/>").unwrap_or(tag.len())];
            let x: f64 = attr(tag, "x").and_then(|v| v.parse().ok()).unwrap_or(0.0);
            let y: f64 = attr(tag, "y").and_then(|v| v.parse().ok()).unwrap_or(0.0);
            let typ = attr(tag, "type");
            let smooth = attr(tag, "smooth").as_deref() == Some("yes");
            pts.push((x, y, typ.is_none(), smooth));
        }
        if !pts.is_empty() {
            contours.push(pts);
        }
    }
    Glyph { contours, width }
}

/// Interpolate two point-compatible glyphs (greens are compatible by the
/// font's own build gate).
fn interp(a: &Glyph, b: &Glyph, t: f64) -> Glyph {
    let contours = a
        .contours
        .iter()
        .zip(&b.contours)
        .map(|(ca, cb)| {
            ca.iter()
                .zip(cb)
                .map(|(pa, pb)| {
                    (lerp(pa.0, pb.0, t), lerp(pa.1, pb.1, t), pa.2, pa.3)
                })
                .collect()
        })
        .collect();
    Glyph { contours, width: lerp(a.width, b.width, t) }
}

fn to_path(g: &Glyph) -> BezPath {
    let mut path = BezPath::new();
    for pts in &g.contours {
        let n = pts.len();
        let Some(start) = pts.iter().position(|p| !p.2) else { continue };
        path.move_to(Point::new(pts[start].0, pts[start].1));
        let mut pending: Vec<Point> = Vec::new();
        for k in 1..=n {
            let p = &pts[(start + k) % n];
            if p.2 {
                pending.push(Point::new(p.0, p.1));
            } else if pending.len() == 2 {
                path.curve_to(pending[0], pending[1], Point::new(p.0, p.1));
                pending.clear();
            } else {
                path.line_to(Point::new(p.0, p.1));
                pending.clear();
            }
        }
        path.close_path();
    }
    path
}

fn points_with_roles(g: &Glyph) -> Vec<(f64, f64, Role)> {
    let mut out = Vec::new();
    for pts in &g.contours {
        for p in pts {
            let role = if p.2 {
                Role::Off
            } else if p.3 {
                Role::Smooth
            } else {
                Role::Corner
            };
            out.push((p.0, p.1, role));
        }
    }
    out
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let format = args.iter().skip(1).find(|a| ["reel", "feed", "wide"].contains(&a.as_str()))
        .map(|s| s.as_str().to_string())
        .unwrap_or_else(|| "reel".to_string());
    let (w, h) = match format.as_str() {
        "feed" => (1080.0, 1350.0),
        "wide" => (1920.0, 1080.0),
        _ => (1080.0, 1920.0),
    };

    let home = env::var("HOME").unwrap();
    let src = PathBuf::from(&home).join("GH/repos/virtua-grotesk/sources");
    let reg_dir = src.join("VirtuaGrotesk-Regular.ufo/glyphs");
    let bold_dir = src.join("VirtuaGrotesk-Bold.ufo/glyphs");

    let regular: Vec<Glyph> = GLYPH_FILES.iter().map(|f| load_glyph(&reg_dir.join(f))).collect();
    let bold: Vec<Glyph> = GLYPH_FILES.iter().map(|f| load_glyph(&bold_dir.join(f))).collect();

    // layout: vertical formats STACK the letters (a horizontal word
    // wastes a 9:16 frame); wide keeps the row. Fit by the BOLD state
    // (the widest/tallest) so the morph never overflows.
    let stacked = format != "wide";
    let max_bold_w = bold.iter().map(|g| g.width).fold(0.0, f64::max);
    let word_units: f64 = bold.iter().map(|g| g.width).sum::<f64>()
        + LETTER_SPACE * (GLYPH_FILES.len() - 1) as f64;
    let n_letters_f = GLYPH_FILES.len() as f64;
    let line_units = 768.0 + 192.0; // cap band + leading, font units
    let scale = if stacked {
        // fill ~88% of height with the stack, capped by width fit
        (h * 0.88 / (line_units * n_letters_f)).min(w * 0.80 / max_bold_w)
    } else {
        w * 0.62 / word_units
    };
    let cap = 768.0 * scale;
    let stack_h = line_units * scale * n_letters_f - 192.0 * scale;
    let baseline_y = (h - cap) / 2.0; // wide: optically center the row

    let frames = (FPS * SECONDS) as usize;
    let mut ctx = Canvas::new(w, h);
    ctx.frame_duration(1.0 / FPS);

    for i in 0..frames {
        if i > 0 {
            ctx.new_page();
        }
        let t = i as f64 / frames as f64;
        ctx.background(Color::rgb(BG.0, BG.1, BG.2));

        // per-frame morph weight: hold Regular, morph to Bold and back
        let morph = ease_in_out_sine(ping_pong(seg(t, 0.55, 0.95)));
        let glyphs: Vec<Glyph> = regular
            .iter()
            .zip(&bold)
            .map(|(r, b)| interp(r, b, morph))
            .collect();

        // per-frame origin (keeps composition centered through the morph)
        let word_now: f64 = glyphs.iter().map(|g| g.width).sum::<f64>()
            + LETTER_SPACE * (glyphs.len() - 1) as f64;
        let origin_x = if stacked {
            0.0 // per-letter x computed in the letter loop
        } else {
            (w - word_now * scale) / 2.0
        };

        // ── grid, in font units under the same transform ──
        // adaptive density: finest power-of-two spacing that keeps grid
        // cells at least ~28 px on screen
        let grid_in = ease_out(seg(t, 0.0, 0.16));
        if grid_in > 0.0 {
            let mut unit = 16.0;
            while unit * scale < 28.0 {
                unit *= 2.0;
            }
            let minor = unit * scale;
            let anchor_x = if stacked { w / 2.0 } else { origin_x };
            let ox = anchor_x % minor;
            let oy = baseline_y % minor;
            let mut k = 0usize;
            let mut gx = ox - minor;
            while gx < w {
                let u = (((gx - anchor_x) / scale).round() as i64).rem_euclid(256);
                let c = if u == 0 { 66 } else if u % 64 == 0 { 44 } else { 24 };
                let reveal = ease_out(stagger(grid_in, k, 40, 0.85));
                let cc = (c as f64 * reveal) as u8;
                ctx.stroke(Color::rgb(cc, cc, cc));
                ctx.stroke_width(1.0);
                ctx.line(gx, 0.0, gx, h);
                gx += minor;
                k += 1;
            }
            let mut k = 0usize;
            let mut gy = oy - minor;
            while gy < h {
                let u = (((gy - baseline_y) / scale).round() as i64).rem_euclid(256);
                let c = if u == 0 { 66 } else if u % 64 == 0 { 44 } else { 24 };
                let reveal = ease_out(stagger(grid_in, k, 40, 0.85));
                let cc = (c as f64 * reveal) as u8;
                ctx.stroke(Color::rgb(cc, cc, cc));
                ctx.stroke_width(1.0);
                ctx.line(0.0, gy, w, gy);
                gy += minor;
                k += 1;
            }
        }

        // ── letters: outline arrives, then points pop ──
        let mut cursor = origin_x;
        let n_letters = glyphs.len();
        let stack_top = (h + stack_h) / 2.0 - cap; // baseline of line 0
        for (li, g) in glyphs.iter().enumerate() {
            let arrive = ease_out_back(stagger(seg(t, 0.14, 0.42), li, n_letters, 0.45));
            let pop_stage = seg(t, 0.40, 0.58);
            if arrive <= 0.0 {
                cursor += (g.width + LETTER_SPACE) * scale;
                continue;
            }
            let s = scale * lerp(0.92, 1.0, arrive);
            let rise = (1.0 - arrive) * 40.0; // eased slide-up, px
            let (lx, ly) = if stacked {
                (
                    (w - g.width * scale) / 2.0,
                    stack_top - li as f64 * line_units * scale,
                )
            } else {
                (cursor, baseline_y)
            };
            let tf = Affine::translate((lx, ly - rise)) * Affine::scale(s);

            let path = tf * to_path(g);
            let alpha = arrive.min(1.0);
            let oc = |v: u8| (v as f64 * alpha) as u8;
            ctx.no_fill();
            ctx.stroke(Color::rgb(oc(OUTLINE.0), oc(OUTLINE.1), oc(OUTLINE.2)));
            ctx.stroke_width(3.0);
            ctx.draw_path(path);

            // points in the runebender palette
            let pts = points_with_roles(g);
            let np = pts.len();
            for (k, (px, py, role)) in pts.iter().enumerate() {
                let pop = ease_out_back(stagger(pop_stage, k, np, 0.75));
                if pop <= 0.0 {
                    continue;
                }
                let p = tf * Point::new(*px, *py);
                let (r, gg, b) = match role {
                    Role::Smooth => SMOOTH,
                    Role::Corner => CORNER,
                    Role::Off => OFFCURVE,
                };
                let size = 7.0 * pop;
                ctx.no_stroke();
                ctx.fill(Color::rgb(r, gg, b));
                match role {
                    Role::Corner => {
                        ctx.rect(p.x - size, p.y - size, size * 2.0, size * 2.0)
                    }
                    _ => ctx.oval(p.x - size, p.y - size, size * 2.0, size * 2.0),
                };
            }
            cursor += (g.width + LETTER_SPACE) * scale;
        }
    }

    let renderer = Renderer::new(w as u32, h as u32);
    renderer
        .render_to_mp4(&ctx, "grid-as-dataset.mp4")
        .expect("mp4 render (needs ffmpeg)");
    println!("rendered {} frames ({format}, {}x{})", ctx.page_count(), w, h);
}
