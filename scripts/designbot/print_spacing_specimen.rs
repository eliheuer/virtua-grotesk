// Landscape PDF specimen for print weight and spacing review.
//
// designbot port of scripts/build_print_spacing_specimen.py (drawbot-skia).
// Grid math from scripts/grid_system.py is inlined below (designbot scripts
// are single-file). designbot uses DrawBot's coordinate system (origin at the
// BOTTOM-LEFT, y increasing upward), so every vertical coordinate here
// matches the Python original's value directly.
//
// Run from the repo root:
//   designbot --render scripts/designbot/print_spacing_specimen.rs \
//     --output documentation/proofs/print-spacing-specimen.pdf
//
// GRID_VIEW=1 in the environment draws the modular grid overlay, matching
// the grid_system.py idiom.

use designbot::prelude::*;
use std::collections::HashMap;

// --- page geometry (grid_system.Grid(792, 612, margin=36) => unit 18) ------
const PAGE_W: f64 = 792.0;
const PAGE_H: f64 = 612.0;
const MARGIN: f64 = 36.0;
const UNIT: f64 = 18.0;

/// X position `units` right of the left margin line.
fn gx(units: f64) -> f64 {
    MARGIN + units * UNIT
}

/// Y position `units` below the top margin line (grid_system's y_top()).
fn gy_top(units: f64) -> f64 {
    PAGE_H - MARGIN - units * UNIT
}

// Main text frame (Python: x(10), y(0), 30 x 29 units).
const MAIN_W: f64 = UNIT * 30.0; // 540
const MAIN_H: f64 = UNIT * 29.0; // 522

// --- fonts ------------------------------------------------------------------
// The four statics share ambiguous family naming (Regular and Bold are both
// family "Virtua Grotesk"; Medium/SemiBold have style-specific family names),
// so the port loads the variable font once and selects weights via wght.
const VF_PATH: &str = "fonts/variable/VirtuaGrotesk[wght].ttf";
const VG_FAMILY: &str = "Virtua Grotesk";
const WGHT: u32 = u32::from_be_bytes(*b"wght");

// Chrome text uses the system Courier family, like the Python original.
const MONO_FAMILY: &str = "Courier";
const MONO_SIZE: f64 = 10.0;

// --- proof text -------------------------------------------------------------
const LATIN_LOWER: &str = "abcdefghijklmnopqrstuvwxyz";
const LATIN_UPPER: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const LATIN_DIGITS: &str = "0123456789";
const LATIN_PUNCT: &str = ".,:;!?/\\-\u{2013}\u{2014}'\"()[]{}";

const BASIC_SPACING_LINES: [&str; 24] = [
    "mimic minimum aluminum animal banana canal cinema dilemma",
    "button sudden hidden ladder middle runner summer tunnel",
    "office affine waffle suffer different effort staff traffic",
    "round crown narrow rhythm thrown weather washer whistle",
    "paper proper pepper upper appear prepare copper zipper",
    "garden agenda edge judge bridge degree gadget budget",
    "heavy behave velvet vivid reviver avenue woven wave",
    "quick equal opaque square antique request quiet unique",
    "frozen zebra lazy dizzy jazz puzzle buzzard zigzag",
    "cliff scale local logical occult account circle cycle",
    "hard shoulder rhythm alphabet method brother bother",
    "story system steady studio status stainless stress",
    "TYPE WATERFALL SPACING RHYTHM TEXTURE LETTERS",
    "HAMBURGEFONTSIV MINIMUM MAXIMUM RHYTHM REVIEW",
    "naive active civic vivid divide individual invitation",
    "orange control corridor record border northern honor",
    "label reliable available village illegal parallel tall",
    "market remark framework maker kerning tracking texture",
    "system stress status stories sister assist session",
    "visual review proof print paper press process",
    "weight width white window woven awkward onward",
    "quiet quality equal square liquid sequel antique",
    "face affine cafe office efficient coefficient traffic",
    "type rhythm texture system spacing kerning proof",
];

