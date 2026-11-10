#!/usr/bin/env python3
"""Serve the live comparison proof of Virtua Grotesk and reference-fonts/ on localhost.

By default the proof uses the current build in fonts/. --snapshot selects a
prepared Before/Working snapshot instead and remembers it in out/.
"""
import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import threading
sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))
from reference_fonts import prepare_live
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / 'out/live-proof-selection.json'
CURRENT_FONT = ROOT / 'fonts/variable/VirtuaGrotesk[wght].ttf'
CURRENT_SNAPSHOT = ROOT / 'out/proof-current'


def selected_snapshot(requested=None):
    if requested is not None:
        return requested.resolve()
    if SELECTION.exists():
        return (ROOT / json.loads(SELECTION.read_text())['snapshot']).resolve()
    raise SystemExit('No remembered snapshot. Pass --current or --snapshot <prepared-directory>.')


def prepare_current(font=CURRENT_FONT, target=CURRENT_SNAPSHOT):
    """Prepare a current-only snapshot from the built variable font."""
    if not font.is_file():
        raise SystemExit(f'Missing {font.relative_to(ROOT)}. Run make build first.')
    revision = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip() or 'unknown'
    dirty = subprocess.run(['git', 'status', '--porcelain', '--', 'sources'], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    note = f'Built from sources at {revision}' + (' with uncommitted source changes' if dirty else '')
    target.mkdir(parents=True, exist_ok=True)
    evidence = target / 'evidence.json'
    evidence.write_text(json.dumps({
        'study': {'id': 'Current build', 'status': 'Current build', 'note': note},
        'fonts': {'after': {'family': 'Virtua Grotesk', 'label': 'Current', 'path': str(font),
                            'sha256': hashlib.sha256(font.read_bytes()).hexdigest()}},
    }, indent=2) + '\n')
    snapshot = target / 'snapshot'
    subprocess.run([sys.executable, str(ROOT / 'scripts/proof-web/app/prepare.py'), '--evidence', str(evidence),
                    '--output-dir', str(snapshot)], check=True, stdout=subprocess.DEVNULL)
    return snapshot


def server_identity(folder, live):
    """Distinguish this server implementation from an older frozen proof."""
    sources = [Path(__file__), ROOT / 'scripts/proof-web/app/reference_fonts.py']
    return dict(project=str(ROOT), directory=str(folder), live=live,
                implementation=hashlib.sha256(b''.join(p.read_bytes() for p in sources)).hexdigest())


def matching_server(url, fonts, identity):
    try:
        with urlopen(url + 'proof-server.json', timeout=2) as response:
            if json.load(response) != identity:
                return False
        with urlopen(url + 'live-fonts.json', timeout=2) as response:
            return json.load(response) == fonts
    except (URLError, OSError, ValueError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, help="Serve a frozen archive explicitly; default uses the current live UI and project references")
    parser.add_argument('--current', action='store_true', help='Compare the current build in fonts/ with reference-fonts/ (make proof-web)')
    parser.add_argument('--snapshot', type=Path, help='Use and remember a prepared Before/Working snapshot for the live proof')
    parser.add_argument('--port', type=int, default=60272)
    parser.add_argument('--check', action='store_true', help='Validate local assets without starting a server')
    args = parser.parse_args()
    if sum(map(bool, (args.directory, args.snapshot, args.current))) > 1:
        parser.error('--directory, --snapshot and --current are mutually exclusive')
    cache = None
    if args.directory:
        folder = args.directory.resolve()
    else:
        folder = ROOT / 'out/live-proof'
        snapshot = prepare_current() if args.current else selected_snapshot(args.snapshot)
        try:
            cache = prepare_live(snapshot, folder, ROOT)
        except (OSError, ValueError, KeyError) as error:
            parser.exit(1, f'Review snapshot unavailable: {error}\n')
    try:
        for name in ['index.html', 'review.css', 'review.js', 'review-data.js', 'fonts/labels.ttf']:
            if not (folder / name).is_file():
                raise ValueError(f'Missing {name}')
        fonts = json.loads((folder / 'live-fonts.json').read_text())
        for role, font in fonts.items():
            for face in font.get('faces', [font]):
                path = (folder / face['url']).resolve()
                if not path.is_relative_to(folder):
                    raise ValueError(f'{role}: font path is outside the review folder')
                if hashlib.sha256(path.read_bytes()).hexdigest() != face['sha256']:
                    raise ValueError(f'{role}: font differs from the recorded snapshot')
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Review assets are not ready: {error}\nRead scripts/proof-web/app/README.md.\nDo not substitute current fonts for missing before/candidate snapshots.\n')
    print(f'Verified {len(fonts)} review font snapshots: {folder}', flush=True)
    if args.snapshot:
        SELECTION.parent.mkdir(parents=True, exist_ok=True)
        temporary = SELECTION.with_suffix('.partial')
        temporary.write_text(json.dumps({'snapshot': str(snapshot.relative_to(ROOT)) if snapshot.is_relative_to(ROOT) else str(snapshot)}) + '\n')
        temporary.replace(SELECTION)
    if args.check:
        return
    if not 1 <= args.port <= 65535:
        parser.error('--port must be between 1 and 65535')
    url = f'http://127.0.0.1:{args.port}/'
    identity = server_identity(folder, cache is not None)
    if matching_server(url, fonts, identity):
        print(f'Existing live review: {url}\nReuse it; no duplicate server started.')
        return
    lock = threading.Lock()
    class Handler(SimpleHTTPRequestHandler):
        def log_request(self, code='-', size='-'):
            if not (self.path.split('?')[0] == '/references.json' and code == 200):
                super().log_request(code, size)
        def end_headers(self):
            self.send_header('Cache-Control', 'no-store')
            super().end_headers()
        def do_GET(self):
            endpoint = self.path.split('?')[0]
            if endpoint == '/proof-server.json':
                data = json.dumps(identity).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif cache is not None and endpoint == '/references.json':
                with lock:
                    data = json.dumps(cache.get()).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                super().do_GET()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(folder)))
    except OSError as error:
        parser.exit(1, f'Could not start the review at {url}: {error}\n'
                    'If this port hosts an older Virtua proof, stop that verified proof process and rerun this command.\n'
                    'Do not stop an unrelated server. Use --port only for an intentional separate review.\n')
    served = 'the current build' if args.current else 'frozen Before/Working'
    print(f'Live review: {url}\nServing {served}; live references follow reference-fonts/. Ctrl-C stops this server.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
