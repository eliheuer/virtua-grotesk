//! Canonical three-sheet review layout. See documentation/qa.md.
//! designbot --raw documentation/proofs/hebrew_review.rs --output OUT.png -- light form BEFORE.ttf AFTER.ttf RUBIK.ttf NOTO.ttf applied
//! sheet: form | text | weight; theme: light | dark; state: applied | candidate
//! REVIEW_GROUP=he-het-tav selects a current/reference review without a candidate.
//! GRID_VIEW=1 shows structural guides; GRID_VIEW=baseline adds 8 px baselines.
//! HEADLINE_TRACKING_EM defaults to -0.02.
use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;

const W: u32 = 1600;
const H: u32 = 1120;
const M: f64 = 80.0;
const LIGHT: Color = Color {
    r: 222,
    g: 222,
    b: 222,
    a: 255,
};
const DARK: Color = Color {
    r: 68,
    g: 68,
    b: 68,
    a: 255,
};
const WEIGHTS: [f32; 3] = [400.0, 550.0, 700.0];
const WGHT: u32 = u32::from_be_bytes(*b"wght");

// Layout and guide rendering share these dimensions. The overlay visualizes
// the actual content modules; it is not a decorative grid laid over the page.
struct ReviewGrid {
    columns: usize,
    rows: usize,
    field_x: f64,
    field_width: f64,
    column_width: f64,
    column_gutter: f64,
    body_top: f64,
    body_bottom: f64,
    row_height: f64,
    row_gutter: f64,
}

impl ReviewGrid {
    fn new(columns: usize, detail: bool) -> Self {
        let field_x = M + 128.0 + 32.0;
        let field_width = W as f64 - M - field_x;
        let column_gutter = if columns == 3 { 64.0 } else { 32.0 };
        let column_width = (field_width - column_gutter * (columns - 1) as f64) / columns as f64;
        let rows = if detail { 2 } else { 3 };
        let body_top = 312.0;
        let body_bottom = H as f64 - M - 24.0;
        let row_gutter = if detail { 96.0 } else { 64.0 };
        let row_height = (body_bottom - body_top - row_gutter * (rows - 1) as f64) / rows as f64;
        Self { columns, rows, field_x, field_width, column_width, column_gutter,
               body_top, body_bottom, row_height, row_gutter }
    }

    fn column_x(&self, index: usize) -> f64 {
        self.field_x + index as f64 * (self.column_width + self.column_gutter)
    }

    fn row_top(&self, index: usize) -> f64 {
        self.body_top + index as f64 * self.row_step()
    }

    fn row_step(&self) -> f64 { self.row_height + self.row_gutter }

    fn divider(&self, index: usize) -> f64 {
        self.row_top(index) + self.row_height + self.row_gutter / 2.0
    }

    fn guides(&self, c: &mut Canvas, ink: Color, baselines: bool) {
        c.fill(ink);
        if baselines {
            for y in (80..=1040).step_by(8) {
                c.rect(M, H as f64 - y as f64, W as f64 - 2.0 * M, 0.1);
            }
        }
        for x in [M, M + 128.0, self.field_x, W as f64 - M] {
            c.rect(x, M, 0.5, H as f64 - 2.0 * M);
        }
        for col in 0..self.columns {
            for x in [self.column_x(col), self.column_x(col) + self.column_width] {
                c.rect(x, M, 0.4, H as f64 - 2.0 * M);
            }
        }
        for y in [M, 224.0, 248.0, 304.0, self.body_bottom, H as f64 - M] {
            c.rect(M, H as f64 - y, W as f64 - 2.0 * M, 0.4);
        }
        for row in 0..self.rows {
            for y in [self.row_top(row), self.row_top(row) + self.row_height] {
                c.rect(M, H as f64 - y, W as f64 - 2.0 * M, 0.4);
            }
        }
    }
}

