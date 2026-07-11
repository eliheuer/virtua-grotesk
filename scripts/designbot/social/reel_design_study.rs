// Social animation — DESIGN STUDY reel. Visual and graphic above all:
// a giant glyph outline with full point structure bleeding off the
// frame, a powers-of-two ladder of small filled repeats running a
// staggered morph wave underneath, and oversized essay text scrolling
// behind as dark texture. Brutalist composition, seamless dwell loop.
//
//   designbot --render scripts/designbot/social/reel_design_study.rs \
//       --output documentation/assets/social/video/design-study-a.mp4 -- a
//   (arg 1: any glyph name present in both masters; default "a")
//
// ORIGINAL HEADER (og.rs):
//
//! Coordinates are DrawBot's (y-up, origin bottom-left), which at this size
//! makes one font unit = one canvas pixel with the baseline at y=324: every
//! font-space coordinate is just BASELINE_Y + value, and the UFO outlines
//! draw with a plain translate. text() anchors the BASELINE at y;
//! rect()/oval() anchor at their bottom-left corner.
//!
//! REBUILD after editing this file (from the elih.net repo root):
//!     cd scripts/virtua-grotesk && cargo run --release --bin og
//!
//! That one command recompiles and overwrites BOTH outputs:
//!     src/content/blog/virtua-grotesk/share-card.png   (post hero)
//!     public/og/virtua-grotesk.png                     (og:image)
//! 
//! Rebuilds take about a second once deps are compiled; reload the post in
//! the browser to see the new card (the Astro dev server serves it as a
//! static asset, no restart needed).
//!
//! Inputs read at render time, from sibling checkouts:
//!     ~/GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo
//!     ~/GH/repos/virtua-grotesk/fonts/variable/VirtuaGrotesk[wght].ttf
//!     ~/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf

use designbot::norad;
use designbot::prelude::*;
use designbot_render::Renderer;
use designbot::kurbo::{Affine, BezPath, Shape};

const FPS: f64 = 30.0;
const SECONDS_PER_LOOP: f64 = 4.0;
const LOOPS: usize = 4;
// fraction of each loop spent holding at each weight extreme, so the
// 400 and 700 states are actually readable before the morph moves on
const DWELL: f64 = 0.18;


// Theme tokens
fn bg() -> Color {
    Color::rgb(0x10, 0x10, 0x10)
}
fn grid() -> Color {
    // dark gray, so the graph paper sits well behind the drawing
    Color::rgb(0x32, 0x32, 0x32)
}
fn rule() -> Color {
    Color::rgb(0x14, 0xd6, 0x7e)
}
fn text_bright() -> Color {
    Color::rgb(0x14, 0xd6, 0x7e)
}
fn subdued() -> Color {
    Color::rgb(0x14, 0xd6, 0x7e)
}
fn red() -> Color {
    Color::rgb(0xff, 0x3a, 0x28)
}
fn blue() -> Color {
    Color::rgb(0x5c, 0x86, 0xff)
}
fn red_fill() -> Color {
    // the mark red at ~40%, so grid and construction lines read through
    Color::rgba(0xff, 0x3a, 0x28, 64)
}

// --- minimal sfnt reader (family name for ctx.font()) ----------------------

fn read_u16(data: &[u8], offset: usize) -> u16 {
    u16::from_be_bytes([data[offset], data[offset + 1]])
}

fn read_u32(data: &[u8], offset: usize) -> u32 {
    u32::from_be_bytes([
        data[offset],
        data[offset + 1],
        data[offset + 2],
        data[offset + 3],
    ])
}

fn find_table(data: &[u8], tag: &[u8; 4]) -> Option<usize> {
    let num_tables = read_u16(data, 4) as usize;
    (0..num_tables)
        .map(|i| 12 + i * 16)
        .find(|&rec| &data[rec..rec + 4] == tag)
        .map(|rec| read_u32(data, rec + 8) as usize)
}

/// Load the font into the renderer and return its Windows-platform family
/// name (id 16 falling back to 1) for ctx.font().
fn load_family(renderer: &mut Renderer, path: &str) -> String {
    let data = std::fs::read(path).unwrap_or_else(|e| panic!("read {path}: {e}"));
    renderer
        .load_font(path)
        .unwrap_or_else(|e| panic!("load {path}: {e:?}"));
    let name = find_table(&data, b"name").expect("no name table");
    let count = read_u16(&data, name + 2) as usize;
    let string_off = name + read_u16(&data, name + 4) as usize;
    for want in [16u16, 1] {
        for i in 0..count {
            let rec = name + 6 + i * 12;
            if read_u16(&data, rec) == 3 && read_u16(&data, rec + 6) == want {
                let len = read_u16(&data, rec + 8) as usize;
                let off = string_off + read_u16(&data, rec + 10) as usize;
                let units: Vec<u16> = data[off..off + len]
                    .chunks_exact(2)
                    .map(|c| u16::from_be_bytes([c[0], c[1]]))
                    .collect();
                return String::from_utf16_lossy(&units);
            }
        }
    }
    panic!("no Windows family name record in {path}");
}