const DOUBLE_TEST_LINES: [&str; 16] = [
    "Hassel Nibble Riddle Saffron Tunnel Pepper Llama",
    "Haggard Bookkeeper Coffee Toffee Office Affinity",
    "Bamboo Balloon Beetle Bubble Butter Succeed",
    "Added Oddity Middle Saddle Fiddle Hidden Sudden",
    "Puzzle Fizz Jazz Buzz Fuzzy Dazzle Sizzle",
    "AARDVARK NIBBLE RIDDLE SAFFRON TUNNEL PEPPER",
    "BOOKKEEPER COFFEE TOFFEE OFFICE AFFINITY",
    "BALLOON BEETLE BUBBLE BUTTER SUCCEED PUZZLE",
    "MIDDLE SADDLE FIDDLE HIDDEN SUDDEN ADDED ODDITY",
    "PUZZLE FIZZ JAZZ BUZZ FUZZY DAZZLE SIZZLE",
    "little letter cellar follow mellow pillow yellow",
    "committee coffee toffee staff office official",
    "copper zipper pepper upper appear appraise",
    "runner tunnel sudden hidden middle fiddle",
    "fuzzy dizzy puzzle sizzle dazzle jazz buzz",
    "minimum maximum mammal common summer hammer",
];

const LOWER_CONTEXTS: &str = "abcdefghijklmnopqrstuvwxyz";
const RIGHT_CONTEXTS: &str = "aeionrumlhspdftckbgwyvzqxj";
const LEFT_CONTEXTS: &str = "haeionrumlspdftckbgwyvzqxj";

const ARABIC_SAMPLES: [(&str, &str); 6] = [
    ("shaping", "\u{628}\u{633}\u{645} \u{627}\u{644}\u{644}\u{647} \u{627}\u{644}\u{631}\u{62D}\u{645}\u{646} \u{627}\u{644}\u{631}\u{62D}\u{64A}\u{645}"),
    ("letters", "\u{633}\u{644}\u{627}\u{645} \u{627}\u{644}\u{639}\u{631}\u{628}\u{64A}\u{629} \u{643}\u{62A}\u{627}\u{628} \u{642}\u{644}\u{645} \u{645}\u{62F}\u{64A}\u{646}\u{629}"),
    ("persian/urdu", "\u{67E} \u{686} \u{698} \u{6AF} \u{6A9} \u{6CC} \u{6C1} \u{6BE} \u{6D2}"),
    ("marks", "\u{628}\u{64E} \u{628}\u{64F} \u{628}\u{650} \u{628}\u{651} \u{628}\u{652} \u{628}\u{64B} \u{628}\u{64C} \u{628}\u{64D}"),
    ("digits", "\u{660}\u{661}\u{662}\u{663}\u{664}\u{665}\u{666}\u{667}\u{668}\u{669}  \u{6F0}\u{6F1}\u{6F2}\u{6F3}\u{6F4}\u{6F5}\u{6F6}\u{6F7}\u{6F8}\u{6F9}"),
    ("punctuation", "\u{60C} \u{61B} \u{61F} \u{66A} \u{66B} \u{66C} \u{60D} \u{6D4}"),
];

