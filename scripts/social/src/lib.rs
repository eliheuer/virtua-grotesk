//! Shared drawing mechanics for the DesignBot social compositions.
//!
//! PORTABLE CORE: this file names no specific font project; retargeting is done
//! entirely in `inputs.rs`. See the README's "Reusing in another repo" section.
//!
//! This mirrors the blog-figure crate's `lib.rs`
//! (`~/GH/repos/elih.net/scripts/virtua-grotesk/src/lib.rs`) but is
//! parameterized by a [`Format`] so one code base can render the square,
//! vertical, and carousel canvases natively instead of letterboxing the fixed
//! 2520x1320 blog card. Visual decisions live in `style.rs`; the reviewed
//! section-03 technical-drawing language lives in `technical.rs`; content and
//! layout live in `src/bin/*.rs`.
//!
//! POINT LANGUAGE (drawn, not told):
//!   - circle = smooth on-curve, square = corner, small circle = off-curve
//!   - GREEN  = on the 8-unit machine grid
//!   - RED    = off 8, on the 2-unit human grid: an optical correction

use designbot::prelude::*;
use designbot_render::Renderer;
use kurbo::{Affine, BezPath, Shape};
use std::path::Path;

pub mod inputs;
pub mod style;
pub mod technical;
pub use style::*;
pub use technical::*;

/// Handle lengths worth calling out (high 2-adic valuation / stem-adjacent).
pub const FAVORED: [f64; 7] = [64.0, 96.0, 128.0, 160.0, 192.0, 224.0, 256.0];

// --- social canvas formats ---------------------------------------------------

/// A native social canvas. Each format owns its pixel size and outer margin so
/// compositions are drawn at the real aspect ratio, never letterboxed.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Format {
    /// Instagram carousel / portrait feed slide.
    Carousel,
    /// Square X / LinkedIn / Instagram card, also the square animation master.
    Square,
    /// Vertical Instagram / TikTok reel & story (9:16).
    Vertical,
}

impl Format {
    pub fn size(self) -> (f64, f64) {
        match self {
            Format::Carousel => (1080.0, 1350.0),
            Format::Square => (2048.0, 2048.0),
            Format::Vertical => (1080.0, 1920.0),
        }
    }
    pub fn w(self) -> f64 {
        self.size().0
    }
    pub fn h(self) -> f64 {
        self.size().1
    }
    pub fn margin(self) -> f64 {
        match self {
            Format::Carousel => 72.0,
            Format::Square => 128.0,
            Format::Vertical => 72.0,
        }
    }
}

// --- color-managed PNG output ------------------------------------------------
//
// Copied verbatim from the blog-figure crate per its README handoff rule: when
// these renderers seed social assets, the sRGB tagging guardrail travels with
// them. DesignBot emits valid pixels but no color-space chunk; an untagged RGB
// PNG is device-dependent, so a social ingestion pipeline may guess wrong when
// it recompresses. Authoring is 8-bit sRGB; we tag that fact.

fn tag_png_as_srgb(path: &Path) {
    const SIGNATURE: &[u8; 8] = b"\x89PNG\r\n\x1a\n";
    const SRGB_GAMMA: u32 = 45_455;
    const SRGB_CHROMATICITIES: [u32; 8] = [
        31_270, 32_900, 64_000, 33_000, 30_000, 60_000, 15_000, 6_000,
    ];

    fn chunk(bytes: &[u8], name: &[u8; 4]) -> Option<(usize, usize)> {
        let mut offset = 8;
        while offset + 12 <= bytes.len() {
            let length =
                u32::from_be_bytes(bytes[offset..offset + 4].try_into().unwrap()) as usize;
            let end = offset + 12 + length;
            assert!(end <= bytes.len(), "truncated PNG chunk in generated image");
            if &bytes[offset + 4..offset + 8] == name {
                return Some((offset, end));
            }
            offset = end;
        }
        None
    }

    fn push_chunk(out: &mut Vec<u8>, name: &[u8; 4], data: &[u8]) {
        out.extend_from_slice(&(data.len() as u32).to_be_bytes());
        out.extend_from_slice(name);
        out.extend_from_slice(data);
        let mut crc = crc32fast::Hasher::new();
        crc.update(name);
        crc.update(data);
        out.extend_from_slice(&crc.finalize().to_be_bytes());
    }

    let bytes = std::fs::read(path).unwrap();
    assert_eq!(&bytes[..8], SIGNATURE, "renderer did not produce a PNG");
    if chunk(&bytes, b"sRGB").is_some() {
        return;
    }
    let (_, ihdr_end) = chunk(&bytes, b"IHDR").expect("generated PNG has no IHDR chunk");
    let mut tagged = Vec::with_capacity(bytes.len() + 96);
    tagged.extend_from_slice(&bytes[..ihdr_end]);
    push_chunk(&mut tagged, b"sRGB", &[1]); // relative colorimetric
    push_chunk(&mut tagged, b"gAMA", &SRGB_GAMMA.to_be_bytes());
    let chromaticities: Vec<u8> = SRGB_CHROMATICITIES
        .into_iter()
        .flat_map(u32::to_be_bytes)
        .collect();
    push_chunk(&mut tagged, b"cHRM", &chromaticities);
    tagged.extend_from_slice(&bytes[ihdr_end..]);
    std::fs::write(path, tagged).unwrap();
}

