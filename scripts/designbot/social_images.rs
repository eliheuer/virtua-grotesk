// Brutalist / neomodernist PNG specimen images for social media posts.
//
// designbot port of scripts/build_social_images.py (drawbot-skia). Grid math
// from scripts/grid_system.py is inlined below (designbot scripts are
// single-file). designbot uses DrawBot semantics (origin bottom-left, y up,
// text() anchored at the first baseline), so the Python's y-up layout math
// passes straight through to the drawing calls.
//
// The designbot CLI rewrites every render_to_* path to --output, so this
// script draws exactly ONE image per run, selected by a mode argument
// (after --) of the form <format>:<image>:
//
//   formats  square (2048x2048)  portrait (1638x2048)  landscape (2048x1152)
//   images   hero  weights  alphabet-<slug>  tabular  chamfer  waterfall
//            symbols  lowercase
//
// Run from the repo root, once per output, e.g.:
//   designbot --render scripts/designbot/social_images.rs \
//     --output documentation/assets/social/square/social-01-hero.png \
//     -- square:hero
//
// Weights are discovered from fonts/ttf/*.ttf at runtime (style name from
// the name table, ordering from OS/2 usWeightClass) exactly like the Python,
// so the alphabet slugs track the built instances. Rendering itself uses the
// variable font + wght (the statics' family names collide, and the statics
// are instances of the VF).
//
// GRID_VIEW=1 in the environment draws the modular grid overlay, matching
// the grid_system.py idiom.

use designbot::prelude::*;

// --- constants mirrored from the Python ------------------------------------
const FONT_DIR: &str = "fonts/ttf";
const VF_PATH: &str = "fonts/variable/VirtuaGrotesk[wght].ttf";
const VG_FAMILY: &str = "Virtua Grotesk";
const CAP_RATIO: f64 = 0.75; // cap height / UPM in this family
const LOGO: char = '\u{E008}'; // 3x3 grid mark from the font's PUA icon block

/// Float RGB -> Color, rounding like skia does (designbot's from_floats
/// truncates, which lands 1/255 low on e.g. 0.96).
fn col(r: f64, g: f64, b: f64) -> Color {
    Color::rgb(
        (r * 255.0).round() as u8,
        (g * 255.0).round() as u8,
        (b * 255.0).round() as u8,
    )
}

fn paper() -> Color {
    col(0.055, 0.055, 0.055)
}
fn ink() -> Color {
    col(0.83, 0.83, 0.80)
}
fn white() -> Color {
    col(0.96, 0.96, 0.94)
}
fn muted() -> Color {
    col(0.56, 0.56, 0.53)
}
fn rule() -> Color {
    col(0.30, 0.30, 0.28)
}
fn red() -> Color {
    // the source markColor, used as the single accent
    col(1.0, 0.29, 0.24)
}
fn tint(t: f64) -> Color {
    col(t, t, t * 0.96)
}

fn grid_view() -> bool {
    matches!(
        std::env::var("GRID_VIEW")
            .unwrap_or_default()
            .to_lowercase()
            .as_str(),
        "1" | "true" | "yes" | "on"
    )
}

// --- per-format geometry (grid_system.Grid + set_format()) -----------------

#[derive(Clone, Copy)]
struct Fmt {
    w: f64,
    h: f64,
    margin: f64,
    unit: f64,
    caption_size: f64,
    band_top: f64,    // y-up, = y_top(2)
    band_bottom: f64, // y-up, = y(2)
}

impl Fmt {
    fn new(name: &str) -> Fmt {
        let (w, h): (f64, f64) = match name {
            "square" => (2048.0, 2048.0),
            "portrait" => (1638.0, 2048.0),
            "landscape" => (2048.0, 1152.0),
            other => panic!("unknown format {other:?} (square|portrait|landscape)"),
        };
        let margin = (w.min(h) / 16.0).round();
        let unit = margin / 2.0;
        let caption_size = (w.min(h) * 0.0225).round().max(36.0);
        Fmt {
            w,
            h,
            margin,
            unit,
            caption_size,
            band_top: h - margin - 2.0 * unit,
            band_bottom: margin + 2.0 * unit,
        }
    }

    fn band(&self) -> f64 {
        self.band_top - self.band_bottom
    }

    /// Snap a length or position to the nearest unit line.
    fn snap(&self, value: f64) -> f64 {
        (value / self.unit).round() * self.unit
    }
}

// --- static-TTF table parsing (metadata + lsb, like fontTools in Python) ---