const KERN_KING_TEXT: &str = concat!(
    "lynx tuft frogs, dolphins abduct by proxy the ever awkward klutz, dud, ",
    "dummkopf, jinx snubnose filmgoer, orphan sgt. renfruw grudgek reyfus, ",
    "md. sikh psych if halt tympany jewelry sri heh! twyer vs jojo pneu ",
    "fylfot alcaaba son of nonplussed halfbreed bubbly playboy guggenheim ",
    "daddy coccyx sgraffito effect, vacuum dirndle impossible attempt to ",
    "disvalue, muzzle the afghan czech czar and exninja, bob bixby dvorak ",
    "wood dhurrie savvy, dizzy eye aeon circumcision uvula scrungy picnic ",
    "luxurious special type carbohydrate ovoid adzuki kumquat bomb? afterglows ",
    "gold girl pygmy gnome lb. ankhs acme aggroupment akmed brouhha tv wt. ",
    "ujjain ms. oz abacus mnemonics bhikku khaki bwana aorta embolism vivid ",
    "owls often kvetch otherwise, wysiwyg densfort wright you've absorbed ",
    "rhythm, put obstacle kyaks krieg kern wurst subject enmity equity coquet ",
    "quorum pique tzetse hepzibah sulfhydryl briefcase ajax ehler kafka fjord ",
    "elfship halfdressed jugful eggcup hummingbirds swingdevil bagpipe legwork ",
    "reproachful hunchback archknave baghdad wejh rijswijk rajbansi rajput ",
    "ajdir okay weekday obfuscate subpoena liebknecht marcgravia ecbolic ",
    "arcticward dickcissel pincpinc boldface maidkin adjective adcraft adman ",
    "dwarfness applejack darkbrown kiln palzy always farmland flimflam unbossy ",
    "nonlineal stepbrother lapdog stopgap sx countdown basketball beaujolais ",
    "vb. flowchart aztec lazy bozo syrup tarzan annoying dyke yucky hawg ",
    "gagzhukz cuzco squire when hiho mayhem nietzsche szasz gumdrop milk ",
    "emplotment ambidextrously lacquer byway ecclesiastes stubchen hobgoblins ",
    "crabmill aqua hawaii blvd. subquality byzantine empire debt obvious ",
    "cervantes jekabzeel anecdote flicflac mechanicville bedbug couldn't i've ",
    "it's they'll they'd dpt. headquarter burkhardt xerxes atkins govt. ",
    "ebenezer lg. lhama amtrak amway fixity axmen quumbabda upjohn hrumpf",
);

// --- proof text builders ----------------------------------------------------

fn repeat_char(c: char, n: usize) -> String {
    std::iter::repeat(c).take(n).collect()
}

fn adjacency_matrix_text(chars: &str) -> String {
    let cs: Vec<char> = chars.chars().collect();
    let control_pair = |a: char, b: char| -> String {
        [
            repeat_char(a, 3),
            repeat_char(b, 3),
            repeat_char(a, 2),
            repeat_char(b, 2),
            repeat_char(a, 1),
            repeat_char(b, 1),
            repeat_char(a, 1),
            repeat_char(b, 2),
            repeat_char(a, 2),
            repeat_char(b, 3),
            repeat_char(a, 3),
        ]
        .concat()
    };
    let mut lines = vec![control_pair(cs[13], cs[14]), control_pair(cs[7], cs[14])];
    for &left in &cs {
        let mut row = String::new();
        for &right in &cs {
            row.push(left);
            row.push(right);
            row.push(left);
        }
        lines.push(row);
    }
    lines.join("\n")
}

fn punctuation_matrix_text(chars: &str) -> String {
    let joined: Vec<String> = chars.chars().map(|c| c.to_string()).collect();
    LATIN_PUNCT
        .chars()
        .map(|punct| {
            let p = punct.to_string();
            format!("{}{}{}", p, joined.join(&p), p)
        })
        .collect::<Vec<_>>()
        .join("\n")
}

