//! Canonical three-sheet review layout. See documentation/qa.md.
//! designbot --raw documentation/proofs/hebrew_review.rs --output OUT.png -- light form BEFORE.ttf AFTER.ttf RUBIK.ttf NOTO.ttf applied
//! sheet: form | text | weight; theme: light | dark; state: applied | candidate
//! REVIEW_GROUP=he-het-tav selects a current/reference review without a candidate.
//! GRID_VIEW=1 overlays the grid. HEADLINE_TRACKING_EM defaults to -0.02.
use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;

const W: u32 = 1600;
const H: u32 = 1280;
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
        "Sample exceeds its column at {size} px/em: {text}"
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
        120.0
    } else if next_group {
        160.0
    } else {
        192.0
    };
    let row_weights: &[f32] = if detail { &[400.0, 700.0] } else { &WEIGHTS };
    let form_text = if next_group { "ה ח ת" } else { "ד ר" };
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
                "120 px per em"
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
            "Bottom line: precomposed he and tav with dagesh remain unchanged.",
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
    label(
        &mut c,
        &r,
        "Virtua Grotesk",
        M,
        120.0,
        20.0,
        ink,
        600.0,
        0.0,
    );
    label(
        &mut c,
        &r,
        "Design Review",
        800.0,
        120.0,
        20.0,
        ink,
        600.0,
        0.0,
    );
    let folio_width = r.text_width(folio, Some("Virtua Grotesk"), 20.0, &[(WGHT, 400.0)]);
    label(
        &mut c,
        &r,
        folio,
        W as f64 - M - folio_width,
        120.0,
        20.0,
        ink,
        80.0,
        0.0,
    );
    label(
        &mut c,
        &r,
        title,
        M,
        200.0,
        64.0,
        ink,
        1440.0,
        headline_em * 64.0,
    );
    label(&mut c, &r, subtitle, M, 240.0, 22.0, ink, 1000.0, 0.0);
    let size_width = r.text_width(size_note, Some("Virtua Grotesk"), 18.0, &[(WGHT, 400.0)]);
    label(
        &mut c,
        &r,
        size_note,
        W as f64 - M - size_width,
        240.0,
        18.0,
        ink,
        400.0,
        0.0,
    );
    c.fill(ink).rect(M, H as f64 - 280.0, 1440.0, 1.0);
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
    let cell = 1440.0 / columns.len() as f64;
    for (col, (name, _, _)) in columns.iter().enumerate() {
        let x = M + col as f64 * cell;
        label(&mut c, &r, name, x, 320.0, 26.0, ink, cell - 40.0, 0.0);
        label(
            &mut c,
            &r,
            roles[col],
            x,
            360.0,
            18.0,
            ink,
            cell - 40.0,
            0.0,
        );
    }
    for (row, weight) in row_weights.iter().enumerate() {
        let y = 400.0 + row as f64 * if detail { 400.0 } else { 240.0 };
        let name = if detail {
            ["Regular", "Bold"][row]
        } else {
            ["Regular", "Midpoint", "Bold"][row]
        };
        label(&mut c, &r, name, M, y, 20.0, ink, 150.0, 0.0);
        label(
            &mut c,
            &r,
            &format!("{weight:.0}"),
            240.0,
            y,
            18.0,
            ink,
            100.0,
            0.0,
        );
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
        let x = M + col as f64 * cell;
        for (row, weight) in row_weights.iter().enumerate() {
            let baseline = if detail {
                680.0 + row as f64 * 400.0
            } else {
                600.0 + row as f64 * 240.0
            };
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
                    cell - 40.0,
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
                    px >= x - 8.0 && px < x + cell - 24.0,
                    "Sample ink leaves its column"
                );
                assert!(
                    py >= 424.0 && py < 1140.0,
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
    c.fill(ink).rect(M, H as f64 - 1160.0, 1440.0, 1.0);
    label(&mut c, &r, footer, M, 1200.0, 18.0, ink, 1280.0, 0.0);
    let theme_label = if a[1] == "light" { "Light" } else { "Dark" };
    let theme_width = r.text_width(theme_label, Some("Virtua Grotesk"), 18.0, &[(WGHT, 400.0)]);
    label(
        &mut c,
        &r,
        theme_label,
        W as f64 - M - theme_width,
        1200.0,
        18.0,
        ink,
        100.0,
        0.0,
    );
    if env::var("GRID_VIEW").as_deref() == Ok("1") {
        for x in (80..=1520).step_by(40) {
            c.fill(ink).rect(x as f64, 80.0, 0.25, 1120.0);
        }
        for y in (80..=1200).step_by(40) {
            c.fill(ink).rect(80.0, y as f64, 1440.0, 0.25);
        }
    }
    r.render_to_png(&c, "out.png").expect("Raw specimen render");
}