fn read_u16(data: &[u8], offset: usize) -> u16 {
    u16::from_be_bytes([data[offset], data[offset + 1]])
}

fn read_i16(data: &[u8], offset: usize) -> i16 {
    i16::from_be_bytes([data[offset], data[offset + 1]])
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
    if data.len() < 12 {
        return None;
    }
    let num_tables = read_u16(data, 4) as usize;
    for i in 0..num_tables {
        let rec = 12 + i * 16;
        if rec + 16 > data.len() {
            break;
        }
        if &data[rec..rec + 4] == tag {
            return Some(read_u32(data, rec + 8) as usize);
        }
    }
    None
}

/// Glyph id for a codepoint via cmap formats 4 and 12.
fn cmap_gid(data: &[u8], cp: u32) -> Option<u16> {
    let cmap = find_table(data, b"cmap")?;
    let num_records = read_u16(data, cmap + 2) as usize;
    for i in 0..num_records {
        let rec = cmap + 4 + i * 8;
        let subtable = cmap + read_u32(data, rec + 4) as usize;
        match read_u16(data, subtable) {
            4 if cp <= 0xFFFF => {
                let seg_count = read_u16(data, subtable + 6) as usize / 2;
                let end_codes = subtable + 14;
                let start_codes = end_codes + seg_count * 2 + 2; // +2 reservedPad
                let deltas = start_codes + seg_count * 2;
                let range_offsets = deltas + seg_count * 2;
                for s in 0..seg_count {
                    let end = read_u16(data, end_codes + s * 2) as u32;
                    let start = read_u16(data, start_codes + s * 2) as u32;
                    if cp < start || cp > end {
                        continue;
                    }
                    let delta = read_u16(data, deltas + s * 2);
                    let range_offset = read_u16(data, range_offsets + s * 2) as usize;
                    if range_offset == 0 {
                        return Some((cp as u16).wrapping_add(delta));
                    }
                    let idx =
                        range_offsets + s * 2 + range_offset + (cp - start) as usize * 2;
                    let gid = read_u16(data, idx);
                    if gid == 0 {
                        return None;
                    }
                    return Some(gid.wrapping_add(delta));
                }
            }
            12 => {
                let n_groups = read_u32(data, subtable + 12) as usize;
                for g in 0..n_groups {
                    let rec = subtable + 16 + g * 12;
                    let start = read_u32(data, rec);
                    let end = read_u32(data, rec + 4);
                    if cp >= start && cp <= end {
                        let start_gid = read_u32(data, rec + 8);
                        return Some((start_gid + (cp - start)) as u16);
                    }
                }
            }
            _ => {}
        }
    }
    None
}

/// (advance, lsb) in font units from hmtx/hhea.
fn hmtx_metrics(data: &[u8], gid: u16) -> Option<(u16, i16)> {
    let hhea = find_table(data, b"hhea")?;
    let num_h = read_u16(data, hhea + 34) as usize;
    let hmtx = find_table(data, b"hmtx")?;
    let gid = gid as usize;
    if gid < num_h {
        Some((
            read_u16(data, hmtx + gid * 4),
            read_i16(data, hmtx + gid * 4 + 2),
        ))
    } else {
        let advance = read_u16(data, hmtx + (num_h - 1) * 4);
        let lsb = read_i16(data, hmtx + num_h * 4 + (gid - num_h) * 2);
        Some((advance, lsb))
    }
}

/// A name-table string, preferring Windows (3,1,0x409), then any platform
/// 3/0 (UTF-16BE), then platform 1 (Latin-1) — fontTools getDebugName-ish.
fn name_string(data: &[u8], name_id: u16) -> Option<String> {
    let name = find_table(data, b"name")?;
    let count = read_u16(data, name + 2) as usize;
    let string_off = name + read_u16(data, name + 4) as usize;
    let mut best: Option<(u8, String)> = None; // (rank, string) lower rank wins
    for i in 0..count {
        let rec = name + 6 + i * 12;
        let (plat, enc, lang, nid) = (
            read_u16(data, rec),
            read_u16(data, rec + 2),
            read_u16(data, rec + 4),
            read_u16(data, rec + 6),
        );
        if nid != name_id {
            continue;
        }
        let len = read_u16(data, rec + 8) as usize;
        let off = string_off + read_u16(data, rec + 10) as usize;
        if off + len > data.len() {
            continue;
        }
        let bytes = &data[off..off + len];
        let (rank, s) = match plat {
            3 | 0 => {
                let units: Vec<u16> = bytes
                    .chunks_exact(2)
                    .map(|c| u16::from_be_bytes([c[0], c[1]]))
                    .collect();
                let rank = if plat == 3 && enc == 1 && lang == 0x409 {
                    0
                } else {
                    1
                };
                (rank, String::from_utf16_lossy(&units))
            }
            _ => (2, bytes.iter().map(|&b| b as char).collect()),
        };
        if best.as_ref().map_or(true, |(r, _)| rank < *r) {
            best = Some((rank, s));
        }
    }
    best.map(|(_, s)| s)
}

