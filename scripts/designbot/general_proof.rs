// Virtua Grotesk Print Proof Generator (designbot port)
//
// Rust port of scripts/build_general_proof.py — a technical document for
// evaluating the typeface. Generates a multi-page PDF with various
// proofing layouts.
//
// Usage:
//     designbot --render scripts/designbot/general_proof.rs \
//         --output documentation/proofs/proof.pdf \
//         -- [font_path] [output_path]
//
// font_path defaults to fonts/ttf/VirtuaGrotesk-Regular.ttf (the Makefile
// `proof` target's REGULAR_FONT). Note the actual output location is the
// CLI's --output flag (the designbot CLI rewrites the render_to_* path);
// the trailing output_path arg is accepted for CLI parity with the Python
// script but --output wins.
//
// Layout note: designbot now matches drawbot's coordinate system: y-up,
// origin at the bottom-left, rect/oval anchored at the bottom-left corner,
// and Canvas::text taking the baseline of the first line. All page math
// below is the original drawbot "baseline cursor" layout (y measured up
// from the page bottom) and passes straight through to the draw calls.
// GRID_VIEW=1 draws the same red modular-grid overlay as
// scripts/grid_system.py.

use designbot::prelude::*;
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::process::Command;

// Page settings (US Letter), matching grid_system.Grid(612, 792, margin=36):
// unit = margin / 2 = 18, baseline grid = unit / 2 = 9.
const PAGE_WIDTH: f64 = 612.0;
const PAGE_HEIGHT: f64 = 792.0;
const MARGIN: f64 = 36.0;
const UNIT: f64 = 18.0;
const BASELINE: f64 = UNIT / 2.0; // 9pt baseline grid for text leading

// ---------------------------------------------------------------------------
// Minimal SFNT parsing (the Python original uses fontTools for this)
// ---------------------------------------------------------------------------

fn be16(d: &[u8], o: usize) -> u32 {
    ((d[o] as u32) << 8) | d[o + 1] as u32
}

fn be32(d: &[u8], o: usize) -> u32 {
    ((d[o] as u32) << 24) | ((d[o + 1] as u32) << 16) | ((d[o + 2] as u32) << 8) | d[o + 3] as u32
}

struct FontInfo {
    family: String,
    style: String,
    version: String,
    designer: String,
    glyph_count: usize,
    upm: f64,
    cmap: BTreeMap<u32, u16>,
    advances: Vec<u16>, // per glyph id, font units
}

impl FontInfo {
    /// Advance width of a string in points at `size` (sum of hmtx advances;
    /// no kerning — used only for line-fit decisions, like textSize()[0]).
    fn width(&self, text: &str, size: f64) -> f64 {
        let mut units: f64 = 0.0;
        for ch in text.chars() {
            if let Some(&gid) = self.cmap.get(&(ch as u32)) {
                units += self.advances[gid as usize % self.advances.len()] as f64;
            }
        }
        units * size / self.upm
    }
}

fn find_table(data: &[u8], tag: &[u8; 4]) -> Option<usize> {
    let num_tables = be16(data, 4) as usize;
    for i in 0..num_tables {
        let rec = 12 + 16 * i;
        if &data[rec..rec + 4] == tag {
            return Some(be32(data, rec + 8) as usize);
        }
    }
    None
}

fn parse_name_table(data: &[u8], off: usize) -> [String; 4] {
    // [family (1), style (2), version (5), designer (9)]
    let ids = [1u32, 2, 5, 9];
    let mut out: [String; 4] = Default::default();
    let mut priority = [0u8; 4]; // prefer Windows-platform records
    let count = be16(data, off + 2) as usize;
    let string_off = off + be16(data, off + 4) as usize;
    for i in 0..count {
        let rec = off + 6 + 12 * i;
        let plat = be16(data, rec);
        let enc = be16(data, rec + 2);
        let nid = be16(data, rec + 6);
        let len = be16(data, rec + 8) as usize;
        let s_off = string_off + be16(data, rec + 10) as usize;
        let Some(slot) = ids.iter().position(|&id| id == nid) else {
            continue;
        };
        if s_off + len > data.len() {
            continue;
        }
        let bytes = &data[s_off..s_off + len];
        let (value, prio) = if plat == 3 || plat == 0 {
            // UTF-16BE
            let units: Vec<u16> = bytes
                .chunks_exact(2)
                .map(|c| ((c[0] as u16) << 8) | c[1] as u16)
                .collect();
            (String::from_utf16_lossy(&units), if plat == 3 && enc == 1 { 3 } else { 2 })
        } else {
            // Mac Roman: treat as Latin-1-ish
            (bytes.iter().map(|&b| b as char).collect(), 1)
        };
        if prio > priority[slot] {
            out[slot] = value;
            priority[slot] = prio;
        }
    }
    out
}

