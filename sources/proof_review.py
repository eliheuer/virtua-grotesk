"""Serve the Virtua Grotesk review index after running make proof."""

from argparse import ArgumentParser
from functools import partial
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib import import_module
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from zipfile import ZipFile
from subprocess import run
from tempfile import TemporaryDirectory
from threading import Lock
from unicodedata import category, normalize
from unittest.mock import patch

from fgtools import media, media_layout, project
from fgtools.proof_web import samples as proof_samples
from fontTools.ttLib import TTFont

OUTPUT = Path(__file__).resolve().parent.parent / 'output'
REV = OUTPUT / 'onboarding-review'
SHEETS = REV / 'Review-sheets'
ZIP = REV / 'Reference-proofs.zip'

PROOF = OUTPUT / 'proof' / 'proof.pdf'
SCRIPTS = ('Latin', 'Arabic', 'Hebrew')
PROOF_NAMES = {'print-proof.pdf': 'Print Proof', 'full-proof.pdf': 'Full Proof'}
GRID_PROOF = 'print-proof-grid.pdf'
PLOTTER = OUTPUT / 'media' / '.build' / 'plotter.rs'
PLOT = PLOTTER.with_name('proof.pdf.plot')
DESIGNBOT = OUTPUT.parent / '.venv' / 'bin' / 'designbot'
proof_lock = Lock()
proof_revision = None
COLUMNS = (69, 309, 549)
COLUMN_WIDTH = 224
TITLE_SIZE = 92.47
TITLE_WEIGHT = 700
TITLE_LEFT_BEARING = 0.03125


def proof_text(x, y, size, weight, text):
    return f'text\t{x}\t{y}\t{size}\t{weight}\t0\t0\t0\t255\t\t{text}'


def proof_rule(y, left=69, right=773):
    # Regular H has an 88-unit crossbar at 1024 UPM, or 1.03125 pt at 12 pt.
    return f'line\t{left}\t{y}\t{right}\t{y}\t1.03125\t0\t0\t0\t255'


def cover(font, facts, weights, stamp):
    left, middle, right = COLUMNS
    yield proof_text(left, 501.5, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, 501.5, 12, 400, stamp)
    yield proof_text(right, 501.5, 12, 400, 'github.com/eliheuer/virtua-grotesk')
    title_top = 489.5
    yield proof_rule(title_top)
    # Current Bold title ink spans about 0.78 em, including overshoots.
    title_height = 8 * round((TITLE_SIZE * 0.78 + 24) / 8)
    title_center = title_top - title_height / 2
    baseline = 73.5 + 4 * round((title_center - TITLE_SIZE * 0.375 - 73.5) / 4)
    yield proof_text(left - TITLE_SIZE * TITLE_LEFT_BEARING, baseline, TITLE_SIZE, TITLE_WEIGHT, 'Virtua Grotesk')

    bands = [
        ('Design Space', [
            ('Weight axis', f'{font.low:g}–{font.high:g}'),
            ('Optical size', '14–144 pt'),
            ('Named weights', str(len(weights))),
        ]),
        ('Character Set', [
            ('Glyphs', str(facts['glyphs'])),
            ('Encoded characters', str(facts['characters'])),
            ('Scripts', 'Latin, Arabic, Hebrew'),
        ]),
        ('Construction', [
            ('Units per em', '1024'),
            ('Cap height', '768'),
            ('x-height', '576'),
        ]),
        ('Distribution', [
            ('Format', 'Variable TrueType'),
            ('Sources', 'UFO and Designspace'),
            ('License', 'SIL Open Font License 1.1'),
        ]),
    ]
    top = title_top - title_height
    for i, (heading, rows) in enumerate(bands):
        yield proof_rule(top)
        height = top - 73.5 if i == len(bands) - 1 else 80
        inset = 4 * round((height - 32) / 8)
        first = top - inset
        yield proof_text(left, first, 12, 400, heading)
        for row, (label, value) in enumerate(rows):
            y = first - row * 20
            yield proof_text(middle, y, 12, 400, label)
            yield proof_text(right, y, 12, 400, value)
        top -= height


def without_reading_marks(text, script):
    if script == 'Arabic':
        # Keep the hamza on إ and أ. Only tashkil are optional in this passage.
        return ''.join(c for c in text if not '\u064b' <= c <= '\u0652')
    return ''.join(c for c in normalize('NFD', text) if category(c) != 'Mn')