/// head.fontRevision as the shortest decimal that round-trips through
/// Fixed 16.16 (fontTools floatToFixedToStr).
fn font_revision_str(data: &[u8]) -> String {
    let head = match find_table(data, b"head") {
        Some(off) => off,
        None => return "0.0".to_string(),
    };
    let raw = read_u32(data, head + 4) as i32;
    let value = raw as f64 / 65536.0;
    for decimals in 1..=8 {
        let s = format!("{value:.decimals$}");
        let parsed: f64 = s.parse().unwrap_or(0.0);
        if (parsed * 65536.0).round() as i32 == raw {
            return s;
        }
    }
    format!("{value}")
}

/// Glyph names from the post table (format 2.0). Standard Macintosh indices
/// are only resolved for the digits (19..=28), which is all this script needs.
fn post_glyph_names(data: &[u8]) -> Vec<String> {
    const STD_DIGITS: [&str; 10] = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ];
    let Some(post) = find_table(data, b"post") else {
        return Vec::new();
    };
    if read_u32(data, post) != 0x0002_0000 {
        return Vec::new();
    }
    let num_glyphs = read_u16(data, post + 32) as usize;
    let index_base = post + 34;
    // Pascal strings for indices >= 258 follow the index array.
    let mut strings = Vec::new();
    let mut off = index_base + num_glyphs * 2;
    while off < data.len() {
        let len = data[off] as usize;
        off += 1;
        if off + len > data.len() {
            break;
        }
        strings.push(String::from_utf8_lossy(&data[off..off + len]).into_owned());
        off += len;
    }
    (0..num_glyphs)
        .map(|gid| {
            let idx = read_u16(data, index_base + gid * 2) as usize;
            if idx >= 258 {
                strings.get(idx - 258).cloned().unwrap_or_default()
            } else if (19..=28).contains(&idx) {
                STD_DIGITS[idx - 19].to_string()
            } else {
                String::new()
            }
        })
        .collect()
}

// --- styles (Python's Style / discover_styles) ------------------------------

struct Style {
    data: Vec<u8>,
    name: String,   // style name: name 17 or 2
    family: String, // name 16 or 1
    weight_class: u16,
    upm: f64,
    version: String,
    tab_width: Option<f64>, // zero.tf advance, font units
}

impl Style {
    fn new(path: &std::path::Path) -> Style {
        let data = std::fs::read(path).expect("failed to read a static TTF");
        let stem = path
            .file_stem()
            .map(|s| s.to_string_lossy().into_owned())
            .unwrap_or_default();
        let name = name_string(&data, 17)
            .or_else(|| name_string(&data, 2))
            .unwrap_or(stem);
        let family = name_string(&data, 16)
            .or_else(|| name_string(&data, 1))
            .unwrap_or_default();
        let os2 = find_table(&data, b"OS/2").expect("no OS/2 table");
        let weight_class = read_u16(&data, os2 + 4);
        let head = find_table(&data, b"head").expect("no head table");
        let upm = read_u16(&data, head + 18) as f64;
        let version = format!("v{}", font_revision_str(&data));
        let names = post_glyph_names(&data);
        let tab_width = names
            .iter()
            .position(|n| n == "zero.tf")
            .and_then(|gid| hmtx_metrics(&data, gid as u16))
            .map(|(advance, _)| advance as f64);
        Style {
            data,
            name,
            family,
            weight_class,
            upm,
            version,
            tab_width,
        }
    }

    fn slug(&self) -> String {
        self.name.to_lowercase().replace(' ', "-")
    }

    fn wght(&self) -> f32 {
        self.weight_class as f32
    }