fn label(
    c: &mut Canvas,
    r: &Renderer,
    text: &str,
    x: f64,
    y: f64,
    size: f64,
    ink: Color,
    limit: f64,
    tracking: f64,
) {
    let width = r.text_width(text, Some("Virtua Grotesk"), size, &[(WGHT, 400.0)]);
    let tracked_width = width + tracking * text.chars().count().saturating_sub(1) as f64;
    assert!(tracked_width <= limit, "Label exceeds its column: {text}");
    c.fill(ink)
        .font("Virtua Grotesk")
        .clear_font_variations()
        .font_variation("wght", 400.0)
        .font_size(size)
        .tracking(tracking);
    c.text(text, x, H as f64 - y);
    c.tracking(0.0);
}

fn add_sample(
    c: &mut Canvas,
    r: &Renderer,
    family: &str,
    text: &str,
    weight: f32,
    size: f64,
    x: f64,
    baseline: f64,
    maximum: f64,
) {
    let width = r.text_width(text, Some(family), size, &[(WGHT, weight)]);
    assert!(
        width <= maximum,
        "Sample exceeds its column ({width} > {maximum}) at {size} px/em: {family} {weight} {text}"
    );
    c.font(family)
        .clear_font_variations()
        .font_variation("wght", weight)
        .font_size(size)
        .tracking(0.0)
        .text(text, x, H as f64 - baseline);
}

