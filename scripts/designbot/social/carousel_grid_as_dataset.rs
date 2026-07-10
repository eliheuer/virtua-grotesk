// Social carousel — the Grid as Dataset essay condensed to 9 slides,
// typeset in Virtua Grotesk itself (display + body) with GeistMono
// captions, in the dimension-sheet visual language: dark ground, subtle
// grid, mark-red display, green mono, one shared margin system.
//
// Renders 1080x1350 PNGs (Instagram carousel / feed size) into
//   documentation/assets/social/carousel/slide-NN.png
// (override the output dir with the first script arg)
//
//   designbot --render scripts/designbot/social/carousel_grid_as_dataset.rs
//
// Inputs read at render time:
//   ~/GH/repos/virtua-grotesk/fonts/variable/VirtuaGrotesk[wght].ttf
//   ~/GH/repos/virtua-grotesk/sources/VirtuaGrotesk-{Regular,Bold}.ufo (slide 7 figure)
//   ~/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf

use designbot::norad;
use designbot::prelude::*;
use designbot_render::Renderer;
use designbot::kurbo::{Affine, BezPath};

const W: f64 = 1080.0;
const H: f64 = 1350.0;
const MARGIN: f64 = 96.0;
const HEADER_RULE_Y: f64 = H - 96.0;
const FOOTER_RULE_Y: f64 = 112.0;