    /// Left side-bearing of the first glyph, in points at `size`
    /// (grid_system.Grid.ink_left).
    fn ink_left(&self, text: &str, size: f64) -> f64 {
        let Some(c) = text.chars().next() else {
            return 0.0;
        };
        let Some(gid) = cmap_gid(&self.data, c as u32) else {
            return 0.0;
        };
        match hmtx_metrics(&self.data, gid) {
            Some((_, lsb)) => lsb as f64 * size / self.upm,
            None => 0.0,
        }
    }

    /// Ink shift, in font units, that tnum would apply to this digit:
    /// lsb(<name>.tf) - lsb(<name>). Used to emulate tabular figures glyph
    /// by glyph (the .tf outlines are the defaults re-centered in the
    /// tabular advance).
    fn tabular_shift(&self, c: char) -> f64 {
        let Some(gid) = cmap_gid(&self.data, c as u32) else {
            return 0.0;
        };
        let names = post_glyph_names(&self.data);
        let Some(base) = names.get(gid as usize).filter(|n| !n.is_empty()) else {
            return 0.0;
        };
        let tf_name = format!("{base}.tf");
        let Some(tf_gid) = names.iter().position(|n| *n == tf_name) else {
            return 0.0;
        };
        let def = hmtx_metrics(&self.data, gid).map(|(_, l)| l).unwrap_or(0);
        let tf = hmtx_metrics(&self.data, tf_gid as u16)
            .map(|(_, l)| l)
            .unwrap_or(0);
        (tf - def) as f64
    }
}

fn discover_styles() -> Vec<Style> {
    let mut paths: Vec<std::path::PathBuf> = std::fs::read_dir(FONT_DIR)
        .expect("no fonts/ttf/ directory — run `make build` from the repo root first")
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| p.extension().map_or(false, |e| e == "ttf"))
        .collect();
    if paths.is_empty() {
        panic!("No fonts in fonts/ttf/. Run `make build` first.");
    }
    paths.sort();
    let mut styles: Vec<Style> = paths.iter().map(|p| Style::new(p)).collect();
    styles.sort_by_key(|s| s.weight_class);
    styles
}

fn style_near<'a>(styles: &'a [Style], weight_class: u16) -> &'a Style {
    styles
        .iter()
        .min_by_key(|s| (s.weight_class as i32 - weight_class as i32).abs())
        .unwrap()
}

// --- drawing helpers ---------------------------------------------------------

struct Page<'a> {
    ctx: Canvas,
    renderer: &'a Renderer,
    fmt: Fmt,
}