// --- UFO outlines -----------------------------------------------------------

/// Point roles, drawn as red-outlined markers knocked out with the background
/// color: smooth = circle, corner = square, off-curve = small circle.
#[derive(Clone, Copy)]
enum Role {
    Smooth,
    Corner,
    Off,
}

struct Outline {
    path: BezPath, // font units, y-up, same as the canvas
    points: Vec<(f64, f64, Role)>,
    handles: Vec<((f64, f64), (f64, f64))>, // on-curve anchor -> off-curve
    width: f64,
    lsb: f64,
    rsb: f64,
}

type RawContours = Vec<Vec<(f64, f64, norad::PointType, bool)>>;

fn load_raw(glif: &std::path::Path) -> (RawContours, f64) {
    let glyph = norad::Glyph::load(glif).expect("failed to load glif");
    let contours = glyph
        .contours
        .iter()
        .map(|c| c.points.iter().map(|p| (p.x, p.y, p.typ.clone(), p.smooth)).collect())
        .collect();
    (contours, glyph.width)
}

/// Interpolate two point-compatible raw glyphs (types from `a`).
fn interp_raw(a: &(RawContours, f64), b: &(RawContours, f64), t: f64) -> (RawContours, f64) {
    let contours = a
        .0
        .iter()
        .zip(&b.0)
        .map(|(ca, cb)| {
            ca.iter()
                .zip(cb)
                .map(|(pa, pb)| {
                    (lerp(pa.0, pb.0, t), lerp(pa.1, pb.1, t), pa.2.clone(), pa.3)
                })
                .collect()
        })
        .collect();
    (contours, lerp(a.1, b.1, t))
}

fn build_outline(raw: &(RawContours, f64)) -> Outline {
    let mut path = BezPath::new();
    let mut points = Vec::new();
    let mut handles = Vec::new();
    for pts in &raw.0 {
        use norad::PointType::*;
        let n = pts.len();
        let Some(start) = pts.iter().position(|p| p.2 != OffCurve) else {
            continue;
        };
        let sp = &pts[start];
        path.move_to((sp.0, sp.1));
        let role = if sp.3 { Role::Smooth } else { Role::Corner };
        points.push((sp.0, sp.1, role));
        let mut prev_on = (sp.0, sp.1);
        let mut pending: Vec<(f64, f64)> = Vec::new();
        for k in 1..=n {
            let p = &pts[(start + k) % n];
            match p.2 {
                OffCurve => {
                    pending.push((p.0, p.1));
                    points.push((p.0, p.1, Role::Off));
                }
                Curve if pending.len() == 2 => {
                    path.curve_to(pending[0], pending[1], (p.0, p.1));
                    handles.push((prev_on, pending[0]));
                    handles.push(((p.0, p.1), pending[1]));
                    pending.clear();
                    prev_on = (p.0, p.1);
                    if k != n {
                        let role = if p.3 { Role::Smooth } else { Role::Corner };
                        points.push((p.0, p.1, role));
                    }
                }
                _ => {
                    path.line_to((p.0, p.1));
                    pending.clear();
                    prev_on = (p.0, p.1);
                    if k != n {
                        let role = if p.3 { Role::Smooth } else { Role::Corner };
                        points.push((p.0, p.1, role));
                    }
                }
            }
        }
        path.close_path();
    }
    let bounds = path.bounding_box();
    Outline {
        lsb: bounds.x0,
        rsb: raw.1 - bounds.x1,
        path,
        points,
        handles,
        width: raw.1,
    }
}

// --- drawing helpers ----------------------------------------------------------

struct Sheet<'a> {
    ctx: Canvas,
    renderer: &'a Renderer,
    mono: String,
}