// Theme tokens (the social palette from the dimension sheets)
fn bg() -> Color {
    Color::rgb(0x10, 0x10, 0x10)
}
fn grid() -> Color {
    Color::rgb(0x1e, 0x1e, 0x1e)
}
fn green() -> Color {
    Color::rgb(0x14, 0xd6, 0x7e)
}
fn red() -> Color {
    Color::rgb(0xff, 0x3a, 0x28)
}
fn red_fill() -> Color {
    Color::rgba(0xff, 0x3a, 0x28, 64)
}
fn body_gray() -> Color {
    Color::rgb(0xc8, 0xc8, 0xc8)
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

// --- UFO outline (slide 7 figure) -------------------------------------------

fn load_path(glif: &std::path::Path) -> (BezPath, f64) {
    let glyph = norad::Glyph::load(glif).expect("failed to load glif");
    let mut path = BezPath::new();
    for c in &glyph.contours {
        use norad::PointType::*;
        let pts: Vec<_> = c.points.iter().collect();
        let n = pts.len();
        let Some(start) = pts.iter().position(|p| p.typ != OffCurve) else {
            continue;
        };
        path.move_to((pts[start].x, pts[start].y));
        let mut pending: Vec<(f64, f64)> = Vec::new();
        for k in 1..=n {
            let p = pts[(start + k) % n];
            match p.typ {
                OffCurve => pending.push((p.x, p.y)),
                Curve if pending.len() == 2 => {
                    path.curve_to(pending[0], pending[1], (p.x, p.y));
                    pending.clear();
                }
                _ => {
                    path.line_to((p.x, p.y));
                    pending.clear();
                }
            }
        }
        path.close_path();
    }
    (path, glyph.width)
}

// --- deck --------------------------------------------------------------------

struct Deck {
    renderer: Renderer,
    mono: String,
    virtua: String,
}

impl Deck {
    /// Slide scaffold: ground, full-bleed subtle grid, header and footer.
    fn begin(&self, n: usize, total: usize) -> Canvas {
        let mut ctx = Canvas::new(W, H);
        ctx.background(bg());

        // subtle 32px grid, margin-aligned
        ctx.no_fill();
        ctx.stroke(grid()).stroke_width(2.0);
        let step = 32.0;
        let mut x = MARGIN;
        while x <= W - MARGIN {
            ctx.line(x, FOOTER_RULE_Y + 32.0, x, HEADER_RULE_Y - 32.0);
            x += step;
        }
        let mut y = FOOTER_RULE_Y + 32.0;
        while y <= HEADER_RULE_Y - 32.0 {
            ctx.line(MARGIN, y, W - MARGIN, y);
            y += step;
        }

        ctx.stroke(green()).stroke_width(3.5).no_fill();
        ctx.line(MARGIN, HEADER_RULE_Y, W - MARGIN, HEADER_RULE_Y);
        ctx.line(MARGIN, FOOTER_RULE_Y, W - MARGIN, FOOTER_RULE_Y);

        self.mono_text(&mut ctx, "VIRTUA GROTESK", MARGIN, HEADER_RULE_Y + 22.0, 30.0, green(), -1);
        self.mono_text(
            &mut ctx,
            &format!("{n:02} / {total:02}"),
            W - MARGIN,
            HEADER_RULE_Y + 22.0,
            30.0,
            green(),
            1,
        );
        self.mono_text(&mut ctx, "GRID AS DATASET", MARGIN, 64.0, 30.0, green(), -1);
        self.mono_text(&mut ctx, "ELIH.NET", W - MARGIN, 64.0, 30.0, green(), 1);
        ctx
    }

    fn mono_text(&self, ctx: &mut Canvas, txt: &str, x: f64, y: f64, size: f64, color: Color, align: i8) {
        let w = self.renderer.text_width(txt, Some(&self.mono), size, &[]);
        let x = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        ctx.font(&self.mono)
            .clear_font_variations()
            .font_size(size)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    /// Virtua Grotesk text at a weight; align -1 left, 0 center.
    fn virtua_text(&self, ctx: &mut Canvas, txt: &str, x: f64, y: f64, size: f64, wght: f32, color: Color, align: i8) {
        let vars = [(u32::from_be_bytes(*b"wght"), wght)];
        let w = self.renderer.text_width(txt, Some(&self.virtua), size, &vars);
        let x = match align {
            -1 => x,
            0 => x - w / 2.0,
            _ => x - w,
        };
        ctx.font(&self.virtua)
            .clear_font_variations()
            .font_variation("wght", wght)
            .font_size(size)
            .fill(color)
            .text_align(TextAlign::Left)
            .text(txt, x, y);
    }

    /// Bold display headline, lines top-down from first baseline.
    fn headline(&self, ctx: &mut Canvas, lines: &[&str], first_baseline: f64) {
        for (i, line) in lines.iter().enumerate() {
            self.virtua_text(ctx, line, MARGIN, first_baseline - i as f64 * 110.0, 96.0, 700.0, red(), -1);
        }
    }

    /// Body text in Virtua Regular, lines top-down from first baseline.
    fn body(&self, ctx: &mut Canvas, lines: &[&str], first_baseline: f64) {
        for (i, line) in lines.iter().enumerate() {
            self.virtua_text(ctx, line, MARGIN, first_baseline - i as f64 * 62.0, 44.0, 400.0, body_gray(), -1);
        }
    }

    /// Green mono block (code / stats), lines top-down from first baseline.
    fn mono_block(&self, ctx: &mut Canvas, lines: &[&str], first_baseline: f64, size: f64) {
        for (i, line) in lines.iter().enumerate() {
            self.mono_text(ctx, line, MARGIN, first_baseline - i as f64 * (size * 1.55), size, green(), -1);
        }
    }
}

fn main() {
    let home = std::env::var("HOME").unwrap();
    let out_dir = std::env::args().nth(1).unwrap_or_else(|| {
        format!("{home}/GH/repos/virtua-grotesk/documentation/assets/social/carousel")
    });
    std::fs::create_dir_all(&out_dir).expect("create output dir");

    let mut renderer = Renderer::new(W as u32, H as u32);
    let mono = load_family(
        &mut renderer,
        &format!("{home}/GH/repos/google-fonts/ofl/geistmono/GeistMono[wght].ttf"),
    );
    let virtua = load_family(
        &mut renderer,
        &format!("{home}/GH/repos/virtua-grotesk/fonts/variable/VirtuaGrotesk[wght].ttf"),
    );
    let deck = Deck {
        renderer,
        mono,
        virtua,
    };

    let g_reg = load_path(&std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Regular.ufo/glyphs/G_.glif"));
    let g_bold = load_path(&std::path::PathBuf::from(&home)
        .join("GH/repos/virtua-grotesk/sources/VirtuaGrotesk-Bold.ufo/glyphs/G_.glif"));

    let total = 9;
    let mut slides: Vec<Canvas> = Vec::new();

    // ── 01 · cover ──
    {
        let mut ctx = deck.begin(1, total);
        deck.virtua_text(&mut ctx, "Aa", W / 2.0, 560.0, 400.0, 700.0, red(), 0);
        deck.headline(&mut ctx, &["Grid as", "Dataset"], 1120.0);
        deck.body(
            &mut ctx,
            &[
                "A typeface designed on a powers of",
                "two grid, and the small neural",
                "network learning to draw it.",
            ],
            330.0,
        );
        slides.push(ctx);
    }

    // ── 02 · a font is a program ──
    {
        let mut ctx = deck.begin(2, total);
        deck.headline(&mut ctx, &["A font is", "a program"], 1120.0);
        deck.mono_block(
            &mut ctx,
            &["MOVE 64 0", "LINE 64 96", "CURVE 64 232 148 328 292 328", "CLOSE"],
            800.0,
            34.0,
        );
        deck.body(
            &mut ctx,
            &[
                "Not a set of pictures. A glyph is",
                "text: a short list of drawing",
                "commands. Start here, curve to",
                "there, close the path.",
                "",
                "Most fonts were never designed to",
                "be training data. This one is.",
            ],
            580.0,
        );
        slides.push(ctx);
    }

    // ── 03 · powers of two ──
    {
        let mut ctx = deck.begin(3, total);
        deck.headline(&mut ctx, &["Powers", "of two"], 1120.0);
        deck.mono_block(
            &mut ctx,
            &[
                "UPM        1024",
                "CAP HEIGHT  768",
                "X-HEIGHT    576",
                "DESCENDER  -256",
                "CHAMFER      16",
                "GRID          2",
            ],
            810.0,
            34.0,
        );
        deck.body(
            &mut ctx,
            &[
                "Every measurement is a power of",
                "two or a short sum of them. The",
                "eye gets the final say, in small",
                "even corrections the grid can",
                "still recover.",
            ],
            450.0,
        );
        slides.push(ctx);
    }

    // ── 04 · consistency is signal ──
    {
        let mut ctx = deck.begin(4, total);
        deck.headline(&mut ctx, &["Consistency", "is signal"], 1120.0);
        deck.body(
            &mut ctx,
            &[
                "One stroke logic, one chamfer, one",
                "start point convention. The model",
                "spends its capacity learning the",
                "design system instead of averaging",
                "a thousand borrowed hands.",
                "",
                "And outputs are checkable: off",
                "grid points are detectable, wrong",
                "stem weights are measurable.",
                "Quality stops being vibes and",
                "becomes a test suite.",
            ],
            830.0,
        );
        slides.push(ctx);
    }

    // ── 05 · glyphs are sentences ──
    {
        let mut ctx = deck.begin(5, total);
        deck.headline(&mut ctx, &["Glyphs are", "sentences"], 1120.0);
        deck.mono_block(
            &mut ctx,
            &[
                "BOS N_two W400 ADV 560",
                "MOVE 64 0",
                "LINE 64 96",
                "CURVE 64 232 148 328 292 328",
                "...",
                "CLOSE",
                "EOS",
            ],
            850.0,
            34.0,
        );
        deck.body(
            &mut ctx,
            &[
                "Drawing commands in order, under",
                "a grammar. Exactly what a",
                "transformer is built to predict.",
                "The font source itself, stripped",
                "to the drawing, is the training",
                "data. About 80 tokens a glyph.",
            ],
            460.0,
        );
        slides.push(ctx);
    }

    // ── 06 · a small model learns to draw ──
    {
        let mut ctx = deck.begin(6, total);
        deck.headline(&mut ctx, &["A small model", "learns to draw"], 1120.0);
        deck.mono_block(
            &mut ctx,
            &[
                "12M PARAMETERS",
                "1,722 TOKENS",
                "2 MASTERS",
                "1 LAPTOP, OVERNIGHT",
            ],
            800.0,
            44.0,
        );
        deck.body(
            &mut ctx,
            &[
                "No cloud, no cluster, no scraped",
                "fonts. It completes held out",
                "glyphs it never saw in training.",
                "Signal at toy scale is the thing",
                "you scale.",
            ],
            450.0,
        );
        slides.push(ctx);
    }

    // ── 07 · boldening is local prediction ──
    {
        let mut ctx = deck.begin(7, total);
        deck.headline(&mut ctx, &["Boldening is", "local prediction"], 1120.0);
        // Regular contour over Bold mass, centered, half scale
        {
            let scale = 0.52;
            let gx = (W - g_bold.1 * scale) / 2.0;
            let gy = 470.0;
            let t = Affine::translate((gx, gy)) * Affine::scale(scale);
            ctx.fill(red_fill()).no_stroke();
            ctx.draw_path(t * g_bold.0.clone());
            ctx.stroke(red()).stroke_width(3.5).no_fill();
            ctx.draw_path(t * g_reg.0.clone());
        }
        deck.body(
            &mut ctx,
            &[
                "The masters are point compatible:",
                "every Bold coordinate sits beside",
                "its Regular twin. The Regular is",
                "forced, the model fills only the",
                "Bold slots.",
            ],
            400.0,
        );
        slides.push(ctx);
    }

    // ── 08 · the designspace is a data factory ──
    {
        let mut ctx = deck.begin(8, total);
        deck.headline(&mut ctx, &["A designspace is", "a data factory"], 1120.0);
        // weight ramp: the same a at five interpolated weights
        {
            let steps = 5;
            for i in 0..steps {
                let wght = 400.0 + 300.0 * (i as f64 / (steps - 1) as f64);
                let x = MARGIN + 40.0 + i as f64 * ((W - 2.0 * MARGIN - 200.0) / (steps - 1) as f64);
                deck.virtua_text(&mut ctx, "a", x, 640.0, 220.0, wght as f32, red(), 0);
            }
        }
        deck.body(
            &mut ctx,
            &[
                "Every interpolation between",
                "masters is a legitimate instance",
                "of the family. Sample a weight,",
                "snap it to the grid: new data,",
                "labeled for free. One family,",
                "unbounded training sequences.",
            ],
            510.0,
        );
        slides.push(ctx);
    }

    // ── 09 · CTA ──
    {
        let mut ctx = deck.begin(9, total);
        deck.virtua_text(&mut ctx, "G", W / 2.0, 620.0, 420.0, 700.0, red(), 0);
        deck.headline(&mut ctx, &["Read the", "full essay"], 1120.0);
        deck.mono_block(
            &mut ctx,
            &[
                "ELIH.NET/BLOG/VIRTUA-GROTESK",
                "GITHUB.COM/ELIHEUER/VIRTUA-GROTESK",
                "SIL OPEN FONT LICENSE 1.1",
            ],
            320.0,
            34.0,
        );
        slides.push(ctx);
    }

    for (i, ctx) in slides.iter().enumerate() {
        let path = format!("{out_dir}/slide-{:02}.png", i + 1);
        deck.renderer
            .render_to_png(ctx, &path)
            .expect("png render");
        println!("wrote {path}");
    }
}
