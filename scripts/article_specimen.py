"""Render the article's outlined SVG from the current variable font.

Run after make build. This uses the compiled glyphs and HarfBuzz shaping;
it does not edit or redraw font sources.
"""
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts/variable/VirtuaGrotesk[wght].ttf"
OUTPUT = ROOT / "documentation/article/weight-specimen.svg"


def main():
    font = TTFont(FONT)
    face = hb.Face(FONT.read_bytes())
    order = font.getGlyphOrder()
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" '
             'height="900" viewBox="0 0 1600 900" role="img">',
             '<title>Virtua Grotesk, Regular through Bold</title>',
             '<rect width="1600" height="900" fill="#eeeae1"/>']

    def line(text, x, y, size, weight, width, color="#20251f"):
        shaped = hb.Font(face)
        shaped.set_variations({"wght": weight})
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(shaped, buf)
        assert all(g.codepoint for g in buf.glyph_infos), text
        total = sum(p.x_advance for p in buf.glyph_positions)
        scale = min(size / face.upem, width / total)
        glyphs = font.getGlyphSet(location={"wght": weight})
        parts.append(f'<g aria-label="{escape(text, quote=True)}" fill="{color}" '
                     f'transform="translate({x} {y}) scale({scale} {-scale})">')
        cursor = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(glyphs)
            glyphs[order[info.codepoint]].draw(pen)
            parts.append(f'<path transform="translate({cursor + pos.x_offset} '
                         f'{pos.y_offset})" d="{pen.getCommands()}"/>')
            cursor += pos.x_advance
        parts.append('</g>')

    line("VIRTUA GROTESK", 80, 105, 28, 600, 1440)
    line("Form follows rhythm", 80, 264, 128, 400, 1440)
    for i, weight in enumerate((400, 500, 600, 700)):
        y = 405 + i * 126
        parts.append(f'<path d="M80 {y - 83} H1520" stroke="#b4b9aa"/>')
        line(str(weight), 80, y, 28, 400, 130, "#52634a")
        line("Aa Bb Gg 0123456789", 250, y, 80, weight, 1270)
    parts.append('</svg>')
    OUTPUT.write_text('\n'.join(parts) + '\n')
    assert OUTPUT.stat().st_size < 800_000
    print(OUTPUT)


if __name__ == "__main__":
    main()
