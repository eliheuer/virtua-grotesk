"""Serve the Virtua Grotesk review index after running make proof."""

from argparse import ArgumentParser
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from zipfile import ZipFile
from subprocess import run
from tempfile import TemporaryDirectory
from threading import Lock

OUTPUT = Path(__file__).resolve().parent.parent / 'output'
REV = OUTPUT / 'onboarding-review'
SHEETS = REV / 'Review-sheets'
ZIP = REV / 'Reference-proofs.zip'

PROOF = OUTPUT / 'proof' / 'proof.pdf'
READING_PAGES = {
    11: ('Latin', 400),
    12: ('Latin', 700),
    13: ('Arabic', 400),
    14: ('Arabic', 700),
    15: ('Hebrew', 400),
    16: ('Hebrew', 700),
}
CORE_PAGES = (1, *READING_PAGES)
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


def cover(original, reading):
    values = [row.split('\t')[-1] for row in original if row.startswith('text\t')]
    version = values[1]
    stamp = next(row.split('\t')[-1].split()[-1] for row in reading if '\tVersion ' in row)
    left, middle, right = COLUMNS
    yield proof_text(left, 501.5, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, 501.5, 12, 400, f'{version} · {stamp}')
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
            ('Weight axis', '400–700'),
            ('Masters', 'Regular, Bold'),
            ('Static weights', '400, 500, 600, 700'),
        ]),
        ('Character Set', [
            ('Glyphs', values[8]),
            ('Encoded characters', values[10]),
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


def reading_page(original, script, weight):
    left, middle, right = COLUMNS
    rtl = script in ('Arabic', 'Hebrew')
    style = {400: 'Regular', 700: 'Bold'}[weight]
    leading = {8: 10, 16: 20}
    sizes = (16, 8) if rtl else (8, 16)
    settings = ' · '.join(f'{size}/{leading[size]} pt' for size in sizes)
    yield proof_text(left, 501.5, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, 501.5, 12, 400, f'{script} · {style} {weight}')
    yield proof_text(right, 501.5, 12, 400, settings)
    yield proof_rule(489.5)

    baseline = {8: 469.5, 16: 465.5}
    # Retain fgtools' line breaks and RTL alignment. Its wide RTL block
    # ends at 517 pt. Move it to the right edge of our middle column.
    offsets = {8: 0, 16: middle + COLUMN_WIDTH - 517 if rtl else middle - 325}
    for row in original:
        fields = row.split('\t')
        if fields[0] != 'text' or fields[3] not in ('8', '16'):
            continue
        size = int(fields[3])
        if baseline[size] >= 81.5:
            fields[1] = f'{float(fields[1]) + offsets[size]:g}'
            fields[2] = str(baseline[size])
            yield '\t'.join(fields)
            baseline[size] -= leading[size]


def draw_print_proof(folder, name, show_grid=False):
    canvas, font, _, *lines = PLOT.read_text().splitlines()
    pages = []
    page_starts = []
    ink_columns = {'text': 5, 'line': 6, 'rect': 5, 'oval': 5, 'path': 2}
    for row in lines:
        fields = row.split('\t')
        kind = fields[0]
        if kind == 'page':
            pages.append(['page\t0\t255\t255\t255'])
            if show_grid:
                if len(pages) in CORE_PAGES:
                    for x in COLUMNS:
                        pages[-1].append(f'rect\t{x}\t73.5\t{COLUMN_WIDTH}\t448\t255\t247\t247\t255')
                # Match the centered 704 × 448 pt live area of the landscape proof.
                for x in range(69, 774, 8):
                    width = 0.5 if (x - 69) % 32 == 0 else 0.15
                    pages[-1].append(f'line\t{x}\t73.5\t{x}\t521.5\t{width}\t244\t191\t191\t255')
                for offset in range(0, 449, 8):
                    y = 73.5 + offset
                    width = 0.5 if offset % 32 == 0 else 0.15
                    pages[-1].append(f'line\t69\t{y}\t773\t{y}\t{width}\t244\t191\t191\t255')
            page_starts.append(len(pages[-1]))
        else:
            start = ink_columns[kind]
            fields[start:start + 4] = ['0', '0', '0', '255']
            pages[-1].append('\t'.join(fields))
    first_reading = page_starts[10]
    pages[0][page_starts[0]:] = cover(pages[0][page_starts[0]:], pages[10][first_reading:])
    for number, (script, weight) in READING_PAGES.items():
        page = pages[number - 1]
        start = page_starts[number - 1]
        page[start:] = reading_page(page[start:], script, weight)
    result = folder / name
    plot = result.with_suffix('.plot')
    core = [line for n in CORE_PAGES for line in pages[n - 1]]
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
            run(['pdfseparate', str(PROOF), str(folder / 'page-%d.pdf')], check=True)
            pages = sorted(folder.glob('page-*.pdf'), key=lambda p: int(p.stem.split('-')[1]))
            detail = [page for n, page in enumerate(pages, 1) if n not in CORE_PAGES]
            regular = draw_print_proof(folder, 'print-proof.pdf')
            grid = draw_print_proof(folder, GRID_PROOF, show_grid=True)
            full = folder / 'full-proof.pdf'
            run(['pdfunite', str(regular), *map(str, detail), str(full)], check=True)
            for result in (regular, full, grid):
                result.replace(PROOF.with_name(result.name))
        proof_revision = revision


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
        parts.append('<p>The Print Proof is a cover and six reading pages. The Full Proof opens with the same seven pages. '
                     'The remaining pages cover character sets, size tests, interpolation, kerning, marks and joining in detail.</p>')
    reports = sorted((OUTPUT / 'diff').glob('*/diffenator.html'))
    if reports:
        parts.append('<h2>Diffenator comparisons</h2><ul>')
        for report in reports:
            style = report.parent.name.removeprefix('VirtuaGrotesk-')
            if style == 'VirtuaGrotesk[wght]':
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
    if parser.parse_args().regular_title:
        TITLE_SIZE = 103.76
        TITLE_WEIGHT = 400
        TITLE_LEFT_BEARING = 24 / 1024
    ThreadingHTTPServer(('127.0.0.1', 8770), Proofs).serve_forever()