/// Render a PNG and normalize its color metadata. All output goes through here.
pub fn write_png(renderer: &Renderer, ctx: &Canvas, out: &Path) {
    std::fs::create_dir_all(out.parent().unwrap()).unwrap();
    renderer
        .render_to_png(ctx, out.to_str().unwrap())
        .unwrap();
    tag_png_as_srgb(out);
}

// --- easing ------------------------------------------------------------------

pub fn lerp(a: f64, b: f64, t: f64) -> f64 {
    a + (b - a) * t
}

/// Classic ease-in-out-sine on [0,1].
pub fn ease_in_out_sine(t: f64) -> f64 {
    -(f64::cos(std::f64::consts::PI * t) - 1.0) / 2.0
}

/// A 0..1 ping-pong ramp with eased ends, for seamless loops. At phase 0 and 1
/// the value is 0; at phase 0.5 it is 1, with matched velocity at the seam.
pub fn loop_pingpong(phase: f64) -> f64 {
    let tri = 1.0 - (2.0 * phase - 1.0).abs(); // 0->1->0 triangle
    -(f64::cos(std::f64::consts::PI * tri) - 1.0) / 2.0
}

// --- UFO outline loading, components resolved --------------------------------

#[derive(Clone, Copy, PartialEq)]
pub enum PtRole {
    Smooth,
    Corner,
    Off,
}

#[derive(Clone)]
pub struct Outline {
    pub path: BezPath,
    pub points: Vec<(f64, f64, PtRole)>,
    pub handles: Vec<((f64, f64), (f64, f64))>,
    pub width: f64,
}

/// UFO3 glif filename: every uppercase letter gets an underscore suffix.
pub fn glif_name(glyph: &str) -> String {
    let mut s = String::new();
    for c in glyph.chars() {
        s.push(c);
        if c.is_uppercase() {
            s.push('_');
        }
    }
    s + ".glif"
}

fn push_on_curve(points: &mut Vec<(f64, f64, PtRole)>, p: &norad::ContourPoint, k: usize, n: usize) {
    if k == n {
        return;
    }
    let role = if p.smooth {
        PtRole::Smooth
    } else {
        PtRole::Corner
    };
    points.push((p.x, p.y, role));
}

/// Load a glyph's outline with components resolved recursively.
pub fn load_outline(glyphs_dir: &Path, name: &str) -> Outline {
    let glif = glyphs_dir.join(glif_name(name));
    let glyph = norad::Glyph::load(&glif).unwrap_or_else(|e| panic!("load {glif:?}: {e}"));
    outline_from_glyph(&glyph, glyphs_dir)
}

