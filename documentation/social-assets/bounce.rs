//! Virtua Grotesk — bouncing-glyphs physics reel (9:16, Instagram Reels).
//!
//! A ~30s deterministic 2D physics demo in the elih.net OG palette: a–z, A–Z,
//! 0–9 bounce around a gray field, colliding with each other and with the two
//! static labels (the "Virtua Grotesk" wordmark and the blog link).
//!
//!   designbot --render documentation/social-assets/bounce.rs \
//!             --output documentation/social-assets/bounce.mp4     # needs ffmpeg
//!
//! Coordinates are y-up (origin bottom-left), like DrawBot.

use designbot::prelude::*;

const FAMILY: &str = "Virtua Grotesk";

// --- deterministic PRNG (no external crate) ---------------------------------
struct Rng(u64);
impl Rng {
    fn unit(&mut self) -> f64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 11) as f64) / ((1u64 << 53) as f64)
    }
    fn range(&mut self, a: f64, b: f64) -> f64 {
        a + self.unit() * (b - a)
    }
}

struct Body {
    x: f64,
    y: f64,
    vx: f64,
    vy: f64,
    r: f64,
    ch: char,
    color: Color,
}

/// Bounce a circle body out of an axis-aligned rectangle (x, y, w, h).
fn hit_rect(b: &mut Body, rect: (f64, f64, f64, f64)) {
    let (rx, ry, rw, rh) = rect;
    let cx = b.x.clamp(rx, rx + rw);
    let cy = b.y.clamp(ry, ry + rh);
    let (dx, dy) = (b.x - cx, b.y - cy);
    let d2 = dx * dx + dy * dy;
    if d2 > 1e-6 && d2 < b.r * b.r {
        let d = d2.sqrt();
        let (nx, ny) = (dx / d, dy / d);
        let overlap = b.r - d;
        b.x += nx * overlap;
        b.y += ny * overlap;
        let vn = b.vx * nx + b.vy * ny;
        if vn < 0.0 {
            b.vx -= 2.0 * vn * nx;
            b.vy -= 2.0 * vn * ny;
        }
    }
}

/// Bounce a circle body off a fixed (immovable) circle obstacle.
fn hit_static_circle(b: &mut Body, cx: f64, cy: f64, cr: f64) {
    let (dx, dy) = (b.x - cx, b.y - cy);
    let d2 = dx * dx + dy * dy;
    let rsum = b.r + cr;
    if d2 > 1e-6 && d2 < rsum * rsum {
        let d = d2.sqrt();
        let (nx, ny) = (dx / d, dy / d);
        b.x = cx + nx * rsum;
        b.y = cy + ny * rsum;
        let vn = b.vx * nx + b.vy * ny;
        if vn < 0.0 {
            b.vx -= 2.0 * vn * nx;
            b.vy -= 2.0 * vn * ny;
        }
    }
}

/// Elastic collision between two equal-mass circle bodies (by index).
fn hit_pair(bodies: &mut [Body], i: usize, j: usize) {
    let (dx, dy) = (bodies[j].x - bodies[i].x, bodies[j].y - bodies[i].y);
    let d2 = dx * dx + dy * dy;
    let rsum = bodies[i].r + bodies[j].r;
    if d2 > 1e-6 && d2 < rsum * rsum {
        let d = d2.sqrt();
        let (nx, ny) = (dx / d, dy / d);
        let overlap = (rsum - d) / 2.0;
        bodies[i].x -= nx * overlap;
        bodies[i].y -= ny * overlap;
        bodies[j].x += nx * overlap;
        bodies[j].y += ny * overlap;
        let vn = (bodies[j].vx - bodies[i].vx) * nx + (bodies[j].vy - bodies[i].vy) * ny;
        if vn < 0.0 {
            bodies[i].vx += vn * nx;
            bodies[i].vy += vn * ny;
            bodies[j].vx -= vn * nx;
            bodies[j].vy -= vn * ny;
        }
    }
}

