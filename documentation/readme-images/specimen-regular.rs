//! Virtua Grotesk — README specimen (Regular).
//!
//! Powers-of-two canvas: 2048 x 1024. Height == the font's UPM (1024), width =
//! 2 UPM — so a 64px grid (UPM / 16) tiles it exactly (32 x 16 cells, no
//! cut-off) and lines up with the font's own coordinate system. Wide enough for
//! X / LinkedIn. Two colors only (theme ground + ink), no furniture, so a theme
//! swap re-skins the whole thing.
//!
//!   designbot documentation/readme-images/specimen-regular.rs
//!
//! Try Theme::dark() / Theme::light(). Edit the rows, margin, and grid below.

use designbot::prelude::*;

fn main() {
    let t = Theme::dark(); // background = t.ground, type = t.ink
    let f = Format::Wide; // 2048 x 1024 powers-of-two; h == UPM (1024)
    let (w, h) = (f.w(), f.h());
    let m = 64.0; // margin — smaller = more room / bigger type; keep a multiple of 64

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    // find_up walks up from the current dir, so this works whether you run
    // designbot from the repo root or from this script's folder.
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk");

    ctx.background(t.ground);

    // Flip on while laying things out; off for the final image.
    const SHOW_GRID: bool = true;
    if SHOW_GRID {
        // UPM-aware grid, inset by the margin (keep the margin a multiple of the
        // grid step so lines still land exactly). `.structural(N)` = finest
        // lines every N units; bigger N = fewer lines. `.subdivisions(0)` shows
        // only the coarse reference lines.
        Grid::upm(1024.0).structural(64.0).margin(m).color(t.grid).draw(&mut ctx, w, h);
    }

    ctx.fill(t.ink).font("Virtua Grotesk").text_align(TextAlign::Left);

    let rows = [
        "abcdefghijklmno",
        "pqrstuvwxyz",
        "ABCDEFGHIJKLMN",
        "OPQRSTUVWXYZ",
        "1234567890",
    ];

    // One size for all rows, fit to whichever constraint binds first:
    //   width  — the widest row spans the margins, or
    //   height — all the rows stack in the live area without overlapping.
    // Taking the smaller of the two means it always fits, for any rows/count.
    let content_w = w - 2.0 * m;
    let content_h = h - 2.0 * m;
    let n = rows.len() as f64;
    let widest = rows
        .iter()
        .map(|row| r.text_width(row, Some("Virtua Grotesk"), 1.0, &[]))
        .fold(0.0_f64, f64::max);
    let fill = 0.92; // BIGGER TYPE: fraction of each row's slot the type fills (→1.0 = tightest)
    let size = (content_w / widest).min(fill * content_h / n);
    let cap = size * 0.72; // Virtua cap height (for centering only — not a size knob)

    // Distribute the rows evenly down the live area (y-up: first row highest),
    // and JUSTIFY each row: spread its glyphs across the full width with even
    // tracking, so every row spans margin-to-margin at one consistent size.
    let slot = content_h / n;
    for (i, row) in rows.iter().enumerate() {
        let baseline = (h - m) - slot * (i as f64 + 0.5) - cap / 2.0;
        let chars: Vec<char> = row.chars().collect();
        let widths: Vec<f64> = chars
            .iter()
            .map(|c| r.text_width(&c.to_string(), Some("Virtua Grotesk"), size, &[]))
            .collect();
        let natural: f64 = widths.iter().sum();
        let track = if chars.len() > 1 {
            (content_w - natural) / (chars.len() - 1) as f64
        } else {
            0.0
        };
        let mut x = m;
        for (c, cw) in chars.iter().zip(&widths) {
            ctx.font_size(size).text(&c.to_string(), x, baseline);
            x += cw + track;
        }
    }

    r.render_to_png(&ctx, "documentation/readme-images/specimen-regular.png").unwrap();
}