fn outline_from_glyph(glyph: &norad::Glyph, glyphs_dir: &Path) -> Outline {
    let mut path = BezPath::new();
    let mut points = Vec::new();
    let mut handles = Vec::new();
    for contour in &glyph.contours {
        use norad::PointType::*;
        let pts = &contour.points;
        let n = pts.len();
        let Some(start) = pts.iter().position(|p| p.typ != OffCurve) else {
            continue;
        };
        let sp = &pts[start];
        path.move_to((sp.x, sp.y));
        let role = if sp.smooth {
            PtRole::Smooth
        } else {
            PtRole::Corner
        };
        points.push((sp.x, sp.y, role));
        let mut prev_on = (sp.x, sp.y);
        let mut pending: Vec<(f64, f64)> = Vec::new();
        for k in 1..=n {
            let p = &pts[(start + k) % n];
            match p.typ {
                OffCurve => {
                    pending.push((p.x, p.y));
                    points.push((p.x, p.y, PtRole::Off));
                }
                Curve if pending.len() == 2 => {
                    path.curve_to(pending[0], pending[1], (p.x, p.y));
                    handles.push((prev_on, pending[0]));
                    handles.push(((p.x, p.y), pending[1]));
                    pending.clear();
                    prev_on = (p.x, p.y);
                    push_on_curve(&mut points, p, k, n);
                }
                _ => {
                    path.line_to((p.x, p.y));
                    pending.clear();
                    prev_on = (p.x, p.y);
                    push_on_curve(&mut points, p, k, n);
                }
            }
        }
        path.close_path();
    }
    for comp in &glyph.components {
        let sub = load_outline(glyphs_dir, comp.base.as_ref());
        let t = &comp.transform;
        let aff = Affine::new([
            t.x_scale, t.xy_scale, t.yx_scale, t.y_scale, t.x_offset, t.y_offset,
        ]);
        path.extend(aff * sub.path);
        let map = |x: f64, y: f64| {
            (
                t.x_scale * x + t.yx_scale * y + t.x_offset,
                t.xy_scale * x + t.y_scale * y + t.y_offset,
            )
        };
        for (x, y, r) in sub.points {
            let (nx, ny) = map(x, y);
            points.push((nx, ny, r));
        }
        for ((ax, ay), (hx, hy)) in sub.handles {
            handles.push((map(ax, ay), map(hx, hy)));
        }
    }
    Outline {
        path,
        points,
        handles,
        width: glyph.width,
    }
}

// --- raw glyph for master interpolation --------------------------------------
//
// The technical drawing needs the interpolated *point structure* (so the point
// language and handles animate too), not just a filled path. Regular and Bold
// are interpolation-compatible masters, so we interpolate contour-point by
// contour-point and rebuild an `Outline`.

#[derive(Clone)]
pub struct RawPt {
    pub x: f64,
    pub y: f64,
    pub off: bool,
    pub smooth: bool,
}

#[derive(Clone)]
pub struct RawGlyph {
    pub contours: Vec<Vec<RawPt>>,
    pub width: f64,
}

pub fn load_raw(glyphs_dir: &Path, name: &str) -> RawGlyph {
    let glif = glyphs_dir.join(glif_name(name));
    let glyph = norad::Glyph::load(&glif).unwrap_or_else(|e| panic!("load {glif:?}: {e}"));
    let contours = glyph
        .contours
        .iter()
        .map(|c| {
            c.points
                .iter()
                .map(|p| RawPt {
                    x: p.x,
                    y: p.y,
                    off: p.typ == norad::PointType::OffCurve,
                    smooth: p.smooth,
                })
                .collect()
        })
        .collect();
    RawGlyph {
        contours,
        width: glyph.width,
    }
}

/// Interpolate two point-compatible masters. Panics loudly on a mismatch so a
/// non-compatible glyph pair never renders a silently wrong morph.
pub fn interp_raw(a: &RawGlyph, b: &RawGlyph, t: f64) -> RawGlyph {
    assert_eq!(
        a.contours.len(),
        b.contours.len(),
        "masters have different contour counts"
    );
    let contours = a
        .contours
        .iter()
        .zip(&b.contours)
        .map(|(ca, cb)| {
            assert_eq!(ca.len(), cb.len(), "contour point counts differ");
            ca.iter()
                .zip(cb)
                .map(|(pa, pb)| RawPt {
                    x: lerp(pa.x, pb.x, t),
                    y: lerp(pa.y, pb.y, t),
                    off: pa.off,
                    smooth: pa.smooth,
                })
                .collect()
        })
        .collect();
    RawGlyph {
        contours,
        width: lerp(a.width, b.width, t),
    }
}