fn main() {
    let f = Format::Vertical; // 1080 x 1920, Reels
    let (w, h) = (f.w(), f.h());
    let m = 64.0;

    // OG palette (from elih.net/blog/virtua-grotesk)
    let bg = Color::rgb(0x92, 0x92, 0x8e);
    let ink = Color::rgb(0x23, 0x23, 0x23);
    let hues = [
        Color::oklch(0.66, 0.175, 28.0),  // red
        Color::oklch(0.74, 0.160, 52.0),  // orange
        Color::oklch(0.88, 0.160, 92.0),  // yellow
        Color::oklch(0.67, 0.160, 159.0), // leaf green
        Color::oklch(0.65, 0.160, 258.0), // blue
        Color::oklch(0.65, 0.160, 302.0), // purple
    ];

    let mut ctx = Canvas::new(w, h);
    let mut r = Renderer::new(w as u32, h as u32);
    r.load_font(find_up("fonts/ttf/VirtuaGrotesk-Regular.ttf")).expect("Virtua Grotesk");

    // --- static labels + their obstacle rectangles ---
    let title = "Virtua Grotesk:\nGrid Systems for\nDataset Engineering"; // blog title, 3 lines
    let link = "elih.net/blog/virtua-grotesk";
    let title_size = 96.0;
    let title_track = -6.0; // tight tracking, like the blog headline
    let title_lh = title_size * 0.98; // tight leading (match the reference)
    let meta_size = 40.0; // link
    let link_w = r.text_width(link, Some(FAMILY), meta_size, &[]);
    let first_base = h - m - title_size; // top line baseline
    let link_base = m; // bottom-left baseline
    let link_rect = (m, link_base - 0.25 * meta_size, link_w, meta_size);

    // Per-letter obstacles for the title: a round bumper at each title glyph, so
    // the flying glyphs bounce off the actual letters, not one big bounding box.
    let mut title_dots: Vec<(f64, f64, f64)> = Vec::new();
    let dot_r = title_size * 0.32;
    for (li, line) in title.split('\n').enumerate() {
        let cy = (first_base - li as f64 * title_lh) + 0.30 * title_size;
        let mut cx = m;
        for ch in line.chars() {
            let cw = r.text_width(&ch.to_string(), Some(FAMILY), title_size, &[]);
            if ch != ' ' {
                title_dots.push((cx + cw / 2.0, cy, dot_r));
            }
            cx += cw + title_track;
        }
    }

    // --- bodies: a-z A-Z 0-9 ---
    let glyphs: Vec<char> = ('a'..='z').chain('A'..='Z').chain('0'..='9').collect();
    let glyph_size = 132.0;
    let radius = glyph_size * 0.38;
    let mut rng = Rng(0x9E37_79B9_7F4A_7C15);
    let mut bodies: Vec<Body> = glyphs
        .iter()
        .enumerate()
        .map(|(i, &ch)| {
            let ang = rng.range(0.0, std::f64::consts::TAU);
            let speed = rng.range(220.0, 420.0);
            Body {
                x: rng.range(radius, w - radius),
                y: rng.range(320.0, h - 320.0),
                vx: speed * ang.cos(),
                vy: speed * ang.sin(),
                r: radius,
                ch,
                color: hues[i % hues.len()],
            }
        })
        .collect();

    // --- simulate + draw ---
    let fps = 30.0;
    let dt = 1.0 / fps;
    let seconds = 30.0; // ~half-minute reel
    let frames = (seconds * fps) as usize;
    ctx.frame_duration(dt);

    for frame in 0..frames {
        if frame > 0 {
            ctx.new_page();
        }

        // integrate + walls + static obstacles
        for b in bodies.iter_mut() {
            b.x += b.vx * dt;
            b.y += b.vy * dt;
            if b.x - b.r < 0.0 {
                b.x = b.r;
                b.vx = b.vx.abs();
            }
            if b.x + b.r > w {
                b.x = w - b.r;
                b.vx = -b.vx.abs();
            }
            if b.y - b.r < 0.0 {
                b.y = b.r;
                b.vy = b.vy.abs();
            }
            if b.y + b.r > h {
                b.y = h - b.r;
                b.vy = -b.vy.abs();
            }
            for &(cx, cy, cr) in &title_dots {
                hit_static_circle(b, cx, cy, cr);
            }
            hit_rect(b, link_rect);
        }
        // pairwise collisions
        for i in 0..bodies.len() {
            for j in (i + 1)..bodies.len() {
                hit_pair(&mut bodies, i, j);
            }
        }

        // draw
        ctx.background(bg);
        for b in &bodies {
            ctx.fill(b.color)
                .stroke(ink)
                .stroke_width(1.0)
                .font(FAMILY)
                .font_size(glyph_size)
                .text_align(TextAlign::Center);
            ctx.text(&b.ch.to_string(), b.x, b.y - glyph_size * 0.35);
        }
        // static labels on top (no stroke)
        ctx.fill(ink).no_stroke().text_align(TextAlign::Left).font(FAMILY);
        ctx.tracking(title_track).font_size(title_size).line_height(title_lh);
        ctx.text(title, m, first_base);
        ctx.auto_line_height().tracking(0.0).font_size(meta_size);
        ctx.text(link, m, link_base);
    }

    r.render_to_mp4(&ctx, "documentation/social-assets/bounce.mp4").expect("render");
    println!("{} frames", ctx.page_count());
}
