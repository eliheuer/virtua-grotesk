// Basic specimen — dual-weight Latin character-set sheet.
// Regular (400) column on the left, Bold (700) column on the right,
// A-Z and a-z, in the house sheet language: dark ground, green rules
// and mono captions, one shared margin system. No background grid —
// the letters do the talking.
//
// Both weights share one size and one uniform leading, set from the
// real ink bounds (glyf yMin/yMax): the leading is the worst
// descender-over-ascender pair plus a fixed air gap, and the block is
// sized to fill the band between the rules exactly.
//
// One PNG per run, size picked by the mode argument (after --):
//   feed 1080x1350   reel 1080x1920   wide 2400x1260
//
//   designbot --render scripts/designbot/specimens/charset.rs \
//     --output documentation/assets/specimens/charset-wide.png -- wide
//
// GRID_VIEW=1 in the environment draws the modular grid overlay
// (unit 32, major every 4 units) in the same coordinate space the
// layout uses. Coordinates are DrawBot's: y-up, origin bottom-left,
// text() anchored at the baseline.
//
// Inputs read at render time:
//   ~/GH/repos/virtua-grotesk/fonts/variable/VirtuaGrotesk[wght].ttf
//   ~/GH/repos/virtua-grotesk/fonts/ttf/VirtuaGrotesk-{Regular,Bold}.ttf
//     (lsb for optical alignment, glyf bounds for tight leading)
//   ~/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf

use designbot::prelude::*;
use designbot_render::Renderer;

const UNIT: f64 = 32.0; // GRID_VIEW dev overlay only
const MARGIN: f64 = 96.0;
const FOOTER_RULE_Y: f64 = 112.0;
const GUTTER: f64 = 64.0;
const MONO_SIZE: f64 = 30.0;
const INK_GAP: f64 = 16.0; // air between row inks, and ink-to-rule clearance