impl RawGlyph {
    /// Convert to an `Outline` (path + point language + handles), same walk as
    /// [`load_outline`] but from raw points. Assumes no components.
    pub fn to_outline(&self) -> Outline {
        let mut path = BezPath::new();
        let mut points = Vec::new();
        let mut handles = Vec::new();
        for pts in &self.contours {
            let n = pts.len();
            let Some(start) = pts.iter().position(|p| !p.off) else {
                continue;
            };
            let sp = &pts[start];
            path.move_to((sp.x, sp.y));
            let role = if sp.smooth {
                PtRole::Smooth
            } else {
                PtRole::Corner
            };
            points.push((sp.x, sp.y, role));
            let mut prev_on = (sp.x, sp.y);
            let mut pending: Vec<(f64, f64)> = Vec::new();
            for k in 1..=n {
                let p = &pts[(start + k) % n];
                if p.off {
                    pending.push((p.x, p.y));
                    points.push((p.x, p.y, PtRole::Off));
                } else if pending.len() == 2 {
                    path.curve_to(pending[0], pending[1], (p.x, p.y));
                    handles.push((prev_on, pending[0]));
                    handles.push(((p.x, p.y), pending[1]));
                    pending.clear();
                    prev_on = (p.x, p.y);
                    if k != n {
                        let r = if p.smooth {
                            PtRole::Smooth
                        } else {
                            PtRole::Corner
                        };
                        points.push((p.x, p.y, r));
                    }
                } else {
                    path.line_to((p.x, p.y));
                    pending.clear();
                    prev_on = (p.x, p.y);
                    if k != n {
                        let r = if p.smooth {
                            PtRole::Smooth
                        } else {
                            PtRole::Corner
                        };
                        points.push((p.x, p.y, r));
                    }
                }
            }
            path.close_path();
        }
        Outline {
            path,
            points,
            handles,
            width: self.width,
        }
    }
}

// --- sfnt family-name reader -------------------------------------------------

fn read_u16(d: &[u8], o: usize) -> u16 {
    u16::from_be_bytes([d[o], d[o + 1]])
}
fn read_u32(d: &[u8], o: usize) -> u32 {
    u32::from_be_bytes([d[o], d[o + 1], d[o + 2], d[o + 3]])
}
fn find_table(d: &[u8], tag: &[u8; 4]) -> Option<usize> {
    let n = read_u16(d, 4) as usize;
    (0..n)
        .map(|i| 12 + i * 16)
        .find(|&r| &d[r..r + 4] == tag)
        .map(|r| read_u32(d, r + 8) as usize)
}

/// Load the font into the renderer and return its Windows family name (the
/// name `ctx.font()` needs).
pub fn load_family(renderer: &mut Renderer, path: &str) -> String {
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
    panic!("no Windows family name in {path}");
}

// --- the sheet ---------------------------------------------------------------

pub struct Sheet<'a> {
    pub ctx: Canvas,
    pub renderer: &'a Renderer,
    pub mono: String,
    pub format: Format,
}

/// A fresh sheet for `format`, background already painted.
pub fn new_sheet<'a>(renderer: &'a Renderer, mono: &str, format: Format) -> Sheet<'a> {
    let (w, h) = format.size();
    let mut sheet = Sheet {
        ctx: Canvas::new(w, h),
        renderer,
        mono: mono.to_string(),
        format,
    };
    sheet.ctx.background(role::canvas::background());
    sheet
}