impl<'a> Page<'a> {
    fn new(renderer: &'a Renderer, fmt: Fmt) -> Page<'a> {
        let mut ctx = Canvas::new(fmt.w, fmt.h);
        ctx.background(paper());
        Page { ctx, renderer, fmt }
    }

    fn text_width(&self, txt: &str, style: &Style, size: f64) -> f64 {
        self.renderer
            .text_width(txt, Some(VG_FAMILY), size, &[(u32::from_be_bytes(*b"wght"), style.wght())])
    }

    /// Virtua Grotesk text with its BASELINE at `baseline`, exactly like the
    /// drawbot original's text() (designbot's text() is baseline-anchored).
    fn vg_text(
        &mut self,
        txt: &str,
        x: f64,
        baseline: f64,
        style: &Style,
        size: f64,
        color: Color,
        align: TextAlign,
    ) {
        self.ctx
            .font(VG_FAMILY)
            .clear_font_variations()
            .font_variation("wght", style.wght())
            .font_size(size)
            .fill(color)
            .text_align(align)
            .text(txt, x, baseline);
        self.ctx.text_align(TextAlign::Left);
    }

    /// Font.Garden poster idiom: small captions in the four corners.
    fn captions(&mut self, lightest: &Style, bottom_left: Option<&str>, footer: bool) {
        let fmt = self.fmt;
        let default_bl = format!(
            "{} {} {}",
            lightest.family, lightest.name, lightest.version
        );
        let bottom_left = bottom_left.unwrap_or(&default_bl).to_string();
        let cs = fmt.caption_size;
        let top_baseline = fmt.h - fmt.margin - cs * CAP_RATIO;
        self.vg_text(
            &format!("{LOGO} Font.Garden/virtua"),
            fmt.margin,
            top_baseline,
            lightest,
            cs,
            muted(),
            TextAlign::Left,
        );
        self.vg_text(
            "Open Font License OFL v1.1",
            fmt.w - fmt.margin,
            top_baseline,
            lightest,
            cs,
            muted(),
            TextAlign::Right,
        );
        if footer {
            self.vg_text(
                &bottom_left,
                fmt.margin,
                fmt.margin,
                lightest,
                cs,
                muted(),
                TextAlign::Left,
            );
            self.vg_text(
                "github.com/eliheuer/virtua-grotesk",
                fmt.w - fmt.margin,
                fmt.margin,
                lightest,
                cs,
                muted(),
                TextAlign::Right,
            );
        }
    }

    /// Largest size where `txt` in `style` spans `target_w`.
    fn fit_size(&self, txt: &str, style: &Style, target_w: f64) -> f64 {
        100.0 * target_w / self.text_width(txt, style, 100.0)
    }

    /// Largest size where the widest row fits the inner width and the block
    /// fits the caption band at tight leading.
    fn fit_stack_size(&self, rows: &[(String, &Style)]) -> f64 {
        let inner = self.fmt.w - self.fmt.margin * 2.0;
        let width_fit = rows
            .iter()
            .map(|(txt, style)| self.fit_size(txt, style, inner))
            .fold(f64::INFINITY, f64::min);
        let band = self.fmt.band();
        let cap_max = band / (1.12 * (rows.len() as f64 - 1.0) + 1.0);
        width_fit.min(cap_max / CAP_RATIO)
    }

    /// Left-aligned repetition block, vertically centered between the
    /// captions, leading clamped between tight and loose. Returns the top
    /// baseline y (y-up).
    fn stack(&mut self, rows: &[(String, &Style)], size: f64, color: Color) -> f64 {
        let fmt = self.fmt;
        let cap = CAP_RATIO * size;
        let count = rows.len() as f64;
        let band = fmt.band();
        let leading = (band - cap) / (count - 1.0).max(1.0);
        let leading = leading.min(cap * 1.55).max(cap * 1.12);
        let block = (count - 1.0) * leading + cap;
        let mut baseline = fmt.band_bottom + (band - block) / 2.0 + block - cap;
        let top_baseline = baseline;
        for (txt, style) in rows {
            let x = fmt.margin - style.ink_left(txt, size);
            self.vg_text(txt, x, baseline, style, size, color, TextAlign::Left);
            baseline -= leading;
        }
        top_baseline
    }

    /// As many repeated rows as fit the caption band at tight leading.
    fn repetition_count(&self, txt: &str, style: &Style) -> usize {
        let size = self.fit_size(txt, style, self.fmt.w - self.fmt.margin * 2.0);
        let cap = CAP_RATIO * size;
        let band = self.fmt.band();
        (((band - cap) / (1.15 * cap)).floor() as usize + 1).max(2)
    }

    /// GRID_VIEW overlay: grid_system.Grid.draw().
    fn draw_grid_overlay(&mut self) {
        let fmt = self.fmt;
        let minor = Color::rgba(255, 0, 0, 71);
        let major = Color::rgba(255, 0, 0, 140);
        let frame = Color::rgba(255, 0, 0, 217);
        let inner_w = fmt.w - 2.0 * fmt.margin;
        let inner_h = fmt.h - 2.0 * fmt.margin;
        let units_x = (inner_w / fmt.unit + 0.5) as i32;
        let units_y = (inner_h / fmt.unit + 0.5) as i32;

        self.ctx.save();
        self.ctx.no_fill();
        self.ctx.stroke_width(1.0);

        self.ctx.stroke(minor);
        for i in 0..=units_x {
            let x = fmt.margin + i as f64 * fmt.unit;
            self.ctx.line(x, fmt.margin, x, fmt.h - fmt.margin);
        }
        for i in 0..=units_y {
            let y = fmt.margin + i as f64 * fmt.unit;
            self.ctx.line(fmt.margin, y, fmt.w - fmt.margin, y);
        }

        self.ctx.stroke(major);
        for i in (0..=units_x).step_by(4) {
            let x = fmt.margin + i as f64 * fmt.unit;
            self.ctx.line(x, fmt.margin, x, fmt.h - fmt.margin);
        }
        for i in (0..=units_y).step_by(4) {
            let y = fmt.margin + i as f64 * fmt.unit;
            self.ctx.line(fmt.margin, y, fmt.w - fmt.margin, y);
        }

        self.ctx.stroke_width(2.0);
        self.ctx.stroke(frame);
        self.ctx.rect(fmt.margin, fmt.margin, inner_w, inner_h);
        self.ctx.line(fmt.w / 2.0, 0.0, fmt.w / 2.0, fmt.h);
        self.ctx.line(0.0, fmt.h / 2.0, fmt.w, fmt.h / 2.0);
        self.ctx.restore();
    }
}

/// Greedy word wrap at (size, wght), mirroring drawbot-skia textBox.
fn wrap_text(page: &Page, text: &str, style: &Style, size: f64, max_w: f64) -> Vec<String> {
    let measure = |s: &str| page.text_width(s, style, size);
    // Trailing whitespace is trimmed by the layouter, so derive the space
    // advance from a spaced pair.
    let space_w = measure("n n") - 2.0 * measure("n");
    let mut out = Vec::new();
    let mut cur = String::new();
    let mut cur_w = 0.0;
    for word in text.split_whitespace() {
        let w = measure(word);
        if cur.is_empty() {
            cur = word.to_string();
            cur_w = w;
        } else if cur_w + space_w + w <= max_w {
            cur.push(' ');
            cur.push_str(word);
            cur_w += space_w + w;
        } else {
            out.push(std::mem::take(&mut cur));
            cur = word.to_string();
            cur_w = w;
        }
    }
    if !cur.is_empty() {
        out.push(cur);
    }
    out
}

// --- the eight images --------------------------------------------------------

/// Repetition poster: the family name over and over, fit to the frame.
fn draw_hero(page: &mut Page, styles: &[Style]) {
    let style = style_near(styles, 500);
    let count = page.repetition_count("Virtua Grotesk", style);
    let rows: Vec<(String, &Style)> = (0..count)
        .map(|_| ("Virtua Grotesk".to_string(), style))
        .collect();
    let size = page.fit_stack_size(&rows);
    page.stack(&rows, size, white());
    page.captions(&styles[0], None, true);
}

/// One row per discovered weight, lightest to heaviest.
fn draw_weights(page: &mut Page, styles: &[Style]) {
    let rows: Vec<(String, &Style)> = styles
        .iter()
        .map(|s| ("Hamburg".to_string(), s))
        .collect();
    let size = page.fit_stack_size(&rows);
    page.stack(&rows, size, ink());
    let lightest = &styles[0];
    let heaviest = &styles[styles.len() - 1];
    let bottom_left = format!(
        "{} wght {}\u{2013}{} {}",
        lightest.family, lightest.weight_class, heaviest.weight_class, lightest.version
    );
    page.captions(lightest, Some(&bottom_left), true);
}

fn draw_alphabet(page: &mut Page, styles: &[Style], style: &Style) {
    let lines = [
        "ABCDEFGHIJ",
        "KLMNOPQR",
        "STUVWXYZ",
        "0123456789",
        "abcdefghij",
        "klmnopqr",
        "stuvwxyz",
    ];
    let rows: Vec<(String, &Style)> = lines.iter().map(|t| (t.to_string(), style)).collect();
    let size = page.fit_stack_size(&rows);
    page.stack(&rows, size, ink());
    let bottom_left = format!("{} {} {}", style.family, style.name, style.version);
    page.captions(&styles[0], Some(&bottom_left), true);
}

fn draw_tabular(page: &mut Page, styles: &[Style]) {
    let style = style_near(styles, 600);
    let tab_units = style
        .tab_width
        .expect("no zero.tf glyph for the tabular image");

    let rows = ["0123456789", "1463082957", "2048102464"];
    // Fit by tabular advance, not proportional widths: every row is
    // digits * tab_width wide once tnum is applied.
    let fmt = page.fmt;
    let digits = rows[0].chars().count() as f64;
    let inner = fmt.w - fmt.margin * 2.0;
    let width_fit = inner * style.upm / (digits * tab_units);
    let band = fmt.band();
    let n = rows.len() as f64;
    let cap_max = band / (1.12 * (n - 1.0) + 1.0);
    let size = width_fit.min(cap_max / CAP_RATIO);
    let tab = tab_units / style.upm * size;
    let cap = CAP_RATIO * size;
    let scale = size / style.upm;

    // stack() layout math, but each digit is placed by hand at its tabular
    // pen position + the .tf ink shift — designbot has no OpenType feature
    // API, and the .tf digits are the default outlines re-centered in the
    // tabular advance, so this reproduces tnum exactly.
    let leading = ((band - cap) / (n - 1.0)).min(cap * 1.55).max(cap * 1.12);
    let block = (n - 1.0) * leading + cap;
    let mut baseline = fmt.band_bottom + (band - block) / 2.0 + block - cap;
    let top_baseline = baseline;
    for row in rows {
        // The Python's ink_left() is feature-unaware: it offsets each row by
        // the DEFAULT lsb of its first digit. Mirror that as-is.
        let x_start = fmt.margin - style.ink_left(row, size);
        for (i, c) in row.chars().enumerate() {
            let x = x_start + i as f64 * tab + style.tabular_shift(c) * scale;
            page.vg_text(
                &c.to_string(),
                x,
                baseline,
                style,
                size,
                ink(),
                TextAlign::Left,
            );
        }
        baseline -= leading;
    }

    let bottom = top_baseline - (n - 1.0) * leading - size * 0.06;
    page.ctx.save();
    page.ctx.stroke(rule());
    page.ctx.stroke_width(2.0);
    for i in 0..=(digits as i32) {
        let x = fmt.margin + i as f64 * tab;
        page.ctx.line(x, bottom, x, top_baseline + cap);
    }
    page.ctx.restore();

    let bottom_left = format!("{} Tabular Figures \u{B7} tnum", style.family);
    page.captions(&styles[0], Some(&bottom_left), true);
}

fn draw_chamfer(page: &mut Page, styles: &[Style]) {
    let heaviest = &styles[styles.len() - 1];
    let rows = vec![("Aa".to_string(), heaviest)];
    let size = page.fit_stack_size(&rows);
    let cap = CAP_RATIO * size;
    let fmt = page.fmt;
    let baseline = (fmt.band_top + fmt.band_bottom) / 2.0 - cap / 2.0;
    let x = fmt.margin - heaviest.ink_left("Aa", size);
    page.vg_text("Aa", x, baseline, heaviest, size, ink(), TextAlign::Left);
    let bottom_left = format!("{} \u{B7} 16-unit chamfered corners", heaviest.family);
    page.captions(&styles[0], Some(&bottom_left), true);
}

/// Split panel: point sizes on the left, the name on the right.
fn draw_waterfall(page: &mut Page, styles: &[Style]) {
    let style = style_near(styles, 600);
    let fmt = page.fmt;
    let split = fmt.snap(fmt.w * 0.36);
    page.ctx.save();
    page.ctx.stroke(rule());
    page.ctx.stroke_width(2.0);
    page.ctx.line(split, fmt.band_bottom - 36.0, split, fmt.band_top + 36.0);
    page.ctx.restore();

    let band = fmt.band();
    let factor = band / 1480.0;
    let sizes: Vec<f64> = [236.0, 196.0, 162.0, 132.0, 106.0, 82.0, 62.0, 46.0]
        .iter()
        .map(|s| (s * factor).round())
        .collect();
    let mut y = fmt.band_top - sizes[0] * 0.82;
    for (index, &size) in sizes.iter().enumerate() {
        let t = (0.83 - index as f64 * 0.07).max(0.30);
        page.vg_text(
            &format!("{}", size as i64),
            split - 56.0,
            y,
            style,
            size,
            tint(t),
            TextAlign::Right,
        );
        let name = if index < 5 { "Virtua\u{A9}" } else { "Grotesk\u{A9}" };
        page.vg_text(name, split + 56.0, y, style, size, ink(), TextAlign::Left);
        y -= size * 1.16 + 14.0 * factor;
    }

    page.captions(&styles[0], None, true);
}

/// Coded strings in the source markColor red.
fn draw_symbols(page: &mut Page, styles: &[Style]) {
    let lightest = &styles[0];
    let lines = [
        "*{Virtua}*",
        "<GROTESK>",
        "(+Chamfer)",
        "@16/1024_u",
        "#OFL\u{2014}2026",
    ];
    let rows: Vec<(String, &Style)> = lines.iter().map(|t| (t.to_string(), lightest)).collect();
    let size = page.fit_stack_size(&rows);
    page.stack(&rows, size, red());
    page.captions(lightest, None, true);
}

/// Giant cropped lowercase, weights receding in tint steps.
fn draw_lowercase(page: &mut Page, styles: &[Style]) {
    let fmt = page.fmt;
    let lightest = &styles[0];
    let heaviest = &styles[styles.len() - 1];
    let mid = style_near(styles, 600);
    let size = fmt.h * 1.12;
    let layers: [(&Style, f64, f64); 3] = [
        (lightest, 0.30, 0.947),
        (mid, 0.50, 0.508),
        (heaviest, 0.83, 0.068),
    ];
    for (style, t, x_frac) in layers.iter().rev() {
        page.vg_text(
            "a",
            fmt.w * x_frac,
            -fmt.h * 0.064,
            style,
            size,
            tint(*t),
            TextAlign::Left,
        );
    }

    // drawbot-skia textBox at the default 1.2 line height: first baseline
    // one fontSize below the box top, greedy wrap to the box width.
    let cs = fmt.caption_size;
    let box_w = fmt.w * 0.625;
    let box_top = fmt.h - fmt.margin - cs * 2.0; // y-up top edge of the box
    let text = "Virtua Grotesk is a geometric grotesk with 16-unit chamfered \
                corners \u{2014} monolinear strokes and a retro-futurist technical \
                character, drawn with modern precision on a 1024-unit grid.";
    let line_height = cs * 1.2;
    let max_lines = (300.0 / line_height).floor() as usize;
    let lines = wrap_text(page, text, lightest, cs, box_w);
    let mut baseline = box_top - cs;
    for line in lines.iter().take(max_lines) {
        page.vg_text(
            line,
            fmt.margin,
            baseline,
            lightest,
            cs,
            muted(),
            TextAlign::Left,
        );
        baseline -= line_height;
    }

    page.captions(lightest, None, false);
}

/// Saving shim: the designbot CLI rewrites the string literal in any
/// `render_to_*(<expr>, "...")` call to the --output path, but (unlike the
/// Python original) it does not create missing parent directories. Routing
/// the call through this wrapper lets the script mkdir the real, rewritten
/// output path before rendering.
struct Saver<'a> {
    renderer: &'a Renderer,
}