fn parse_cmap_table(data: &[u8], off: usize) -> BTreeMap<u32, u16> {
    let mut map = BTreeMap::new();
    let n = be16(data, off + 2) as usize;
    let mut best: Option<(usize, u32)> = None; // (subtable offset, format)
    for i in 0..n {
        let rec = off + 4 + 8 * i;
        let sub = off + be32(data, rec + 4) as usize;
        if sub + 2 > data.len() {
            continue;
        }
        let fmt = be16(data, sub);
        match fmt {
            12 => best = Some((sub, 12)),
            4 if best.map(|(_, f)| f != 12).unwrap_or(true) => best = Some((sub, 4)),
            _ => {}
        }
        if let Some((_, 12)) = best {
            break;
        }
    }
    let Some((sub, fmt)) = best else { return map };
    if fmt == 12 {
        let n_groups = be32(data, sub + 12) as usize;
        for g in 0..n_groups {
            let rec = sub + 16 + 12 * g;
            let start = be32(data, rec);
            let end = be32(data, rec + 4);
            let start_gid = be32(data, rec + 8);
            for cp in start..=end {
                let gid = start_gid + (cp - start);
                if gid != 0 {
                    map.insert(cp, gid as u16);
                }
            }
        }
    } else {
        let seg_x2 = be16(data, sub + 6) as usize;
        let end_base = sub + 14;
        let start_base = end_base + seg_x2 + 2;
        let delta_base = start_base + seg_x2;
        let range_base = delta_base + seg_x2;
        for s in 0..seg_x2 / 2 {
            let end = be16(data, end_base + 2 * s);
            let start = be16(data, start_base + 2 * s);
            let delta = be16(data, delta_base + 2 * s);
            let range_off = be16(data, range_base + 2 * s) as usize;
            if start == 0xFFFF {
                continue;
            }
            for cp in start..=end.min(0xFFFE) {
                let gid = if range_off == 0 {
                    (cp + delta) & 0xFFFF
                } else {
                    let addr = range_base + 2 * s + range_off + 2 * (cp - start) as usize;
                    if addr + 2 > data.len() {
                        continue;
                    }
                    let g = be16(data, addr);
                    if g == 0 { 0 } else { (g + delta) & 0xFFFF }
                };
                if gid != 0 {
                    map.insert(cp, gid as u16);
                }
            }
        }
    }
    map
}

fn get_font_info(font_path: &str) -> Result<FontInfo, String> {
    let data = fs::read(font_path).map_err(|e| format!("{e}"))?;
    if data.len() < 12 {
        return Err("not an SFNT font".into());
    }
    let head = find_table(&data, b"head").ok_or("no head table")?;
    let hhea = find_table(&data, b"hhea").ok_or("no hhea table")?;
    let maxp = find_table(&data, b"maxp").ok_or("no maxp table")?;
    let name = find_table(&data, b"name").ok_or("no name table")?;
    let cmap_off = find_table(&data, b"cmap").ok_or("no cmap table")?;
    let hmtx = find_table(&data, b"hmtx").ok_or("no hmtx table")?;

    let upm = be16(&data, head + 18) as f64;
    let num_h_metrics = be16(&data, hhea + 34) as usize;
    let glyph_count = be16(&data, maxp + 4) as usize;

    let mut advances = Vec::with_capacity(glyph_count);
    let mut last = 0u16;
    for gid in 0..glyph_count {
        if gid < num_h_metrics {
            last = be16(&data, hmtx + 4 * gid) as u16;
        }
        advances.push(last);
    }

    let [family, style, version, designer] = parse_name_table(&data, name);
    let cmap = parse_cmap_table(&data, cmap_off);

    Ok(FontInfo {
        family,
        style,
        version,
        designer,
        glyph_count,
        upm,
        cmap,
        advances,
    })
}