def paired_lines(font, script, text, measure, size, weight, limit):
    # Break on the same word in both settings, even when accents extend the ink.
    marked = ''
    for word in text.split():
        trial = f'{marked} {word}'.strip()
        pair = (without_reading_marks(trial, script), trial)
        widths = (font.measure(line, weight) for line in pair)
        if marked and any((max(advance, right) - min(0, left)) * size > measure
                          for advance, left, right in widths):
            yield without_reading_marks(marked, script), marked
            if limit is not None:
                limit -= 1
                if not limit:
                    return
            marked = word
        else:
            marked = trial
    if marked:
        yield without_reading_marks(marked, script), marked


def reading_page(font, script, style, weight, text):
    left, middle, right = COLUMNS
    rtl = script in ('Arabic', 'Hebrew')
    # Stacked Arabic marks in Black span 2.19 em from highest to lowest ink.
    leading = {8: 18, 16: 36} if script == 'Arabic' else {8: 10, 16: 20}
    sizes = (16, 8) if rtl else (8, 16)
    settings = ' · '.join(f'{size}/{leading[size]} pt' for size in sizes)
    yield proof_text(left, 501.5, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, 501.5, 12, 400, f'{script} · {style} {weight:g}')
    yield proof_text(right, 501.5, 12, 400, settings)
    yield proof_rule(489.5)
    band_height = 208

    columns = [(8, 457.5, right + COLUMN_WIDTH if rtl else left, COLUMN_WIDTH),
               (16, 453.5, middle + COLUMN_WIDTH if rtl else middle, 2 * COLUMN_WIDTH)]
    for size, baseline, start, measure in columns:
        if script == 'Arabic':
            baseline -= size / 2
        room = int((baseline - 293.5) // leading[size]) + 1
        for i, pair in enumerate(paired_lines(font, script, text, measure, size, weight, room)):
            for band, line in enumerate(pair):
                x = start - font.measure(line, weight)[2] * size if rtl else start
                y = baseline - i * leading[size] - band * band_height
                yield proof_text(f'{x:g}', y, size, f'{weight:g}', line)


def grid_lines():
    for x in COLUMNS:
        yield f'rect\t{x}\t73.5\t{COLUMN_WIDTH}\t448\t255\t247\t247\t255'
    # Match the centered 704 × 448 pt live area of the landscape proof.
    for x in range(69, 774, 8):
        width = 0.5 if (x - 69) % 32 == 0 else 0.15
        yield f'line\t{x}\t73.5\t{x}\t521.5\t{width}\t244\t191\t191\t255'
    for offset in range(0, 449, 8):
        y = 73.5 + offset
        width = 0.5 if offset % 32 == 0 else 0.15
        yield f'line\t69\t{y}\t773\t{y}\t{width}\t244\t191\t191\t255'


def proof_content():
    canvas, font_row, _, *lines = PLOT.read_text().splitlines()
    layout = project.load(OUTPUT.parent)
    font, facts = media.font_type(layout)
    if Path(font_row.split('\t')[1]) != font.path:
        raise ValueError('Run make proof to update the detail pages for the current font.')
    with TTFont(font.path, lazy=True) as built:
        optical_default = next((axis.defaultValue for axis in built['fvar'].axes if axis.axisTag == 'opsz'), None)
        weights = sorted(
            (instance.coordinates['wght'], built['name'].getDebugName(instance.subfamilyNameID))
            for instance in built['fvar'].instances
            if instance.coordinates.get('opsz', optical_default) == optical_default
        )
    print_pages = []
    replaced = {1}
    stamp = f'Version {facts["version"]}'
    reading_headings = {f'Reading, {script}' for script in SCRIPTS}
    page_number = 0
    for row in lines:
        if row.startswith('page\t'):
            page_number += 1
        elif row.startswith('text\t'):
            label = row.rsplit('\t', 1)[-1]
            if label in reading_headings:
                replaced.add(page_number)
            elif page_number in replaced and label.startswith('Version '):
                version, *revision = label.split(maxsplit=2)[1:]
                stamp = ' · '.join([f'Version {version}', *revision])

    print_pages.append(tuple(cover(font, facts, weights, stamp)))
    samples, _ = proof_samples.read(layout.sources)
    for script in SCRIPTS:
        paragraphs = samples['text'][f'{script.lower()}-reading-marks']['paragraphs']
        text = ' '.join(paragraph['text'] for paragraph in paragraphs)
        if not all(font.covers(t.replace(' ', '')) for t in (text, without_reading_marks(text, script))):
            raise ValueError(f'The built font cannot set the {script} reading sample.')
        text = ' '.join([text] * 4)
        for weight, style in weights:
            print_pages.append(tuple(reading_page(font, script, style, weight, text)))
    return canvas, font_row, print_pages, replaced


def draw_print_proof(folder, name, canvas, font, pages, show_grid=False):
    result = folder / name
    plot = result.with_suffix('.plot')
    page_start = ['page\t0\t255\t255\t255', *(grid_lines() if show_grid else ())]
    core = [line for page in pages for line in (*page_start, *page)]
    plot.write_text('\n'.join([canvas, font, f'output\t{result}', *core]) + '\n')
    run([str(DESIGNBOT), str(PLOTTER), '--', f'plot={plot}'], check=True)
    return result


def prepare_proofs():
    global proof_revision
    with proof_lock:
        revision = (PROOF.stat().st_mtime_ns, PLOT.stat().st_mtime_ns)
        names = (*PROOF_NAMES, GRID_PROOF)
        if revision == proof_revision and all(PROOF.with_name(n).exists() for n in names):
            return
        with TemporaryDirectory(dir=PROOF.parent) as work:
            folder = Path(work)
            canvas, font, print_pages, replaced = proof_content()
            run(['pdfseparate', str(PROOF), str(folder / 'page-%d.pdf')], check=True)
            pages = sorted(folder.glob('page-*.pdf'), key=lambda p: int(p.stem.split('-')[1]))
            detail = [page for n, page in enumerate(pages, 1) if n not in replaced]
            regular = draw_print_proof(folder, 'print-proof.pdf', canvas, font, print_pages)
            grid = draw_print_proof(folder, GRID_PROOF, canvas, font, print_pages, show_grid=True)
            full = folder / 'full-proof.pdf'
            run(['pdfunite', str(regular), *map(str, detail), str(full)], check=True)
            for result in (regular, full, grid):
                result.replace(PROOF.with_name(result.name))
        proof_revision = revision


class ProofSheet(media_layout.Sheet):
    def paragraph(self, text, col, row, cols, size, leading, weight=None, limit=None, color='ink', drop=0):
        if not self.type.right_to_left(text):
            return super().paragraph(text, col, row, cols, size, leading, weight, limit, color, drop)
        if not self.type.covers(text.replace(' ', '')):
            return 0

        module = self.grid['module']
        script = 'Arabic' if any('\u0600' <= c <= '\u06ff' for c in text) else 'Hebrew'
        lines = [line for _, line in paired_lines(self.type, script, text, cols * module, size, weight, limit)]
        for index, line in enumerate(lines):
            self.text(line, col + cols, row, size, weight, color, optical=True,
                      flush='right', drop=drop + index * leading)
        return -(-(drop + (len(lines) - 1) * leading + size) // module) if lines else 0


def draw_arabic_marks(sheet, job):
    default = import_module('fgtools.media_formats.proofs.arabic-marks')
    font = job.type
    marks = [(name, mark) for name, mark in default.MARKS if font.covers(mark)]
    bases = [base for base in default.BASES if font.covers(base)]
    if not marks or not bases:
        return 'the font has no Arabic marks yet'
    size, col_width = default.SIZE, default.CELL
    row_height = 3
    rows_per_page = (sheet.rows - 2) // row_height
    for weight in sorted({font.low, font.high}):
        for start in range(0, len(bases), rows_per_page):
            lines = bases[start:start + rows_per_page]
            sheet.page()
            sheet.header(job.family, 'Arabic marks', f'Wght {weight:g}', sheet.size(size), job.stamp)
            for place, (name, mark) in enumerate(marks):
                col = place * col_width
                sheet.label(name, col, 1, drop=0)
                for line, base in enumerate(lines):
                    sheet.text(base + mark, col, 3 + line * row_height, size, weight, optical=True)
            for line in range(len(lines) + 1):
                sheet.rule(2 + line * row_height)


def compose_proof(compose, table, job, canvas, units, colors, name):
    # fgtools supplies the other detail formats and writes the checked book.
    if name not in ('reading', 'lines', 'arabic-marks'):
        return compose(table, job, canvas, units, colors, name)
    sheet = ProofSheet(media_layout.lattice(canvas, units), job.type, colors, name)
    draw = draw_arabic_marks if name == 'arabic-marks' else import_module(f'fgtools.media_formats.proofs.{name}').draw
    reason = draw(sheet, job)
    if reason or not sheet.pages:
        return None, reason or 'the format drew nothing'
    sheet.check()
    return sheet, None


def link(p, title=None, thumb=False):
    url = '/' + quote(p.relative_to(OUTPUT).as_posix())
    name = escape(title or p.stem.replace('-', ' '))
    picture = f'<img loading="lazy" src="{url}" alt="">' if thumb else ''
    return f'<a href="{url}">{picture}{name}</a>'

def index():
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Virtua Grotesk proofs</title><style>body{max-width:960px;margin:48px auto;padding:0 24px;background:#f6f5f0;color:#222;font:16px/1.5 system-ui}h1{font-size:36px;letter-spacing:-.045em}a{color:#234836;text-underline-offset:3px}.primary{display:inline-block;font-size:22px;margin:0 24px 20px 0}details{border-top:1px solid #babdb4;padding:14px 0}summary{cursor:pointer;font-weight:600}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;margin:16px 0}.grid img{display:block;width:100%;height:116px;object-fit:contain;background:#303030;margin-bottom:5px}li{margin:6px 0}</style><main><h1>Virtua Grotesk proofs</h1>']
    if PROOF.is_file():
        for name, title in PROOF_NAMES.items():
            parts.append('<span class="primary">'+link(PROOF.with_name(name),title)+'</span>')
        parts.append('<p>'+link(PROOF.with_name(GRID_PROOF),'Print Proof with red grid (temporary)')+'</p>')
        parts.append('<p>The Print Proof includes a cover and reading pages for every named weight in Latin, Arabic and Hebrew. '
                     'The Full Proof begins with the Print Proof. '
                     'The remaining pages cover character sets, size tests, interpolation, kerning, marks and joining in detail.</p>')
    reports = sorted((OUTPUT / 'diff').glob('*/diffenator.html'))
    if reports:
        parts.append('<h2>Diffenator comparisons</h2><ul>')
        for report in reports:
            style = report.parent.name.removeprefix('VirtuaGrotesk-')
            if style.startswith('VirtuaGrotesk[') and style.endswith(']'):
                style = 'Variable font'
            parts.append('<li>'+link(report,style)+'</li>')
        parts.append('</ul>')
    parts.append('<h2>Marketing and README images</h2>')
    media_index = OUTPUT / 'media' / 'index.html'
    if media_index.is_file():
        parts.append('<p>'+link(media_index,'Marketing gallery')+'</p>')
    readme_images = sorted((OUTPUT / 'readme-images').glob('*'))
    parts.append('<div class="grid">'+''.join(link(image,thumb=True) for image in readme_images)+'</div>')
    sheets = sorted(SHEETS.glob('*.png'))
    for title,prefixes in [('Latin',('Latin-',)),('Hebrew',('Hebrew-',)),('Arabic, Persian and numerals',('Arabic-','Persian-','Urdu-','Numerals-'))]:
        parts.append(f'<details><summary>{title} proof sheets</summary><div class="grid">')
        parts.extend(link(p,thumb=True) for p in sheets if p.name.startswith(prefixes))
        parts.append('</div></details>')
    if ZIP.is_file():
        parts.append('<details><summary>Reference font PDFs</summary><ul>')
        with ZipFile(ZIP) as z:
            for n in sorted(z.namelist()):
                if n.endswith('.pdf'):parts.append(f'<li><a href="/reference/{quote(n)}">{escape(n[:-4].replace("-"," "))}</a></li>')
        parts.append('</ul></details>')
    parts.append('<details><summary>Earlier proofs and other files</summary><ul>')
    for p in sorted(REV.glob('*')):
        if p.suffix in ('.png','.pdf'):parts.append('<li>'+link(p)+'</li>')
    for directory in ('render','diff','media','qa','weight-pass','onboarding-review'):
        parts.append(f'<li><a href="/{directory}/">{directory}/</a></li>')
    return ''.join(parts)+'</ul></details></main></html>'

class Proofs(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(OUTPUT),**kwargs)
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path=='/':
            data=index().encode();kind='text/html; charset=utf-8'
        elif path in {f'/proof/{name}' for name in (*PROOF_NAMES, GRID_PROOF)}:
            prepare_proofs()
            return super().do_GET()
        elif path.startswith('/reference/'):
            with ZipFile(ZIP) as z:
                n=path.removeprefix('/reference/')
                if n not in z.namelist() or not n.endswith('.pdf'):return self.send_error(404)
                data=z.read(n);kind='application/pdf'
        else:
            if not Path(self.translate_path(self.path)).resolve().is_relative_to(OUTPUT):return self.send_error(404)
            return super().do_GET()
        self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--regular-title', action='store_true', help='Try the cover title at weight 400.')
    parser.add_argument('--build-proof', nargs='*', help='Build the source proof or the named pages.')
    args = parser.parse_args()
    if args.build_proof is not None:
        with patch.object(media, 'compose', partial(compose_proof, media.compose)):
            media.main(['--proof', *args.build_proof])
        raise SystemExit
    if args.regular_title:
        TITLE_SIZE = 103.76
        TITLE_WEIGHT = 400
        TITLE_LEFT_BEARING = 24 / 1024
    ThreadingHTTPServer(('127.0.0.1', 8770), Proofs).serve_forever()