impl Sheet<'_> {
    pub fn w(&self) -> f64 {
        self.format.w()
    }
    pub fn h(&self) -> f64 {
        self.format.h()
    }
    pub fn margin(&self) -> f64 {
        self.format.margin()
    }

    pub fn mono_width(&self, txt: &str, size: f64) -> f64 {
        self.renderer.text_width(txt, Some(&self.mono), size, &[])
    }

    pub fn mono_width_weighted(&self, txt: &str, size: f64, weight: f32) -> f64 {
        self.renderer.text_width(
            txt,
            Some(&self.mono),
            size,
            &[(u32::from_be_bytes(*b"wght"), weight)],
        )
    }

    /// Mono label with its baseline at y. align: -1 left, 0 center, 1 right.
    pub fn label(&mut self, txt: &str, x: f64, y: f64, size: f64, color: Color, align: i8) {
        self.label_weighted(txt, x, y, size, color, align, 400.0);
    }

    pub fn label_weighted(
        &mut self,
        txt: &str,
        x: f64,
        y: f64,
        size: f64,
        color: Color,
        align: i8,
        weight: f32,
    ) {
        let w = self.mono_width_weighted(txt, size, weight);
        let x = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        self.ctx
            .font(&self.mono)
            .clear_font_variations()
            .font_variation("wght", weight)
            .font_size(size)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    /// Like `label_weighted`, but shrinks the size until the text fits within
    /// `max_width`. Keeps long strings inside the margins.
    pub fn label_fit(
        &mut self,
        txt: &str,
        x: f64,
        y: f64,
        size: f64,
        max_width: f64,
        color: Color,
        align: i8,
        weight: f32,
    ) {
        let mut s = size;
        while s > 10.0 && self.mono_width_weighted(txt, s, weight) > max_width {
            s -= 1.0;
        }
        self.label_weighted(txt, x, y, s, color, align, weight);
    }

    pub fn label_padded(&mut self, txt: &str, x: f64, y: f64, size: f64, color: Color, align: i8) {
        self.label_padded_on(txt, x, y, size, color, align, role::canvas::background(), 400.0);
    }

    pub fn label_padded_on(
        &mut self,
        txt: &str,
        x: f64,
        y: f64,
        size: f64,
        color: Color,
        align: i8,
        background: Color,
        weight: f32,
    ) {
        let w = self.mono_width_weighted(txt, size, weight);
        let pad = 10.0;
        let x0 = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        self.ctx.fill(background).no_stroke();
        self.ctx
            .rect(x0 - pad, y - 0.30 * size, w + 2.0 * pad, 1.32 * size);
        self.label_weighted(txt, x0, y, size, color, -1, weight);
    }

    pub fn save(&self, out: &Path) {
        write_png(self.renderer, &self.ctx, out);
    }
}

// --- coordinate frame --------------------------------------------------------

/// Source-space -> canvas mapping. DesignBot's canvas is y-UP (origin at the
/// bottom-left, larger y is higher on screen), like the canonical blog-figure
/// crate, so the scale is applied WITHOUT a sign flip. `baseline` is the canvas
/// y of source y=0.
#[derive(Clone, Copy)]
pub struct Frame {
    pub s: f64,
    pub x0: f64,
    pub baseline: f64,
}

impl Frame {
    pub fn x(&self, ux: f64) -> f64 {
        self.x0 + ux * self.s
    }
    pub fn y(&self, uy: f64) -> f64 {
        self.baseline + uy * self.s
    }

    /// Fit a source run [0,run] x [bottom,top] centered inside the format
    /// margins, reserving `band_top` pixels at the top and `band_bottom` at the
    /// bottom of the live area (for a title band / caption band).
    pub fn fit(
        format: Format,
        run: f64,
        bottom: f64,
        top: f64,
        band_top: f64,
        band_bottom: f64,
    ) -> Self {
        let m = format.margin();
        let avail_w = format.w() - 2.0 * m;
        let avail_h = format.h() - 2.0 * m - band_top - band_bottom;
        let s = (avail_w / run).min(avail_h / (top - bottom));
        let x0 = (format.w() - run * s) / 2.0;
        let content_h = (top - bottom) * s;
        // y-up: source `bottom` sits `band_bottom` above the bottom margin,
        // vertically centered in the leftover live-area height.
        let bottom_y = m + band_bottom + (avail_h - content_h) / 2.0;
        Frame {
            s,
            x0,
            baseline: bottom_y - bottom * s,
        }
    }
}

// --- point language ----------------------------------------------------------

pub fn on8(x: f64, y: f64) -> bool {
    x.rem_euclid(8.0) == 0.0 && y.rem_euclid(8.0) == 0.0
}

#[derive(Clone, Copy)]
pub struct PointStyle {
    pub size: f64,
    pub stroke_width: f64,
}

/// Draw a glyph body (opaque fill + pen outline).
pub fn draw_body(sheet: &mut Sheet, o: &Outline, f: &Frame, fill: Color, stroke: Color, sw: f64) {
    let place = Affine::new([f.s, 0.0, 0.0, f.s, f.x0, f.baseline]);
    sheet.ctx.fill(fill).stroke(stroke).stroke_width(sw);
    sheet.ctx.draw_path(place * o.path.clone());
}