fn number_matrix_text() -> String {
    let digits: Vec<char> = LATIN_DIGITS.chars().collect();
    let mut digit_rows = vec!["00011100110101100111000".to_string()];
    for &left in &digits {
        let mut row = String::new();
        for &right in &digits {
            row.push(left);
            row.push(right);
            row.push(left);
        }
        digit_rows.push(row);
    }
    let joined: Vec<String> = digits.iter().map(|c| c.to_string()).collect();
    let interleave = |op: char| -> String {
        let p = op.to_string();
        format!("{}{}{}", p, joined.join(&p), p)
    };
    let operator_rows: Vec<String> = "+-\u{B1}\u{D7}\u{F7}=/".chars().map(interleave).collect();
    let currency_rows: Vec<String> = "\u{B0}$\u{20AC}\u{A3}#%".chars().map(interleave).collect();
    let punctuation_rows: Vec<String> = digits
        .iter()
        .map(|d| format!("{d}% {d}\u{2030} {d}-{d}.{d},{d}\u{2026}{d}\u{B0}"))
        .collect();
    [
        digit_rows.join("\n"),
        operator_rows.join("\n"),
        currency_rows.join("\n"),
        punctuation_rows.join("\n"),
    ]
    .join("\n\n")
}

fn context_pair(letter: char) -> (String, String) {
    let right = RIGHT_CONTEXTS
        .chars()
        .filter(|&c| c != letter)
        .map(|c| format!("{letter}{c}"))
        .collect::<Vec<_>>()
        .join(" ");
    let left = LEFT_CONTEXTS
        .chars()
        .filter(|&c| c != letter)
        .map(|c| format!("{c}{letter}"))
        .collect::<Vec<_>>()
        .join(" ");
    (format!("{letter}+  {right}"), format!("+{letter}  {left}"))
}

fn context_strings_text(letters: &str) -> String {
    let mut lines = Vec::new();
    for letter in letters.chars() {
        let (right, left) = context_pair(letter);
        lines.push(right);
        lines.push(left);
        lines.push(String::new());
    }
    lines.join("\n")
}

// --- font metadata (glyph count from the TTF maxp table) --------------------

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

fn glyph_count(data: &[u8]) -> u16 {
    match find_table(data, b"maxp") {
        Some(off) if off + 6 <= data.len() => read_u16(data, off + 4),
        _ => 0,
    }
}

/// Codepoints covered by the font's cmap (formats 4 and 12). Used to detect
/// characters that would trigger system-font fallback, which needs the
/// segmented drawing workaround below.
fn cmap_codepoints(data: &[u8]) -> std::collections::HashSet<u32> {
    let mut set = std::collections::HashSet::new();
    let Some(cmap) = find_table(data, b"cmap") else {
        return set;
    };
    if cmap + 4 > data.len() {
        return set;
    }
    let num_records = read_u16(data, cmap + 2) as usize;
    for i in 0..num_records {
        let rec = cmap + 4 + i * 8;
        if rec + 8 > data.len() {
            break;
        }
        let subtable = cmap + read_u32(data, rec + 4) as usize;
        if subtable + 2 > data.len() {
            continue;
        }
        match read_u16(data, subtable) {
            4 => {
                let seg_count = read_u16(data, subtable + 6) as usize / 2;
                let end_codes = subtable + 14;
                let start_codes = end_codes + seg_count * 2 + 2; // +2 reservedPad
                for s in 0..seg_count {
                    let end = read_u16(data, end_codes + s * 2) as u32;
                    let start = read_u16(data, start_codes + s * 2) as u32;
                    if start == 0xFFFF {
                        continue;
                    }
                    for c in start..=end.min(0xFFFE) {
                        set.insert(c);
                    }
                }
            }
            12 => {
                let n_groups = read_u32(data, subtable + 12) as usize;
                for g in 0..n_groups {
                    let rec = subtable + 16 + g * 12;
                    if rec + 12 > data.len() {
                        break;
                    }
                    let start = read_u32(data, rec);
                    let end = read_u32(data, rec + 4);
                    for c in start..=end.min(start + 0xFFFF) {
                        set.insert(c);
                    }
                }
            }
            _ => {}
        }
    }
    set
}