fn main() {
    let a: Vec<_> = env::args().collect();
    assert_eq!(
        a.len(),
        8,
        "theme sheet before.ttf after.ttf rubik.ttf noto.ttf applied|candidate"
    );
    assert!(matches!(a[1].as_str(), "light" | "dark"));
    assert!(matches!(
        a[2].as_str(),
        "form" | "text" | "weight" | "marks" | "detail-he" | "detail-het" | "detail-tav"
    ));
    assert!(matches!(a[7].as_str(), "applied" | "candidate"));
    let group = env::var("REVIEW_GROUP").unwrap_or("dalet-resh".into());
    assert!(matches!(
        group.as_str(),
        "dalet-resh" | "he-het-tav" | "he-het-tav-candidate"
    ));
    let next_group = group.starts_with("he-het-tav");
    let compare_group = group == "he-het-tav-candidate";
    let detail = a[2].starts_with("detail-");
    let form_size = if compare_group {
        136.0
    } else if next_group {
        160.0
    } else {
        192.0
    };
    let row_weights: &[f32] = if detail { &[400.0, 700.0] } else { &WEIGHTS };
    let form_text = if next_group { "החת" } else { "ד ר" };
    let reading_text = if next_group {
        "היה חיה תחיה"
    } else {
        "דרך חדר סדר"
    };
    let repeat_text = if next_group {
        "הח חה חת תח"
    } else {
        "דרדר רדרד"
    };
    let headline_em: f64 = env::var("HEADLINE_TRACKING_EM")
        .unwrap_or("-0.02".into())
        .parse()
        .expect("Numeric headline tracking");
    assert!(headline_em.is_finite() && (-0.05..=0.0).contains(&headline_em));
    let (paper, ink) = if a[1] == "light" {
        (LIGHT, DARK)
    } else {
        (DARK, LIGHT)
    };
    let (title, subtitle, folio, size_note, footer) = match a[2].as_str() {
        "form" => (
            if next_group {
                "He, Het and Tav"
            } else {
                "Dalet and Resh"
            },
            "Hebrew Letterforms",
            "01",
            if compare_group {
                "136 px per em"
            } else if next_group {
                "160 px per em"
            } else {
                "192 px per em"
            },
            "Equal scale and baseline. Weight coordinates are not optical matches.",
        ),
        "text" => (
            "Reading Texture",
            "Reading at Three Sizes",
            "02",
            "44, 32 and 24 px per em",
            "Read right to left within each column. Other Hebrew drawings remain unfinished.",
        ),
        "marks" => (
            "Marks and Related Forms",
            "Attachment and Standalone Forms",
            "07",
            "72 and 64 px per em",
            "Precomposed he and tav with dagesh remain unchanged in the third line.",
        ),
        "detail-he" | "detail-het" | "detail-tav" => (
            match a[2].as_str() {
                "detail-he" => "He",
                "detail-het" => "Het",
                _ => "Tav",
            },
            "Outline Detail",
            match a[2].as_str() {
                "detail-he" => "04",
                "detail-het" => "05",
                _ => "06",
            },
            "384 px per em",
            "Same scale and baseline. Exposed chamfers stay 16 font units in both masters.",
        ),
        _ => (
            "Latin and Hebrew",
            "Weight Across Scripts",
            "03",
            if next_group {
                "160 px per em"
            } else {
                "176 px per em"
            },
            "Equal scale and baseline. The cross-script weight relationship remains provisional.",
        ),
    };
    let mut r = Renderer::new(W, H);
    r.load_font(&a[4]).expect("Current Virtua label font");
    let mut c = Canvas::new(W as f64, H as f64);
    c.background(paper);
    // A label rail and a comparison field. The 8 px baseline unit supports
    // tight captions; 32/64 px gutters separate the comparison columns.
    let grid = ReviewGrid::new(if a[2] == "weight" || (next_group && !compare_group) { 3 } else { 4 }, detail);
    let field_x = grid.field_x;
    let field_width = grid.field_width;
    label(&mut c, &r, "Virtua Grotesk", M, 112.0, 18.0, ink, 144.0, 0.0);
    label(&mut c, &r, "Design Review", M, 136.0, 16.0, ink, 144.0, 0.0);
    label(&mut c, &r, title, field_x, 144.0, 56.0, ink, field_width, headline_em * 56.0);
    label(&mut c, &r, subtitle, field_x, 184.0, 20.0, ink, 800.0, 0.0);
    let size_width = r.text_width(size_note, Some("Virtua Grotesk"), 16.0, &[(WGHT, 400.0)]);
    label(&mut c, &r, size_note, W as f64 - M - size_width, 184.0, 16.0, ink, 360.0, 0.0);
    c.fill(ink).rect(field_x, H as f64 - 224.0, field_width, 1.0);
    let columns: Vec<(&str, &str, &str)> = if a[2] == "weight" {
        vec![
            ("Latin Lowercase", &a[4], "Virtua Grotesk"),
            ("Latin Capitals", &a[4], "Virtua Grotesk"),
            ("Hebrew", &a[4], "Virtua Grotesk"),
        ]
    } else if next_group && !compare_group {
        vec![
            ("Virtua Grotesk", &a[4], "Virtua Grotesk"),
            ("Rubik", &a[5], "Rubik"),
            ("Noto Sans Hebrew", &a[6], "Noto Sans Hebrew"),
        ]
    } else {
        vec![
            ("Virtua Grotesk", &a[3], "Virtua Grotesk"),
            ("Virtua Grotesk", &a[4], "Virtua Grotesk"),
            ("Rubik", &a[5], "Rubik"),
            ("Noto Sans Hebrew", &a[6], "Noto Sans Hebrew"),
        ]
    };
    let after_role = if a[7] == "applied" {
        "Applied"
    } else {
        "Candidate"
    };
    let roles = if a[2] == "weight" {
        vec!["Green Reference", "Green Reference", "Provisional Weight"]
    } else if next_group && !compare_group {
        vec!["Current", "Reference", "Reference"]
    } else {
        vec!["Before", after_role, "Reference", "Reference"]
    };
    assert_eq!(columns.len(), grid.columns);
    let column_width = grid.column_width;
    for (col, (name, _, _)) in columns.iter().enumerate() {
        let x = grid.column_x(col);
        label(&mut c, &r, name, x, 272.0, 22.0, ink, column_width, 0.0);
        label(&mut c, &r, roles[col], x, 296.0, 16.0, ink, column_width, 0.0);
    }
    let first_baseline = match a[2].as_str() {
        "form" => 432.0,
        "text" | "weight" => 448.0,
        "marks" => 480.0,
        _ => 560.0,
    };
    let row_step = grid.row_step();
    let center_offset = match a[2].as_str() {
        "form" => form_size * 0.28,
        "text" => 56.0,
        "weight" => 64.0,
        "marks" => 80.0,
        _ => 112.0,
    };
    for (row, weight) in row_weights.iter().enumerate() {
        let center = first_baseline + row as f64 * row_step - center_offset;
        let y = ((center - 8.0) / 8.0).round() * 8.0;
        let name = if detail { ["Regular", "Bold"][row] }
                   else { ["Regular", "Midpoint", "Bold"][row] };
        label(&mut c, &r, name, M, y, 20.0, ink, 128.0, 0.0);
        label(&mut c, &r, &format!("{weight:.0}"), M, y + 24.0, 16.0, ink, 128.0, 0.0);
        if row + 1 < row_weights.len() {
            let divider = grid.divider(row);
            c.fill(ink).rect(field_x, H as f64 - divider, field_width, 0.5);
        }
    }
    for (col, (_, path, family)) in columns.iter().enumerate() {
        // One font per renderer: before/after never share a font collection.
        let mut sample_r = Renderer::new(W, H);
        sample_r.load_font(path).expect("Explicit sample font");
        let mut sample_c = Canvas::new(W as f64, H as f64);
        sample_c.background(Color {
            r: 0,
            g: 0,
            b: 0,
            a: 0,
        });
        sample_c.fill(ink);
        let x = grid.column_x(col);
        for (row, weight) in row_weights.iter().enumerate() {
            let baseline = first_baseline + row as f64 * row_step;
            let samples: Vec<(&str, f64, f64)> = match a[2].as_str() {
                "form" => vec![(form_text, form_size, baseline)],
                "marks" => vec![
                    ("הָ חַ תֵ", 72.0, baseline - 120.0),
                    ("הּ חִ תַ", 64.0, baseline - 56.0),
                    ("הּ תּ", 64.0, baseline),
                ],
                "detail-he" => vec![("ה", 384.0, baseline)],
                "detail-het" => vec![("ח", 384.0, baseline)],
                "detail-tav" => vec![("ת", 384.0, baseline)],
                "text" => vec![
                    (reading_text, 44.0, baseline - 80.0),
                    (repeat_text, 32.0, baseline - 40.0),
                    (reading_text, 24.0, baseline),
                ],
                _ => vec![(
                    ["n o", "H O", form_text][col],
                    if next_group { 160.0 } else { 176.0 },
                    baseline,
                )],
            };
            for (text, size, y) in samples {
                add_sample(
                    &mut sample_c,
                    &sample_r,
                    family,
                    text,
                    *weight,
                    size,
                    x,
                    y,
                    column_width,
                );
            }
        }
        let mut pixels = sample_r.render_frames(&sample_c).remove(0).0;
        // Validate actual ink as well as advances, before native-size composition.
        for (i, pixel) in pixels.chunks_exact_mut(4).enumerate() {
            if pixel[3] != 0 {
                let px = (i % W as usize) as f64;
                let py = (i / W as usize) as f64;
                assert!(
                    px >= x - 8.0 && px < x + column_width + 1.0,
                    "Sample ink leaves its column"
                );
                assert!(
                    py >= 312.0 && py < 1016.0,
                    "Sample ink collides with page furniture"
                );
            }
            // render_frames is premultiplied in this backend; image_rgba wants
            // straight alpha. Restore known monochrome RGB, preserving coverage.
            pixel[0] = ink.r;
            pixel[1] = ink.g;
            pixel[2] = ink.b;
        }
        c.image_rgba(pixels, W, H, 0.0, 0.0, 1.0);
    }
    c.fill(ink).rect(field_x, H as f64 - 1016.0, field_width, 1.0);
    label(&mut c, &r, folio, M, 1040.0, 16.0, ink, 128.0, 0.0);
    label(&mut c, &r, footer, field_x, 1040.0, 16.0, ink, field_width, 0.0);
    let grid_view = env::var("GRID_VIEW").unwrap_or("0".into());
    assert!(matches!(grid_view.as_str(), "0" | "1" | "baseline"));
    if grid_view != "0" {
        grid.guides(&mut c, ink, grid_view == "baseline");
    }
    r.render_to_png(&c, "out.png").expect("Raw specimen render");
}