// ---------------------------------------------------------------------------
// Layout helpers
// ---------------------------------------------------------------------------

/// Round a leading to the nearest baseline-grid step.
fn snap_baseline(value: f64) -> f64 {
    BASELINE.max((value / BASELINE).round() * BASELINE)
}

/// Draw `text` in the proofed font with its baseline at `y`.
fn font_text(ctx: &mut Canvas, fi: &FontInfo, text: &str, x: f64, y: f64, size: f64) {
    ctx.font(&fi.family);
    ctx.font_size(size);
    ctx.text(text, x, y);
}

/// Draw a Helvetica caption/label with its baseline at `y`.
fn label_text(ctx: &mut Canvas, text: &str, x: f64, y: f64, size: f64) {
    ctx.font("Helvetica");
    ctx.font_size(size);
    ctx.text(text, x, y);
}

fn grid_view() -> bool {
    matches!(
        env::var("GRID_VIEW").unwrap_or_default().to_lowercase().as_str(),
        "1" | "true" | "yes" | "on"
    )
}

/// The live modular-grid overlay from scripts/grid_system.py (GRID_VIEW=1):
/// unit lines, heavier major lines every 4 units, the margin frame, and
/// full-bleed center crosshairs, all drawn directly in y-up page
/// coordinates.
fn draw_grid_overlay(ctx: &mut Canvas) {
    let minor = Color::rgba(255, 0, 0, 71);
    let major = Color::rgba(255, 0, 0, 140);
    let frame = Color::rgba(255, 0, 0, 217);
    let inner_w = PAGE_WIDTH - 2.0 * MARGIN;
    let inner_h = PAGE_HEIGHT - 2.0 * MARGIN;
    let units_x = (inner_w / UNIT + 0.5) as i32;
    let units_y = (inner_h / UNIT + 0.5) as i32;

    ctx.save();
    ctx.no_fill();
    ctx.stroke_width(1.0);

    ctx.stroke(minor);
    for i in 0..=units_x {
        let x = MARGIN + i as f64 * UNIT;
        ctx.line(x, MARGIN, x, PAGE_HEIGHT - MARGIN);
    }
    for i in 0..=units_y {
        let y = MARGIN + i as f64 * UNIT;
        ctx.line(MARGIN, y, PAGE_WIDTH - MARGIN, y);
    }

    ctx.stroke(major);
    for i in (0..=units_x).step_by(4) {
        let x = MARGIN + i as f64 * UNIT;
        ctx.line(x, MARGIN, x, PAGE_HEIGHT - MARGIN);
    }
    for i in (0..=units_y).step_by(4) {
        let y = MARGIN + i as f64 * UNIT;
        ctx.line(MARGIN, y, PAGE_WIDTH - MARGIN, y);
    }

    ctx.stroke_width(2.0);
    ctx.stroke(frame);
    ctx.rect(MARGIN, MARGIN, inner_w, inner_h);
    ctx.line(PAGE_WIDTH / 2.0, 0.0, PAGE_WIDTH / 2.0, PAGE_HEIGHT);
    ctx.line(0.0, PAGE_HEIGHT / 2.0, PAGE_WIDTH, PAGE_HEIGHT / 2.0);

    ctx.restore();
}

struct Pager {
    started: bool,
}

impl Pager {
    fn new_page(&mut self, ctx: &mut Canvas) {
        if self.started {
            ctx.new_page();
        } else {
            self.started = true;
        }
        if grid_view() {
            draw_grid_overlay(ctx);
        }
    }
}

fn now(format: &str) -> String {
    Command::new("date")
        .arg(format!("+{format}"))
        .output()
        .ok()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}