impl Sheet<'_> {
    fn mono_width(&self, txt: &str, size: f64) -> f64 {
        self.renderer.text_width(txt, Some(&self.mono), size, &[])
    }

    /// Mono label with its baseline at y. align: -1 left, 0 center, 1 right.
    fn label(&mut self, txt: &str, x: f64, y: f64, size: f64, color: Color, align: i8) {
        let w = self.mono_width(txt, size);
        let x = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        self.ctx
            .font(&self.mono)
            .clear_font_variations()
            .font_size(size)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    /// Label over a background patch so it stays legible on the grid.
    fn label_padded(&mut self, txt: &str, x: f64, y: f64, size: f64, color: Color, align: i8) {
        let w = self.mono_width(txt, size);
        let pad = 10.0;
        let x0 = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        self.ctx.no_stroke().fill(bg());
        self.ctx
            .rect(x0 - pad, y - size * 0.28, w + pad * 2.0, size * 1.14);
        self.label(txt, x0, y, size, color, -1);
    }

    /// Metric-line tag: a background-filled, blue-outlined box snapped to the
    /// 16-unit grid (32 high, width in whole cells), floating one grid unit
    /// off the line at y_line (above or below it), with the text optically
    /// centered. x_edge must be a grid line; align -1 grows the box
    /// rightward, 1 leftward.
    fn metric_tag(&mut self, txt: &str, x_edge: f64, y_line: f64, above: bool, align: i8) {
        let size = 30.0;
        let w = self.mono_width(txt, size);
        let box_w = ((w + 16.0) / 16.0).ceil() * 16.0;
        let box_h = 32.0;
        let x0 = if align < 0 { x_edge } else { x_edge - box_w };
        let y0 = if above {
            y_line + 16.0
        } else {
            y_line - box_h - 16.0
        };
        self.ctx.fill(bg()).stroke(blue()).stroke_width(3.5);
        self.ctx.rect(x0, y0, box_w, box_h);
        // Geist Mono caps/figures are ~0.73 em tall; center that ink box
        let baseline = y0 + (box_h - 0.73 * size) / 2.0;
        self.label(txt, x0 + box_w / 2.0, baseline, size, blue(), 0);
    }

    /// 45-degree hatching clipped to a rect, Replica side-bearing style.
    fn hatch(&mut self, x0: f64, y0: f64, x1: f64, y1: f64, color: Color) {
        let h = y1 - y0;
        self.ctx.stroke(color).stroke_width(3.5).no_fill();
        let step = 6.0;
        let mut t = x0 - h;
        while t < x1 {
            // segment from (t, y0) to (t + h, y1), clipped to [x0, x1]
            let sx = t.max(x0);
            let ex = (t + h).min(x1);
            if ex > sx {
                self.ctx.line(sx, y0 + (sx - t), ex, y0 + (ex - t));
            }
            t += step;
        }
    }

    /// Small circle node at a blue-line crossing, knocked out with the
    /// background color like the point markers.
    fn node(&mut self, x: f64, y: f64, r: f64) {
        self.ctx.fill(bg()).stroke(blue()).stroke_width(3.5);
        self.ctx.oval(x - r, y - r, r * 2.0, r * 2.0);
    }
}

const W: f64 = 1080.0;
const H: f64 = 1920.0;

fn ticker_gray() -> Color {
    Color::rgb(0x26, 0x26, 0x26)
}

/// The dwell loop curve: hold 0, sine-ease to 1, hold 1, sine-ease back.
fn dwell_morph(t: f64) -> f64 {
    let t = t.rem_euclid(1.0);
    let ease = |u: f64| (1.0 - (std::f64::consts::PI * u.clamp(0.0, 1.0)).cos()) / 2.0;
    let half = 0.5 - DWELL;
    if t < DWELL {
        0.0
    } else if t < DWELL + half {
        ease((t - DWELL) / half)
    } else if t < 0.5 + DWELL {
        1.0
    } else {
        1.0 - ease((t - 0.5 - DWELL) / half)
    }
}