/// Local date as YYYY-MM-DD (matches Python's datetime.now()); the generated
/// script project has no chrono, so shell out to `date` with a UTC fallback.
fn today() -> String {
    if let Ok(out) = std::process::Command::new("date").arg("+%Y-%m-%d").output() {
        if out.status.success() {
            let s = String::from_utf8_lossy(&out.stdout).trim().to_string();
            if !s.is_empty() {
                return s;
            }
        }
    }
    // Fallback: UTC civil date from the epoch (Howard Hinnant's algorithm).
    let secs = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0);
    let z = secs.div_euclid(86_400) + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146_096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = if m <= 2 { y + 1 } else { y };
    format!("{:04}-{:02}-{:02}", y, m, d)
}

fn grid_view() -> bool {
    matches!(
        std::env::var("GRID_VIEW").unwrap_or_default().to_lowercase().as_str(),
        "1" | "true" | "yes" | "on"
    )
}

// --- text measuring / wrapping ----------------------------------------------

/// Greedy word wrap in Virtua Grotesk at (size, wght), mirroring drawbot-skia
/// textBox: split on \n (blank lines kept), wrap overlong lines on spaces.
fn wrap_text(renderer: &Renderer, text: &str, size: f64, wght: f32, max_w: f64) -> Vec<String> {
    let vars = [(WGHT, wght)];
    let measure = |s: &str| renderer.text_width(s, Some(VG_FAMILY), size, &vars);
    // Trailing whitespace is trimmed by the layouter, so derive the space
    // advance from a spaced pair.
    let space_w = measure("n n") - 2.0 * measure("n");

    let mut out = Vec::new();
    for raw in text.split('\n') {
        if raw.is_empty() {
            out.push(String::new());
            continue;
        }
        if measure(raw) <= max_w {
            out.push(raw.to_string());
            continue;
        }
        let mut cache: HashMap<&str, f64> = HashMap::new();
        let mut cur = String::new();
        let mut cur_w = 0.0;
        for word in raw.split(' ') {
            let w = *cache.entry(word).or_insert_with(|| measure(word));
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
    }
    out
}

// --- drawing helpers ----------------------------------------------------------

/// Chrome (Courier) text with its BASELINE at `baseline`.
fn mono_text(ctx: &mut Canvas, s: &str, x: f64, baseline: f64) {
    ctx.font(MONO_FAMILY);
    ctx.clear_font_variations();
    ctx.font_size(MONO_SIZE);
    ctx.fill(Color::black());
    ctx.text(s, x, baseline);
}

/// Virtua Grotesk text at (size, wght) with its BASELINE at `baseline`.
fn vg_text(ctx: &mut Canvas, s: &str, x: f64, baseline: f64, size: f64, wght: f32) {
    ctx.font(VG_FAMILY);
    ctx.clear_font_variations();
    ctx.font_variation("wght", wght);
    ctx.font_size(size);
    ctx.fill(Color::black());
    ctx.text(s, x, baseline);
}

/// GRID_VIEW overlay: the modular grid from grid_system.Grid.draw() (major
/// horizontals count up from the BOTTOM margin line, as in the Python).
fn draw_grid_overlay(ctx: &mut Canvas) {
    let minor = Color::rgba(255, 0, 0, 71);
    let major = Color::rgba(255, 0, 0, 140);
    let frame = Color::rgba(255, 0, 0, 217);
    let units_x = ((PAGE_W - 2.0 * MARGIN) / UNIT + 0.5) as i32; // 40
    let units_y = ((PAGE_H - 2.0 * MARGIN) / UNIT + 0.5) as i32; // 30

    ctx.save();
    ctx.no_fill();
    ctx.stroke_width(1.0);

    ctx.stroke(minor);
    for i in 0..=units_x {
        let x = gx(i as f64);
        ctx.line(x, MARGIN, x, PAGE_H - MARGIN);
    }
    for i in 0..=units_y {
        let y = MARGIN + i as f64 * UNIT;
        ctx.line(MARGIN, y, PAGE_W - MARGIN, y);
    }

    ctx.stroke(major);
    for i in (0..=units_x).step_by(4) {
        let x = gx(i as f64);
        ctx.line(x, MARGIN, x, PAGE_H - MARGIN);
    }
    for i in (0..=units_y).step_by(4) {
        let y = MARGIN + i as f64 * UNIT;
        ctx.line(MARGIN, y, PAGE_W - MARGIN, y);
    }

    ctx.stroke_width(2.0);
    ctx.stroke(frame);
    ctx.rect(MARGIN, MARGIN, PAGE_W - 2.0 * MARGIN, PAGE_H - 2.0 * MARGIN);
    ctx.line(PAGE_W / 2.0, 0.0, PAGE_W / 2.0, PAGE_H);
    ctx.line(0.0, PAGE_H / 2.0, PAGE_W, PAGE_H / 2.0);
    ctx.restore();
}

struct PageChrome {
    date: String,
    glyphs: u16,
    page_num: usize,
}

impl PageChrome {
    /// Header rules, page number, running head, and sidebar. Same layout as
    /// the Python:
    ///   header rule  y_top(1)          -> 558
    ///   header text  baseline rule+3up -> 561
    ///   bottom rule  MARGIN            -> 36
    ///   sidebar title y_top(3)+3       -> 525
    ///   sidebar meta  y_top(6)+3       -> 471 (-18 per following line)
    fn draw(&mut self, ctx: &mut Canvas, style: &str, title: &str, size: f64) {
        self.page_num += 1;
        ctx.background(Color::white());
        if grid_view() {
            draw_grid_overlay(ctx);
        }

        let header_rule_y = gy_top(1.0); // 558
        let header_baseline = header_rule_y + 3.0; // 561
        let bottom_rule_y = MARGIN; // 36
        // Python: SIDEBAR_TITLE_Y = y_top(3) + 3 = 525
        let sidebar_title_baseline = gy_top(3.0) + 3.0;
        // Python: SIDEBAR_META_Y = y_top(6) + 3 = 471
        let sidebar_meta_baseline = gy_top(6.0) + 3.0;

        ctx.save();
        ctx.stroke(Color::black());
        ctx.stroke_width(1.0);
        ctx.line(MARGIN, header_rule_y, PAGE_W - MARGIN, header_rule_y);
        ctx.line(MARGIN, bottom_rule_y, PAGE_W - MARGIN, bottom_rule_y);
        ctx.restore();

        ctx.save();
        mono_text(ctx, &self.page_num.to_string(), MARGIN, header_baseline);
        mono_text(ctx, &format!("{VG_FAMILY} {style}"), gx(10.0), header_baseline);
        mono_text(ctx, &self.date, gx(24.0), header_baseline);
        mono_text(ctx, "Font Engineer: Eli Heuer", gx(32.0), header_baseline);

        mono_text(
            ctx,
            &format!("{}pt {}", size, title),
            MARGIN,
            sidebar_title_baseline,
        );
        mono_text(ctx, &format!("Style: {style}"), MARGIN, sidebar_meta_baseline);
        mono_text(
            ctx,
            &format!("Glyphs: {}", self.glyphs),
            MARGIN,
            sidebar_meta_baseline - UNIT,
        );
        mono_text(
            ctx,
            "Grid: 18pt unit",
            MARGIN,
            sidebar_meta_baseline - UNIT * 2.0,
        );
        ctx.restore();
    }
}

/// Draw one line left-to-right, splitting it into manually-advanced segments
/// so that characters missing from Virtua Grotesk (which parley shapes with a
/// system fallback font, i.e. a separate glyph run) still land at the right
/// x position despite the designbot renderer dropping per-run line offsets.
/// Spaces are advanced explicitly because the layouter trims trailing spaces
/// when measuring.
#[allow(clippy::too_many_arguments)]
fn vg_text_segmented(
    ctx: &mut Canvas,
    renderer: &Renderer,
    cmap: &std::collections::HashSet<u32>,
    line: &str,
    x: f64,
    baseline: f64,
    size: f64,
    wght: f32,
) {
    let vars = [(WGHT, wght)];
    let measure = |s: &str| renderer.text_width(s, Some(VG_FAMILY), size, &vars);
    let space_w = measure("n n") - 2.0 * measure("n");

    let mut cursor = x;
    let mut seg = String::new();
    let mut flush = |ctx: &mut Canvas, seg: &mut String, cursor: &mut f64| {
        if !seg.is_empty() {
            vg_text(ctx, seg, *cursor, baseline, size, wght);
            *cursor += measure(seg);
            seg.clear();
        }
    };
    for c in line.chars() {
        if c == ' ' {
            flush(ctx, &mut seg, &mut cursor);
            cursor += space_w;
        } else if cmap.contains(&(c as u32)) {
            seg.push(c);
        } else {
            flush(ctx, &mut seg, &mut cursor);
            let s = c.to_string();
            vg_text(ctx, &s, cursor, baseline, size, wght);
            cursor += measure(&s);
        }
    }
    flush(ctx, &mut seg, &mut cursor);
}

/// A standard proof page: chrome plus a wrapped text block in the main frame.
/// Mirrors drawbot-skia textBox: first baseline sits `size` below the frame
/// top, baselines step by `leading`, and lines past floor(height/leading)
/// are dropped.
#[allow(clippy::too_many_arguments)]
fn proof_page(
    ctx: &mut Canvas,
    renderer: &Renderer,
    cmap: &std::collections::HashSet<u32>,
    chrome: &mut PageChrome,
    style: &str,
    wght: f32,
    title: &str,
    text: &str,
    size: f64,
    leading: f64,
) {
    chrome.draw(ctx, style, title, size);

    let main_x = gx(10.0); // 216
    let frame_top = gy_top(1.0); // 558 (frame top == header rule)
    let lines = wrap_text(renderer, text.trim(), size, wght, MAIN_W);
    let max_lines = (MAIN_H / leading).floor() as usize;
    for (i, line) in lines.iter().take(max_lines).enumerate() {
        if line.is_empty() {
            continue;
        }
        let baseline = frame_top - size - i as f64 * leading;
        if line.chars().all(|c| c == ' ' || cmap.contains(&(c as u32))) {
            vg_text(ctx, line, main_x, baseline, size, wght);
        } else {
            vg_text_segmented(ctx, renderer, cmap, line, main_x, baseline, size, wght);
        }
    }
}

/// Draw a right-aligned RTL line token by token, in logical order from the
/// right edge leftwards.
///
/// Workaround for a designbot renderer gap: within one text() call every
/// glyph run of a line is positioned from x=0 (the run's own line offset is
/// dropped), so any line that shapes to multiple bidi runs — Arabic plus
/// digits or punctuation — collapses its runs on top of each other. Each
/// space-separated token here is a single run, laid out manually.
fn draw_rtl_line(
    ctx: &mut Canvas,
    renderer: &Renderer,
    sample: &str,
    right_edge: f64,
    baseline: f64,
    size: f64,
    wght: f32,
) {
    let vars = [(WGHT, wght)];
    let measure = |s: &str| renderer.text_width(s, Some(VG_FAMILY), size, &vars);
    let space_w = measure("\u{628} \u{628}") - 2.0 * measure("\u{628}");
    let mut x_right = right_edge;
    for token in sample.split(' ') {
        if token.is_empty() {
            // Consecutive spaces in the source string.
            x_right -= space_w;
            continue;
        }
        let w = measure(token);
        vg_text(ctx, token, x_right - w, baseline, size, wght);
        x_right -= w + space_w;
    }
}

/// Arabic page: Courier label on the left, RTL sample right-aligned to the
/// main frame's right edge. As in the Python, label rows start at y_top(3)
/// and step down 4 units per row; the sample baseline sits 1 unit lower.
fn arabic_grid_page(
    ctx: &mut Canvas,
    renderer: &Renderer,
    chrome: &mut PageChrome,
    style: &str,
    wght: f32,
) {
    chrome.draw(ctx, style, "Arabic Strings", 18.0);

    let main_x = gx(10.0);
    let right_edge = main_x + MAIN_W; // 756
    let mut label_baseline = gy_top(3.0); // 522
    for (label, sample) in ARABIC_SAMPLES {
        mono_text(ctx, label, main_x, label_baseline);
        draw_rtl_line(ctx, renderer, sample, right_edge, label_baseline - UNIT, 18.0, wght);
        label_baseline -= UNIT * 4.0;
    }
}

// --- main ---------------------------------------------------------------------

fn main() {
    let mut ctx = Canvas::new(PAGE_W, PAGE_H);
    let mut renderer = Renderer::new(PAGE_W as u32, PAGE_H as u32);
    renderer
        .load_font(VF_PATH)
        .expect("failed to load fonts/variable/VirtuaGrotesk[wght].ttf — run `make build` from the repo root first");

    let font_data = std::fs::read(VF_PATH).expect("failed to read the variable font");
    let cmap = cmap_codepoints(&font_data);
    let mut chrome = PageChrome {
        date: today(),
        glyphs: glyph_count(&font_data),
        page_num: 0,
    };

    let weights: [(&str, f32); 4] = [
        ("Regular", 400.0),
        ("Medium", 500.0),
        ("SemiBold", 600.0),
        ("Bold", 700.0),
    ];

    let upper_matrix = adjacency_matrix_text(LATIN_UPPER);
    let lower_matrix = adjacency_matrix_text(LATIN_LOWER);
    let punct_matrix = format!(
        "UPPERCASE\n{}\n\nLOWERCASE\n{}",
        punctuation_matrix_text(LATIN_UPPER),
        punctuation_matrix_text(LATIN_LOWER)
    );
    let number_matrix = number_matrix_text();
    let basic_words = BASIC_SPACING_LINES.join("\n");
    let doubles = DOUBLE_TEST_LINES.join("\n");
    let contexts_am = context_strings_text(&LOWER_CONTEXTS[0..13]);
    let contexts_nz = context_strings_text(&LOWER_CONTEXTS[13..26]);

    let mut first_page = true;
    for (style, wght) in weights {
        let pages: [(&str, &str, f64, f64); 9] = [
            ("Uppercase Matrix", upper_matrix.as_str(), 7.5, 11.5),
            ("Lowercase Matrix", lower_matrix.as_str(), 7.5, 11.5),
            ("Punctuation Matrix", punct_matrix.as_str(), 8.0, 11.5),
            ("Number Matrix", number_matrix.as_str(), 8.5, 12.0),
            ("Kern King", KERN_KING_TEXT, 14.0, 19.5),
            ("Basic Word Tests", basic_words.as_str(), 11.0, 15.0),
            ("Doubles", doubles.as_str(), 12.0, 16.0),
            ("Lowercase Contexts A-M", contexts_am.as_str(), 9.0, 12.0),
            ("Lowercase Contexts N-Z", contexts_nz.as_str(), 9.0, 12.0),
        ];
        for (title, text, size, leading) in pages {
            if !first_page {
                ctx.new_page();
            }
            first_page = false;
            proof_page(&mut ctx, &renderer, &cmap, &mut chrome, style, wght, title, text, size, leading);
        }
        ctx.new_page();
        arabic_grid_page(&mut ctx, &renderer, &mut chrome, style, wght);
    }

    renderer
        .render_to_pdf(&ctx, "documentation/proofs/print-spacing-specimen.pdf")
        .expect("failed to write PDF");
    println!("Pages: {}", ctx.page_count());
}
