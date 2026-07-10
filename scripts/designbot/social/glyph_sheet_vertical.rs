// Social animation — single-glyph dimension sheet, VERTICAL.
// The OG sheet re-composed for portrait aspect ratios: one glyph in the
// full spec treatment (grid, metric tags, dimension row, hatched side
// bearings), morphing Regular <-> Bold on the same seamless dwell loop
// as og_dimension_sheet.rs. One font unit = one pixel at 1080 wide.
//
//   designbot --render scripts/designbot/social/glyph_sheet_vertical.rs \
//       --output documentation/assets/social/video/glyph-sheet-reel.mp4 -- reel
//   (formats: reel = 1080x1920, feed = 1080x1350)
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

const GLYPH: &str = "G_";

fn main() {
    let format = std::env::args().nth(1).unwrap_or_else(|| "reel".to_string());
    let (w, h): (f64, f64) = match format.as_str() {
        "reel" => (1080.0, 1920.0),
        "feed" => (1080.0, 1350.0),
        other => panic!("unknown format {other:?} (use reel|feed)"),
    };

    let home = std::env::var("HOME").unwrap();
    let reg = std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo/glyphs")
        .join(format!("{GLYPH}.glif"));
    let bold = std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Bold.ufo/glyphs")
        .join(format!("{GLYPH}.glif"));
    let mono_path = format!("{home}/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf");

    let raw_reg = load_raw(&reg);
    let raw_bold = load_raw(&bold);

    let mut renderer = Renderer::new(w as u32, h as u32);
    let mono = load_family(&mut renderer, &mono_path);
    let mut sheet = Sheet {
        ctx: Canvas::new(w, h),
        renderer: &renderer,
        mono,
    };
    sheet.ctx.frame_duration(1.0 / FPS);

    // ── static vertical layout: one cell, sized to the Bold advance ──
    let cell = raw_bold.1; // multiple of 8; G_ is 832 = 52 whole grid cells
    let grid_left = ((w - cell) / 2.0).round();
    let grid_right = grid_left + cell;

    let header_rule_y = h - 96.0;
    let footer_rule_y = 128.0;
    // content block: dimension-row hatch bottom (baseline-134) up to the
    // overshoot tag top (baseline+832); center it between the rules
    let avail = header_rule_y - footer_rule_y;
    let baseline_y = (footer_rule_y + (avail - 966.0) / 2.0 + 134.0).round();
    let grid_top = baseline_y + 784.0;
    let grid_bottom = baseline_y - 80.0;
    let row_y = baseline_y - 120.0;

    let frames = (FPS * SECONDS_PER_LOOP) as usize * LOOPS;
    for frame in 0..frames {
        if frame > 0 {
            sheet.ctx.new_page();
        }
        // seamless loop with dwells, identical to the OG sheet
        let phase = (frame as f64 / frames as f64) * LOOPS as f64;
        let t = phase.fract();
        let ease = |u: f64| (1.0 - (std::f64::consts::PI * u.clamp(0.0, 1.0)).cos()) / 2.0;
        let half = 0.5 - DWELL;
        let morph = if t < DWELL {
            0.0
        } else if t < DWELL + half {
            ease((t - DWELL) / half)
        } else if t < 0.5 + DWELL {
            1.0
        } else {
            1.0 - ease((t - 0.5 - DWELL) / half)
        };
        let weight_now = 400.0 + 300.0 * morph;

        let o = build_outline(&interp_raw(&raw_reg, &raw_bold, morph));
        let dx = ((cell - o.width) / 2.0).round(); // center advance in cell
        sheet.ctx.background(bg());

        // ── the 16-unit design grid over the cell ──
        {
            let step = 16.0;
            let ctx = &mut sheet.ctx;
            ctx.no_fill();
            ctx.stroke(grid()).stroke_width(2.5);
            let mut x = grid_left;
            while x <= grid_right {
                ctx.line(x, grid_bottom, x, grid_top);
                x += step;
            }
            let mut y = grid_bottom;
            while y <= grid_top {
                ctx.line(grid_left, y, grid_right, y);
                y += step;
            }
        }

        // ── cell boundaries + vertical metrics ──
        {
            let ctx = &mut sheet.ctx;
            ctx.stroke(blue()).stroke_width(3.5).no_fill();
            ctx.line(grid_left, grid_bottom, grid_left, grid_top);
            ctx.line(grid_right, grid_bottom, grid_right, grid_top);
            ctx.line_dash(&[10.0, 10.0]);
            for y in [784.0, -16.0] {
                ctx.line(grid_left, baseline_y + y, grid_right, baseline_y + y);
            }
            ctx.line_dash(&[]);
            for y in [768.0, 576.0, 0.0] {
                ctx.line(grid_left, baseline_y + y, grid_right, baseline_y + y);
            }
        }

        // ── the glyph: fill + contour, then handles and point markers ──
        sheet.ctx.fill(red_fill()).stroke(red()).stroke_width(3.5);
        sheet
            .ctx
            .draw_path(Affine::translate((grid_left + dx, baseline_y)) * o.path.clone());
        let (gx, gy) = (grid_left + dx, baseline_y);
        sheet.ctx.stroke(red()).stroke_width(3.5).no_fill();
        for ((x1, y1), (x2, y2)) in &o.handles {
            sheet.ctx.line(gx + x1, gy + y1, gx + x2, gy + y2);
        }
        sheet.ctx.fill(bg()).stroke(red()).stroke_width(3.5);
        for (x, y, role) in &o.points {
            let (px, py) = (gx + x, gy + y);
            match role {
                Role::Smooth => {
                    sheet.ctx.oval(px - 7.0, py - 7.0, 14.0, 14.0);
                }
                Role::Corner => {
                    sheet.ctx.rect(px - 6.0, py - 6.0, 12.0, 12.0);
                }
                Role::Off => {
                    sheet.ctx.oval(px - 7.0, py - 7.0, 14.0, 14.0);
                }
            }
        }

        // ── metric tags, docked inside the cell edges ──
        sheet.metric_tag("CAP 768", grid_left, baseline_y + 768.0, false, -1);
        sheet.metric_tag("X-HEIGHT 576", grid_left, baseline_y + 576.0, true, -1);
        sheet.metric_tag("BASELINE 0", grid_left, baseline_y, true, -1);
        sheet.metric_tag("OVERSHOOT +16", grid_right, baseline_y + 784.0, true, 1);
        sheet.metric_tag("OVERSHOOT -16", grid_right, baseline_y - 16.0, false, 1);

        // ── dimension row: ink width centered, side bearings at the edges ──
        {
            let ink0 = grid_left + dx + o.lsb;
            let ink1 = grid_left + dx + o.width - o.rsb;
            sheet
                .ctx
                .stroke(subdued())
                .stroke_width(3.5)
                .no_fill()
                .line(grid_left, row_y, grid_right, row_y);
            sheet.hatch(grid_left, row_y - 14.0, ink0, row_y + 14.0, red());
            sheet.hatch(ink1, row_y - 14.0, grid_right, row_y + 14.0, red());
            sheet.label_padded(
                &format!("{}", (ink1 - ink0).round()),
                (grid_left + grid_right) / 2.0,
                row_y - 11.0,
                30.0,
                text_bright(),
                0,
            );
            sheet.label(
                &format!("{}", (ink0 - grid_left).round()),
                grid_left + 10.0,
                row_y + 22.0,
                30.0,
                red(),
                -1,
            );
            sheet.label(
                &format!("{}", (grid_right - ink1).round()),
                grid_right - 10.0,
                row_y + 22.0,
                30.0,
                red(),
                1,
            );
        }

        // ── boundary ticks + nodes ──
        for b in [grid_left, grid_right] {
            let tick_end = row_y - 14.0;
            sheet
                .ctx
                .stroke(blue())
                .stroke_width(3.5)
                .no_fill()
                .line(b, grid_bottom, b, tick_end);
            sheet.node(b, tick_end, 6.0);
            for y in [784.0, 768.0, 576.0, 0.0, -16.0] {
                sheet.node(b, baseline_y + y, 6.0);
            }
        }

        // ── header + footer, docked to the cell edges ──
        {
            let ctx = &mut sheet.ctx;
            ctx.stroke(rule()).stroke_width(3.5).no_fill();
            ctx.line(grid_left, header_rule_y, grid_right, header_rule_y);
            ctx.line(grid_left, footer_rule_y, grid_right, footer_rule_y);
        }
        sheet.label("VIRTUA GROTESK", grid_left, header_rule_y + 22.0, 30.0, text_bright(), -1);
        sheet.label("OFL 1.1", grid_right, header_rule_y + 22.0, 30.0, text_bright(), 1);
        sheet.label(
            &format!("POWERS OF TWO GRID / WEIGHT {weight_now:.0} / UPM 1024"),
            grid_left,
            84.0,
            30.0,
            text_bright(),
            -1,
        );
        sheet.label(
            "GITHUB.COM/ELIHEUER/VIRTUA-GROTESK",
            grid_left,
            40.0,
            30.0,
            text_bright(),
            -1,
        );
    } // end frame loop

    let out = format!("glyph-sheet-{format}.mp4");
    renderer
        .render_to_mp4(&sheet.ctx, &out)
        .expect("mp4 render (needs ffmpeg)");
    println!(
        "rendered {} frames -> {out}: {LOOPS} seamless loops of {SECONDS_PER_LOOP}s at {FPS} fps",
        (FPS * SECONDS_PER_LOOP) as usize * LOOPS
    );
}