fn marker(sheet: &mut Sheet, cx: f64, cy: f64, role: PtRole, stroke: Color, fill: Color, size: f64, sw: f64) {
    let half = size / 2.0;
    sheet.ctx.fill(fill).stroke(stroke).stroke_width(sw);
    match role {
        PtRole::Corner => {
            sheet.ctx.rect(cx - half, cy - half, size, size);
        }
        _ => {
            sheet.ctx.oval(cx - half, cy - half, size, size);
        }
    }
}

/// Handles + point markers colored by grid level: green on the 8-unit machine
/// grid, red off it (the human 2-unit optical corrections). Uniform marker
/// size in the simplified figure language, so it stays legible on a phone.
pub fn draw_points_gridlevel(
    sheet: &mut Sheet,
    o: &Outline,
    f: &Frame,
    style: PointStyle,
) {
    let pen = role::figure::pen();
    let on = role::figure::green();
    let off = role::figure::red();
    sheet.ctx.no_fill().stroke(pen).stroke_width(style.stroke_width);
    for ((ax, ay), (hx, hy)) in &o.handles {
        sheet.ctx.line(f.x(*ax), f.y(*ay), f.x(*hx), f.y(*hy));
    }
    for (px, py, role) in &o.points {
        let fill = if on8(*px, *py) { on } else { off };
        marker(sheet, f.x(*px), f.y(*py), *role, pen, fill, style.size, style.stroke_width);
    }
}

/// Neutral two-tier point language (the `no`/`HO` treatment): fills are the two
/// light grays, geometry still distinguishes smooth / corner / off-curve.
pub fn draw_points_neutral(sheet: &mut Sheet, o: &Outline, f: &Frame, style: PointStyle) {
    let pen = role::figure::pen();
    sheet.ctx.no_fill().stroke(pen).stroke_width(style.stroke_width);
    for ((ax, ay), (hx, hy)) in &o.handles {
        sheet.ctx.line(f.x(*ax), f.y(*ay), f.x(*hx), f.y(*hy));
    }
    for (px, py, role) in &o.points {
        let fill = match role {
            PtRole::Off => role::figure::correction_point_fill(),
            _ => role::figure::point_fill(),
        };
        marker(sheet, f.x(*px), f.y(*py), *role, pen, fill, style.size, style.stroke_width);
    }
}

// --- grids -------------------------------------------------------------------

/// Draw the real uniform source grid over the bounding region of `glyphs`
/// (each entry is (outline, origin_ux)), plus the vertical grid running through
/// each glyph's advance box. Coordinates are truthful source units.
pub fn source_grid(
    sheet: &mut Sheet,
    f: &Frame,
    glyphs: &[(&Outline, f64)],
    bottom: f64,
    top: f64,
    unit: f64,
    color: Color,
    sw: f64,
) {
    let x_left = f.x(0.0);
    let x_right = f.x(glyphs
        .last()
        .map(|(o, origin)| origin + o.width)
        .unwrap_or(0.0));
    sheet.ctx.no_fill().stroke(color).stroke_width(sw);
    let mut v = bottom;
    while v <= top + 0.01 {
        sheet.ctx.line(x_left, f.y(v), x_right, f.y(v));
        v += unit;
    }
    for (o, origin) in glyphs {
        let mut u = 0.0;
        while u <= o.width + 0.01 {
            let x = f.x(origin + u);
            sheet.ctx.line(x, f.y(bottom), x, f.y(top));
            u += unit;
        }
    }
}

/// A full-bleed background grid at a source phase, for the reel reveal. Draws
/// the whole canvas, not just a glyph box.
pub fn full_grid(sheet: &mut Sheet, f: &Frame, unit: f64, color: Color, sw: f64) {
    let (w, h) = (sheet.w(), sheet.h());
    let step = unit * f.s;
    sheet.ctx.no_fill().stroke(color).stroke_width(sw);
    let mut x = f.x(0.0).rem_euclid(step);
    while x <= w {
        sheet.ctx.line(x, 0.0, x, h);
        x += step;
    }
    let mut y = f.y(0.0).rem_euclid(step);
    while y <= h {
        sheet.ctx.line(0.0, y, w, y);
        y += step;
    }
}