impl Saver<'_> {
    fn mkdirs(path: &str) {
        if let Some(dir) = std::path::Path::new(path).parent() {
            let _ = std::fs::create_dir_all(dir);
        }
    }

    fn render_to_png(&self, ctx: &Canvas, path: &str) {
        Self::mkdirs(path);
        self.renderer.render_to_png(ctx, path).unwrap();
    }

    /// Social-optimized PNG (sRGB chunk + alpha passthrough pixel); the CLI
    /// rewrites render calls to this when invoked with --social.
    #[allow(dead_code)]
    fn render_to_png_social(&self, ctx: &Canvas, path: &str) {
        Self::mkdirs(path);
        self.renderer.render_to_png_social(ctx, path).unwrap();
    }

    #[allow(dead_code)]
    fn render_to_pdf(&self, ctx: &Canvas, path: &str) {
        Self::mkdirs(path);
        self.renderer.render_to_pdf(ctx, path).unwrap();
    }
}

// --- main ---------------------------------------------------------------------

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mode = args.first().map(String::as_str).unwrap_or_else(|| {
        panic!(
            "usage: -- <format>:<image>  (formats: square|portrait|landscape; \
             images: hero|weights|alphabet-<slug>|tabular|chamfer|waterfall|symbols|lowercase)"
        )
    });
    let (fmt_name, image) = mode
        .split_once(':')
        .unwrap_or_else(|| panic!("mode must be <format>:<image>, got {mode:?}"));

    let fmt = Fmt::new(fmt_name);
    let styles = discover_styles();

    let mut renderer = Renderer::new(fmt.w as u32, fmt.h as u32);
    renderer.load_font(VF_PATH).expect(
        "failed to load fonts/variable/VirtuaGrotesk[wght].ttf — run `make build` from the repo root first",
    );

    let mut page = Page::new(&renderer, fmt);
    match image {
        "hero" => draw_hero(&mut page, &styles),
        "weights" => draw_weights(&mut page, &styles),
        "tabular" => draw_tabular(&mut page, &styles),
        "chamfer" => draw_chamfer(&mut page, &styles),
        "waterfall" => draw_waterfall(&mut page, &styles),
        "symbols" => draw_symbols(&mut page, &styles),
        "lowercase" => draw_lowercase(&mut page, &styles),
        other => {
            let Some(slug) = other.strip_prefix("alphabet-") else {
                panic!("unknown image {other:?}");
            };
            let style = styles
                .iter()
                .find(|s| s.slug() == slug)
                .unwrap_or_else(|| panic!("no style with slug {slug:?} in fonts/ttf/"));
            draw_alphabet(&mut page, &styles, style);
        }
    }

    if grid_view() {
        page.draw_grid_overlay();
    }

    let Page { ctx, .. } = page;
    let saver = Saver {
        renderer: &renderer,
    };
    saver.render_to_png(&ctx, "out.png");
}