// ---------------------------------------------------------------------------
// Page furniture
// ---------------------------------------------------------------------------

fn draw_header(ctx: &mut Canvas, fi: &FontInfo, page_title: &str) {
    ctx.save();
    ctx.fill(Color::gray(102)); // 0.4

    // Left: font name
    let header_text = format!("{} {}", fi.family, fi.style);
    label_text(ctx, &header_text, MARGIN, PAGE_HEIGHT - MARGIN + 9.0, 9.0);

    // Right: page title
    ctx.text_align(TextAlign::Right);
    label_text(ctx, page_title, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN + 9.0, 9.0);
    ctx.text_align(TextAlign::Left);

    ctx.restore();
}

fn draw_footer(ctx: &mut Canvas) {
    ctx.save();
    ctx.fill(Color::gray(128)); // 0.5
    label_text(ctx, &now("%Y-%m-%d"), MARGIN, MARGIN - 18.0, 8.0);
    ctx.restore();
}

// ---------------------------------------------------------------------------
// Pages
// ---------------------------------------------------------------------------

fn title_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 72.0;

    // Font family name large
    ctx.fill(Color::black());
    font_text(ctx, fi, &fi.family, MARGIN, y, 48.0);

    y -= 54.0;

    // Style name
    font_text(ctx, fi, &fi.style, MARGIN, y, 24.0);

    y -= 90.0;

    // Large specimen text
    font_text(ctx, fi, "Aa Bb Cc", MARGIN, y, 72.0);

    y -= 90.0;
    font_text(ctx, fi, "Dd Ee Ff", MARGIN, y, 72.0);

    y -= 90.0;
    font_text(ctx, fi, "Gg Hh Ii", MARGIN, y, 72.0);

    y -= 126.0;

    // Metadata section
    ctx.fill(Color::gray(77)); // 0.3

    let mut meta_lines = vec![
        format!("Family: {}", fi.family),
        format!("Style: {}", fi.style),
        format!("Version: {}", fi.version),
        format!("Glyphs: {}", fi.glyph_count),
        format!("Units per Em: {}", fi.upm as i64),
        format!("Generated: {}", now("%Y-%m-%d %H:%M")),
    ];
    if !fi.designer.is_empty() {
        meta_lines.insert(2, format!("Designer: {}", fi.designer));
    }

    for line in &meta_lines {
        label_text(ctx, line, MARGIN, y, 10.0);
        y -= 18.0;
    }
}

fn alphabet_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Alphabet");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 36.0;

    let uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let lowercase = "abcdefghijklmnopqrstuvwxyz";
    let sizes = [48.0, 36.0, 24.0, 18.0, 14.0, 11.0, 9.0];

    for &size in &sizes {
        ctx.fill(Color::black());

        // Check if uppercase fits
        if fi.width(uppercase, size) > PAGE_WIDTH - 2.0 * MARGIN {
            let mid = uppercase.len() / 2;
            font_text(ctx, fi, &uppercase[..mid], MARGIN, y, size);
            y -= snap_baseline(size * 1.3);
            font_text(ctx, fi, &uppercase[mid..], MARGIN, y, size);
        } else {
            font_text(ctx, fi, uppercase, MARGIN, y, size);
        }

        y -= snap_baseline(size * 1.3);

        // Lowercase
        if fi.width(lowercase, size) > PAGE_WIDTH - 2.0 * MARGIN {
            let mid = lowercase.len() / 2;
            font_text(ctx, fi, &lowercase[..mid], MARGIN, y, size);
            y -= snap_baseline(size * 1.3);
            font_text(ctx, fi, &lowercase[mid..], MARGIN, y, size);
        } else {
            font_text(ctx, fi, lowercase, MARGIN, y, size);
        }

        y -= snap_baseline(size * 1.8);

        if y < MARGIN + 50.0 {
            break;
        }
    }
}