// Theme tokens (the social palette from the dimension sheets)
fn bg() -> Color {
    Color::rgb(0x10, 0x10, 0x10)
}
fn green() -> Color {
    Color::rgb(0x14, 0xd6, 0x7e)
}
fn ink() -> Color {
    Color::rgb(0xd4, 0xd4, 0xd0)
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

// --- minimal sfnt reader ----------------------------------------------------

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
                    let idx = range_offsets + s * 2 + range_offset + (cp - start) as usize * 2;
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

/// (yMin, yMax) in font units from the glyf header (composites carry their
/// bounds there too). None for empty glyphs.
fn glyf_bounds(data: &[u8], gid: u16) -> Option<(i16, i16)> {
    let head = find_table(data, b"head")?;
    let long_loca = read_i16(data, head + 50) != 0;
    let loca = find_table(data, b"loca")?;
    let glyf = find_table(data, b"glyf")?;
    let gid = gid as usize;
    let (start, end) = if long_loca {
        (
            read_u32(data, loca + gid * 4) as usize,
            read_u32(data, loca + gid * 4 + 4) as usize,
        )
    } else {
        (
            read_u16(data, loca + gid * 2) as usize * 2,
            read_u16(data, loca + gid * 2 + 2) as usize * 2,
        )
    };
    if end <= start {
        return None;
    }
    let off = glyf + start;
    Some((read_i16(data, off + 4), read_i16(data, off + 8)))
}

/// One weight column: static TTF bytes (for metrics) + the wght value the
/// VF draws it at.
struct Weight {
    data: Vec<u8>,
    upm: f64,
    wght: f32,
    label: &'static str,
}

impl Weight {
    fn new(path: &str, wght: f32, label: &'static str) -> Weight {
        let data = std::fs::read(path).unwrap_or_else(|e| panic!("read {path}: {e}"));
        let head = find_table(&data, b"head").expect("no head table");
        let upm = read_u16(&data, head + 18) as f64;
        Weight {
            data,
            upm,
            wght,
            label,
        }
    }

    /// Left side-bearing of the first glyph, in px at `size`, so display
    /// rows can put their INK (not their pen origin) on the column line.
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

    /// Real ink extents of a row, (ascent, descent) in font units, both
    /// positive. Drives the tight leading.
    fn row_ink(&self, text: &str) -> (f64, f64) {
        let mut asc: f64 = 0.0;
        let mut desc: f64 = 0.0;
        for c in text.chars() {
            let Some(gid) = cmap_gid(&self.data, c as u32) else {
                continue;
            };
            if let Some((y_min, y_max)) = glyf_bounds(&self.data, gid) {
                asc = asc.max(y_max as f64);
                desc = desc.max(-(y_min as f64));
            }
        }
        (asc, desc.max(0.0))
    }
}

// --- sheet -------------------------------------------------------------------

struct Sheet {
    renderer: Renderer,
    mono: String,
    virtua: String,
    w: f64,
    h: f64,
    header: f64,     // header rule y = top edge of the lattice
    footer: f64,     // footer rule y = bottom edge of the lattice
    right_edge: f64, // last lattice vertical = right end of the rules
}

impl Sheet {
    fn vg_width(&self, txt: &str, size: f64, wght: f32) -> f64 {
        let vars = [(u32::from_be_bytes(*b"wght"), wght)];
        self.renderer.text_width(txt, Some(&self.virtua), size, &vars)
    }

    fn mono_width(&self, txt: &str) -> f64 {
        self.renderer.text_width(txt, Some(&self.mono), MONO_SIZE, &[])
    }

    fn mono_text(&self, ctx: &mut Canvas, txt: &str, x: f64, y: f64, color: Color, align: i8) {
        let w = self.mono_width(txt);
        let x = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        ctx.font(&self.mono)
            .clear_font_variations()
            .font_size(MONO_SIZE)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    fn vg_text(&self, ctx: &mut Canvas, txt: &str, x: f64, y: f64, size: f64, wght: f32, color: Color) {
        ctx.font(&self.virtua)
            .clear_font_variations()
            .font_variation("wght", wght)
            .font_size(size)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    /// Sheet scaffold: ground and the green header/footer rules. Captions
    /// are drawn by main — the header line doubles as the column labels.
    fn begin(&self) -> Canvas {
        let mut ctx = Canvas::new(self.w, self.h);
        ctx.background(bg());

        ctx.stroke(green()).stroke_width(3.5).no_fill();
        ctx.line(MARGIN, self.header, self.right_edge, self.header);
        ctx.line(MARGIN, self.footer, self.right_edge, self.footer);
        ctx
    }

    /// GRID_VIEW overlay on the same lattice: minor lines every unit, major
    /// every 4 units, lattice frame, center crosshairs.
    fn draw_grid_overlay(&self, ctx: &mut Canvas) {
        let minor = Color::rgba(255, 0, 0, 71);
        let major = Color::rgba(255, 0, 0, 140);
        let frame = Color::rgba(255, 0, 0, 217);
        let units_x = ((self.right_edge - MARGIN) / UNIT + 0.5) as i32;
        let units_y = ((self.header - self.footer) / UNIT + 0.5) as i32;

        ctx.save();
        ctx.no_fill();
        ctx.stroke_width(1.0);

        ctx.stroke(minor);
        for i in 0..=units_x {
            let x = MARGIN + i as f64 * UNIT;
            ctx.line(x, self.footer, x, self.header);
        }
        for i in 0..=units_y {
            let y = self.footer + i as f64 * UNIT;
            ctx.line(MARGIN, y, self.right_edge, y);
        }

        ctx.stroke(major);
        for i in (0..=units_x).step_by(4) {
            let x = MARGIN + i as f64 * UNIT;
            ctx.line(x, self.footer, x, self.header);
        }
        for i in (0..=units_y).step_by(4) {
            let y = self.footer + i as f64 * UNIT;
            ctx.line(MARGIN, y, self.right_edge, y);
        }

        ctx.stroke_width(2.0);
        ctx.stroke(frame);
        ctx.rect(MARGIN, self.footer, self.right_edge - MARGIN, self.header - self.footer);
        ctx.line(self.w / 2.0, 0.0, self.w / 2.0, self.h);
        ctx.line(0.0, self.h / 2.0, self.w, self.h / 2.0);
        ctx.restore();
    }
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "feed".to_string());
    let (w, h): (f64, f64) = match mode.as_str() {
        "feed" => (1080.0, 1350.0),
        "reel" => (1080.0, 1920.0),
        "wide" => (2400.0, 1260.0),
        other => panic!("unknown mode {other:?} (feed|reel|wide)"),
    };

    let home = std::env::var("HOME").unwrap();
    let vg = format!("{home}/GH/repos/virtua-grotesk");

    let mut renderer = Renderer::new(w as u32, h as u32);
    let mono = load_family(
        &mut renderer,
        &format!("{home}/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf"),
    );
    let virtua = load_family(
        &mut renderer,
        &format!("{vg}/fonts/variable/VirtuaGrotesk[wght].ttf"),
    );

    let header = h - MARGIN;
    let footer = FOOTER_RULE_Y;
    let right_edge = w - MARGIN;

    let sheet = Sheet {
        renderer,
        mono,
        virtua,
        w,
        h,
        header,
        footer,
        right_edge,
    };

    let weights = [
        Weight::new(&format!("{vg}/fonts/ttf/VirtuaGrotesk-Regular.ttf"), 400.0, "REGULAR 400"),
        Weight::new(&format!("{vg}/fonts/ttf/VirtuaGrotesk-Bold.ttf"), 700.0, "BOLD 700"),
    ];

    // Per-format structure, chosen so the block FILLS the band with type
    // as big as width and height jointly allow. wide and feed run the two
    // weights side by side (nine / seven letters per row); reel is too
    // tall for columns, so it stacks the Regular block over the Bold
    // block at full width, which buys ~35% more type size. A row's
    // weight of `None` means it appears in both columns; `Some(i)` means
    // it is a single full-width row in weights[i].
    let rows: Vec<(&str, Option<usize>)> = match mode.as_str() {
        "wide" => ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ", "abcdefghi", "jklmnopqr", "stuvwxyz"]
            .iter()
            .map(|r| (*r, None))
            .collect(),
        "reel" => {
            let block = ["ABCDEFGHIJ", "KLMNOPQRST", "UVWXYZ", "abcdefghij", "klmnopqrst", "uvwxyz"];
            block
                .iter()
                .map(|r| (*r, Some(0)))
                .chain(block.iter().map(|r| (*r, Some(1))))
                .collect()
        }
        // feed: the two digit rows bring the block to an exact vertical
        // fill at tight leading — remove them and the slack returns as
        // top/bottom air.
        _ => [
            "ABCDEFG", "HIJKLMN", "OPQRSTU", "VWXYZ",
            "abcdefg", "hijklmn", "opqrstu", "vwxyz",
            "01234", "56789",
        ]
        .iter()
        .map(|r| (*r, None))
        .collect(),
    };
    let n = rows.len();
    let stacked = rows.iter().any(|(_, weight)| weight.is_some());

    // Two equal columns split by a centered gutter, or one full-width
    // column when the weights are stacked.
    let col_w = if stacked {
        w - 2.0 * MARGIN
    } else {
        (w - 2.0 * MARGIN - GUTTER) / 2.0
    };
    let col_x = [MARGIN, MARGIN + col_w + GUTTER];

    // ONE uniform leading for the whole block: the worst real ink pair
    // (descender row over ascender row) plus the air gap; the top and
    // bottom pads clear the rules the same way. Sizing policy differs by
    // structure: on wide the two columns share one size (better combined
    // fill there); elsewhere each weight fills its own column width.
    // Start from the width fits and scale down together until the block
    // fits the band; leftover band space becomes equal top/bottom air.
    let row_weights = |row_weight: &Option<usize>| -> Vec<usize> {
        match row_weight {
            Some(i) => vec![*i],
            None => (0..weights.len()).collect(),
        }
    };
    let mut sizes: Vec<f64> = weights
        .iter()
        .enumerate()
        .map(|(i, weight)| {
            rows.iter()
                .filter(|(_, rw)| row_weights(rw).contains(&i))
                .map(|(r, _)| {
                    let ink_w = sheet.vg_width(r, 100.0, weight.wght) - weight.ink_left(r, 100.0);
                    100.0 * col_w / ink_w
                })
                .fold(f64::INFINITY, f64::min)
                .floor()
        })
        .collect();
    if mode == "wide" {
        let shared = sizes.iter().copied().fold(f64::INFINITY, f64::min);
        sizes = vec![shared; weights.len()];
    }

    // Ink extents per row, in font units, per weight it renders in.
    let ink_units: Vec<Vec<(usize, (f64, f64))>> = rows
        .iter()
        .map(|(r, row_weight)| {
            row_weights(row_weight)
                .into_iter()
                .map(|i| (i, weights[i].row_ink(r)))
                .collect()
        })
        .collect();
    let upm = weights[0].upm;
    let band = header - footer;

    let (leading, top_pad, bottom_pad) = loop {
        let row_px = |i: usize| -> (f64, f64) {
            ink_units[i].iter().fold((0.0f64, 0.0f64), |acc, (w, e)| {
                (
                    acc.0.max(e.0 * sizes[*w] / upm),
                    acc.1.max(e.1 * sizes[*w] / upm),
                )
            })
        };
        let leading = (1..n)
            .map(|i| row_px(i - 1).1 + row_px(i).0 + INK_GAP)
            .fold(0.0f64, f64::max);
        let top_pad = row_px(0).0 + INK_GAP;
        let bottom_pad = row_px(n - 1).1 + INK_GAP;
        if top_pad + (n as f64 - 1.0) * leading + bottom_pad <= band {
            break (leading, top_pad, bottom_pad);
        }
        for s in &mut sizes {
            *s = (*s * 0.99).floor();
        }
    };

    // Leftover band space becomes equal air against the two rules.
    let slack = band - (top_pad + (n as f64 - 1.0) * leading + bottom_pad);
    let baselines: Vec<f64> = (0..n)
        .map(|i| header - top_pad - slack / 2.0 - i as f64 * leading)
        .collect();

    let mut ctx = sheet.begin();
    sheet.mono_text(&mut ctx, "VIRTUA GROTESK", MARGIN, header + 22.0, green(), -1);
    sheet.mono_text(&mut ctx, "CHARACTER SET", right_edge, header + 22.0, green(), 1);
    sheet.mono_text(
        &mut ctx,
        "OPEN FONT LICENSE 1.1",
        MARGIN,
        footer - 48.0,
        green(),
        -1,
    );
    sheet.mono_text(
        &mut ctx,
        "ELIH.NET/VIRTUA-GROTESK",
        right_edge,
        footer - 48.0,
        green(),
        1,
    );

    // Weight labels live in the rag space after each weight's last
    // (shortest) row, right-aligned to the column edge on its baseline.
    // When the rag can't hold the full label with clearance, fall back
    // to the bare weight number.
    let label_for = |i: usize, row: &str| -> String {
        let weight = &weights[i];
        let size = sizes[i];
        let rag = col_w - (sheet.vg_width(row, size, weight.wght) - weight.ink_left(row, size));
        let full = weight.label.to_string();
        if sheet.mono_width(&full) + 24.0 <= rag {
            full
        } else {
            format!("{}", weight.wght as i32)
        }
    };
    if stacked {
        for ((row, row_weight), baseline) in rows.iter().zip(&baselines) {
            let i = row_weight.unwrap();
            let weight = &weights[i];
            let x = MARGIN - weight.ink_left(row, sizes[i]);
            sheet.vg_text(&mut ctx, row, x, *baseline, sizes[i], weight.wght, ink());
        }
        for (i, weight) in weights.iter().enumerate() {
            let _ = weight;
            let last = rows.iter().rposition(|(_, rw)| *rw == Some(i)).unwrap();
            let label = label_for(i, rows[last].0);
            sheet.mono_text(&mut ctx, &label, MARGIN + col_w, baselines[last], green(), 1);
        }
    } else {
        for (i, (weight, x0)) in weights.iter().zip(col_x).enumerate() {
            for ((row, _), baseline) in rows.iter().zip(&baselines) {
                let x = x0 - weight.ink_left(row, sizes[i]);
                sheet.vg_text(&mut ctx, row, x, *baseline, sizes[i], weight.wght, ink());
            }
            let label = label_for(i, rows[n - 1].0);
            sheet.mono_text(&mut ctx, &label, x0 + col_w, baselines[n - 1], green(), 1);
        }
    }

    if grid_view() {
        sheet.draw_grid_overlay(&mut ctx);
    }

    // The CLI rewrites the literal in any render_to_*(<expr>, "...") call
    // to --output; the wrapper mkdirs the real, rewritten path first (the
    // CLI does not create parent directories).
    let saver = Saver {
        renderer: &sheet.renderer,
    };
    saver.render_to_png(&ctx, "out.png");
}

struct Saver<'a> {
    renderer: &'a Renderer,
}

impl Saver<'_> {
    fn render_to_png(&self, ctx: &Canvas, path: &str) {
        if let Some(dir) = std::path::Path::new(path).parent() {
            let _ = std::fs::create_dir_all(dir);
        }
        self.renderer.render_to_png(ctx, path).unwrap();
        println!("wrote {path}");
    }
}
