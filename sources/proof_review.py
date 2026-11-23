"""Serve the Virtua Grotesk review index after running make proofs."""

from argparse import ArgumentParser
from functools import partial
from html import escape
import json
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
README_IMAGES = [p for folder in ('article', 'readme-images')
                 for p in (OUTPUT.parent / 'documentation' / folder).glob('*')
                 if p.suffix in ('.svg', '.png')]
REV = OUTPUT / 'onboarding-review'
SHEETS = REV / 'Review-sheets'
ZIP = REV / 'Reference-proofs.zip'

PROOF = OUTPUT / 'proof' / 'proof.pdf'
SCRIPTS = ('Latin', 'Arabic', 'Hebrew')
PROOF_NAMES = {'print-proof.pdf': 'Print Proof', 'full-proof.pdf': 'Full Proof'}
GRID_PROOFS = {'print-proof-grid.pdf': 'Print Proof with red grid',
               'full-proof-grid.pdf': 'Full Proof with red grid'}
PLOTTER = OUTPUT / 'media' / '.build' / 'plotter.rs'
PLOT = PLOTTER.with_name('proof.pdf.plot')
DESIGNBOT = OUTPUT.parent / '.venv' / 'bin' / 'designbot'
proof_lock = Lock()
proof_revision = None
COLUMNS = (69, 309, 549)
COLUMN_WIDTH = 224
def right_label(font, y, text):
    size = 12
    end = COLUMNS[-1] + COLUMN_WIDTH
    ink_right = font.measure(text, 400, size=size)[2]
    return proof_text(end - size * ink_right, y, size, 400, text)


def proof_text(x, y, size, weight, text, opsz=None):
    if opsz is None:
        opsz = size
    return f'text\t{x}\t{y}\t{size}\t{weight},opsz={opsz}\t0\t0\t0\t255\t\t{text}'


def proof_rule(y, left=69, right=773):
    # Regular H has an 88-unit crossbar at 1024 UPM, or 1.03125 pt at 12 pt.
    return f'line\t{left}\t{y}\t{right}\t{y}\t1.03125\t0\t0\t0\t255'


def cover_title(font, weight, title_top, unit):
    title = font.family
    _, ink_left, ink_right = font.measure(title, weight, size=144 / font.scale)
    size = (COLUMNS[-1] + COLUMN_WIDTH - COLUMNS[0]) / (ink_right - ink_left)
    # Align the cap height to the nearest grid line, with a unit on either side.
    baseline = title_top - unit - unit * round(size * 0.75 / unit)
    return baseline, proof_text(COLUMNS[0] - size * ink_left, baseline, size, weight, title, opsz=144)


def cover(font, facts, weights, stamp):
    left, middle, right = COLUMNS
    unit = 8
    header_baseline = 521.5 - 2 * unit
    yield proof_text(left, header_baseline, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, header_baseline, 12, 400, stamp)
    yield right_label(font, header_baseline, 'github.com/eliheuer/virtua-grotesk')
    title_top = header_baseline - unit
    yield proof_rule(title_top)
    baseline, title_row = cover_title(font, 400, title_top, unit)
    yield title_row
    baseline, title_row = cover_title(font, 700, baseline, unit)
    yield title_row

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
    top = baseline - unit
    leading = 2 * unit
    for heading, rows in bands:
        yield proof_rule(top)
        first = top - 2 * unit
        yield proof_text(left, first, 12, 400, heading)
        for row, (label, value) in enumerate(rows):
            y = first - row * leading
            yield proof_text(middle, y, 12, 400, label)
            yield right_label(font, y, value)
        top = first - (len(rows) - 1) * leading - unit


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
        widths = (font.measure(line, weight, size=size) for line in pair)
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