fn main() {
    let glyph = std::env::args().nth(1).unwrap_or_else(|| "a".to_string());

    let home = std::env::var("HOME").unwrap();
    let reg = std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo/glyphs")
        .join(format!("{glyph}.glif"));
    let bold = std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Bold.ufo/glyphs")
        .join(format!("{glyph}.glif"));
    let mono_path = format!("{home}/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf");
    let virtua_path = format!("{home}/GH/repos/virtua-grotesk/fonts/variable/VirtuaGrotesk[wght].ttf");

    let raw_reg = load_raw(&reg);
    let raw_bold = load_raw(&bold);

    let mut renderer = Renderer::new(W as u32, H as u32);
    let mono = load_family(&mut renderer, &mono_path);
    let virtua = load_family(&mut renderer, &virtua_path);
    let mut sheet = Sheet {
        ctx: Canvas::new(W, H),
        renderer: &renderer,
        mono,
    };
    sheet.ctx.frame_duration(1.0 / FPS);

    // ticker copy, adapted from the essay — texture, not prose
    let ticker_top = "A FONT IS A PROGRAM ";
    let ticker_bottom = "THE DATASET IS THE SOURCE CODE ";
    let wght_tag = u32::from_be_bytes(*b"wght");

    let frames = (FPS * SECONDS_PER_LOOP) as usize * LOOPS;
    for frame in 0..frames {
        if frame > 0 {
            sheet.ctx.new_page();
        }
        let phase = (frame as f64 / frames as f64) * LOOPS as f64;
        let t = phase.fract(); // one loop, 0..1
        let morph = dwell_morph(t);
        let weight_now = 400.0 + 300.0 * morph;

        sheet.ctx.background(bg());

        // ── scrolling essay text, oversized, dark-on-dark texture ──
        // linear scroll of exactly one copy-width per loop = seamless
        {
            let vars = [(wght_tag, 700.0f32)];
            for (txt, size, y, dir) in [
                (ticker_top, 300.0, 1400.0, -1.0),
                (ticker_bottom, 170.0, 190.0, 1.0),
            ] {
                let tw = sheet
                    .renderer
                    .text_width(txt, Some(&virtua), size, &vars);
                let off = (t * tw * dir).rem_euclid(tw);
                sheet
                    .ctx
                    .font(&virtua)
                    .clear_font_variations()
                    .font_variation("wght", 700.0)
                    .font_size(size)
                    .fill(ticker_gray())
                    .text_align(TextAlign::Left);
                let mut x = -off;
                while x < W {
                    sheet.ctx.text(txt, x, y);
                    x += tw;
                }
            }
        }

        // ── hero: giant outline with point structure, bleeding the frame ──
        let hero = build_outline(&interp_raw(&raw_reg, &raw_bold, morph));
        {
            let scale = 1.9;
            let gx = (W - hero.width * scale) / 2.0;
            let gy = 620.0; // baseline; x-height glyphs run to ~1715px
            let tr = Affine::translate((gx, gy)) * Affine::scale(scale);

            sheet.ctx.fill(red_fill()).stroke(red()).stroke_width(5.0);
            sheet.ctx.draw_path(tr * hero.path.clone());

            sheet.ctx.stroke(red()).stroke_width(4.0).no_fill();
            for ((x1, y1), (x2, y2)) in &hero.handles {
                sheet.ctx.line(
                    gx + x1 * scale,
                    gy + y1 * scale,
                    gx + x2 * scale,
                    gy + y2 * scale,
                );
            }
            sheet.ctx.fill(bg()).stroke(red()).stroke_width(4.0);
            for (x, y, role) in &hero.points {
                let (px, py) = (gx + x * scale, gy + y * scale);
                match role {
                    Role::Smooth => {
                        sheet.ctx.oval(px - 12.0, py - 12.0, 24.0, 24.0);
                    }
                    Role::Corner => {
                        sheet.ctx.rect(px - 11.0, py - 11.0, 22.0, 22.0);
                    }
                    Role::Off => {
                        sheet.ctx.oval(px - 12.0, py - 12.0, 24.0, 24.0);
                    }
                }
            }
        }

        // ── powers-of-two ladder: filled repeats, staggered morph wave ──
        {
            let base_y = 320.0;
            let mut x = 72.0;
            for (i, s) in [0.0625, 0.125, 0.25, 0.5].iter().enumerate() {
                // each rung runs the same loop, offset in time
                let m = dwell_morph(t - 0.1 * (i as f64 + 1.0));
                let o = build_outline(&interp_raw(&raw_reg, &raw_bold, m));
                let tr = Affine::translate((x, base_y)) * Affine::scale(*s);
                sheet.ctx.fill(red()).no_stroke();
                sheet.ctx.draw_path(tr * o.path.clone());
                x += o.width * s + 48.0;
            }
        }

        // ── minimal spec accents ──
        {
            let ctx = &mut sheet.ctx;
            ctx.stroke(rule()).stroke_width(3.5).no_fill();
            ctx.line(72.0, H - 96.0, W - 72.0, H - 96.0);
            ctx.line(72.0, 112.0, W - 72.0, 112.0);
        }
        sheet.label("VIRTUA GROTESK", 72.0, H - 74.0, 30.0, text_bright(), -1);
        sheet.label(
            &format!("WGHT {weight_now:.0}"),
            W - 72.0,
            H - 74.0,
            30.0,
            text_bright(),
            1,
        );
        sheet.label("GRID AS DATASET", 72.0, 64.0, 30.0, text_bright(), -1);
        sheet.label("ELIH.NET", W - 72.0, 64.0, 30.0, text_bright(), 1);
    } // end frame loop

    let out = format!("design-study-{glyph}.mp4");
    renderer
        .render_to_mp4(&sheet.ctx, &out)
        .expect("mp4 render (needs ffmpeg)");
    println!(
        "rendered {frames} frames -> {out}: {LOOPS} seamless loops of {SECONDS_PER_LOOP}s at {FPS} fps"
    );
}
