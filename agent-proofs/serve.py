#!/usr/bin/env python3
"""Validate and serve the current live design-review snapshot on localhost."""
import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / 'agent-proofs/cases/arabic-006/batches/03-noon/working'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=CURRENT)
    parser.add_argument('--port', type=int, default=60272)
    parser.add_argument('--check', action='store_true', help='Validate local assets without starting a server')
    args = parser.parse_args()
    folder = args.directory.resolve()
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
    if args.check:
        return
    if not 1 <= args.port <= 65535:
        parser.error('--port must be between 1 and 65535')
    url = f'http://127.0.0.1:{args.port}/'
    try:
        with urlopen(url + 'live-fonts.json', timeout=2) as response:
            remote_fonts = json.load(response)
        with urlopen(url, timeout=2) as response:
            page = response.read().decode('utf-8')
        if remote_fonts == fonts and 'Virtua Grotesk — Live Review' in page:
            print(f'Existing live review: {url}\nReuse it; no duplicate server started.')
            return
    except (URLError, OSError, ValueError):
        pass
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(SimpleHTTPRequestHandler, directory=str(folder)))
    except OSError as error:
        parser.exit(1, f'Could not start the review: {error}\nUse --port with another free port; do not stop an unrelated server.\n')
    print(f'Live review: {url}\nServing the frozen review; this command does not rebuild fonts. Ctrl-C stops this server.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
