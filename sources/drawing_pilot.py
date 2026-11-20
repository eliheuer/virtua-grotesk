"""Show the selected drawing references and proof a returned glyph."""
import argparse
import hashlib
import plistlib
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.ufoLib.glifLib import readGlyphFromString
from fontTools.pens.recordingPen import RecordingPointPen
from fgtools.render_glyphs import render

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ('Thin', 'Regular', 'Bold', 'Black')
OUTPUT = ROOT / 'output/drawing-pilot'


def brief(weight):
    reference = ROOT / 'sources' / 'drawing-references' / f'DrawingReference-{weight}.ufo'
    donors = plistlib.loads((reference / 'glyphs/contents.plist').read_bytes())
    print(f'{weight} drawing references:', ', '.join(donors))
    rules = (ROOT / 'CONTEXT.md').read_text().splitlines()
    for rule in (1, 5, 6, 13, 14, 16, 17, 18, 48):
        print(next(line for line in rules if line.startswith(f'- R{rule}.')))
    for name, filename in donors.items():
        data = (reference / 'glyphs' / filename).read_bytes()
        print(f'\n{weight} {name} SHA-256 {hashlib.sha256(data).hexdigest()}')
        print(data.decode())


def proof(weight, data=None):
    reference = ROOT / 'sources' / 'drawing-references' / f'DrawingReference-{weight}.ufo'
    donors = plistlib.loads((reference / 'glyphs/contents.plist').read_bytes())
    names = list(donors)
    if data is not None:
        root = ET.fromstring(data)
        name = root.get('name')
        if not name or name in donors or root.find('outline/contour') is None or root.findall('outline/component'):
            raise ValueError('Expected a standalone candidate distinct from the donors')
        readGlyphFromString(data, pointPen=RecordingPointPen())
        names = [name]
    (OUTPUT / weight).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as work:
        folder = Path(work)
        sources = folder / 'sources'
        sources.mkdir()
        ufo = sources / f'VirtuaGrotesk-{weight}.ufo'
        shutil.copytree(ROOT / 'sources' / ufo.name, ufo)
        files = plistlib.loads((ufo / 'glyphs/contents.plist').read_bytes())
        for donor, filename in donors.items():
            shutil.copyfile(reference / 'glyphs' / filename, ufo / 'glyphs' / files[donor])
        if data is not None:
            (ufo / 'glyphs' / files[name]).write_bytes(data)
        (sources / 'config.yaml').write_text(f'sources: [{ufo.name}]\n')
        shutil.copyfile(ROOT / 'CONTEXT.md', folder / 'CONTEXT.md')
        render(names, masters=[weight], beside=list(donors) if data is not None else [], root=folder,
               out=OUTPUT / weight / ('candidate.png' if data is not None else 'references.png'))


def alignment(donor_path, draft_path):
    """Compare corresponding straight segments in compatible masters."""
    donor, draft = (ET.parse(path).getroot() for path in (donor_path, draft_path))
    print(f'Donor {donor_path}  |  draft {draft_path}')
    if donor.get('name') != draft.get('name'):
        raise ValueError('Compare the same glyph in both masters')
    contours = [glyph.findall('outline/contour') for glyph in (donor, draft)]
    if not all(contours):
        raise ValueError('Expected contour glyphs')
    compared = changed = 0
    for index, (original, candidate) in enumerate(zip(*contours, strict=True), 1):
        points = [contour.findall('point') for contour in (original, candidate)]
        if [p.get('type') for p in points[0]] != [p.get('type') for p in points[1]]:
            raise ValueError(f'Point types differ in contour {index}')
        for j, point in enumerate(points[0]):
            if point.get('type') != 'line' or (j == 0 and points[0][0].get('type') == 'move'):
                continue
            for axis, direction in (('x', 'vertical'), ('y', 'horizontal')):
                previous = points[0][j - 1]
                if float(point.get(axis)) != float(previous.get(axis)):
                    continue
                compared += 1
                start, end = points[1][j - 1], points[1][j]
                drift = float(end.get(axis)) - float(start.get(axis))
                if drift:
                    changed += 1
                    print(f'Contour {index}, ({start.get("x")},{start.get("y")}) to '
                          f'({end.get("x")},{end.get("y")}): donor {direction}, '
                          f'draft {axis} drift {drift:+g} units')
    print(f'{changed} direction changes across {compared} donor-aligned edges.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weight', choices=WEIGHTS, default='Regular')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('brief')
    commands.add_parser('references')
    commands.add_parser('proof').add_argument('candidate', type=Path)
    compare = commands.add_parser('alignment')
    compare.add_argument('donor', type=Path)
    compare.add_argument('draft', type=Path)
    args = parser.parse_args()
    if args.command == 'alignment':
        alignment(args.donor, args.draft)
    elif args.command == 'brief':
        brief(args.weight)
    elif args.command == 'references':
        proof(args.weight)
    else:
        proof(args.weight, args.candidate.read_bytes())
