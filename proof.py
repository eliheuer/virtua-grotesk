#!/usr/bin/env python3
"""
Virtua Grotesk Print Proof Generator

A technical document for evaluating the typeface using DrawBot.
Generates a multi-page PDF with various proofing layouts.

Usage:
    python proof.py [font_path] [output_path]

Defaults to fonts/VirtuaGrotesk-Regular.ttf and proof.pdf
"""

import drawBot as db
from fontTools.ttLib import TTFont
from pathlib import Path
import sys
from datetime import datetime

# Page settings
PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # US Letter
MARGIN = 36  # 0.5 inch margins


def get_font_info(font_path):
    """Extract font metadata using fontTools."""
    tt = TTFont(font_path)
    name_table = tt['name']

    info = {
        'family': '',
        'style': '',
        'version': '',
        'designer': '',
    }

    for record in name_table.names:
        if record.nameID == 1:
            info['family'] = record.toUnicode()
        elif record.nameID == 2:
            info['style'] = record.toUnicode()
        elif record.nameID == 5:
            info['version'] = record.toUnicode()
        elif record.nameID == 9:
            info['designer'] = record.toUnicode()

    # Get glyph count
    info['glyph_count'] = len(tt.getGlyphOrder())

    # Get units per em
    info['upm'] = tt['head'].unitsPerEm

    tt.close()
    return info


def get_cmap(font_path):
    """Get character map from font."""
    tt = TTFont(font_path)
    cmap = tt.getBestCmap()
    tt.close()
    return cmap


def draw_header(font_info, page_title):
    """Draw page header with font name and page title."""
    db.save()
    db.font("Helvetica", 9)
    db.fill(0.4)

    # Left: Font name
    header_text = f"{font_info['family']} {font_info['style']}"
    db.text(header_text, (MARGIN, PAGE_HEIGHT - MARGIN + 10))

    # Right: Page title
    title_width = db.textSize(page_title)[0]
    db.text(page_title, (PAGE_WIDTH - MARGIN - title_width, PAGE_HEIGHT - MARGIN + 10))

    db.restore()


def draw_footer():
    """Draw page footer with date."""
    db.save()
    db.font("Helvetica", 8)
    db.fill(0.5)

    # Left: Date
    date_str = datetime.now().strftime("%Y-%m-%d")
    db.text(date_str, (MARGIN, MARGIN - 20))

    db.restore()


def title_page(font_path, font_info):
    """Create title page with font specimen and metadata."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)

    y = PAGE_HEIGHT - MARGIN - 80

    # Font family name large
    db.font(font_path, 48)
    db.fill(0)
    db.text(font_info['family'], (MARGIN, y))

    y -= 50

    # Style name
    db.font(font_path, 24)
    db.text(font_info['style'], (MARGIN, y))

    y -= 80

    # Large specimen text
    db.font(font_path, 72)
    specimen = "Aa Bb Cc"
    db.text(specimen, (MARGIN, y))

    y -= 90
    db.text("Dd Ee Ff", (MARGIN, y))

    y -= 90
    db.text("Gg Hh Ii", (MARGIN, y))

    y -= 120

    # Metadata section
    db.font("Helvetica", 10)
    db.fill(0.3)

    meta_lines = [
        f"Family: {font_info['family']}",
        f"Style: {font_info['style']}",
        f"Version: {font_info['version']}",
        f"Glyphs: {font_info['glyph_count']}",
        f"Units per Em: {font_info['upm']}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ]

    if font_info['designer']:
        meta_lines.insert(2, f"Designer: {font_info['designer']}")

    for line in meta_lines:
        db.text(line, (MARGIN, y))
        y -= 16


def alphabet_page(font_path, font_info):
    """Full alphabet display in multiple sizes."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Alphabet")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 40

    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"

    sizes = [48, 36, 24, 18, 14, 11, 9]

    for size in sizes:
        db.font(font_path, size)
        db.fill(0)

        # Check if uppercase fits
        uc_width = db.textSize(uppercase)[0]
        if uc_width > PAGE_WIDTH - 2 * MARGIN:
            # Split into two lines
            mid = len(uppercase) // 2
            db.text(uppercase[:mid], (MARGIN, y))
            y -= size * 1.3
            db.text(uppercase[mid:], (MARGIN, y))
        else:
            db.text(uppercase, (MARGIN, y))

        y -= size * 1.3

        # Lowercase
        lc_width = db.textSize(lowercase)[0]
        if lc_width > PAGE_WIDTH - 2 * MARGIN:
            mid = len(lowercase) // 2
            db.text(lowercase[:mid], (MARGIN, y))
            y -= size * 1.3
            db.text(lowercase[mid:], (MARGIN, y))
        else:
            db.text(lowercase, (MARGIN, y))

        y -= size * 1.8

        if y < MARGIN + 50:
            break