fn numerals_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Numerals & Punctuation");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 54.0;

    let numerals = "0123456789";
    let punctuation = ".,;:!?\"'`-\u{2013}\u{2014}()[]{}/@#$%^&*+=<>";
    let sizes = [72.0, 48.0, 36.0, 24.0, 18.0, 14.0];

    // Numerals
    ctx.fill(Color::gray(128));
    label_text(ctx, "NUMERALS", MARGIN, y, 10.0);
    y -= 18.0;

    for &size in &sizes[..4] {
        ctx.fill(Color::black());
        font_text(ctx, fi, numerals, MARGIN, y, size);
        y -= snap_baseline(size * 1.5);
    }

    y -= 18.0;

    // Punctuation
    ctx.fill(Color::gray(128));
    label_text(ctx, "PUNCTUATION", MARGIN, y, 10.0);
    y -= 18.0;

    for &size in &sizes[2..] {
        ctx.fill(Color::black());

        // Split if too long
        if fi.width(punctuation, size) > PAGE_WIDTH - 2.0 * MARGIN {
            let chars: Vec<char> = punctuation.chars().collect();
            let mid = chars.len() / 2;
            let first: String = chars[..mid].iter().collect();
            let second: String = chars[mid..].iter().collect();
            font_text(ctx, fi, &first, MARGIN, y, size);
            y -= snap_baseline(size * 1.3);
            font_text(ctx, fi, &second, MARGIN, y, size);
        } else {
            font_text(ctx, fi, punctuation, MARGIN, y, size);
        }
        y -= snap_baseline(size * 1.5);

        if y < MARGIN + 30.0 {
            break;
        }
    }
}

fn waterfall_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Size Waterfall");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 36.0;

    let sample = "Hamburgefontsiv";
    let sizes = [
        72.0, 60.0, 48.0, 36.0, 30.0, 24.0, 20.0, 18.0, 16.0, 14.0, 12.0, 11.0, 10.0, 9.0, 8.0,
        7.0, 6.0,
    ];

    for &size in &sizes {
        // Size label
        ctx.save();
        ctx.fill(Color::gray(128));
        label_text(ctx, &format!("{}pt", size as i64), MARGIN, y, 8.0);
        ctx.restore();

        // Sample text
        ctx.fill(Color::black());
        font_text(ctx, fi, sample, MARGIN + 36.0, y, size);

        y -= snap_baseline(size * 1.4);

        if y < MARGIN + 20.0 {
            break;
        }
    }
}

fn spacing_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Spacing Proof");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 36.0;
    let size = 14.0;
    let line_height = snap_baseline(size * 1.4);

    ctx.fill(Color::black());

    let lowercase = "abcdefghijklmnopqrstuvwxyz";

    for c in lowercase.chars() {
        // line = c + c.join(lowercase) + c
        let mut line = String::new();
        line.push(c);
        for (i, ch) in lowercase.chars().enumerate() {
            if i > 0 {
                line.push(c);
            }
            line.push(ch);
        }
        line.push(c);

        // Truncate if the line does not fit
        while fi.width(&line, size) > PAGE_WIDTH - 2.0 * MARGIN && line.len() > 10 {
            line.truncate(line.len() - 2);
        }

        font_text(ctx, fi, &line, MARGIN, y, size);
        y -= line_height;

        if y < MARGIN + 30.0 {
            pager.new_page(ctx);
            draw_header(ctx, fi, "Spacing Proof (continued)");
            draw_footer(ctx);
            ctx.fill(Color::black());
            y = PAGE_HEIGHT - MARGIN - 36.0;
        }
    }
}

fn paragraph_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Paragraph Setting");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 36.0;

    let sample_text = "The quick brown fox jumps over the lazy dog. Pack my box with five \
dozen liquor jugs. How vexingly quick daft zebras jump! The five boxing wizards jump quickly. \
Sphinx of black quartz, judge my vow. Two driven jocks help fax my big quiz. The jay, pig, \
fox, zebra, and my wolves quack!";

    let sizes = [14.0, 12.0, 10.0, 9.0, 8.0];

    for &size in &sizes {
        // Label
        ctx.fill(Color::gray(128));
        let label = format!("{}pt / {}pt leading", size as i64, (size * 1.4) as i64);
        label_text(ctx, &label, MARGIN, y, 8.0);
        y -= 18.0;

        // Paragraph
        ctx.fill(Color::black());
        ctx.font(&fi.family);
        ctx.font_size(size);

        let box_height = snap_baseline(size * 6.0);
        let box_width = PAGE_WIDTH - 2.0 * MARGIN;

        // y is the top of the box; text_box anchors at the bottom-left
        ctx.text_box(sample_text, MARGIN, y - box_height, box_width, box_height);

        y -= box_height + 27.0;

        if y < MARGIN + 80.0 {
            break;
        }
    }
}