// --- metric rules ------------------------------------------------------------

/// Horizontal font metrics (baseline / x-height / cap etc.), solid + dashed,
/// spanning the source x-range [left,right].
pub fn metric_rules(
    sheet: &mut Sheet,
    f: &Frame,
    left: f64,
    right: f64,
    solid: &[f64],
    dashed: &[f64],
    color: Color,
    sw: f64,
) {
    let (x0, x1) = (f.x(left), f.x(right));
    sheet.ctx.no_fill().stroke(color).stroke_width(sw);
    sheet.ctx.line_dash(&[12.0, 12.0]);
    for &uy in dashed {
        sheet.ctx.line(x0, f.y(uy), x1, f.y(uy));
    }
    sheet.ctx.line_dash(&[]);
    for &uy in solid {
        sheet.ctx.line(x0, f.y(uy), x1, f.y(uy));
    }
}

// --- dimensions --------------------------------------------------------------

/// Horizontal dimension: capped line with a centered value above it. Source
/// coordinates in, so the value follows the current outline.
pub fn dim_h(sheet: &mut Sheet, f: &Frame, ux0: f64, ux1: f64, uy: f64, color: Color) {
    let (x0, x1, y) = (f.x(ux0), f.x(ux1), f.y(uy));
    let sw = role::line::DIMENSION;
    sheet.ctx.no_fill().stroke(color).stroke_width(sw);
    sheet.ctx.line(x0, y, x1, y);
    sheet.ctx.line(x0, y - 16.0, x0, y + 16.0);
    sheet.ctx.line(x1, y - 16.0, x1, y + 16.0);
    let val = (ux1 - ux0).round() as i64;
    sheet.label_padded(&fmt_val(val), (x0 + x1) / 2.0, y - 24.0, role::text::DIMENSION, color, 0);
}

/// Vertical dimension: capped line with the value beside it.
pub fn dim_v(sheet: &mut Sheet, f: &Frame, ux: f64, uy0: f64, uy1: f64, color: Color, right: bool) {
    let (x, y0, y1) = (f.x(ux), f.y(uy0), f.y(uy1));
    let sw = role::line::DIMENSION;
    sheet.ctx.no_fill().stroke(color).stroke_width(sw);
    sheet.ctx.line(x, y0, x, y1);
    sheet.ctx.line(x - 16.0, y0, x + 16.0, y0);
    sheet.ctx.line(x - 16.0, y1, x + 16.0, y1);
    let val = (uy1 - uy0).round() as i64;
    let (lx, align) = if right { (x + 28.0, -1) } else { (x - 28.0, 1) };
    sheet.label_padded(&fmt_val(val), lx, (y0 + y1) / 2.0 + 12.0, role::text::DIMENSION, color, align);
}

// --- powers-of-two formatting ------------------------------------------------

pub fn p2sum(v: i64) -> String {
    let mut parts = Vec::new();
    let mut bit = 1i64 << 62;
    while bit > 0 {
        if v & bit != 0 {
            parts.push(bit.to_string());
        }
        bit >>= 1;
    }
    parts.join("+")
}

/// "96 (64+32)"; pure powers stay bare ("128").
pub fn fmt_val(v: i64) -> String {
    if v.count_ones() <= 1 {
        v.to_string()
    } else {
        format!("{v} ({})", p2sum(v))
    }
}

// --- outline measurement helpers ---------------------------------------------

pub fn h_crossings(path: &BezPath, y: f64) -> Vec<f64> {
    use kurbo::{Line, Point};
    let bbox = path.bounding_box();
    let line = Line::new(Point::new(bbox.x0 - 16.0, y), Point::new(bbox.x1 + 16.0, y));
    let mut xs: Vec<f64> = path
        .segments()
        .flat_map(|seg| {
            seg.intersect_line(line)
                .into_iter()
                .map(|hit| line.p0.x + hit.line_t * (line.p1.x - line.p0.x))
                .collect::<Vec<_>>()
        })
        .collect();
    xs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    xs.dedup_by(|a, b| (*a - *b).abs() < 0.5);
    xs
}

pub fn bbox(o: &Outline) -> kurbo::Rect {
    o.path.bounding_box()
}