def numerals_page(font_path, font_info):
    """Numbers and punctuation."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Numerals & Punctuation")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 50

    numerals = "0123456789"
    punctuation = ".,;:!?\"'`-–—()[]{}/@#$%^&*+=<>"

    sizes = [72, 48, 36, 24, 18, 14]

    # Numerals
    db.font("Helvetica", 10)
    db.fill(0.5)
    db.text("NUMERALS", (MARGIN, y))
    y -= 20

    for size in sizes[:4]:
        db.font(font_path, size)
        db.fill(0)
        db.text(numerals, (MARGIN, y))
        y -= size * 1.5

    y -= 20

    # Punctuation
    db.font("Helvetica", 10)
    db.fill(0.5)
    db.text("PUNCTUATION", (MARGIN, y))
    y -= 20

    for size in sizes[2:]:
        db.font(font_path, size)
        db.fill(0)

        # Split if too long
        if db.textSize(punctuation)[0] > PAGE_WIDTH - 2 * MARGIN:
            mid = len(punctuation) // 2
            db.text(punctuation[:mid], (MARGIN, y))
            y -= size * 1.3
            db.text(punctuation[mid:], (MARGIN, y))
        else:
            db.text(punctuation, (MARGIN, y))
        y -= size * 1.5

        if y < MARGIN + 30:
            break


def waterfall_page(font_path, font_info):
    """Size waterfall with sample text."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Size Waterfall")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 40

    sample = "Hamburgefontsiv"
    sizes = [72, 60, 48, 36, 30, 24, 20, 18, 16, 14, 12, 11, 10, 9, 8, 7, 6]

    for size in sizes:
        db.font(font_path, size)
        db.fill(0)

        # Size label
        db.save()
        db.font("Helvetica", 8)
        db.fill(0.5)
        db.text(f"{size}pt", (MARGIN, y))
        db.restore()

        # Sample text
        db.font(font_path, size)
        db.fill(0)
        db.text(sample, (MARGIN + 40, y))

        y -= size * 1.4

        if y < MARGIN + 20:
            break


def spacing_page(font_path, font_info):
    """Spacing proof with letter combinations."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Spacing Proof")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 40
    size = 14
    line_height = size * 1.4

    db.font(font_path, size)
    db.fill(0)

    # Lowercase spacing
    lowercase = "abcdefghijklmnopqrstuvwxyz"

    for c in lowercase:
        line = c + c.join(list(lowercase)) + c

        # Check if line fits
        if db.textSize(line)[0] > PAGE_WIDTH - 2 * MARGIN:
            # Truncate
            while db.textSize(line)[0] > PAGE_WIDTH - 2 * MARGIN and len(line) > 10:
                line = line[:-2]

        db.text(line, (MARGIN, y))
        y -= line_height

        if y < MARGIN + 30:
            db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
            draw_header(font_info, "Spacing Proof (continued)")
            draw_footer()
            y = PAGE_HEIGHT - MARGIN - 40


def paragraph_page(font_path, font_info):
    """Paragraph text at various sizes."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Paragraph Setting")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 40

    sample_text = """The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! The five boxing wizards jump quickly. Sphinx of black quartz, judge my vow. Two driven jocks help fax my big quiz. The jay, pig, fox, zebra, and my wolves quack!"""

    sizes = [14, 12, 10, 9, 8]

    for size in sizes:
        # Label
        db.font("Helvetica", 8)
        db.fill(0.5)
        db.text(f"{size}pt / {int(size * 1.4)}pt leading", (MARGIN, y))
        y -= 14

        # Paragraph
        db.font(font_path, size)
        db.fill(0)

        box_height = size * 6
        box_width = PAGE_WIDTH - 2 * MARGIN

        db.textBox(sample_text, (MARGIN, y - box_height, box_width, box_height))

        y -= box_height + 30

        if y < MARGIN + 80:
            break