def reading_page(font, script, style, weight, text, guides):
    left, middle, right = COLUMNS
    rtl = script in ('Arabic', 'Hebrew')
    # Stacked Arabic marks in Black span 2.19 em from highest to lowest ink.
    leading = {8: 18, 16: 36} if script == 'Arabic' else {8: 10, 16: 20}
    sizes = (16, 8) if rtl else (8, 16)
    settings = ' · '.join(f'{size}/{leading[size]} pt' for size in sizes)
    yield proof_text(left, 497.5, 12, 400, 'Virtua Grotesk')
    yield proof_text(middle, 497.5, 12, 400, f'{script} · {style} {weight:g}')
    yield right_label(font, 497.5, settings)
    yield proof_rule(489.5)
    band_height = 208

    end = right + COLUMN_WIDTH
    narrow = (right, end) if rtl else (left, left + COLUMN_WIDTH)
    wide = (left, middle + COLUMN_WIDTH) if rtl else (middle, end)
    for size, baseline, (x_min, x_max) in [(8, 457.5, narrow), (16, 453.5, wide)]:
        measure = x_max - x_min
        start = x_max if rtl else x_min
        if script == 'Arabic':
            baseline -= size / 2
        room = int((baseline - 293.5) // leading[size]) + 1
        for i, pair in enumerate(paired_lines(font, script, text, measure, size, weight, room)):
            for band, line in enumerate(pair):
                x = start - font.measure(line, weight, size=size)[2] * size if rtl else start
                y = baseline - i * leading[size] - band * band_height
                guides.append((x_min, x_max, y))
                yield proof_text(f'{x:g}', y, size, f'{weight:g}', line)


def grid_lines(baselines, screen=False):
    tint = '28\t8\t8' if screen else '255\t247\t247'
    rule = '94\t37\t37' if screen else '244\t191\t191'
    left, _, right = COLUMNS
    end = right + COLUMN_WIDTH
    bottom, top = 73.5, 521.5
    if baselines is not None:
        for x in COLUMNS:
            yield f'rect\t{x}\t{bottom}\t{COLUMN_WIDTH}\t{top-bottom}\t{tint}\t255'
        minor = '58\t25\t25' if screen else '249\t221\t221'
        major = '88\t37\t37' if screen else '236\t185\t185'
        baseline = '156\t65\t65' if screen else '201\t110\t110'
        for offset in range(8, int(end - left), 8):
            color, width = (major, 0.4) if offset % 32 == 0 else (minor, 0.25)
            x = left + offset
            yield f'line\t{x}\t{bottom}\t{x}\t{top}\t{width}\t{color}\t255'
        for offset in range(8, int(top - bottom), 8):
            color, width = (major, 0.4) if offset % 32 == 0 else (minor, 0.25)
            y = bottom + offset
            yield f'line\t{left}\t{y}\t{end}\t{y}\t{width}\t{color}\t255'
        for x1, x2, y in baselines:
            if (y - bottom) % 2:
                raise ValueError(f'Proof baseline at {y} falls outside the 2 pt grid')
            yield f'line\t{x1}\t{y}\t{x2}\t{y}\t0.45\t{baseline}\t255'
    for x in (left, end):
        yield f'line\t{x}\t{bottom}\t{x}\t{top}\t0.5\t{rule}\t255'
    for y in (bottom, top):
        yield f'line\t{left}\t{y}\t{end}\t{y}\t0.5\t{rule}\t255'


def proof_content():
    canvas, font_row, _, *lines = PLOT.read_text().splitlines()
    layout = project.load(OUTPUT.parent)
    font, facts = media.font_type(layout)
    if Path(font_row.split('\t')[1]) != font.path:
        raise ValueError('Run make proofs to update the detail pages for the current font.')
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
    # Cover text occupies one column, except for the full-width family name.
    cover_guides = []
    for row in print_pages[0]:
        fields = row.split('\t')
        if fields[0] == 'text':
            x, y, size = map(float, fields[1:4])
            left = COLUMNS[0] if size != 12 else max(col for col in COLUMNS if col <= x + 1)
            end = COLUMNS[-1] + COLUMN_WIDTH if size != 12 else left + COLUMN_WIDTH
            cover_guides.append((left, end, y))
    page_guides = [cover_guides]
    samples, _ = proof_samples.read(layout.sources)
    for script in SCRIPTS:
        paragraphs = samples['text'][f'{script.lower()}-reading-marks']['paragraphs']
        text = ' '.join(paragraph['text'] for paragraph in paragraphs)
        if not all(font.covers(t.replace(' ', '')) for t in (text, without_reading_marks(text, script))):
            raise ValueError(f'The built font cannot set the {script} reading sample.')
        text = ' '.join([text] * 4)
        for weight, style in weights:
            guides = [(x, x + COLUMN_WIDTH, 497.5) for x in COLUMNS]
            print_pages.append(tuple(reading_page(font, script, style, weight, text, guides)))
            page_guides.append(guides)
    return canvas, font_row, print_pages, page_guides, replaced


def draw_proof(folder, name, canvas, font, rows):
    result = folder / name
    plot = result.with_suffix('.plot')
    plot.write_text('\n'.join([canvas, font, f'output\t{result}', *rows]) + '\n')
    run([str(DESIGNBOT), str(PLOTTER), '--', f'plot={plot}'], check=True)
    return result


def screen_rows(rows):
    for row in rows:
        fields = row.split('\t')
        command = fields[0]
        color = {'page': 2, 'text': 5, 'line': 6}.get(command)
        if color is None:
            raise ValueError(f'Unsupported Full Proof drawing command: {command}')
        fields[color:color + 3] = ['0' if command == 'page' else '255'] * 3
        yield '\t'.join(fields)


def prepare_proofs():
    global proof_revision
    with proof_lock:
        revision = (PROOF.stat().st_mtime_ns, PLOT.stat().st_mtime_ns)
        names = (*PROOF_NAMES, *GRID_PROOFS)
        if revision == proof_revision and all(PROOF.with_name(n).exists() for n in names):
            return
        with TemporaryDirectory(dir=PROOF.parent) as work:
            folder = Path(work)
            canvas, font, print_pages, page_guides, replaced = proof_content()
            page_start = 'page\t0\t255\t255\t255'
            # Both editions use this page sequence. Print stops after the reading pages.
            pages = [(page_start, *page) for page in print_pages]
            print_count = len(pages)
            page_number = 0
            for row in PLOT.read_text().splitlines()[3:]:
                if row.startswith('page\t'):
                    page_number += 1
                    if page_number not in replaced:
                        pages.append([])
                if page_number and page_number not in replaced:
                    pages[-1].append(row)

            results = []
            for filename in (*PROOF_NAMES, *GRID_PROOFS):
                screen = filename.startswith('full-')
                grid = filename in GRID_PROOFS
                rows = []
                for i, page in enumerate(pages if screen else pages[:print_count]):
                    start, *content = screen_rows(page) if screen else page
                    rows.append(start)
                    if grid:
                        guides = page_guides[i] if i < print_count else None
                        rows.extend(grid_lines(guides, screen=screen))
                    rows.extend(content)
                results.append(draw_proof(folder, filename, canvas, font, rows))
            for result in results:
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

def social_media_sections():
    clip_dir = OUTPUT / 'x'
    clips = []
    for script in sorted((OUTPUT.parent / 'documentation/media/x/animations').glob('*.rs')):
        title = script.stem.replace('-', ' ').title()
        for suffix, label in [('', title + ' · Clean'), ('-grid', title + ' · Red Grid'), ('-crt', title + ' · CRT')]:
            path = clip_dir / f'{script.stem}{suffix}.mp4'
            if path.is_file():
                clips.append((path, label))
    if clips:
        yield ('<details open id="x-animations"><summary>X Animations</summary><div class="grid posts">' +
               ''.join(f'<article><video controls loop playsinline muted preload="metadata" src="/x/{path.name}"></video>'
                       f'{link(path, title)}</article>' for path, title in clips) + '</div></details>')
    groups = {
        'Instagram Carousels': ('carousel', {'portrait', 'square'}),
        'Instagram Animations': ('video', {'vertical', 'portrait', 'square'}),
        'X Images': ('image', {'landscape', 'card'}),
        'Instagram Images': ('image', {'portrait', 'square', 'vertical'}),
    }
    records = [(path.parent, json.loads(path.read_text()))
               for path in sorted((OUTPUT / 'media').glob('*/*/*.json'))]
    for title, (kind, canvases) in groups.items():
        items = []
        for directory, record in records:
            if record['kind'] != kind or record['canvas'] not in canvases:
                continue
            files = [directory / name for name in record['files']]
            if not files or not all(path.is_file() for path in files):
                continue
            first = '/' + quote(files[0].relative_to(OUTPUT).as_posix())
            label = escape(record['format'].replace('-', ' ').title())
            if files[0].stem.endswith('_lattice'):
                label += ' With Grid'
            size = f"{record['width']} × {record['height']}"
            alt = escape(record.get('alt', ''))
            preview = (f'<video controls playsinline muted preload="metadata" aria-label="{alt}" src="{first}"></video>'
                       if kind == 'video' else f'<a href="{first}"><img loading="lazy" alt="{alt}" src="{first}"></a>')
            if kind == 'carousel':
                assets = ' · '.join(link(path, 'PDF' if path.suffix == '.pdf' else str(i))
                                    for i, path in enumerate(files, 1))
            else:
                assets = link(files[0], 'Open file')
            items.append(f'<article>{preview}<strong>{label}</strong><small>{size}</small>'
                         f'<div>{assets}</div><p>{escape(record.get("caption", ""))}</p></article>')
        if items:
            yield f'<details><summary>{title}</summary><div class="grid posts">{"".join(items)}</div></details>'


def index():
    parts = ["""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Virtua Grotesk Proofs</title>
<style>
@font-face { font-family: Virtua; src: url('/virtua.ttf') format('truetype'); font-weight: 100 900; }
:root { color-scheme: dark; background: #171717; color: #f4f4f4; }
body { max-width: 960px; margin: 48px auto; padding: 0 24px; font: 18px/1.45 Virtua, sans-serif; }
h1 { font-size: clamp(32px, 6vw, 56px); font-weight: 400; }
a { color: inherit; text-underline-offset: .18em; }
nav { display: grid; grid-template-columns: auto auto; justify-content: start; gap: 12px 32px; margin-bottom: 32px; }
details { border-top: 1px solid #555; padding: 12px 0; }
summary { cursor: pointer; }
.grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(180px,1fr)); gap: 16px; }
.grid img { display: block; width: 100%; height: 116px; object-fit: contain; }
.posts { margin: 16px 0; grid-template-columns: repeat(auto-fit,minmax(min(100%,230px),1fr)); }
.posts img, .posts video { width: 100%; height: 180px; object-fit: contain; background: #111; }
.posts strong, .posts small { display: block; }
.posts small, .posts p { font-size: 15px; color: #ccc; }
</style><main><h1>Virtua Grotesk Proofs</h1><nav aria-label="Proof PDFs">"""]
    for name, title in PROOF_NAMES.items():
        grid = name.replace('.pdf', '-grid.pdf')
        parts.append(link(PROOF.with_name(name), title))
        parts.append(link(PROOF.with_name(grid), title + ' With Grid'))
    parts.append('</nav>')
    reports = sorted((OUTPUT / 'diff').glob('*/diffenator.html'))
    if reports:
        parts.append('<h2>Diffenator comparisons</h2><ul>')
        for report in reports:
            style = report.parent.name.removeprefix('VirtuaGrotesk-')
            if style.startswith('VirtuaGrotesk[') and style.endswith(']'):
                style = 'Variable font'
            parts.append('<li>'+link(report,style)+'</li>')
        parts.append('</ul>')
    parts.extend(social_media_sections())
    readme = OUTPUT.parent / 'README.md'
    for path in README_IMAGES:
        if path.is_file() and str(path.relative_to(OUTPUT.parent)) in readme.read_text():
            url = '/readme/' + quote(path.name)
            parts.append(f'<p><a href="{url}">{escape(path.stem.replace("-", " ").title())} (README)</a></p>')
    renders = sorted((OUTPUT / 'render').glob('*.png'))
    if renders:
        parts.append('<details><summary>Glyph Comparisons</summary><div class="grid">')
        parts.extend(link(path, thumb=True) for path in renders)
        parts.append('</div></details>')
    sheets = sorted(SHEETS.glob('*.png'))
    for title,prefixes in [('Latin',('Latin-',)),('Hebrew',('Hebrew-',)),('Arabic, Persian and numerals',('Arabic-','Persian-','Urdu-','Numerals-'))]:
        if not any(p.name.startswith(prefixes) for p in sheets):
            continue
        parts.append(f'<details><summary>{title} proof sheets</summary><div class="grid">')
        parts.extend(link(p,thumb=True) for p in sheets if p.name.startswith(prefixes))
        parts.append('</div></details>')
    if ZIP.is_file():
        parts.append('<details><summary>Reference font PDFs</summary><ul>')
        with ZipFile(ZIP) as z:
            for n in sorted(z.namelist()):
                if n.endswith('.pdf'):parts.append(f'<li><a href="/reference/{quote(n)}">{escape(n[:-4].replace("-"," "))}</a></li>')
        parts.append('</ul></details>')
    return ''.join(parts) + '</main></html>'

class Proofs(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(OUTPUT),**kwargs)
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path=='/':
            data=index().encode();kind='text/html; charset=utf-8'
        elif path.startswith('/readme/'):
            image = next((p for p in README_IMAGES if path == '/readme/' + p.name), None)
            if image is None:
                return self.send_error(404)
            data = image.read_bytes()
            kind = self.guess_type(str(image))
        elif path == '/virtua.ttf':
            font = next((OUTPUT.parent / 'fonts' / 'variable').glob('VirtuaGrotesk*.ttf'), None)
            if font is None:
                return self.send_error(404)
            data = font.read_bytes()
            kind = 'font/ttf'
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
    parser.add_argument('--build-proof', nargs='*', help='Build the source proof or the named pages.')
    args = parser.parse_args()
    if args.build_proof is not None:
        with patch.object(media, 'compose', partial(compose_proof, media.compose)):
            media.main(['--proof', *args.build_proof])
        prepare_proofs()
        print("Review index: http://127.0.0.1:8770/")
        raise SystemExit
    ThreadingHTTPServer(('127.0.0.1', 8770), Proofs).serve_forever()