fn kerning_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Kerning Pairs");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 54.0;

    let kern_pairs = [
        "AV AW AT AY Av Aw Ay AC AG AO AQ AU",
        "FA TA PA VA WA YA LT LV LW LY",
        "To Tr Tu Tw Ty Te Ta Tc Ts",
        "Vo Va Ve Vu Vy Wo Wa We Wy",
        "Ya Ye Yo Yu \"A\" 'A' \"T\" 'T' \"V\"",
        "ff fi fl ffi ffl ft",
        "oo oc oe og oq op od ob",
        "rv ry rw ra re ro rc",
    ];

    let size = 24.0;

    for pairs in &kern_pairs {
        ctx.fill(Color::black());
        font_text(ctx, fi, pairs, MARGIN, y, size);
        y -= snap_baseline(size * 1.6);

        if y < MARGIN + 30.0 {
            break;
        }
    }
}

fn glyph_set_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    pager.new_page(ctx);
    draw_header(ctx, fi, "Character Set");
    draw_footer(ctx);

    // Grid settings
    let cols = 12.0;
    let cell_size = (PAGE_WIDTH - 2.0 * MARGIN) / cols;
    let glyph_size = cell_size * 0.6;

    let x_start = MARGIN;
    let y_start = PAGE_HEIGHT - MARGIN - 54.0;

    let mut x = x_start;
    let mut y = y_start;

    let mut page_num = 1;

    for (&cp, _) in fi.cmap.iter() {
        let Some(ch) = char::from_u32(cp) else { continue };
        let s = ch.to_string();

        // Draw cell (y is the top of the cell; rect anchors at the bottom-left)
        ctx.save();
        ctx.stroke(Color::gray(217)); // 0.85
        ctx.stroke_width(0.5);
        ctx.no_fill();
        ctx.rect(x, y - cell_size, cell_size, cell_size);
        ctx.restore();

        // Draw glyph, centered in the cell
        ctx.save();
        ctx.fill(Color::black());
        let char_width = fi.width(&s, glyph_size);
        let char_x = x + (cell_size - char_width) / 2.0;
        let char_y = y - cell_size + cell_size * 0.25;
        font_text(ctx, fi, &s, char_x, char_y, glyph_size);
        ctx.restore();

        // Draw unicode label
        ctx.save();
        ctx.fill(Color::gray(153)); // 0.6
        label_text(ctx, &format!("{cp:04X}"), x + 2.0, y - cell_size + 3.0, 5.0);
        ctx.restore();

        // Move to next cell
        x += cell_size;

        if x + cell_size > PAGE_WIDTH - MARGIN {
            x = x_start;
            y -= cell_size;

            if y - cell_size < MARGIN {
                page_num += 1;
                pager.new_page(ctx);
                draw_header(ctx, fi, &format!("Character Set (page {page_num})"));
                draw_footer(ctx);
                x = x_start;
                y = y_start;
            }
        }
    }
}

