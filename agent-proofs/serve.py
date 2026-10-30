#!/usr/bin/env python3
"""Validate and serve the current live design-review snapshot on localhost."""
import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading
sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))
from reference_fonts import prepare_live
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'design/reviews/current.json'
SELECTION = ROOT / 'out/live-proof-selection.json'


def selected_snapshot(requested=None):
    if requested is not None:
        return requested.resolve()
    if SELECTION.exists():
        return (ROOT / json.loads(SELECTION.read_text())['snapshot']).resolve()
    return (ROOT / json.loads(STATE.read_text())['proof_snapshot']).resolve()


def server_identity(folder, live):
    """Distinguish this server implementation from an older frozen proof."""
    sources = [Path(__file__), ROOT / 'agent-proofs/app/reference_fonts.py']
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
    parser.add_argument('--snapshot', type=Path, help='Use and remember a prepared Before/Working snapshot for the live proof')
    parser.add_argument('--port', type=int, default=60272)
    parser.add_argument('--check', action='store_true', help='Validate local assets without starting a server')
    args = parser.parse_args()
    if args.directory and args.snapshot:
        parser.error('--directory and --snapshot are mutually exclusive')
    cache = None
    if args.directory:
        folder = args.directory.resolve()
    else:
        folder = ROOT / 'out/live-proof'
        snapshot = selected_snapshot(args.snapshot)
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
        parser.exit(1, f'Review assets are not ready: {error}\nRead agent-proofs/app/README.md.\nDo not substitute current fonts for missing before/candidate snapshots.\n')
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
    print(f'Live review: {url}\nServing frozen Before/Working; live references follow reference-fonts/. This command does not rebuild fonts. Ctrl-C stops this server.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
