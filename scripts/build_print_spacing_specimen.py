#!/usr/bin/env python3
"""Build a landscape PDF specimen for print weight and spacing review."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from fontTools.ttLib import TTFont

try:
    from drawbot_skia.drawing import Drawing
except ModuleNotFoundError as error:
    raise SystemExit(
        "drawbot_skia is required. Run through `make specimen` "
        "after setting DRAWBOT_SKIA_REPO=/path/to/drawbot-skia, or install drawbot_skia in .venv."
    ) from error


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONTS = [
    ROOT / "fonts/ttf/VirtuaGrotesk-Regular.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Medium.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-SemiBold.ttf",
    ROOT / "fonts/ttf/VirtuaGrotesk-Bold.ttf",
]
DEFAULT_OUTPUT = ROOT / "documentation/proofs/print-spacing-specimen.pdf"

from grid_system import Grid, grid_view

PAGE_WIDTH = 792
PAGE_HEIGHT = 612
MARGIN = 36
PAGE_GRID = Grid(PAGE_WIDTH, PAGE_HEIGHT, margin=MARGIN)  # unit = 18

LATIN_LOWER = "abcdefghijklmnopqrstuvwxyz"
LATIN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_DIGITS = "0123456789"
LATIN_PUNCT = ".,:;!?/\\-–—'\"()[]{}"

BASIC_SPACING_LINES = [
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
]

DOUBLE_TEST_LINES = [
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
]

LOWER_CONTEXTS = "abcdefghijklmnopqrstuvwxyz"
RIGHT_CONTEXTS = "aeionrumlhspdftckbgwyvzqxj"
LEFT_CONTEXTS = "haeionrumlspdftckbgwyvzqxj"

ARABIC_SAMPLES = [
    ("shaping", "بسم الله الرحمن الرحيم"),
    ("letters", "سلام العربية كتاب قلم مدينة"),
    ("persian/urdu", "پ چ ژ گ ک ی ہ ھ ے"),
    ("marks", "بَ بُ بِ بّ بْ بً بٌ بٍ"),
    ("digits", "٠١٢٣٤٥٦٧٨٩  ۰۱۲۳۴۵۶۷۸۹"),
    ("punctuation", "، ؛ ؟ ٪ ٫ ٬ ؍ ۔"),
]

MAIN_X = PAGE_GRID.x(10)
MAIN_Y = PAGE_GRID.y(0)
MAIN_WIDTH = PAGE_GRID.unit * 30
MAIN_HEIGHT = PAGE_GRID.unit * 29
HEADER_RULE_Y = PAGE_GRID.y_top(1)
HEADER_TEXT_Y = HEADER_RULE_Y + 3
SIDEBAR_TITLE_Y = PAGE_GRID.y_top(3) + 3
SIDEBAR_META_Y = PAGE_GRID.y_top(6) + 3

KERN_KING_TEXT = (
    "lynx tuft frogs, dolphins abduct by proxy the ever awkward klutz, dud, "
    "dummkopf, jinx snubnose filmgoer, orphan sgt. renfruw grudgek reyfus, "
    "md. sikh psych if halt tympany jewelry sri heh! twyer vs jojo pneu "
    "fylfot alcaaba son of nonplussed halfbreed bubbly playboy guggenheim "
    "daddy coccyx sgraffito effect, vacuum dirndle impossible attempt to "
    "disvalue, muzzle the afghan czech czar and exninja, bob bixby dvorak "
    "wood dhurrie savvy, dizzy eye aeon circumcision uvula scrungy picnic "
    "luxurious special type carbohydrate ovoid adzuki kumquat bomb? afterglows "
    "gold girl pygmy gnome lb. ankhs acme aggroupment akmed brouhha tv wt. "
    "ujjain ms. oz abacus mnemonics bhikku khaki bwana aorta embolism vivid "
    "owls often kvetch otherwise, wysiwyg densfort wright you've absorbed "
    "rhythm, put obstacle kyaks krieg kern wurst subject enmity equity coquet "
    "quorum pique tzetse hepzibah sulfhydryl briefcase ajax ehler kafka fjord "
    "elfship halfdressed jugful eggcup hummingbirds swingdevil bagpipe legwork "
    "reproachful hunchback archknave baghdad wejh rijswijk rajbansi rajput "
    "ajdir okay weekday obfuscate subpoena liebknecht marcgravia ecbolic "
    "arcticward dickcissel pincpinc boldface maidkin adjective adcraft adman "
    "dwarfness applejack darkbrown kiln palzy always farmland flimflam unbossy "
    "nonlineal stepbrother lapdog stopgap sx countdown basketball beaujolais "
    "vb. flowchart aztec lazy bozo syrup tarzan annoying dyke yucky hawg "
    "gagzhukz cuzco squire when hiho mayhem nietzsche szasz gumdrop milk "
    "emplotment ambidextrously lacquer byway ecclesiastes stubchen hobgoblins "
    "crabmill aqua hawaii blvd. subquality byzantine empire debt obvious "
    "cervantes jekabzeel anecdote flicflac mechanicville bedbug couldn't i've "
    "it's they'll they'd dpt. headquarter burkhardt xerxes atkins govt. "
    "ebenezer lg. lhama amtrak amway fixity axmen quumbabda upjohn hrumpf"
)

def adjacency_matrix_text(chars: str) -> str:
    control = [
        chars[13] * 3 + chars[14] * 3 + chars[13] * 2 + chars[14] * 2 + chars[13] + chars[14] + chars[13] + chars[14] * 2 + chars[13] * 2 + chars[14] * 3 + chars[13] * 3,
        chars[7] * 3 + chars[14] * 3 + chars[7] * 2 + chars[14] * 2 + chars[7] + chars[14] + chars[7] + chars[14] * 2 + chars[7] * 2 + chars[14] * 3 + chars[7] * 3,
    ]
    matrix = ["".join(left + right + left for right in chars) for left in chars]
    return "\n".join(control + matrix)


def punctuation_matrix_text(chars: str) -> str:
    rows = [f"{punct}{punct.join(chars)}{punct}" for punct in LATIN_PUNCT]
    return "\n".join(rows)


def number_matrix_text() -> str:
    digit_rows = [
        "00011100110101100111000",
        *["".join(f"{left}{right}{left}" for right in LATIN_DIGITS) for left in LATIN_DIGITS],
    ]
    operators = "+-±×÷=/"
    operator_rows = [f"{op}{op.join(LATIN_DIGITS)}{op}" for op in operators]
    currency_rows = [f"{op}{op.join(LATIN_DIGITS)}{op}" for op in "°$€£#%"]
    punctuation_rows = [f"{digit}% {digit}‰ {digit}-{digit}.{digit},{digit}…{digit}°" for digit in LATIN_DIGITS]
    return "\n\n".join(
        [
            "\n".join(digit_rows),
            "\n".join(operator_rows),
            "\n".join(currency_rows),
            "\n".join(punctuation_rows),
        ]
    )


def context_strings_text(letters: str) -> str:
    lines = []
    for letter in letters:
        right, left = context_pair(letter)
        lines.append(right)
        lines.append(left)
        lines.append("")
    return "\n".join(lines)


def proof_chrome(
    db: Drawing,
    font_path: Path,
    page_index: list[dict[str, str | int]],
    title: str,
    section: str,
    size: float,
) -> None:
    info = font_info(font_path)
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    db.save()
    db.fill(1)
    db.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT)
    db.restore()
    if grid_view():
        PAGE_GRID.draw(db)
    page_index.append({"page": len(page_index) + 1, "title": f"{font_label(font_path)} {title}", "section": section})

    db.save()
    db.stroke(0)
    db.strokeWidth(1)
    db.line((MARGIN, HEADER_RULE_Y), (PAGE_WIDTH - MARGIN, HEADER_RULE_Y))
    db.line((MARGIN, MARGIN), (PAGE_WIDTH - MARGIN, MARGIN))
    db.restore()

    db.save()
    db.font("Courier", 10)
    db.fill(0)
    db.text(str(len(page_index)), (MARGIN, HEADER_TEXT_Y))
    db.text(f"{info['family']} {font_label(font_path)}", (PAGE_GRID.x(10), HEADER_TEXT_Y))
    db.text(datetime.now().strftime("%Y-%m-%d"), (PAGE_GRID.x(24), HEADER_TEXT_Y))
    db.text("Font Engineer: Eli Heuer", (PAGE_GRID.x(32), HEADER_TEXT_Y))

    db.text(f"{size:g}pt {title}", (MARGIN, SIDEBAR_TITLE_Y))
    db.text(f"Style: {font_label(font_path)}", (MARGIN, SIDEBAR_META_Y))
    db.text(f"Glyphs: {info['glyphs']}", (MARGIN, SIDEBAR_META_Y - PAGE_GRID.unit))
    db.text("Grid: 18pt unit", (MARGIN, SIDEBAR_META_Y - PAGE_GRID.unit * 2))
    db.restore()


def proof_page(
    db: Drawing,
    font_path: Path,
    page_index: list[dict[str, str | int]],
    title: str,
    section: str,
    text: str,
    size: float,
    leading: float,
) -> None:
    proof_chrome(db, font_path, page_index, title, section, size)

    db.save()
    db.font(str(font_path), size)
    db.lineHeight(leading)
    db.fill(0)
    db.textBox(text.strip(), (MAIN_X, MAIN_Y, MAIN_WIDTH, MAIN_HEIGHT))
    db.restore()


def arabic_grid_page(db: Drawing, font_path: Path, page_index: list[dict[str, str | int]]) -> None:
    proof_chrome(
        db,
        font_path,
        page_index,
        "Arabic Strings",
        "Arabic shaping, marks, numerals, and punctuation on the same grid system.",
        18,
    )
    y = PAGE_GRID.y_top(3)
    for sample_label, sample_text in ARABIC_SAMPLES:
        db.save()
        db.font("Courier", 10)
        db.fill(0)
        db.text(sample_label, (MAIN_X, y))
        db.restore()
        db.save()
        db.font(str(font_path), 18)
        db.fill(0)
        text_width = db.textSize(sample_text)[0]
        db.text(sample_text, (MAIN_X + MAIN_WIDTH - text_width, y - PAGE_GRID.unit))
        db.restore()
        y -= PAGE_GRID.unit * 4


def font_info(font_path: Path) -> dict[str, str | int]:
    font = TTFont(font_path)
    info: dict[str, str | int] = {
        "family": "",
        "style": font_path.stem.removeprefix("VirtuaGrotesk-"),
        "glyphs": len(font.getGlyphOrder()),
        "version": "",
    }
    for record in font["name"].names:
        if record.nameID == 1 and not info["family"]:
            info["family"] = record.toUnicode()
        elif record.nameID == 2 and not info["style"]:
            info["style"] = record.toUnicode()
        elif record.nameID == 5 and not info["version"]:
            info["version"] = record.toUnicode()
    font.close()
    return info


def font_label(font_path: Path) -> str:
    info = font_info(font_path)
    return str(info["style"])


def context_pair(letter: str) -> tuple[str, str]:
    right = " ".join(letter + char for char in RIGHT_CONTEXTS if char != letter)
    left = " ".join(char + letter for char in LEFT_CONTEXTS if char != letter)
    return f"{letter}+  {right}", f"+{letter}  {left}"


def build(font_paths: list[Path], output_path: Path) -> None:
    missing = [path for path in font_paths if not path.exists()]
    if missing:
        raise SystemExit("Missing font files: " + ", ".join(str(path) for path in missing))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    db = Drawing()
    db.newDrawing()
    page_index: list[dict[str, str | int]] = []

    for font_path in font_paths:
        proof_page(
            db,
            font_path,
            page_index,
            "Uppercase Matrix",
            "Recursive-style all-uppercase adjacency matrix for sidebearing and rhythm review.",
            adjacency_matrix_text(LATIN_UPPER),
            7.5,
            11.5,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Lowercase Matrix",
            "Recursive-style all-lowercase adjacency matrix for sidebearing and rhythm review.",
            adjacency_matrix_text(LATIN_LOWER),
            7.5,
            11.5,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Punctuation Matrix",
            "Punctuation against uppercase and lowercase alphabets.",
            "UPPERCASE\n"
            + punctuation_matrix_text(LATIN_UPPER)
            + "\n\nLOWERCASE\n"
            + punctuation_matrix_text(LATIN_LOWER),
            8,
            11.5,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Number Matrix",
            "Figures, operators, currency, percent, punctuation, and long digit texture.",
            number_matrix_text(),
            8.5,
            12,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Kern King",
            "Dense weird-word paragraph for kerning, spacing, and texture review.",
            KERN_KING_TEXT,
            14,
            19.5,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Basic Word Tests",
            "Dense word-based spacing tests.",
            "\n".join(BASIC_SPACING_LINES),
            11,
            15,
        )
        proof_page(
            db,
            font_path,
            page_index,
            "Doubles",
            "Double-letter spacing and kerning tests.",
            "\n".join(DOUBLE_TEST_LINES),
            12,
            16,
        )
        for label_text, letters in [
            ("Lowercase Contexts A-M", LOWER_CONTEXTS[0:13]),
            ("Lowercase Contexts N-Z", LOWER_CONTEXTS[13:26]),
        ]:
            proof_page(
                db,
                font_path,
                page_index,
                label_text,
                "a+ and +a style sidebearing/context tests.",
                context_strings_text(letters),
                9,
                12,
            )
        arabic_grid_page(db, font_path, page_index)

    db.saveImage(str(output_path))
    page_count = db.pageCount()
    db.endDrawing()
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise SystemExit(f"Print spacing specimen was not written: {output_path}")

    print(f"Wrote {output_path}")
    print(f"Pages: {page_count}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("fonts", nargs="*", type=Path, default=DEFAULT_FONTS)
    args = parser.parse_args()

    build(
        [path.resolve() for path in args.fonts],
        args.output.resolve(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