fn arabic_page(ctx: &mut Canvas, pager: &mut Pager, fi: &FontInfo) {
    // Check if font has Arabic (U+0600..U+06FE, matching the Python range)
    let arabic_chars: Vec<char> = (0x0600u32..0x06FF)
        .filter(|cp| fi.cmap.contains_key(cp))
        .filter_map(char::from_u32)
        .collect();

    if arabic_chars.is_empty() {
        return;
    }

    pager.new_page(ctx);
    draw_header(ctx, fi, "Arabic");
    draw_footer(ctx);

    let mut y = PAGE_HEIGHT - MARGIN - 54.0;

    let sample_lines = [
        ("salaam", "\u{633}\u{644}\u{627}\u{645}"),
        ("arabic", "\u{627}\u{644}\u{639}\u{631}\u{628}\u{64A}\u{629}"),
        ("bismillah", "\u{628}\u{633}\u{645} \u{627}\u{644}\u{644}\u{647}"),
        ("lam-alef", "\u{644}\u{627}"),
    ];

    ctx.fill(Color::gray(128));
    label_text(ctx, "ARABIC SHAPING SAMPLES", MARGIN, y, 10.0);
    y -= 18.0;

    for (label, sample) in &sample_lines {
        ctx.fill(Color::gray(115)); // 0.45
        label_text(ctx, label, MARGIN, y + 8.0, 8.0);
        ctx.fill(Color::black());
        font_text(ctx, fi, sample, MARGIN + 72.0, y, 36.0);
        y -= 54.0;
    }

    y -= 9.0;
    ctx.fill(Color::gray(128));
    label_text(ctx, "ARABIC CMAP SAMPLE", MARGIN, y, 10.0);
    y -= 27.0;

    let first: String = arabic_chars.iter().take(28).collect();
    let second: String = if arabic_chars.len() > 28 {
        arabic_chars.iter().skip(28).take(28).collect()
    } else {
        String::new()
    };
    let samples = [first, second];

    let sizes = [48.0, 36.0, 24.0, 18.0];

    for &size in &sizes {
        ctx.fill(Color::black());

        for sample in &samples {
            if !sample.is_empty() {
                font_text(ctx, fi, sample, MARGIN, y, size);
                y -= snap_baseline(size * 1.5);
            }
        }

        y -= 18.0;

        if y < MARGIN + 50.0 {
            break;
        }
    }
}

// ---------------------------------------------------------------------------

fn main() {
    // Defaults from the Makefile `proof` target:
    //   scripts/build_general_proof.py "$(REGULAR_FONT)" documentation/proofs/proof.pdf
    let args: Vec<String> = env::args().collect();
    let font_path = args
        .get(1)
        .cloned()
        .unwrap_or_else(|| "fonts/ttf/VirtuaGrotesk-Regular.ttf".to_string());
    if args.get(2).is_some() {
        eprintln!(
            "note: output path is controlled by the designbot --output flag; \
             the trailing output argument is ignored"
        );
    }

    let fi = match get_font_info(&font_path) {
        Ok(fi) => fi,
        Err(e) => {
            eprintln!("Error: could not read font at {font_path}: {e}");
            std::process::exit(1);
        }
    };

    println!("Generating proof for: {font_path}");
    println!("  Family: {}", fi.family);
    println!("  Style: {}", fi.style);
    println!("  Glyphs: {}", fi.glyph_count);

    let mut ctx = Canvas::new(PAGE_WIDTH, PAGE_HEIGHT);
    ctx.background(Color::white());

    let mut renderer = Renderer::new(PAGE_WIDTH as u32, PAGE_HEIGHT as u32);
    if let Err(e) = renderer.load_font(&font_path) {
        eprintln!("Error: could not load font into renderer: {e}");
        std::process::exit(1);
    }

    println!("  Creating pages...");

    let mut pager = Pager { started: false };
    title_page(&mut ctx, &mut pager, &fi);
    alphabet_page(&mut ctx, &mut pager, &fi);
    numerals_page(&mut ctx, &mut pager, &fi);
    waterfall_page(&mut ctx, &mut pager, &fi);
    spacing_page(&mut ctx, &mut pager, &fi);
    paragraph_page(&mut ctx, &mut pager, &fi);
    kerning_page(&mut ctx, &mut pager, &fi);
    glyph_set_page(&mut ctx, &mut pager, &fi);
    arabic_page(&mut ctx, &mut pager, &fi);

    let total_pages = ctx.page_count();

    // The designbot CLI rewrites this literal path to its --output value.
    renderer.render_to_pdf(&ctx, "documentation/proofs/proof.pdf").unwrap();

    println!("  Pages: {total_pages}");
}