def kerning_page(font_path, font_info):
    """Common kerning pairs."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Kerning Pairs")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 50

    kern_pairs = [
        "AV AW AT AY Av Aw Ay AC AG AO AQ AU",
        "FA TA PA VA WA YA LT LV LW LY",
        "To Tr Tu Tw Ty Te Ta Tc Ts",
        "Vo Va Ve Vu Vy Wo Wa We Wy",
        "Ya Ye Yo Yu \"A\" 'A' \"T\" 'T' \"V\"",
        "ff fi fl ffi ffl ft",
        "oo oc oe og oq op od ob",
        "rv ry rw ra re ro rc",
    ]

    size = 24

    for pairs in kern_pairs:
        db.font(font_path, size)
        db.fill(0)
        db.text(pairs, (MARGIN, y))
        y -= size * 1.6

        if y < MARGIN + 30:
            break


def glyph_set_page(font_path, font_info, cmap, start_page=1):
    """Display all glyphs in a grid."""
    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Character Set")
    draw_footer()

    # Grid settings
    cols = 12
    cell_size = (PAGE_WIDTH - 2 * MARGIN) / cols
    glyph_size = cell_size * 0.6

    x_start = MARGIN
    y_start = PAGE_HEIGHT - MARGIN - 50

    x = x_start
    y = y_start

    # Sort codepoints
    codepoints = sorted(cmap.keys())

    page_num = start_page

    for i, cp in enumerate(codepoints):
        char = chr(cp)

        # Draw cell
        db.save()
        db.stroke(0.85)
        db.strokeWidth(0.5)
        db.fill(None)
        db.rect(x, y - cell_size, cell_size, cell_size)
        db.restore()

        # Draw glyph
        db.save()
        db.font(font_path, glyph_size)
        db.fill(0)

        # Center glyph in cell
        char_width = db.textSize(char)[0]
        char_x = x + (cell_size - char_width) / 2
        char_y = y - cell_size + cell_size * 0.25

        db.text(char, (char_x, char_y))
        db.restore()

        # Draw unicode label
        db.save()
        db.font("Helvetica", 5)
        db.fill(0.6)
        label = f"{cp:04X}"
        db.text(label, (x + 2, y - cell_size + 3))
        db.restore()

        # Move to next cell
        x += cell_size

        if x + cell_size > PAGE_WIDTH - MARGIN:
            x = x_start
            y -= cell_size

            if y - cell_size < MARGIN:
                page_num += 1
                db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
                draw_header(font_info, f"Character Set (page {page_num})")
                draw_footer()
                x = x_start
                y = y_start

    return page_num


def arabic_page(font_path, font_info, cmap):
    """Arabic character display if present."""
    # Check if font has Arabic
    arabic_range = range(0x0600, 0x06FF)
    arabic_chars = [chr(cp) for cp in arabic_range if cp in cmap]

    if not arabic_chars:
        return

    db.newPage(PAGE_WIDTH, PAGE_HEIGHT)
    draw_header(font_info, "Arabic")
    draw_footer()

    y = PAGE_HEIGHT - MARGIN - 50

    # Sample Arabic text
    samples = [
        "".join(arabic_chars[:28]),
        "".join(arabic_chars[28:56]) if len(arabic_chars) > 28 else "",
    ]

    sizes = [48, 36, 24, 18]

    for size in sizes:
        db.font(font_path, size)
        db.fill(0)

        for sample in samples:
            if sample:
                db.text(sample, (MARGIN, y))
                y -= size * 1.5

        y -= 20

        if y < MARGIN + 50:
            break


def generate_proof(font_path, output_path):
    """Generate complete proof document."""
    font_path = Path(font_path).resolve()
    output_path = Path(output_path).resolve()

    if not font_path.exists():
        print(f"Error: Font not found at {font_path}")
        return False

    print(f"Generating proof for: {font_path.name}")

    # Get font info
    font_info = get_font_info(str(font_path))
    cmap = get_cmap(str(font_path))

    print(f"  Family: {font_info['family']}")
    print(f"  Style: {font_info['style']}")
    print(f"  Glyphs: {font_info['glyph_count']}")

    # Start document
    db.newDrawing()

    # Generate pages
    print("  Creating pages...")

    title_page(str(font_path), font_info)
    alphabet_page(str(font_path), font_info)
    numerals_page(str(font_path), font_info)
    waterfall_page(str(font_path), font_info)
    spacing_page(str(font_path), font_info)
    paragraph_page(str(font_path), font_info)
    kerning_page(str(font_path), font_info)
    glyph_set_page(str(font_path), font_info, cmap)
    arabic_page(str(font_path), font_info, cmap)

    # Save PDF
    total_pages = db.pageCount()
    db.saveImage(str(output_path))
    db.endDrawing()

    print(f"  Saved: {output_path}")
    print(f"  Pages: {total_pages}")

    return True


if __name__ == "__main__":
    # Default paths
    script_dir = Path(__file__).parent
    default_font = script_dir / "fonts" / "VirtuaGrotesk-Regular.ttf"
    default_output = script_dir / "proof.pdf"

    # Parse arguments
    font_path = sys.argv[1] if len(sys.argv) > 1 else default_font
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output

    # Generate proof
    success = generate_proof(font_path, output_path)
    sys.exit(0 if success else 1)
